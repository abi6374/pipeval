"""File readers for multiple formats."""

import json
import csv
from typing import List, Dict, Any, Optional
from pathlib import Path


class FileReader:
    """Handles reading from multiple file formats."""
    
    @staticmethod
    def read_json(file_path: str) -> List[Dict[str, Any]]:
        """Read JSON file and return list of records.
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            List of dictionaries
            
        Raises:
            FileNotFoundError: If file doesn't exist
            json.JSONDecodeError: If JSON is invalid
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Ensure we return a list
        if isinstance(data, list):
            return data
        else:
            return [data]
    
    @staticmethod
    def read_csv(
        file_path: str, 
        delimiter: str = ',',
        encoding: str = 'utf-8'
    ) -> List[Dict[str, Any]]:
        """Read CSV file and return list of records.
        
        Args:
            file_path: Path to CSV file
            delimiter: CSV delimiter (default: comma)
            encoding: File encoding (default: utf-8)
            
        Returns:
            List of dictionaries
            
        Raises:
            FileNotFoundError: If file doesn't exist
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        records = []
        with open(path, 'r', encoding=encoding) as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            for row in reader:
                records.append(row)
        
        return records
    
    @staticmethod
    def read_parquet(file_path: str) -> List[Dict[str, Any]]:
        """Read Parquet file and return list of records.
        
        Args:
            file_path: Path to Parquet file
            
        Returns:
            List of dictionaries
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ImportError: If pyarrow is not installed
        """
        try:
            import pyarrow.parquet as pq
        except ImportError:
            raise ImportError(
                "pyarrow is required for Parquet support. "
                "Install with: pip install data-validator[parquet]"
            )
        
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        table = pq.read_table(path)
        data = table.to_pandas().to_dict('records')
        
        return data
    
    @staticmethod
    def auto_read(file_path: str, **kwargs) -> List[Dict[str, Any]]:
        """Automatically detect format and read file.
        
        Args:
            file_path: Path to file
            **kwargs: Additional arguments for specific readers
            
        Returns:
            List of dictionaries
            
        Raises:
            ValueError: If file format is not supported
        """
        path = Path(file_path)
        suffix = path.suffix.lower()
        
        if suffix == '.json':
            return FileReader.read_json(file_path)
        elif suffix == '.csv':
            return FileReader.read_csv(file_path, **kwargs)
        elif suffix == '.parquet' or suffix == '.pq':
            return FileReader.read_parquet(file_path)
        else:
            raise ValueError(
                f"Unsupported file format: {suffix}. "
                "Supported: .json, .csv, .parquet"
            )


class FileValidator:
    """Validate files directly without manual reading."""
    
    @staticmethod
    def validate_json_file(schema, file_path: str):
        """Validate JSON file against schema.
        
        Args:
            schema: Schema object
            file_path: Path to JSON file
            
        Returns:
            ValidationResult
        """
        records = FileReader.read_json(file_path)
        return schema.validate_batch(records)
    
    @staticmethod
    def validate_csv_file(
        schema, 
        file_path: str,
        delimiter: str = ',',
        encoding: str = 'utf-8'
    ):
        """Validate CSV file against schema.
        
        Args:
            schema: Schema object
            file_path: Path to CSV file
            delimiter: CSV delimiter
            encoding: File encoding
            
        Returns:
            ValidationResult
        """
        records = FileReader.read_csv(file_path, delimiter, encoding)
        return schema.validate_batch(records)
    
    @staticmethod
    def validate_parquet_file(schema, file_path: str):
        """Validate Parquet file against schema.
        
        Args:
            schema: Schema object
            file_path: Path to Parquet file
            
        Returns:
            ValidationResult
        """
        records = FileReader.read_parquet(file_path)
        return schema.validate_batch(records)
    
    @staticmethod
    def validate_file(schema, file_path: str, **kwargs):
        """Validate file (auto-detect format).
        
        Args:
            schema: Schema object
            file_path: Path to file
            **kwargs: Additional arguments for specific readers
            
        Returns:
            ValidationResult
        """
        records = FileReader.auto_read(file_path, **kwargs)
        return schema.validate_batch(records)
