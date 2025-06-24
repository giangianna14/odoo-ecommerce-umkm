#!/usr/bin/env python3

"""
UMKM Marketplace Module Setup Script
This script helps install and configure the UMKM Marketplace module
"""

import xmlrpc.client
import time
import sys

def connect_to_odoo():
    """Connect to Odoo instance"""
    url = 'http://localhost:8069'
    db = 'postgres'
    username = 'admin'
    password = 'admin'
    
    try:
        common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
        uid = common.authenticate(db, username, password, {})
        
        if uid:
            print(f"✅ Connected to Odoo as user ID: {uid}")
            models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
            return models, db, uid, password
        else:
            print("❌ Failed to authenticate with Odoo")
            return None, None, None, None
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        print("Make sure Odoo is running at http://localhost:8069")
        return None, None, None, None

def install_module(models, db, uid, password):
    """Install the UMKM Marketplace module"""
    try:
        # Update module list
        print("🔄 Updating module list...")
        models.execute_kw(db, uid, password, 'ir.module.module', 'update_list', [])
        
        # Find the module
        module_ids = models.execute_kw(db, uid, password,
            'ir.module.module', 'search',
            [[['name', '=', 'umkm_marketplace']]])
        
        if not module_ids:
            print("❌ UMKM Marketplace module not found in module list")
            print("Please make sure the module files are in the correct location:")
            print("  /mnt/extra-addons/umkm_marketplace/")
            return False
        
        module_id = module_ids[0]
        
        # Check current state
        module_info = models.execute_kw(db, uid, password,
            'ir.module.module', 'read',
            [module_id], {'fields': ['name', 'state']})
        
        current_state = module_info[0]['state']
        print(f"📋 Current module state: {current_state}")
        
        if current_state == 'installed':
            print("✅ Module is already installed!")
            return True
        elif current_state in ['uninstalled', 'to upgrade']:
            print("🔄 Installing module...")
            models.execute_kw(db, uid, password,
                'ir.module.module', 'button_immediate_install', [module_id])
            print("✅ Module installation initiated!")
            return True
        else:
            print(f"ℹ️ Module is in state: {current_state}")
            return True
            
    except Exception as e:
        print(f"❌ Error installing module: {e}")
        return False

def assign_admin_groups(models, db, uid, password):
    """Assign admin user to UMKM groups"""
    try:
        # Find UMKM groups
        group_names = ['UMKM Administrator', 'UMKM Manager', 'UMKM Vendor']
        
        for group_name in group_names:
            group_ids = models.execute_kw(db, uid, password,
                'res.groups', 'search',
                [[['name', '=', group_name]]])
            
            if group_ids:
                print(f"✅ Found group: {group_name}")
                
                # Add admin user to group
                models.execute_kw(db, uid, password,
                    'res.users', 'write',
                    [uid, {'groups_id': [(4, group_ids[0])]}])
                
                print(f"✅ Added admin user to {group_name}")
            else:
                print(f"⚠️ Group not found: {group_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error assigning groups: {e}")
        return False

def verify_installation(models, db, uid, password):
    """Verify that the module is properly installed"""
    try:
        # Check module status
        module_ids = models.execute_kw(db, uid, password,
            'ir.module.module', 'search',
            [[['name', '=', 'umkm_marketplace']]])
        
        if module_ids:
            module_info = models.execute_kw(db, uid, password,
                'ir.module.module', 'read',
                [module_ids[0]], {'fields': ['name', 'state']})
            
            print(f"📋 Module status: {module_info[0]['state']}")
        
        # Check if main menu exists
        menu_ids = models.execute_kw(db, uid, password,
            'ir.ui.menu', 'search',
            [[['name', '=', 'UMKM Marketplace']]])
        
        if menu_ids:
            print("✅ UMKM Marketplace menu found!")
        else:
            print("⚠️ UMKM Marketplace menu not found")
        
        # Check models
        model_names = [
            'umkm.vendor', 'umkm.product', 'umkm.order', 
            'umkm.commission', 'umkm.dashboard'
        ]
        
        for model_name in model_names:
            try:
                count = models.execute_kw(db, uid, password,
                    model_name, 'search_count', [[]])
                print(f"✅ Model {model_name}: {count} records")
            except Exception:
                print(f"❌ Model {model_name}: Not accessible")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during verification: {e}")
        return False

def main():
    """Main setup function"""
    print("=" * 50)
    print("UMKM MARKETPLACE MODULE SETUP")
    print("=" * 50)
    
    # Connect to Odoo
    models, db, uid, password = connect_to_odoo()
    if not models:
        sys.exit(1)
    
    # Install module
    if install_module(models, db, uid, password):
        print("✅ Module installation completed")
    else:
        print("❌ Module installation failed")
        sys.exit(1)
    
    # Wait a moment for installation to complete
    print("⏳ Waiting for installation to complete...")
    time.sleep(5)
    
    # Assign groups
    if assign_admin_groups(models, db, uid, password):
        print("✅ Group assignment completed")
    else:
        print("⚠️ Group assignment had issues")
    
    # Verify installation
    print("\n" + "=" * 30)
    print("VERIFICATION RESULTS")
    print("=" * 30)
    
    verify_installation(models, db, uid, password)
    
    print("\n" + "=" * 50)
    print("SETUP COMPLETED!")
    print("=" * 50)
    print("You can now access the UMKM Marketplace:")
    print("🌐 URL: http://localhost:8069")
    print("👤 Login: admin")
    print("🔐 Password: admin")
    print("📋 Look for 'UMKM Marketplace' in the main menu")
    print("=" * 50)

if __name__ == "__main__":
    main()
