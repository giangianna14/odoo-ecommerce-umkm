# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools, _
from odoo.exceptions import ValidationError


class UmkmCommission(models.Model):
    _name = 'umkm.commission'
    _description = 'UMKM Commission'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'

    name = fields.Char('Reference', required=True, copy=False, readonly=True,
                      default=lambda self: _('New'))
    
    # Vendor Information
    vendor_id = fields.Many2one('umkm.vendor', string='Vendor', required=True)
    vendor_order_id = fields.Many2one('umkm.vendor.order', string='Vendor Order')
    
    # Commission Details
    commission_type = fields.Selection([
        ('sale', 'Sales Commission'),
        ('subscription', 'Subscription Fee'),
        ('listing', 'Listing Fee'),
        ('transaction', 'Transaction Fee'),
        ('penalty', 'Penalty'),
        ('bonus', 'Bonus')
    ], string='Type', required=True, default='sale')
    
    # Amounts
    base_amount = fields.Float('Base Amount', required=True, help='Amount on which commission is calculated')
    commission_rate = fields.Float('Commission Rate (%)', required=True)
    commission_amount = fields.Float('Commission Amount', compute='_compute_commission_amount', store=True)
    
    # Currency
    currency_id = fields.Many2one('res.currency', string='Currency',
                                 default=lambda self: self.env.company.currency_id)
    
    # Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)
    
    # Dates
    date = fields.Date('Commission Date', required=True, default=fields.Date.today)
    due_date = fields.Date('Due Date')
    payment_date = fields.Date('Payment Date')
    
    # Payment Information
    invoice_id = fields.Many2one('account.move', string='Invoice')
    payment_id = fields.Many2one('account.payment', string='Payment')
    
    # Description
    description = fields.Text('Description')
    notes = fields.Text('Notes')
    
    # Computed fields
    is_overdue = fields.Boolean('Is Overdue', compute='_compute_overdue', store=True)
    days_overdue = fields.Integer('Days Overdue', compute='_compute_overdue', store=True)

    @api.depends('base_amount', 'commission_rate')
    def _compute_commission_amount(self):
        for commission in self:
            commission.commission_amount = (commission.base_amount * commission.commission_rate) / 100

    @api.depends('due_date', 'state')
    def _compute_overdue(self):
        today = fields.Date.today()
        for commission in self:
            if commission.due_date and commission.state not in ('paid', 'cancelled'):
                commission.is_overdue = commission.due_date < today
                commission.days_overdue = (today - commission.due_date).days if commission.is_overdue else 0
            else:
                commission.is_overdue = False
                commission.days_overdue = 0

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('umkm.commission') or _('New')
        return super(UmkmCommission, self).create(vals)

    def action_confirm(self):
        """Confirm commission"""
        self.state = 'confirmed'

    def action_pay(self):
        """Mark commission as paid"""
        self.state = 'paid'
        self.payment_date = fields.Date.today()

    def action_cancel(self):
        """Cancel commission"""
        self.state = 'cancelled'

    def action_view_invoice(self):
        """View the invoice related to this commission"""
        if self.invoice_id:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'account.move',
                'res_id': self.invoice_id.id,
                'view_mode': 'form',
                'view_type': 'form',
                'target': 'current'
            }
        return {'type': 'ir.actions.act_window_close'}

    def action_create_invoice(self):
        """Create invoice for commission"""
        if self.invoice_id:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'account.move',
                'res_id': self.invoice_id.id,
                'view_mode': 'form',
                'target': 'current',
            }
        
        # Create invoice (simplified)
        invoice_vals = {
            'partner_id': self.vendor_id.partner_id.id,
            'move_type': 'out_invoice',
            'invoice_date': self.date,
            'invoice_line_ids': [(0, 0, {
                'name': self.description or f'Commission - {self.name}',
                'quantity': 1,
                'price_unit': self.commission_amount,
            })],
        }
        invoice = self.env['account.move'].create(invoice_vals)
        self.invoice_id = invoice.id
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'view_mode': 'form',
            'target': 'current',
        }


class UmkmCommissionRule(models.Model):
    _name = 'umkm.commission.rule'
    _description = 'Commission Rule'
    _order = 'sequence, name'

    name = fields.Char('Rule Name', required=True)
    sequence = fields.Integer('Sequence', default=10)
    active = fields.Boolean('Active', default=True)
    
    # Rule Conditions
    vendor_category_ids = fields.Many2many('umkm.vendor.category', string='Vendor Categories')
    product_category_ids = fields.Many2many('product.category', string='Product Categories')
    min_amount = fields.Float('Minimum Amount')
    max_amount = fields.Float('Maximum Amount')
    
    # Commission Settings
    commission_type = fields.Selection([
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount')
    ], string='Commission Type', required=True, default='percentage')
    
    commission_rate = fields.Float('Commission Rate (%)', help='Percentage rate for commission')
    fixed_amount = fields.Float('Fixed Amount', help='Fixed commission amount')
    
    # Validity
    date_start = fields.Date('Start Date')
    date_end = fields.Date('End Date')
    
    # Description
    description = fields.Text('Description')

    @api.constrains('commission_rate')
    def _check_commission_rate(self):
        for rule in self:
            if rule.commission_type == 'percentage' and (rule.commission_rate < 0 or rule.commission_rate > 100):
                raise ValidationError(_('Commission rate must be between 0 and 100 percent.'))

    @api.constrains('min_amount', 'max_amount')
    def _check_amount_range(self):
        for rule in self:
            if rule.min_amount and rule.max_amount and rule.min_amount > rule.max_amount:
                raise ValidationError(_('Minimum amount cannot be greater than maximum amount.'))

    def get_commission_amount(self, base_amount, vendor=None, product=None):
        """Calculate commission amount based on rule"""
        self.ensure_one()
        
        # Check if rule applies
        if not self._rule_applies(base_amount, vendor, product):
            return 0.0
        
        if self.commission_type == 'percentage':
            return (base_amount * self.commission_rate) / 100
        else:
            return self.fixed_amount

    def _rule_applies(self, amount, vendor=None, product=None):
        """Check if rule applies to given parameters"""
        # Check amount range
        if self.min_amount and amount < self.min_amount:
            return False
        if self.max_amount and amount > self.max_amount:
            return False
        
        # Check vendor categories
        if self.vendor_category_ids and vendor:
            if not any(cat in vendor.category_ids for cat in self.vendor_category_ids):
                return False
        
        # Check product categories
        if self.product_category_ids and product:
            if product.category_id not in self.product_category_ids:
                return False
        
        # Check date validity
        today = fields.Date.today()
        if self.date_start and today < self.date_start:
            return False
        if self.date_end and today > self.date_end:
            return False
        
        return True


class UmkmCommissionReport(models.Model):
    _name = 'umkm.commission.report'
    _description = 'Commission Report'
    _auto = False
    _rec_name = 'vendor_id'

    vendor_id = fields.Many2one('umkm.vendor', string='Vendor')
    vendor_name = fields.Char('Vendor Name')
    commission_type = fields.Selection([
        ('sale', 'Sales Commission'),
        ('subscription', 'Subscription Fee'),
        ('listing', 'Listing Fee'),
        ('transaction', 'Transaction Fee'),
        ('penalty', 'Penalty'),
        ('bonus', 'Bonus')
    ], string='Type')
    
    total_commission = fields.Float('Total Commission')
    paid_commission = fields.Float('Paid Commission')
    pending_commission = fields.Float('Pending Commission')
    commission_count = fields.Integer('Commission Count')
    
    period = fields.Char('Period')
    year = fields.Integer('Year')
    month = fields.Integer('Month')
    date = fields.Date('Date')

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                SELECT
                    row_number() OVER () AS id,
                    c.vendor_id,
                    v.name as vendor_name,
                    c.commission_type,
                    SUM(c.commission_amount) as total_commission,
                    SUM(CASE WHEN c.state = 'paid' THEN c.commission_amount ELSE 0 END) as paid_commission,
                    SUM(CASE WHEN c.state != 'paid' THEN c.commission_amount ELSE 0 END) as pending_commission,
                    COUNT(*) as commission_count,
                    CONCAT(EXTRACT(year FROM c.date), '-', LPAD(EXTRACT(month FROM c.date)::text, 2, '0')) as period,
                    EXTRACT(year FROM c.date) as year,
                    EXTRACT(month FROM c.date) as month,
                    c.date
                FROM umkm_commission c
                LEFT JOIN umkm_vendor v ON v.id = c.vendor_id
                GROUP BY
                    c.vendor_id, v.name, c.commission_type,
                    EXTRACT(year FROM c.date), EXTRACT(month FROM c.date), c.date
            )
        """ % self._table)
