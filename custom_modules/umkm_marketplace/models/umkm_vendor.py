from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, date
import phonenumbers
import logging

_logger = logging.getLogger(__name__)


class UMKMVendor(models.Model):
    """
    Model untuk mengelola vendor UMKM dengan fitur khusus Indonesia
    """
    _name = 'umkm.vendor'
    _description = 'UMKM Vendor Profile'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _order = 'name asc'
    _rec_name = 'name'

    # Basic Information
    name = fields.Char(
        string='Business Name',
        required=True,
        tracking=True,
        help='Nama usaha UMKM'
    )
    
    partner_id = fields.Many2one(
        'res.partner',
        string='Contact',
        required=True,
        ondelete='cascade',
        help='Kontak person untuk UMKM ini'
    )
    
    user_id = fields.Many2one(
        'res.users',
        string='Vendor User',
        help='User account untuk vendor ini'
    )
    
    # Business Details
    business_type = fields.Selection([
        ('mikro', 'Usaha Mikro'),
        ('kecil', 'Usaha Kecil'),
        ('menengah', 'Usaha Menengah'),
        ('startup', 'Startup'),
        ('koperasi', 'Koperasi'),
    ], string='Business Type', required=True, tracking=True)
    
    established_year = fields.Integer(
        string='Established Year',
        help='Tahun berdiri usaha',
        default=lambda self: datetime.now().year
    )
    
    employee_count = fields.Selection([
        ('1-5', '1-5 orang'),
        ('6-20', '6-20 orang'),
        ('21-50', '21-50 orang'),
        ('51-100', '51-100 orang'),
        ('100+', 'Lebih dari 100 orang'),
    ], string='Employee Count')
    
    monthly_revenue = fields.Selection([
        ('under_50m', 'Di bawah Rp 50 juta'),
        ('50m_300m', 'Rp 50 juta - Rp 300 juta'),
        ('300m_2.5b', 'Rp 300 juta - Rp 2.5 miliar'),
        ('2.5b_50b', 'Rp 2.5 miliar - Rp 50 miliar'),
        ('over_50b', 'Di atas Rp 50 miliar'),
    ], string='Monthly Revenue Range')
    
    # Legal Documents
    nib_number = fields.Char(
        string='NIB Number',
        help='Nomor Induk Berusaha (NIB)'
    )
    
    npwp_number = fields.Char(
        string='NPWP Number',
        help='Nomor Pokok Wajib Pajak'
    )
    
    siup_number = fields.Char(
        string='SIUP Number',
        help='Surat Izin Usaha Perdagangan'
    )
    
    # Certifications
    halal_certified = fields.Boolean(
        string='Halal Certified',
        default=False,
        tracking=True
    )
    
    halal_certificate_number = fields.Char(
        string='Halal Certificate Number'
    )
    
    halal_expiry_date = fields.Date(
        string='Halal Certificate Expiry'
    )
    
    sni_certified = fields.Boolean(
        string='SNI Certified',
        default=False,
        help='Standar Nasional Indonesia'
    )
    
    local_product_certified = fields.Boolean(
        string='Local Product Certified',
        default=False,
        help='Produk Dalam Negeri (PDN)'
    )
    
    # Business Capacity
    monthly_capacity = fields.Integer(
        string='Monthly Production Capacity',
        help='Kapasitas produksi per bulan (unit)'
    )
    
    min_order_quantity = fields.Integer(
        string='Minimum Order Quantity',
        default=1,
        help='Minimal pemesanan'
    )
    
    lead_time_days = fields.Integer(
        string='Lead Time (Days)',
        default=3,
        help='Waktu pemrosesan pesanan dalam hari'
    )
    
    # Specialization
    specialization_ids = fields.Many2many(
        'product.category',
        string='Product Specializations',
        help='Kategori produk yang menjadi spesialisasi'
    )
    
    # Location
    province_id = fields.Many2one(
        'res.country.state',
        string='Province',
        domain="[('country_id.code', '=', 'ID')]"
    )
    
    city = fields.Char(string='City/Regency')
    district = fields.Char(string='District')
    village = fields.Char(string='Village')
    postal_code = fields.Char(string='Postal Code')
    
    # Contact Information
    phone = fields.Char(string='Phone Number')
    whatsapp = fields.Char(string='WhatsApp Number')
    email = fields.Char(string='Email')
    website = fields.Char(string='Website')
    
    # Social Media
    instagram = fields.Char(string='Instagram')
    facebook = fields.Char(string='Facebook')
    tiktok = fields.Char(string='TikTok')
    
    # Business Story
    story = fields.Text(
        string='Business Story',
        help='Cerita bisnis dan visi misi UMKM'
    )
    
    description = fields.Text(
        string='Description',
        help='Deskripsi singkat tentang bisnis'
    )
    
    # Status and Performance
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending Verification'),
        ('verified', 'Verified'),
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('blocked', 'Blocked'),
    ], string='Status', default='draft', tracking=True)
    
    created_date = fields.Datetime(
        string='Created Date',
        default=fields.Datetime.now,
        readonly=True
    )
    
    verification_date = fields.Datetime(
        string='Verification Date',
        readonly=True
    )
    
    verified_by = fields.Many2one(
        'res.users',
        string='Verified By',
        readonly=True
    )
    
    # Performance Metrics
    total_sales = fields.Monetary(
        string='Total Sales',
        currency_field='currency_id',
        readonly=True,
        compute='_compute_performance_metrics',
        store=True
    )
    
    total_orders = fields.Integer(
        string='Total Orders',
        readonly=True,
        compute='_compute_performance_metrics',
        store=True
    )
    
    avg_rating = fields.Float(
        string='Average Rating',
        readonly=True,
        compute='_compute_performance_metrics',
        store=True
    )
    
    response_time = fields.Float(
        string='Avg Response Time (hours)',
        readonly=True,
        compute='_compute_performance_metrics',
        store=True
    )
    
    # Commission Settings
    commission_rate = fields.Float(
        string='Commission Rate (%)',
        default=5.0,
        help='Persentase komisi per transaksi'
    )
    
    commission_type = fields.Selection([
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ], string='Commission Type', default='percentage')
    
    fixed_commission = fields.Monetary(
        string='Fixed Commission Amount',
        currency_field='currency_id'
    )
    
    # Relations
    # Note: product_ids and order_ids would need vendor_id fields added to those models
    # or separate intermediary models to be created
    
    certification_ids = fields.One2many(
        'umkm.certification',
        'vendor_id',
        string='Certifications'
    )
    
    # System Fields
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id
    )
    
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company
    )
    
    active = fields.Boolean(default=True)
    
    # Computed Fields
    product_count = fields.Integer(
        string='Product Count',
        compute='_compute_product_count'
    )
    
    order_count = fields.Integer(
        string='Order Count',
        compute='_compute_order_count'
    )
    
    # Constraints
    @api.constrains('phone', 'whatsapp')
    def _check_phone_numbers(self):
        """Validasi format nomor telepon Indonesia"""
        for record in self:
            if record.phone:
                try:
                    parsed = phonenumbers.parse(record.phone, 'ID')
                    if not phonenumbers.is_valid_number(parsed):
                        raise ValidationError(_('Invalid phone number format'))
                except:
                    raise ValidationError(_('Invalid phone number format'))
    
    @api.constrains('commission_rate')
    def _check_commission_rate(self):
        """Validasi rate komisi"""
        for record in self:
            if record.commission_rate < 0 or record.commission_rate > 50:
                raise ValidationError(_('Commission rate must be between 0% and 50%'))
    
    @api.constrains('established_year')
    def _check_established_year(self):
        """Validasi tahun berdiri"""
        current_year = datetime.now().year
        for record in self:
            if record.established_year > current_year:
                raise ValidationError(_('Established year cannot be in the future'))
            if record.established_year < 1945:
                raise ValidationError(_('Established year cannot be before 1945'))
    
    # Compute Methods
    def _compute_product_count(self):
        for record in self:
            # This would need to be implemented when product model is extended
            record.product_count = 0
    
    def _compute_order_count(self):
        for record in self:
            # This would need to be implemented when order model is extended
            record.order_count = 0
    
    def _compute_performance_metrics(self):
        for record in self:
            # Initialize with default values for now
            # These would be computed from actual orders when order system is implemented
            record.total_sales = 0.0
            record.total_orders = 0
            record.avg_rating = 0.0
            record.response_time = 2.5  # Default 2.5 hours
    
    # CRUD Methods
    @api.model
    def create(self, vals):
        """Override create untuk setup awal vendor"""
        # Auto-create partner if not provided
        if not vals.get('partner_id'):
            partner_vals = {
                'name': vals.get('name'),
                'is_company': True,
                'supplier_rank': 1,
                'customer_rank': 0,
                'phone': vals.get('phone'),
                'email': vals.get('email'),
                'website': vals.get('website'),
            }
            partner = self.env['res.partner'].create(partner_vals)
            vals['partner_id'] = partner.id
        
        vendor = super().create(vals)
        
        # Send welcome email
        vendor._send_welcome_email()
        
        return vendor
    
    # Action Methods
    def action_submit_for_verification(self):
        """Submit vendor untuk verifikasi"""
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft vendors can be submitted for verification'))
        
        # Check required fields
        required_fields = ['name', 'business_type', 'phone', 'email']
        missing_fields = []
        for field in required_fields:
            if not getattr(self, field):
                missing_fields.append(self._fields[field].string)
        
        if missing_fields:
            raise UserError(_('Please complete the following fields: %s') % ', '.join(missing_fields))
        
        self.state = 'pending'
        self.message_post(
            body=_('Vendor submitted for verification'),
            message_type='notification'
        )
    
    def action_verify(self):
        """Verify vendor (admin action)"""
        self.ensure_one()
        if self.state != 'pending':
            raise UserError(_('Only pending vendors can be verified'))
        
        self.write({
            'state': 'verified',
            'verification_date': fields.Datetime.now(),
            'verified_by': self.env.user.id,
        })
        
        self.message_post(
            body=_('Vendor verified by %s') % self.env.user.name,
            message_type='notification'
        )
        
        # Send verification email
        self._send_verification_email()
    
    def action_activate(self):
        """Activate vendor"""
        self.ensure_one()
        if self.state not in ['verified', 'suspended']:
            raise UserError(_('Only verified or suspended vendors can be activated'))
        
        self.state = 'active'
        self.message_post(
            body=_('Vendor activated'),
            message_type='notification'
        )
    
    def action_suspend(self):
        """Suspend vendor"""
        self.ensure_one()
        if self.state != 'active':
            raise UserError(_('Only active vendors can be suspended'))
        
        self.state = 'suspended'
        self.message_post(
            body=_('Vendor suspended'),
            message_type='notification'
        )
    
    def action_block(self):
        """Block vendor permanently"""
        self.ensure_one()
        self.state = 'blocked'
        self.active = False
        self.message_post(
            body=_('Vendor blocked permanently'),
            message_type='notification'
        )
    
    def action_approve(self):
        """Approve vendor registration"""
        self.write({
            'state': 'verified',
            'verification_date': fields.Datetime.now(),
            'verified_by': self.env.user.id,
        })
    
    def action_reject(self):
        """Reject vendor registration"""
        self.write({
            'state': 'draft',
        })
    
    # Business Methods
    def calculate_commission(self, amount):
        """Calculate commission untuk amount tertentu"""
        self.ensure_one()
        if self.commission_type == 'percentage':
            return amount * (self.commission_rate / 100)
        else:
            return self.fixed_commission
    
    def get_available_products(self):
        """Get produk yang tersedia untuk dijual"""
        self.ensure_one()
        return self.product_ids.filtered(
            lambda p: p.sale_ok and p.active and p.qty_available > 0
        )
    
    def get_performance_summary(self):
        """Get ringkasan performance vendor"""
        self.ensure_one()
        return {
            'total_sales': self.total_sales,
            'total_orders': self.total_orders,
            'avg_rating': self.avg_rating,
            'response_time': self.response_time,
            'product_count': self.product_count,
            'commission_rate': self.commission_rate,
        }
    
    # Notification Methods
    def _send_welcome_email(self):
        """Send welcome email ke vendor baru"""
        template = self.env.ref('umkm_marketplace.email_template_vendor_welcome', raise_if_not_found=False)
        if template:
            template.send_mail(self.id, force_send=True)
    
    def _send_verification_email(self):
        """Send verification confirmation email"""
        template = self.env.ref('umkm_marketplace.email_template_vendor_verified', raise_if_not_found=False)
        if template:
            template.send_mail(self.id, force_send=True)
    
    # API Methods untuk Mobile App
    @api.model
    def api_search_vendors(self, domain=None, limit=20, offset=0):
        """API untuk search vendors dari mobile app"""
        if not domain:
            domain = [('state', '=', 'active')]
        
        vendors = self.search(domain, limit=limit, offset=offset)
        
        return [{
            'id': v.id,
            'name': v.name,
            'business_type': v.business_type,
            'city': v.city,
            'province': v.province_id.name if v.province_id else '',
            'avg_rating': v.avg_rating,
            'product_count': v.product_count,
            'specializations': [s.name for s in v.specialization_ids],
            'halal_certified': v.halal_certified,
            'response_time': v.response_time,
        } for v in vendors]
    
    def api_get_vendor_detail(self):
        """API untuk get detail vendor"""
        self.ensure_one()
        return {
            'id': self.id,
            'name': self.name,
            'business_type': self.business_type,
            'description': self.description,
            'story': self.story,
            'established_year': self.established_year,
            'employee_count': self.employee_count,
            'location': {
                'city': self.city,
                'province': self.province_id.name if self.province_id else '',
                'district': self.district,
            },
            'contact': {
                'phone': self.phone,
                'whatsapp': self.whatsapp,
                'email': self.email,
                'website': self.website,
            },
            'social_media': {
                'instagram': self.instagram,
                'facebook': self.facebook,
                'tiktok': self.tiktok,
            },
            'certifications': {
                'halal_certified': self.halal_certified,
                'sni_certified': self.sni_certified,
                'local_product_certified': self.local_product_certified,
            },
            'performance': self.get_performance_summary(),
            'specializations': [s.name for s in self.specialization_ids],
        }
