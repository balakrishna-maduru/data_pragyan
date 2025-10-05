#!/bin/bash

# Development setup script for Data Pragyan

echo "🔧 Setting up Data Pragyan development environment..."

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "❌ Poetry is not installed. Please install Poetry first:"
    echo "   curl -sSL https://install.python-poetry.org | python3 -"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies with Poetry..."
poetry install

# Copy environment file
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration"
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p uploads logs

# Set up pre-commit hooks
echo "🔗 Setting up pre-commit hooks..."
poetry run pre-commit install

# Run initial tests
echo "🧪 Running initial tests..."
poetry run pytest --version
poetry run pytest tests/ -v

echo "✅ Development environment setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Start PostgreSQL database: docker-compose up postgres -d"
echo "3. Run the application: poetry run streamlit run src/app.py"
echo "4. Access the application at http://localhost:8501"