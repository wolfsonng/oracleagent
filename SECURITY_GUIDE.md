# Security Guide - Oracle Agent

## 🚨 CRITICAL: Credential Protection

### What's Safe to Upload to Git ✅

**SAFE FILES (will be committed):**
- `app.py` - Main application code
- `config.py` - Configuration logic (no real credentials)
- `oracle_utils.py` - Database utilities
- `Dockerfile` - Container configuration
- `docker-compose.yml` - Service orchestration
- `requirements.txt` - Python dependencies
- `instantclient_23_8/` - Oracle client libraries
- `deploy/deploy.sh` - Deployment script
- `AUTO_DEPLOY_SETUP.md` - Setup instructions
- `env.template` - Template file (no real credentials)
- `encrypt_credentials.py` - Encryption helper script

### What's NOT Safe to Upload to Git ❌

**PROTECTED FILES (will be ignored):**
- `.env` - Real environment variables with credentials
- `envexample.py` - Example with potential credentials
- `gkey.py` - Encryption keys
- `deploy/webhook.sh` - Webhook handler with secrets
- `*.log` - Log files that might contain sensitive data

## 🔐 How to Protect Credentials

### 1. Environment Variables (Recommended)

**Never commit real credentials to Git!**

Instead, use environment variables:

```bash
# Set these in your deployment environment
export DB1_ORACLE_HOST=your-real-db1-host
export DB1_ORACLE_USER=your-real-db1-username
export DB2_ORACLE_HOST=your-real-db2-host
export DB2_ORACLE_USER=your-real-db2-username
export ENCRYPTION_KEY=your-real-encryption-key
export DB1_ENCRYPTED_SECRET=your-real-db1-encrypted-secret
export DB1_ENCRYPTED_ORACLE_PASSWORD=your-real-db1-encrypted-password
export DB2_ENCRYPTED_SECRET=your-real-db2-encrypted-secret
export DB2_ENCRYPTED_ORACLE_PASSWORD=your-real-db2-encrypted-password
```

### 2. Template Files

Use the template file for documentation:

```bash
# Copy template and fill in real values
cp env.template .env
nano .env  # Edit with real credentials
```

### 3. Generate Encrypted Credentials

Use the encryption helper script:

```bash
# Generate encrypted credentials
python encrypt_credentials.py

# This will prompt for your passwords and generate encrypted values
```

## 📁 File Structure

```
oracleagent/
├── ✅ SAFE TO COMMIT
│   ├── app.py
│   ├── config.py
│   ├── oracle_utils.py
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── requirements.txt
│   ├── instantclient_23_8/
│   ├── deploy/deploy.sh
│   ├── env.template
│   ├── encrypt_credentials.py
│   └── AUTO_DEPLOY_SETUP.md
│
├── ❌ PROTECTED (in .gitignore)
│   ├── .env
│   ├── gkey.py
│   ├── deploy/webhook.sh
│   └── *.log
```

## 🚀 Deployment Security

### 1. VM Setup

```bash
# On your VM, create .env file with real credentials
nano .env

# Set proper permissions
chmod 600 .env
```

### 2. Environment Variables

```bash
# Set in your deployment environment
export DB1_ORACLE_HOST=real-host
export DB1_ORACLE_USER=real-username
export ENCRYPTION_KEY=real-key
export DB1_ENCRYPTED_ORACLE_PASSWORD=real-encrypted-password
# ... etc
```

### 3. Docker Deployment

```bash
# Use environment variables, not .env files
docker run -e DB1_ORACLE_HOST=real-host -e ENCRYPTION_KEY=real-key ...
```

## 🔍 Verification

### Check What Will Be Committed

```bash
# See what files will be uploaded
git status

# See what's in staging
git diff --cached

# Check if sensitive files are ignored
git check-ignore .env
```

### Test Before Committing

```bash
# Dry run - see what would be committed
git add .
git status  # Review carefully!

# If you see sensitive files, remove them
git reset
git add .  # .gitignore will prevent sensitive files
```

## 🛡️ Best Practices

1. **Never commit credentials** - Use environment variables
2. **Use templates** - Provide examples without real data
3. **Regular audits** - Check what's in your repository
4. **Rotate secrets** - Change passwords regularly
5. **Limit access** - Use IP whitelisting
6. **Monitor logs** - Watch for suspicious activity
7. **Encrypt passwords** - Use the encryption helper script

## 🚨 Emergency Response

If you accidentally commit credentials:

1. **Immediately change passwords** in your databases
2. **Remove from Git history**:
   ```bash
   git filter-branch --force --index-filter \
   'git rm --cached --ignore-unmatch .env' \
   --prune-empty --tag-name-filter cat -- --all
   ```
3. **Force push** to remove from remote:
   ```bash
   git push origin --force
   ```
4. **Notify team** about the security incident

## 📋 Pre-Commit Checklist

Before pushing to Git:

- [ ] No `.env` files in staging
- [ ] No real credentials in any files
- [ ] Template file only contains examples
- [ ] `.gitignore` is properly configured
- [ ] All sensitive files are ignored
- [ ] Test deployment with environment variables
- [ ] Use encrypted credentials only

## 🔒 Additional Security

1. **Encryption at rest** - Use encrypted storage
2. **Network security** - Use VPNs and firewalls
3. **Access control** - Implement proper authentication
4. **Audit logging** - Track all access attempts
5. **Regular updates** - Keep dependencies updated

**Remember: Security is everyone's responsibility!** 🔐 