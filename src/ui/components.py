"""UI components and widgets for the Streamlit application."""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import logging
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)


class UIComponents:
    """Reusable UI components for the Streamlit application."""
    
    def __init__(self) -> None:
        """Initialize UI components."""
        self.chart_types = {
            'bar': 'Bar Chart',
            'line': 'Line Chart',
            'scatter': 'Scatter Plot',
            'histogram': 'Histogram',
            'box': 'Box Plot',
            'pie': 'Pie Chart'
        }
    
    def display_dataframe_with_stats(self, df: pd.DataFrame) -> None:
        """Display DataFrame with basic statistics."""
        if df is None or df.empty:
            st.warning("No data to display")
            return
        
        # Basic info
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Rows", f"{len(df):,}")
        
        with col2:
            st.metric("Columns", len(df.columns))
        
        with col3:
            memory_usage = df.memory_usage(deep=True).sum() / (1024 * 1024)
            st.metric("Memory", f"{memory_usage:.2f} MB")
        
        with col4:
            numeric_cols = len(df.select_dtypes(include=['number']).columns)
            st.metric("Numeric Columns", numeric_cols)
        
        # Data preview
        st.subheader("Data Preview")
        
        # Show/hide options
        with st.expander("Display Options"):
            show_nulls = st.checkbox("Highlight null values", value=True)
            
            # Handle edge cases for sliders
            max_possible_rows = min(1000, len(df))
            if max_possible_rows <= 10:
                max_rows = max_possible_rows
                st.info(f"Showing all {max_possible_rows} rows")
            else:
                max_rows = st.slider("Max rows to display", 10, max_possible_rows, min(100, max_possible_rows))
            
            max_possible_cols = len(df.columns)
            if max_possible_cols <= 5:
                max_cols = max_possible_cols
                st.info(f"Showing all {max_possible_cols} columns")
            else:
                max_cols = st.slider("Max columns to display", 5, max_possible_cols, min(20, max_possible_cols))
        
        # Display data
        display_df = df.head(max_rows).iloc[:, :max_cols]
        
        if show_nulls:
            # Use a custom styling function that's compatible with current pandas
            def highlight_nulls(val):
                return 'background-color: lightcoral' if pd.isna(val) else ''
            
            st.dataframe(
                display_df.style.map(highlight_nulls),
                width='stretch'
            )
        else:
            st.dataframe(display_df, width='stretch')
        
        # Quick stats
        with st.expander("Quick Statistics"):
            if numeric_cols > 0:
                st.write("**Numeric Columns Summary:**")
                st.dataframe(df.describe(), width='stretch')
            
            # Data types
            st.write("**Column Data Types:**")
            dtype_df = pd.DataFrame({
                'Column': df.columns,
                'Data Type': df.dtypes.astype(str),
                'Non-Null Count': df.count(),
                'Null Count': df.isnull().sum()
            })
            st.dataframe(dtype_df, width='stretch')
    
    def offer_visualization_options(self, df: pd.DataFrame) -> None:
        """Offer visualization options for the DataFrame."""
        if df is None or df.empty:
            return
        
        st.subheader("📊 Data Visualization")
        
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        if not numeric_columns and not categorical_columns:
            st.info("No suitable columns for visualization")
            return
        
        # Store DataFrame in session state to prevent loss during widget changes
        if 'current_dataframe' not in st.session_state:
            st.session_state.current_dataframe = df
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            chart_type = st.selectbox("Chart Type", list(self.chart_types.keys()), 
                                    format_func=lambda x: self.chart_types[x],
                                    key="viz_chart_type")
            
            if chart_type in ['bar', 'line', 'scatter']:
                x_column = st.selectbox("X-axis", categorical_columns + numeric_columns,
                                       key="viz_x_axis")
                y_column = st.selectbox("Y-axis", numeric_columns,
                                       key="viz_y_axis") if numeric_columns else None
                
                if chart_type == 'scatter' and len(numeric_columns) > 1:
                    color_column = st.selectbox("Color by", [None] + categorical_columns + numeric_columns,
                                               key="viz_color_by")
                else:
                    color_column = None
            
            elif chart_type == 'histogram':
                x_column = st.selectbox("Column", numeric_columns,
                                       key="viz_hist_column")
                y_column = None
                color_column = None
                bins = st.slider("Number of bins", 10, 100, 30,
                                key="viz_hist_bins")
            
            elif chart_type == 'box':
                x_column = st.selectbox("Category", categorical_columns,
                                       key="viz_box_category") if categorical_columns else None
                y_column = st.selectbox("Values", numeric_columns,
                                       key="viz_box_values") if numeric_columns else None
                color_column = None
            
            elif chart_type == 'pie':
                x_column = st.selectbox("Category", categorical_columns,
                                       key="viz_pie_category") if categorical_columns else None
                y_column = st.selectbox("Values", numeric_columns,
                                       key="viz_pie_values") if numeric_columns else None
                color_column = None
        
        with col2:
            # Auto-generate chart when options change
            if x_column and (y_column or chart_type in ['histogram', 'pie']):
                try:
                    chart = self._create_chart(df, chart_type, x_column, y_column, color_column, 
                                             locals().get('bins', 30))
                    if chart:
                        st.plotly_chart(chart, width='stretch')
                except Exception as e:
                    st.error(f"Error creating chart: {str(e)}")
            else:
                st.info("Select appropriate columns to generate chart")
    
    def _create_chart(self, df: pd.DataFrame, chart_type: str, x_column: Optional[str], 
                     y_column: Optional[str], color_column: Optional[str], bins: int = 30) -> Optional[go.Figure]:
        """Create a plotly chart based on parameters."""
        try:
            if chart_type == 'bar' and x_column and y_column:
                fig = px.bar(df, x=x_column, y=y_column, color=color_column,
                           title=f"{y_column} by {x_column}")
            
            elif chart_type == 'line' and x_column and y_column:
                fig = px.line(df, x=x_column, y=y_column, color=color_column,
                            title=f"{y_column} over {x_column}")
            
            elif chart_type == 'scatter' and x_column and y_column:
                fig = px.scatter(df, x=x_column, y=y_column, color=color_column,
                               title=f"{y_column} vs {x_column}")
            
            elif chart_type == 'histogram' and x_column:
                fig = px.histogram(df, x=x_column, nbins=bins,
                                 title=f"Distribution of {x_column}")
            
            elif chart_type == 'box' and y_column:
                fig = px.box(df, x=x_column, y=y_column,
                           title=f"Box plot of {y_column}" + (f" by {x_column}" if x_column else ""))
            
            elif chart_type == 'pie' and x_column:
                if y_column:
                    fig = px.pie(df, names=x_column, values=y_column,
                               title=f"{y_column} by {x_column}")
                else:
                    value_counts = df[x_column].value_counts()
                    fig = px.pie(values=value_counts.values, names=value_counts.index,
                               title=f"Distribution of {x_column}")
            
            else:
                return None
            
            # Customize layout
            fig.update_layout(
                showlegend=True,
                height=500,
                margin=dict(l=0, r=0, t=30, b=0)
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Chart creation failed: {str(e)}")
            return None
    
    def display_query_history(self, queries: List[Dict[str, Any]]) -> None:
        """Display query history."""
        if not queries:
            st.info("No query history available")
            return
        
        st.subheader("📋 Query History")
        
        for i, query_info in enumerate(reversed(queries[-10:])):  # Show last 10 queries
            with st.expander(f"Query {len(queries) - i}: {query_info.get('timestamp', 'Unknown time')}"):
                st.code(query_info.get('sql', ''), language='sql')
                
                if query_info.get('execution_time'):
                    st.text(f"Execution time: {query_info['execution_time']:.2f}s")
                
                if query_info.get('row_count'):
                    st.text(f"Rows returned: {query_info['row_count']:,}")
                
                if st.button(f"Rerun Query {len(queries) - i}", key=f"rerun_{i}"):
                    st.session_state['rerun_query'] = query_info.get('sql', '')
    
    def show_error_with_suggestion(self, error_message: str, sql_query: str) -> None:
        """Show error message with helpful suggestions."""
        st.error(f"❌ Query Error: {error_message}")
        
        # Common error patterns and suggestions
        suggestions = []
        
        if "column" in error_message.lower() and "does not exist" in error_message.lower():
            suggestions.append("🔍 Check column names in the schema information above")
            suggestions.append("📝 Verify column name spelling and case sensitivity")
        
        elif "table" in error_message.lower() and "does not exist" in error_message.lower():
            suggestions.append("🔍 Check table names in the schema information")
            suggestions.append("📝 Ensure you're using the correct table name")
        
        elif "syntax error" in error_message.lower():
            suggestions.append("🔧 Check SQL syntax - missing commas, quotes, or parentheses")
            suggestions.append("📖 Verify PostgreSQL-specific syntax")
        
        elif "permission denied" in error_message.lower():
            suggestions.append("🔐 Check database permissions for the current user")
        
        if suggestions:
            st.info("💡 **Suggestions:**")
            for suggestion in suggestions:
                st.write(f"  {suggestion}")
        
        # Option to get AI help (if available)
        if st.button("🤖 Get AI Help with This Error"):
            st.session_state['get_ai_help'] = {
                'error': error_message,
                'query': sql_query
            }