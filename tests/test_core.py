"""Tests for core validation engine."""

import pytest
from pipeval import Schema, Field, DataType, Validators


def test_basic_validation():
    """Test basic field validation."""
    schema = Schema([
        Field("name", DataType.STRING, required=True),
        Field("age", DataType.INTEGER),
    ])
    
    record = {"name": "John", "age": 30}
    errors, converted = schema.validate_record(record)
    assert len(errors) == 0


def test_required_field():
    """Test required field validation."""
    schema = Schema([
        Field("email", DataType.STRING, required=True),
    ])
    
    record = {"email": ""}
    errors, _ = schema.validate_record(record)
    assert len(errors) == 1
    assert "Required" in errors[0].message


def test_type_conversion():
    """Test type conversion."""
    schema = Schema([
        Field("count", DataType.INTEGER),
        Field("price", DataType.FLOAT),
    ])
    
    record = {"count": "42", "price": "19.99"}
    errors, converted = schema.validate_record(record)
    assert len(errors) == 0
    assert converted["count"] == 42
    assert converted["price"] == 19.99


def test_custom_validators():
    """Test custom validators."""
    schema = Schema([
        Field("email", DataType.STRING, validators=[Validators.email()]),
        Field("age", DataType.INTEGER, validators=[Validators.range_check(0, 150)]),
    ])
    
    # Valid record
    record = {"email": "test@example.com", "age": 25}
    errors, _ = schema.validate_record(record)
    assert len(errors) == 0
    
    # Invalid email
    record = {"email": "invalid", "age": 25}
    errors, _ = schema.validate_record(record)
    assert len(errors) == 1
    
    # Invalid age
    record = {"email": "test@example.com", "age": 200}
    errors, _ = schema.validate_record(record)
    assert len(errors) == 1


def test_batch_validation():
    """Test validating multiple records."""
    schema = Schema([
        Field("id", DataType.INTEGER, required=True),
        Field("status", DataType.STRING, validators=[Validators.one_of(["active", "inactive"])]),
    ])
    
    records = [
        {"id": 1, "status": "active"},
        {"id": 2, "status": "pending"},  # Invalid
        {"id": "", "status": "active"},  # Invalid
    ]
    
    result = schema.validate_batch(records)
    assert not result.valid
    assert len(result.errors) == 2
    assert result.records_validated == 3


def test_boolean_conversion():
    """Test boolean type conversion."""
    schema = Schema([
        Field("active", DataType.BOOLEAN),
    ])
    
    # Test various truthy values
    for val in ["true", "1", "yes", "True", "YES"]:
        record = {"active": val}
        errors, converted = schema.validate_record(record)
        assert len(errors) == 0
        assert converted["active"] is True
    
    # Test various falsy values
    for val in ["false", "0", "no", "False", "NO"]:
        record = {"active": val}
        errors, converted = schema.validate_record(record)
        assert len(errors) == 0
        assert converted["active"] is False


def test_string_length_validators():
    """Test string length validators."""
    schema = Schema([
        Field("username", DataType.STRING, validators=[
            Validators.min_length(3),
            Validators.max_length(20)
        ]),
    ])
    
    # Valid
    record = {"username": "john"}
    errors, _ = schema.validate_record(record)
    assert len(errors) == 0
    
    # Too short
    record = {"username": "ab"}
    errors, _ = schema.validate_record(record)
    assert len(errors) == 1
    
    # Too long
    record = {"username": "a" * 25}
    errors, _ = schema.validate_record(record)
    assert len(errors) == 1


def test_validation_result_summary():
    """Test ValidationResult summary."""
    schema = Schema([
        Field("id", DataType.INTEGER, required=True),
    ])
    
    result = schema.validate_batch([{"id": 1}])
    assert result.valid
    assert "Valid" in result.summary()
    
    result = schema.validate_batch([{"id": ""}])
    assert not result.valid
    assert "Invalid" in result.summary()


def test_schema_export():
    """Test schema export to dict."""
    schema = Schema([
        Field("id", DataType.INTEGER, required=True),
        Field("name", DataType.STRING),
    ])
    
    schema_dict = schema.to_dict()
    assert len(schema_dict["fields"]) == 2
    assert schema_dict["fields"][0]["name"] == "id"
    assert schema_dict["fields"][0]["required"] is True
