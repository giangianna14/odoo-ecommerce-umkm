# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class UmkmOrder(models.Model):
    _name = 'umkm.order'
    _description = 'UMKM Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_order desc'

    name = fields.Char('Order Reference', required=True, copy=False, readonly=True, 
                      default=lambda self: _('New'))
    
    # Customer Information
    customer_id = fields.Many2one('res.partner', string='Customer', required=True)
    customer_email = fields.Char('Customer Email', related='customer_id.email')
    customer_phone = fields.Char('Customer Phone', related='customer_id.phone')
    
    # Order Information
    date_order = fields.Datetime('Order Date', required=True, default=fields.Datetime.now)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, copy=False, index=True, tracking=True, default='draft')
    
    # Multi-vendor support
    vendor_orders = fields.One2many('umkm.vendor.order', 'main_order_id', string='Vendor Orders')
    vendor_count = fields.Integer('Vendor Count', compute='_compute_vendor_count')
    
    # Order Lines
    order_line_ids = fields.One2many('umkm.order.line', 'order_id', string='Order Lines')
    
    # Amounts
    amount_untaxed = fields.Float('Untaxed Amount', compute='_compute_amounts', store=True)
    amount_tax = fields.Float('Tax Amount', compute='_compute_amounts', store=True)
    amount_total = fields.Float('Total Amount', compute='_compute_amounts', store=True)
    amount_delivery = fields.Float('Delivery Cost', default=0.0)
    
    # Currency
    currency_id = fields.Many2one('res.currency', string='Currency', 
                                 default=lambda self: self.env.company.currency_id)
    
    # Delivery Information
    delivery_address_id = fields.Many2one('res.partner', string='Delivery Address')
    delivery_method_id = fields.Many2one('umkm.delivery.method', string='Delivery Method')
    delivery_tracking_number = fields.Char('Tracking Number')
    delivery_status = fields.Selection([
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed')
    ], string='Delivery Status', default='pending')
    
    # Payment Information
    payment_method_id = fields.Many2one('umkm.payment.method', string='Payment Method')
    payment_status = fields.Selection([
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('partial', 'Partially Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded')
    ], string='Payment Status', default='pending')
    payment_reference = fields.Char('Payment Reference')
    
    # Dates
    confirmation_date = fields.Datetime('Confirmation Date')
    expected_delivery_date = fields.Date('Expected Delivery Date')
    delivery_date = fields.Datetime('Delivery Date')
    
    # Notes
    note = fields.Text('Internal Notes')
    customer_note = fields.Text('Customer Notes')

    @api.depends('vendor_orders')
    def _compute_vendor_count(self):
        for order in self:
            order.vendor_count = len(order.vendor_orders)

    @api.depends('order_line_ids.price_subtotal')
    def _compute_amounts(self):
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line_ids:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
            order.amount_untaxed = amount_untaxed
            order.amount_tax = amount_tax
            order.amount_total = amount_untaxed + amount_tax + order.amount_delivery

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('umkm.order') or _('New')
        return super(UmkmOrder, self).create(vals)

    def action_confirm(self):
        """Confirm the order"""
        self.state = 'sale'
        self.confirmation_date = fields.Datetime.now()
        # Create vendor orders
        self._create_vendor_orders()

    def action_view_vendor_orders(self):
        """View vendor orders related to this order"""
        action = self.env.ref('umkm_marketplace.umkm_vendor_order_action').read()[0]
        action['domain'] = [('order_id', '=', self.id)]
        action['context'] = {'default_order_id': self.id}
        return action

    def _create_vendor_orders(self):
        """Create individual vendor orders from main order"""
        vendor_lines = {}
        for line in self.order_line_ids:
            vendor_id = line.product_id.vendor_id.id
            if vendor_id not in vendor_lines:
                vendor_lines[vendor_id] = []
            vendor_lines[vendor_id].append(line)
        
        for vendor_id, lines in vendor_lines.items():
            vendor_order = self.env['umkm.vendor.order'].create({
                'main_order_id': self.id,
                'vendor_id': vendor_id,
                'customer_id': self.customer_id.id,
                'date_order': self.date_order,
                'delivery_address_id': self.delivery_address_id.id,
                'state': 'confirmed',
            })
            
            for line in lines:
                line.vendor_order_id = vendor_order.id


class UmkmOrderLine(models.Model):
    _name = 'umkm.order.line'
    _description = 'UMKM Order Line'

    order_id = fields.Many2one('umkm.order', string='Order', required=True, ondelete='cascade')
    vendor_order_id = fields.Many2one('umkm.vendor.order', string='Vendor Order')
    product_id = fields.Many2one('umkm.product', string='Product', required=True)
    vendor_id = fields.Many2one('umkm.vendor', string='Vendor', related='product_id.vendor_id', store=True)
    
    name = fields.Text('Description', required=True)
    sequence = fields.Integer('Sequence', default=10)
    
    price_unit = fields.Float('Unit Price', required=True, default=0.0)
    product_uom_qty = fields.Float('Quantity', required=True, default=1.0)
    
    price_subtotal = fields.Float('Subtotal', compute='_compute_amount', store=True)
    price_tax = fields.Float('Tax Amount', compute='_compute_amount', store=True)
    price_total = fields.Float('Total', compute='_compute_amount', store=True)
    
    tax_ids = fields.Many2many('account.tax', string='Taxes')
    discount = fields.Float('Discount (%)', default=0.0)
    
    # Product information
    product_image = fields.Image('Product Image', related='product_id.image_128')

    @api.depends('product_uom_qty', 'price_unit', 'tax_ids', 'discount')
    def _compute_amount(self):
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            line.price_subtotal = price * line.product_uom_qty
            
            # Calculate tax (simplified)
            tax_amount = 0.0
            if line.tax_ids:
                tax_rate = sum(line.tax_ids.mapped('amount')) / 100
                tax_amount = line.price_subtotal * tax_rate
            
            line.price_tax = tax_amount
            line.price_total = line.price_subtotal + tax_amount

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.name = self.product_id.name
            self.price_unit = self.product_id.price


class UmkmVendorOrder(models.Model):
    _name = 'umkm.vendor.order'
    _description = 'Vendor Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Reference', required=True, copy=False, readonly=True, 
                      default=lambda self: _('New'))
    main_order_id = fields.Many2one('umkm.order', string='Main Order', required=True)
    vendor_id = fields.Many2one('umkm.vendor', string='Vendor', required=True)
    customer_id = fields.Many2one('res.partner', string='Customer', required=True)
    
    date_order = fields.Datetime('Order Date', required=True)
    state = fields.Selection([
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('ready', 'Ready to Ship'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='confirmed', tracking=True)
    
    order_line_ids = fields.One2many('umkm.order.line', 'vendor_order_id', string='Order Lines')
    
    # Delivery
    delivery_address_id = fields.Many2one('res.partner', string='Delivery Address')
    delivery_method_id = fields.Many2one('umkm.delivery.method', string='Delivery Method')
    tracking_number = fields.Char('Tracking Number')
    
    # Amounts
    amount_total = fields.Float('Total Amount', compute='_compute_amount')
    commission_amount = fields.Float('Commission Amount', compute='_compute_commission')
    vendor_amount = fields.Float('Vendor Amount', compute='_compute_vendor_amount')
    
    @api.depends('order_line_ids.price_total')
    def _compute_amount(self):
        for order in self:
            order.amount_total = sum(order.order_line_ids.mapped('price_total'))
    
    def _compute_commission(self):
        for order in self:
            # Calculate commission based on vendor commission rate
            commission_rate = order.vendor_id.commission_rate / 100
            order.commission_amount = order.amount_total * commission_rate
    
    @api.depends('amount_total', 'commission_amount')
    def _compute_vendor_amount(self):
        for order in self:
            order.vendor_amount = order.amount_total - order.commission_amount

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('umkm.vendor.order') or _('New')
        return super(UmkmVendorOrder, self).create(vals)

    def action_process(self):
        """Mark order as processing"""
        self.state = 'processing'

    def action_ready_to_ship(self):
        """Mark order as ready to ship"""
        self.state = 'ready'

    def action_ship(self):
        """Ship the order"""
        self.state = 'shipped'

    def action_deliver(self):
        """Mark order as delivered"""
        self.state = 'delivered'
