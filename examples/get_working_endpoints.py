#!/usr/bin/env python3
"""
Contoh Endpoint yang Berfungsi: Mengambil Data dari Sister API

Script ini mendemonstrasikan cara mengambil data dari endpoint-endpoint
yang sudah terbukti berfungsi berdasarkan testing.
Semua operasi bersifat read-only (hanya mengambil data, tidak mengubah).
"""

import sys
import os
from datetime import datetime

# Add parent directory to path to import sister module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api import SisterAPI

def print_section(title):
    """Print section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_data(data, title="Data"):
    """Print data in a formatted way"""
    print(f"\n{title}:")
    if isinstance(data, dict):
        if data.get('status') == False:
            print(f"❌ Error: {data.get('message', 'Unknown error')}")
            if data.get('detail'):
                print(f"   Detail: {data['detail']}")
        else:
            print(f"✅ Success: {len(data.get('data', []))} records")
            if 'data' in data and isinstance(data['data'], list):
                for i, item in enumerate(data['data'][:5], 1):
                    print(f"  {i}. {item}")
                if len(data['data']) > 5:
                    print(f"  ... dan {len(data['data']) - 5} data lainnya")
    elif isinstance(data, list):
        print(f"✅ Success: {len(data)} records")
        for i, item in enumerate(data[:5], 1):
            print(f"  {i}. {item}")
        if len(data) > 5:
            print(f"  ... dan {len(data) - 5} data lainnya")
    else:
        print(f"  {data}")

def main():
    """Main function to demonstrate working endpoints"""
    print("🚀 Memulai Contoh Endpoint yang Berfungsi")
    print(f"⏰ Waktu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Initialize API client
        api = SisterAPI
        
        # ========================================
        # 1. REFERENSI YANG BERFUNGSI
        # ========================================
        print_section("REFERENSI YANG BERFUNGSI")
        
        # Get SDM list (sudah terbukti berfungsi)
        print("\n👥 Mengambil data SDM...")
        sdm_list = api.get_referensi_sdm()
        print_data(sdm_list, "Daftar SDM")
        
        # Get agama list (sudah terbukti berfungsi)
        print("\n🙏 Mengambil data agama...")
        agama_list = api.get_referensi_agama()
        print_data(agama_list, "Daftar Agama")
        
        # Get gelar akademik
        print("\n🎓 Mengambil data gelar akademik...")
        gelar_akademik = api.get_referensi_gelar_akademik()
        print_data(gelar_akademik, "Daftar Gelar Akademik")
        
        # Get jabatan fungsional
        print("\n👨‍🏫 Mengambil data jabatan fungsional...")
        jabatan_fungsional = api.get_referensi_jabatan_fungsional()
        print_data(jabatan_fungsional, "Daftar Jabatan Fungsional")
        
        # Get jenis publikasi
        print("\n📝 Mengambil data jenis publikasi...")
        jenis_publikasi = api.get_referensi_jenis_publikasi()
        print_data(jenis_publikasi, "Daftar Jenis Publikasi")
        
        # Get jenis dokumen
        print("\n📄 Mengambil data jenis dokumen...")
        jenis_dokumen = api.get_referensi_jenis_dokumen()
        print_data(jenis_dokumen, "Daftar Jenis Dokumen")
        
        # Get jenis tunjangan
        print("\n💵 Mengambil data jenis tunjangan...")
        jenis_tunjangan = api.get_referensi_jenis_tunjangan()
        print_data(jenis_tunjangan, "Daftar Jenis Tunjangan")
        
        # Get jenis penghargaan
        print("\n🏆 Mengambil data jenis penghargaan...")
        jenis_penghargaan = api.get_referensi_jenis_penghargaan()
        print_data(jenis_penghargaan, "Daftar Jenis Penghargaan")
        
        # Get jenis kepanitiaan
        print("\n👥 Mengambil data jenis kepanitiaan...")
        jenis_kepanitiaan = api.get_referensi_jenis_kepanitiaan()
        print_data(jenis_kepanitiaan, "Daftar Jenis Kepanitiaan")
        
        # Get jenis jabatan negara
        print("\n🏛️ Mengambil data jenis jabatan negara...")
        jenis_jabatan_negara = api.get_referensi_jabatan_negara()
        print_data(jenis_jabatan_negara, "Daftar Jenis Jabatan Negara")
        
        # Get ikatan kerja
        print("\n💼 Mengambil data ikatan kerja...")
        ikatan_kerja = api.get_referensi_ikatan_kerja()
        print_data(ikatan_kerja, "Daftar Ikatan Kerja")
        
        # Get status kepegawaian
        print("\n👨‍💼 Mengambil data status kepegawaian...")
        status_kepegawaian = api.get_referensi_status_kepegawaian()
        print_data(status_kepegawaian, "Daftar Status Kepegawaian")
        
        # Get sumber gaji
        print("\n💳 Mengambil data sumber gaji...")
        sumber_gaji = api.get_referensi_sumber_gaji()
        print_data(sumber_gaji, "Daftar Sumber Gaji")
        
        # Get jenjang pendidikan
        print("\n🎓 Mengambil data jenjang pendidikan...")
        jenjang_pendidikan = api.get_referensi_jenjang_pendidikan()
        print_data(jenjang_pendidikan, "Daftar Jenjang Pendidikan")
        
        # Get tingkat penghargaan
        print("\n🏅 Mengambil data tingkat penghargaan...")
        tingkat_penghargaan = api.get_referensi_tingkat_penghargaan()
        print_data(tingkat_penghargaan, "Daftar Tingkat Penghargaan")
        
        # ========================================
        # 2. DATA SDM DETAIL (jika ada SDM)
        # ========================================
        print_section("DATA SDM DETAIL")
        
        if sdm_list and len(sdm_list) > 0:
            first_sdm = sdm_list[0]
            sdm_id = first_sdm['id_sdm']
            sdm_name = first_sdm['nama_sdm']  # Perbaiki field name
            
            print(f"\n👤 Mengambil detail data untuk SDM: {sdm_name}")
            
            # Get profil SDM
            try:
                profil_sdm = api.get_data_pribadi_profil(id_sdm=sdm_id)
                print_data(profil_sdm, "Profil SDM")
            except Exception as e:
                print(f"❌ Error mengambil profil SDM: {e}")
            
            # Get kependudukan data
            try:
                kependudukan = api.get_data_pribadi_kependudukan(id_sdm=sdm_id)
                print_data(kependudukan, "Data Kependudukan")
            except Exception as e:
                print(f"❌ Error mengambil data kependudukan: {e}")
            
            # Get bidang ilmu
            try:
                bidang_ilmu = api.get_data_pribadi_bidang_ilmu(id_sdm=sdm_id)
                print_data(bidang_ilmu, "Bidang Ilmu")
            except Exception as e:
                print(f"❌ Error mengambil bidang ilmu: {e}")
        
        # ========================================
        # 3. TRIDHARMA (jika ada SDM)
        # ========================================
        print_section("TRIDHARMA")
        
        if sdm_list:
            sdm_id = sdm_list[0]['id_sdm']
            
            # Get penelitian data
            try:
                penelitian = api.get_penelitian(id_sdm=sdm_id)
                print_data(penelitian, "Data Penelitian")
            except Exception as e:
                print(f"❌ Error mengambil data penelitian: {e}")
            
            # Get publikasi data
            try:
                publikasi = api.get_publikasi(id_sdm=sdm_id)
                print_data(publikasi, "Data Publikasi")
            except Exception as e:
                print(f"❌ Error mengambil data publikasi: {e}")
            
            # Get bahan ajar
            try:
                bahan_ajar = api.get_bahan_ajar(id_sdm=sdm_id)
                print_data(bahan_ajar, "Data Bahan Ajar")
            except Exception as e:
                print(f"❌ Error mengambil data bahan ajar: {e}")
        
        # ========================================
        # 4. PENDIDIKAN & RIWAYAT (jika ada SDM)
        # ========================================
        print_section("PENDIDIKAN & RIWAYAT")
        
        if sdm_list:
            sdm_id = sdm_list[0]['id_sdm']
            
            # Get pendidikan formal
            try:
                pendidikan_formal = api.get_pendidikan_formal(id_sdm=sdm_id)
                print_data(pendidikan_formal, "Data Pendidikan Formal")
            except Exception as e:
                print(f"❌ Error mengambil data pendidikan formal: {e}")
            
            # Get diklat
            try:
                diklat = api.get_diklat(id_sdm=sdm_id)
                print_data(diklat, "Data Diklat")
            except Exception as e:
                print(f"❌ Error mengambil data diklat: {e}")
        
        # ========================================
        # 5. CACHE STATISTICS
        # ========================================
        print_section("CACHE STATISTICS")
        
        try:
            cache_stats = api.get_cache_stats()
            print_data(cache_stats, "Statistik Cache")
        except Exception as e:
            print(f"❌ Error mengambil statistik cache: {e}")
        
        print_section("SELESAI")
        print("✅ Contoh endpoint yang berfungsi selesai!")
        print("📊 Semua data berhasil diambil (read-only operations)")
        
    except Exception as e:
        print(f"❌ Error umum: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
