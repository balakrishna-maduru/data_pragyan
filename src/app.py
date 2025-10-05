"""Main Streamlit application for Data Pragyan."""

import streamlit as st
import pandas as pd
import logging
from pathlib import Path
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add src to path for imports
sys.path.append(str(Path(__file__).parent))

from config.settings import Settings
from database.connection import DatabaseManager
from utils.llm_processor import NLToSQLProcessor
from utils.parsers import FileParser
from utils.schema_manager import SchemaManager
from ui.components import UIComponents


def configure_page():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title="Data Pragyan",
        page_icon="🔧",
        layout="wide",
        initial_sidebar_state="expanded"
    )


def initialize_session_state():
    """Initialize session state variables."""
    if 'generated_sql' not in st.session_state:
        st.session_state.generated_sql = ""
    if 'schema_info' not in st.session_state:
        st.session_state.schema_info = None
    if 'db_connected' not in st.session_state:
        st.session_state.db_connected = False
    if 'query_results' not in st.session_state:
        st.session_state.query_results = None
    if 'last_executed_sql' not in st.session_state:
        st.session_state.last_executed_sql = ""
    if 'query_explanation' not in st.session_state:
        st.session_state.query_explanation = ""


@st.cache_resource
def get_components():
    """Initialize and cache application components."""
    settings = Settings()
    
    # Try to connect to database, but don't fail if it's not available
    db_manager = None
    try:
        db_manager = DatabaseManager(settings.database_url)
        if not db_manager.test_connection():
            st.warning("⚠️ Database connection failed. Some features may be limited.")
            db_manager = None
    except Exception as e:
        st.error(f"❌ Failed to connect to database: {str(e)}")
        st.info("💡 To run with full database features:")
        st.code("""
# 1. Install Docker Desktop from https://www.docker.com/products/docker-desktop
# 2. Run these commands in terminal:
cd /path/to/data_pragyan
docker compose up mariadb -d
# 3. Refresh this page
        """)
        db_manager = None
    
    nl_processor = NLToSQLProcessor(settings)
    schema_manager = SchemaManager(db_manager) if db_manager else None
    file_parser = FileParser()
    ui_components = UIComponents()
    
    return settings, db_manager, nl_processor, schema_manager, file_parser, ui_components


def main():
    """Main application entry point."""
    configure_page()
    initialize_session_state()
    
    # Get cached components
    settings, db_manager, nl_processor, schema_manager, file_parser, ui_components = get_components()
    
    # App header
    col1, col2 = st.columns([2, 3])
    
    with col1:
        # Title with database status indicator
        title_col1, title_col2 = st.columns([4, 1])
        with title_col1:
            st.title("🔧 Data Pragyan")
        with title_col2:
            if db_manager is not None:
                st.markdown(
                    '<div style="margin-top: 20px;"><span style="color: #00ff00; font-size: 20px;" title="Database connected successfully!">●</span></div>', 
                    unsafe_allow_html=True
                )
        st.markdown("*AI-powered data exploration and analysis tool*")
    
    with col2:
        st.markdown("### 💡 Quick Query Ideas:")
        st.markdown("""
        **How to use:**
        1. 🔍 Select a table from the dropdown in Schema Browser
        2. 👀 Browse columns and sample data  
        3. 💬 Click any suggestion button to auto-fill your query
        4. 🪄 Generate SQL or ask in plain English
        """)
    
    # Sidebar navigation
    with st.sidebar:
        st.header("Navigation")
        
        # Only show database option if database is available
        if db_manager is not None:
            data_source = st.selectbox(
                "Choose Data Source", 
                ["Database", "File Upload"],
                key="data_source"
            )
            
            if data_source == "Database":
                query_method = st.selectbox(
                    "Query Method", 
                    ["Natural Language", "SQL Query", "Schema Browser"],
                    key="query_method"
                )
        else:
            st.info("📁 File Upload Mode Only")
            data_source = "File Upload"
    
    # Main content area
    if data_source == "Database" and db_manager is not None:
        handle_database_queries(
            query_method, db_manager, nl_processor, 
            schema_manager, ui_components
        )
    else:
        handle_file_upload(file_parser, ui_components)


def handle_database_queries(query_method, db_manager, nl_processor, schema_manager, ui_components):
    """Handle database query operations."""
    try:
        # Test database connection
        if not st.session_state.db_connected:
            with st.spinner("Connecting to database..."):
                if db_manager.test_connection():
                    st.session_state.db_connected = True
                else:
                    st.error("❌ Failed to connect to database. Please check your configuration.")
                    return
        
        if query_method == "Natural Language":
            handle_natural_language_query(db_manager, nl_processor, schema_manager, ui_components)
        elif query_method == "Schema Browser":
            handle_schema_browser(db_manager, schema_manager, ui_components)
        else:
            handle_sql_query(db_manager, ui_components)
            
    except Exception as e:
        logger.error(f"Database query error: {str(e)}")
        st.error(f"Database error: {str(e)}")


def handle_schema_browser(db_manager, schema_manager, ui_components):
    """Handle dedicated schema browser interface."""
    st.subheader("📋 Database Schema Browser")
    
    # Build schema info if not available
    if 'schema_tables' not in st.session_state:
        st.session_state.schema_tables = schema_manager._build_schema_info()
    
    if st.session_state.get('schema_tables'):
        # Table selector with search
        table_names = [table['table_name'] for table in st.session_state.schema_tables]
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Searchable table dropdown
            selected_table = st.selectbox(
                "🔍 Select a table to explore:",
                [""] + table_names,
                key="schema_table_select",
                help="Choose a table to see its columns and sample data"
            )
        
        with col2:
            # Quick search/filter
            search_term = st.text_input(
                "🔎 Search tables/columns:",
                key="schema_search",
                placeholder="e.g., customer, order, date..."
            )
        
        # Display selected table details
        if selected_table:
            table_info = next((t for t in st.session_state.schema_tables if t['table_name'] == selected_table), None)
            if table_info:
                st.subheader(f"📊 Table: `{selected_table}`")
                
                # Columns information
                st.write("**Columns:**")
                col_data = []
                for col in table_info['columns']:
                    col_type = col['data_type']
                    if col.get('character_maximum_length'):
                        col_type += f"({col['character_maximum_length']})"
                    
                    nullable = "NULL" if col['is_nullable'] == 'YES' else "NOT NULL"
                    default = col.get('column_default', 'None')
                    
                    col_data.append({
                        'Column': col['column_name'],
                        'Type': col_type,
                        'Nullable': nullable,
                        'Default': default
                    })
                
                cols_df = pd.DataFrame(col_data)
                st.dataframe(cols_df, width='stretch', hide_index=True)
                
                # Sample data
                if table_info.get('sample_data'):
                    st.write("**Sample Data:**")
                    sample_df = pd.DataFrame(table_info['sample_data'])
                    st.dataframe(sample_df, width='stretch', hide_index=True)
                
                # Quick query suggestions
                st.write("**💡 Quick Query Ideas:**")
                suggestions = [
                    f"Show me all data from {selected_table}",
                    f"Count total records in {selected_table}",
                    f"Show me the latest entries from {selected_table}"
                ]
                
                if 'customer' in selected_table.lower():
                    suggestions.append(f"Find customers from a specific city")
                elif 'order' in selected_table.lower():
                    suggestions.append(f"Show orders from the last month")
                elif 'product' in selected_table.lower():
                    suggestions.append(f"List products by category")
                
                st.write("**🚀 Use these suggestions in Natural Language or SQL Query tabs:**")
                for suggestion in suggestions:
                    st.code(f"💬 {suggestion}")
        
        # Search results
        elif search_term:
            st.write(f"🔍 **Search results for:** `{search_term}`")
            matching_tables = []
            
            for table in st.session_state.schema_tables:
                table_name = table['table_name']
                # Check if search term matches table name
                if search_term.lower() in table_name.lower():
                    matching_tables.append({
                        'Table': table_name,
                        'Match': 'Table name',
                        'Columns': len(table['columns'])
                    })
                else:
                    # Check if search term matches any column name
                    matching_cols = [col['column_name'] for col in table['columns'] 
                                   if search_term.lower() in col['column_name'].lower()]
                    if matching_cols:
                        matching_tables.append({
                            'Table': table_name,
                            'Match': f"Columns: {', '.join(matching_cols)}",
                            'Columns': len(table['columns'])
                        })
            
            if matching_tables:
                search_df = pd.DataFrame(matching_tables)
                st.dataframe(search_df, width='stretch', hide_index=True)
            else:
                st.info(f"No tables or columns found matching '{search_term}'")
        
        else:
            # Overview when nothing selected
            st.write("**📋 Database Overview:**")
            overview_data = []
            for table in st.session_state.schema_tables:
                overview_data.append({
                    'Table': table['table_name'],
                    'Columns': len(table['columns']),
                    'Has Sample Data': 'Yes' if table.get('sample_data') else 'No'
                })
            
            overview_df = pd.DataFrame(overview_data)
            st.dataframe(overview_df, width='stretch', hide_index=True)
            
            st.info("💡 Select a table above to see detailed column information and sample data")
    else:
        st.error("Failed to load database schema information.")


def handle_natural_language_query(db_manager, nl_processor, schema_manager, ui_components):
    """Handle natural language to SQL conversion and execution."""
    st.subheader("🗣️ Ask Your Data in Plain English")
    
    # Get schema information
    if st.session_state.schema_info is None:
        with st.spinner("Loading database schema..."):
            st.session_state.schema_info = schema_manager.get_formatted_schema()
            # Also store structured schema for the browser
            if 'schema_tables' not in st.session_state:
                st.session_state.schema_tables = schema_manager._build_schema_info()
    
    # Tip for using Schema Browser
    st.info(" **Tip:** Use the 'Schema Browser' tab to explore tables and get query suggestions!")
    
    # Natural language input
    # Check if there's a suggested query to pre-fill
    initial_query = st.session_state.get('suggested_query', '')
    if initial_query:
        st.info(f"💡 Applied suggestion: {initial_query}")
        # Clear the suggestion after using it
        st.session_state.suggested_query = ''
    
    natural_query = st.text_area(
        "What would you like to know?",
        value=initial_query,
        placeholder="e.g., Show me all customers from New York who made purchases last month",
        height=100,
        key="nl_query"
    )
    
    # Generate SQL button
    if st.button("🪄 Generate SQL", type="primary"):
        if natural_query.strip():
            with st.spinner("Converting to SQL..."):
                try:
                    sql_query = nl_processor.generate_sql(
                        natural_query, 
                        st.session_state.schema_info
                    )
                    st.session_state.generated_sql = sql_query
                    st.session_state['just_generated'] = True  # Flag to auto-execute
                    st.success("SQL generated successfully!")
                except Exception as e:
                    logger.error(f"SQL generation error: {str(e)}")
                    st.error(f"Error generating SQL: {str(e)}")
        else:
            st.warning("Please enter a question first.")
    
    # Display generated SQL and execute options (if SQL is available)
    if st.session_state.generated_sql:
        # TOP: Generated SQL Query Section
        st.subheader("📝 Generated SQL Query")
        sql_query = st.text_area(
            "Review and edit if needed:",
            value=st.session_state.generated_sql,
            height=150,
            key="sql_editor"
        )
        
        # Update the stored SQL if user edits it
        if sql_query != st.session_state.generated_sql:
            st.session_state.generated_sql = sql_query
        
        # Execute buttons
        col1, col2 = st.columns([1, 1])
        
        with col1:
            execute_button = st.button("▶️ Execute Query", type="primary")
        
        with col2:
            if sql_query != st.session_state.get('original_generated_sql', ''):
                execute_edited_button = st.button("🔄 Execute Edited Query", type="secondary")
            else:
                execute_edited_button = False
        
        # Execute if button clicked OR if we just generated new SQL
        should_execute = (execute_button or execute_edited_button or 
                         (natural_query and st.session_state.get('just_generated', False)))
        
        if should_execute:
            # Reset the just_generated flag
            st.session_state['just_generated'] = False
            # Store original for comparison
            st.session_state['original_generated_sql'] = st.session_state.generated_sql
            # Force execution by clearing the last executed SQL
            st.session_state['last_executed_sql'] = ""
        
        # ALWAYS show results if they exist (persistent display)
        execute_sql_query_with_results_display(sql_query, db_manager, nl_processor, ui_components)


def execute_sql_query_with_results_display(sql_query, db_manager, nl_processor, ui_components):
    """Execute SQL query and display results in the center area."""
    if sql_query.strip():
        # Only execute if SQL has changed or no results cached
        if (sql_query != st.session_state.get('last_executed_sql', '') or 
            st.session_state.query_results is None):
            
            with st.spinner("Executing query..."):
                try:
                    df = db_manager.execute_query(sql_query)
                    
                    if df is not None and not df.empty:
                        # Store results in session state
                        st.session_state.query_results = df
                        st.session_state.last_executed_sql = sql_query
                        
                        # Generate explanation if using NL processor
                        if nl_processor:
                            try:
                                explanation = nl_processor.explain_query(sql_query)
                                st.session_state.query_explanation = explanation
                            except Exception as e:
                                logger.warning(f"Could not explain query: {str(e)}")
                                st.session_state.query_explanation = ""
                    else:
                        st.session_state.query_results = None
                        st.warning("Query executed successfully but returned no results.")
                        return
                        
                except Exception as e:
                    logger.error(f"Query execution error: {str(e)}")
                    st.error(f"Error executing query: {str(e)}")
                    st.session_state.query_results = None
                    return
    
    # Always display results if available (from cache or fresh execution)
    if st.session_state.query_results is not None:
        # CENTER: Query Results
        st.subheader("📊 Query Results")
        ui_components.display_dataframe_with_stats(st.session_state.query_results)
        
        # Show cached explanation
        if st.session_state.get('query_explanation'):
            st.info(f"**Query Explanation:** {st.session_state.query_explanation}")
        
        # CENTER: Data Visualization (persistent)
        ui_components.offer_visualization_options(st.session_state.query_results)
    else:
        if sql_query.strip():
            st.warning("Please execute a query to see results.")


def handle_sql_query(db_manager, ui_components):
    """Handle direct SQL query execution."""
    st.subheader("💻 Direct SQL Query")
    
    sql_query = st.text_area(
        "Enter your SQL query:",
        value="SELECT * FROM customers LIMIT 10;",
        height=150,
        key="direct_sql"
    )
    
    if st.button("▶️ Run Query", type="primary"):
        execute_sql_query(sql_query, db_manager, None, ui_components)


def execute_sql_query(sql_query, db_manager, nl_processor, ui_components):
    """Execute SQL query and display results."""
    if sql_query.strip():
        with st.spinner("Executing query..."):
            try:
                df = db_manager.execute_query(sql_query)
                
                if df is not None and not df.empty:
                    st.subheader("📊 Query Results")
                    ui_components.display_dataframe_with_stats(df)
                    
                    # Show query explanation if using NL processor
                    if nl_processor:
                        try:
                            explanation = nl_processor.explain_query(sql_query)
                            st.info(f"**Query Explanation:** {explanation}")
                        except Exception as e:
                            logger.warning(f"Could not explain query: {str(e)}")
                    
                    # Offer visualization options
                    ui_components.offer_visualization_options(df)
                else:
                    st.warning("Query executed successfully but returned no results.")
                    
            except Exception as e:
                logger.error(f"Query execution error: {str(e)}")
                st.error(f"Error executing query: {str(e)}")
    else:
        st.warning("Please enter a SQL query.")


def handle_file_upload(file_parser, ui_components):
    """Handle file upload and analysis."""
    st.subheader("📁 File Upload & Analysis")
    
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['csv', 'xlsx', 'xls', 'json'],
        key="file_upload"
    )
    
    if uploaded_file is not None:
        try:
            with st.spinner("Processing file..."):
                df = file_parser.parse_file(uploaded_file)
                
            st.success(f"✅ File loaded successfully! Shape: {df.shape}")
            ui_components.display_dataframe_with_stats(df)
            ui_components.offer_visualization_options(df)
            
            # Future: Natural language queries on uploaded data
            st.subheader("🤖 Ask Questions About Your Data")
            data_question = st.text_input(
                "What would you like to know about this data?",
                key="file_nl_query"
            )
            if data_question:
                st.info("🚧 Feature coming soon: Natural language queries on uploaded data!")
                
        except Exception as e:
            logger.error(f"File processing error: {str(e)}")
            st.error(f"Error processing file: {str(e)}")


if __name__ == "__main__":
    main()