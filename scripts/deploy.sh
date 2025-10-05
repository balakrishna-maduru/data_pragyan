#!/bin/bash

# Data Pragyan - Easy Deployment Script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    log_success "Docker and Docker Compose are installed"
}

# Create necessary directories
create_directories() {
    log_info "Creating necessary directories..."
    mkdir -p uploads logs backups ssl
    log_success "Directories created"
}

# Setup environment file
setup_env() {
    if [ ! -f .env ]; then
        log_info "Creating .env file from template..."
        cp .env.example .env
        log_warning "Please edit .env file with your configuration before running the application"
        log_warning "Important: Set GOOGLE_API_KEY and secure passwords!"
        echo
        read -p "Do you want to edit .env now? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            ${EDITOR:-nano} .env
        fi
    else
        log_info ".env file already exists"
    fi
}

# Deploy function
deploy() {
    local env=${1:-development}
    
    log_info "Deploying Data Pragyan in $env mode..."
    
    case $env in
        "development"|"dev")
            log_info "Starting development environment..."
            docker-compose -f docker-compose.dev.yml up -d
            ;;
        "production"|"prod")
            log_info "Starting production environment..."
            docker-compose -f docker-compose.prod.yml up -d
            ;;
        *)
            log_info "Starting default environment..."
            docker-compose up -d
            ;;
    esac
    
    log_success "Deployment started!"
    log_info "Waiting for services to be ready..."
    sleep 30
    
    # Check if services are running
    if docker-compose ps | grep -q "Up"; then
        log_success "Services are running!"
        echo
        log_info "🌐 Application URLs:"
        case $env in
            "development"|"dev")
                echo "   📊 Data Pragyan: http://localhost:8501"
                echo "   🗄️  phpMyAdmin: http://localhost:8080"
                ;;
            "production"|"prod")
                echo "   📊 Data Pragyan: http://localhost"
                echo "   🗄️  Database access via secure connection only"
                ;;
            *)
                echo "   📊 Data Pragyan: http://localhost:8501"
                echo "   🗄️  phpMyAdmin: http://localhost:8080"
                ;;
        esac
        echo
    else
        log_error "Some services failed to start. Check logs with: docker-compose logs"
        exit 1
    fi
}

# Stop function
stop() {
    log_info "Stopping Data Pragyan services..."
    docker-compose down
    log_success "Services stopped"
}

# Backup function
backup() {
    log_info "Creating database backup..."
    timestamp=$(date +%Y%m%d_%H%M%S)
    backup_file="backups/data_pragyan_backup_$timestamp.sql"
    
    docker-compose exec mariadb mysqldump -u root -p data_pragyan > $backup_file
    log_success "Backup created: $backup_file"
}

# Update function
update() {
    log_info "Updating Data Pragyan..."
    git pull
    docker-compose build --no-cache
    docker-compose up -d
    log_success "Update completed"
}

# Logs function
logs() {
    docker-compose logs -f
}

# Status function
status() {
    log_info "Data Pragyan Service Status:"
    docker-compose ps
}

# Help function
show_help() {
    echo "Data Pragyan - Easy Deployment Script"
    echo
    echo "Usage: $0 [command] [options]"
    echo
    echo "Commands:"
    echo "  deploy [env]    Deploy the application (env: dev, prod, default)"
    echo "  stop            Stop all services"
    echo "  restart [env]   Restart services"
    echo "  backup          Create database backup"
    echo "  update          Update application and restart"
    echo "  logs            Show application logs"
    echo "  status          Show service status"
    echo "  help            Show this help message"
    echo
    echo "Examples:"
    echo "  $0 deploy dev       # Deploy development environment"
    echo "  $0 deploy prod      # Deploy production environment"
    echo "  $0 restart          # Restart with default settings"
    echo "  $0 backup           # Create database backup"
    echo
}

# Main script
main() {
    check_docker
    create_directories
    
    case ${1:-help} in
        "deploy")
            setup_env
            deploy ${2:-development}
            ;;
        "stop")
            stop
            ;;
        "restart")
            stop
            sleep 5
            deploy ${2:-development}
            ;;
        "backup")
            backup
            ;;
        "update")
            update
            ;;
        "logs")
            logs
            ;;
        "status")
            status
            ;;
        "help"|*)
            show_help
            ;;
    esac
}

# Run main function with all arguments
main "$@"