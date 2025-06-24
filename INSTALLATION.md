# Installation Guide - UMKM Marketplace

## 🚀 Quick Installation

### Prerequisites
- Docker & Docker Compose installed
- 4GB+ RAM available
- 20GB+ disk space

### One-Line Installation
```bash
git clone https://github.com/YOUR_USERNAME/odoo-ecommerce-umkm.git && cd odoo-ecommerce-umkm && docker-compose up -d && python3 install_umkm.py
```

## 📋 Detailed Installation Steps

### Step 1: System Preparation

#### Ubuntu/Debian
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y git curl python3 python3-pip

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Logout and login again for Docker group changes
```

#### CentOS/RHEL
```bash
# Update system
sudo yum update -y

# Install required packages
sudo yum install -y git curl python3 python3-pip

# Install Docker
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install -y docker-ce docker-ce-cli containerd.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### Step 2: Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/odoo-ecommerce-umkm.git
cd odoo-ecommerce-umkm
```

### Step 3: Environment Configuration

#### Create Environment File
```bash
cp .env.example .env
```

#### Edit Environment Variables
```bash
nano .env
```

**Minimal Configuration:**
```env
# Database Configuration
POSTGRES_DB=umkm_db
POSTGRES_USER=odoo
POSTGRES_PASSWORD=SecurePassword123!

# Odoo Configuration
ODOO_ADMIN_PASSWORD=AdminPassword123!

# External Services (Optional)
PAYMENT_API_KEY=your_payment_gateway_key
SHIPPING_API_KEY=your_shipping_api_key
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your_email@domain.com
EMAIL_PASSWORD=your_email_password
```

### Step 4: Start Services

#### Basic Startup
```bash
# Start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f odoo
```

#### Production Startup
```bash
# Use production configuration
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Step 5: Install UMKM Module

#### Automated Installation (Recommended)
```bash
# Wait for services to be ready (2-3 minutes)
sleep 180

# Run installation script
python3 install_umkm.py
```

#### Manual Installation
1. Open browser: `http://localhost:8069`
2. Create database:
   - Database Name: `umkm_db`
   - Email: `admin@example.com`
   - Password: `admin`
   - Phone: `+62812345678`
   - Language: `Indonesian / English`
   - Country: `Indonesia`
3. Install UMKM Marketplace module:
   - Go to Apps
   - Update Apps List
   - Search "UMKM Marketplace"
   - Click Install

### Step 6: Post-Installation Setup

#### Assign User Groups
```bash
python3 assign_admin_groups.py
```

#### Verify Installation
```bash
python3 install_umkm.py
```

#### Initial Configuration
1. **Access System**: `http://localhost:8069`
2. **Login**: admin / admin
3. **Go to UMKM Marketplace menu**
4. **Configure**:
   - Payment methods
   - Delivery methods
   - Commission rules
   - Vendor categories

## 🐳 Docker Configuration

### Service Overview
- **odoo**: Main Odoo application
- **db**: PostgreSQL database
- **redis**: Cache and session storage
- **nginx**: Reverse proxy and load balancer
- **api**: Mobile API service
- **elasticsearch**: Search engine
- **kibana**: Log analytics
- **grafana**: Monitoring dashboard
- **prometheus**: Metrics collection

### Resource Allocation

#### Minimum Resources
```yaml
version: '3.8'
services:
  odoo:
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
  db:
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '0.5'
```

#### Production Resources
```yaml
version: '3.8'
services:
  odoo:
    deploy:
      replicas: 2
      resources:
        limits:
          memory: 4G
          cpus: '2.0'
  db:
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
```

### Custom Docker Configurations

#### Development Mode
```bash
# Start with development settings
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

#### Production Mode
```bash
# Start with production optimizations
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## 🔧 Advanced Configuration

### SSL/HTTPS Setup

#### Using Let's Encrypt
```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com

# Update nginx configuration
sudo nano /etc/nginx/sites-available/umkm-marketplace
```

#### SSL Configuration
```nginx
server {
    listen 443 ssl;
    server_name yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    location / {
        proxy_pass http://localhost:8069;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Database Optimization

#### PostgreSQL Configuration
```bash
# Edit PostgreSQL config
docker-compose exec db nano /var/lib/postgresql/data/postgresql.conf
```

**Recommended Settings:**
```conf
# Memory settings
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 4MB

# Performance settings
max_connections = 100
checkpoint_completion_target = 0.9
wal_buffers = 16MB

# Logging
log_statement = 'all'
log_duration = on
```

### Email Configuration

#### Gmail SMTP
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
EMAIL_USE_TLS=True
```

#### Local SMTP Server
```bash
# Install Postfix
sudo apt install postfix

# Configure in .env
EMAIL_HOST=localhost
EMAIL_PORT=25
EMAIL_USE_TLS=False
```

## 🔍 Troubleshooting Installation

### Common Issues

#### Port Already in Use
```bash
# Check what's using port 8069
sudo netstat -tulpn | grep 8069

# Kill the process or change port in docker-compose.yml
```

#### Docker Permission Denied
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Logout and login again
```

#### Database Connection Failed
```bash
# Check database logs
docker-compose logs db

# Restart database
docker-compose restart db

# Reset database
docker-compose down -v
docker-compose up -d
```

#### Module Installation Failed
```bash
# Check Odoo logs
docker-compose logs odoo

# Update apps list manually
docker-compose exec odoo odoo -u all -d umkm_db --stop-after-init

# Restart Odoo
docker-compose restart odoo
```

#### Out of Memory
```bash
# Check memory usage
free -h

# Increase swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### Performance Issues

#### Slow Startup
```bash
# Increase memory allocation
# Edit docker-compose.yml:
services:
  odoo:
    mem_limit: 4g
```

#### Database Performance
```bash
# Analyze database
docker-compose exec db psql -U odoo -d umkm_db -c "VACUUM ANALYZE;"

# Rebuild indexes
docker-compose exec db psql -U odoo -d umkm_db -c "REINDEX DATABASE umkm_db;"
```

## 📊 Monitoring Setup

### Health Checks
```bash
# Check service health
docker-compose ps

# Check individual service logs
docker-compose logs -f odoo
docker-compose logs -f db
docker-compose logs -f redis
```

### Automated Monitoring
```bash
# Install monitoring tools
docker-compose -f docker-compose.yml -f docker-compose.monitoring.yml up -d

# Access monitoring dashboards
# Grafana: http://localhost:3000 (admin/admin)
# Prometheus: http://localhost:9090
# Kibana: http://localhost:5601
```

## 🔄 Maintenance

### Regular Backups
```bash
# Create backup script
cat > backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose exec db pg_dump -U odoo umkm_db > backup_${DATE}.sql
tar -czf backup_${DATE}.tar.gz backup_${DATE}.sql custom_modules/
rm backup_${DATE}.sql
EOF

chmod +x backup.sh

# Run daily backup (add to crontab)
0 2 * * * /path/to/backup.sh
```

### Updates
```bash
# Update system
git pull origin main

# Update Docker images
docker-compose pull

# Restart services
docker-compose up -d

# Update modules
python3 install_umkm.py
```

## 🚀 Production Deployment

### Scaling Configuration
```yaml
version: '3.8'
services:
  odoo:
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
        max_attempts: 3
  
  nginx:
    deploy:
      replicas: 2
      placement:
        constraints:
          - node.role == manager
```

### Load Balancer Setup
```nginx
upstream odoo_servers {
    server odoo_1:8069;
    server odoo_2:8069;
    server odoo_3:8069;
}

server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://odoo_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

*For more detailed information, please refer to the main [User Guide](USER_GUIDE.md).*
