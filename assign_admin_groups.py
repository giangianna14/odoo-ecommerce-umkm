#!/usr/bin/env python3
import xmlrpc.client

# Connection parameters
url = 'http://localhost:8069'
db = 'postgres'
username = 'admin'
password = 'admin'

# Connect to Odoo
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})

if uid:
    print(f"✅ Connected to Odoo as user ID: {uid}")
    
    # Get the object proxy
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
    
    try:
        # Find UMKM groups
        umkm_admin_group = models.execute_kw(db, uid, password,
            'res.groups', 'search',
            [[['name', '=', 'UMKM Administrator']]])
        
        umkm_manager_group = models.execute_kw(db, uid, password,
            'res.groups', 'search',
            [[['name', '=', 'UMKM Manager']]])
        
        umkm_vendor_group = models.execute_kw(db, uid, password,
            'res.groups', 'search',
            [[['name', '=', 'UMKM Vendor']]])
        
        if umkm_admin_group:
            print(f"✅ Found UMKM Administrator group: {umkm_admin_group[0]}")
            
            # Add admin user to UMKM groups
            admin_user = models.execute_kw(db, uid, password,
                'res.users', 'search',
                [[['login', '=', 'admin']]])
            
            if admin_user:
                # Add groups to admin user
                models.execute_kw(db, uid, password,
                    'res.users', 'write',
                    [admin_user, {'groups_id': [(4, umkm_admin_group[0])]}])
                
                print(f"✅ Added admin user to UMKM Administrator group")
            else:
                print("❌ Admin user not found")
        else:
            print("❌ UMKM Administrator group not found")
        
        # Check if the module is properly installed
        module = models.execute_kw(db, uid, password,
            'ir.module.module', 'search_read',
            [[['name', '=', 'umkm_marketplace']]],
            {'fields': ['name', 'state']})
        
        if module:
            print(f"✅ UMKM Marketplace module status: {module[0]['state']}")
        else:
            print("❌ UMKM Marketplace module not found")
        
        # Check if menu exists
        menu = models.execute_kw(db, uid, password,
            'ir.ui.menu', 'search_read',
            [[['name', '=', 'UMKM Marketplace']]],
            {'fields': ['name', 'active']})
        
        if menu:
            print(f"✅ UMKM Marketplace menu found: {menu[0]['name']}")
        else:
            print("❌ UMKM Marketplace menu not found")
        
        print("\n========================================")
        print("Setup completed! You can now:")
        print("1. Login to Odoo at http://localhost:8069")
        print("2. Use admin/admin credentials")
        print("3. Look for 'UMKM Marketplace' in the main menu")
        print("========================================")
        
    except Exception as e:
        print(f"❌ Error during setup: {e}")
else:
    print("❌ Failed to connect to Odoo")
