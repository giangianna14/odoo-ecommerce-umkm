{
    'name': 'UMKM Marketplace',
    'version': '17.0.1.0.0',
    'category': 'eCommerce',
    'summary': 'Multi-vendor marketplace solution for Indonesian UMKM',
    'description': """
        UMKM Marketplace Module
        =======================
        
        This module provides comprehensive marketplace functionality specifically 
        designed for Indonesian UMKM (Usaha Mikro, Kecil, dan Menengah) including:
        
        * Multi-vendor product management
        * Commission management system
        * Indonesian payment gateway integration
        * Local shipping provider integration
        * UMKM certification tracking
        * Vendor performance analytics
        * Customer review and rating system
        * Mobile API endpoints
        
        Key Features:
        - Vendor onboarding with business verification
        - Product certification management (Halal, SNI, etc.)
        - Automated commission calculation
        - Integrated Indonesian payment methods
        - Real-time order tracking
        - Comprehensive vendor dashboard
        - Multi-language support (Indonesian/English)
    """,
    'author': 'UMKM Digital Solutions',
    'website': 'https://umkmdigital.id',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'website',
        'website_sale',
        'sale_management',
        'purchase',
        'stock',
        'account',
        'payment',
        'website_payment',
        'portal',
        'rating',
        'hr',
        'project',
        'calendar',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        
        # Data files
        'data/sequences.xml',
        'data/dashboard.xml',
        'data/payment_methods.xml',
        'data/shipping_methods.xml',
        'data/certification_types.xml',
        'data/commission_rules.xml',
        
        # Views
        'views/vendor_views.xml',
        'views/product_views.xml',
        'views/order_views.xml',
        'views/commission_views.xml',
        'views/certification_views.xml',
        'views/dashboard_views.xml',
        
        # Website templates
        'views/website_templates.xml',
        'views/vendor_portal_templates.xml',
        'views/customer_portal_templates.xml',
        
        # Reports
        'reports/vendor_report.xml',
        'reports/commission_report.xml',
        'reports/sales_report.xml',
        
        # Wizards
        'wizard/vendor_onboarding_wizard.xml',
        'wizard/bulk_product_upload_wizard.xml',
        'wizard/commission_calculation_wizard.xml',
        
        # Menus
        'views/menu.xml',
    ],
    'demo': [
        'demo/vendors.xml',
        'demo/products.xml',
        'demo/orders.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'umkm_marketplace/static/src/css/backend.css',
            'umkm_marketplace/static/src/js/dashboard.js',
            'umkm_marketplace/static/src/js/vendor_management.js',
            'umkm_marketplace/static/src/xml/dashboard_templates.xml',
        ],
        'web.assets_frontend': [
            'umkm_marketplace/static/src/css/frontend.css',
            'umkm_marketplace/static/src/js/marketplace.js',
            'umkm_marketplace/static/src/js/vendor_portal.js',
            'umkm_marketplace/static/src/css/indonesian_theme.css',
        ],
        'web.assets_qweb': [
            'umkm_marketplace/static/src/xml/marketplace_templates.xml',
        ],
    },
    'external_dependencies': {
        'python': [
            'requests',
            'pillow',
            'phonenumbers',
            'geopy',
        ],
    },
    'images': [
        'static/description/banner.png',
        'static/description/icon.png',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'sequence': 10,
    'price': 999.00,
    'currency': 'USD',
    'live_test_url': 'https://demo.umkmdigital.id',
    'support': 'support@umkmdigital.id',
}
