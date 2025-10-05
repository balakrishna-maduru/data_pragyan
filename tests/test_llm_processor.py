"""Tests for LLM processor functionality."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.utils.llm_processor import NLToSQLProcessor
from src.config.settings import Settings


class TestNLToSQLProcessor:
    """Test cases for NLToSQLProcessor class."""
    
    @pytest.fixture
    def mock_settings(self):
        """Create mock settings for testing."""
        settings = Mock(spec=Settings)
        settings.openai_api_key = "test-api-key"
        settings.llm_model = "gpt-4"
        settings.llm_temperature = 0.1
        return settings
    
    @pytest.fixture
    def mock_settings_no_key(self):
        """Create mock settings without API key."""
        settings = Mock(spec=Settings)
        settings.openai_api_key = None
        settings.llm_model = "gpt-4"
        settings.llm_temperature = 0.1
        return settings
    
    def test_init_with_api_key(self, mock_settings):
        """Test initialization with valid API key."""
        processor = NLToSQLProcessor(mock_settings)
        assert processor.settings == mock_settings
    
    def test_init_without_api_key(self, mock_settings_no_key):
        """Test initialization without API key."""
        processor = NLToSQLProcessor(mock_settings_no_key)
        assert processor.settings == mock_settings_no_key
    
    @patch('src.utils.llm_processor.openai.ChatCompletion.create')
    def test_generate_sql_success(self, mock_openai_create, mock_settings):
        """Test successful SQL generation."""
        # Mock OpenAI response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "SELECT * FROM customers WHERE city = 'New York'"
        mock_openai_create.return_value = mock_response
        
        processor = NLToSQLProcessor(mock_settings)
        
        result = processor.generate_sql(
            "Show me all customers from New York",
            "Table: customers\nColumns: id, name, city"
        )
        
        assert result == "SELECT * FROM customers WHERE city = 'New York'"
        mock_openai_create.assert_called_once()
    
    @patch('src.utils.llm_processor.openai.ChatCompletion.create')
    def test_generate_sql_with_code_blocks(self, mock_openai_create, mock_settings):
        """Test SQL generation with markdown code blocks."""
        # Mock OpenAI response with code blocks
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "```sql\nSELECT * FROM customers\n```"
        mock_openai_create.return_value = mock_response
        
        processor = NLToSQLProcessor(mock_settings)
        
        result = processor.generate_sql(
            "Show all customers",
            "Table: customers\nColumns: id, name"
        )
        
        assert result == "SELECT * FROM customers"
    
    def test_generate_sql_no_api_key(self, mock_settings_no_key):
        """Test SQL generation without API key."""
        processor = NLToSQLProcessor(mock_settings_no_key)
        
        with pytest.raises(ValueError, match="OpenAI API key not configured"):
            processor.generate_sql("test query", "test schema")
    
    @patch('src.utils.llm_processor.openai.ChatCompletion.create')
    def test_generate_sql_api_error(self, mock_openai_create, mock_settings):
        """Test SQL generation with API error."""
        mock_openai_create.side_effect = Exception("API Error")
        
        processor = NLToSQLProcessor(mock_settings)
        
        with pytest.raises(Exception, match="API Error"):
            processor.generate_sql("test query", "test schema")
    
    @patch('src.utils.llm_processor.openai.ChatCompletion.create')
    def test_explain_query_success(self, mock_openai_create, mock_settings):
        """Test successful query explanation."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "This query retrieves all customer data from New York"
        mock_openai_create.return_value = mock_response
        
        processor = NLToSQLProcessor(mock_settings)
        
        result = processor.explain_query("SELECT * FROM customers WHERE city = 'New York'")
        
        assert result == "This query retrieves all customer data from New York"
        mock_openai_create.assert_called_once()
    
    def test_explain_query_no_api_key(self, mock_settings_no_key):
        """Test query explanation without API key."""
        processor = NLToSQLProcessor(mock_settings_no_key)
        
        result = processor.explain_query("SELECT * FROM customers")
        
        assert "unavailable" in result.lower()
    
    @patch('src.utils.llm_processor.openai.ChatCompletion.create')
    def test_suggest_improvements_success(self, mock_openai_create, mock_settings):
        """Test successful query improvement suggestions."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Consider adding an index on the city column"
        mock_openai_create.return_value = mock_response
        
        processor = NLToSQLProcessor(mock_settings)
        
        result = processor.suggest_improvements("SELECT * FROM customers WHERE city = 'New York'")
        
        assert result == "Consider adding an index on the city column"
        mock_openai_create.assert_called_once()
    
    def test_build_sql_prompt(self, mock_settings):
        """Test SQL prompt building."""
        processor = NLToSQLProcessor(mock_settings)
        
        prompt = processor._build_sql_prompt(
            "Show all customers",
            "Table: customers\nColumns: id, name"
        )
        
        assert "Show all customers" in prompt
        assert "Table: customers" in prompt
        assert "PostgreSQL" in prompt
        assert "LIMIT" in prompt


class TestLLMProcessorEdgeCases:
    """Test edge cases and error conditions."""
    
    @pytest.fixture
    def processor_with_key(self):
        """Create processor with API key."""
        settings = Mock()
        settings.openai_api_key = "test-key"
        settings.llm_model = "gpt-4"
        settings.llm_temperature = 0.1
        return NLToSQLProcessor(settings)
    
    def test_empty_natural_query(self, processor_with_key):
        """Test with empty natural language query."""
        with patch('src.utils.llm_processor.openai.ChatCompletion.create') as mock_create:
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = ""
            mock_create.return_value = mock_response
            
            result = processor_with_key.generate_sql("", "schema")
            assert result == ""
    
    def test_empty_schema(self, processor_with_key):
        """Test with empty schema information."""
        with patch('src.utils.llm_processor.openai.ChatCompletion.create') as mock_create:
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = "SELECT 1"
            mock_create.return_value = mock_response
            
            result = processor_with_key.generate_sql("test query", "")
            assert result == "SELECT 1"
    
    @patch('src.utils.llm_processor.openai.ChatCompletion.create')
    def test_rate_limit_error(self, mock_openai_create, processor_with_key):
        """Test handling of rate limit errors."""
        mock_openai_create.side_effect = Exception("Rate limit exceeded")
        
        with pytest.raises(Exception, match="Rate limit exceeded"):
            processor_with_key.generate_sql("test", "schema")