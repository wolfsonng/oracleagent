#!/bin/bash

# Auto-deployment script for Oracle Agent
# This script pulls latest code, rebuilds Docker containers, and restarts services

set -e  # Exit on any error

echo "🚀 Starting auto-deployment..."

# Configuration
PROJECT_DIR="/home/oracleagent/oracleagent"
DOCKER_COMPOSE_FILE="$PROJECT_DIR/docker-compose.yml"
LOG_FILE="$PROJECT_DIR/deploy.log"

# Log function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Change to project directory
cd "$PROJECT_DIR" || {
    log "❌ Failed to change to project directory: $PROJECT_DIR"
    exit 1
}

# Pull latest code from Git
log "📥 Pulling latest code from Git..."
git pull origin main

# Stop existing containers
log "🛑 Stopping existing containers..."
docker-compose down

# Build and start new containers
log "🔨 Building and starting new containers..."
docker-compose up -d --build

# Wait for containers to be healthy
log "⏳ Waiting for containers to be healthy..."
sleep 30

# Check container status
log "🔍 Checking container status..."
docker-compose ps

# Test health endpoints
log "🏥 Testing health endpoints..."
if curl -f http://localhost:5001/health > /dev/null 2>&1; then
    log "✅ Database 1 agent is healthy"
else
    log "❌ Database 1 agent health check failed"
fi

if curl -f http://localhost:5002/health > /dev/null 2>&1; then
    log "✅ Database 2 agent is healthy"
else
    log "❌ Database 2 agent health check failed"
fi

log "🎉 Deployment completed successfully!"