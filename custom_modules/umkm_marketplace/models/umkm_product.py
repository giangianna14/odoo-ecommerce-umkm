# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class UmkmProduct(models.Model):
    _name = 'umkm.product'
    _description = 'UMKM Product'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char('Product Name', required=True, tracking=True)
    description = fields.Html('Description')
    vendor_id = fields.Many2one('umkm.vendor', string='Vendor', required=True)
    category_id = fields.Many2one('product.category', string='Category')
    price = fields.Float('Price', required=True, tracking=True)
    cost_price = fields.Float('Cost Price')
    currency_id = fields.Many2one('res.currency', string='Currency', 
                                 default=lambda self: self.env.company.currency_id)
    
    # Stock Information
    qty_available = fields.Float('Quantity on Hand', default=0)
    virtual_available = fields.Float('Forecast Quantity', default=0)
    
    # Product Specifications
    weight = fields.Float('Weight (kg)')
    length = fields.Float('Length (cm)')
    width = fields.Float('Width (cm)')
    height = fields.Float('Height (cm)')
    
    # Images
    image_1920 = fields.Image('Main Image', max_width=1920, max_height=1920)
    image_1024 = fields.Image('Image 1024', related='image_1920', max_width=1024, max_height=1024, store=True)
    image_512 = fields.Image('Image 512', related='image_1920', max_width=512, max_height=512, store=True)
    image_256 = fields.Image('Image 256', related='image_1920', max_width=256, max_height=256, store=True)
    image_128 = fields.Image('Image 128', related='image_1920', max_width=128, max_height=128, store=True)
    
    # Additional Images
    product_image_ids = fields.One2many('umkm.product.image', 'product_id', string='Additional Images')
    
    # Status and Visibility
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('published', 'Published'),
        ('archived', 'Archived')
    ], default='draft', string='Status', tracking=True)
    
    active = fields.Boolean('Active', default=True)
    website_published = fields.Boolean('Published on Website', default=False)
    
    # Certifications
    certification_ids = fields.Many2many('umkm.certification', string='Certifications')
    is_halal_certified = fields.Boolean('Halal Certified', compute='_compute_certifications', store=True)
    is_sni_certified = fields.Boolean('SNI Certified', compute='_compute_certifications', store=True)
    
    # Tags and Keywords
    tag_ids = fields.Many2many('umkm.product.tag', string='Tags')
    keywords = fields.Text('Keywords')
    
    # SEO
    website_meta_title = fields.Char('Website Meta Title')
    website_meta_description = fields.Text('Website Meta Description')
    website_meta_keywords = fields.Char('Website Meta Keywords')
    
    # Sales Data
    sale_count = fields.Integer('Sales Count', compute='_compute_sale_count')
    revenue_total = fields.Float('Total Revenue', compute='_compute_revenue_total')
    
    # Dates
    created_date = fields.Datetime('Created Date', default=fields.Datetime.now)
    published_date = fields.Datetime('Published Date')
    last_modified_date = fields.Datetime('Last Modified', default=fields.Datetime.now)

    @api.depends('certification_ids')
    def _compute_certifications(self):
        for product in self:
            halal_cert = product.certification_ids.filtered(lambda c: c.certification_type == 'halal')
            sni_cert = product.certification_ids.filtered(lambda c: c.certification_type == 'sni')
            product.is_halal_certified = bool(halal_cert)
            product.is_sni_certified = bool(sni_cert)

    def _compute_sale_count(self):
        for product in self:
            # Compute from sale order lines or similar
            product.sale_count = 0  # Placeholder

    def _compute_revenue_total(self):
        for product in self:
            # Compute total revenue from sales
            product.revenue_total = 0.0  # Placeholder

    @api.constrains('price')
    def _check_price(self):
        for product in self:
            if product.price < 0:
                raise ValidationError(_('Product price cannot be negative.'))

    def action_submit_for_approval(self):
        """Submit product for approval"""
        self.state = 'pending'

    def action_approve(self):
        """Approve product"""
        self.state = 'approved'

    def action_reject(self):
        """Reject product"""
        self.state = 'rejected'

    def action_publish(self):
        """Publish product to website"""
        self.state = 'published'
        self.website_published = True
        self.published_date = fields.Datetime.now()

    def action_archive(self):
        """Archive product"""
        self.state = 'archived'
        self.website_published = False

    def action_view_sales(self):
        """View sales orders related to this product"""
        action = self.env.ref('umkm_marketplace.action_umkm_order').read()[0]
        action['domain'] = [('order_line.product_id', '=', self.id)]
        action['context'] = {'default_product_id': self.id}
        return action


class UmkmProductImage(models.Model):
    _name = 'umkm.product.image'
    _description = 'Product Additional Images'
    _order = 'sequence, id'

    name = fields.Char('Name', required=True)
    sequence = fields.Integer('Sequence', default=1)
    product_id = fields.Many2one('umkm.product', string='Product', required=True, ondelete='cascade')
    image_1920 = fields.Image('Image', max_width=1920, max_height=1920, required=True)
    image_1024 = fields.Image('Image 1024', related='image_1920', max_width=1024, max_height=1024, store=True)
    image_512 = fields.Image('Image 512', related='image_1920', max_width=512, max_height=512, store=True)
    image_256 = fields.Image('Image 256', related='image_1920', max_width=256, max_height=256, store=True)
    image_128 = fields.Image('Image 128', related='image_1920', max_width=128, max_height=128, store=True)


class UmkmProductTag(models.Model):
    _name = 'umkm.product.tag'
    _description = 'Product Tags'
    _order = 'name'

    name = fields.Char('Tag Name', required=True)
    color = fields.Integer('Color')
    active = fields.Boolean('Active', default=True)
    product_count = fields.Integer('Product Count', compute='_compute_product_count')

    def _compute_product_count(self):
        for tag in self:
            tag.product_count = self.env['umkm.product'].search_count([('tag_ids', 'in', tag.id)])
