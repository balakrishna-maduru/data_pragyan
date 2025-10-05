"""Tests for database connection and query execution."""

import pytest
import pandas as pd
from unittest.mock import Mock, patch, MagicMock
from src.database.connection import DatabaseManager


class TestDatabaseManager:
    """Test cases for DatabaseManager class."""
    
    @pytest.fixture
    def db_manager(self):
        """Create a DatabaseManager instance for testing."""
        return DatabaseManager("postgresql://test:test@localhost:5432/test")
    
    @patch('src.database.connection.create_engine')
    def test_engine_creation(self, mock_create_engine, db_manager):
        """Test that engine is created with correct parameters."""
        mock_engine = Mock()
        mock_create_engine.return_value = mock_engine
        
        engine = db_manager.engine
        
        mock_create_engine.assert_called_once_with(
            "postgresql://test:test@localhost:5432/test",
            pool_size=5,
            max_overflow=10,
            pool_recycle=3600,
            pool_pre_ping=True
        )
        assert engine == mock_engine
    
    @patch('src.database.connection.create_engine')
    def test_test_connection_success(self, mock_create_engine, db_manager):
        """Test successful database connection test."""
        mock_engine = Mock()
        mock_connection = Mock()
        mock_create_engine.return_value = mock_engine
        mock_engine.connect.return_value.__enter__ = Mock(return_value=mock_connection)
        mock_engine.connect.return_value.__exit__ = Mock(return_value=None)
        
        result = db_manager.test_connection()
        
        assert result is True
        mock_connection.execute.assert_called_once()
    
    @patch('src.database.connection.create_engine')
    def test_test_connection_failure(self, mock_create_engine, db_manager):
        """Test failed database connection test."""
        mock_engine = Mock()
        mock_create_engine.return_value = mock_engine
        mock_engine.connect.side_effect = Exception("Connection failed")
        
        result = db_manager.test_connection()
        
        assert result is False
    
    @patch('src.database.connection.pd.read_sql_query')
    @patch('src.database.connection.create_engine')
    def test_execute_query_success(self, mock_create_engine, mock_read_sql, db_manager):
        """Test successful query execution."""
        mock_engine = Mock()
        mock_connection = Mock()
        mock_df = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
        
        mock_create_engine.return_value = mock_engine
        mock_engine.connect.return_value.__enter__ = Mock(return_value=mock_connection)
        mock_engine.connect.return_value.__exit__ = Mock(return_value=None)
        mock_read_sql.return_value = mock_df
        
        result = db_manager.execute_query("SELECT * FROM test")
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        mock_read_sql.assert_called_once()
    
    @patch('src.database.connection.create_engine')
    def test_execute_query_failure(self, mock_create_engine, db_manager):
        """Test query execution failure."""
        mock_engine = Mock()
        mock_create_engine.return_value = mock_engine
        mock_engine.connect.side_effect = Exception("Query failed")
        
        with pytest.raises(Exception, match="Query failed"):
            db_manager.execute_query("INVALID SQL")
    
    @patch('src.database.connection.create_engine')
    def test_get_table_names(self, mock_create_engine, db_manager):
        """Test retrieving table names."""
        mock_engine = Mock()
        mock_create_engine.return_value = mock_engine
        
        with patch.object(db_manager, 'execute_query') as mock_execute:
            mock_df = pd.DataFrame({'table_name': ['users', 'orders', 'products']})
            mock_execute.return_value = mock_df
            
            result = db_manager.get_table_names()
            
            assert result == ['users', 'orders', 'products']
            mock_execute.assert_called_once()
    
    @patch('src.database.connection.create_engine')
    def test_get_table_schema(self, mock_create_engine, db_manager):
        """Test retrieving table schema."""
        mock_engine = Mock()
        mock_create_engine.return_value = mock_engine
        
        with patch.object(db_manager, 'execute_query') as mock_execute:
            mock_df = pd.DataFrame({
                'column_name': ['id', 'name'],
                'data_type': ['integer', 'varchar'],
                'is_nullable': ['NO', 'YES'],
                'column_default': [None, None],
                'character_maximum_length': [None, 100]
            })
            mock_execute.return_value = mock_df
            
            result = db_manager.get_table_schema('users')
            
            assert isinstance(result, pd.DataFrame)
            assert len(result) == 2
            mock_execute.assert_called_once()
    
    def test_close(self, db_manager):
        """Test closing database connections."""
        mock_engine = Mock()
        db_manager._engine = mock_engine
        
        db_manager.close()
        
        mock_engine.dispose.assert_called_once()
        assert db_manager._engine is None


@pytest.fixture
def sample_dataframe():
    """Create a sample DataFrame for testing."""
    return pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
        'age': [25, 30, 35, 28, 42],
        'city': ['New York', 'London', 'Paris', 'Tokyo', 'Sydney']
    })


class TestDatabaseIntegration:
    """Integration tests for database operations."""
    
    @pytest.mark.integration
    def test_full_database_workflow(self):
        """Test complete database workflow (requires actual database)."""
        # This test requires a real database connection
        # It should be run separately as an integration test
        pytest.skip("Integration test - requires database setup")
    
    @pytest.mark.integration
    def test_postgresql_specific_queries(self):
        """Test PostgreSQL-specific query features."""
        pytest.skip("Integration test - requires PostgreSQL database")