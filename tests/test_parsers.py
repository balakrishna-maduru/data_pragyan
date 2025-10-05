"""Tests for file parsing utilities."""

import pytest
import pandas as pd
from io import BytesIO
from unittest.mock import Mock, patch
from src.utils.parsers import FileParser


class TestFileParser:
    """Test cases for FileParser class."""
    
    @pytest.fixture
    def file_parser(self):
        """Create FileParser instance for testing."""
        return FileParser()
    
    @pytest.fixture
    def sample_csv_content(self):
        """Create sample CSV content for testing."""
        return b"name,age,city\nJohn,25,New York\nJane,30,London"
    
    @pytest.fixture
    def sample_json_content(self):
        """Create sample JSON content for testing."""
        return b'[{"name": "John", "age": 25, "city": "New York"}, {"name": "Jane", "age": 30, "city": "London"}]'
    
    def test_init(self, file_parser):
        """Test FileParser initialization."""
        assert file_parser.supported_extensions == {'.csv', '.xlsx', '.xls', '.json'}
    
    def test_parse_csv_success(self, file_parser, sample_csv_content):
        """Test successful CSV parsing."""
        mock_file = Mock()
        mock_file.name = "test.csv"
        mock_file.read.return_value = sample_csv_content
        
        result = file_parser.parse_file(mock_file)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert list(result.columns) == ['name', 'age', 'city']
        assert result.iloc[0]['name'] == 'John'
    
    def test_parse_json_success(self, file_parser, sample_json_content):
        """Test successful JSON parsing."""
        mock_file = Mock()
        mock_file.name = "test.json"
        mock_file.read.return_value = sample_json_content
        
        result = file_parser.parse_file(mock_file)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert 'name' in result.columns
        assert result.iloc[0]['name'] == 'John'
    
    @patch('src.utils.parsers.pd.read_excel')
    def test_parse_excel_success(self, mock_read_excel, file_parser):
        """Test successful Excel parsing."""
        mock_file = Mock()
        mock_file.name = "test.xlsx"
        mock_file.read.return_value = b"fake excel content"
        
        mock_df = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
        mock_read_excel.return_value = mock_df
        
        result = file_parser.parse_file(mock_file)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        mock_read_excel.assert_called()
    
    def test_parse_unsupported_file(self, file_parser):
        """Test parsing unsupported file type."""
        mock_file = Mock()
        mock_file.name = "test.txt"
        mock_file.read.return_value = b"some text content"
        
        with pytest.raises(ValueError, match="Unsupported file type"):
            file_parser.parse_file(mock_file)
    
    def test_parse_csv_different_separators(self, file_parser):
        """Test CSV parsing with different separators."""
        # Test semicolon separator
        csv_content = b"name;age;city\nJohn;25;New York\nJane;30;London"
        
        mock_file = Mock()
        mock_file.name = "test.csv"
        mock_file.read.return_value = csv_content
        
        result = file_parser.parse_file(mock_file)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert list(result.columns) == ['name', 'age', 'city']
    
    def test_parse_csv_different_encodings(self, file_parser):
        """Test CSV parsing with different encodings."""
        # Test latin-1 encoding
        csv_content = "name,age,city\nJöhn,25,New York\nJané,30,London".encode('latin-1')
        
        mock_file = Mock()
        mock_file.name = "test.csv"
        mock_file.read.return_value = csv_content
        
        result = file_parser.parse_file(mock_file)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
    
    @patch('src.utils.parsers.pd.ExcelFile')
    def test_parse_excel_multiple_sheets(self, mock_excel_file, file_parser):
        """Test Excel parsing with multiple sheets."""
        mock_file = Mock()
        mock_file.name = "test.xlsx"
        mock_file.read.return_value = b"fake excel content"
        
        # Mock ExcelFile
        mock_excel_instance = Mock()
        mock_excel_instance.sheet_names = ['Sheet1', 'Sheet2']
        mock_excel_file.return_value = mock_excel_instance
        
        # Mock pd.read_excel to return DataFrame for first sheet
        with patch('src.utils.parsers.pd.read_excel') as mock_read_excel:
            mock_df = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
            mock_read_excel.return_value = mock_df
            
            result = file_parser.parse_file(mock_file)
            
            assert isinstance(result, pd.DataFrame)
    
    def test_parse_json_different_orientations(self, file_parser):
        """Test JSON parsing with different orientations."""
        # Test records orientation
        json_content = b'[{"name": "John", "age": 25}, {"name": "Jane", "age": 30}]'
        
        mock_file = Mock()
        mock_file.name = "test.json"
        mock_file.read.return_value = json_content
        
        result = file_parser.parse_file(mock_file)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
    
    def test_get_file_info_with_file_object(self, file_parser):
        """Test getting file info from file object."""
        mock_file = Mock()
        mock_file.name = "test.csv"
        mock_file.read.return_value = b"test content"
        
        result = file_parser.get_file_info(mock_file)
        
        assert result['filename'] == "test.csv"
        assert result['extension'] == '.csv'
        assert result['supported'] is True
        assert 'size_bytes' in result
        assert 'size_mb' in result
    
    def test_get_file_info_with_path(self, file_parser):
        """Test getting file info from file path."""
        with patch('pathlib.Path.stat') as mock_stat:
            mock_stat_result = Mock()
            mock_stat_result.st_size = 1024
            mock_stat.return_value = mock_stat_result
            
            result = file_parser.get_file_info("test.csv")
            
            assert result['filename'] == "test.csv"
            assert result['extension'] == '.csv'
            assert result['supported'] is True
            assert result['size_bytes'] == 1024
    
    def test_csv_parsing_error_handling(self, file_parser):
        """Test CSV parsing error handling."""
        # Invalid CSV content
        invalid_csv = b"invalid,csv,content\nwith,missing\ncolumns"
        
        mock_file = Mock()
        mock_file.name = "test.csv"
        mock_file.read.return_value = invalid_csv
        
        # Should still parse, pandas is quite forgiving
        result = file_parser.parse_file(mock_file)
        assert isinstance(result, pd.DataFrame)
    
    def test_json_parsing_error_handling(self, file_parser):
        """Test JSON parsing error handling."""
        # Invalid JSON content
        invalid_json = b'{"invalid": json content}'
        
        mock_file = Mock()
        mock_file.name = "test.json"
        mock_file.read.return_value = invalid_json
        
        with pytest.raises(ValueError, match="Could not parse JSON file"):
            file_parser.parse_file(mock_file)


class TestFileParserIntegration:
    """Integration tests for file parser."""
    
    @pytest.fixture
    def file_parser(self):
        """Create FileParser instance for testing."""
        return FileParser()
    
    def test_real_csv_parsing(self, file_parser):
        """Test parsing with real CSV data."""
        csv_data = """id,name,email,age
1,John Doe,john@example.com,25
2,Jane Smith,jane@example.com,30
3,Bob Johnson,bob@example.com,35"""
        
        mock_file = Mock()
        mock_file.name = "users.csv"
        mock_file.read.return_value = csv_data.encode('utf-8')
        
        result = file_parser.parse_file(mock_file)
        
        assert len(result) == 3
        assert 'email' in result.columns
        assert result['age'].dtype in ['int64', 'object']  # Could be either depending on pandas version
    
    def test_large_file_handling(self, file_parser):
        """Test handling of large files."""
        # Create a large CSV content
        rows = []
        for i in range(1000):
            rows.append(f"{i},User{i},user{i}@example.com,{20+i%50}")
        
        large_csv = "id,name,email,age\n" + "\n".join(rows)
        
        mock_file = Mock()
        mock_file.name = "large.csv"
        mock_file.read.return_value = large_csv.encode('utf-8')
        
        result = file_parser.parse_file(mock_file)
        
        assert len(result) == 1000
        assert list(result.columns) == ['id', 'name', 'email', 'age']