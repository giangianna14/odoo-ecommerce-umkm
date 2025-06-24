# UMKM Marketplace - User Guide

## 📋 Table of Contents

1. [Overview](#overview)
2. [System Requirements](#system-requirements)
3. [Installation Guide](#installation-guide)
4. [Quick Start](#quick-start)
5. [User Roles & Permissions](#user-roles--permissions)
6. [Feature Guide](#feature-guide)
7. [API Documentation](#api-documentation)
8. [Troubleshooting](#troubleshooting)
9. [FAQ](#faq)
10. [Support](#support)

---

## 🎯 Overview

UMKM Marketplace is a comprehensive e-commerce platform specifically designed for Indonesian Micro, Small, and Medium Enterprises (UMKM). Built on Odoo 17, it provides a complete marketplace solution with multi-vendor support, Indonesian payment methods, and local business compliance features.

### Key Features

- **Multi-Vendor Marketplace**: Support for multiple vendors with individual vendor management
- **Product Certification**: Halal, SNI, ISO, and other Indonesian certifications
- **Commission Management**: Automated commission calculation and payment tracking
- **Indonesian Payment Methods**: Dana, OVO, GoPay, Bank Transfer, and more
- **Real-time Dashboard**: Comprehensive analytics for vendors and administrators
- **Mobile API**: RESTful API for mobile app integration
- **Shipping Integration**: JNE, POS Indonesia, and other local couriers
- **Multi-language Support**: Indonesian and English

---

## 💻 System Requirements

### Minimum Requirements
- **RAM**: 4GB
- **Storage**: 20GB free space
- **CPU**: 2 cores
- **OS**: Ubuntu 18.04+, CentOS 7+, or similar Linux distribution

### Recommended Requirements
- **RAM**: 8GB or more
- **Storage**: 50GB+ SSD
- **CPU**: 4+ cores
- **OS**: Ubuntu 20.04+ LTS

### Software Dependencies
- Docker 20.10+
- Docker Compose 1.29+
- Python 3.8+ (for setup scripts)
- Git

---

## 🚀 Installation Guide

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/odoo-ecommerce-umkm.git
cd odoo-ecommerce-umkm
```

### Step 2: Environment Setup

1. **Copy environment file:**
```bash
cp .env.example .env
```

2. **Edit environment variables:**
```bash
nano .env
```

Configure the following variables:
```env
# Database
POSTGRES_DB=umkm_db
POSTGRES_USER=odoo
POSTGRES_PASSWORD=your_secure_password

# Odoo
ODOO_ADMIN_PASSWORD=your_admin_password

# External APIs
PAYMENT_API_KEY=your_payment_api_key
SHIPPING_API_KEY=your_shipping_api_key
```

### Step 3: Start Services

```bash
# Start all services
docker-compose up -d

# Check service status
docker-compose ps
```

### Step 4: Install UMKM Module

**Option A: Using Setup Script (Recommended)**
```bash
python3 install_umkm.py
```

**Option B: Manual Installation**
1. Access Odoo at `http://localhost:8069`
2. Login with admin credentials
3. Go to Apps → Update Apps List
4. Search for "UMKM Marketplace"
5. Click Install

### Step 5: Initial Configuration

```bash
# Run group assignment
python3 assign_admin_groups.py

# Verify installation
python3 install_umkm.py
```

---

## ⚡ Quick Start

### 1. Access the System

1. Open your browser and navigate to `http://localhost:8069`
2. Login with admin credentials:
   - **Username**: admin
   - **Password**: admin (or your configured password)

### 2. First-Time Setup

1. **Navigate to UMKM Marketplace menu**
2. **Configure Payment Methods**:
   - Go to Configuration → Payment Methods
   - Enable required payment gateways
3. **Setup Delivery Methods**:
   - Go to Configuration → Delivery Methods
   - Configure shipping options
4. **Create Vendor Categories**:
   - Go to Vendors → Categories
   - Add vendor categories (e.g., Food & Beverage, Fashion, Electronics)

### 3. Create Your First Vendor

1. Go to **Vendors → All Vendors**
2. Click **Create**
3. Fill in vendor information:
   - Business name and description
   - Contact information
   - Business registration details
   - Commission rates
4. Save the vendor

### 4. Add Products

1. Go to **Products → All Products**
2. Click **Create**
3. Enter product details:
   - Name and description
   - Select vendor
   - Set pricing
   - Upload images
   - Add certifications if applicable
4. Submit for approval

### 5. Process Orders

1. **View Orders**: Go to Sales → Orders
2. **Confirm Orders**: Click on an order and use action buttons
3. **Track Vendor Orders**: Go to Sales → Vendor Orders
4. **Manage Commissions**: Go to Commission → All Commissions

---

## 👥 User Roles & Permissions

### 1. UMKM Administrator
**Full system access including:**
- User management
- System configuration
- All vendor and product management
- Financial reports and commission management
- System maintenance

### 2. UMKM Manager
**Business operations management:**
- Vendor onboarding and approval
- Product approval and management
- Order processing
- Commission calculation
- Business reports

### 3. UMKM Vendor
**Vendor-specific operations:**
- Own product management
- Order management for their products
- Commission tracking
- Performance dashboard

### 4. Customer (Portal User)
**Customer-facing features:**
- Browse and search products
- Place orders
- Track order status
- Manage account information

---

## 📖 Feature Guide

### 🏪 Vendor Management

#### Vendor Registration
1. **Manual Registration** (Admin/Manager):
   - Go to Vendors → All Vendors → Create
   - Fill in business information
   - Set commission rates
   - Assign vendor category

2. **Self Registration** (via Portal):
   - Vendors can register through customer portal
   - Requires admin approval
   - Automatic onboarding wizard

#### Vendor Approval Process
1. **Pending Vendors**: Check Documents → Verify Information
2. **Approve/Reject**: Use action buttons
3. **Commission Setup**: Configure commission rates
4. **Category Assignment**: Assign to vendor categories

#### Vendor Dashboard
- **Sales Performance**: Revenue, orders, top products
- **Commission Tracking**: Earned, pending, paid commissions
- **Product Management**: Quick product actions
- **Order Management**: Vendor-specific orders

### 📦 Product Management

#### Product Creation
1. **Basic Information**:
   - Name, description, category
   - Pricing and inventory
   - Images and specifications

2. **Certifications**:
   - Halal certification
   - SNI (Indonesian National Standard)
   - ISO certifications
   - Custom certifications

3. **SEO Optimization**:
   - Meta title and description
   - Keywords
   - URL slug

#### Product Approval Workflow
1. **Draft**: Vendor creates product
2. **Pending**: Submitted for approval
3. **Approved**: Ready for publishing
4. **Published**: Live on marketplace
5. **Rejected**: Needs revision

#### Bulk Product Upload
1. Go to Products → Import Products
2. Download template
3. Fill product data
4. Upload CSV file
5. Review and confirm

### 🛒 Order Management

#### Order Processing Flow
1. **Customer Places Order**
2. **Order Confirmation**: Admin/Manager confirms
3. **Vendor Notification**: Automatic notification to vendors
4. **Vendor Order Creation**: Individual orders per vendor
5. **Fulfillment**: Vendors process their orders
6. **Delivery Tracking**: Real-time tracking updates
7. **Completion**: Order marked as delivered

#### Multi-Vendor Orders
- **Single Checkout**: Customers buy from multiple vendors
- **Split Orders**: Automatic creation of vendor-specific orders
- **Independent Processing**: Each vendor manages their portion
- **Consolidated Tracking**: Unified tracking for customers

### 💰 Commission Management

#### Commission Calculation
- **Automatic Calculation**: Based on predefined rules
- **Multiple Commission Types**:
  - Sales commission (percentage)
  - Listing fees (fixed)
  - Transaction fees
  - Subscription fees

#### Commission Rules
1. **Create Rules**: Go to Commission → Commission Rules
2. **Set Conditions**:
   - Vendor categories
   - Product categories
   - Amount ranges
   - Date ranges
3. **Configure Rates**: Percentage or fixed amounts

#### Payment Processing
1. **Generate Invoices**: Automatic invoice creation
2. **Payment Tracking**: Monitor payment status
3. **Reports**: Commission reports and analytics

### 📊 Dashboard & Analytics

#### Admin Dashboard
- **Sales Overview**: Total sales, orders, revenue
- **Vendor Performance**: Top vendors, new registrations
- **Product Analytics**: Best sellers, category performance
- **Financial Summary**: Commissions, payments, profits

#### Vendor Dashboard
- **Sales Metrics**: Personal sales performance
- **Product Performance**: Top products, views, conversions
- **Commission Tracking**: Earnings and payments
- **Order Management**: Recent orders and status

#### Custom Reports
1. **Sales Reports**: Detailed sales analytics
2. **Commission Reports**: Commission breakdowns
3. **Vendor Reports**: Vendor performance metrics
4. **Financial Reports**: Revenue and profit analysis

---

## 🔌 API Documentation

### Authentication
All API endpoints require authentication using API keys or OAuth tokens.

```bash
# Get API token
curl -X POST http://localhost:8069/api/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin"}'
```

### Product API

#### Get Products
```bash
GET /api/products
```

Parameters:
- `limit`: Number of products (default: 20)
- `offset`: Pagination offset
- `vendor_id`: Filter by vendor
- `category_id`: Filter by category

#### Create Product
```bash
POST /api/products
Content-Type: application/json

{
  "name": "Product Name",
  "description": "Product Description",
  "price": 100000,
  "vendor_id": 1,
  "category_id": 2
}
```

### Order API

#### Get Orders
```bash
GET /api/orders
```

#### Create Order
```bash
POST /api/orders
Content-Type: application/json

{
  "customer_id": 1,
  "order_lines": [
    {
      "product_id": 1,
      "quantity": 2,
      "price_unit": 100000
    }
  ]
}
```

### Vendor API

#### Get Vendor Dashboard
```bash
GET /api/vendor/dashboard/{vendor_id}
```

#### Update Vendor Information
```bash
PUT /api/vendor/{vendor_id}
Content-Type: application/json

{
  "name": "Updated Vendor Name",
  "description": "Updated Description"
}
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Module Installation Failed
**Problem**: Module won't install or shows errors

**Solutions**:
```bash
# Check Odoo logs
docker-compose logs odoo

# Restart services
docker-compose restart

# Update module list
python3 install_umkm.py
```

#### 2. Permission Denied Errors
**Problem**: Users can't access certain features

**Solutions**:
```bash
# Assign admin groups
python3 assign_admin_groups.py

# Or manually in Odoo:
# Settings → Users → Select User → Groups Tab
```

#### 3. Database Connection Issues
**Problem**: Can't connect to database

**Solutions**:
```bash
# Check database status
docker-compose ps

# Restart database
docker-compose restart db

# Check database logs
docker-compose logs db
```

#### 4. Port Conflicts
**Problem**: Port 8069 already in use

**Solutions**:
```bash
# Check what's using the port
sudo netstat -tulpn | grep 8069

# Change port in docker-compose.yml
# Then restart services
docker-compose down
docker-compose up -d
```

### Performance Issues

#### Slow Loading
1. **Check System Resources**:
```bash
# Check memory usage
free -h

# Check disk space
df -h

# Check CPU usage
top
```

2. **Optimize Database**:
```bash
# Access database container
docker-compose exec db psql -U odoo -d umkm_db

# Run VACUUM
VACUUM ANALYZE;
```

3. **Clear Cache**:
```bash
# Restart Odoo to clear cache
docker-compose restart odoo
```

---

## ❓ FAQ

### General Questions

**Q: What is UMKM Marketplace?**
A: It's a comprehensive e-commerce platform designed specifically for Indonesian Micro, Small, and Medium Enterprises, built on Odoo 17.

**Q: Can I customize the platform?**
A: Yes, the platform is highly customizable. You can modify views, add fields, create custom modules, and integrate with external services.

**Q: Is it suitable for large enterprises?**
A: While designed for UMKM, the platform can scale to support larger enterprises with proper infrastructure.

### Technical Questions

**Q: How do I backup my data?**
A: Use the provided backup scripts or create database dumps:
```bash
# Create backup
docker-compose exec db pg_dump -U odoo umkm_db > backup.sql

# Restore backup
docker-compose exec -T db psql -U odoo umkm_db < backup.sql
```

**Q: Can I integrate with external payment gateways?**
A: Yes, the platform supports integration with various Indonesian payment gateways like Midtrans, Xendit, and others.

**Q: How do I add custom fields?**
A: Create custom modules or modify existing models through the Odoo interface or code.

### Business Questions

**Q: What commission models are supported?**
A: The platform supports percentage-based, fixed amount, tiered, and custom commission structures.

**Q: Can vendors manage their own products?**
A: Yes, vendors have access to their own portal where they can manage products, orders, and view analytics.

**Q: Is multi-language support available?**
A: Yes, the platform supports Indonesian and English, with the ability to add more languages.

---

## 📞 Support

### Community Support
- **GitHub Issues**: Report bugs and request features
- **Documentation**: Check the latest documentation
- **Community Forum**: Join discussions with other users

### Professional Support
For enterprise support, customization, and consulting services:

- **Email**: support@umkmdigital.id
- **Website**: https://umkmdigital.id
- **WhatsApp**: +62-XXX-XXXX-XXXX

### Contributing
We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### License
This project is licensed under LGPL-3. See the [LICENSE](LICENSE) file for details.

---

## 📝 Changelog

### Version 1.0.0 (Current)
- Initial release
- Multi-vendor marketplace functionality
- Indonesian payment methods integration
- Product certification management
- Commission calculation system
- Mobile API endpoints
- Admin and vendor dashboards

---

## 🚀 Roadmap

### Version 1.1.0 (Planned)
- Advanced analytics and reporting
- Enhanced mobile app integration
- Social media marketing tools
- Inventory management improvements

### Version 1.2.0 (Future)
- AI-powered product recommendations
- Advanced shipping integrations
- Multi-currency support
- Enhanced SEO tools

---

*This documentation is actively maintained. For the latest updates, please check our GitHub repository.*
