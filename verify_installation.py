#!/usr/bin/env python3

"""
UMKM Marketplace Module Verification Script
This script verifies that the UMKM Marketplace module is properly installed and functional
"""

import xmlrpc.client
import time
import sys
import json

def test_connection():
    """Test connection to Odoo instance"""
    print("🔍 Testing Odoo connection...")
    
    url = 'http://localhost:8069'
    db = 'umkm_db'
    username = 'admin'
    password = 'admin'
    
    try:
        common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
        uid = common.authenticate(db, username, password, {})
        
        if uid:
            print(f"✅ Successfully connected to Odoo (User ID: {uid})")
            models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
            return models, db, uid, password
        else:
            print("❌ Failed to authenticate with Odoo")
            return None, None, None, None
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return None, None, None, None

def verify_module_installation(models, db, uid, password):
    """Verify that the UMKM module is installed"""
    print("\n📦 Verifying module installation...")
    
    try:
        # Check module status
        module_ids = models.execute_kw(db, uid, password,
            'ir.module.module', 'search',
            [[['name', '=', 'umkm_marketplace']]])
        
        if not module_ids:
            print("❌ UMKM Marketplace module not found")
            return False
        
        module_info = models.execute_kw(db, uid, password,
            'ir.module.module', 'read',
            [module_ids[0]], {'fields': ['name', 'state', 'summary']})
        
        module = module_info[0]
        print(f"📋 Module: {module['name']}")
        print(f"📊 Status: {module['state']}")
        print(f"📝 Summary: {module.get('summary', 'N/A')}")
        
        if module['state'] == 'installed':
            print("✅ Module is properly installed")
            return True
        else:
            print(f"⚠️ Module state is: {module['state']}")
            return False
            
    except Exception as e:
        print(f"❌ Error checking module: {e}")
        return False

def verify_models(models, db, uid, password):
    """Verify that all UMKM models are accessible"""
    print("\n🏗️ Verifying models...")
    
    umkm_models = {
        'umkm.vendor': 'Vendor Management',
        'umkm.product': 'Product Catalog',
        'umkm.order': 'Order Processing',
        'umkm.commission': 'Commission Management',
        'umkm.certification': 'Certification Management',
        'umkm.dashboard': 'Dashboard Analytics'
    }
    
    model_status = {}
    
    for model_name, description in umkm_models.items():
        try:
            # Try to access the model
            count = models.execute_kw(db, uid, password,
                model_name, 'search_count', [[]])
            
            # Try to get model fields
            fields = models.execute_kw(db, uid, password,
                model_name, 'fields_get', [])
            
            print(f"✅ {description} ({model_name}): {count} records, {len(fields)} fields")
            model_status[model_name] = {
                'accessible': True,
                'record_count': count,
                'field_count': len(fields)
            }
            
        except Exception as e:
            print(f"❌ {description} ({model_name}): Error - {e}")
            model_status[model_name] = {
                'accessible': False,
                'error': str(e)
            }
    
    return model_status

def verify_views(models, db, uid, password):
    """Verify that all UMKM views are created"""
    print("\n👁️ Verifying views...")
    
    try:
        # Search for UMKM-related views
        view_ids = models.execute_kw(db, uid, password,
            'ir.ui.view', 'search',
            [[['name', 'ilike', 'umkm']]])
        
        if view_ids:
            views = models.execute_kw(db, uid, password,
                'ir.ui.view', 'read',
                [view_ids], {'fields': ['name', 'model', 'type']})
            
            print(f"📋 Found {len(views)} UMKM views:")
            
            view_types = {}
            for view in views:
                model = view['model']
                view_type = view['type']
                
                if model not in view_types:
                    view_types[model] = []
                view_types[model].append(view_type)
                
                print(f"  • {view['name']} ({model}, {view_type})")
            
            # Verify that each model has the essential views
            essential_views = ['form', 'tree']
            missing_views = []
            
            for model in ['umkm.vendor', 'umkm.product', 'umkm.order', 'umkm.commission']:
                if model in view_types:
                    for view_type in essential_views:
                        if view_type not in view_types[model]:
                            missing_views.append(f"{model} - {view_type}")
            
            if missing_views:
                print("⚠️ Missing essential views:")
                for missing in missing_views:
                    print(f"  • {missing}")
            else:
                print("✅ All essential views are present")
            
            return True
        else:
            print("❌ No UMKM views found")
            return False
            
    except Exception as e:
        print(f"❌ Error verifying views: {e}")
        return False

def verify_menus(models, db, uid, password):
    """Verify that UMKM menus are created"""
    print("\n📋 Verifying menus...")
    
    try:
        # Search for UMKM main menu
        menu_ids = models.execute_kw(db, uid, password,
            'ir.ui.menu', 'search',
            [[['name', '=', 'UMKM Marketplace']]])
        
        if menu_ids:
            # Get submenu items
            submenu_ids = models.execute_kw(db, uid, password,
                'ir.ui.menu', 'search',
                [[['parent_id', 'in', menu_ids]]])
            
            if submenu_ids:
                submenus = models.execute_kw(db, uid, password,
                    'ir.ui.menu', 'read',
                    [submenu_ids], {'fields': ['name', 'sequence']})
                
                print(f"✅ UMKM Marketplace menu found with {len(submenus)} submenus:")
                for submenu in sorted(submenus, key=lambda x: x['sequence']):
                    print(f"  • {submenu['name']}")
                
                return True
            else:
                print("⚠️ UMKM main menu found but no submenus")
                return False
        else:
            print("❌ UMKM Marketplace menu not found")
            return False
            
    except Exception as e:
        print(f"❌ Error verifying menus: {e}")
        return False

def verify_security(models, db, uid, password):
    """Verify that security groups and access rights are configured"""
    print("\n🔒 Verifying security configuration...")
    
    try:
        # Check for UMKM groups
        group_names = ['UMKM Administrator', 'UMKM Manager', 'UMKM Vendor']
        found_groups = []
        
        for group_name in group_names:
            group_ids = models.execute_kw(db, uid, password,
                'res.groups', 'search',
                [[['name', '=', group_name]]])
            
            if group_ids:
                found_groups.append(group_name)
                print(f"✅ Security group found: {group_name}")
            else:
                print(f"❌ Security group missing: {group_name}")
        
        # Check access rights
        access_ids = models.execute_kw(db, uid, password,
            'ir.model.access', 'search',
            [[['name', 'ilike', 'umkm']]])
        
        if access_ids:
            print(f"✅ Found {len(access_ids)} UMKM access rights")
        else:
            print("❌ No UMKM access rights found")
        
        return len(found_groups) == len(group_names) and len(access_ids) > 0
        
    except Exception as e:
        print(f"❌ Error verifying security: {e}")
        return False

def verify_data(models, db, uid, password):
    """Verify that initial data is loaded"""
    print("\n📊 Verifying initial data...")
    
    try:
        data_checks = [
            ('umkm.payment.method', 'Payment Methods'),
            ('umkm.delivery.method', 'Delivery Methods'),
            ('ir.sequence', 'Sequences')
        ]
        
        all_data_ok = True
        
        for model_name, description in data_checks:
            try:
                count = models.execute_kw(db, uid, password,
                    model_name, 'search_count', [[]])
                
                if count > 0:
                    print(f"✅ {description}: {count} records")
                else:
                    print(f"⚠️ {description}: No records found")
                    all_data_ok = False
                    
            except Exception:
                print(f"❌ {description}: Model not accessible")
                all_data_ok = False
        
        return all_data_ok
        
    except Exception as e:
        print(f"❌ Error verifying data: {e}")
        return False

def test_basic_operations(models, db, uid, password):
    """Test basic CRUD operations"""
    print("\n🧪 Testing basic operations...")
    
    try:
        # Test creating a vendor
        print("Testing vendor creation...")
        vendor_data = {
            'name': 'Test Vendor',
            'email': 'test@example.com',
            'phone': '+6281234567890',
            'description': 'Test vendor for verification'
        }
        
        vendor_id = models.execute_kw(db, uid, password,
            'umkm.vendor', 'create', [vendor_data])
        
        if vendor_id:
            print(f"✅ Successfully created test vendor (ID: {vendor_id})")
            
            # Test reading the vendor
            vendor = models.execute_kw(db, uid, password,
                'umkm.vendor', 'read',
                [vendor_id], {'fields': ['name', 'email']})
            
            if vendor and vendor[0]['name'] == 'Test Vendor':
                print("✅ Successfully read vendor data")
                
                # Test updating the vendor
                models.execute_kw(db, uid, password,
                    'umkm.vendor', 'write',
                    [vendor_id, {'description': 'Updated test vendor'}])
                
                print("✅ Successfully updated vendor")
                
                # Clean up - delete the test vendor
                models.execute_kw(db, uid, password,
                    'umkm.vendor', 'unlink', [vendor_id])
                
                print("✅ Successfully deleted test vendor")
                return True
            else:
                print("❌ Failed to read vendor data correctly")
                return False
        else:
            print("❌ Failed to create test vendor")
            return False
            
    except Exception as e:
        print(f"❌ Error during basic operations test: {e}")
        return False

def generate_report(results):
    """Generate a verification report"""
    print("\n" + "="*60)
    print("📊 VERIFICATION REPORT")
    print("="*60)
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    print("\nDetailed Results:")
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
    
    if passed_tests == total_tests:
        print("\n🎉 ALL TESTS PASSED!")
        print("The UMKM Marketplace module is fully functional and ready to use.")
        print("\nNext Steps:")
        print("1. Access the web interface: http://localhost:8069")
        print("2. Login with admin credentials")
        print("3. Navigate to UMKM Marketplace menu")
        print("4. Start creating vendors and products")
    else:
        print(f"\n⚠️ {total_tests - passed_tests} TEST(S) FAILED")
        print("Please check the errors above and fix any issues.")
        print("You may need to:")
        print("1. Restart Odoo services")
        print("2. Reinstall the module")
        print("3. Check database permissions")
    
    return passed_tests == total_tests

def main():
    """Main verification function"""
    print("="*60)
    print("🔍 UMKM MARKETPLACE MODULE VERIFICATION")
    print("="*60)
    print("This script will verify that the UMKM Marketplace module")
    print("is properly installed and functional.")
    print("="*60)
    
    # Test connection
    models, db, uid, password = test_connection()
    if not models:
        print("\n❌ Cannot connect to Odoo. Make sure:")
        print("1. Odoo is running (docker-compose ps)")
        print("2. Database is accessible")
        print("3. Credentials are correct")
        sys.exit(1)
    
    # Run verification tests
    results = {}
    
    results['Module Installation'] = verify_module_installation(models, db, uid, password)
    results['Models Accessibility'] = verify_models(models, db, uid, password)
    results['Views Creation'] = verify_views(models, db, uid, password)
    results['Menus Configuration'] = verify_menus(models, db, uid, password)
    results['Security Setup'] = verify_security(models, db, uid, password)
    results['Initial Data'] = verify_data(models, db, uid, password)
    results['Basic Operations'] = test_basic_operations(models, db, uid, password)
    
    # Generate report
    success = generate_report(results)
    
    print("\n" + "="*60)
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
