# Sister
Simple Sister API client (Dikti/Kemdikbudristek) using Python.

## 🚀 Quick Setup

### Option 1: Automated Setup
```bash
# Clone the repository
git clone <repository-url>
cd sister

# Run automated setup script
./setup_venv.sh
```

### Option 2: Manual Setup
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp env.example .env
# Edit .env with your Sister credentials
```

## Sister Credential Preparation
1. Get your developer credential from **akses.ristekdikti.go.id**.
2. In there, create new user with role "Developer".
3. Open your sister, and syncronize to get new "developer user".
4. Login to your sister using developer credential.
5. Copy username, password, and id_pengguna, and put it on `.env` file.

## Environment Configuration
1. Copy `env.example` to `.env`
2. Set your Sister URL with schema, example: `https://sister.umko.ac.id`
3. Set credential username, password, and id_pengguna of your account

### Required Environment Variables
```bash
# .env
SISTER_URL=https://sister.umko.ac.id
SISTER_USERNAME=your_developer_username
SISTER_PASSWORD=your_developer_password
SISTER_ID_PENGGUNA=your_developer_id_pengguna
```

For detailed environment configuration, see [ENV_SETUP.md](ENV_SETUP.md).

## Official API Guide
https://sister.kemdikbud.go.id

## How to Use
### Basic Use
```
from sister import SisterAPI 

# get SDM data of university
api = SisterAPI()
res = api.get_data('/referensi/sdm')
print(res)
```

## What You Have to Know
This code use automatic function fetched from Sister api spec. So, you can easily call path using below code:
```
# path /referensi/perguruan_tinggi
# remember that / in path is _ in function
res = api.get_referensi_perguruan_tinggi()
print(res)

# path /referensi/sdm
res = api.get_referensi_sdm()
print(res)

# path /dokumen
res = api.get_dokumen(id_sdm='get user id in UUID format')
print(res)
```

## 📚 Examples

Contoh penggunaan Sister API client dapat ditemukan di direktori `examples/`:

### Script Dasar
- `simple_example.py` - Contoh dasar penggunaan API dengan data referensi yang berfungsi
- `get_working_endpoints.py` - Contoh komprehensif endpoint yang berfungsi

### Script Spesifik
- `get_reference_data.py` - Contoh mengambil data referensi
- `get_sdm_details.py` - Contoh mengambil detail data SDM
- `get_academic_data.py` - Contoh mengambil data akademik
- `get_sdm_by_nidn.py` - Contoh mengambil data SDM berdasarkan NIDN (dapat dimasukkan via command line)

### Cara Menjalankan Contoh

```bash
# Contoh sederhana
python examples/simple_example.py

# Contoh komprehensif
python examples/get_working_endpoints.py

# Contoh spesifik
python examples/get_reference_data.py
python examples/get_sdm_details.py
python examples/get_academic_data.py
python examples/get_sdm_by_nidn.py 0227118803
```

### Endpoint yang Berfungsi

Berdasarkan testing, endpoint berikut berfungsi dengan baik:

### 📋 Contoh Penggunaan NIDN

Script `get_sdm_by_nidn.py` memungkinkan Anda mengambil data SDM berdasarkan NIDN spesifik:

```bash
# Menggunakan NIDN yang valid
python examples/get_sdm_by_nidn.py 0227118803

# Mencari NIDN lain
python examples/get_sdm_by_nidn.py 0012345678

# Melihat bantuan
python examples/get_sdm_by_nidn.py --help
```

**Fitur:**
- ✅ Validasi format NIDN (10 digit angka)
- ✅ Pencarian otomatis dengan fallback
- ✅ Menampilkan data komprehensif SDM
- ✅ Error handling yang informatif
- ✅ Semua operasi read-only (aman)

**Data Referensi:**
- ✅ `get_referensi_sdm()` - Data SDM
- ✅ `get_referensi_agama()` - Data agama
- ✅ `get_referensi_gelar_akademik()` - Data gelar akademik
- ✅ `get_referensi_jabatan_fungsional()` - Data jabatan fungsional
- ✅ `get_referensi_jenis_publikasi()` - Data jenis publikasi
- ✅ `get_referensi_jenis_dokumen()` - Data jenis dokumen
- ✅ `get_referensi_jenis_tunjangan()` - Data jenis tunjangan
- ✅ `get_referensi_jenis_penghargaan()` - Data jenis penghargaan
- ✅ `get_referensi_jenis_kepanitiaan()` - Data jenis kepanitiaan
- ✅ `get_referensi_jabatan_negara()` - Data jabatan negara
- ✅ `get_referensi_ikatan_kerja()` - Data ikatan kerja
- ✅ `get_referensi_status_kepegawaian()` - Data status kepegawaian
- ✅ `get_referensi_sumber_gaji()` - Data sumber gaji
- ✅ `get_referensi_jenjang_pendidikan()` - Data jenjang pendidikan
- ✅ `get_referensi_tingkat_penghargaan()` - Data tingkat penghargaan

**Data SDM:**
- ✅ `get_data_pribadi_profil()` - Profil SDM
- ✅ `get_data_pribadi_kependudukan()` - Data kependudukan
- ✅ `get_data_pribadi_bidang_ilmu()` - Bidang ilmu

**Data Akademik:**
- ✅ `get_penelitian()` - Data penelitian
- ✅ `get_publikasi()` - Data publikasi
- ✅ `get_bahan_ajar()` - Data bahan ajar
- ✅ `get_pendidikan_formal()` - Data pendidikan formal
- ✅ `get_diklat()` - Data diklat

### Want to See Available Paths?

```
paths = api.spec.get_paths()
for path in paths:
    print(path)

# output
/authorize
/referensi/kategori_capaian_luaran
/referensi/perguruan_tinggi
/referensi/unit_kerja
/referensi/mahasiswa_pddikti
/referensi/agama
/referensi/bidang_studi
/referensi/bidang_usaha
/referensi/gelar_akademik
/referensi/golongan_pangkat
/referensi/ikatan_kerja
/referensi/jenis_dokumen
/referensi/jabatan_fungsional
/referensi/jabatan_negara
/referensi/jabatan_tugas_tambahan
/referensi/jenis_penghargaan
/referensi/jenis_kepanitiaan
/referensi/jenis_kesejahteraan
/referensi/jenis_beasiswa
/referensi/jenis_diklat
/referensi/jenis_keluar
/referensi/jenis_pekerjaan
/referensi/jenis_publikasi
/referensi/jenis_tes
/referensi/jenis_tunjangan
/referensi/profil_pt
/referensi/status_kepegawaian
/referensi/tingkat_penghargaan
/referensi/media_publikasi
/referensi/negara
/referensi/kategori_kegiatan
/referensi/kelompok_bidang
/referensi/wilayah
/referensi/sdm
/referensi/semester
/referensi/sumber_gaji
/data_pribadi/foto/{id_sdm}
/data_pribadi/profil/{id_sdm}
/data_pribadi/kependudukan/{id_sdm}
/data_pribadi/keluarga/{id_sdm}
/data_pribadi/alamat/{id_sdm}
/data_pribadi/kepegawaian/{id_sdm}
/data_pribadi/lain/{id_sdm}
/data_pribadi/bidang_ilmu/{id_sdm}
/data_pribadi/ajuan
/data_pribadi/ajuan/{id}
/inpassing
/inpassing/{id}
/jabatan_fungsional
/jabatan_fungsional/{id}
/jabatan_fungsional/ajuan
/jabatan_fungsional/ajuan/{id}
/kepangkatan
/kepangkatan/{id}
/kepangkatan/ajuan
/kepangkatan/ajuan/{id}
/penugasan
/penugasan/{id}
/pengajaran
/pengajaran/{id}
/pengajaran/{id}/bidang_ilmu
/bimbingan_mahasiswa
/bimbingan_mahasiswa/{id}
/bimbingan_mahasiswa/{id}/bidang_ilmu
/pengujian_mahasiswa
/pengujian_mahasiswa/{id}
/pengujian_mahasiswa/{id}/bidang_ilmu
/anggota_profesi
/anggota_profesi/{id}
/detasering
/detasering/{id}
/orasi_ilmiah
/orasi_ilmiah/{id}
/bahan_ajar
/bahan_ajar/{id}
/bimbing_dosen
/bimbing_dosen/{id}
/tugas_tambahan
/tugas_tambahan/{id}
/penelitian
/penelitian/{id}
/penelitian/{id}/bidang_ilmu
/publikasi
/publikasi/{id}
/publikasi/{id}/bidang_ilmu
/pengabdian
/pengabdian/{id}
/pengabdian/{id}/bidang_ilmu
/pembicara
/pembicara/{id}
/jabatan_struktural
/jabatan_struktural/{id}
/pengelola_jurnal
/pengelola_jurnal/{id}
/penghargaan
/penghargaan/{id}
/visiting_scientist
/visiting_scientist/{id}
/penunjang_lain
/penunjang_lain/{id}
/kekayaan_intelektual
/kekayaan_intelektual/{id}
/kekayaan_intelektual/{id}/bidang_ilmu
/pendidikan_formal
/pendidikan_formal/{id}
/pendidikan_formal/ajuan
/pendidikan_formal/ajuan/{id}
/diklat
/diklat/{id}
/riwayat_pekerjaan
/riwayat_pekerjaan/{id}
/sertifikasi_profesi
/sertifikasi_profesi/{id}
/sertifikasi_dosen
/sertifikasi_dosen/{id}
/sertifikasi_dosen/ajuan
/sertifikasi_dosen/ajuan/{id}
/nilai_tes
/nilai_tes/{id}
/nilai_tes/ajuan
/nilai_tes/ajuan/{id}
/beasiswa
/beasiswa/{id}
/kesejahteraan
/kesejahteraan/{id}
/tunjangan
/tunjangan/{id}
/dokumen
/dokumen/{id}
/dokumen/{id}/download
/kolaborator_eksternal
/kolaborator_eksternal/{id}
```

## 🧹 Cache Management

Sister API client includes a comprehensive cache management system with automatic cleanup capabilities.

### Quick Cache Commands
```bash
# View cache statistics
python cache_manager.py --stats

# Clean up expired cache
python cache_manager.py --cleanup

# Clear all cache
python cache_manager.py --clear

# Enable automatic cleanup
python cache_manager.py --auto-cleanup
```

### Using Cache Management in Python
```python
from sister import SisterAPI

api = SisterAPI()

# Get cache statistics
stats = api.get_cache_stats()
print(f"Cache entries: {stats['total_cache_entries']}")

# Clean up expired cache
result = api.cleanup_expired_cache()
print(f"Removed {result['expired_count']} expired entries")

# Enable automatic cleanup
api.enable_auto_cleanup(True)
```

For detailed cache management documentation, see [CACHE_MANAGEMENT.md](CACHE_MANAGEMENT.md).

## 🐛 Bug Fixes & Improvements

This version includes comprehensive bug fixes and improvements. See [BUGFIXES.md](BUGFIXES.md) for detailed information.

### Key Improvements:
- ✅ **Fixed infinite recursion bug** in token refresh
- ✅ **Fixed authentication header issues**
- ✅ **Added proper error handling** and input validation
- ✅ **Improved thread safety** for cache operations
- ✅ **Enhanced security** with specific exception handling
- ✅ **Better code quality** and maintainability
- ✅ **Added cache cleanup features** for better disk management
- ✅ **Environment-based configuration** using .env files

### Testing
Run the test suite to verify all fixes:
```bash
python test_fixes.py
```

## 📁 Project Structure
```
sister/
├── api.py                 # Main API client
├── sister.py              # Entry point
├── settings.py            # Configuration settings
├── requirements.txt       # Python dependencies
├── setup_venv.sh         # Automated setup script
├── cache_manager.py      # Cache management utility
├── test_fixes.py         # Test suite for bug fixes
├── test_cache_cleanup.py # Test suite for cache features
├── env.example           # Environment variables template
├── .env                  # Your environment variables (create this)
├── BUGFIXES.md           # Detailed bug fix documentation
├── CACHE_MANAGEMENT.md   # Cache management guide
├── ENV_SETUP.md          # Environment configuration guide
├── examples/             # Example scripts
│   ├── simple_example.py # Basic API usage example
│   ├── get_working_endpoints.py # Comprehensive working endpoints
│   ├── get_reference_data.py # Reference data examples
│   ├── get_sdm_details.py # SDM data examples
│   ├── get_academic_data.py # Academic data examples
│   └── get_sdm_by_nidn.py # SDM data by NIDN example
├── config/
│   └── api_spec.yaml     # OpenAPI specification
└── library/
    ├── api_spec.py       # API specification parser
    ├── cache.py          # Caching system with cleanup
    ├── connector.py      # HTTP session management
    ├── io.py             # Input/output operations
    ├── template.py       # Response templates
    └── webservice.py     # Core web service logic
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite: `python test_fixes.py`
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.