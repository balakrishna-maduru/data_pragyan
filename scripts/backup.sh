#!/bin/bash

# Database Backup Script for Data Pragyan

set -e

# Configuration
BACKUP_DIR="/backups"
RETENTION_DAYS=${BACKUP_RETENTION_DAYS:-30}
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DB_NAME=${MYSQL_DATABASE:-data_pragyan}
DB_USER="root"
DB_PASSWORD=${MYSQL_ROOT_PASSWORD}

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Generate backup filename
BACKUP_FILE="$BACKUP_DIR/data_pragyan_backup_$TIMESTAMP.sql"

echo "[$(date)] Starting database backup..."

# Create database backup
mysqldump -h mariadb -u $DB_USER -p$DB_PASSWORD \
    --single-transaction \
    --routines \
    --triggers \
    --events \
    --hex-blob \
    $DB_NAME > $BACKUP_FILE

# Compress the backup
gzip $BACKUP_FILE

echo "[$(date)] Backup completed: ${BACKUP_FILE}.gz"

# Clean up old backups
echo "[$(date)] Cleaning up backups older than $RETENTION_DAYS days..."
find $BACKUP_DIR -name "data_pragyan_backup_*.sql.gz" -type f -mtime +$RETENTION_DAYS -delete

# Log backup size
BACKUP_SIZE=$(du -h "${BACKUP_FILE}.gz" | cut -f1)
echo "[$(date)] Backup size: $BACKUP_SIZE"

echo "[$(date)] Backup process completed successfully"
