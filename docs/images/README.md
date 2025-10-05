# Screenshots Placeholder

This directory contains application screenshots for the README.md file.

## Required Screenshots:

1. **main-dashboard.png** - Main application interface
2. **schema-browser.png** - Database schema exploration interface
3. **natural-language-query.png** - Natural language query input
4. **sql-generation.png** - Generated SQL query display
5. **query-results.png** - Query results table
6. **data-visualization.png** - Charts and data visualizations
7. **file-upload.png** - File upload interface
8. **data-processing.png** - File processing and preview

## Screenshot Guidelines:

- **Resolution**: Minimum 1200px wide for main screenshots
- **Format**: PNG for best quality
- **Content**: Use realistic sample data
- **UI State**: Show the application in a clean, professional state
- **Browser**: Use a clean browser window (hide bookmarks, extensions)

## To Capture Screenshots:

1. Run the application: `docker-compose up -d` or `poetry run streamlit run src/app.py`
2. Open http://localhost:8503
3. Navigate through the application features
4. Capture screenshots of each major feature
5. Save them in this directory with the exact filenames listed above

Run `./scripts/capture_screenshots.sh` for detailed instructions.