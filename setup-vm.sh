#!/bin/bash

# Oracle Agent VM Setup Script
# Run this script on your VM to configure and deploy the agent

set -e

echo "🚀 Oracle Agent VM Setup"
echo "========================"

# Configuration
PROJECT_DIR="/home/oracleagent/oracleagent"
ENV_FILE="$PROJECT_DIR/.env"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as oracleagent user
if [ "$USER" != "oracleagent" ]; then
    print_warning "This script should be run as the oracleagent user"
    print_status "Switching to oracleagent user..."
    sudo su - oracleagent -c "cd $PROJECT_DIR && $0"
    exit 0
fi

# Check if project directory exists
if [ ! -d "$PROJECT_DIR" ]; then
    print_error "Project directory not found: $PROJECT_DIR"
    print_status "Please clone the repository first:"
    echo "git clone https://github.com/yourusername/oracleagent.git $PROJECT_DIR"
    exit 1
fi

cd "$PROJECT_DIR"

# Check if .env file exists
if [ -f "$ENV_FILE" ]; then
    print_warning ".env file already exists. Do you want to overwrite it? (y/N)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        print_status "Keeping existing .env file"
    else
        print_status "Backing up existing .env file..."
        cp "$ENV_FILE" "${ENV_FILE}.backup.$(date +%Y%m%d_%H%M%S)"
    fi
fi

# Create .env file from template
print_status "Creating .env file from template..."
cp env.template "$ENV_FILE"

# Prompt for database credentials
echo ""
print_status "Please enter your database credentials:"
echo ""

# Database 1
echo "=== Database 1 Configuration ==="
read -p "DB1 Oracle Host: " db1_host
read -p "DB1 Oracle Port [1521]: " db1_port
db1_port=${db1_port:-1521}
read -p "DB1 Oracle Service: " db1_service
read -p "DB1 Oracle User: " db1_user

# Database 2
echo ""
echo "=== Database 2 Configuration ==="
read -p "DB2 Oracle Host: " db2_host
read -p "DB2 Oracle Port [1521]: " db2_port
db2_port=${db2_port:-1521}
read -p "DB2 Oracle Service: " db2_service
read -p "DB2 Oracle User: " db2_user

# Security
echo ""
echo "=== Security Configuration ==="
read -s -p "Encryption Key: " encryption_key
echo ""
read -s -p "DB1 Encrypted Secret: " db1_encrypted_secret
echo ""
read -s -p "DB1 Encrypted Oracle Password: " db1_encrypted_oracle_password
echo ""
read -s -p "DB2 Encrypted Secret: " db2_encrypted_secret
echo ""
read -s -p "DB2 Encrypted Oracle Password: " db2_encrypted_oracle_password
echo ""

# Update .env file with real values
print_status "Updating .env file with provided credentials..."

# Use sed to replace placeholder values
sed -i "s/your-db1-host/$db1_host/g" "$ENV_FILE"
sed -i "s/1521/$db1_port/g" "$ENV_FILE"
sed -i "s/your-db1-service/$db1_service/g" "$ENV_FILE"
sed -i "s/your-db1-username/$db1_user/g" "$ENV_FILE"

# Add DB2 configuration
cat >> "$ENV_FILE" << EOF

# Database 2 Configuration
DB2_ORACLE_HOST=$db2_host
DB2_ORACLE_PORT=$db2_port
DB2_ORACLE_SERVICE=$db2_service
DB2_ORACLE_USER=$db2_user

# Encrypted Credentials (Security)
ENCRYPTION_KEY=$encryption_key
DB1_ENCRYPTED_SECRET=$db1_encrypted_secret
DB1_ENCRYPTED_ORACLE_PASSWORD=$db1_encrypted_oracle_password
DB2_ENCRYPTED_SECRET=$db2_encrypted_secret
DB2_ENCRYPTED_ORACLE_PASSWORD=$db2_encrypted_oracle_password

# Debug Mode
DEBUG_AGENT=true

# IP Whitelist (optional)
ALLOWED_IPS=
EOF

# Set proper permissions
chmod 600 "$ENV_FILE"

print_status ".env file created successfully!"

# Make deployment script executable
chmod +x deploy/deploy.sh

# Deploy the application
print_status "Deploying Oracle Agent..."
./deploy/deploy.sh

print_status "Setup completed successfully!"
echo ""
print_status "Your Oracle Agent is now running on:"
echo "  - Database 1: http://$(hostname -I | awk '{print $1}'):5001"
echo "  - Database 2: http://$(hostname -I | awk '{print $1}'):5002"
echo ""
print_status "To test the connections:"
echo "  curl http://$(hostname -I | awk '{print $1}'):5001/health"
echo "  curl http://$(hostname -I | awk '{print $1}'):5002/health"