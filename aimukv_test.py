import pytest
import numpy as np

import unittest

import ukv.rocksdb as ukv

def config()->str:
    config_path = "./config.json"

    with open(config_path, 'r') as file:
        config = file.read().replace('\n', '')
    
    return config

def test_get_none():
    db = ukv.DataBase(config)
    assert not db.main.get(1)

def test_put_get():
    db = ukv.DataBase(config)

    db.main.set(1, b"b")
    assert db.main[1] == b'b'
    db.clear()

def int_to_bytes(ob):
    return str(ob).encode('ascii')

def test_multi_get():
    db = ukv.DataBase(config)

    db.main.set(1, b"1")
    db.main.set(2, b"2")
    db.main.set(3, b"3")

    vals = db.main.get((1, 2, 3))
    assert len(vals) == 3

    targets = [b'1', b'2', b'3']

    for i, v in enumerate(vals):
        assert v.as_py() == targets[i]

    assert list(db.main.items) == [
        (1, b'1'), (2, b'2'), (3, b'3')]
    db.clear()


def test_delete():
    db = ukv.DataBase(config)

    db.main.set(1, b"a")
    assert db.main[1] == b'a'
   
    db.main.pop(1)
    db.main.get(1) != b'a'
    db.clear()

def test_key_may_exists():
    db = ukv.DataBase(config)

    db.main.set(1, b'a')

    assert db.main.has_key(1)

    db.main.set((2, 3), (b'b', b'c'))
    assert db.main.has_key((2, 3)) == (True, True)

    db.main.set((3, 4), None)
    assert db.main.has_key((3, 4)) == (False, False)

    db.clear()

def test_creat_column_family():
    db = ukv.DataBase(config)
    cf_a = db[b'A']
    cf_b = db[b'B']

    families = db.collection_names()
    assert families[1] == b'A'
    assert families[2] == b'B'
    db.clear()

def test_iter_items():
    db = ukv.DataBase(config)
    for x in range(300):
        db.main.set(x, int_to_bytes(x * 1000))

    iterated_items = []
    for item in db.main.items:
        iterated_items.append(item)

    ref = sorted([x for x in range(300)])
    ref = [(x, int_to_bytes(int(x) * 1000)) for x in ref]
    assert iterated_items == ref

    iterated_items.clear()
    for item in db.main.items.since(90):
        iterated_items.append(item)

    ref = [(x, int_to_bytes(x * 1000)) for x in range(90, 300)]
    assert iterated_items == ref
    it = db.main.items.since(90)
    assert ref == list(it)

    db.clear()