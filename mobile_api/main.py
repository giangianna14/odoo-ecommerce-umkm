"""
Mobile API endpoints untuk UMKM Marketplace
Menggunakan FastAPI sebagai API gateway yang berkomunikasi dengan Odoo
"""

from fastapi import FastAPI, HTTPException, Depends, status, File, UploadFile
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, date
import xmlrpc.client
import json
import os
from PIL import Image
import io
import base64

# Initialize FastAPI app
app = FastAPI(
    title="UMKM Marketplace Mobile API",
    description="REST API untuk aplikasi mobile UMKM Marketplace",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Odoo connection settings
ODOO_URL = os.getenv("ODOO_URL", "http://localhost:8069")
ODOO_DB = os.getenv("ODOO_DB", "umkm_marketplace")
ODOO_USERNAME = os.getenv("ODOO_USERNAME", "admin")
ODOO_PASSWORD = os.getenv("ODOO_PASSWORD", "admin")

# Odoo XML-RPC clients
common = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')

# Pydantic models for request/response
class VendorRegistration(BaseModel):
    name: str = Field(..., description="Nama usaha")
    business_type: str = Field(..., description="Jenis usaha")
    owner_name: str = Field(..., description="Nama pemilik")
    phone: str = Field(..., description="Nomor telepon")
    email: str = Field(..., description="Email")
    city: str = Field(..., description="Kota")
    province_id: Optional[int] = Field(None, description="ID provinsi")
    description: Optional[str] = Field(None, description="Deskripsi usaha")

class VendorLogin(BaseModel):
    email: str
    password: str

class ProductCreate(BaseModel):
    name: str = Field(..., description="Nama produk")
    description: Optional[str] = Field(None, description="Deskripsi produk")
    list_price: float = Field(..., description="Harga jual")
    standard_price: float = Field(..., description="Harga pokok")
    categ_id: int = Field(..., description="ID kategori")
    weight: Optional[float] = Field(0, description="Berat (kg)")
    length: Optional[float] = Field(0, description="Panjang (cm)")
    width: Optional[float] = Field(0, description="Lebar (cm)")
    height: Optional[float] = Field(0, description="Tinggi (cm)")

class OrderUpdate(BaseModel):
    status: str = Field(..., description="Status pesanan")
    tracking_number: Optional[str] = Field(None, description="Nomor resi")
    notes: Optional[str] = Field(None, description="Catatan")

class VendorResponse(BaseModel):
    id: int
    name: str
    business_type: str
    city: str
    province: str
    avg_rating: float
    product_count: int
    status: str

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    list_price: float
    image_url: str
    category: str
    weight: float
    in_stock: bool

class OrderResponse(BaseModel):
    id: int
    name: str
    partner_name: str
    amount_total: float
    state: str
    date_order: datetime
    product_count: int

# Utility functions
def get_odoo_uid():
    """Get Odoo user ID"""
    try:
        uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})
        return uid
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Odoo connection failed: {str(e)}")

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token (simplified - implement proper JWT verification)"""
    # In production, implement proper JWT verification
    token = credentials.credentials
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token

def resize_image(image_data: bytes, max_size: tuple = (800, 800)) -> bytes:
    """Resize image untuk optimasi mobile"""
    image = Image.open(io.BytesIO(image_data))
    image.thumbnail(max_size, Image.Resampling.LANCZOS)
    
    output = io.BytesIO()
    image.save(output, format='JPEG', quality=85)
    return output.getvalue()

# API Endpoints

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now()}

# Authentication endpoints
@app.post("/api/auth/register")
async def register_vendor(vendor_data: VendorRegistration):
    """Register vendor baru"""
    try:
        uid = get_odoo_uid()
        
        # Create partner first
        partner_vals = {
            'name': vendor_data.owner_name,
            'email': vendor_data.email,
            'phone': vendor_data.phone,
            'is_company': False,
            'supplier_rank': 1,
            'city': vendor_data.city,
        }
        partner_id = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'res.partner', 'create', [partner_vals]
        )
        
        # Create vendor
        vendor_vals = {
            'name': vendor_data.name,
            'business_type': vendor_data.business_type,
            'partner_id': partner_id,
            'phone': vendor_data.phone,
            'email': vendor_data.email,
            'city': vendor_data.city,
            'province_id': vendor_data.province_id,
            'description': vendor_data.description,
            'state': 'draft',
        }
        
        vendor_id = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'umkm.vendor', 'create', [vendor_vals]
        )
        
        return {
            "success": True,
            "vendor_id": vendor_id,
            "message": "Vendor berhasil didaftarkan. Menunggu verifikasi."
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/auth/login")
async def login_vendor(login_data: VendorLogin):
    """Login vendor"""
    try:
        uid = get_odoo_uid()
        
        # Find vendor by email
        vendor_ids = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'umkm.vendor', 'search',
            [[('email', '=', login_data.email)]]
        )
        
        if not vendor_ids:
            raise HTTPException(status_code=401, detail="Email tidak ditemukan")
        
        vendor = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'umkm.vendor', 'read',
            [vendor_ids[0]], {'fields': ['id', 'name', 'state', 'partner_id']}
        )[0]
        
        # In production, verify password properly
        # For now, we'll generate a simple token
        token = f"vendor_{vendor['id']}_token"
        
        return {
            "success": True,
            "token": token,
            "vendor": {
                "id": vendor['id'],
                "name": vendor['name'],
                "status": vendor['state']
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Vendor endpoints
@app.get("/api/vendors", response_model=List[VendorResponse])
async def get_vendors(
    limit: int = 20,
    offset: int = 0,
    city: Optional[str] = None,
    business_type: Optional[str] = None
):
    """Get daftar vendor"""
    try:
        uid = get_odoo_uid()
        
        domain = [('state', '=', 'active')]
        if city:
            domain.append(('city', 'ilike', city))
        if business_type:
            domain.append(('business_type', '=', business_type))
        
        vendor_ids = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'umkm.vendor', 'search',
            [domain], {'limit': limit, 'offset': offset}
        )
        
        vendors = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'umkm.vendor', 'read',
            [vendor_ids], {
                'fields': ['id', 'name', 'business_type', 'city', 'province_id', 
                          'avg_rating', 'product_count', 'state']
            }
        )
        
        result = []
        for vendor in vendors:
            result.append(VendorResponse(
                id=vendor['id'],
                name=vendor['name'],
                business_type=vendor['business_type'],
                city=vendor['city'] or '',
                province=vendor['province_id'][1] if vendor['province_id'] else '',
                avg_rating=vendor['avg_rating'],
                product_count=vendor['product_count'],
                status=vendor['state']
            ))
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/vendors/{vendor_id}")
async def get_vendor_detail(vendor_id: int):
    """Get detail vendor"""
    try:
        uid = get_odoo_uid()
        
        vendor = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'umkm.vendor', 'api_get_vendor_detail',
            [vendor_id]
        )
        
        return {"success": True, "vendor": vendor}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Product endpoints
@app.get("/api/vendors/{vendor_id}/products", response_model=List[ProductResponse])
async def get_vendor_products(
    vendor_id: int,
    limit: int = 20,
    offset: int = 0
):
    """Get produk dari vendor tertentu"""
    try:
        uid = get_odoo_uid()
        
        product_ids = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'product.template', 'search',
            [[('vendor_id', '=', vendor_id), ('sale_ok', '=', True)]],
            {'limit': limit, 'offset': offset}
        )
        
        products = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'product.template', 'read',
            [product_ids], {
                'fields': ['id', 'name', 'description_sale', 'list_price', 
                          'image_1920', 'categ_id', 'weight', 'qty_available']
            }
        )
        
        result = []
        for product in products:
            # Convert image to URL (simplified)
            image_url = f"/api/products/{product['id']}/image" if product['image_1920'] else ""
            
            result.append(ProductResponse(
                id=product['id'],
                name=product['name'],
                description=product['description_sale'] or '',
                list_price=product['list_price'],
                image_url=image_url,
                category=product['categ_id'][1] if product['categ_id'] else '',
                weight=product['weight'],
                in_stock=product['qty_available'] > 0
            ))
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/vendors/{vendor_id}/products")
async def create_product(
    vendor_id: int,
    product_data: ProductCreate,
    token: str = Depends(verify_token)
):
    """Buat produk baru"""
    try:
        uid = get_odoo_uid()
        
        product_vals = {
            'name': product_data.name,
            'description_sale': product_data.description,
            'list_price': product_data.list_price,
            'standard_price': product_data.standard_price,
            'categ_id': product_data.categ_id,
            'vendor_id': vendor_id,
            'sale_ok': True,
            'purchase_ok': True,
            'weight': product_data.weight,
            'product_length': product_data.length,
            'product_width': product_data.width,
            'product_height': product_data.height,
        }
        
        product_id = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'product.template', 'create', [product_vals]
        )
        
        return {
            "success": True,
            "product_id": product_id,
            "message": "Produk berhasil dibuat"
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/products/{product_id}/image")
async def upload_product_image(
    product_id: int,
    file: UploadFile = File(...),
    token: str = Depends(verify_token)
):
    """Upload gambar produk"""
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File harus berupa gambar")
        
        # Read and resize image
        image_data = await file.read()
        resized_image = resize_image(image_data)
        
        # Convert to base64
        image_base64 = base64.b64encode(resized_image).decode('utf-8')
        
        uid = get_odoo_uid()
        
        # Update product image
        models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'product.template', 'write',
            [[product_id], {'image_1920': image_base64}]
        )
        
        return {
            "success": True,
            "message": "Gambar berhasil diupload",
            "image_url": f"/api/products/{product_id}/image"
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Order endpoints
@app.get("/api/vendors/{vendor_id}/orders", response_model=List[OrderResponse])
async def get_vendor_orders(
    vendor_id: int,
    limit: int = 20,
    offset: int = 0,
    state: Optional[str] = None,
    token: str = Depends(verify_token)
):
    """Get pesanan vendor"""
    try:
        uid = get_odoo_uid()
        
        domain = [('vendor_id', '=', vendor_id)]
        if state:
            domain.append(('state', '=', state))
        
        order_ids = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'sale.order', 'search',
            [domain], {'limit': limit, 'offset': offset, 'order': 'date_order desc'}
        )
        
        orders = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'sale.order', 'read',
            [order_ids], {
                'fields': ['id', 'name', 'partner_id', 'amount_total', 
                          'state', 'date_order', 'order_line']
            }
        )
        
        result = []
        for order in orders:
            result.append(OrderResponse(
                id=order['id'],
                name=order['name'],
                partner_name=order['partner_id'][1],
                amount_total=order['amount_total'],
                state=order['state'],
                date_order=order['date_order'],
                product_count=len(order['order_line'])
            ))
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/orders/{order_id}/status")
async def update_order_status(
    order_id: int,
    update_data: OrderUpdate,
    token: str = Depends(verify_token)
):
    """Update status pesanan"""
    try:
        uid = get_odoo_uid()
        
        # Update order
        update_vals = {}
        
        if update_data.status == 'confirmed':
            # Confirm order
            models.execute_kw(
                ODOO_DB, uid, ODOO_PASSWORD,
                'sale.order', 'action_confirm',
                [[order_id]]
            )
        elif update_data.status == 'shipped':
            update_vals['carrier_tracking_ref'] = update_data.tracking_number
        
        if update_data.notes:
            update_vals['note'] = update_data.notes
        
        if update_vals:
            models.execute_kw(
                ODOO_DB, uid, ODOO_PASSWORD,
                'sale.order', 'write',
                [[order_id], update_vals]
            )
        
        return {
            "success": True,
            "message": "Status pesanan berhasil diupdate"
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Analytics endpoints
@app.get("/api/vendors/{vendor_id}/analytics")
async def get_vendor_analytics(
    vendor_id: int,
    period: str = "month",  # day, week, month, year
    token: str = Depends(verify_token)
):
    """Get analytics vendor"""
    try:
        uid = get_odoo_uid()
        
        # Get vendor performance summary
        vendor_performance = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'umkm.vendor', 'get_performance_summary',
            [[vendor_id]]
        )[0]
        
        # Get sales data (simplified - would need proper time-based queries)
        sales_data = {
            "daily_sales": [100, 150, 200, 180, 220, 250, 300],
            "top_products": [
                {"name": "Produk A", "sales": 50},
                {"name": "Produk B", "sales": 30},
                {"name": "Produk C", "sales": 20},
            ],
            "customer_demographics": {
                "age_groups": {"18-25": 30, "26-35": 40, "36-45": 20, "45+": 10},
                "locations": {"Jakarta": 40, "Bandung": 25, "Surabaya": 20, "Others": 15}
            }
        }
        
        return {
            "success": True,
            "performance": vendor_performance,
            "sales_data": sales_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Utility endpoints
@app.get("/api/categories")
async def get_product_categories():
    """Get kategori produk"""
    try:
        uid = get_odoo_uid()
        
        category_ids = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'product.category', 'search',
            [[]]
        )
        
        categories = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'product.category', 'read',
            [category_ids], {'fields': ['id', 'name', 'parent_id']}
        )
        
        return {"success": True, "categories": categories}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/provinces")
async def get_provinces():
    """Get daftar provinsi Indonesia"""
    try:
        uid = get_odoo_uid()
        
        province_ids = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'res.country.state', 'search',
            [[('country_id.code', '=', 'ID')]]
        )
        
        provinces = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'res.country.state', 'read',
            [province_ids], {'fields': ['id', 'name', 'code']}
        )
        
        return {"success": True, "provinces": provinces}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# WebSocket for real-time notifications (placeholder)
@app.get("/api/notifications/{vendor_id}")
async def get_notifications(vendor_id: int, token: str = Depends(verify_token)):
    """Get notifikasi vendor (placeholder for WebSocket)"""
    # In production, implement WebSocket for real-time notifications
    notifications = [
        {
            "id": 1,
            "type": "new_order",
            "title": "Pesanan Baru",
            "message": "Anda mendapat pesanan baru dari Customer A",
            "timestamp": datetime.now(),
            "read": False
        },
        {
            "id": 2,
            "type": "payment_received",
            "title": "Pembayaran Diterima",
            "message": "Pembayaran untuk order #12345 telah diterima",
            "timestamp": datetime.now(),
            "read": False
        }
    ]
    
    return {"success": True, "notifications": notifications}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
