"""Database connection and query management."""

import pandas as pd
import logging
from typing import Optional, Dict, Any, List
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages database connections and queries."""
    
    def __init__(self, database_url: str) -> None:
        """Initialize database manager with connection URL."""
        self.database_url = database_url
        self._engine: Optional[Engine] = None
        self._connection_pool: Optional[Any] = None
    
    @property
    def engine(self) -> Engine:
        """Get or create SQLAlchemy engine."""
        if self._engine is None:
            # Add connection arguments for MariaDB/MySQL
            connect_args = {}
            if 'mysql' in self.database_url:
                connect_args = {
                    'connect_timeout': 20,
                    'read_timeout': 20,
                    'write_timeout': 20,
                    'charset': 'utf8mb4'
                }
            
            self._engine = create_engine(
                self.database_url,
                pool_size=5,
                max_overflow=10,
                pool_recycle=3600,
                pool_pre_ping=True,
                connect_args=connect_args
            )
        return self._engine
    
    def test_connection(self) -> bool:
        """Test database connection."""
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("Database connection successful")
            return True
        except Exception as e:
            logger.error(f"Database connection failed: {str(e)}")
            return False
    
    def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> Optional[pd.DataFrame]:
        """Execute SQL query and return results as DataFrame."""
        try:
            logger.info(f"Executing query: {query[:100]}...")
            
            with self.engine.connect() as conn:
                result = pd.read_sql_query(
                    text(query),
                    conn,
                    params=params or {}
                )
            
            # Fix all columns that might cause PyArrow issues
            for col in result.columns:
                try:
                    # Check for problematic data types
                    if result[col].dtype == 'object':
                        # Try to detect if this is a timestamp/datetime column
                        sample_val = result[col].dropna().iloc[0] if not result[col].dropna().empty else None
                        if sample_val and any(word in str(sample_val).lower() for word in ['2023', '2024', '2025', ':']):
                            # Likely a timestamp, convert to string
                            result[col] = result[col].astype(str)
                        elif any(word in col.lower() for word in ['date', 'time', 'created', 'updated']):
                            # Column name suggests timestamp
                            result[col] = result[col].astype(str)
                    elif 'datetime' in str(result[col].dtype).lower() or 'timestamp' in str(result[col].dtype).lower():
                        # Explicit datetime/timestamp types
                        result[col] = result[col].astype(str)
                except Exception as e:
                    # If any conversion fails, continue with next column
                    logger.warning(f"Could not process column {col}: {str(e)}")
                    continue
            
            logger.info(f"Query executed successfully. Rows returned: {len(result)}")
            return result
            
        except Exception as e:
            logger.error(f"Query execution failed: {str(e)}")
            raise
    
    def get_table_names(self) -> List[str]:
        """Get list of all table names in the database."""
        try:
            query = """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = DATABASE()
            ORDER BY table_name;
            """
            result = self.execute_query(query)
            return result['table_name'].tolist() if result is not None else []
        except Exception as e:
            logger.error(f"Failed to get table names: {str(e)}")
            return []
    
    def get_table_schema(self, table_name: str) -> Optional[pd.DataFrame]:
        """Get schema information for a specific table."""
        try:
            query = """
            SELECT 
                column_name,
                data_type,
                is_nullable,
                column_default,
                character_maximum_length
            FROM information_schema.columns 
            WHERE table_name = :table_name
            AND table_schema = DATABASE()
            ORDER BY ordinal_position;
            """
            return self.execute_query(query, {"table_name": table_name})
        except Exception as e:
            logger.error(f"Failed to get schema for table {table_name}: {str(e)}")
            return None
    
    def get_sample_data(self, table_name: str, limit: int = 5) -> Optional[pd.DataFrame]:
        """Get sample data from a table."""
        try:
            query = f"SELECT * FROM {table_name} LIMIT :limit"
            return self.execute_query(query, {"limit": limit})
        except Exception as e:
            logger.error(f"Failed to get sample data for table {table_name}: {str(e)}")
            return None
    
    def close(self) -> None:
        """Close database connections."""
        if self._engine:
            self._engine.dispose()
            self._engine = None
        logger.info("Database connections closed")