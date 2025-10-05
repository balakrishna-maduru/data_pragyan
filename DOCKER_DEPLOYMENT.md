# Data Pragyan - Docker Deployment Guide

This guide provides comprehensive instructions for deploying Data Pragyan using Docker in different environments.

## 🚀 Quick Start

### Prerequisites
- Docker Engine 20.10+
- Docker Compose 2.0+
- Git

### One-Command Deployment

```bash
# Clone and deploy in development mode
git clone <repository-url>
cd data_pragyan
./scripts/deploy.sh deploy dev
```

## 📋 Deployment Options

### 1. Development Environment
```bash
# Start development environment with live reload
./scripts/deploy.sh deploy dev

# Or manually
docker-compose -f docker-compose.dev.yml up -d
```

**Features:**
- Live code reload
- Database exposed on port 3306
- phpMyAdmin for database management
- Redis for caching
- Debug logging enabled

**URLs:**
- 📊 Data Pragyan: http://localhost:8501
- 🗄️ phpMyAdmin: http://localhost:8080
- 🔴 Redis: localhost:6379

### 2. Production Environment
```bash
# Start production environment
./scripts/deploy.sh deploy prod

# Or manually
docker-compose -f docker-compose.prod.yml up -d
```

**Features:**
- Nginx reverse proxy
- SSL support (configure certificates)
- Automated backups
- Resource limits
- Security hardening
- Health checks

**URLs:**
- 📊 Data Pragyan: http://localhost (port 80)
- 🔒 HTTPS: https://localhost (port 443, if SSL configured)

### 3. Default Environment
```bash
# Start with default settings
./scripts/deploy.sh deploy

# Or manually
docker-compose up -d
```

## ⚙️ Configuration

### Environment Variables

Copy and customize the environment file:
```bash
cp .env.example .env
```

**Required Variables:**
```bash
# Google Gemini API (Required)
GOOGLE_API_KEY=your_google_api_key_here

# Database Security (Change defaults!)
MYSQL_ROOT_PASSWORD=your_secure_root_password
MYSQL_PASSWORD=your_secure_password

# Application Settings
ENVIRONMENT=production  # development, production, staging
```

**Optional Variables:**
```bash
# Ports
APP_PORT=8501
PHPMYADMIN_PORT=8080
NGINX_PORT=80

# Security
SECRET_KEY=your_secret_key_here
SSL_CERT_PATH=/etc/nginx/ssl/cert.pem
SSL_KEY_PATH=/etc/nginx/ssl/key.pem

# Resources
MAX_UPLOAD_SIZE=200MB
MAX_MEMORY_USAGE=2G
```

### SSL Configuration (Production)

1. Place your SSL certificates:
```bash
mkdir -p ssl
cp your-cert.pem ssl/cert.pem
cp your-key.pem ssl/key.pem
```

2. Update nginx.conf to enable HTTPS section

3. Restart with production profile:
```bash
./scripts/deploy.sh restart prod
```

## 🛠️ Management Commands

### Deployment Management
```bash
# Deploy specific environment
./scripts/deploy.sh deploy [dev|prod]

# Stop all services
./scripts/deploy.sh stop

# Restart services
./scripts/deploy.sh restart [dev|prod]

# Check service status
./scripts/deploy.sh status

# View logs
./scripts/deploy.sh logs
```

### Database Management
```bash
# Create database backup
./scripts/deploy.sh backup

# Manual backup
docker-compose exec mariadb mysqldump -u root -p data_pragyan > backup.sql

# Restore from backup
docker-compose exec -T mariadb mysql -u root -p data_pragyan < backup.sql
```

### Updates
```bash
# Update application
./scripts/deploy.sh update

# Manual update
git pull
docker-compose build --no-cache
docker-compose up -d
```

## 📊 Monitoring & Logs

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f data-pragyan
docker-compose logs -f mariadb
docker-compose logs -f nginx
```

### Health Checks
```bash
# Check service health
docker-compose ps

# Application health
curl http://localhost:8501/_stcore/health

# Nginx health (production)
curl http://localhost/health
```

## 🔧 Troubleshooting

### Common Issues

1. **Port Already in Use**
```bash
# Stop conflicting services
sudo lsof -ti:8501 | xargs kill -9

# Or change ports in .env file
APP_PORT=8502
```

2. **Permission Issues**
```bash
# Fix file permissions
sudo chown -R $USER:$USER uploads logs backups
chmod 755 uploads logs backups
```

3. **Database Connection Failed**
```bash
# Check database status
docker-compose exec mariadb mysql -u root -p -e "SELECT 1"

# Reset database
docker-compose down -v
docker-compose up -d
```

4. **Out of Memory**
```bash
# Check resource usage
docker stats

# Increase Docker memory limit or adjust MAX_MEMORY_USAGE
```

### Reset Everything
```bash
# Complete reset (WARNING: Deletes all data)
docker-compose down -v
docker system prune -a -f
./scripts/deploy.sh deploy
```

## 🔐 Security Considerations

### Production Security Checklist

- [ ] Change default passwords in .env
- [ ] Configure SSL certificates
- [ ] Restrict database access (remove port exposure)
- [ ] Set up firewall rules
- [ ] Enable automatic security updates
- [ ] Configure backup encryption
- [ ] Set up monitoring and alerting
- [ ] Review and update dependencies regularly

### Network Security
```bash
# Production: Remove database port exposure
# Comment out in docker-compose.prod.yml:
# ports:
#   - "3306:3306"
```

## 📦 Docker Profiles

Use profiles to start specific service combinations:

```bash
# Start with admin tools (phpMyAdmin)
docker-compose --profile admin up -d

# Start production with nginx
docker-compose -f docker-compose.prod.yml --profile production up -d
```

## 🔄 Backup Strategy

### Automated Backups
- Daily backups at 2 AM (configurable)
- 30-day retention (configurable)
- Compressed storage
- Health monitoring

### Manual Backup
```bash
# Create immediate backup
./scripts/deploy.sh backup

# Restore specific backup
docker-compose exec -T mariadb mysql -u root -p data_pragyan < backups/backup_file.sql
```

## 📈 Scaling (Advanced)

### Horizontal Scaling
```yaml
# In docker-compose.yml
services:
  data-pragyan:
    scale: 3  # Run 3 instances
```

### Load Balancing
Configure nginx upstream with multiple app instances for high availability.

## 🆘 Support

### Getting Help
1. Check logs: `./scripts/deploy.sh logs`
2. Verify configuration: `./scripts/deploy.sh status`
3. Review environment variables in `.env`
4. Check Docker resources: `docker system df`

### Useful Commands
```bash
# Container shell access
docker-compose exec data-pragyan bash
docker-compose exec mariadb bash

# Resource monitoring
docker stats
docker system df

# Network inspection
docker network ls
docker network inspect data_pragyan_data_pragyan_network
```

---

## 📝 Summary

This Docker setup provides:
- ✅ Easy one-command deployment
- ✅ Development and production environments
- ✅ Automated backups and health checks
- ✅ SSL/HTTPS support
- ✅ Resource management and scaling
- ✅ Comprehensive logging and monitoring
- ✅ Security best practices

Choose your deployment mode and run:
```bash
./scripts/deploy.sh deploy [dev|prod]
```