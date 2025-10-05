# 🔧 Data Pragyan

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org) [![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io) [![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com) [![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An **AI-powered data exploration and analysis tool** that seamlessly connects natural language queries to SQL databases, processes uploaded files, and provides interactive visualizations - all through an intuitive web interface.

## 📸 Application Preview

<div align="center">

### Main Interface
![Main Dashboard](docs/images/main-dashboard.png)

### Key Features in Action
<table>
  <tr>
    <td align="center">
      <img src="docs/images/schema-browser.png" width="400px" alt="Schema Browser"/>
      <br><b>Interactive Schema Browser</b>
    </td>
    <td align="center">
      <img src="docs/images/natural-language-query.png" width="400px" alt="Natural Language Query"/>
      <br><b>Natural Language to SQL</b>
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="docs/images/query-results.png" width="400px" alt="Query Results"/>
      <br><b>Formatted Results & Charts</b>
    </td>
    <td align="center">
      <img src="docs/images/data-visualization.png" width="400px" alt="Data Visualization"/>
      <br><b>Interactive Visualizations</b>
    </td>
  </tr>
</table>

</div>

## 🌟 Key Features

### 🤖 AI-Powered Query Generation
- **Natural Language to SQL**: Convert plain English questions to SQL using Google Gemini Flash 2.5
- **Interactive Schema Browser**: Explore database tables, columns, and sample data in a dedicated tab
- **Smart Query Suggestions**: Get contextual query ideas based on selected tables
- **Query Explanation**: Understand what your generated SQL does in plain English

### 📊 Multi-Source Data Analysis
- **MariaDB Integration**: Optimized connection to MariaDB with performance monitoring
- **File Processing**: Upload and analyze CSV, Excel (.xlsx, .xls), JSON, and text files
- **Real-time Results**: Instant query execution with formatted, persistent results
- **Data Visualization**: Interactive charts and graphs with Plotly integration

### 🎯 Enhanced User Experience
- **Separate Tabs**: Dedicated Schema Browser and Query tabs for organized workflow
- **Green Dot Status**: Real-time database connection indicator with hover details
- **Persistent Results**: Query results remain visible while exploring other features
- **Optimized Layout**: Clean, responsive design for better usability

### 🚀 Production Ready
- **Docker Compose**: Complete containerized setup with dev/prod environments
- **SSL Support**: Production-ready HTTPS configuration with Nginx
- **Health Monitoring**: Built-in status checks, logging, and performance metrics
- **Automated Backups**: Scheduled database backups and restore procedures

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Features Guide](#-features-guide)
- [Docker Deployment](#-docker-deployment)
- [Configuration](#-configuration)
- [Development](#-development)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/balakrishna-maduru/data_pragyan.git
cd data_pragyan

# Copy environment template
cp .env.example .env

# Add your Google Gemini API key to .env
echo "GEMINI_API_KEY=your_api_key_here" >> .env

# Start with Docker Compose
docker-compose up -d

# Access the application
open http://localhost:8503
```

### Option 2: Development Setup

```bash
# Install Poetry (if not installed)
curl -sSL https://install.python-poetry.org | python3 - 

# Install dependencies
poetry install

# Configure environment
cp .env.example .env

# Run the application
poetry run streamlit run src/app.py --server.port 8503
```

## 📦 Installation

### Prerequisites

- **Python 3.10+**
- **Poetry** (for dependency management)
- **Docker & Docker Compose** (for containerized deployment)
- **Google Gemini API Key** (for AI features)
### 1. Clone Repository

```bash
git clone https://github.com/balakrishna-maduru/data_pragyan.git
cd data_pragyan
```

### 2. Environment Setup

```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 - 

# Install dependencies
poetry install

# Install additional Excel support
poetry add openpyxl
```

### 3. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit configuration
nano .env
```

Required environment variables:

```bash
# Google Gemini Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# MariaDB Configuration
MARIADB_HOST=localhost
MARIADB_PORT=3306
MARIADB_DATABASE=data_pragyan
MARIADB_USER=data_pragyan
MARIADB_PASSWORD=your_secure_password

# Application Settings
STREAMLIT_PORT=8503
DEBUG=True
```

### 4. Database Setup

```bash
# Using Docker (Recommended)
docker-compose up -d mariadb

# Or install MariaDB locally
# macOS:
brew install mariadb
brew services start mariadb

# Ubuntu/Debian:
sudo apt-get install mariadb-server
sudo systemctl start mariadb
```

## ✨ Features Guide

### 🖥️ Application Screenshots

#### Main Dashboard
![Main Dashboard](docs/images/main-dashboard.png)
*Clean, intuitive interface with real-time database connection status*

#### Schema Browser
![Schema Browser](docs/images/schema-browser.png)
*Interactive database schema exploration with table details and sample data*

#### Natural Language Query Interface
![Natural Language Query](docs/images/natural-language-query.png)
*Convert plain English questions into optimized SQL queries*

#### Query Results & Visualization
![Query Results](docs/images/query-results.png)
*Formatted results with automatic chart generation and export options*

### 🤖 Natural Language Queries

1. **Open Schema Browser Tab**
   - Click "Schema Browser" to explore your database
   - Browse tables and columns with search functionality
   - View sample data and table statistics

2. **Ask in Plain English**
   ```
   "Show me all customers from California who made orders last month"
   "What are the top 5 products by sales volume?"
   "Find all orders with amounts greater than $1000"
   ```

3. **Review Generated SQL**
   - AI generates optimized SQL queries
   - Edit queries before execution
   - Get explanations of what queries do

4. **Execute and Visualize**
   - Run queries with one click
   - View results in formatted tables
   - Create interactive charts automatically

### 📁 File Upload & Analysis

#### File Upload Interface
![File Upload](docs/images/file-upload.png)
*Drag-and-drop interface supporting CSV, Excel, and JSON files*

#### Data Processing & Preview
![Data Processing](docs/images/data-processing.png)
*Automatic file type detection with instant data preview and statistics*

1. **Upload Data Files**
   - Drag and drop CSV, Excel, or JSON files
   - Automatic file type detection
   - Instant data preview with statistics

2. **Query Uploaded Data**
   - Use natural language on uploaded files
   - Generate pandas operations
   - Export results and visualizations

### 📊 Data Visualization

#### Interactive Charts & Graphs
![Data Visualization](docs/images/data-visualization.png)
*AI-powered chart recommendations with interactive features*

- **Automatic Chart Suggestions**: AI recommends optimal chart types
- **Interactive Plots**: Zoom, filter, and export visualizations
- **Multiple Chart Types**: Bar, line, scatter, histogram, pie charts
- **Export Options**: PNG, SVG, PDF, and HTML formats

## 🐳 Docker Deployment

### Development Environment

```bash
# Start development stack
docker-compose -f docker-compose.dev.yml up -d

# View logs
docker-compose logs -f app

# Access application
open http://localhost:8503
```

### Production Environment

```bash
# Start production stack with SSL
docker-compose -f docker-compose.prod.yml up -d

# Check status
docker-compose ps

# Access application
open https://yourdomain.com
```

### Docker Commands

```bash
# Build custom image
docker build -t data-pragyan:latest .

# Run standalone container
docker run -p 8503:8503 \
  -e GEMINI_API_KEY=your_key \
  data-pragyan:latest

# Scale application
docker-compose up -d --scale app=3

# Backup database
docker-compose exec mariadb mysqldump -u root -p data_pragyan > backup.sql

# Restore database
docker-compose exec -T mariadb mysql -u root -p data_pragyan < backup.sql
```

## ⚙️ Configuration

### Environment Variables

```bash
# Core Configuration
GEMINI_API_KEY=your_gemini_api_key_here
STREAMLIT_PORT=8503
DEBUG=False

# MariaDB Configuration
MARIADB_HOST=mariadb
MARIADB_PORT=3306
MARIADB_DATABASE=data_pragyan
MARIADB_USER=data_pragyan
MARIADB_PASSWORD=secure_password
MARIADB_ROOT_PASSWORD=root_password

# Application Settings
MAX_UPLOAD_SIZE=100
QUERY_TIMEOUT=30
CACHE_TTL=3600
LOG_LEVEL=INFO
```

### Streamlit Configuration

Create `.streamlit/config.toml`:

```toml
[server]
port = 8503
address = "0.0.0.0"
maxUploadSize = 100
enableCORS = true

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
```

## 🔌 API Integration

### Google Gemini Setup

1. **Get API Key**
   ```bash
   # Visit Google AI Studio
   https://aistudio.google.com/app/apikey
   
   # Create new API key
   echo "GEMINI_API_KEY=your_key_here" >> .env
   ```

2. **Test Connection**
   ```python
   import google.generativeai as genai
   
   genai.configure(api_key="your_api_key")
   model = genai.GenerativeModel('gemini-2.0-flash-exp')
   response = model.generate_content("Hello, Gemini!")
   print(response.text)
   ```

## 🛠 Development

### Project Structure

```
data-pragyan/
├── src/                          # Source code
│   ├── app.py                    # Main Streamlit application
│   ├── database/
│   │   ├── connection.py         # Database connection management
│   │   └── schema_manager.py     # Schema introspection
│   ├── utils/
│   │   ├── llm_processor.py      # Gemini AI integration
│   │   ├── parsers.py            # File parsing utilities
│   │   └── validators.py         # Input validation
│   └── ui/
│       ├── components.py         # Reusable UI components
│       └── styles.py             # CSS styling
├── docker-compose.yml            # Docker development stack
├── docker-compose.dev.yml        # Development environment
├── docker-compose.prod.yml       # Production environment
├── sql/                          # Database scripts
├── scripts/                      # Utility scripts
├── tests/                        # Test suite
├── .streamlit/                   # Streamlit configuration
├── pyproject.toml               # Poetry dependencies
├── .env.example                 # Environment template
└── README.md                    # This file
```

### Development Commands

```bash
# Install development dependencies
poetry install --with dev

# Run tests
poetry run pytest

# Code formatting
poetry run black src/

# Type checking
poetry run mypy src/

# Run application with hot reload
poetry run streamlit run src/app.py --server.port 8503
```

## 🔧 Troubleshooting

### Common Issues

#### Database Connection Issues

**Problem**: `mariadb.OperationalError: Can't connect to MariaDB server`

```bash
# Check if MariaDB is running
docker-compose ps mariadb

# View MariaDB logs
docker-compose logs mariadb

# Restart MariaDB
docker-compose restart mariadb
```

#### Gemini API Issues

**Problem**: `google.api_core.exceptions.Unauthenticated: 401 API key not valid`

```bash
# Verify API key in environment
echo $GEMINI_API_KEY

# Update .env file
nano .env
```

#### File Upload Issues

**Problem**: `ModuleNotFoundError: No module named 'openpyxl'`

```bash
# Install Excel support
poetry add openpyxl

# Or for Docker deployment
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Debug Mode

```bash
# Set debug environment
export DEBUG=True
export LOG_LEVEL=DEBUG

# Run with debug
poetry run streamlit run src/app.py --logger.level debug
```

### Health Checks

```bash
# Check application health
curl http://localhost:8503/_stcore/health

# Check database health
docker-compose exec mariadb mysqladmin ping -u root -p
```

## 📊 Monitoring & Performance

### Application Metrics
- Query execution time tracking
- Database connection monitoring
- File upload success rates
- User interaction analytics

### Health Checks
- Database connectivity status (green dot indicator)
- Gemini API availability monitoring
- File system access validation
- Real-time performance metrics

## 🔒 Security Features

- Environment-based credential management
- File upload validation and sanitization
- SQL injection prevention with parameterized queries
- Docker security best practices
- Production SSL/TLS configuration

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### Development Workflow

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make changes and test**
   ```bash
   poetry run pytest
   poetry run black src/
   poetry run mypy src/
   ```
4. **Commit with conventional commits**
   ```bash
   git commit -m "feat: add amazing feature"
   ```
5. **Push and create PR**

### Code Style

- **Black** for code formatting
- **mypy** for type checking
- **pytest** for testing
- **Conventional Commits** for commit messages

## 📚 Additional Resources

- **Google Gemini Documentation**: [AI Model Integration Guide](https://ai.google.dev/docs)
- **MariaDB Documentation**: [Database Setup Guide](https://mariadb.org/documentation/)
- **Streamlit Documentation**: [Web Framework Guide](https://docs.streamlit.io/)
- **Docker Documentation**: [Containerization Guide](https://docs.docker.com/)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini** for advanced AI language model
- **MariaDB** for robust database performance
- **Streamlit** for the intuitive web framework
- **Docker** for containerization excellence
- **Poetry** for modern Python dependency management

---

## 📞 Support & Community

- **Issues**: [GitHub Issues](https://github.com/balakrishna-maduru/data_pragyan/issues)
- **Discussions**: [GitHub Discussions](https://github.com/balakrishna-maduru/data_pragyan/discussions)
- **Docker Hub**: [Official Images](https://hub.docker.com/r/balakrishna-maduru/data_pragyan)

---

**🚀 Ready to transform your data workflow? Deploy Data Pragyan today!**

*Made with ❤️ for the modern data community*