#!/usr/bin/env python3
"""
Contoh Komprehensif: Mengambil Berbagai Jenis Data dari Sister API

Script ini mendemonstrasikan cara mengambil berbagai jenis data dari Sister API,
termasuk data referensi, data SDM, aktivitas akademik, dan lainnya.
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
    if isinstance(data, list):
        print(f"Jumlah data: {len(data)}")
        for i, item in enumerate(data[:5], 1):  # Show first 5 items
            print(f"  {i}. {item}")
        if len(data) > 5:
            print(f"  ... dan {len(data) - 5} data lainnya")
    else:
        print(f"  {data}")

def main():
    """Main function to demonstrate comprehensive data retrieval"""
    print("🚀 Memulai Contoh Komprehensif Sister API")
    print(f"⏰ Waktu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Initialize API client
        api = SisterAPI
        
        # ========================================
        # 1. DATA REFERENSI (Reference Data)
        # ========================================
        print_section("DATA REFERENSI")
        
        # Get perguruan tinggi list
        print("\n📚 Mengambil data perguruan tinggi...")
        pt_list = api.get_referensi_perguruan_tinggi()
        print_data(pt_list, "Daftar Perguruan Tinggi")
        
        # Get unit kerja for first PT (if available)
        if pt_list:
            first_pt = pt_list[0]
            print(f"\n🏢 Mengambil unit kerja untuk PT: {first_pt.get('nama', 'Unknown')}")
            unit_kerja = api.get_referensi_unit_kerja(id_perguruan_tinggi=first_pt['id'])
            print_data(unit_kerja, "Daftar Unit Kerja")
        
        # Get agama list
        print("\n🙏 Mengambil data agama...")
        agama_list = api.get_referensi_agama()
        print_data(agama_list, "Daftar Agama")
        
        # Get bidang studi
        print("\n🔬 Mengambil data bidang studi...")
        bidang_studi = api.get_referensi_bidang_studi()
        print_data(bidang_studi, "Daftar Bidang Studi")
        
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
        
        # Get negara
        print("\n🌍 Mengambil data negara...")
        negara_list = api.get_referensi_negara()
        print_data(negara_list, "Daftar Negara")
        
        # Get semester
        print("\n📅 Mengambil data semester...")
        semester_list = api.get_referensi_semester()
        print_data(semester_list, "Daftar Semester")
        
        # Get profil PT
        print("\n🏛️ Mengambil profil perguruan tinggi...")
        profil_pt = api.get_referensi_profil_pt()
        print_data(profil_pt, "Profil Perguruan Tinggi")
        
        # ========================================
        # 2. DATA SDM (Staff Data)
        # ========================================
        print_section("DATA SDM")
        
        # Get SDM list (first 10)
        print("\n👥 Mengambil data SDM...")
        sdm_list = api.get_referensi_sdm()
        print_data(sdm_list, "Daftar SDM")
        
        # If we have SDM data, get detailed information for first SDM
        if sdm_list:
            first_sdm = sdm_list[0]
            sdm_id = first_sdm['id_sdm']
            sdm_name = first_sdm['nama']
            
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
        # 3. AKTIVITAS AKADEMIK (Academic Activities)
        # ========================================
        print_section("AKTIVITAS AKADEMIK")
        
        if sdm_list and semester_list:
            sdm_id = sdm_list[0]['id_sdm']
            semester_id = semester_list[0]['id']
            
            print(f"\n📚 Mengambil aktivitas akademik untuk semester: {semester_id}")
            
            # Get pengajaran data
            try:
                pengajaran = api.get_pengajaran(id_sdm=sdm_id, id_semester=semester_id)
                print_data(pengajaran, "Data Pengajaran")
            except Exception as e:
                print(f"❌ Error mengambil data pengajaran: {e}")
            
            # Get bimbingan mahasiswa
            try:
                bimbingan = api.get_bimbingan_mahasiswa(id_sdm=sdm_id, id_semester=semester_id)
                print_data(bimbingan, "Data Bimbingan Mahasiswa")
            except Exception as e:
                print(f"❌ Error mengambil data bimbingan: {e}")
            
            # Get pengujian mahasiswa
            try:
                pengujian = api.get_pengujian_mahasiswa(id_sdm=sdm_id, id_semester=semester_id)
                print_data(pengujian, "Data Pengujian Mahasiswa")
            except Exception as e:
                print(f"❌ Error mengambil data pengujian: {e}")
        
        # ========================================
        # 4. TRIDHARMA (Research, Teaching, Community Service)
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
        # 5. PENUNJANG (Supporting Activities)
        # ========================================
        print_section("PENUNJANG")
        
        if sdm_list:
            sdm_id = sdm_list[0]['id_sdm']
            
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
        # 6. PENDIDIKAN & RIWAYAT (Education & History)
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
            
            # Get nilai tes
            try:
                nilai_tes = api.get_nilai_tes(id_sdm=sdm_id)
                print_data(nilai_tes, "Data Nilai Tes")
            except Exception as e:
                print(f"❌ Error mengambil data nilai tes: {e}")
        
        # ========================================
        # 7. REWARD & KESEJAHTERAAN (Rewards & Welfare)
        # ========================================
        print_section("REWARD & KESEJAHTERAAN")
        
        if sdm_list:
            sdm_id = sdm_list[0]['id_sdm']
            
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
        # 8. BKD (BEBAN KERJA DOSEN)
        # ========================================
        print_section("BKD (BEBAN KERJA DOSEN)")
        
        if sdm_list and semester_list:
            sdm_id = sdm_list[0]['id_sdm']
            semester_id = semester_list[0]['id']
            
            # Get laporan akhir BKD
            try:
                laporan_bkd = api.get_bkd_laporan_akhir_bkd(id_sdm=sdm_id)
                print_data(laporan_bkd, "Laporan Akhir BKD")
            except Exception as e:
                print(f"❌ Error mengambil laporan BKD: {e}")
            
            # Get BKD pendidikan
            try:
                bkd_pendidikan = api.get_bkd_pendidikan(id_sdm=sdm_id, id_smt=semester_id)
                print_data(bkd_pendidikan, "BKD Pendidikan")
            except Exception as e:
                print(f"❌ Error mengambil BKD pendidikan: {e}")
            
            # Get BKD pengajaran
            try:
                bkd_ajar = api.get_bkd_ajar(id_sdm=sdm_id, id_smt=semester_id)
                print_data(bkd_ajar, "BKD Pengajaran")
            except Exception as e:
                print(f"❌ Error mengambil BKD pengajaran: {e}")
            
            # Get BKD penelitian
            try:
                bkd_penelitian = api.get_bkd_penelitian(id_sdm=sdm_id, id_smt=semester_id)
                print_data(bkd_penelitian, "BKD Penelitian")
            except Exception as e:
                print(f"❌ Error mengambil BKD penelitian: {e}")
            
            # Get BKD pengabdian
            try:
                bkd_pengmas = api.get_bkd_pengmas(id_sdm=sdm_id, id_smt=semester_id)
                print_data(bkd_pengmas, "BKD Pengabdian")
            except Exception as e:
                print(f"❌ Error mengambil BKD pengabdian: {e}")
            
            # Get BKD penunjang
            try:
                bkd_tunjang = api.get_bkd_tunjang(id_sdm=sdm_id, id_smt=semester_id)
                print_data(bkd_tunjang, "BKD Penunjang")
            except Exception as e:
                print(f"❌ Error mengambil BKD penunjang: {e}")
        
        # ========================================
        # 9. DOKUMEN (Documents)
        # ========================================
        print_section("DOKUMEN")
        
        if sdm_list:
            sdm_id = sdm_list[0]['id_sdm']
            
            # Get dokumen list
            try:
                dokumen_list = api.get_dokumen(id_sdm=sdm_id)
                print_data(dokumen_list, "Daftar Dokumen")
            except Exception as e:
                print(f"❌ Error mengambil data dokumen: {e}")
        
        # ========================================
        # 10. KOLABORATOR EKSTERNAL
        # ========================================
        print_section("KOLABORATOR EKSTERNAL")
        
        # Get kolaborator eksternal
        try:
            kolaborator = api.get_kolaborator_eksternal()
            print_data(kolaborator, "Data Kolaborator Eksternal")
        except Exception as e:
            print(f"❌ Error mengambil data kolaborator: {e}")
        
        print_section("SELESAI")
        print("✅ Contoh komprehensif selesai!")
        print("📊 Semua data berhasil diambil (read-only operations)")
        
    except Exception as e:
        print(f"❌ Error umum: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
