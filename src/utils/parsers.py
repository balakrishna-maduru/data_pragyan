"""
File parsing utilities for different formats.
"""
import pandas as pd
from pathlib import Path
from typing import Dict, Any, List, Union
import csv
import json
import io


class FileParser:
    """Handle different file format parsing."""
    
    def __init__(self) -> None:
        self.supported_formats = {
            '.csv': self._parse_csv,
            '.json': self._parse_json,
            '.xlsx': self._parse_excel,
            '.xls': self._parse_excel,
            '.txt': self._parse_text
        }
    
    def parse_file(self, file_input: Union[str, Any]) -> pd.DataFrame:
        """Parse file based on extension. Handles both file paths and Streamlit UploadedFile objects."""
        # Check if it's a Streamlit UploadedFile object
        if hasattr(file_input, 'name') and hasattr(file_input, 'read'):
            return self._parse_uploaded_file(file_input)
        
        # Handle regular file path
        path = Path(file_input)
        extension = path.suffix.lower()
        
        if extension not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {extension}")
        
        print(f"Parsing {extension} file: {file_input}")
        return self.supported_formats[extension](file_input)
    
    def _parse_uploaded_file(self, uploaded_file) -> pd.DataFrame:
        """Parse Streamlit UploadedFile object."""
        # Get file extension from name
        file_name = uploaded_file.name
        extension = Path(file_name).suffix.lower()
        
        if extension not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {extension}")
        
        print(f"Parsing uploaded {extension} file: {file_name}")
        
        # Read file content into memory
        file_content = uploaded_file.read()
        uploaded_file.seek(0)  # Reset file pointer for potential re-reads
        
        # Parse based on extension
        if extension == '.csv':
            return self._parse_csv_content(file_content)
        elif extension == '.json':
            return self._parse_json_content(file_content)
        elif extension in ['.xlsx', '.xls']:
            return self._parse_excel_content(file_content)
        elif extension == '.txt':
            return self._parse_text_content(file_content)
        else:
            raise ValueError(f"Unsupported file format: {extension}")
    
    def _parse_csv_content(self, content: bytes) -> pd.DataFrame:
        """Parse CSV content from bytes."""
        try:
            # Try different encodings
            for encoding in ['utf-8', 'latin-1', 'cp1252']:
                try:
                    text_content = content.decode(encoding)
                    df = pd.read_csv(io.StringIO(text_content))
                    print(f"Successfully parsed CSV with {encoding} encoding")
                    return df
                except UnicodeDecodeError:
                    continue
            
            # If all encodings fail, try with errors='ignore'
            text_content = content.decode('utf-8', errors='ignore')
            df = pd.read_csv(io.StringIO(text_content))
            return df
            
        except Exception as e:
            print(f"Failed to parse CSV content: {e}")
            raise
    
    def _parse_json_content(self, content: bytes) -> pd.DataFrame:
        """Parse JSON content from bytes."""
        try:
            text_content = content.decode('utf-8')
            data = json.loads(text_content)
            
            # Handle different JSON structures
            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, dict):
                # Try to find the main data array
                for key in ['data', 'records', 'items', 'results']:
                    if key in data and isinstance(data[key], list):
                        df = pd.DataFrame(data[key])
                        break
                else:
                    # Flatten the dictionary
                    df = pd.json_normalize(data)
            else:
                raise ValueError("Unsupported JSON structure")
            
            print("Successfully parsed JSON content")
            return df
            
        except Exception as e:
            print(f"Failed to parse JSON content: {e}")
            raise
    
    def _parse_excel_content(self, content: bytes) -> pd.DataFrame:
        """Parse Excel content from bytes."""
        try:
            # Create BytesIO object for pandas to read
            excel_buffer = io.BytesIO(content)
            df = pd.read_excel(excel_buffer, sheet_name=0)
            print("Successfully parsed Excel content")
            return df
            
        except Exception as e:
            print(f"Failed to parse Excel content: {e}")
            raise
    
    def _parse_text_content(self, content: bytes) -> pd.DataFrame:
        """Parse text content from bytes (assume tab-separated)."""
        try:
            text_content = content.decode('utf-8')
            df = pd.read_csv(io.StringIO(text_content), sep='\t')
            print("Successfully parsed text content")
            return df
            
        except Exception as e:
            print(f"Failed to parse text content: {e}")
            raise
    
    def _parse_csv(self, file_path: str) -> pd.DataFrame:
        """Parse CSV file."""
        try:
            # Try different encodings and separators
            for encoding in ['utf-8', 'latin-1', 'cp1252']:
                try:
                    df = pd.read_csv(file_path, encoding=encoding)
                    print(f"Successfully parsed CSV with {encoding} encoding")
                    return df
                except UnicodeDecodeError:
                    continue
            
            # If all encodings fail, try with errors='ignore'
            df = pd.read_csv(file_path, encoding='utf-8', errors='ignore')
            return df
            
        except Exception as e:
            print(f"Failed to parse CSV: {e}")
            raise
    
    def _parse_json(self, file_path: str) -> pd.DataFrame:
        """Parse JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle different JSON structures
            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, dict):
                # Try to find the main data array
                for key in ['data', 'records', 'items', 'results']:
                    if key in data and isinstance(data[key], list):
                        df = pd.DataFrame(data[key])
                        break
                else:
                    # Flatten the dictionary
                    df = pd.json_normalize(data)
            else:
                raise ValueError("Unsupported JSON structure")
            
            print("Successfully parsed JSON file")
            return df
            
        except Exception as e:
            print(f"Failed to parse JSON: {e}")
            raise
    
    def _parse_excel(self, file_path: str) -> pd.DataFrame:
        """Parse Excel file."""
        try:
            # Read the first sheet
            df = pd.read_excel(file_path, sheet_name=0)
            print("Successfully parsed Excel file")
            return df
            
        except Exception as e:
            print(f"Failed to parse Excel: {e}")
            raise
    
    def _parse_text(self, file_path: str) -> pd.DataFrame:
        """Parse text file (assume tab-separated)."""
        try:
            df = pd.read_csv(file_path, sep='\t', encoding='utf-8')
            print("Successfully parsed text file")
            return df
            
        except Exception as e:
            print(f"Failed to parse text file: {e}")
            raise
    
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """Get basic information about the file."""
        try:
            df = self.parse_file(file_path)
            info = {
                'file_name': Path(file_path).name,
                'file_size': Path(file_path).stat().st_size,
                'rows': len(df),
                'columns': len(df.columns),
                'column_names': df.columns.tolist(),
                'data_types': df.dtypes.to_dict(),
                'missing_values': df.isnull().sum().to_dict(),
                'sample_data': df.head().to_dict('records')
            }
            return info
            
        except Exception as e:
            print(f"Failed to get file info: {e}")
            raise
    
    def validate_data_quality(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Perform basic data quality checks."""
        quality_report = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'missing_data': {
                'total_missing': df.isnull().sum().sum(),
                'missing_by_column': df.isnull().sum().to_dict(),
                'missing_percentage': (df.isnull().sum() / len(df) * 100).to_dict()
            },
            'duplicates': {
                'total_duplicates': df.duplicated().sum(),
                'duplicate_percentage': df.duplicated().sum() / len(df) * 100
            },
            'data_types': df.dtypes.to_dict(),
            'numeric_columns': df.select_dtypes(include=['number']).columns.tolist(),
            'text_columns': df.select_dtypes(include=['object']).columns.tolist(),
            'datetime_columns': df.select_dtypes(include=['datetime']).columns.tolist()
        }
        
        return quality_report