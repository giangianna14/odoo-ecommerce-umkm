# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class UmkmDashboard(models.Model):
    _name = 'umkm.dashboard'
    _description = 'UMKM Dashboard'

    name = fields.Char('Dashboard Name', default='UMKM Dashboard')
    
    # Sales Metrics
    total_sales = fields.Float('Total Sales', compute='_compute_sales_metrics')
    monthly_sales = fields.Float('Monthly Sales', compute='_compute_sales_metrics')
    daily_sales = fields.Float('Daily Sales', compute='_compute_sales_metrics')
    sales_growth = fields.Float('Sales Growth %', compute='_compute_sales_metrics')
    
    # Order Metrics
    total_orders = fields.Integer('Total Orders', compute='_compute_order_metrics')
    pending_orders = fields.Integer('Pending Orders', compute='_compute_order_metrics')
    completed_orders = fields.Integer('Completed Orders', compute='_compute_order_metrics')
    cancelled_orders = fields.Integer('Cancelled Orders', compute='_compute_order_metrics')
    
    # Vendor Metrics
    total_vendors = fields.Integer('Total Vendors', compute='_compute_vendor_metrics')
    active_vendors = fields.Integer('Active Vendors', compute='_compute_vendor_metrics')
    new_vendors_this_month = fields.Integer('New Vendors This Month', compute='_compute_vendor_metrics')
    top_vendor_id = fields.Many2one('umkm.vendor', string='Top Vendor', compute='_compute_vendor_metrics')
    
    # Product Metrics
    total_products = fields.Integer('Total Products', compute='_compute_product_metrics')
    published_products = fields.Integer('Published Products', compute='_compute_product_metrics')
    pending_approval_products = fields.Integer('Pending Approval', compute='_compute_product_metrics')
    low_stock_products = fields.Integer('Low Stock Products', compute='_compute_product_metrics')
    
    # Commission Metrics
    total_commission = fields.Float('Total Commission', compute='_compute_commission_metrics')
    monthly_commission = fields.Float('Monthly Commission', compute='_compute_commission_metrics')
    pending_commission = fields.Float('Pending Commission', compute='_compute_commission_metrics')
    paid_commission = fields.Float('Paid Commission', compute='_compute_commission_metrics')
    
    # Customer Metrics
    total_customers = fields.Integer('Total Customers', compute='_compute_customer_metrics')
    new_customers_this_month = fields.Integer('New Customers This Month', compute='_compute_customer_metrics')
    repeat_customers = fields.Integer('Repeat Customers', compute='_compute_customer_metrics')
    
    # Financial Metrics
    revenue_today = fields.Float('Revenue Today', compute='_compute_financial_metrics')
    revenue_this_week = fields.Float('Revenue This Week', compute='_compute_financial_metrics')
    revenue_this_month = fields.Float('Revenue This Month', compute='_compute_financial_metrics')
    average_order_value = fields.Float('Average Order Value', compute='_compute_financial_metrics')
    
    # Last Update
    last_update = fields.Datetime('Last Update', default=fields.Datetime.now)

    def _compute_sales_metrics(self):
        for dashboard in self:
            # Get current month and previous month data
            today = fields.Date.today()
            current_month_start = today.replace(day=1)
            
            # Total sales
            total_sales = self.env['umkm.order'].search([
                ('state', '=', 'done')
            ])
            dashboard.total_sales = sum(total_sales.mapped('amount_total'))
            
            # Monthly sales
            monthly_orders = self.env['umkm.order'].search([
                ('state', '=', 'done'),
                ('date_order', '>=', current_month_start)
            ])
            dashboard.monthly_sales = sum(monthly_orders.mapped('amount_total'))
            
            # Daily sales
            daily_orders = self.env['umkm.order'].search([
                ('state', '=', 'done'),
                ('date_order', '>=', today)
            ])
            dashboard.daily_sales = sum(daily_orders.mapped('amount_total'))
            
            # Sales growth (placeholder)
            dashboard.sales_growth = 0.0

    def _compute_order_metrics(self):
        for dashboard in self:
            dashboard.total_orders = self.env['umkm.order'].search_count([])
            dashboard.pending_orders = self.env['umkm.order'].search_count([('state', '=', 'draft')])
            dashboard.completed_orders = self.env['umkm.order'].search_count([('state', '=', 'done')])
            dashboard.cancelled_orders = self.env['umkm.order'].search_count([('state', '=', 'cancel')])

    def _compute_vendor_metrics(self):
        for dashboard in self:
            dashboard.total_vendors = self.env['umkm.vendor'].search_count([])
            dashboard.active_vendors = self.env['umkm.vendor'].search_count([('active', '=', True)])
            
            # New vendors this month
            today = fields.Date.today()
            current_month_start = today.replace(day=1)
            dashboard.new_vendors_this_month = self.env['umkm.vendor'].search_count([
                ('create_date', '>=', current_month_start)
            ])
            
            # Top vendor by sales
            top_vendor = self.env['umkm.vendor'].search([], limit=1)  # Simplified
            dashboard.top_vendor_id = top_vendor.id if top_vendor else False

    def _compute_product_metrics(self):
        for dashboard in self:
            dashboard.total_products = self.env['umkm.product'].search_count([])
            dashboard.published_products = self.env['umkm.product'].search_count([('state', '=', 'published')])
            dashboard.pending_approval_products = self.env['umkm.product'].search_count([('state', '=', 'pending')])
            dashboard.low_stock_products = self.env['umkm.product'].search_count([('qty_available', '<', 10)])

    def _compute_commission_metrics(self):
        for dashboard in self:
            commissions = self.env['umkm.commission'].search([])
            dashboard.total_commission = sum(commissions.mapped('commission_amount'))
            dashboard.pending_commission = sum(commissions.filtered(lambda c: c.state != 'paid').mapped('commission_amount'))
            dashboard.paid_commission = sum(commissions.filtered(lambda c: c.state == 'paid').mapped('commission_amount'))
            
            # Monthly commission
            today = fields.Date.today()
            current_month_start = today.replace(day=1)
            monthly_commissions = commissions.filtered(lambda c: c.date >= current_month_start)
            dashboard.monthly_commission = sum(monthly_commissions.mapped('commission_amount'))

    def _compute_customer_metrics(self):
        for dashboard in self:
            dashboard.total_customers = self.env['res.partner'].search_count([('is_company', '=', False)])
            
            # New customers this month
            today = fields.Date.today()
            current_month_start = today.replace(day=1)
            dashboard.new_customers_this_month = self.env['res.partner'].search_count([
                ('is_company', '=', False),
                ('create_date', '>=', current_month_start)
            ])
            
            # Repeat customers (simplified)
            dashboard.repeat_customers = 0

    def _compute_financial_metrics(self):
        for dashboard in self:
            today = fields.Date.today()
            
            # Revenue today
            today_orders = self.env['umkm.order'].search([
                ('state', '=', 'done'),
                ('date_order', '>=', today)
            ])
            dashboard.revenue_today = sum(today_orders.mapped('amount_total'))
            
            # Revenue this week
            week_start = today - fields.timedelta(days=today.weekday())
            week_orders = self.env['umkm.order'].search([
                ('state', '=', 'done'),
                ('date_order', '>=', week_start)
            ])
            dashboard.revenue_this_week = sum(week_orders.mapped('amount_total'))
            
            # Revenue this month
            month_start = today.replace(day=1)
            month_orders = self.env['umkm.order'].search([
                ('state', '=', 'done'),
                ('date_order', '>=', month_start)
            ])
            dashboard.revenue_this_month = sum(month_orders.mapped('amount_total'))
            
            # Average order value
            total_orders = self.env['umkm.order'].search([('state', '=', 'done')])
            if total_orders:
                dashboard.average_order_value = sum(total_orders.mapped('amount_total')) / len(total_orders)
            else:
                dashboard.average_order_value = 0.0

    def action_refresh_dashboard(self):
        """Refresh dashboard data"""
        self.last_update = fields.Datetime.now()
        # Force recomputation of all computed fields
        self._compute_sales_metrics()
        self._compute_order_metrics()
        self._compute_vendor_metrics()
        self._compute_product_metrics()
        self._compute_commission_metrics()
        self._compute_customer_metrics()
        self._compute_financial_metrics()
        
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }


class UmkmPaymentMethod(models.Model):
    _name = 'umkm.payment.method'
    _description = 'Payment Method'
    _order = 'sequence, name'

    name = fields.Char('Method Name', required=True)
    code = fields.Char('Code', required=True)
    sequence = fields.Integer('Sequence', default=10)
    active = fields.Boolean('Active', default=True)
    
    # Indonesian specific payment methods
    method_type = fields.Selection([
        ('bank_transfer', 'Bank Transfer'),
        ('virtual_account', 'Virtual Account'),
        ('ewallet', 'E-Wallet'),
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('cash_on_delivery', 'Cash on Delivery'),
        ('qris', 'QRIS'),
        ('instalment', 'Instalment')
    ], string='Method Type', required=True)
    
    provider = fields.Char('Provider')
    description = fields.Text('Description')
    fees = fields.Float('Transaction Fees (%)')
    min_amount = fields.Float('Minimum Amount')
    max_amount = fields.Float('Maximum Amount')
    
    # Configuration
    is_online = fields.Boolean('Online Payment', default=True)
    requires_verification = fields.Boolean('Requires Verification', default=False)
    processing_time = fields.Char('Processing Time')
    
    # Images
    icon = fields.Image('Icon', max_width=128, max_height=128)


class UmkmDeliveryMethod(models.Model):
    _name = 'umkm.delivery.method'
    _description = 'Delivery Method'
    _order = 'sequence, name'

    name = fields.Char('Method Name', required=True)
    code = fields.Char('Code', required=True)
    sequence = fields.Integer('Sequence', default=10)
    active = fields.Boolean('Active', default=True)
    
    # Indonesian specific delivery services
    provider = fields.Selection([
        ('jne', 'JNE'),
        ('pos', 'Pos Indonesia'),
        ('tiki', 'TIKI'),
        ('jnt', 'J&T Express'),
        ('sicepat', 'SiCepat'),
        ('anteraja', 'AnterAja'),
        ('ninja', 'Ninja Express'),
        ('gosend', 'GoSend'),
        ('grab', 'GrabExpress'),
        ('pickup', 'Self Pickup'),
        ('other', 'Other')
    ], string='Provider', required=True)
    
    service_type = fields.Char('Service Type')  # REG, YES, OKE, etc.
    description = fields.Text('Description')
    
    # Pricing
    base_price = fields.Float('Base Price')
    price_per_kg = fields.Float('Price per KG')
    
    # Delivery Info
    estimated_days_min = fields.Integer('Min Delivery Days')
    estimated_days_max = fields.Integer('Max Delivery Days')
    max_weight = fields.Float('Maximum Weight (KG)')
    
    # Coverage
    coverage_area_ids = fields.Many2many('res.country.state', string='Coverage Areas')
    
    # Features
    has_tracking = fields.Boolean('Has Tracking', default=True)
    has_insurance = fields.Boolean('Has Insurance', default=False)
    requires_pickup = fields.Boolean('Requires Pickup', default=False)
    
    # Images
    logo = fields.Image('Logo', max_width=128, max_height=128)
