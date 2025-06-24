# Contributing Guidelines

## 🎯 Welcome Contributors!

Thank you for your interest in contributing to the UMKM Marketplace project! This guide will help you get started with contributing to our open-source e-commerce platform for Indonesian MSMEs.

## 📋 Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [Contributing Process](#contributing-process)
5. [Coding Standards](#coding-standards)
6. [Testing Guidelines](#testing-guidelines)
7. [Documentation](#documentation)
8. [Review Process](#review-process)

---

## 🤝 Code of Conduct

### Our Pledge
We are committed to making participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Expected Behavior
- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

### Unacceptable Behavior
- The use of sexualized language or imagery
- Personal attacks or insulting/derogatory comments
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Docker & Docker Compose
- Git
- Basic knowledge of Odoo framework
- Understanding of Python, JavaScript, XML

### First Contribution
1. **Find an Issue**: Look for issues labeled `good first issue` or `help wanted`
2. **Fork the Repository**: Create your own fork of the project
3. **Create a Branch**: Make a feature branch from `develop`
4. **Make Changes**: Implement your changes following our guidelines
5. **Submit a PR**: Create a pull request with a clear description

### Types of Contributions
- **Bug Fixes**: Fix existing issues
- **Features**: Add new functionality
- **Documentation**: Improve documentation
- **Testing**: Add or improve tests
- **Translations**: Add or improve language support
- **Performance**: Optimize existing code

---

## 💻 Development Setup

### 1. Fork and Clone
```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/odoo-ecommerce-umkm.git
cd odoo-ecommerce-umkm

# Add upstream remote
git remote add upstream https://github.com/ORIGINAL_OWNER/odoo-ecommerce-umkm.git
```

### 2. Development Environment
```bash
# Copy environment file
cp .env.example .env.dev

# Start development environment
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# Install development dependencies
pip install -r requirements-dev.txt
```

### 3. Database Setup
```bash
# Initialize development database
python3 scripts/init_dev_db.py

# Load test data
python3 scripts/load_test_data.py
```

### 4. Enable Developer Mode
1. Access Odoo at `http://localhost:8069`
2. Go to Settings → Activate Developer Mode
3. Install UMKM Marketplace module

---

## 🔄 Contributing Process

### 1. Create Feature Branch
```bash
# Update your fork
git fetch upstream
git checkout develop
git merge upstream/develop

# Create feature branch
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-number-description
```

### 2. Make Changes
- Follow our coding standards
- Add tests for new functionality
- Update documentation as needed
- Ensure all tests pass

### 3. Commit Changes
```bash
# Stage your changes
git add .

# Commit with descriptive message
git commit -m "feat: add vendor commission calculation

- Implement automatic commission calculation
- Add commission rules configuration
- Update vendor dashboard with commission data
- Add tests for commission calculation logic

Closes #123"
```

### 4. Push and Create PR
```bash
# Push to your fork
git push origin feature/your-feature-name

# Create Pull Request on GitHub
# Include description, issue references, and testing instructions
```

---

## 📝 Coding Standards

### Python Code Style
We follow PEP 8 with some modifications:

```python
# Good: Clear variable names
def calculate_vendor_commission(order_amount, commission_rate):
    """Calculate commission for vendor based on order amount."""
    return order_amount * (commission_rate / 100)

# Good: Proper docstrings
class UmkmVendor(models.Model):
    """UMKM Vendor model for marketplace vendors.
    
    This model handles vendor information, commission rates,
    and business verification status.
    """
    _name = 'umkm.vendor'
    _description = 'UMKM Marketplace Vendor'
```

### JavaScript/XML Standards
```javascript
// Good: Use modern JavaScript
const calculateTotal = (items) => {
    return items.reduce((total, item) => total + item.price, 0);
};

// Good: Consistent XML formatting
<record id="umkm_vendor_form_view" model="ir.ui.view">
    <field name="name">umkm.vendor.form</field>
    <field name="model">umkm.vendor</field>
    <field name="arch" type="xml">
        <form string="Vendor">
            <group>
                <field name="name" required="1"/>
                <field name="email"/>
            </group>
        </form>
    </field>
</record>
```

### Code Quality Tools
```bash
# Install development tools
pip install flake8 black isort pylint

# Format code
black custom_modules/
isort custom_modules/

# Check code quality
flake8 custom_modules/
pylint custom_modules/
```

---

## 🧪 Testing Guidelines

### Test Structure
```
tests/
├── unit/           # Unit tests
├── integration/    # Integration tests
├── functional/     # Functional tests
└── fixtures/       # Test data
```

### Writing Tests
```python
# Example unit test
from odoo.tests import TransactionCase

class TestUmkmCommission(TransactionCase):
    
    def setUp(self):
        super().setUp()
        self.vendor = self.env['umkm.vendor'].create({
            'name': 'Test Vendor',
            'commission_rate': 5.0
        })
    
    def test_commission_calculation(self):
        """Test commission calculation logic."""
        order_amount = 1000000  # 1 million IDR
        expected_commission = 50000  # 5% of 1 million
        
        commission = self.vendor._calculate_commission(order_amount)
        self.assertEqual(commission, expected_commission)
```

### Running Tests
```bash
# Run all tests
docker-compose exec odoo python -m pytest tests/

# Run specific test file
docker-compose exec odoo python -m pytest tests/unit/test_commission.py

# Run with coverage
docker-compose exec odoo python -m pytest --cov=custom_modules tests/
```

---

## � Documentation

### Code Documentation
- Use clear docstrings for all methods and classes
- Include parameter descriptions and return values
- Add usage examples for complex functions

### User Documentation
- Update user guides for new features
- Include screenshots for UI changes
- Provide step-by-step instructions

### API Documentation
- Document all new API endpoints
- Include request/response examples
- Update OpenAPI specifications

---

## 👀 Review Process

### Pull Request Guidelines
1. **Clear Title**: Use descriptive title with prefix (feat:, fix:, docs:, etc.)
2. **Description**: Include what, why, and how
3. **Issue Reference**: Link to related issues
4. **Testing**: Describe how to test the changes
5. **Breaking Changes**: Highlight any breaking changes

### PR Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issues
Closes #123

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Screenshots (if applicable)
![Screenshot](url)

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated
```

---

## 📞 Getting Help

### Communication Channels
- **GitHub Issues**: Bug reports and feature requests
- **Discussions**: General questions and ideas
- **Email**: contact@umkmdigital.id

### Mentorship Program
New contributors can request mentorship from experienced contributors. Contact us to be paired with a mentor.

---

Thank you for contributing to UMKM Marketplace! Together, we can build an amazing e-commerce platform for Indonesian MSMEs. 🚀

```python
def calculate_commission(self, amount: float) -> float:
    """
    Calculate commission untuk amount tertentu.
    
    Args:
        amount (float): Jumlah transaksi
        
    Returns:
        float: Jumlah komisi yang dihitung
    """
    if self.commission_type == 'percentage':
        return amount * (self.commission_rate / 100)
    return self.fixed_commission
```

### JavaScript/TypeScript
- Gunakan ESLint dengan konfigurasi yang ada
- Gunakan Prettier untuk formatting
- Ikuti naming conventions yang konsisten

### Odoo XML Views
- Gunakan indentation yang konsisten (4 spaces)
- Gruppingkan fields yang serupa
- Tambahkan help text untuk fields yang tidak obvious

## 🧪 Testing

### Unit Tests
```bash
# Python tests
pytest mobile_api/tests/ -v

# Odoo tests
python odoo-bin --test-enable --stop-after-init -d test_database
```

### Integration Tests
```bash
# Full system test
python tests/integration_test.py
```

## 📋 Commit Message Convention

Gunakan [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types:
- `feat`: Fitur baru
- `fix`: Bug fix
- `docs`: Update dokumentasi
- `style`: Formatting, missing semi colons, dll
- `refactor`: Code refactoring
- `test`: Menambah atau update tests
- `chore`: Update build tasks, package manager configs, dll

### Contoh:
```
feat(vendor): menambahkan sistem rating vendor

- Tambah model rating di database
- Implementasi API endpoints untuk rating
- Update UI untuk menampilkan rating

Closes #123
```

## 🐛 Melaporkan Bug

Gunakan GitHub Issues dengan template berikut:

### Bug Report Template
```markdown
**Describe the bug**
Deskripsi singkat dan jelas tentang bug.

**To Reproduce**
Steps untuk reproduce bug:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
Apa yang diharapkan terjadi.

**Screenshots**
Jika applicable, tambahkan screenshots.

**Environment:**
 - OS: [e.g. Ubuntu 20.04]
 - Browser: [e.g. Chrome 91]
 - Odoo Version: [e.g. 17.0]
 - Python Version: [e.g. 3.9]

**Additional context**
Tambahan context tentang problem.
```

## 💡 Mengusulkan Fitur

Gunakan GitHub Issues dengan label "enhancement":

### Feature Request Template
```markdown
**Is your feature request related to a problem?**
Deskripsi jelas tentang problem. Ex. I'm always frustrated when [...]

**Describe the solution you'd like**
Deskripsi jelas dan concise tentang yang Anda inginkan.

**Describe alternatives you've considered**
Deskripsi tentang alternative solutions atau features yang sudah dipertimbangkan.

**Additional context**
Tambahan context atau screenshots tentang feature request.
```

## 🏗️ Development Workflow

### 1. Issue Assignment
- Cek GitHub Issues untuk tasks yang available
- Comment di issue untuk assign ke diri sendiri
- Atau buat issue baru untuk fitur yang ingin dikerjakan

### 2. Branch Naming
- `feature/issue-number-feature-name`
- `bugfix/issue-number-bug-description`
- `hotfix/critical-bug-description`
- `docs/documentation-update`

### 3. Code Review Process
- Semua PR harus di-review minimal oleh 1 maintainer
- Address semua feedback sebelum merge
- Pastikan semua tests passing
- Update documentation jika diperlukan

### 4. Deployment
- `main` branch adalah production-ready
- `develop` branch untuk development
- Feature branches di-merge ke `develop` dulu
- Release dari `develop` ke `main`

## 📚 Resources

### Documentation
- [Odoo Development Documentation](https://www.odoo.com/documentation/17.0/developer/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

### Community
- [GitHub Discussions](https://github.com/umkm-digital/odoo-ecommerce-umkm/discussions)
- [Discord Server](https://discord.gg/umkm-digital)
- [Telegram Group](https://t.me/umkmdigitalhub)

## 🙏 Recognition

Kontributor akan diakui dalam:
- README.md contributors section
- Release notes
- Annual contributor report
- Swag dan merchandise untuk top contributors

## ❓ Questions?

Jika ada pertanyaan, jangan ragu untuk:
- Buat issue dengan label "question"
- Join Discord/Telegram untuk realtime chat
- Email ke: contributors@umkmdigital.id

Terima kasih telah berkontribusi untuk memajukan UMKM Indonesia! 🇮🇩✨
