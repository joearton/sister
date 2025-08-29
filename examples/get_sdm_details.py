#!/usr/bin/env python3
"""
Sister API Client - SDM Details Examples
Contoh script untuk mengambil detail data SDM (read-only operations)

Data yang diambil:
- Profil SDM
- Data pribadi
- Riwayat pendidikan
- Jabatan dan kepangkatan
"""

import sys
import os
import json
from datetime import datetime

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def main():
    print("👥 Sister API Client - SDM Details Examples")
    print("=" * 60)
    
    try:
        from sister import SisterAPI
        
        # Initialize API client
        print("🔌 Initializing Sister API client...")
        api = SisterAPI
        
        # Get SDM list first
        print("\n📋 Getting SDM List...")
        try:
            sdm_list = api.get_referensi_sdm()
            if not sdm_list['status']:
                print(f"❌ Failed to get SDM list: {sdm_list['message']}")
                return
            
            print(f"✅ Found {len(sdm_list['data'])} SDM records")
            
            # Get first SDM for detailed example
            if sdm_list['data']:
                first_sdm = sdm_list['data'][0]
                sdm_id = first_sdm.get('id_sdm')
                sdm_name = first_sdm.get('nama', 'Unknown')
                
                print(f"\n🔍 Getting details for: {sdm_name} (ID: {sdm_id})")
                
                # Test 1: Get SDM Profile
                print("\n1️⃣  Getting SDM Profile...")
                try:
                    profile_data = api.get_data_pribadi_profil_bypath(id_sdm=sdm_id)
                    if profile_data['status']:
                        print(f"✅ Success! Profile data retrieved")
                        print(f"📊 Cache: {profile_data['cache']}")
                        
                        profile = profile_data['data']
                        print(f"   📝 Name: {profile.get('nama', 'N/A')}")
                        print(f"   🆔 NIDN: {profile.get('nidn', 'N/A')}")
                        print(f"   📧 Email: {profile.get('email', 'N/A')}")
                        print(f"   📱 Phone: {profile.get('no_hp', 'N/A')}")
                    else:
                        print(f"❌ Failed: {profile_data['message']}")
                except Exception as e:
                    print(f"❌ Error getting profile: {e}")
                
                # Test 2: Get SDM Kependudukan Data
                print("\n2️⃣  Getting SDM Kependudukan Data...")
                try:
                    kependudukan_data = api.get_data_pribadi_kependudukan_bypath(id_sdm=sdm_id)
                    if kependudukan_data['status']:
                        print(f"✅ Success! Kependudukan data retrieved")
                        print(f"📊 Cache: {kependudukan_data['cache']}")
                        
                        kependudukan = kependudukan_data['data']
                        print(f"   🆔 NIK: {kependudukan.get('nik', 'N/A')}")
                        print(f"   📅 Birth Date: {kependudukan.get('tanggal_lahir', 'N/A')}")
                        print(f"   🏠 Birth Place: {kependudukan.get('tempat_lahir', 'N/A')}")
                        print(f"   👫 Gender: {kependudukan.get('jenis_kelamin', 'N/A')}")
                    else:
                        print(f"❌ Failed: {kependudukan_data['message']}")
                except Exception as e:
                    print(f"❌ Error getting kependudukan: {e}")
                
                # Test 3: Get SDM Family Data
                print("\n3️⃣  Getting SDM Family Data...")
                try:
                    keluarga_data = api.get_data_pribadi_keluarga_bypath(id_sdm=sdm_id)
                    if keluarga_data['status']:
                        print(f"✅ Success! Family data retrieved")
                        print(f"📊 Cache: {keluarga_data['cache']}")
                        
                        keluarga_list = keluarga_data['data']
                        print(f"   👨‍👩‍👧‍👦 Found {len(keluarga_list)} family members")
                        
                        for i, anggota in enumerate(keluarga_list[:3]):
                            print(f"   {i+1}. {anggota.get('nama', 'N/A')} - {anggota.get('hubungan', 'N/A')}")
                        
                        if len(keluarga_list) > 3:
                            print(f"   ... and {len(keluarga_list) - 3} more family members")
                    else:
                        print(f"❌ Failed: {keluarga_data['message']}")
                except Exception as e:
                    print(f"❌ Error getting family data: {e}")
                
                # Test 4: Get SDM Address Data
                print("\n4️⃣  Getting SDM Address Data...")
                try:
                    alamat_data = api.get_data_pribadi_alamat_bypath(id_sdm=sdm_id)
                    if alamat_data['status']:
                        print(f"✅ Success! Address data retrieved")
                        print(f"📊 Cache: {alamat_data['cache']}")
                        
                        alamat_list = alamat_data['data']
                        print(f"   🏠 Found {len(alamat_list)} addresses")
                        
                        for i, alamat in enumerate(alamat_list[:2]):
                            print(f"   {i+1}. {alamat.get('alamat', 'N/A')}")
                            print(f"      📍 {alamat.get('kota', 'N/A')}, {alamat.get('provinsi', 'N/A')}")
                    else:
                        print(f"❌ Failed: {alamat_data['message']}")
                except Exception as e:
                    print(f"❌ Error getting address data: {e}")
                
                # Test 5: Get SDM Employment Data
                print("\n5️⃣  Getting SDM Employment Data...")
                try:
                    kepegawaian_data = api.get_data_pribadi_kepegawaian_bypath(id_sdm=sdm_id)
                    if kepegawaian_data['status']:
                        print(f"✅ Success! Employment data retrieved")
                        print(f"📊 Cache: {kepegawaian_data['cache']}")
                        
                        kepegawaian = kepegawaian_data['data']
                        print(f"   🏢 Institution: {kepegawaian.get('nama_perguruan_tinggi', 'N/A')}")
                        print(f"   📅 Join Date: {kepegawaian.get('tanggal_bergabung', 'N/A')}")
                        print(f"   📋 Status: {kepegawaian.get('status_kepegawaian', 'N/A')}")
                    else:
                        print(f"❌ Failed: {kepegawaian_data['message']}")
                except Exception as e:
                    print(f"❌ Error getting employment data: {e}")
                
                # Test 6: Get SDM Academic Field Data
                print("\n6️⃣  Getting SDM Academic Field Data...")
                try:
                    bidang_ilmu_data = api.get_data_pribadi_bidang_ilmu_bypath(id_sdm=sdm_id)
                    if bidang_ilmu_data['status']:
                        print(f"✅ Success! Academic field data retrieved")
                        print(f"📊 Cache: {bidang_ilmu_data['cache']}")
                        
                        bidang_list = bidang_ilmu_data['data']
                        print(f"   🔬 Found {len(bidang_list)} academic fields")
                        
                        for i, bidang in enumerate(bidang_list[:3]):
                            print(f"   {i+1}. {bidang.get('nama_bidang_ilmu', 'N/A')}")
                        
                        if len(bidang_list) > 3:
                            print(f"   ... and {len(bidang_list) - 3} more fields")
                    else:
                        print(f"❌ Failed: {bidang_ilmu_data['message']}")
                except Exception as e:
                    print(f"❌ Error getting academic field data: {e}")
                
            else:
                print("❌ No SDM data found")
        
        except Exception as e:
            print(f"❌ Error getting SDM list: {e}")
        
        print("\n🎉 SDM details examples completed!")
        print("\n💡 Tips:")
        print("   - All operations are read-only (safe)")
        print("   - Data is cached for better performance")
        print("   - Use different SDM IDs to get different data")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're in the correct directory and virtual environment is activated")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
