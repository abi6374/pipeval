"""Core validation engine."""

from typing import Any, Dict, List, Optional, Callable
from .types import DataType, ValidationError, ValidationResult


class Field:
    """Represents a single field in a schema."""
    
    def __init__(
        self,
        name: str,
        data_type: DataType,
        required: bool = False,
        validators: Optional[List[Callable]] = None,
        default: Any = None
    ):
        self.name = name
        self.data_type = data_type
        self.required = required
        self.validators = validators or []
        self.default = default
    
    def validate(self, value: Any, row: Optional[int] = None) -> tuple:
        """Validate a value for this field.
        
        Returns:
            (is_valid, error_message, converted_value)
        """
        # Handle missing values
        if value is None or value == "":
            if self.required:
                return False, "Required field", None
            return True, None, self.default
        
        # Type checking and conversion
        try:
            converted = self._convert_type(value)
        except ValueError as e:
            return False, str(e), None
        
        # Run custom validators
        for validator in self.validators:
            is_valid, error_msg = validator(converted)
            if not is_valid:
                return False, error_msg, None
        
        return True, None, converted
    
    def _convert_type(self, value: Any) -> Any:
        """Convert value to expected type."""
        if self.data_type == DataType.STRING:
            return str(value)
        elif self.data_type == DataType.INTEGER:
            return int(float(value))
        elif self.data_type == DataType.FLOAT:
            return float(value)
        elif self.data_type == DataType.BOOLEAN:
            if isinstance(value, bool):
                return value
            if str(value).lower() in ('true', '1', 'yes', 'y'):
                return True
            if str(value).lower() in ('false', '0', 'no', 'n'):
                return False
            raise ValueError(f"Cannot convert '{value}' to boolean")
        return value


class Schema:
    """Defines the structure and validation rules for data."""
    
    def __init__(self, fields: List[Field]):
        self.fields = fields
        self.field_map = {f.name: f for f in fields}
    
    def validate_record(
        self, 
        record: Dict[str, Any], 
        row: Optional[int] = None
    ) -> tuple:
        """Validate a single record/row.
        
        Returns:
            (errors_list, converted_record)
        """
        errors = []
        converted_record = {}
        
        for field in self.fields:
            value = record.get(field.name)
            is_valid, error_msg, converted_value = field.validate(value, row)
            
            if not is_valid:
                errors.append(ValidationError(
                    field=field.name,
                    value=value,
                    message=error_msg,
                    row=row
                ))
            else:
                converted_record[field.name] = converted_value
        
        return errors, converted_record
    
    def validate_batch(
        self, 
        records: List[Dict[str, Any]]
    ) -> ValidationResult:
        """Validate multiple records.
        
        Returns:
            ValidationResult with all errors and converted records
        """
        all_errors = []
        converted_records = []
        
        for row_num, record in enumerate(records, start=1):
            errors, converted = self.validate_record(record, row=row_num)
            all_errors.extend(errors)
            converted_records.append(converted)
        
        return ValidationResult(
            valid=len(all_errors) == 0,
            errors=all_errors,
            records_validated=len(records)
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Export schema definition."""
        return {
            "fields": [
                {
                    "name": f.name,
                    "type": f.data_type.value,
                    "required": f.required,
                    "has_validators": len(f.validators) > 0
                }
                for f in self.fields
            ]
        }