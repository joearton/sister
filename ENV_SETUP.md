# Sister API Client - Environment Configuration Guide

## Overview
Sister API client now uses environment variables for configuration instead of `config.json`. This provides better security, easier deployment, and follows modern development practices.

## 🚀 Quick Setup

### 1. Create Environment File
```bash
# Copy the example file
cp env.example .env

# Edit with your credentials
nano .env
```

### 2. Fill in Your Credentials
```bash
# Required variables
SISTER_URL=https://sister.umko.ac.id
SISTER_USERNAME=your_developer_username
SISTER_PASSWORD=your_developer_password
SISTER_ID_PENGGUNA=your_developer_id_pengguna

# Optional variables
USE_SANDBOX=true
CACHE_EXPIRATION_DAYS=1
AUTO_CLEANUP_CACHE=false
```

## 📋 Environment Variables

### Required Variables
| Variable | Description | Example |
|----------|-------------|---------|
| `SISTER_URL` | Your Sister instance URL | `https://sister.umko.ac.id` |
| `SISTER_USERNAME` | Developer username | `developer_user` |
| `SISTER_PASSWORD` | Developer password | `your_password` |
| `SISTER_ID_PENGGUNA` | Developer ID | `12345` |

### Optional Variables
| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `USE_SANDBOX` | Use sandbox environment | `true` | `true` or `false` |
| `CACHE_EXPIRATION_DAYS` | Cache expiration in days | `1` | `7` |
| `AUTO_CLEANUP_CACHE` | Enable auto cache cleanup | `false` | `true` or `false` |
| `API_TIMEOUT_SECONDS` | API request timeout | `30` | `60` |
| `MAX_RETRIES` | Maximum retry attempts | `3` | `5` |

## 🔧 Configuration Examples

### Basic Configuration
```bash
# .env
SISTER_URL=https://sister.umko.ac.id
SISTER_USERNAME=developer_user
SISTER_PASSWORD=secure_password
SISTER_ID_PENGGUNA=12345
```

### Advanced Configuration
```bash
# .env
SISTER_URL=https://sister.umko.ac.id
SISTER_USERNAME=developer_user
SISTER_PASSWORD=secure_password
SISTER_ID_PENGGUNA=12345

# Cache settings
CACHE_EXPIRATION_DAYS=7
AUTO_CLEANUP_CACHE=true

# API settings
API_TIMEOUT_SECONDS=60
MAX_RETRIES=5

# Environment
USE_SANDBOX=false
```

### Development Configuration
```bash
# .env
SISTER_URL=https://sister-dev.umko.ac.id
SISTER_USERNAME=dev_user
SISTER_PASSWORD=dev_password
SISTER_ID_PENGGUNA=dev_123

# Development settings
USE_SANDBOX=true
CACHE_EXPIRATION_DAYS=1
AUTO_CLEANUP_CACHE=true
API_TIMEOUT_SECONDS=30
MAX_RETRIES=3
```

## 🛡️ Security Best Practices

### 1. Never Commit .env Files
```bash
# Add to .gitignore
echo ".env" >> .gitignore
echo "*.env" >> .gitignore
```

### 2. Use Strong Passwords
```bash
# Good password example
SISTER_PASSWORD=MySecureP@ssw0rd2024!

# Avoid weak passwords
SISTER_PASSWORD=password123  # ❌ Bad
```

### 3. Environment-Specific Files
```bash
# Development
cp env.example .env.development

# Production
cp env.example .env.production

# Staging
cp env.example .env.staging
```

### 4. Use Environment Variables in Production
```bash
# Instead of .env file, set environment variables
export SISTER_URL=https://sister.umko.ac.id
export SISTER_USERNAME=prod_user
export SISTER_PASSWORD=prod_password
export SISTER_ID_PENGGUNA=prod_123
```

## 🚀 Deployment

### Docker Deployment
```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Use environment variables
CMD ["python", "sister.py"]
```

```bash
# docker-compose.yml
version: '3.8'
services:
  sister-api:
    build: .
    environment:
      - SISTER_URL=${SISTER_URL}
      - SISTER_USERNAME=${SISTER_USERNAME}
      - SISTER_PASSWORD=${SISTER_PASSWORD}
      - SISTER_ID_PENGGUNA=${SISTER_ID_PENGGUNA}
      - USE_SANDBOX=${USE_SANDBOX}
      - CACHE_EXPIRATION_DAYS=${CACHE_EXPIRATION_DAYS}
      - AUTO_CLEANUP_CACHE=${AUTO_CLEANUP_CACHE}
```

### Kubernetes Deployment
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sister-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: sister-api
  template:
    metadata:
      labels:
        app: sister-api
    spec:
      containers:
      - name: sister-api
        image: sister-api:latest
        env:
        - name: SISTER_URL
          valueFrom:
            secretKeyRef:
              name: sister-secrets
              key: sister-url
        - name: SISTER_USERNAME
          valueFrom:
            secretKeyRef:
              name: sister-secrets
              key: sister-username
        - name: SISTER_PASSWORD
          valueFrom:
            secretKeyRef:
              name: sister-secrets
              key: sister-password
        - name: SISTER_ID_PENGGUNA
          valueFrom:
            secretKeyRef:
              name: sister-secrets
              key: sister-id-pengguna
```

### Heroku Deployment
```bash
# Set environment variables
heroku config:set SISTER_URL=https://sister.umko.ac.id
heroku config:set SISTER_USERNAME=your_username
heroku config:set SISTER_PASSWORD=your_password
heroku config:set SISTER_ID_PENGGUNA=your_id

# Deploy
git push heroku main
```

## 🔍 Validation

### Check Environment Variables
```python
from sister import SisterAPI

# This will validate all required environment variables
api = SisterAPI()
```

### Manual Validation
```bash
# Check if .env file exists
ls -la .env

# Validate environment variables
python -c "
import os
from dotenv import load_dotenv
load_dotenv()

required = ['SISTER_URL', 'SISTER_USERNAME', 'SISTER_PASSWORD', 'SISTER_ID_PENGGUNA']
missing = [var for var in required if not os.getenv(var)]

if missing:
    print(f'Missing: {missing}')
else:
    print('All required variables are set!')
"
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Missing .env File
```bash
# Error: Missing required environment variables
# Solution: Create .env file
cp env.example .env
# Edit .env with your credentials
```

#### 2. Invalid URL
```bash
# Error: URL is not valid
# Solution: Check SISTER_URL format
SISTER_URL=https://sister.umko.ac.id  # ✅ Correct
SISTER_URL=sister.umko.ac.id          # ❌ Missing protocol
```

#### 3. Authentication Failed
```bash
# Error: API key invalid
# Solution: Check credentials
SISTER_USERNAME=your_actual_username
SISTER_PASSWORD=your_actual_password
SISTER_ID_PENGGUNA=your_actual_id
```

#### 4. Cache Issues
```bash
# Error: Cache not working
# Solution: Check cache configuration
CACHE_EXPIRATION_DAYS=1
AUTO_CLEANUP_CACHE=false
```

## 📊 Environment Variable Reference

### Full .env Template
```bash
# Sister API Configuration
SISTER_URL=https://sister.example.com
USE_SANDBOX=true

# Sister Developer Credentials
SISTER_USERNAME=your_developer_username
SISTER_PASSWORD=your_developer_password
SISTER_ID_PENGGUNA=your_developer_id_pengguna

# Cache Configuration
CACHE_EXPIRATION_DAYS=1
AUTO_CLEANUP_CACHE=false

# API Configuration
API_TIMEOUT_SECONDS=30
MAX_RETRIES=3
```

### Type Reference
| Variable | Type | Required | Default |
|----------|------|----------|---------|
| `SISTER_URL` | string | ✅ | - |
| `SISTER_USERNAME` | string | ✅ | - |
| `SISTER_PASSWORD` | string | ✅ | - |
| `SISTER_ID_PENGGUNA` | string | ✅ | - |
| `USE_SANDBOX` | boolean | ❌ | `true` |
| `CACHE_EXPIRATION_DAYS` | integer | ❌ | `1` |
| `AUTO_CLEANUP_CACHE` | boolean | ❌ | `false` |
| `API_TIMEOUT_SECONDS` | integer | ❌ | `30` |
| `MAX_RETRIES` | integer | ❌ | `3` |

## 🎯 Migration from config.json

### Old config.json Format
```json
{
    "sister_url": "https://sister.umko.ac.id",
    "use_sandbox": true,
    "username": "developer_user",
    "password": "password123",
    "id_pengguna": "12345"
}
```

### New .env Format
```bash
SISTER_URL=https://sister.umko.ac.id
USE_SANDBOX=true
SISTER_USERNAME=developer_user
SISTER_PASSWORD=password123
SISTER_ID_PENGGUNA=12345
```

### Migration Steps
1. **Backup old config**
   ```bash
   cp config/config.json config/config.json.backup
   ```

2. **Create .env file**
   ```bash
   cp env.example .env
   ```

3. **Copy values**
   ```bash
   # Convert config.json values to .env format
   SISTER_URL=$(jq -r '.sister_url' config/config.json)
   SISTER_USERNAME=$(jq -r '.username' config/config.json)
   SISTER_PASSWORD=$(jq -r '.password' config/config.json)
   SISTER_ID_PENGGUNA=$(jq -r '.id_pengguna' config/config.json)
   ```

4. **Test new configuration**
   ```bash
   python test_fixes.py
   ```

5. **Remove old config (optional)**
   ```bash
   rm config/config.json
   ```

## 📝 Summary

Environment variable configuration provides:

- ✅ **Better Security**: No credentials in code
- ✅ **Easier Deployment**: Environment-specific configs
- ✅ **Modern Practices**: Follows 12-factor app principles
- ✅ **Flexibility**: Easy to change without code changes
- ✅ **Scalability**: Works with container orchestration
- ✅ **Version Control Safe**: .env files can be gitignored

The Sister API client now follows modern development practices while maintaining backward compatibility.
