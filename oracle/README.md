# Oracle Database Support

This directory contains Oracle Instant Client libraries and JDBC drivers for connecting to Oracle databases.

## Setup

### Automatic Setup (Recommended)
The system will automatically detect and use the Oracle libraries in this directory. No additional configuration is needed.

### Manual Setup (Alternative)
If you prefer to use system-installed Oracle libraries, set one of these environment variables:

```bash
# Option 1: Set ORACLE_HOME to your Oracle installation
export ORACLE_HOME=/path/to/oracle/instantclient

# Option 2: Set ORACLE_LIB_PATH to the library directory
export ORACLE_LIB_PATH=/path/to/oracle/instantclient
```

## Connection Methods

The reporting system supports three Oracle connection methods:

### 1. Service Name (Recommended)
```json
{
  "host": "your-oracle-host",
  "port": "1521",
  "username": "your_username",
  "password": "your_password",
  "service_name": "your_service_name"
}
```

### 2. SID (Legacy)
```json
{
  "host": "your-oracle-host",
  "port": "1521",
  "username": "your_username",
  "password": "your_password",
  "sid": "your_sid"
}
```

### 3. TNS Name
```json
{
  "username": "your_username",
  "password": "your_password",
  "tns_name": "your_tns_name"
}
```

## Testing Oracle Connections

Use the `/api/reporting/connections/test-oracle` endpoint to test Oracle connections:

```bash
curl -X POST http://localhost:5000/api/reporting/connections/test-oracle \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "host": "your-oracle-host",
    "port": "1521",
    "username": "your_username",
    "password": "your_password",
    "service_name": "your_service_name"
  }'
```

## Files Included

- `ojdbc8.jar`, `ojdbc11.jar` - Oracle JDBC drivers
- `libclntsh.dylib*` - Oracle client libraries
- `libocci.dylib*` - Oracle C++ libraries
- `libnnz.dylib` - Oracle networking libraries
- Other Oracle Instant Client components

## Troubleshooting

1. **"Failed to initialize Oracle client"**: Check that the Oracle libraries are accessible
2. **"Connection failed"**: Verify your connection parameters (host, port, service_name/sid)
3. **"ORA-12541: TNS:no listener"**: Check that the Oracle database is running and accessible 