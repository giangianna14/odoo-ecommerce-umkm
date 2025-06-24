# API Documentation - UMKM Marketplace

## 🌐 API Overview

The UMKM Marketplace provides a comprehensive RESTful API for mobile applications and third-party integrations. The API follows REST principles and returns JSON responses.

**Base URL**: `http://localhost:8069/api/v1`
**Authentication**: Bearer Token / API Key
**Content-Type**: `application/json`

## 🔐 Authentication

### Get Access Token
```bash
POST /api/auth/login
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "user_id": 1,
  "user_name": "Administrator"
}
```

### Using Token
Include the token in all subsequent requests:
```bash
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

## 👤 User Management

### Get Current User
```bash
GET /api/user/me
Authorization: Bearer {token}
```

**Response:**
```json
{
  "id": 1,
  "name": "Administrator",
  "email": "admin@example.com",
  "is_vendor": false,
  "vendor_id": null,
  "groups": ["UMKM Administrator"]
}
```

### Update User Profile
```bash
PUT /api/user/me
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Updated Name",
  "email": "new_email@example.com",
  "phone": "+6281234567890"
}
```

## 🏪 Vendor Management

### Get All Vendors
```bash
GET /api/vendors
Authorization: Bearer {token}
```

**Parameters:**
- `limit` (int): Number of results (default: 20)
- `offset` (int): Pagination offset (default: 0)
- `search` (string): Search term
- `category_id` (int): Filter by category
- `state` (string): Filter by state (draft, pending, approved)

**Response:**
```json
{
  "count": 150,
  "results": [
    {
      "id": 1,
      "name": "Toko Baju Indah",
      "description": "Menjual pakaian berkualitas",
      "email": "vendor@example.com",
      "phone": "+6281234567890",
      "address": "Jl. Sudirman No. 123",
      "state": "approved",
      "commission_rate": 5.0,
      "category_id": 1,
      "category_name": "Fashion",
      "created_date": "2024-01-15T10:30:00Z",
      "product_count": 25,
      "order_count": 150
    }
  ]
}
```

### Get Vendor Details
```bash
GET /api/vendors/{vendor_id}
Authorization: Bearer {token}
```

### Create Vendor
```bash
POST /api/vendors
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Toko Elektronik Maju",
  "description": "Menjual elektronik terbaru",
  "email": "elektronik@example.com",
  "phone": "+6281234567890",
  "address": "Jl. Teknologi No. 456",
  "category_id": 2,
  "commission_rate": 7.5,
  "business_license": "123456789",
  "tax_number": "987654321"
}
```

### Update Vendor
```bash
PUT /api/vendors/{vendor_id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Updated Vendor Name",
  "description": "Updated description",
  "commission_rate": 6.0
}
```

### Vendor Dashboard
```bash
GET /api/vendors/{vendor_id}/dashboard
Authorization: Bearer {token}
```

**Response:**
```json
{
  "vendor_id": 1,
  "sales_summary": {
    "total_revenue": 50000000,
    "total_orders": 250,
    "total_products": 30,
    "avg_order_value": 200000
  },
  "commission_summary": {
    "total_earned": 2500000,
    "pending": 500000,
    "paid": 2000000
  },
  "recent_orders": [...],
  "top_products": [...],
  "performance_chart": [...]
}
```

## 📦 Product Management

### Get All Products
```bash
GET /api/products
Authorization: Bearer {token}
```

**Parameters:**
- `limit` (int): Number of results (default: 20)
- `offset` (int): Pagination offset (default: 0)
- `search` (string): Search term
- `vendor_id` (int): Filter by vendor
- `category_id` (int): Filter by category
- `state` (string): Filter by state
- `min_price` (float): Minimum price
- `max_price` (float): Maximum price
- `has_certification` (bool): Filter certified products

**Response:**
```json
{
  "count": 500,
  "results": [
    {
      "id": 1,
      "name": "Kemeja Batik Premium",
      "description": "Kemeja batik berkualitas tinggi",
      "price": 250000,
      "currency": "IDR",
      "vendor_id": 1,
      "vendor_name": "Toko Baju Indah",
      "category_id": 1,
      "category_name": "Fashion",
      "state": "published",
      "qty_available": 50,
      "images": [
        "http://localhost:8069/web/image/product.product/1/image_1920"
      ],
      "certifications": ["halal"],
      "created_date": "2024-01-20T10:30:00Z",
      "rating": 4.5,
      "review_count": 25
    }
  ]
}
```

### Get Product Details
```bash
GET /api/products/{product_id}
Authorization: Bearer {token}
```

**Response:**
```json
{
  "id": 1,
  "name": "Kemeja Batik Premium",
  "description": "Kemeja batik berkualitas tinggi dengan motif tradisional",
  "price": 250000,
  "cost_price": 150000,
  "currency": "IDR",
  "vendor_id": 1,
  "vendor_name": "Toko Baju Indah",
  "category_id": 1,
  "category_name": "Fashion",
  "state": "published",
  "qty_available": 50,
  "virtual_available": 45,
  "weight": 0.3,
  "dimensions": {
    "length": 30,
    "width": 25,
    "height": 2
  },
  "images": [
    {
      "id": 1,
      "name": "Front View",
      "image_url": "http://localhost:8069/web/image/product.image/1/image_1920"
    }
  ],
  "certifications": [
    {
      "id": 1,
      "type": "halal",
      "name": "Halal MUI",
      "certificate_number": "HAS23050123456789",
      "issuing_authority": "MUI Pusat",
      "expiry_date": "2025-05-01"
    }
  ],
  "tags": ["batik", "premium", "formal"],
  "seo": {
    "meta_title": "Kemeja Batik Premium - Toko Baju Indah",
    "meta_description": "Kemeja batik berkualitas tinggi dengan motif tradisional",
    "keywords": "kemeja, batik, premium, formal"
  },
  "reviews": {
    "average_rating": 4.5,
    "review_count": 25,
    "rating_distribution": {
      "5": 15,
      "4": 8,
      "3": 2,
      "2": 0,
      "1": 0
    }
  }
}
```

### Create Product
```bash
POST /api/products
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Tas Kulit Asli",
  "description": "Tas kulit asli buatan tangan",
  "price": 500000,
  "cost_price": 300000,
  "vendor_id": 1,
  "category_id": 2,
  "qty_available": 20,
  "weight": 0.8,
  "dimensions": {
    "length": 35,
    "width": 25,
    "height": 15
  },
  "tags": ["tas", "kulit", "handmade"],
  "certifications": [1, 2]
}
```

### Update Product
```bash
PUT /api/products/{product_id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Updated Product Name",
  "price": 280000,
  "qty_available": 45
}
```

### Upload Product Images
```bash
POST /api/products/{product_id}/images
Authorization: Bearer {token}
Content-Type: multipart/form-data

{
  "image": [file],
  "name": "Product Image 1",
  "sequence": 1
}
```

### Product Reviews
```bash
GET /api/products/{product_id}/reviews
Authorization: Bearer {token}
```

**Parameters:**
- `limit` (int): Number of results (default: 10)
- `offset` (int): Pagination offset (default: 0)
- `rating` (int): Filter by rating (1-5)

## 🛒 Order Management

### Get All Orders
```bash
GET /api/orders
Authorization: Bearer {token}
```

**Parameters:**
- `limit` (int): Number of results (default: 20)
- `offset` (int): Pagination offset (default: 0)
- `customer_id` (int): Filter by customer
- `vendor_id` (int): Filter by vendor
- `state` (string): Filter by state
- `date_from` (date): Filter from date
- `date_to` (date): Filter to date

**Response:**
```json
{
  "count": 100,
  "results": [
    {
      "id": 1,
      "name": "SO001",
      "customer_id": 5,
      "customer_name": "John Doe",
      "date_order": "2024-01-25T14:30:00Z",
      "state": "sale",
      "amount_total": 750000,
      "currency": "IDR",
      "vendor_count": 2,
      "delivery_status": "shipped",
      "payment_status": "paid",
      "tracking_number": "JNE123456789"
    }
  ]
}
```

### Get Order Details
```bash
GET /api/orders/{order_id}
Authorization: Bearer {token}
```

**Response:**
```json
{
  "id": 1,
  "name": "SO001",
  "customer_id": 5,
  "customer_name": "John Doe",
  "customer_email": "john@example.com",
  "customer_phone": "+6281234567890",
  "date_order": "2024-01-25T14:30:00Z",
  "state": "sale",
  "amount_untaxed": 700000,
  "amount_tax": 50000,
  "amount_total": 750000,
  "currency": "IDR",
  "delivery_address": {
    "name": "John Doe",
    "street": "Jl. Sudirman No. 123",
    "city": "Jakarta",
    "zip": "12345",
    "country": "Indonesia"
  },
  "payment_method": "bank_transfer",
  "delivery_method": "jne_regular",
  "order_lines": [
    {
      "id": 1,
      "product_id": 1,
      "product_name": "Kemeja Batik Premium",
      "vendor_id": 1,
      "vendor_name": "Toko Baju Indah",
      "quantity": 2,
      "price_unit": 250000,
      "price_subtotal": 500000,
      "price_total": 500000
    }
  ],
  "vendor_orders": [
    {
      "id": 1,
      "vendor_id": 1,
      "vendor_name": "Toko Baju Indah",
      "state": "shipped",
      "tracking_number": "JNE123456789",
      "amount_total": 500000
    }
  ]
}
```

### Create Order
```bash
POST /api/orders
Authorization: Bearer {token}
Content-Type: application/json

{
  "customer_id": 5,
  "delivery_address_id": 10,
  "payment_method_id": 1,
  "delivery_method_id": 1,
  "order_lines": [
    {
      "product_id": 1,
      "quantity": 2,
      "price_unit": 250000
    },
    {
      "product_id": 2,
      "quantity": 1,
      "price_unit": 150000
    }
  ],
  "customer_note": "Mohon dikemas dengan rapi"
}
```

### Update Order Status
```bash
PUT /api/orders/{order_id}/status
Authorization: Bearer {token}
Content-Type: application/json

{
  "state": "done",
  "delivery_status": "delivered",
  "tracking_number": "JNE123456789",
  "notes": "Delivered successfully"
}
```

### Get Vendor Orders
```bash
GET /api/vendor-orders
Authorization: Bearer {token}
```

**Parameters:**
- `vendor_id` (int): Filter by vendor (required for vendor users)
- `state` (string): Filter by state
- `date_from` (date): Filter from date
- `date_to` (date): Filter to date

## 💰 Commission Management

### Get Commissions
```bash
GET /api/commissions
Authorization: Bearer {token}
```

**Parameters:**
- `vendor_id` (int): Filter by vendor
- `state` (string): Filter by state
- `commission_type` (string): Filter by type
- `date_from` (date): Filter from date
- `date_to` (date): Filter to date

**Response:**
```json
{
  "count": 50,
  "results": [
    {
      "id": 1,
      "name": "COM001",
      "vendor_id": 1,
      "vendor_name": "Toko Baju Indah",
      "commission_type": "sale",
      "base_amount": 500000,
      "commission_rate": 5.0,
      "commission_amount": 25000,
      "state": "confirmed",
      "date": "2024-01-25",
      "due_date": "2024-02-25",
      "payment_date": null,
      "is_overdue": false
    }
  ]
}
```

### Get Commission Details
```bash
GET /api/commissions/{commission_id}
Authorization: Bearer {token}
```

### Create Commission
```bash
POST /api/commissions
Authorization: Bearer {token}
Content-Type: application/json

{
  "vendor_id": 1,
  "vendor_order_id": 5,
  "commission_type": "sale",
  "base_amount": 500000,
  "commission_rate": 5.0,
  "due_date": "2024-02-25",
  "description": "Commission for order SO001"
}
```

### Commission Summary
```bash
GET /api/commissions/summary
Authorization: Bearer {token}
```

**Parameters:**
- `vendor_id` (int): Filter by vendor
- `period` (string): Period (monthly, quarterly, yearly)
- `year` (int): Year
- `month` (int): Month (if period is monthly)

**Response:**
```json
{
  "period": "2024-01",
  "vendor_id": 1,
  "total_commission": 500000,
  "paid_commission": 300000,
  "pending_commission": 200000,
  "commission_count": 20,
  "breakdown": {
    "sale": 450000,
    "listing": 50000
  }
}
```

## 📊 Analytics & Reports

### Sales Analytics
```bash
GET /api/analytics/sales
Authorization: Bearer {token}
```

**Parameters:**
- `vendor_id` (int): Filter by vendor
- `period` (string): Period (daily, weekly, monthly, yearly)
- `date_from` (date): Start date
- `date_to` (date): End date
- `group_by` (string): Group by (vendor, category, product)

**Response:**
```json
{
  "period": "monthly",
  "date_from": "2024-01-01",
  "date_to": "2024-01-31",
  "total_sales": 50000000,
  "total_orders": 200,
  "avg_order_value": 250000,
  "top_vendors": [
    {
      "vendor_id": 1,
      "vendor_name": "Toko Baju Indah",
      "sales": 10000000,
      "orders": 50
    }
  ],
  "top_products": [
    {
      "product_id": 1,
      "product_name": "Kemeja Batik Premium",
      "sales": 5000000,
      "quantity_sold": 20
    }
  ],
  "sales_chart": [
    {
      "date": "2024-01-01",
      "sales": 1000000,
      "orders": 5
    }
  ]
}
```

### Product Analytics
```bash
GET /api/analytics/products
Authorization: Bearer {token}
```

**Parameters:**
- `vendor_id` (int): Filter by vendor
- `category_id` (int): Filter by category
- `period` (string): Period
- `metric` (string): Metric (sales, views, conversions)

### Vendor Performance
```bash
GET /api/analytics/vendors
Authorization: Bearer {token}
```

**Parameters:**
- `period` (string): Period
- `metric` (string): Metric (sales, orders, commission)
- `limit` (int): Number of top vendors

## 🔧 Configuration

### Payment Methods
```bash
GET /api/config/payment-methods
Authorization: Bearer {token}
```

**Response:**
```json
{
  "results": [
    {
      "id": 1,
      "name": "Bank Transfer",
      "code": "bank_transfer",
      "active": true,
      "provider": "manual",
      "description": "Transfer bank manual"
    },
    {
      "id": 2,
      "name": "OVO",
      "code": "ovo",
      "active": true,
      "provider": "xendit",
      "description": "Pembayaran menggunakan OVO"
    }
  ]
}
```

### Delivery Methods
```bash
GET /api/config/delivery-methods
Authorization: Bearer {token}
```

### Categories
```bash
GET /api/config/categories
Authorization: Bearer {token}
```

**Response:**
```json
{
  "results": [
    {
      "id": 1,
      "name": "Fashion",
      "parent_id": null,
      "child_ids": [2, 3],
      "product_count": 150
    },
    {
      "id": 2,
      "name": "Pakaian Pria",
      "parent_id": 1,
      "child_ids": [],
      "product_count": 75
    }
  ]
}
```

## 📱 Mobile App Integration

### App Configuration
```bash
GET /api/mobile/config
Authorization: Bearer {token}
```

**Response:**
```json
{
  "app_name": "UMKM Marketplace",
  "version": "1.0.0",
  "api_version": "v1",
  "features": {
    "push_notifications": true,
    "offline_mode": true,
    "biometric_auth": true
  },
  "payment_methods": [...],
  "delivery_methods": [...],
  "supported_languages": ["id", "en"]
}
```

### Push Notifications
```bash
POST /api/mobile/notifications/register
Authorization: Bearer {token}
Content-Type: application/json

{
  "device_token": "fcm_device_token_here",
  "platform": "android",
  "app_version": "1.0.0"
}
```

### Offline Sync
```bash
GET /api/mobile/sync
Authorization: Bearer {token}
```

**Parameters:**
- `last_sync` (datetime): Last sync timestamp
- `models` (array): Models to sync

## 🔒 Error Handling

### Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": {
      "field": "price",
      "message": "Price must be greater than 0"
    }
  },
  "timestamp": "2024-01-25T14:30:00Z",
  "request_id": "req_123456789"
}
```

### Common Error Codes
- `AUTHENTICATION_FAILED`: Invalid credentials
- `AUTHORIZATION_DENIED`: Insufficient permissions
- `VALIDATION_ERROR`: Data validation failed
- `NOT_FOUND`: Resource not found
- `RATE_LIMIT_EXCEEDED`: Too many requests
- `INTERNAL_ERROR`: Server error

### HTTP Status Codes
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `422`: Validation Error
- `429`: Rate Limit Exceeded
- `500`: Internal Server Error

## 📈 Rate Limiting

- **Default Limit**: 1000 requests per hour per user
- **Burst Limit**: 100 requests per minute
- **Headers**:
  - `X-RateLimit-Limit`: Rate limit
  - `X-RateLimit-Remaining`: Remaining requests
  - `X-RateLimit-Reset`: Reset time

## 🧪 Testing

### API Testing with curl
```bash
# Get access token
curl -X POST http://localhost:8069/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin"}'

# Use token for API calls
curl -X GET http://localhost:8069/api/products \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Postman Collection
Import the provided Postman collection for easy API testing:
- [Download Collection](api/postman/UMKM_Marketplace_API.postman_collection.json)

---

*For more information and examples, check our [GitHub repository](https://github.com/YOUR_USERNAME/odoo-ecommerce-umkm).*
