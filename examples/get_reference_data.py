#!/usr/bin/env python3
"""
Sister API Client - Reference Data Examples
Contoh script untuk mengambil data referensi (read-only operations)

Data yang diambil:
- Data perguruan tinggi
- Data SDM
- Data referensi lainnya
"""

import sys
import os
import json
from datetime import datetime

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def main():
    print("🏫 Sister API Client - Reference Data Examples")
    print("=" * 60)
    
    try:
        from sister import SisterAPI
        
        # Initialize API client
        print("🔌 Initializing Sister API client...")
        api = SisterAPI
        
        # Test 1: Get Perguruan Tinggi Data
        print("\n1️⃣  Getting Perguruan Tinggi Data...")
        try:
            pt_data = api.get_referensi_perguruan_tinggi()
            if pt_data['status']:
                print(f"✅ Success! Found {len(pt_data['data'])} perguruan tinggi")
                print(f"📊 Cache: {pt_data['cache']}")
                print(f"⏰ Accessed: {pt_data['accessed_at']}")
                
                # Show first 3 entries
                for i, pt in enumerate(pt_data['data'][:3]):
                    print(f"   {i+1}. {pt.get('nama_perguruan_tinggi', 'N/A')} - {pt.get('kode_perguruan_tinggi', 'N/A')}")
                
                if len(pt_data['data']) > 3:
                    print(f"   ... and {len(pt_data['data']) - 3} more")
            else:
                print(f"❌ Failed: {pt_data['message']}")
        except Exception as e:
            print(f"❌ Error getting PT data: {e}")
        
        # Test 2: Get SDM Data
        print("\n2️⃣  Getting SDM Data...")
        try:
            sdm_data = api.get_referensi_sdm()
            if sdm_data['status']:
                print(f"✅ Success! Found {len(sdm_data['data'])} SDM records")
                print(f"📊 Cache: {sdm_data['cache']}")
                print(f"⏰ Accessed: {sdm_data['accessed_at']}")
                
                # Show first 3 entries
                for i, sdm in enumerate(sdm_data['data'][:3]):
                    print(f"   {i+1}. {sdm.get('nama', 'N/A')} - {sdm.get('nidn', 'N/A')}")
                
                if len(sdm_data['data']) > 3:
                    print(f"   ... and {len(sdm_data['data']) - 3} more")
            else:
                print(f"❌ Failed: {sdm_data['message']}")
        except Exception as e:
            print(f"❌ Error getting SDM data: {e}")
        
        # Test 3: Get Agama Data
        print("\n3️⃣  Getting Agama Data...")
        try:
            agama_data = api.get_referensi_agama()
            if agama_data['status']:
                print(f"✅ Success! Found {len(agama_data['data'])} agama records")
                print(f"📊 Cache: {agama_data['cache']}")
                
                # Show all agama data
                for agama in agama_data['data']:
                    print(f"   - {agama.get('nama_agama', 'N/A')} (ID: {agama.get('id_agama', 'N/A')})")
            else:
                print(f"❌ Failed: {agama_data['message']}")
        except Exception as e:
            print(f"❌ Error getting agama data: {e}")
        
        # Test 4: Get Bidang Studi Data
        print("\n4️⃣  Getting Bidang Studi Data...")
        try:
            bidang_data = api.get_referensi_bidang_studi()
            if bidang_data['status']:
                print(f"✅ Success! Found {len(bidang_data['data'])} bidang studi records")
                print(f"📊 Cache: {bidang_data['cache']}")
                
                # Show first 5 entries
                for i, bidang in enumerate(bidang_data['data'][:5]):
                    print(f"   {i+1}. {bidang.get('nama_bidang_studi', 'N/A')}")
                
                if len(bidang_data['data']) > 5:
                    print(f"   ... and {len(bidang_data['data']) - 5} more")
            else:
                print(f"❌ Failed: {bidang_data['message']}")
        except Exception as e:
            print(f"❌ Error getting bidang studi data: {e}")
        
        # Test 5: Get Gelar Akademik Data
        print("\n5️⃣  Getting Gelar Akademik Data...")
        try:
            gelar_data = api.get_referensi_gelar_akademik()
            if gelar_data['status']:
                print(f"✅ Success! Found {len(gelar_data['data'])} gelar akademik records")
                print(f"📊 Cache: {gelar_data['cache']}")
                
                # Show first 5 entries
                for i, gelar in enumerate(gelar_data['data'][:5]):
                    print(f"   {i+1}. {gelar.get('nama_gelar', 'N/A')} - {gelar.get('singkatan', 'N/A')}")
                
                if len(gelar_data['data']) > 5:
                    print(f"   ... and {len(gelar_data['data']) - 5} more")
            else:
                print(f"❌ Failed: {gelar_data['message']}")
        except Exception as e:
            print(f"❌ Error getting gelar akademik data: {e}")
        
        # Test 6: Get Cache Statistics
        print("\n6️⃣  Getting Cache Statistics...")
        try:
            cache_stats = api.get_cache_stats()
            print(f"📊 Cache Statistics:")
            print(f"   Total entries: {cache_stats['total_cache_entries']}")
            print(f"   Total size: {cache_stats['total_size_mb']} MB")
            print(f"   Total bytes: {cache_stats['total_size_bytes']}")
        except Exception as e:
            print(f"❌ Error getting cache stats: {e}")
        
        print("\n🎉 Reference data examples completed!")
        print("\n💡 Tips:")
        print("   - Data is cached for better performance")
        print("   - Use cache_manager.py to manage cache")
        print("   - All operations are read-only (safe)")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're in the correct directory and virtual environment is activated")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
