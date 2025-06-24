from odoo import api, fields, models, _


class UMKMCertification(models.Model):
    """
    Model untuk mengelola sertifikasi vendor UMKM
    """
    _name = 'umkm.certification'
    _description = 'UMKM Vendor Certification'
    _order = 'name asc'
    
    name = fields.Char(
        string='Certification Name',
        required=True
    )
    
    vendor_id = fields.Many2one(
        'umkm.vendor',
        string='Vendor',
        required=True,
        ondelete='cascade'
    )
    
    certification_type = fields.Selection([
        ('halal', 'Halal'),
        ('sni', 'SNI'),
        ('iso', 'ISO'),
        ('haccp', 'HACCP'),
        ('organic', 'Organic'),
        ('fair_trade', 'Fair Trade'),
        ('other', 'Other'),
    ], string='Type', required=True)
    
    certificate_number = fields.Char(
        string='Certificate Number'
    )
    
    issuing_authority = fields.Char(
        string='Issuing Authority'
    )
    
    issue_date = fields.Date(
        string='Issue Date'
    )
    
    expiry_date = fields.Date(
        string='Expiry Date'
    )
    
    description = fields.Text(
        string='Description'
    )
    
    active = fields.Boolean(
        string='Active',
        default=True
    )
