"""Database schema management utilities."""

import logging
from typing import List, Dict, Any, Optional
from database.connection import DatabaseManager

logger = logging.getLogger(__name__)


class SchemaManager:
    """Manages database schema information for LLM context."""
    
    def __init__(self, db_manager: DatabaseManager) -> None:
        """Initialize schema manager with database manager."""
        self.db_manager = db_manager
        self._cached_schema: Optional[str] = None
    
    def get_formatted_schema(self, use_cache: bool = True) -> str:
        """Get formatted schema information for LLM consumption."""
        if use_cache and self._cached_schema:
            return self._cached_schema
        
        try:
            schema_info = self._build_schema_info()
            formatted_schema = self._format_schema_for_llm(schema_info)
            
            if use_cache:
                self._cached_schema = formatted_schema
            
            return formatted_schema
            
        except Exception as e:
            logger.error(f"Failed to get formatted schema: {str(e)}")
            return "Schema information unavailable"
    
    def _build_schema_info(self) -> List[Dict[str, Any]]:
        """Build comprehensive schema information."""
        schema_info = []
        
        try:
            table_names = self.db_manager.get_table_names()
            
            for table_name in table_names:
                table_schema = self.db_manager.get_table_schema(table_name)
                sample_data = self.db_manager.get_sample_data(table_name, limit=3)
                
                if table_schema is not None:
                    schema_info.append({
                        'table_name': table_name,
                        'columns': table_schema.to_dict('records'),
                        'sample_data': sample_data.to_dict('records') if sample_data is not None else []
                    })
            
            return schema_info
            
        except Exception as e:
            logger.error(f"Failed to build schema info: {str(e)}")
            return []
    
    def _format_schema_for_llm(self, schema_info: List[Dict[str, Any]]) -> str:
        """Format schema information for LLM consumption."""
        if not schema_info:
            return "No schema information available"
        
        formatted_parts = ["DATABASE SCHEMA INFORMATION:\n"]
        
        for table_info in schema_info:
            table_name = table_info['table_name']
            columns = table_info['columns']
            sample_data = table_info['sample_data']
            
            formatted_parts.append(f"\nTable: {table_name}")
            formatted_parts.append("Columns:")
            
            for col in columns:
                col_info = f"  - {col['column_name']} ({col['data_type']}"
                if col['character_maximum_length']:
                    col_info += f"({col['character_maximum_length']})"
                if col['is_nullable'] == 'NO':
                    col_info += ", NOT NULL"
                if col['column_default']:
                    col_info += f", DEFAULT: {col['column_default']}"
                col_info += ")"
                formatted_parts.append(col_info)
            
            # Add sample data if available
            if sample_data:
                formatted_parts.append("Sample data:")
                for i, row in enumerate(sample_data[:3], 1):
                    sample_values = ", ".join([f"{k}={v}" for k, v in row.items()])
                    formatted_parts.append(f"  Row {i}: {sample_values}")
            
            formatted_parts.append("")  # Empty line between tables
        
        # Add helpful notes
        formatted_parts.extend([
            "\nNOTES:",
            "- Use proper table and column names as shown above",
            "- Add appropriate WHERE clauses to filter data",
            "- Use LIMIT to restrict result set size",
            "- Consider using JOINs when querying related tables",
            "- Use proper PostgreSQL syntax"
        ])
        
        return "\n".join(formatted_parts)
    
    def get_table_relationships(self) -> Dict[str, List[str]]:
        """Get foreign key relationships between tables."""
        try:
            query = """
            SELECT 
                tc.table_name as source_table,
                kcu.column_name as source_column,
                ccu.table_name as target_table,
                ccu.column_name as target_column
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu 
                ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage ccu 
                ON ccu.constraint_name = tc.constraint_name
            WHERE tc.constraint_type = 'FOREIGN KEY'
            AND tc.table_schema = 'public';
            """
            
            result = self.db_manager.execute_query(query)
            relationships = {}
            
            if result is not None:
                for _, row in result.iterrows():
                    source = row['source_table']
                    target = row['target_table']
                    
                    if source not in relationships:
                        relationships[source] = []
                    relationships[source].append(target)
            
            return relationships
            
        except Exception as e:
            logger.error(f"Failed to get table relationships: {str(e)}")
            return {}
    
    def clear_cache(self) -> None:
        """Clear cached schema information."""
        self._cached_schema = None
        logger.info("Schema cache cleared")