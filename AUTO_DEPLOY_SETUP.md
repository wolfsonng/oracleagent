# Auto-Deployment Setup for Oracle Agent

## Overview

This setup provides:
- **Git-based auto-deployment** on every commit to main branch
- **Multiple database connections** (2 separate Oracle databases)
- **Docker containers** for each database connection
- **Health monitoring** and automatic restarts

## Architecture

```
GitHub Repository
       ↓
   Webhook/CI
       ↓
   VM Server
       ↓
   Docker Containers
   ├── oracleagent-db1 (Port 5001)
   └── oracleagent-db2 (Port 5002)
```

## 1. VM Setup

### 1.1. Install Prerequisites

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install Git
sudo apt install git -y

# Install curl (for health checks)
sudo apt install curl -y
```

### 1.2. Create Deployment User

```bash
# Create user
sudo useradd -m -s /bin/bash oracleagent
sudo usermod -aG docker oracleagent

# Switch to user
sudo su - oracleagent
```

### 1.3. Clone Repository

```bash
# Clone your repository
git clone https://github.com/yourusername/oracleagent.git
cd oracleagent

# Make scripts executable
chmod +x deploy/deploy.sh
chmod +x deploy/webhook.sh
```

## 2. Environment Configuration

### 2.1. Set Environment Variables

Create a `.env` file in the project root:

```bash
# Copy from configs and modify
cp configs/db1.env .env

# Edit with your actual values
nano .env
```

### 2.2. Configure Both Databases

Your `.env` file should contain:

```bash
# Database 1 Configuration
DB1_ORACLE_HOST=your-db1-host
DB1_ORACLE_PORT=1521
DB1_ORACLE_SERVICE=your-db1-service
DB1_ORACLE_USER=your-db1-username
DB1_ORACLE_PASSWORD=your-db1-password

# Database 2 Configuration
DB2_ORACLE_HOST=your-db2-host
DB2_ORACLE_PORT=1521
DB2_ORACLE_SERVICE=your-db2-service
DB2_ORACLE_USER=your-db2-username
DB2_ORACLE_PASSWORD=your-db2-password

# Agent Security (encrypted)
ENCRYPTION_KEY=your-encryption-key
DB1_ENCRYPTED_SECRET=your-db1-encrypted-secret
DB1_ENCRYPTED_ORACLE_PASSWORD=your-db1-encrypted-password
DB2_ENCRYPTED_SECRET=your-db2-encrypted-secret
DB2_ENCRYPTED_ORACLE_PASSWORD=your-db2-encrypted-password

# Debug Mode
DEBUG_AGENT=true

# IP Whitelist (optional)
ALLOWED_IPS=192.168.1.100,10.0.0.50
```

## 3. Auto-Deployment Setup

### 3.1. Option A: GitHub Webhook (Recommended)

#### Set up webhook server:

```bash
# Install nginx for webhook handling
sudo apt install nginx -y

# Create webhook configuration
sudo nano /etc/nginx/sites-available/webhook
```

Add this configuration:

```nginx
server {
    listen 80;
    server_name your-vm-ip;

    location /webhook {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/webhook /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Set up webhook server
sudo nano /etc/systemd/system/webhook.service
```

Add this service configuration:

```ini
[Unit]
Description=GitHub Webhook Server
After=network.target

[Service]
Type=simple
User=oracleagent
WorkingDirectory=/home/oracleagent/oracleagent
ExecStart=/home/oracleagent/oracleagent/deploy/webhook.sh
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Start webhook service
sudo systemctl daemon-reload
sudo systemctl enable webhook
sudo systemctl start webhook
```

#### Configure GitHub Webhook:

1. Go to your GitHub repository
2. Settings → Webhooks → Add webhook
3. Payload URL: `http://your-vm-ip/webhook`
4. Content type: `application/json`
5. Secret: `your-webhook-secret`
6. Events: Just the push event
7. Active: ✓

### 3.2. Option B: GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to VM

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - name: Deploy to VM
      uses: appleboy/ssh-action@v0.1.5
      with:
        host: ${{ secrets.VM_HOST }}
        username: ${{ secrets.VM_USER }}
        key: ${{ secrets.VM_SSH_KEY }}
        script: |
          cd /home/oracleagent/oracleagent
          ./deploy/deploy.sh
```

## 4. Initial Deployment

### 4.1. Test Deployment

```bash
# Test the deployment script
./deploy/deploy.sh

# Check container status
docker-compose ps

# Test endpoints
curl http://localhost:5001/health
curl http://localhost:5002/health
```

### 4.2. Test Database Connections

```bash
# Test Database 1
curl -X POST http://localhost:5001/run-query \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: your-db1-secret" \
  -d '{"sql": "SELECT 1 FROM DUAL"}'

# Test Database 2
curl -X POST http://localhost:5002/run-query \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: your-db2-secret" \
  -d '{"sql": "SELECT 1 FROM DUAL"}'
```

## 5. Monitoring and Maintenance

### 5.1. View Logs

```bash
# View deployment logs
tail -f deploy.log

# View webhook logs
tail -f webhook.log

# View container logs
docker-compose logs -f oracleagent-db1
docker-compose logs -f oracleagent-db2
```

### 5.2. Manual Operations

```bash
# Restart all services
docker-compose restart

# Update and redeploy
git pull
docker-compose up -d --build

# Stop all services
docker-compose down

# Check container health
docker-compose ps
```

## 6. Security Considerations

1. **Firewall**: Only open ports 80 (webhook) and 5001-5002 (agents)
2. **SSH**: Use key-based authentication only
3. **Secrets**: Never commit `.env` files to Git
4. **Updates**: Regularly update Docker images and system packages
5. **Monitoring**: Set up log monitoring and alerting

## 7. Troubleshooting

### Common Issues:

1. **Webhook not triggering**: Check nginx logs and webhook service status
2. **Container not starting**: Check Docker logs and environment variables
3. **Database connection failed**: Verify credentials and network connectivity
4. **Port conflicts**: Ensure ports 5001 and 5002 are available

### Debug Commands:

```bash
# Check service status
sudo systemctl status webhook
sudo systemctl status nginx

# Check Docker status
docker-compose ps
docker-compose logs

# Test webhook manually
curl -X POST http://localhost:8080/webhook \
  -H "Content-Type: application/json" \
  -d '{"ref":"refs/heads/main"}'
```

## 8. Usage

After setup, your agents will be available at:

- **Database 1**: `http://your-vm-ip:5001/run-query`
- **Database 2**: `http://your-vm-ip:5002/run-query`

Each commit to the main branch will automatically:
1. Pull the latest code
2. Rebuild Docker containers
3. Restart services
4. Verify health status

Your auto-deployment system is now ready! 🚀 