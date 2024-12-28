## Basic ORM for sqlite database specially designed for RPA based tools

## Usage example
```py
from sqliteorm.model_base import ORMBase

class TestModel(ORMBase):
    table_name = "users"

# create object of model
tets = TestModel()
# create table
tets.create_table()


# bulk insersion normal mode
name_list = [
    {"name":"rkp_normal-01"},
    {"name":"bkt_normal-02"},
    {"name":"rkp_normal-03"},
    {"name":"rkp_normal-04"},
    {"name":"rkp_normal-05"},
    {"name":"rkp_normal-06"}
]

for count,data in enumerate(name_list):
    test.objects.create(**data)

# bulk insersion with transaction
try:
    with test.atomic():
        for count,data in enumerate(name_list):
            test.objects.create(**data)
except Exception as e:
    test.rollback()

### Other available options
# test.all()
# test.get({"name": "roshan", "email": "rkp@gmail.com"})
# test.filter({"name": "roshan", "email": "rkp@gmail.com"})
# test.update({"name": "roshan", "email": "rkp@gmail.com"})
```

## Inspired by Django ORM