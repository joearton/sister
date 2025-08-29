#!/usr/bin/env python3
"""
Sister API Client - Simple Example
Contoh sederhana penggunaan Sister API client

Script ini menunjukkan cara dasar menggunakan API client
untuk mengambil data dari Sister API.
"""

import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def main():
    print("🚀 Sister API Client - Simple Example")
    print("=" * 50)
    
    try:
        from sister import SisterAPI
        
        # Initialize API client (SisterAPI is already an instance)
        print("🔌 Initializing Sister API client...")
        api = SisterAPI
        
        # Example 1: Get basic reference data
        print("\n📋 Example 1: Getting SDM Reference Data")
        print("-" * 40)
        
        try:
            sdm_data = api.get_referensi_sdm()
            
            if sdm_data['status']:
                print(f"✅ Success! Found {len(sdm_data['data'])} SDM records")
                print(f"📊 From cache: {sdm_data['cache']}")
                print(f"⏰ Accessed: {sdm_data['accessed_at_iso']}")
                
                # Show first 3 SDM records
                print("\n📝 First 3 SDM records:")
                for i, sdm in enumerate(sdm_data['data'][:3]):
                    print(f"   {i+1}. {sdm.get('nama', 'N/A')} - {sdm.get('nidn', 'N/A')}")
            else:
                print(f"❌ Failed: {sdm_data['message']}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Example 2: Get gelar akademik data
        print("\n🎓 Example 2: Getting Gelar Akademik Data")
        print("-" * 40)
        
        try:
            gelar_data = api.get_referensi_gelar_akademik()
            
            if gelar_data['status']:
                print(f"✅ Success! Found {len(gelar_data['data'])} gelar akademik records")
                print(f"📊 From cache: {gelar_data['cache']}")
                
                # Show first 5 gelar akademik records
                print("\n📝 First 5 Gelar Akademik:")
                for i, gelar in enumerate(gelar_data['data'][:5]):
                    print(f"   {i+1}. {gelar.get('nama', 'N/A')} ({gelar.get('singkatan', 'N/A')})")
            else:
                print(f"❌ Failed: {gelar_data['message']}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Example 3: Get jabatan fungsional data
        print("\n👨‍🏫 Example 3: Getting Jabatan Fungsional Data")
        print("-" * 40)
        
        try:
            jabatan_data = api.get_referensi_jabatan_fungsional()
            
            if jabatan_data['status']:
                print(f"✅ Success! Found {len(jabatan_data['data'])} jabatan fungsional records")
                print(f"📊 From cache: {jabatan_data['cache']}")
                
                # Show all jabatan fungsional data
                print("\n📝 All Jabatan Fungsional records:")
                for jabatan in jabatan_data['data']:
                    print(f"   - {jabatan.get('nama', 'N/A')} (ID: {jabatan.get('id', 'N/A')})")
            else:
                print(f"❌ Failed: {jabatan_data['message']}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Example 4: Get agama data
        print("\n🙏 Example 4: Getting Agama Data")
        print("-" * 40)
        
        try:
            agama_data = api.get_referensi_agama()
            
            if agama_data['status']:
                print(f"✅ Success! Found {len(agama_data['data'])} agama records")
                print(f"📊 From cache: {agama_data['cache']}")
                
                # Show all agama data
                print("\n📝 All Agama records:")
                for agama in agama_data['data']:
                    print(f"   - {agama.get('nama', 'N/A')} (ID: {agama.get('id', 'N/A')})")
            else:
                print(f"❌ Failed: {agama_data['message']}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Example 5: Get cache statistics
        print("\n📊 Example 5: Getting Cache Statistics")
        print("-" * 40)
        
        try:
            cache_stats = api.get_cache_stats()
            print(f"📊 Cache Statistics:")
            print(f"   Total entries: {cache_stats['total_cache_entries']}")
            print(f"   Total size: {cache_stats['total_size_mb']} MB")
            print(f"   Total bytes: {cache_stats['total_size_bytes']}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n🎉 Simple example completed!")
        print("\n💡 What you learned:")
        print("   - How to initialize the API client")
        print("   - How to get reference data")
        print("   - How to check cache status")
        print("   - All operations are read-only (safe)")
        
        print("\n📚 Next steps:")
        print("   - Try other reference endpoints")
        print("   - Get detailed SDM data")
        print("   - Explore academic data")
        print("   - Use cache management tools")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're in the correct directory and virtual environment is activated")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
