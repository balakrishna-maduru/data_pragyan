"""Natural Language to SQL conversion using Google Gemini."""

import google.generativeai as genai
import logging
from typing import Optional
from config.settings import Settings

logger = logging.getLogger(__name__)


class NLToSQLProcessor:
    """Processes natural language queries and converts them to SQL using Google Gemini."""
    
    def __init__(self, settings: Settings) -> None:
        """Initialize the NL to SQL processor."""
        self.settings = settings
        
        # Check for Google API key in environment or settings
        google_api_key = getattr(settings, 'google_api_key', None) or getattr(settings, 'openai_api_key', None)
        
        if not google_api_key:
            logger.warning("Google API key not provided. NL to SQL functionality will be limited.")
        
        # Initialize Google Gemini client
        if google_api_key:
            genai.configure(api_key=google_api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        else:
            self.model = None
    
    def generate_sql(self, natural_query: str, schema_info: str) -> str:
        """Convert natural language query to SQL."""
        if not self.model:
            raise ValueError("Google API key not configured")
        
        try:
            prompt = self._build_sql_prompt(natural_query, schema_info)
            
            response = self.model.generate_content(prompt)
            
            sql_query = response.text.strip()
            
            # Clean up the response (remove markdown code blocks if present)
            if sql_query.startswith("```sql"):
                sql_query = sql_query[6:]
            if sql_query.startswith("```"):
                sql_query = sql_query[3:]
            if sql_query.endswith("```"):
                sql_query = sql_query[:-3]
            
            logger.info(f"Generated SQL for query: {natural_query[:50]}...")
            return sql_query.strip()
            
        except Exception as e:
            logger.error(f"Failed to generate SQL: {str(e)}")
            raise
    
    def explain_query(self, sql_query: str) -> str:
        """Explain what the SQL query does in plain English."""
        if not self.model:
            return "Query explanation unavailable (Google API key not configured)"
        
        try:
            prompt = f"""
            Explain what this SQL query does in simple, non-technical terms:
            
            {sql_query}
            
            Provide a clear, concise explanation that a business user would understand.
            """
            
            response = self.model.generate_content(prompt)
            
            explanation = response.text.strip()
            logger.info("Generated query explanation")
            return explanation
            
        except Exception as e:
            logger.error(f"Failed to explain query: {str(e)}")
            return f"Could not explain query: {str(e)}"
    
    def _build_sql_prompt(self, natural_query: str, schema_info: str) -> str:
        """Build the prompt for SQL generation."""
        return f"""
You are an expert SQL developer. Convert the following natural language query to a valid MariaDB/MySQL SQL query.

Database Schema Information:
{schema_info}

IMPORTANT RULES:
1. Return ONLY the SQL query, no explanations, no markdown formatting, no code blocks
2. Use proper MariaDB/MySQL syntax
3. For complex queries involving counts or aggregations, use appropriate GROUP BY and HAVING clauses
4. For "customers who ordered only X" queries, use COUNT() with GROUP BY and HAVING
5. Always use proper table aliases for joins (c for customers, o for orders, etc.)
6. Include appropriate LIMIT clauses for large result sets (default LIMIT 100)
7. Use proper table and column names exactly as shown in the schema
8. For date/time comparisons, use proper MySQL date functions
9. Always use INNER JOIN, LEFT JOIN, or RIGHT JOIN explicitly - never implicit joins

EXAMPLES OF COMPLEX QUERIES:
- "customers who ordered only 1": SELECT c.* FROM customers c INNER JOIN (SELECT customer_id FROM orders GROUP BY customer_id HAVING COUNT(*) = 1) single_orders ON c.id = single_orders.customer_id LIMIT 100;
- "customers with most orders": SELECT c.*, COUNT(o.id) as order_count FROM customers c LEFT JOIN orders o ON c.id = o.customer_id GROUP BY c.id ORDER BY order_count DESC LIMIT 10;
- "customer information for those who ordered exactly once": SELECT c.* FROM customers c INNER JOIN (SELECT customer_id FROM orders GROUP BY customer_id HAVING COUNT(*) = 1) single_orders ON c.id = single_orders.customer_id LIMIT 100;

IMPORTANT: When asked about customers, ALWAYS return full customer information (c.* or customers.*), not just customer_id.

Natural Language Query: "{natural_query}"

Generate the SQL query:"""
    
    def suggest_improvements(self, sql_query: str) -> str:
        """Suggest improvements for the SQL query."""
        if not self.model:
            return "Query improvement suggestions unavailable (Google API key not configured)"
        
        try:
            prompt = f"""
            Analyze this SQL query and suggest improvements for performance, readability, or best practices:
            
            {sql_query}
            
            Provide specific, actionable suggestions.
            """
            
            response = self.model.generate_content(prompt)
            
            suggestions = response.text.strip()
            logger.info("Generated query improvement suggestions")
            return suggestions
            
        except Exception as e:
            logger.error(f"Failed to generate suggestions: {str(e)}")
            return f"Could not generate suggestions: {str(e)}"