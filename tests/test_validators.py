"""Tests for validators."""

from pipeval import Validators


def test_email_validator():
    """Test email validation."""
    validator = Validators.email()
    
    valid, msg = validator("test@example.com")
    assert valid
    
    valid, msg = validator("invalid-email")
    assert not valid


def test_range_validator():
    """Test range validation."""
    validator = Validators.range_check(0, 100)
    
    valid, msg = validator(50)
    assert valid
    
    valid, msg = validator(150)
    assert not valid


def test_length_validators():
    """Test string length validation."""
    min_validator = Validators.min_length(3)
    valid, msg = min_validator("hello")
    assert valid
    
    valid, msg = min_validator("hi")
    assert not valid
    
    max_validator = Validators.max_length(5)
    valid, msg = max_validator("hello")
    assert valid
    
    valid, msg = max_validator("toolong")
    assert not valid


def test_one_of_validator():
    """Test one_of validator."""
    validator = Validators.one_of(["admin", "user", "guest"])
    
    valid, msg = validator("admin")
    assert valid
    
    valid, msg = validator("superuser")
    assert not valid


def test_url_validator():
    """Test URL validation."""
    validator = Validators.url()
    
    valid, msg = validator("https://example.com")
    assert valid
    
    valid, msg = validator("invalid-url")
    assert not valid


def test_phone_validator():
    """Test phone number validation."""
    validator = Validators.phone()
    
    valid, msg = validator("+1(555)123-4567")
    assert valid
    
    valid, msg = validator("invalid")
    assert not valid


def test_minimum_validator():
    """Test minimum value validator."""
    validator = Validators.minimum(10)
    
    valid, msg = validator(15)
    assert valid
    
    valid, msg = validator(5)
    assert not valid


def test_maximum_validator():
    """Test maximum value validator."""
    validator = Validators.maximum(100)
    
    valid, msg = validator(50)
    assert valid
    
    valid, msg = validator(150)
    assert not valid


def test_required_validator():
    """Test required validator."""
    validator = Validators.required()
    
    valid, msg = validator("value")
    assert valid
    
    valid, msg = validator("")
    assert not valid
    
    valid, msg = validator(None)
    assert not valid


def test_regex_validator():
    """Test regex validator."""
    validator = Validators.regex(r'^\d{3}-\d{3}-\d{4}$', 'phone format')
    
    valid, msg = validator("123-456-7890")
    assert valid
    
    valid, msg = validator("1234567890")
    assert not valid
