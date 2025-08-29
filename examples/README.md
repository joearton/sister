# Sister API Client - Examples

Direktori ini berisi contoh-contoh script untuk menggunakan Sister API client. Semua script ini **read-only** dan aman untuk dijalankan.

## 📁 Available Examples

### 1. `simple_example.py` - Contoh Dasar
**Level**: Beginner  
**Description**: Contoh sederhana penggunaan API client

```bash
python examples/simple_example.py
```

**Yang dipelajari:**
- Cara inisialisasi API client
- Cara mengambil data referensi dasar
- Cara mengecek status cache
- Struktur response data

### 2. `get_reference_data.py` - Data Referensi
**Level**: Beginner  
**Description**: Mengambil berbagai data referensi

```bash
python examples/get_reference_data.py
```

**Data yang diambil:**
- Data perguruan tinggi
- Data SDM
- Data agama
- Data bidang studi
- Data gelar akademik
- Statistik cache

### 3. `get_sdm_details.py` - Detail SDM
**Level**: Intermediate  
**Description**: Mengambil detail lengkap data SDM

```bash
python examples/get_sdm_details.py
```

**Data yang diambil:**
- Profil SDM
- Data kependudukan
- Data keluarga
- Data alamat
- Data kepegawaian
- Data bidang ilmu

### 4. `get_academic_data.py` - Data Akademik
**Level**: Advanced  
**Description**: Mengambil data akademik SDM

```bash
python examples/get_academic_data.py
```

**Data yang diambil:**
- Data penelitian
- Data publikasi
- Data pengajaran
- Data pengabdian
- Data bimbingan mahasiswa
- Data penghargaan

## 🚀 How to Run

### Prerequisites
1. **Setup environment** (sudah dilakukan):
   ```bash
   cp env.example .env
   # Edit .env dengan credentials Anda
   ```

2. **Activate virtual environment**:
   ```bash
   source venv/bin/activate
   ```

### Running Examples
```bash
# Dari root directory
python examples/simple_example.py

# Atau dari examples directory
cd examples
python simple_example.py
```

## 📊 Expected Output

### Simple Example Output
```
🚀 Sister API Client - Simple Example
==================================================

🔌 Initializing Sister API client...

📋 Example 1: Getting SDM Reference Data
----------------------------------------
✅ Success! Found 150 SDM records
📊 From cache: False
⏰ Accessed: 2024-01-01 10:00:00

📝 First 3 SDM records:
   1. Dr. John Doe - 0001018501
   2. Prof. Jane Smith - 0002018502
   3. Dr. Bob Johnson - 0003018503
```

### Reference Data Output
```
🏫 Sister API Client - Reference Data Examples
============================================================

🔌 Initializing Sister API client...

1️⃣  Getting Perguruan Tinggi Data...
✅ Success! Found 1 perguruan tinggi
📊 Cache: False
⏰ Accessed: 2024-01-01 10:00:00
   1. Universitas Example - 123456
```

## 🔧 Customization

### Using Different SDM IDs
```python
# Edit script untuk menggunakan SDM ID tertentu
sdm_id = "your-specific-sdm-id"

# Contoh di get_sdm_details.py
profile_data = api.get_data_pribadi_profil_bypath(id_sdm=sdm_id)
```

### Adding More Endpoints
```python
# Tambahkan endpoint baru
try:
    new_data = api.get_referensi_bidang_studi()
    if new_data['status']:
        print(f"Found {len(new_data['data'])} bidang studi")
except Exception as e:
    print(f"Error: {e}")
```

## 🛡️ Safety Features

### Read-Only Operations
- ✅ **Semua script read-only** - Tidak ada operasi write/update/delete
- ✅ **Safe untuk production** - Tidak akan mengubah data
- ✅ **Error handling** - Graceful error handling
- ✅ **Cache management** - Otomatis cache untuk performance

### Error Handling
```python
try:
    data = api.get_referensi_sdm()
    if data['status']:
        # Process data
        pass
    else:
        print(f"Failed: {data['message']}")
except Exception as e:
    print(f"Error: {e}")
```

## 📈 Performance Tips

### Cache Management
```bash
# Check cache status
python cache_manager.py --stats

# Clean expired cache
python cache_manager.py --cleanup

# Enable auto cleanup
python cache_manager.py --auto-cleanup
```

### Batch Processing
```python
# Process multiple SDM records
sdm_list = api.get_referensi_sdm()
for sdm in sdm_list['data'][:10]:  # Process first 10
    sdm_id = sdm['id_sdm']
    profile = api.get_data_pribadi_profil_bypath(id_sdm=sdm_id)
    # Process profile data
```

## 🔍 Debugging

### Enable Debug Mode
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# API calls will show detailed logs
api = SisterAPI()
data = api.get_referensi_sdm()
```

### Check Response Structure
```python
data = api.get_referensi_sdm()
print(f"Status: {data['status']}")
print(f"Cache: {data['cache']}")
print(f"Message: {data['message']}")
print(f"Data length: {len(data['data'])}")
```

## 📚 Next Steps

### After Running Examples
1. **Explore more endpoints** - Coba endpoint lain
2. **Customize scripts** - Sesuaikan dengan kebutuhan
3. **Build your own** - Buat script sesuai use case
4. **Production deployment** - Deploy ke production

### Advanced Usage
- **Data analysis** - Analisis data SDM
- **Reporting** - Generate reports
- **Integration** - Integrasi dengan sistem lain
- **Automation** - Otomatisasi proses

## 🆘 Troubleshooting

### Common Issues

#### 1. Import Error
```bash
# Solution: Check virtual environment
source venv/bin/activate
pip install -r requirements.txt
```

#### 2. Environment Variables
```bash
# Solution: Check .env file
cat .env
# Make sure all required variables are set
```

#### 3. API Connection
```bash
# Solution: Check Sister URL
# Make sure SISTER_URL is correct and accessible
```

#### 4. Authentication
```bash
# Solution: Check credentials
# Verify SISTER_USERNAME, SISTER_PASSWORD, SISTER_ID_PENGGUNA
```

## 📝 Notes

- **All examples are safe** - Tidak ada operasi yang mengubah data
- **Cache is enabled** - Data akan di-cache untuk performance
- **Error handling** - Semua script memiliki error handling
- **Documentation** - Setiap script memiliki dokumentasi lengkap

## 🤝 Contributing

Untuk menambah contoh baru:
1. Buat file `.py` baru di direktori `examples/`
2. Pastikan script **read-only**
3. Tambahkan error handling
4. Dokumentasikan dengan baik
5. Test script sebelum commit
