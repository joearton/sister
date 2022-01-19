# Sister
Simple Sister API client (Dikti/Kemdikbudristek) using Python.

## Sister Credential Preparation
1. Get your developer credential from **akses.ristekdikti.go.id**.
2. In there, create new user with role "Developer".
3. Open your sister, and syncronize to get new "developer user".
4. Login to your sister using developer credential.
5. Copy username, password, and id_pengguna, and put it on "config.json".

## Config Preparation
1. Copy/rename "config.template.json" to "config.json" in config folder.
2. Set your Sister URL with schema, example: https://sister.umko.ac.id.
3. Set credential username, password, and id_pengguna of your account.

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