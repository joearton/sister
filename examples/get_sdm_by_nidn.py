#!/usr/bin/env python3
"""
Contoh: Mengambil Data SDM berdasarkan NIDN

Script ini mendemonstrasikan cara mengambil data SDM berdasarkan NIDN spesifik.
NIDN dapat dimasukkan melalui command line argument.

Usage:
    python examples/get_sdm_by_nidn.py [NIDN]
    
Examples:
    python examples/get_sdm_by_nidn.py 0227118803
    python examples/get_sdm_by_nidn.py 0012345678

Semua operasi bersifat read-only (hanya mengambil data, tidak mengubah).
"""

import sys
import os
import argparse
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

def find_sdm_by_nidn(api, nidn):
    """Find SDM by NIDN"""
    try:
        # Search SDM by NIDN
        sdm_response = api.get_referensi_sdm(nidn=nidn)
        
        # Check if response is a dict with data
        if isinstance(sdm_response, dict) and sdm_response.get('status'):
            sdm_list = sdm_response.get('data', [])
        else:
            sdm_list = sdm_response if isinstance(sdm_response, list) else []
        
        if sdm_list and len(sdm_list) > 0:
            # Find the specific SDM with matching NIDN
            for sdm in sdm_list:
                if sdm.get('nidn') == nidn:
                    return sdm
        return None
    except Exception as e:
        print(f"❌ Error mencari SDM dengan NIDN {nidn}: {e}")
        return None

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Mengambil data SDM berdasarkan NIDN",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python examples/get_sdm_by_nidn.py 0227118803
  python examples/get_sdm_by_nidn.py 0012345678
        """
    )
    parser.add_argument(
        'nidn',
        help='NIDN (Nomor Induk Dosen Nasional) yang akan dicari'
    )
    return parser.parse_args()

def validate_nidn(nidn):
    """Validate NIDN format"""
    if not nidn.isdigit():
        return False, "NIDN harus berupa angka"
    if len(nidn) != 10:
        return False, "NIDN harus terdiri dari 10 digit"
    return True, ""

def main():
    """Main function to demonstrate SDM data retrieval by NIDN"""
    # Parse command line arguments
    args = parse_arguments()
    NIDN_TARGET = args.nidn
    
    # Validate NIDN format
    is_valid, error_message = validate_nidn(NIDN_TARGET)
    if not is_valid:
        print(f"❌ Error: {error_message}")
        print(f"💡 NIDN yang dimasukkan: {NIDN_TARGET}")
        return 1
    
    print("🚀 Contoh: Mengambil Data SDM berdasarkan NIDN")
    print(f"🎯 Target NIDN: {NIDN_TARGET}")
    print(f"⏰ Waktu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Initialize API client
        api = SisterAPI
        
        # ========================================
        # 1. MENCARI SDM BERDASARKAN NIDN
        # ========================================
        print_section("MENCARI SDM BERDASARKAN NIDN")
        
        print(f"\n🔍 Mencari SDM dengan NIDN: {NIDN_TARGET}")
        sdm_data = find_sdm_by_nidn(api, NIDN_TARGET)
        
        if not sdm_data:
            print(f"❌ SDM dengan NIDN {NIDN_TARGET} tidak ditemukan")
            print("💡 Mencoba mencari di semua data SDM...")
            
            # Fallback: search in all SDM data
            all_sdm_response = api.get_referensi_sdm()
            
            # Check if response is a dict with data
            if isinstance(all_sdm_response, dict) and all_sdm_response.get('status'):
                all_sdm = all_sdm_response.get('data', [])
            else:
                all_sdm = all_sdm_response if isinstance(all_sdm_response, list) else []
            
            if all_sdm and len(all_sdm) > 0:
                for sdm in all_sdm:
                    if sdm.get('nidn') == NIDN_TARGET:
                        sdm_data = sdm
                        break
                
                if not sdm_data:
                    print(f"❌ SDM dengan NIDN {NIDN_TARGET} tidak ditemukan dalam database")
                    print("📝 Menampilkan beberapa SDM yang tersedia:")
                    for i, sdm in enumerate(all_sdm[:10], 1):
                        print(f"  {i}. {sdm.get('nama_sdm', 'N/A')} - NIDN: {sdm.get('nidn', 'N/A')}")
                    return 1
        
        if sdm_data:
            print(f"✅ SDM ditemukan!")
            print(f"👤 Nama: {sdm_data.get('nama_sdm', 'N/A')}")
            print(f"🆔 ID SDM: {sdm_data.get('id_sdm', 'N/A')}")
            print(f"📋 NIDN: {sdm_data.get('nidn', 'N/A')}")
            print(f"🏷️ NUPTK: {sdm_data.get('nuptk', 'N/A')}")
            print(f"👔 Status: {sdm_data.get('nama_status_aktif', 'N/A')}")
            print(f"💼 Jenis Pegawai: {sdm_data.get('nama_status_pegawai', 'N/A')}")
            print(f"🎓 Jenis SDM: {sdm_data.get('jenis_sdm', 'N/A')}")
            print(f"📅 Update: {sdm_data.get('waktu_data_update', 'N/A')}")
            
            sdm_id = sdm_data['id_sdm']
            sdm_name = sdm_data['nama_sdm']
            
            # ========================================
            # 2. DATA PRIBADI SDM
            # ========================================
            print_section("DATA PRIBADI SDM")
            
            print(f"\n👤 Mengambil data pribadi untuk: {sdm_name}")
            
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
            
            # Get keluarga data
            try:
                keluarga = api.get_data_pribadi_keluarga(id_sdm=sdm_id)
                print_data(keluarga, "Data Keluarga")
            except Exception as e:
                print(f"❌ Error mengambil data keluarga: {e}")
            
            # Get alamat data
            try:
                alamat = api.get_data_pribadi_alamat(id_sdm=sdm_id)
                print_data(alamat, "Data Alamat")
            except Exception as e:
                print(f"❌ Error mengambil data alamat: {e}")
            
            # Get kepegawaian data
            try:
                kepegawaian = api.get_data_pribadi_kepegawaian(id_sdm=sdm_id)
                print_data(kepegawaian, "Data Kepegawaian")
            except Exception as e:
                print(f"❌ Error mengambil data kepegawaian: {e}")
            
            # Get bidang ilmu
            try:
                bidang_ilmu = api.get_data_pribadi_bidang_ilmu(id_sdm=sdm_id)
                print_data(bidang_ilmu, "Bidang Ilmu")
            except Exception as e:
                print(f"❌ Error mengambil bidang ilmu: {e}")
            
            # ========================================
            # 3. TRIDHARMA (Penelitian, Pengabdian, Pengajaran)
            # ========================================
            print_section("TRIDHARMA")
            
            print(f"\n🔬 Mengambil data tridharma untuk: {sdm_name}")
            
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
            
            # Get pengabdian data
            try:
                pengabdian = api.get_pengabdian(id_sdm=sdm_id)
                print_data(pengabdian, "Data Pengabdian")
            except Exception as e:
                print(f"❌ Error mengambil data pengabdian: {e}")
            
            # Get bahan ajar
            try:
                bahan_ajar = api.get_bahan_ajar(id_sdm=sdm_id)
                print_data(bahan_ajar, "Data Bahan Ajar")
            except Exception as e:
                print(f"❌ Error mengambil data bahan ajar: {e}")
            
            # Get tugas tambahan
            try:
                tugas_tambahan = api.get_tugas_tambahan(id_sdm=sdm_id)
                print_data(tugas_tambahan, "Data Tugas Tambahan")
            except Exception as e:
                print(f"❌ Error mengambil data tugas tambahan: {e}")
            
            # ========================================
            # 4. PENDIDIKAN & RIWAYAT
            # ========================================
            print_section("PENDIDIKAN & RIWAYAT")
            
            print(f"\n🎓 Mengambil data pendidikan untuk: {sdm_name}")
            
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
            
            # Get riwayat pekerjaan
            try:
                riwayat_pekerjaan = api.get_riwayat_pekerjaan(id_sdm=sdm_id)
                print_data(riwayat_pekerjaan, "Data Riwayat Pekerjaan")
            except Exception as e:
                print(f"❌ Error mengambil data riwayat pekerjaan: {e}")
            
            # Get sertifikasi profesi
            try:
                sertifikasi_profesi = api.get_sertifikasi_profesi(id_sdm=sdm_id)
                print_data(sertifikasi_profesi, "Data Sertifikasi Profesi")
            except Exception as e:
                print(f"❌ Error mengambil data sertifikasi profesi: {e}")
            
            # ========================================
            # 5. PENUNJANG
            # ========================================
            print_section("PENUNJANG")
            
            print(f"\n🏆 Mengambil data penunjang untuk: {sdm_name}")
            
            # Get anggota profesi
            try:
                anggota_profesi = api.get_anggota_profesi(id_sdm=sdm_id)
                print_data(anggota_profesi, "Data Anggota Profesi")
            except Exception as e:
                print(f"❌ Error mengambil data anggota profesi: {e}")
            
            # Get penghargaan
            try:
                penghargaan = api.get_penghargaan(id_sdm=sdm_id)
                print_data(penghargaan, "Data Penghargaan")
            except Exception as e:
                print(f"❌ Error mengambil data penghargaan: {e}")
            
            # Get pengelola jurnal
            try:
                pengelola_jurnal = api.get_pengelola_jurnal(id_sdm=sdm_id)
                print_data(pengelola_jurnal, "Data Pengelola Jurnal")
            except Exception as e:
                print(f"❌ Error mengambil data pengelola jurnal: {e}")
            
            # Get visiting scientist
            try:
                visiting_scientist = api.get_visiting_scientist(id_sdm=sdm_id)
                print_data(visiting_scientist, "Data Visiting Scientist")
            except Exception as e:
                print(f"❌ Error mengambil data visiting scientist: {e}")
            
            # ========================================
            # 6. REWARD & KESEJAHTERAAN
            # ========================================
            print_section("REWARD & KESEJAHTERAAN")
            
            print(f"\n💰 Mengambil data reward untuk: {sdm_name}")
            
            # Get beasiswa
            try:
                beasiswa = api.get_beasiswa(id_sdm=sdm_id)
                print_data(beasiswa, "Data Beasiswa")
            except Exception as e:
                print(f"❌ Error mengambil data beasiswa: {e}")
            
            # Get kesejahteraan
            try:
                kesejahteraan = api.get_kesejahteraan(id_sdm=sdm_id)
                print_data(kesejahteraan, "Data Kesejahteraan")
            except Exception as e:
                print(f"❌ Error mengambil data kesejahteraan: {e}")
            
            # Get tunjangan
            try:
                tunjangan = api.get_tunjangan(id_sdm=sdm_id)
                print_data(tunjangan, "Data Tunjangan")
            except Exception as e:
                print(f"❌ Error mengambil data tunjangan: {e}")
            
            # ========================================
            # 7. DOKUMEN
            # ========================================
            print_section("DOKUMEN")
            
            print(f"\n📄 Mengambil data dokumen untuk: {sdm_name}")
            
            # Get dokumen list
            try:
                dokumen_list = api.get_dokumen(id_sdm=sdm_id)
                print_data(dokumen_list, "Daftar Dokumen")
            except Exception as e:
                print(f"❌ Error mengambil data dokumen: {e}")
            
            # ========================================
            # 8. BKD (BEBAN KERJA DOSEN)
            # ========================================
            print_section("BKD (BEBAN KERJA DOSEN)")
            
            print(f"\n📊 Mengambil data BKD untuk: {sdm_name}")
            
            # Get laporan akhir BKD
            try:
                laporan_bkd = api.get_bkd_laporan_akhir_bkd(id_sdm=sdm_id)
                print_data(laporan_bkd, "Laporan Akhir BKD")
            except Exception as e:
                print(f"❌ Error mengambil laporan BKD: {e}")
            
            print_section("SELESAI")
            print("✅ Contoh pengambilan data SDM berdasarkan NIDN selesai!")
            print(f"📊 Data berhasil diambil untuk SDM: {sdm_name} (NIDN: {NIDN_TARGET})")
            print("🔒 Semua operasi bersifat read-only (aman)")
        
    except Exception as e:
        print(f"❌ Error umum: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
