from sqliteorm.model_base import ORMBase,ModelManagerBase
from sqliteorm.sqlite_backend import SqliteBackendBase
from sqliteorm.orm_exceptions import TableCreationError

class CustomManager(ModelManagerBase):
    def __init__(self) -> None:
        super().__init__()

class SqliteBackend(SqliteBackendBase):
    def __init__(self, db_path=None) -> None:
        super().__init__(db_path="C:/Users/GuestUser/Documents/quickfox/orm_test/sqlite_orm_o/test_sqlite.db")
 
class TestModel(ORMBase):
    table_name = "rkp_test_table"
    objects = CustomManager()
    db = SqliteBackend().get_db

    def __init__(self) -> None:
        super().__init__()

    

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


tets = TestModel()
tets.create_table()
tets.objects.create(name="a")

# from models import TestModel

# base = ORMBase()
# test = TestModel()
# print(test.objects.table_name)
# test.objects.create_table()

# name_list = [
#     {"name":"rkp_normal-01"},
#     {"name":"bkt_normal-02"},
#     {"name":"rkp_normal-03"},
#     {"name":"rkp_normal-04"},
#     {"name":"rkp_normal-05"},
#     {"name":"rkp_normal-06"}
#     ]

# """
# NORMAL
# """
# for count,data in enumerate(name_list):
#     test.objects.create(**data)

# """
# WITH TRANSACTION
# """
# try:
#     with test.atomic():
#         for count,data in enumerate(name_list):
#             print(data)
#             test.objects.create(**data)
# except Exception as e:
#     print(e)
#     test.rollback()



# class BaseMeta(type):
#     def __new__(cls, name, bases, attrs):
#     obj = attrs.get('obj')
#     obj.model = 'New'
#     return super().__new__(cls, name, bases, attrs)

# class Manager():

#     def __init__(self,model) -> None:
#         self.model=model
#         print("from meta+++")
#         print("printed model in set from meta", self.model)


# class BaseModel(metaclass=BaseMeta):
#     def __init__(self) -> None:
#         print("init in base model")
#     obj = Manager()

#     print(BaseModel())
