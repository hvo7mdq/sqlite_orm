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
