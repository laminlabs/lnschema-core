from lndb_schema_core import ExampleClass, example_function


def test_dummy():
    assert example_function("A") == "a"
    ex = ExampleClass(1)
    assert ex.bar() == "hello"
