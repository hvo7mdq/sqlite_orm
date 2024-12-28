from sqliteorm.model_base import ORMBase, ModelManagerBase
from sqliteorm.sqlite_backend import SqliteBackendBase


class CustomManager(ModelManagerBase):
    def __init__(self) -> None:
        super().__init__()


class SqliteBackend(SqliteBackendBase):
    def __init__(self, db_path=None) -> None:
        super().__init__(db_path="test_sqlite.db")
 

class TestModel(ORMBase):
    table_name = "rkp_test_table"
    # objects = CustomManager()
    # db = SqliteBackend().get_db


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
