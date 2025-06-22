# Contributing to UMKM Digital Hub

Terima kasih atas minat Anda untuk berkontribusi pada UMKM Digital Hub! 🎉

## 🚀 Cara Berkontribusi

### 1. Fork Repository
- Fork repository ini ke akun GitHub Anda
- Clone repository yang sudah di-fork ke local machine

```bash
git clone https://github.com/[username]/odoo-ecommerce-umkm.git
cd odoo-ecommerce-umkm
```

### 2. Setup Development Environment
Ikuti panduan di [README.md](./README.md) untuk setup environment development.

### 3. Buat Branch Baru
```bash
git checkout -b feature/nama-fitur-baru
# atau
git checkout -b bugfix/nama-bug-yang-diperbaiki
```

### 4. Lakukan Perubahan
- Ikuti coding standards yang ada
- Tambahkan tests untuk fitur baru
- Update dokumentasi jika diperlukan

### 5. Commit dan Push
```bash
git add .
git commit -m "feat: menambahkan fitur X"
git push origin feature/nama-fitur-baru
```

### 6. Buat Pull Request
- Buat pull request dari branch Anda ke branch `main`
- Berikan deskripsi yang jelas tentang perubahan
- Link ke issue yang terkait (jika ada)

## 📝 Coding Standards

### Python Code
- Ikuti [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Gunakan `black` untuk formatting
- Gunakan `flake8` untuk linting
- Tambahkan docstrings untuk functions dan classes

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
