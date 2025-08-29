# Sister API Client - Cache Management Guide

## Overview
Sister API client includes a comprehensive cache management system with automatic cleanup capabilities to maintain optimal performance and disk space usage.

## 🗂️ Cache Structure

### Storage Architecture
```
.cache/
├── cache_db.json          # Cache metadata database
├── ABC123DEF456.json      # Individual cache files (UUID-based)
├── GHI789JKL012.json
└── ...
```

### Cache Database Schema
```json
{
  "referensi-sdm": {
    "id": "referensi-sdm",
    "path": "/referensi/sdm",
    "filename": "ABC123DEF456.json",
    "filepath": ".cache/ABC123DEF456.json",
    "accessed_at": "2024-01-01T10:00:00.000000",
    "expired_at": "2024-01-02T10:00:00.000000",
    "length": 1500
  }
}
```

## 🧹 Cache Cleanup Features

### 1. Automatic Cache Cleanup
Cache yang expired akan otomatis dihapus saat melakukan API call (jika diaktifkan).

#### Enable/Disable Auto Cleanup
```python
from sister import SisterAPI

api = SisterAPI()

# Enable automatic cleanup
api.enable_auto_cleanup(True)

# Disable automatic cleanup
api.enable_auto_cleanup(False)
```

### 2. Manual Cache Cleanup
Hapus cache yang expired secara manual.

#### Using Python API
```python
from sister import SisterAPI

api = SisterAPI()

# Clean up expired cache
result = api.cleanup_expired_cache()
print(f"Removed {result['expired_count']} expired entries")
print(f"Remaining cache: {result['remaining_cache']} entries")
```

#### Using Command Line
```bash
# Clean up expired cache
python cache_manager.py --cleanup
```

### 3. Cache Statistics
Lihat statistik cache untuk monitoring.

#### Using Python API
```python
from sister import SisterAPI

api = SisterAPI()

# Get cache statistics
stats = api.get_cache_stats()
print(f"Total entries: {stats['total_cache_entries']}")
print(f"Total size: {stats['total_size_mb']} MB")
```

#### Using Command Line
```bash
# Show cache statistics
python cache_manager.py --stats
```

### 4. Clear All Cache
Hapus semua cache entries.

#### Using Python API
```python
from sister import SisterAPI

api = SisterAPI()

# Clear all cache
result = api.clear_all_cache()
print(f"Removed {result['removed_files']} files")
```

#### Using Command Line
```bash
# Clear all cache (with confirmation)
python cache_manager.py --clear
```

### 5. Delete Specific Cache
Hapus cache untuk path tertentu.

#### Using Python API
```python
from sister import SisterAPI

api = SisterAPI()

# Delete cache for specific path
success = api.delete_cache_by_path("/referensi/sdm")
if success:
    print("Cache deleted successfully")
```

#### Using Command Line
```bash
# Delete cache for specific path
python cache_manager.py --delete "/referensi/sdm"
```

## 🛠️ Cache Management Utility

### Command Line Interface
```bash
python cache_manager.py [OPTIONS]

Options:
  --stats                    Show cache statistics
  --cleanup                 Remove expired cache entries
  --clear                   Clear all cache entries
  --delete PATH             Delete cache for specific path
  --auto-cleanup            Enable automatic cache cleanup
  --disable-auto-cleanup    Disable automatic cache cleanup
  -h, --help                Show help message
```

### Examples
```bash
# View cache statistics
python cache_manager.py --stats

# Clean up expired cache
python cache_manager.py --cleanup

# Clear all cache (with confirmation)
python cache_manager.py --clear

# Delete specific cache
python cache_manager.py --delete "/referensi/sdm"

# Enable auto cleanup
python cache_manager.py --auto-cleanup

# Disable auto cleanup
python cache_manager.py --disable-auto-cleanup
```

## ⚙️ Configuration

### Default Settings
```python
# Cache expiration (default: 1 day)
cache_expired_datetime = {"days": 1}

# Cache directory
CACHE_DIR = ".cache"

# Auto cleanup (default: disabled)
auto_cleanup_cache = False
```

### Custom Configuration
```python
from sister import SisterAPI

api = SisterAPI()

# Set custom cache expiration
api.cache_expired_datetime = {"hours": 6}  # 6 hours

# Enable auto cleanup
api.enable_auto_cleanup(True)

# Disable caching entirely
api.use_cache(False)
```

## 🔄 Cache Lifecycle

### 1. Cache Creation
```python
# API call creates cache automatically
response = api.get_referensi_sdm()
# Cache saved to .cache/ABC123.json
# Metadata saved to .cache/cache_db.json
```

### 2. Cache Retrieval
```python
# Subsequent calls check cache first
response = api.get_referensi_sdm()
# If cache exists and not expired → return cached data
# If cache expired → fetch fresh data and update cache
```

### 3. Cache Expiration
```python
# Cache expires after configured time
# Default: 1 day from creation
# Configurable: hours, days, weeks, etc.
```

### 4. Cache Cleanup
```python
# Automatic cleanup (if enabled)
# Manual cleanup via API or CLI
# Corrupted cache auto-removed
```

## 🚀 Performance Benefits

### Cache Hit Benefits
- **Instant Response**: Data langsung dari disk
- **Reduced API Calls**: Tidak perlu hit Sister API
- **Bandwidth Saving**: Mengurangi network traffic
- **Rate Limit Protection**: Mengurangi beban ke API

### Example Performance
```python
# First call (cache miss)
start_time = time.time()
response = api.get_referensi_sdm()  # API call
print(f"Time: {time.time() - start_time:.2f}s")

# Second call (cache hit)
start_time = time.time()
response = api.get_referensi_sdm()  # Cache hit
print(f"Time: {time.time() - start_time:.2f}s")  # Much faster!
```

## 🛡️ Thread Safety

### File Locking
- **Shared Lock**: Multiple processes can read simultaneously
- **Exclusive Lock**: Write operations are exclusive
- **Automatic Release**: Locks released with `finally` blocks

### Concurrent Access
```python
# Safe for multi-threaded applications
import threading

def worker():
    api = SisterAPI()
    response = api.get_referensi_sdm()

# Multiple threads can safely access cache
threads = [threading.Thread(target=worker) for _ in range(5)]
for t in threads:
    t.start()
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Cache Corruption
```bash
# Symptoms: JSON decode errors
# Solution: Automatic cleanup removes corrupted entries
python cache_manager.py --cleanup
```

#### 2. Disk Space Issues
```bash
# Check cache size
python cache_manager.py --stats

# Clear cache if needed
python cache_manager.py --clear
```

#### 3. Cache Not Working
```python
# Check if caching is enabled
api = SisterAPI()
print(f"Caching enabled: {api.caching_system}")

# Enable caching if disabled
api.use_cache(True)
```

### Debug Information
```python
# Enable debug mode for cache operations
import logging
logging.basicConfig(level=logging.DEBUG)

# Cache operations will show detailed logs
api = SisterAPI()
response = api.get_referensi_sdm()
```

## 📊 Monitoring

### Cache Metrics
```python
# Get detailed cache information
stats = api.get_cache_stats()
print(f"Cache entries: {stats['total_cache_entries']}")
print(f"Total size: {stats['total_size_mb']} MB")
print(f"Average size per entry: {stats['total_size_bytes'] / max(stats['total_cache_entries'], 1)} bytes")
```

### Response Metadata
```python
response = api.get_referensi_sdm()
print(f"From cache: {response['cache']}")
print(f"Accessed at: {response['accessed_at']}")
print(f"Expires at: {response['expired_at']}")
```

## 🎯 Best Practices

### 1. Regular Cleanup
```bash
# Schedule regular cleanup (e.g., daily cron job)
0 2 * * * cd /path/to/sister && python cache_manager.py --cleanup
```

### 2. Monitor Cache Size
```bash
# Check cache size regularly
python cache_manager.py --stats
```

### 3. Selective Caching
```python
# Disable cache for frequently changing data
api.use_cache(False)
response = api.get_dokumen(id_sdm='uuid')

# Re-enable for static data
api.use_cache(True)
response = api.get_referensi_sdm()
```

### 4. Custom Expiration
```python
# Set shorter expiration for dynamic data
api.cache_expired_datetime = {"hours": 1}  # 1 hour
response = api.get_data('/dynamic/endpoint')

# Set longer expiration for static data
api.cache_expired_datetime = {"days": 7}   # 1 week
response = api.get_data('/static/endpoint')
```

## 📝 Summary

Sister API client cache management system provides:

- ✅ **Automatic cleanup** of expired cache
- ✅ **Manual management** via API and CLI
- ✅ **Thread-safe operations** with file locking
- ✅ **Performance optimization** with cache hits
- ✅ **Disk space management** with cleanup tools
- ✅ **Monitoring capabilities** with statistics
- ✅ **Flexible configuration** for different use cases

The cache system significantly improves performance while maintaining data freshness and managing disk space efficiently.
