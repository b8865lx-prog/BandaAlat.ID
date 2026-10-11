# Bandar Alat (bandaralat.id) - situs statis

## Pasang di GitHub Pages
1. Buat repo baru di GitHub (Private juga boleh), upload SEMUA isi folder ini (termasuk folder .github).
2. Repo > Settings > Pages > Build and deployment > Source: **GitHub Actions**.
3. Tab Actions > workflow "Deploy" > Run workflow. Tunggu hijau, situs hidup.
4. Domain: Settings > Pages > Custom domain: bandaralat.id, lalu arahkan DNS domain ke GitHub Pages. Aktifkan Enforce HTTPS.
   Sebelum domain siap, tes di alamat github.io dengan mengisi "base" di config.json, misal "/nama-repo".

## Sambungkan Google Sheets
1. Tiap tab unit: File > Bagikan > Publikasikan ke web > pilih tab > format CSV > Publikasikan > copy link.
2. Tempel link di config.json bagian "sheets" (satu per jenis alat). Kosong = tampil data contoh.
3. Jangan publikasikan tab Petunjuk dan Data Internal.
Situs dibangun ulang otomatis sekitar tiap 30 menit (GitHub kadang telat). Bisa juga manual lewat Run workflow.
Kalau Sheet gagal dibaca, build gagal dan situs lama tetap tampil.

## Yang bisa diedit
- config.json: nomor WA, alamat, jam kunjung, link Sheets.
- Foto: taruh file di assets/img/ dengan nama sesuai alamat halaman: excavator-bekas.jpg, mini-excavator-bekas.jpg, dump-truck-bekas.jpg, dozer-bekas.jpg, vibro-roller-bekas.jpg, alat-berat-bekas-lainnya.jpg (rasio 4:3).
- Logo: assets/logo.jpg.
