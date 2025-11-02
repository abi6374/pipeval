"""Tests for file readers."""

import json
import csv
import tempfile
from pathlib import Path

import pytest
from pipeval import Schema, Field, DataType, Validators
from pipeval.readers import FileReader, FileValidator


@pytest.fixture
def temp_json_file():
    """Create temporary JSON file."""
    data = [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"},
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(data, f)
        temp_path = f.name
    
    yield temp_path
    Path(temp_path).unlink()


@pytest.fixture
def temp_csv_file():
    """Create temporary CSV file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'name', 'email'])
        writer.writeheader()
        writer.writerow({'id': '1', 'name': 'Alice', 'email': 'alice@example.com'})
        writer.writerow({'id': '2', 'name': 'Bob', 'email': 'bob@example.com'})
        temp_path = f.name
    
    yield temp_path
    Path(temp_path).unlink()


def test_read_json(temp_json_file):
    """Test reading JSON file."""
    records = FileReader.read_json(temp_json_file)
    assert len(records) == 2
    assert records[0]['name'] == 'Alice'


def test_read_csv(temp_csv_file):
    """Test reading CSV file."""
    records = FileReader.read_csv(temp_csv_file)
    assert len(records) == 2
    assert records[0]['name'] == 'Alice'


def test_read_json_not_found():
    """Test error when JSON file not found."""
    with pytest.raises(FileNotFoundError):
        FileReader.read_json('nonexistent.json')


def test_read_csv_not_found():
    """Test error when CSV file not found."""
    with pytest.raises(FileNotFoundError):
        FileReader.read_csv('nonexistent.csv')


def test_validate_json_file(temp_json_file):
    """Test validating JSON file."""
    schema = Schema([
        Field("id", DataType.INTEGER, required=True),
        Field("name", DataType.STRING, required=True),
        Field("email", DataType.STRING, validators=[Validators.email()]),
    ])
    
    result = FileValidator.validate_json_file(schema, temp_json_file)
    assert result.valid
    assert result.records_validated == 2


def test_validate_csv_file(temp_csv_file):
    """Test validating CSV file."""
    schema = Schema([
        Field("id", DataType.INTEGER, required=True),
        Field("name", DataType.STRING, required=True),
        Field("email", DataType.STRING, validators=[Validators.email()]),
    ])
    
    result = FileValidator.validate_csv_file(schema, temp_csv_file)
    assert result.valid
    assert result.records_validated == 2


def test_auto_read_json(temp_json_file):
    """Test auto-detect and read JSON."""
    records = FileReader.auto_read(temp_json_file)
    assert len(records) == 2


def test_auto_read_csv(temp_csv_file):
    """Test auto-detect and read CSV."""
    records = FileReader.auto_read(temp_csv_file)
    assert len(records) == 2


def test_auto_read_unsupported():
    """Test error on unsupported file format."""
    with pytest.raises(ValueError):
        FileReader.auto_read('file.txt')
