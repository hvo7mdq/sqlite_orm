"""
@ARTHUR:rkp
"""
import sqlite3
from sqlite_orm.base.sqlite_base import sqlite
from sqlite_orm.base.orm_exceptions import MultipleValueReturn


class Atomic():
    """
    FOR ATOMIC TRANSACTIONS
    can be used like:
    with dbModel.atomic():
        //do stuff
    """
    
    def __init__(self,cursor) -> None:
        self.cursor = cursor

    def __enter__(self):
       print("inside __enter__")

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            try:
                self.cursor.execute('rollback')
            except Exception as e:
                pass
        try:
            self.cursor.execute("commit")
        except Exception as e:
            pass
        self.cursor.close()

class ModelManagerBase():
    def __init__(self) -> None:
        self.db = None
        self.cursor = None
        self.table_name = None
        self.is_atomic = False

    @staticmethod
    def decode_row_object(obj):
        data = None
        if isinstance(obj, sqlite3.Row):
            data = {}
            keys = obj.keys()
            for key in keys:
                data[key] = obj[key]

        elif isinstance(obj, list):
            data = []
            for raw_data in obj:
                keys = raw_data.keys()
                data_dict = {}
                for key in keys:
                    data_dict[key] = raw_data[key]
                data.append(data_dict)
        return data

    def all(self,**kwargs):
        query = f"SELECT * FROM {self.table_name}"
        selector = self.cursor.execute(query)
        result = selector.fetchall()
        # self.cursor.close()
        data = self.decode_row_object(result)
        # set id as none
        self.id = None
        return data

    def get(self,**kwargs):
        query = f"SELECT * FROM {self.table_name} WHERE "
        counter = 1
        for key,value in kwargs.items():
            if counter == 1:
                query += f"{key}= '{value}' "
            else:
                query += f"AND {key}= '{value}' "
            counter += 1

        selector = self.cursor.execute(query)
        result = selector.fetchall()

        if not result:
            return self

        # self.cursor.close()
        if len(result) > 1:
            raise MultipleValueReturn()
        data = self.decode_row_object(result[0])

        # set instance
        self.instance = data
        return self
    
    def filter(self, **kwargs):
        query = f"SELECT * FROM {self.table_name} WHERE "
        counter = 1
        for key,value in kwargs.items():
            if counter == 1:
                query += f"{key}= '{value}' "
            else:
                query += f"AND {key}= '{value}' "
            counter += 1

        selector = self.cursor.execute(query)
        result = selector.fetchall()
        # self.cursor.close()
        data = self.decode_row_object(result)
        # set id as none
        self.id = None
        return data

    @staticmethod
    def get_key_value(kwargs):
        keys = ""
        values = ""
        counter = 1
        for key, value in kwargs.items():
            if counter == 1:
                keys += f'{key}'
                values += f"'{value}'"
            else:
                keys += f',{key}'
                values += f",'{value}'"
            counter +=1
        return keys,values



    def create(self,**kwargs):
        # RecursiveIndexModel(**kwargs)
        query = f"INSERT INTO {self.table_name} "
        keys,values = self.get_key_value(kwargs)
        query += f"({keys}) VALUES ({values})"
        selector = self.cursor.execute(query)

        if not self.is_atomic:
            id = selector.lastrowid
            self.db.conn.commit()
            data = self.get(id=id)
            #set instance
            self.instance = data
        return self

    def update(self,**kwargs):
        query = f"UPDATE {self.table_name} SET "

        counter = 1
        for key, value in kwargs.items():
            if counter == 1:
                query += f"{key}= '{value}'"
            else:
                query += f",{key}= '{value}'"
            counter += 1

        # get instance
        instance_id = self.instance.get('id')
        query += f" WHERE id = {instance_id}"

        selector = self.cursor.execute(query)
        self.db.conn.commit()

        # set instance
        data = self.get(id=instance_id)
        self.instance = data.instance
        return self

class ORMMETABase(type):
    def __new__(cls, name, bases, attrs):
        objects = attrs.get('objects')
        table_name = attrs.get('table_name')
        if not objects:
            objects = ModelManagerBase()
        objects.table_name = table_name
        objects.db = sqlite()
        objects.cursor = objects.db.conn.cursor() 

        attrs['objects'] = objects
        super_new = super().__new__(cls, name, bases, attrs)
        return super_new

class ORMBase(metaclass=ORMMETABase):
    def __init__(
        self,
        table_name=None,#pass from base class
        db = sqlite(),
        cursor = None, #set when call is invoked
        is_atomic=False,
        ) -> None:

        self.table_name = table_name
        self.db = db
        self.cursor = cursor
        self.is_atomic = is_atomic

    def atomic(self,**kwargs):
        self.is_atomic = True
        self.cursor = self.db.conn.cursor()
        self.objects.is_atomic = True
        return Atomic(cursor=self.cursor)

    def rollback(self):
        try:
            self.cursor.execute("rollback")
        except Exception as e:
            pass

    def check_if_table_exists(self):
        query = f"select * FROM sqlite_master WHERE name = '{self.table_name}' and type = 'table'"
        selector = self.cursor.execute(query)
        status = selector.fetchone()
        return status

    def close_connection(self):
        self.conn.close()

    # @property
    # def objects(self):
    #     self.cursor = self.db.conn.cursor()
    #     return self

    

    # @staticmethod
    # def decode_row_object(obj):
    #     data = None
    #     if isinstance(obj, sqlite3.Row):
    #         data = {}
    #         keys = obj.keys()
    #         for key in keys:
    #             data[key] = obj[key]

    #     elif isinstance(obj, list):
    #         data = []
    #         for raw_data in obj:
    #             keys = raw_data.keys()
    #             data_dict = {}
    #             for key in keys:
    #                 data_dict[key] = raw_data[key]
    #             data.append(data_dict)
    #     return data

    # def all(self,**kwargs):
    #     query = f"SELECT * FROM {self.table_name}"
    #     selector = self.cursor.execute(query)
    #     result = selector.fetchall()
    #     self.cursor.close()
    #     data = self.decode_row_object(result)
    #     # set id as none
    #     self.id = None
    #     return data

    # def get(self,**kwargs):
    #     query = f"SELECT * FROM {self.table_name} WHERE "
    #     counter = 1
    #     for key,value in kwargs.items():
    #         if counter == 1:
    #             query += f"{key}= '{value}' "
    #         else:
    #             query += f"AND {key}= '{value}' "
    #         counter += 1

    #     selector = self.cursor.execute(query)
    #     result = selector.fetchall()

    #     if not result:
    #         return self

    #     # self.cursor.close()
    #     if len(result) > 1:
    #         raise MultipleValueReturn()
    #     data = self.decode_row_object(result[0])

    #     # set instance
    #     self.instance = data
    #     return self
    
    # def filter(self, **kwargs):
    #     query = f"SELECT * FROM {self.table_name} WHERE "
    #     counter = 1
    #     for key,value in kwargs.items():
    #         if counter == 1:
    #             query += f"{key}= '{value}' "
    #         else:
    #             query += f"AND {key}= '{value}' "
    #         counter += 1

    #     selector = self.cursor.execute(query)
    #     result = selector.fetchall()
    #     self.cursor.close()
    #     data = self.decode_row_object(result)
    #     # set id as none
    #     self.id = None
    #     return data

    # @staticmethod
    # def get_key_value(kwargs):
    #     keys = ""
    #     values = ""
    #     counter = 1
    #     for key, value in kwargs.items():
    #         if counter == 1:
    #             keys += f'{key}'
    #             values += f"'{value}'"
    #         else:
    #             keys += f',{key}'
    #             values += f",'{value}'"
    #         counter +=1
    #     return keys,values



    # def create(self,**kwargs):
    #     # RecursiveIndexModel(**kwargs)
    #     query = f"INSERT INTO {self.table_name} "
    #     keys,values = self.get_key_value(kwargs)
    #     query += f"({keys}) VALUES ({values})"
    #     selector = self.cursor.execute(query)

    #     if not self.is_atomic:
    #         id = selector.lastrowid
    #         self.db.conn.commit()
    #         data = self.get(id=id)
    #         #set instance
    #         self.instance = data
    #     return self

    # def update(self,**kwargs):
    #     query = f"UPDATE {self.table_name} SET "

    #     counter = 1
    #     for key, value in kwargs.items():
    #         if counter == 1:
    #             query += f"{key}= '{value}'"
    #         else:
    #             query += f",{key}= '{value}'"
    #         counter += 1

    #     # get instance
    #     instance_id = self.instance.get('id')
    #     query += f" WHERE id = {instance_id}"

    #     selector = self.cursor.execute(query)
    #     self.db.conn.commit()

    #     # set instance
    #     data = self.get(id=instance_id)
    #     self.instance = data.instance
    #     return self