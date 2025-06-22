# UMKM Digital Marketplace - Development Setup Guide

## 🚀 QUICK START GUIDE

### Prerequisites
- **Python 3.9+**
- **PostgreSQL 12+**
- **Node.js 16+** (untuk frontend development)
- **Docker & Docker Compose** (recommended)
- **Git**

### 1. Environment Setup

#### Clone Repository
```bash
git clone https://github.com/umkm-digital/odoo-ecommerce-umkm.git
cd odoo-ecommerce-umkm
```

#### Create Environment File
```bash
cp .env.example .env
```

Edit `.env` file:
```env
# Odoo Configuration
ODOO_VERSION=17.0
ODOO_DB_HOST=db
ODOO_DB_PORT=5432
ODOO_DB_USER=odoo
ODOO_DB_PASSWORD=odoo_password
ODOO_ADMIN_PASSWORD=admin123

# Database Configuration
POSTGRES_DB=postgres
POSTGRES_USER=odoo
POSTGRES_PASSWORD=odoo_password

# API Configuration
API_SECRET_KEY=your-secret-key-here
API_HOST=localhost
API_PORT=8000

# External Services
MIDTRANS_SERVER_KEY=your-midtrans-key
MIDTRANS_CLIENT_KEY=your-midtrans-client-key
MIDTRANS_IS_PRODUCTION=false

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### 2. Docker Development Setup (Recommended)

#### Start Services
```bash
docker-compose up -d
```

#### Check Services Status
```bash
docker-compose ps
```

#### Access Applications
- **Odoo**: http://localhost:8069
- **API Documentation**: http://localhost:8000/api/docs
- **Database**: localhost:5432

#### Initial Setup
1. Access Odoo at http://localhost:8069
2. Create database: `umkm_marketplace`
3. Install custom modules from `/custom_modules`

### 3. Manual Development Setup

#### Install Python Dependencies
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install Odoo
pip install -r requirements.txt

# Install API dependencies
cd mobile_api
pip install -r requirements.txt
cd ..
```

#### Setup PostgreSQL
```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE USER odoo WITH PASSWORD 'odoo_password';
CREATE DATABASE umkm_marketplace OWNER odoo;
GRANT ALL PRIVILEGES ON DATABASE umkm_marketplace TO odoo;
\q
```

#### Start Odoo
```bash
python odoo/odoo-bin \
  --addons-path=odoo/addons,custom_modules \
  --database=umkm_marketplace \
  --db_host=localhost \
  --db_port=5432 \
  --db_user=odoo \
  --db_password=odoo_password \
  --xmlrpc-port=8069 \
  --logfile=odoo.log
```

#### Start API Server
```bash
cd mobile_api
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 📁 PROJECT STRUCTURE

```
odoo-ecommerce-umkm/
├── custom_modules/              # Custom Odoo modules
│   ├── umkm_marketplace/        # Main marketplace module
│   ├── umkm_payment/           # Payment integration
│   ├── umkm_shipping/          # Shipping integration
│   └── umkm_mobile/            # Mobile app connector
├── mobile_api/                 # FastAPI mobile backend
│   ├── main.py                 # Main API file
│   ├── models/                 # Pydantic models
│   ├── routers/                # API routers
│   └── utils/                  # Utility functions
├── mobile_app/                 # Flutter mobile app
│   ├── android/                # Android specific
│   ├── ios/                    # iOS specific
│   ├── lib/                    # Dart source code
│   └── pubspec.yaml            # Dependencies
├── web_frontend/               # Custom web frontend
│   ├── src/                    # Source code
│   ├── public/                 # Static assets
│   └── package.json            # Dependencies
├── docker-compose.yml          # Docker services
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
└── README.md                  # This file
```

---

## 🔧 DEVELOPMENT WORKFLOW

### 1. Custom Module Development

#### Create New Module
```bash
cd custom_modules
mkdir new_module_name
cd new_module_name
```

#### Module Structure
```
new_module_name/
├── __manifest__.py           # Module manifest
├── __init__.py              # Module initialization
├── models/                  # Data models
│   ├── __init__.py
│   └── model_name.py
├── views/                   # XML views
│   ├── model_views.xml
│   └── menu.xml
├── data/                    # Default data
├── demo/                    # Demo data
├── static/                  # Static assets
│   ├── src/
│   │   ├── css/
│   │   ├── js/
│   │   └── xml/
│   └── description/
├── security/                # Security rules
│   ├── ir.model.access.csv
│   └── security.xml
└── tests/                   # Unit tests
```

#### Install Module
```bash
# Through Odoo interface
1. Go to Apps menu
2. Update Apps List
3. Search for your module
4. Install

# Or via command line
python odoo-bin -u new_module_name -d umkm_marketplace
```

### 2. API Development

#### Add New Endpoint
```python
# mobile_api/routers/new_router.py
from fastapi import APIRouter, Depends
from typing import List

router = APIRouter(prefix="/api/new", tags=["new"])

@router.get("/items")
async def get_items():
    return {"items": []}

# mobile_api/main.py
from routers import new_router
app.include_router(new_router.router)
```

#### Test API
```bash
# Run tests
pytest mobile_api/tests/

# Manual testing
curl -X GET "http://localhost:8000/api/new/items"
```

### 3. Database Management

#### Backup Database
```bash
pg_dump -h localhost -U odoo umkm_marketplace > backup.sql
```

#### Restore Database
```bash
psql -h localhost -U odoo umkm_marketplace < backup.sql
```

#### Database Migration
```bash
# Odoo automatic migration
python odoo-bin -u all -d umkm_marketplace

# Manual SQL scripts
psql -h localhost -U odoo umkm_marketplace -f migration.sql
```

### 4. Testing

#### Run Odoo Tests
```bash
python odoo-bin --test-enable --stop-after-init -d umkm_marketplace
```

#### Run API Tests
```bash
cd mobile_api
pytest tests/ -v
```

#### Run Integration Tests
```bash
# Full system test
python tests/integration_test.py
```

---

## 🐛 DEBUGGING

### 1. Odoo Debugging

#### Enable Debug Mode
Add `?debug=1` to URL or:
```bash
# Start with debug
python odoo-bin --dev=all -d umkm_marketplace
```

#### Log Configuration
```python
# In odoo.conf
[options]
log_level = debug
log_handler = :DEBUG,werkzeug:CRITICAL,odoo.service.server:INFO
```

#### Python Debugger
```python
# In Python code
import pdb; pdb.set_trace()

# Or use Odoo debugger
from odoo.tools import debug; debug()
```

### 2. API Debugging

#### FastAPI Debug Mode
```bash
uvicorn main:app --reload --log-level debug
```

#### API Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.get("/debug")
async def debug_endpoint():
    logger.debug("Debug message")
    return {"debug": True}
```

### 3. Database Debugging

#### Query Logging
```sql
-- Enable query logging
ALTER SYSTEM SET log_statement = 'all';
SELECT pg_reload_conf();

-- View logs
tail -f /var/log/postgresql/postgresql-12-main.log
```

#### Performance Analysis
```sql
-- Explain query
EXPLAIN ANALYZE SELECT * FROM umkm_vendor WHERE state = 'active';

-- Index usage
SELECT schemaname, tablename, indexname, idx_scan 
FROM pg_stat_user_indexes 
ORDER BY idx_scan DESC;
```

---

## 🚀 DEPLOYMENT

### 1. Production Environment

#### Docker Production
```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy
docker-compose -f docker-compose.prod.yml up -d
```

#### Environment Variables
```env
# Production settings
ODOO_ADMIN_PASSWORD=strong-password
API_SECRET_KEY=strong-secret-key
POSTGRES_PASSWORD=strong-db-password

# External services
MIDTRANS_IS_PRODUCTION=true
SMTP_SERVER=production-smtp.com
```

#### SSL/HTTPS Setup
```nginx
# nginx.conf
server {
    listen 443 ssl;
    server_name umkmdigital.id;
    
    ssl_certificate /etc/ssl/certs/cert.pem;
    ssl_certificate_key /etc/ssl/private/key.pem;
    
    location / {
        proxy_pass http://localhost:8069;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 2. CI/CD Pipeline

#### GitHub Actions
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Run tests
      run: |
        docker-compose -f docker-compose.test.yml up --abort-on-container-exit
  
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - name: Deploy to server
      run: |
        ssh user@server 'cd /app && git pull && docker-compose up -d'
```

### 3. Monitoring & Logging

#### Application Monitoring
```python
# Add to main.py
from prometheus_fastapi_instrumentator import Instrumentator

instrumentator = Instrumentator()
instrumentator.instrument(app)
instrumentator.expose(app)
```

#### Log Aggregation
```yaml
# docker-compose.yml
services:
  app:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

---

## 📚 USEFUL COMMANDS

### Odoo Commands
```bash
# Start Odoo in development mode
python odoo-bin --dev=all

# Update specific module
python odoo-bin -u module_name -d database_name

# Install module
python odoo-bin -i module_name -d database_name

# Shell access
python odoo-bin shell -d database_name

# Create new database
python odoo-bin -d new_database --stop-after-init
```

### API Commands
```bash
# Start API with auto-reload
uvicorn main:app --reload

# Run with specific configuration
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# Generate OpenAPI spec
curl http://localhost:8000/openapi.json > api_spec.json
```

### Database Commands
```bash
# Backup
pg_dump -h localhost -U odoo database_name > backup.sql

# Restore
createdb -h localhost -U odoo new_database
psql -h localhost -U odoo new_database < backup.sql

# Connect to database
psql -h localhost -U odoo database_name
```

### Docker Commands
```bash
# View logs
docker-compose logs -f service_name

# Execute command in container
docker-compose exec service_name bash

# Rebuild specific service
docker-compose build service_name

# Scale service
docker-compose up -d --scale api=3
```

---

## 🆘 TROUBLESHOOTING

### Common Issues

#### 1. Odoo Module Not Found
```bash
# Check addons path
python odoo-bin --addons-path=custom_modules,odoo/addons

# Update apps list
# Apps > Update Apps List
```

#### 2. Database Connection Error
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check connection
psql -h localhost -U odoo -d postgres

# Reset password
sudo -u postgres psql
ALTER USER odoo PASSWORD 'new_password';
```

#### 3. API CORS Issues
```python
# Add CORS middleware
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 4. Module Dependency Issues
```python
# Check __manifest__.py
'depends': ['base', 'web', 'website', 'sale']

# Install dependencies first
python odoo-bin -i base,web,website,sale -d database_name
```

### Getting Help

- **Odoo Documentation**: https://www.odoo.com/documentation/17.0/
- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Community Forum**: https://github.com/umkm-digital/discussions
- **Email Support**: tech-support@umkmdigital.id

---

*Happy coding! 🚀*
