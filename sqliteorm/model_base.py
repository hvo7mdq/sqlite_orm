"""
@ARTHUR:rkp
"""

import sqlite3
from sqliteorm.orm_exceptions import MultipleValueReturn
from sqliteorm.sqlite_backend import SqliteBackendBase
from sqliteorm.orm_exceptions import TableCreationError


class ORMMETABase(type):
    def __new__(cls, name, bases, attrs):
        objects = attrs.get('objects')
        db = attrs.get('db')
        if not db:
            db = SqliteBackendBase('sqlite.db').get_db()
        table_name = attrs.get('table_name')
        if not objects:
            objects = ModelManagerBase()
        objects.table_name = table_name
        objects.db = db
        attrs['objects'] = objects
        attrs['db'] = db
        super_new = super().__new__(cls, name, bases, attrs)
        return super_new


class Atomic():
    """
    FOR ATOMIC TRANSACTIONS
    can be used like:
    with dbModel.atomic():
        //do stuff
    """

    def __init__(self, cursor) -> None:
        self.cursor = cursor

    def __enter__(self):
        print("inside __enter__")

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            try:
                self.cursor.execute('rollback')
            except Exception as e:
                print(e)
                pass
        try:
            self.cursor.execute("commit")
        except Exception as e:
            raise Exception(e)

        self.cursor.close()


class ModelManagerBase():
    def __init__(self) -> None:
        self.db = None
        self.cursor = None
        self.table_name = None
        self.is_atomic = False

    def check_conn(self):
        # check_cursor
        if not self.cursor:
            if self.db:
                self.cursor = self.db().conn.cursor()
            else:
                raise Exception('DB not set in Manager')

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

    def all(self, **kwargs):
        self.check_conn()

        query = f"SELECT * FROM {self.table_name}"
        selector = self.cursor.execute(query)
        result = selector.fetchall()
        # self.cursor.close()
        data = self.decode_row_object(result)
        # set id as none
        self.id = None
        return data

    def get(self, **kwargs):
        self.check_conn()
        query = f"SELECT * FROM {self.table_name} WHERE "
        counter = 1
        for key, value in kwargs.items():
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
        self.check_conn()
        query = f"SELECT * FROM {self.table_name} WHERE "
        counter = 1
        for key, value in kwargs.items():
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
            counter += 1
        return keys, values

    def create(self, **kwargs):
        self.check_conn()
        query = f"INSERT INTO {self.table_name} "
        keys, values = self.get_key_value(kwargs)
        query += f"({keys}) VALUES ({values})"
        selector = self.cursor.execute(query)

        if not self.is_atomic:
            id = selector.lastrowid
            self.db.conn.commit()
            data = self.get(id=id)
            # set instance
            self.instance = data
        return self

    def update(self, **kwargs):
        self.check_conn()
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

        self.cursor.execute(query)
        self.db.conn.commit()

        # set instance
        data = self.get(id=instance_id)
        self.instance = data.instance
        return self


class ORMBase(metaclass=ORMMETABase):
    def __init__(
        self,
        # set when call is invoked
        cursor=None,
        is_atomic=False,
    ) -> None:
        self.cursor = cursor
        self.is_atomic = is_atomic

    def check_conn(self):
        # check_cursor
        if not self.cursor:
            if self.db:
                self.cursor = self.db().conn.cursor()
            else:
                raise Exception('DB not set in ORMBase')

    def create_table(self):

        self.check_conn()

        table_exists = self.check_if_table_exists()
        if not table_exists:
            try:
                # IF NOT EXISTS: creates table if doesnot exist
                # else table creation will ignored
                query = f"CREATE TABLE IF NOT EXISTS {self.table_name}(\
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\
                    name CHAR(100),\
                    created_at CHAR(100) NULL,\
                    updated_at CHAR(100) NULL\
                        )"
                query_status = self.cursor.execute(query)
            except Exception as e:
                print(e)
                raise TableCreationError(e)

        else:
            query_status = None
        return query_status

    def atomic(self, **kwargs):
        self.check_conn()
        self.is_atomic = True
        self.objects.is_atomic = True
        self.objects.cursor = self.cursor
        return Atomic(cursor=self.cursor)

    def rollback(self):
        self.check_conn()
        try:
            self.cursor.execute("rollback")
        except Exception as e:
            print(e)
            pass

    def check_if_table_exists(self):
        query = f"select * FROM sqlite_master WHERE name = '{self.table_name}' and type = 'table'"
        selector = self.cursor.execute(query)
        status = selector.fetchone()
        return status

    def close_connection(self):
        self.conn.close()
