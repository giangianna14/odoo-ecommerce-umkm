# 🏪 UMKM Marketplace - E-commerce Platform for Indonesian MSMEs

[![License](https://img.shields.io/badge/license-LGPL--3-blue.svg)](LICENSE)
[![Odoo Version](https://img.shields.io/badge/Odoo-17.0-purple.svg)](https://www.odoo.com/)
[![Python Version](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

**UMKM Marketplace** is a comprehensive e-commerce platform specifically designed for Indonesian Micro, Small, and Medium Enterprises (UMKM). Built on Odoo 17, it provides a complete marketplace solution with multi-vendor support, Indonesian payment methods, and local business compliance features.

## 🎯 Features

### 🏪 Multi-Vendor Marketplace
- **Vendor Management**: Complete vendor onboarding and management system
- **Product Catalog**: Rich product catalog with categories and certifications
- **Order Processing**: Automated order processing with vendor notifications
- **Commission System**: Flexible commission calculation and payment tracking

### 💰 Indonesian Payment Integration
- **Local Payment Methods**: Dana, OVO, GoPay, Bank Transfer, and more
- **Midtrans Integration**: Secure payment processing
- **Multiple Currencies**: IDR primary with multi-currency support
- **Payment Tracking**: Real-time payment status monitoring

### 📋 Business Compliance
- **Halal Certification**: MUI Halal certification management
- **SNI Standards**: Indonesian National Standard compliance
- **Business Licenses**: Automated business verification
- **Tax Integration**: Indonesian tax calculation and reporting

### 📊 Analytics & Reporting
- **Vendor Dashboard**: Comprehensive vendor performance analytics
- **Admin Dashboard**: System-wide analytics and reporting
- **Sales Reports**: Detailed sales and commission reports
- **Performance Metrics**: Real-time business intelligence

### 📱 Mobile & API
- **RESTful API**: Complete API for mobile apps and integrations
- **Mobile Responsive**: Mobile-optimized web interface
- **Real-time Updates**: WebSocket support for live updates
- **Offline Capability**: Progressive Web App features

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/odoo-ecommerce-umkm.git
cd odoo-ecommerce-umkm
```

2. **Setup environment**
```bash
cp .env.example .env
# Edit .env file with your configuration
```

3. **Start services**
```bash
docker-compose up -d
```

4. **Install UMKM module**
```bash
python3 install_umkm.py
```

5. **Access the system**
- **Web Interface**: http://localhost:8069
- **Admin Login**: admin / admin
- **API Documentation**: http://localhost:8069/api/docs

### Manual Installation

See [INSTALLATION.md](INSTALLATION.md) for detailed manual installation instructions.

## 📋 System Requirements

### Minimum Requirements
- **RAM**: 4GB
- **Storage**: 20GB free space
- **CPU**: 2 cores
- **OS**: Ubuntu 18.04+, CentOS 7+, or similar Linux distribution

### Recommended for Production
- **RAM**: 8GB or more
- **Storage**: 50GB+ SSD
- **CPU**: 4+ cores
- **OS**: Ubuntu 20.04+ LTS

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Odoo Core     │    │   Database      │
│   (Web/Mobile)  │◄──►│   Application   │◄──►│   PostgreSQL    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Mobile API    │    │   UMKM Module   │    │   Redis Cache   │
│   (FastAPI)     │    │   (Custom)      │    │   & Sessions    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Payment       │    │   Monitoring    │    │   File Storage  │
│   Gateways      │    │   & Analytics   │    │   & CDN         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
odoo-ecommerce-umkm/
├── custom_modules/              # Custom Odoo modules
│   └── umkm_marketplace/        # Main UMKM module
│       ├── models/              # Data models
│       ├── views/               # UI views and templates
│       ├── static/              # CSS, JS, images
│       ├── data/                # Initial data and configs
│       ├── security/            # Access rights and rules
│       └── wizard/              # Wizard forms
├── mobile_api/                  # FastAPI mobile backend
├── config/                      # Configuration files
├── nginx/                       # Nginx configuration
├── monitoring/                  # Monitoring setup
├── docs/                        # Documentation
├── tests/                       # Test files
├── scripts/                     # Utility scripts
├── docker-compose.yml           # Docker orchestration
├── .env.example                 # Environment template
└── requirements.txt             # Python dependencies
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
# Database Configuration
POSTGRES_DB=umkm_db
POSTGRES_USER=odoo
POSTGRES_PASSWORD=your_secure_password

# Odoo Configuration
ODOO_ADMIN_PASSWORD=your_admin_password
ODOO_DB_FILTER=umkm_db

# API Configuration
API_SECRET_KEY=your_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_here

# Payment Gateway Configuration
MIDTRANS_SERVER_KEY=your_midtrans_server_key
MIDTRANS_CLIENT_KEY=your_midtrans_client_key
MIDTRANS_IS_PRODUCTION=false

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@domain.com
EMAIL_HOST_PASSWORD=your_email_password

# External Services
WHATSAPP_API_KEY=your_whatsapp_api_key
SMS_API_KEY=your_sms_api_key
```

### Payment Gateway Setup

#### Midtrans Configuration
1. Register at [Midtrans](https://midtrans.com/)
2. Get your Server Key and Client Key
3. Configure in environment variables
4. Set webhook URL: `https://yourdomain.com/payment/midtrans/webhook`

#### Other Payment Methods
- **Bank Transfer**: Configure bank accounts in Payment Methods
- **E-wallet**: Setup OVO, Dana, GoPay integration
- **Credit Card**: Enable through Midtrans

## 🔌 API Documentation

The UMKM Marketplace provides a comprehensive RESTful API for mobile applications and third-party integrations.

### Authentication
```bash
POST /api/auth/login
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

### Key Endpoints
- **Products**: `/api/products` - Product management
- **Orders**: `/api/orders` - Order processing
- **Vendors**: `/api/vendors` - Vendor management
- **Customers**: `/api/customers` - Customer data
- **Analytics**: `/api/analytics` - Business intelligence

For complete API documentation, see [API_DOCUMENTATION.md](API_DOCUMENTATION.md).

## 🧪 Testing

### Running Tests
```bash
# Run all tests
docker-compose exec odoo python -m pytest tests/

# Run specific test categories
docker-compose exec odoo python -m pytest tests/unit/
docker-compose exec odoo python -m pytest tests/integration/

# Run with coverage
docker-compose exec odoo python -m pytest --cov=custom_modules tests/
```

### Test Data
```bash
# Load test data
python3 scripts/load_test_data.py

# Create demo vendors and products
python3 scripts/create_demo_data.py
```

## 📊 Monitoring & Analytics

### Built-in Monitoring
- **Grafana Dashboard**: http://localhost:3000 (admin/admin)
- **Prometheus Metrics**: http://localhost:9090
- **Elasticsearch Logs**: http://localhost:9200
- **Kibana Analytics**: http://localhost:5601

### Performance Monitoring
- Real-time system metrics
- Application performance monitoring
- Database query optimization
- User behavior analytics

## 🚀 Deployment

### Development
```bash
# Start development environment
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

### Production
```bash
# Start production environment
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Scaling
```bash
# Scale Odoo instances
docker-compose up -d --scale odoo=3

# Scale API instances
docker-compose up -d --scale api=2
```

## 🔒 Security

### Security Features
- **Input Validation**: All inputs are validated and sanitized
- **Access Control**: Role-based access control (RBAC)
- **Data Encryption**: Sensitive data encryption at rest
- **Secure Communication**: HTTPS/TLS encryption
- **Audit Logs**: Comprehensive audit trail

### Security Best Practices
- Regular security updates
- Strong password policies
- Multi-factor authentication (MFA)
- Regular backups and disaster recovery
- Penetration testing

## 🌐 Internationalization

### Supported Languages
- **Indonesian** (Bahasa Indonesia) - Primary
- **English** - Secondary
- **Extensible**: Easy to add more languages

### Adding Translations
1. Extract translatable strings
2. Create language-specific PO files
3. Translate strings
4. Compile translations

## 📚 Documentation

- **[User Guide](USER_GUIDE.md)** - Complete user documentation
- **[Installation Guide](INSTALLATION.md)** - Detailed installation instructions
- **[API Documentation](API_DOCUMENTATION.md)** - Complete API reference
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute to the project
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:

- Code of conduct
- Development setup
- Submission process
- Coding standards
- Testing requirements

### Quick Contribution Steps
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the **LGPL-3 License** - see the [LICENSE](LICENSE) file for details.

## 🏆 Acknowledgments

- **Odoo Community**: For the amazing framework
- **Indonesian UMKM Community**: For inspiration and feedback
- **Contributors**: All our amazing contributors
- **Open Source Libraries**: Various open source projects that make this possible

## 📞 Support & Contact

### Community Support
- **GitHub Issues**: [Report bugs and request features](https://github.com/YOUR_USERNAME/odoo-ecommerce-umkm/issues)
- **Discussions**: [Join community discussions](https://github.com/YOUR_USERNAME/odoo-ecommerce-umkm/discussions)
- **Documentation**: [Browse our docs](https://umkm-marketplace.readthedocs.io)

### Professional Support
- **Email**: support@umkmdigital.id
- **Website**: https://umkmdigital.id
- **LinkedIn**: [UMKM Digital Solutions](https://linkedin.com/company/umkm-digital)

### Enterprise Services
We offer enterprise services including:
- Custom development and integration
- Deployment and hosting
- Training and consulting
- 24/7 technical support
- SLA guarantees

## 🗺️ Roadmap

### Version 1.1.0 (Q2 2024)
- [ ] Advanced analytics and reporting
- [ ] Enhanced mobile app integration
- [ ] Social media marketing tools
- [ ] Inventory management improvements

### Version 1.2.0 (Q3 2024)
- [ ] AI-powered product recommendations
- [ ] Advanced shipping integrations
- [ ] Multi-currency support
- [ ] Enhanced SEO tools

### Version 2.0.0 (Q4 2024)
- [ ] Marketplace federation
- [ ] Blockchain integration for supply chain
- [ ] Advanced AI features
- [ ] Enhanced mobile apps

## 📈 Statistics

- **⭐ Stars**: Help us reach 1000 stars!
- **🍴 Forks**: Join our growing community
- **📊 Used by**: Growing number of Indonesian MSMEs
- **🌍 Countries**: Expanding beyond Indonesia

---

<div align="center">

**Made with ❤️ for Indonesian MSMEs**

[⭐ Star this project](https://github.com/YOUR_USERNAME/odoo-ecommerce-umkm) | 
[🐛 Report Bug](https://github.com/YOUR_USERNAME/odoo-ecommerce-umkm/issues) | 
[✨ Request Feature](https://github.com/YOUR_USERNAME/odoo-ecommerce-umkm/issues) | 
[📖 Documentation](USER_GUIDE.md)

</div>
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
