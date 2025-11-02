"""Type system for validators."""

from typing import Any, Optional, List
from enum import Enum


class DataType(Enum):
    """Supported data types."""
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    DATE = "date"
    DATETIME = "datetime"
    LIST = "list"
    DICT = "dict"


class ValidationError:
    """Represents a validation error."""
    
    def __init__(
        self, 
        field: str, 
        value: Any, 
        message: str, 
        row: Optional[int] = None
    ):
        self.field = field
        self.value = value
        self.message = message
        self.row = row
    
    def __str__(self):
        if self.row is not None:
            return f"Row {self.row}, Field '{self.field}': {self.message}"
        return f"Field '{self.field}': {self.message}"
    
    def __repr__(self):
        return f"ValidationError(field={self.field}, row={self.row}, message={self.message})"
    
    def to_dict(self):
        return {
            "field": self.field,
            "value": str(self.value)[:100],
            "message": self.message,
            "row": self.row
        }


class ValidationResult:
    """Result of validation."""
    
    def __init__(
        self, 
        valid: bool, 
        errors: Optional[List[ValidationError]] = None,
        records_validated: int = 0
    ):
        self.valid = valid
        self.errors = errors or []
        self.records_validated = records_validated
    
    def __str__(self):
        if self.valid:
            return f"✓ Valid ({self.records_validated} records)"
        return f"✗ Invalid ({len(self.errors)} errors)"
    
    def to_dict(self):
        return {
            "valid": self.valid,
            "records_validated": self.records_validated,
            "error_count": len(self.errors),
            "errors": [e.to_dict() for e in self.errors]
        }
    
    def summary(self):
        """Return a human-readable summary."""
        if self.valid:
            return f"✓ All {self.records_validated} records valid"
        return f"✗ {len(self.errors)} error(s) in {self.records_validated} records"
