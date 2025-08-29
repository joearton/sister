#!/usr/bin/env python3
"""
Sister API Client - Academic Data Examples
Contoh script untuk mengambil data akademik (read-only operations)

Data yang diambil:
- Data penelitian
- Data publikasi
- Data pengajaran
- Data pengabdian
"""

import sys
import os
import json
from datetime import datetime

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def main():
    print("🎓 Sister API Client - Academic Data Examples")
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
            
            # Get first SDM for academic data example
            if sdm_list['data']:
                first_sdm = sdm_list['data'][0]
                sdm_id = first_sdm.get('id_sdm')
                sdm_name = first_sdm.get('nama', 'Unknown')
                
                print(f"\n🔍 Getting academic data for: {sdm_name} (ID: {sdm_id})")
                
                # Test 1: Get Research Data
                print("\n1️⃣  Getting Research Data...")
                try:
                    penelitian_data = api.get_penelitian_bypath(id_sdm=sdm_id)
                    if penelitian_data['status']:
                        print(f"✅ Success! Research data retrieved")
                        print(f"📊 Cache: {penelitian_data['cache']}")
                        
                        penelitian_list = penelitian_data['data']
                        print(f"   🔬 Found {len(penelitian_list)} research projects")
                        
                        for i, penelitian in enumerate(penelitian_list[:3]):
                            print(f"   {i+1}. {penelitian.get('judul_penelitian', 'N/A')}")
                            print(f"      📅 Year: {penelitian.get('tahun_penelitian', 'N/A')}")
                            print(f"      💰 Funding: {penelitian.get('sumber_dana', 'N/A')}")
                            print(f"      👥 Role: {penelitian.get('peran_peneliti', 'N/A')}")
                        
                        if len(penelitian_list) > 3:
                            print(f"   ... and {len(penelitian_list) - 3} more research projects")
                    else:
                        print(f"❌ Failed: {penelitian_data['message']}")
                except Exception as e:
                    print(f"❌ Error getting research data: {e}")
                
                # Test 2: Get Publication Data
                print("\n2️⃣  Getting Publication Data...")
                try:
                    publikasi_data = api.get_publikasi_bypath(id_sdm=sdm_id)
                    if publikasi_data['status']:
                        print(f"✅ Success! Publication data retrieved")
                        print(f"📊 Cache: {publikasi_data['cache']}")
                        
                        publikasi_list = publikasi_data['data']
                        print(f"   📚 Found {len(publikasi_list)} publications")
                        
                        for i, publikasi in enumerate(publikasi_list[:3]):
                            print(f"   {i+1}. {publikasi.get('judul_publikasi', 'N/A')}")
                            print(f"      📅 Year: {publikasi.get('tahun_publikasi', 'N/A')}")
                            print(f"      📖 Type: {publikasi.get('jenis_publikasi', 'N/A')}")
                            print(f"      👥 Role: {publikasi.get('peran_penulis', 'N/A')}")
                        
                        if len(publikasi_list) > 3:
                            print(f"   ... and {len(publikasi_list) - 3} more publications")
                    else:
                        print(f"❌ Failed: {publikasi_data['message']}")
                except Exception as e:
                    print(f"❌ Error getting publication data: {e}")
                
                # Test 3: Get Teaching Data
                print("\n3️⃣  Getting Teaching Data...")
                try:
                    pengajaran_data = api.get_pengajaran_bypath(id_sdm=sdm_id)
                    if pengajaran_data['status']:
                        print(f"✅ Success! Teaching data retrieved")
                        print(f"📊 Cache: {pengajaran_data['cache']}")
                        
                        pengajaran_list = pengajaran_data['data']
                        print(f"   📖 Found {len(pengajaran_list)} teaching records")
                        
                        for i, pengajaran in enumerate(pengajaran_list[:3]):
                            print(f"   {i+1}. {pengajaran.get('nama_mata_kuliah', 'N/A')}")
                            print(f"      📅 Semester: {pengajaran.get('semester', 'N/A')}")
                            print(f"      📚 Program: {pengajaran.get('program_studi', 'N/A')}")
                            print(f"      👥 Students: {pengajaran.get('jumlah_mahasiswa', 'N/A')}")
                        
                        if len(pengajaran_list) > 3:
                            print(f"   ... and {len(pengajaran_list) - 3} more teaching records")
                    else:
                        print(f"❌ Failed: {pengajaran_data['message']}")
                except Exception as e:
                    print(f"❌ Error getting teaching data: {e}")
                
                # Test 4: Get Community Service Data
                print("\n4️⃣  Getting Community Service Data...")
                try:
                    pengabdian_data = api.get_pengabdian_bypath(id_sdm=sdm_id)
                    if pengabdian_data['status']:
                        print(f"✅ Success! Community service data retrieved")
                        print(f"📊 Cache: {pengabdian_data['cache']}")
                        
                        pengabdian_list = pengabdian_data['data']
                        print(f"   🤝 Found {len(pengabdian_list)} community service projects")
                        
                        for i, pengabdian in enumerate(pengabdian_list[:3]):
                            print(f"   {i+1}. {pengabdian.get('judul_kegiatan', 'N/A')}")
                            print(f"      📅 Year: {pengabdian.get('tahun_kegiatan', 'N/A')}")
                            print(f"      🎯 Target: {pengabdian.get('sasaran_kegiatan', 'N/A')}")
                            print(f"      👥 Role: {pengabdian.get('peran_kegiatan', 'N/A')}")
                        
                        if len(pengabdian_list) > 3:
                            print(f"   ... and {len(pengabdian_list) - 3} more community service projects")
                    else:
                        print(f"❌ Failed: {pengabdian_data['message']}")
                except Exception as e:
                    print(f"❌ Error getting community service data: {e}")
                
                # Test 5: Get Student Supervision Data
                print("\n5️⃣  Getting Student Supervision Data...")
                try:
                    bimbingan_data = api.get_bimbingan_mahasiswa_bypath(id_sdm=sdm_id)
                    if bimbingan_data['status']:
                        print(f"✅ Success! Student supervision data retrieved")
                        print(f"📊 Cache: {bimbingan_data['cache']}")
                        
                        bimbingan_list = bimbingan_data['data']
                        print(f"   👨‍🎓 Found {len(bimbingan_list)} student supervision records")
                        
                        for i, bimbingan in enumerate(bimbingan_list[:3]):
                            print(f"   {i+1}. {bimbingan.get('nama_mahasiswa', 'N/A')}")
                            print(f"      📚 Program: {bimbingan.get('program_studi', 'N/A')}")
                            print(f"      📝 Type: {bimbingan.get('jenis_bimbingan', 'N/A')}")
                            print(f"      📅 Year: {bimbingan.get('tahun_bimbingan', 'N/A')}")
                        
                        if len(bimbingan_list) > 3:
                            print(f"   ... and {len(bimbingan_list) - 3} more supervision records")
                    else:
                        print(f"❌ Failed: {bimbingan_data['message']}")
                except Exception as e:
                    print(f"❌ Error getting student supervision data: {e}")
                
                # Test 6: Get Awards Data
                print("\n6️⃣  Getting Awards Data...")
                try:
                    penghargaan_data = api.get_penghargaan_bypath(id_sdm=sdm_id)
                    if penghargaan_data['status']:
                        print(f"✅ Success! Awards data retrieved")
                        print(f"📊 Cache: {penghargaan_data['cache']}")
                        
                        penghargaan_list = penghargaan_data['data']
                        print(f"   🏆 Found {len(penghargaan_list)} awards")
                        
                        for i, penghargaan in enumerate(penghargaan_list[:3]):
                            print(f"   {i+1}. {penghargaan.get('nama_penghargaan', 'N/A')}")
                            print(f"      📅 Year: {penghargaan.get('tahun_penghargaan', 'N/A')}")
                            print(f"      🏢 Institution: {penghargaan.get('lembaga_pemberi', 'N/A')}")
                            print(f"      📋 Level: {penghargaan.get('tingkat_penghargaan', 'N/A')}")
                        
                        if len(penghargaan_list) > 3:
                            print(f"   ... and {len(penghargaan_list) - 3} more awards")
                    else:
                        print(f"❌ Failed: {penghargaan_data['message']}")
                except Exception as e:
                    print(f"❌ Error getting awards data: {e}")
                
            else:
                print("❌ No SDM data found")
        
        except Exception as e:
            print(f"❌ Error getting SDM list: {e}")
        
        print("\n🎉 Academic data examples completed!")
        print("\n💡 Tips:")
        print("   - All operations are read-only (safe)")
        print("   - Data is cached for better performance")
        print("   - Use different SDM IDs to get different academic data")
        print("   - Academic data includes research, publications, teaching, etc.")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're in the correct directory and virtual environment is activated")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
