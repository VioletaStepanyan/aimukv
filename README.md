# ukv.rocksdb: python wrapper for rocksdb

`ukv.rocksdb` is a python package written by python C bindings.

It uses statically linked libraries for rocksdb and compression libraries it depends on, 
so `ukv.rocksdb` can be used out of the box (without requiring additional installation of any of those).

### Example usage

```python
import ukv.rocksdb as ukv

db_path = '/tmp/example_db'
db = ukv.DataBase(db_path)

db.main.set(1, b'value_1')
db.main.set(2, b'value_1')

...

value = db.main.get(1)
values = db.main.get((1, 2))

...

db.close()

```
