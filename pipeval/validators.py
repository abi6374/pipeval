"""Built-in validator functions."""

import re
from datetime import datetime
from typing import Callable


class Validators:
    """Collection of reusable validators."""
    
    @staticmethod
    def required() -> Callable:
        """Validator: value must not be empty."""
        def validate(value):
            if value is None or value == "" or value == []:
                return False, "Required field cannot be empty"
            return True, None
        return validate
    
    @staticmethod
    def min_length(length: int) -> Callable:
        """Validator: string minimum length."""
        def validate(value):
            if not isinstance(value, str):
                return False, f"Expected string, got {type(value).__name__}"
            if len(value) < length:
                return False, f"String must be at least {length} characters (got {len(value)})"
            return True, None
        return validate
    
    @staticmethod
    def max_length(length: int) -> Callable:
        """Validator: string maximum length."""
        def validate(value):
            if not isinstance(value, str):
                return False, f"Expected string, got {type(value).__name__}"
            if len(value) > length:
                return False, f"String must not exceed {length} characters (got {len(value)})"
            return True, None
        return validate
    
    @staticmethod
    def email() -> Callable:
        """Validator: email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        def validate(value):
            if not isinstance(value, str):
                return False, "Email must be a string"
            if not re.match(pattern, value):
                return False, "Invalid email format"
            return True, None
        return validate
    
    @staticmethod
    def range_check(min_val: float, max_val: float) -> Callable:
        """Validator: numeric range."""
        def validate(value):
            try:
                num = float(value)
            except (ValueError, TypeError):
                return False, f"Expected number, got {type(value).__name__}"
            
            if num < min_val or num > max_val:
                return False, f"Value must be between {min_val} and {max_val}, got {num}"
            return True, None
        return validate
    
    @staticmethod
    def one_of(allowed: list) -> Callable:
        """Validator: value must be one of allowed options."""
        def validate(value):
            if value not in allowed:
                allowed_str = ", ".join(map(str, allowed))
                return False, f"Value must be one of: {allowed_str}. Got '{value}'"
            return True, None
        return validate
    
    @staticmethod
    def regex(pattern: str, name: str = "pattern") -> Callable:
        """Validator: regex pattern match."""
        def validate(value):
            if not isinstance(value, str):
                return False, "Regex validation requires string input"
            if not re.match(pattern, value):
                return False, f"Value does not match {name}"
            return True, None
        return validate
    
    @staticmethod
    def url() -> Callable:
        """Validator: valid URL format."""
        pattern = r'^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(:[0-9]+)?(/.*)?$'
        def validate(value):
            if not isinstance(value, str):
                return False, "URL must be a string"
            if not re.match(pattern, value):
                return False, "Invalid URL format"
            return True, None
        return validate
    
    @staticmethod
    def phone() -> Callable:
        """Validator: phone number format."""
        pattern = r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$'
        def validate(value):
            if not isinstance(value, str):
                return False, "Phone must be a string"
            if not re.match(pattern, value.replace(" ", "")):
                return False, "Invalid phone format"
            return True, None
        return validate
    
    @staticmethod
    def minimum(min_val: float) -> Callable:
        """Validator: minimum numeric value."""
        def validate(value):
            try:
                num = float(value)
            except (ValueError, TypeError):
                return False, f"Expected number"
            if num < min_val:
                return False, f"Value must be >= {min_val}"
            return True, None
        return validate
    
    @staticmethod
    def maximum(max_val: float) -> Callable:
        """Validator: maximum numeric value."""
        def validate(value):
            try:
                num = float(value)
            except (ValueError, TypeError):
                return False, f"Expected number"
            if num > max_val:
                return False, f"Value must be <= {max_val}"
            return True, None
        return validate
