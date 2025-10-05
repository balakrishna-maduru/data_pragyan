# Docker Setup Guide for Data Pragyan

## Current Status
✅ **Application is running successfully** at http://localhost:8503  
❌ **Database connection failed** - MariaDB not available  

## Quick Setup (5 minutes)

### Step 1: Install Docker Desktop
1. Download Docker Desktop from: https://www.docker.com/products/docker-desktop
2. Install and start Docker Desktop
3. Verify installation by running in terminal:
   ```bash
   docker --version
   ```

### Step 2: Start MariaDB Database
1. Open terminal and navigate to your project:
   ```bash
   cd /Users/balakrishnamaduru/Documents/git_hub/data_pragyan
   ```

2. Start the MariaDB database:
   ```bash
   docker compose up mariadb -d
   ```

3. Wait about 30 seconds for MariaDB to fully start

### Step 3: Verify Database Connection
1. Refresh your browser at http://localhost:8503
2. You should now see "Database" option in the sidebar
3. Optional: Access phpMyAdmin at http://localhost:8080
   - Username: `root`
   - Password: `rootpassword`

## What You Get With Database

### Without Database (Current)
- ✅ File upload and analysis
- ✅ CSV/Excel data parsing
- ✅ Data visualization
- ❌ Natural language to SQL
- ❌ Database queries
- ❌ Data persistence

### With Database
- ✅ Everything above, plus:
- ✅ Natural language to SQL conversion
- ✅ Database queries
- ✅ Data persistence
- ✅ Sample data to query
- ✅ Schema exploration

## Troubleshooting

### Docker not starting
```bash
# Check if Docker is running
docker ps

# If not running, start Docker Desktop application
```

### Database connection still failing
```bash
# Check if MariaDB container is running
docker ps

# Restart MariaDB if needed
docker compose restart mariadb

# Check logs if issues persist
docker compose logs mariadb
```

### Reset everything
```bash
# Stop and remove all containers
docker compose down

# Start fresh
docker compose up mariadb -d
```

## Sample Data Included

Once connected, you can query:
- **employees** table (10 sample employees)
- **departments** table (5 departments)
- **projects** table (5 projects)
- **sales** table (10 sales records)

Try asking: *"Show me all employees in the Engineering department"*