import csv,io,json,os,shutil,sys,datetime,urllib.parse,urllib.request
from html import escape as E
R=os.path.dirname(os.path.abspath(__file__));C=json.load(open(R+"/config.json",encoding="utf-8"))
S=C["site_url"].rstrip("/");P=C.get("base","").rstrip("/");W=C["wa"];D=R+"/dist";AD=C["address"]
U=lambda p:P+p
wa=lambda t:f"https://wa.me/{W}?text="+urllib.parse.quote(t)
HM=["Merk","Model","Tahun","Hourmeter (jam)","Ukuran Bucket (m3)"]
CATS=[("excavator","Excavator","excavator-bekas",HM,"Cocok untuk galian, pematangan lahan, dan proyek infrastruktur."),
("mini-excavator","Mini Excavator","mini-excavator-bekas",HM,"Pas untuk area sempit, galian saluran, dan pekerjaan perumahan."),
("dump-truck","Dump Truck","dump-truck-bekas",["Merk","Model","Tahun","Kilometer","Kapasitas Bak (m3)"],"Untuk angkut tanah, batu, dan material proyek."),
("dozer","Dozer","dozer-bekas",["Merk","Model","Tahun","Hourmeter (jam)","Tipe Blade"],"Untuk land clearing, perataan, dan pekerjaan tanah berat."),
("vibro-roller","Vibro Roller","vibro-roller-bekas",["Merk","Model","Tahun","Hourmeter (jam)","Berat Operasi (ton)"],"Untuk pemadatan tanah dan lapisan jalan."),
("lainnya","Alat Berat Lainnya","alat-berat-bekas-lainnya",["Jenis Alat","Merk","Model","Tahun","Hourmeter (jam)","Spesifikasi"],"Termasuk backhoe, wheel loader, dan alat berat lainnya.")]
FAQ=[("Harganya berapa?","Harga menyesuaikan unit, kondisi, dan tujuan pengiriman. Hubungi admin untuk penawaran dan jadwal survey."),
("Apa bedanya as is dan rekondisi?","As is dijual sesuai kondisi saat ini. Rekondisi sudah melalui perbaikan, dan daftar perbaikannya dijelaskan per unit."),
("Boleh survey unit dulu?","Boleh. Atur jadwal lewat admin, lalu datang ke pool di Cimanggu, Bogor."),
("Bisa kirim ke luar Jawa?","Bisa. Pengiriman ke seluruh Indonesia memakai lowbed atau kapal. Biaya dan waktu tergantung tujuan."),
("Bagaimana cara pembayarannya?","Skema pembayaran disepakati bersama admin saat nego. Tanyakan opsi yang tersedia."),
("Apakah ada garansi?","Ketentuan berbeda tiap unit, terutama antara as is dan rekondisi. Admin menjelaskan sebelum deal."),
("Saya punya alat dan ingin menitipkan jual. Bisa?","Bisa. Hubungi admin lewat WhatsApp dengan info jenis alat, merk, tahun, dan lokasi.")]
def load(k,cols):
    u=C["sheets"].get(k,"").strip()
    if not u:
        r={c:"-" for c in cols};r.update({"Kode Unit":"CONTOH-01","Tahun":"2015","Kondisi":"Rekondisi","Status":"Tersedia","Catatan":"Data contoh. Isi link Google Sheets di config.json"});return [r]
    with urllib.request.urlopen(u,timeout=30) as f:t=f.read().decode("utf-8-sig")
    out=[]
    for r in csv.DictReader(io.StringIO(t)):
        r={(a or "").strip():(b or "").strip() for a,b in r.items()}
        if r.get("Tampilkan","").lower()=="ya" and r.get("Status","").lower()!="terjual" and r.get("Kode Unit"):
            out.append({c:r.get(c,"") for c in ["Kode Unit"]+cols+["Kondisi","Status","Catatan"]})
    return out
def img(s,n):
    f=f"/assets/img/{s}.jpg"
    return f'<img src="{U(f)}" alt="{E(n)} bekas dijual" loading="lazy">' if os.path.exists(R+f) else f'<div class="ph">Foto {E(n)} (contoh)</div>'
def page(path,title,desc,body,ld=()):
    lds="".join('<script type="application/ld+json">'+json.dumps(x,ensure_ascii=False)+'</script>' for x in ld)
    css,js,lg,hm=U("/assets/style.css"),U("/assets/app.js"),U("/assets/logo.jpg"),U("/")
    w1=wa("Halo admin Bandar Alat, saya mau tanya unit alat berat bekas.")
    return f"""<!doctype html><html lang="id"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)}</title><meta name="description" content="{E(desc)}"><link rel="canonical" href="{S+path}"><meta name="theme-color" content="#16171a"><meta property="og:type" content="website"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{S+path}"><meta property="og:image" content="{S}/assets/logo.jpg"><meta property="og:locale" content="id_ID"><link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E%F0%9F%9A%9C%3C/text%3E%3C/svg%3E"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap"><link rel="stylesheet" href="{css}">{lds}</head><body data-wa="{W}"><header class="hd"><div class="wrap"><a href="{hm}"><img src="{lg}" alt="Bandar Alat ID, penyedia alat berat terpercaya" width="640" height="349"></a><a class="btn wa" href="{w1}" target="_blank" rel="noopener">Chat WA</a></div></header><div class="hz"></div><main>{body}</main><footer><div class="wrap"><b>Bandar Alat</b><br>Jual alat berat bekas berkualitas. Pool di {E(AD)}, kirim ke seluruh Indonesia.<br>WhatsApp: 0881-5972-233<br><br>Ketersediaan unit dapat berubah sewaktu-waktu. Foto pada halaman ini hanya contoh.</div></footer><a class="btn wa fab" href="{w1}" target="_blank" rel="noopener">WhatsApp</a><script src="{js}" defer></script></body></html>"""
def faq(items):return "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q,a in items)
def faqld(items):return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in items]}
BIZ={"@context":"https://schema.org","@type":"LocalBusiness","name":"Bandar Alat","url":S,"image":S+"/assets/logo.jpg","telephone":"+"+W,"description":"Jual alat berat bekas, as is dan rekondisi, pool di Bogor, kirim seluruh Indonesia.","address":{"@type":"PostalAddress","streetAddress":"Cimanggu","addressLocality":"Bogor","addressRegion":"Jawa Barat","addressCountry":"ID"},"areaServed":"ID"}
def home():
    hw="".join(f'<span class="{"y" if w in("siap","kerja,") else ""}" style="--i:{i}">{E(w)}</span> ' for i,w in enumerate("Alat berat bekas siap kerja, kirim ke seluruh Indonesia".split()))
    cards="".join(f'<a class="cc rv" data-a="u" href="{U("/"+s+"/")}">{img(s,n)}<h3>{E(n)}</h3><span>Lihat unit tersedia →</span></a>' for k,n,s,c,x in CATS)
    why=[("Boleh survey dulu","Datang ke pool, lihat dan tes unitnya sebelum memutuskan."),("Data unit jelas","Tahun, hour meter, dan kondisi disampaikan terbuka."),("Foto & video lengkap","Video walk-around dikirim lewat WhatsApp."),("Kirim ke seluruh Indonesia","Via lowbed atau kapal sesuai lokasi proyek Anda.")]
    wy="".join(f'<div class="rv" data-a="{"l" if i%2==0 else "r"}"><i>0{i+1}</i><span><h3>{E(a)}</h3><p>{E(b)}</p></span></div>' for i,(a,b) in enumerate(why))
    st=[("Tanya unit","Chat admin atau isi form."),("Survey","Lihat unit di pool atau lewat video."),("Nego & deal","Sepakati harga dan pembayaran."),("Kirim","Unit dikirim ke lokasi Anda.")]
    tl="".join(f'<li class="rv" data-a="l"><b>{E(a)}</b>{E(b)}</li>' for a,b in st)
    opt="".join(f"<option>{E(n)}</option>" for k,n,s,c,x in CATS)
    b=f"""<div class="hero"><div class="wrap"><h1>{hw}</h1><p>Excavator, dump truck, dozer, vibro roller, dan alat lainnya dari berbagai merk. Dijual apa adanya atau sudah direkondisi. Boleh survey dulu di Bogor sebelum deal.</p><div class="cta"><a class="btn y" href="#form">Tanya harga &amp; survey</a><a class="btn o" href="{wa('Halo admin Bandar Alat, saya mau tanya unit alat berat bekas.')}" target="_blank" rel="noopener">Chat admin di WhatsApp</a></div><div class="fx"><b>Pool di Bogor</b><b>Kirim nasional</b><b>As is &amp; rekondisi</b><b>Video walk-around</b></div></div></div>
<section><div class="wrap"><h2 class="rv" data-a="u">Pilih jenis alat</h2><p class="mu">Foto hanya contoh. Klik jenis alat untuk melihat daftar unit yang sedang tersedia.</p><div class="sw">{cards}</div></div></section>
<section style="background:var(--card)"><div class="wrap sp"><div class="rv" data-a="l"><h2>As is atau rekondisi?</h2><p class="mu">Setiap unit diberi label yang jelas, jadi Anda tahu persis apa yang dibeli.</p></div><div class="rv" data-a="r"><div class="tabs" role="tablist"><button data-tab="a" aria-selected="true">As Is</button><button data-tab="r" aria-selected="false">Rekondisi</button></div><div class="pn" data-panel="a"><h3>Dijual apa adanya</h3><ul><li>Kondisi sesuai saat ini</li><li>Cocok untuk yang punya bengkel sendiri</li><li>Boleh survey dan cek langsung</li></ul></div><div class="pn" data-panel="r" hidden><h3>Sudah diperbaiki</h3><ul><li>Komponen penting dicek dan diperbaiki</li><li>Daftar perbaikan dijelaskan per unit</li><li>Lebih siap langsung kerja</li></ul></div></div></div></section>
<section class="dk"><div class="wrap"><h2>Kenapa beli lewat kami</h2><div class="wy">{wy}</div></div></section>
<section><div class="wrap"><h2>Pool di Bogor</h2><p class="mu">Lihat langsung kondisi unit sebelum memutuskan.</p><div class="pl"><iframe title="Peta lokasi pool" loading="lazy" src="https://www.google.com/maps?q=Cimanggu,+Bogor&amp;output=embed"></iframe><div class="inf"><b>Lokasi</b><p class="mu">{E(AD)}. Alamat lengkap dikirim admin.</p><b>Jam kunjung</b><p class="mu">{E(C['hours'])}</p><a class="btn wa" href="{wa('Halo admin, saya mau survey unit di pool Bogor.')}" target="_blank" rel="noopener">Atur jadwal survey</a></div></div></div></section>
<section style="background:var(--card)"><div class="wrap"><h2>Cara beli</h2><ol class="tl">{tl}</ol></div></section>
<section><div class="wrap"><h2>Pertanyaan umum</h2><div style="margin-top:18px">{faq(FAQ)}</div></div></section>
<section id="form" style="padding-top:0"><div class="wrap"><div class="fb"><h2>Tanya harga &amp; survey</h2><p style="color:#d3d5d9;margin:0">Isi singkat, admin membalas lewat WhatsApp.</p><form id="f" novalidate><div class="fg"><label>Nama *<input name="nama" autocomplete="name"></label><label>Nomor WhatsApp *<input name="wa" type="tel" inputmode="tel" autocomplete="tel" placeholder="08xxxxxxxxxx"></label></div><label>Alat yang diminati *<select name="unit"><option value="">Pilih jenis alat</option>{opt}</select></label><div class="fg"><label>Kota / lokasi proyek<input name="kota"></label><label>Kebutuhan<select name="butuh"><option>Belum tahu</option><option>As is</option><option>Rekondisi</option></select></label></div><label>Rencana beli<select name="rencana"><option>Masih lihat-lihat</option><option>Dalam 1 bulan</option><option>Segera</option></select></label><label>Catatan<textarea name="cat" placeholder="Merk, tahun, atau kebutuhan lain (opsional)"></textarea></label><p class="er" id="err" role="alert"></p><button class="btn wa" type="submit">Kirim lewat WhatsApp</button><p class="nt">Data Anda hanya dipakai untuk menghubungi Anda terkait unit yang ditanyakan.</p></form></div></div></section>"""
    return page("/","Jual Alat Berat Bekas Berkualitas Bogor, Kirim Seluruh Indonesia | Bandar Alat","Jual alat berat bekas: excavator, dump truck, dozer, vibro roller. Unit as is dan rekondisi, pool di Bogor, boleh survey, kirim ke seluruh Indonesia.",b,[BIZ,faqld(FAQ)])
def cat(k,n,s,cols,x):
    rows=load(k,cols);h1="Alat Berat Bekas Lainnya" if k=="lainnya" else f"Jual {n} Bekas"
    heads=["Kode Unit"]+cols+["Kondisi","Status","Catatan"]
    th="".join(f"<th>{E(c)}</th>" for c in heads)+"<th></th>"
    def cell(c,v):
        v=v or "-"
        return f'<span class="bd {v.lower().replace(" ","")}">{E(v)}</span>' if c in("Kondisi","Status") else E(v)
    tr=""
    for r in rows:
        nm=" ".join(r.get(c,"") for c in("Merk","Model","Tahun") if r.get(c,"") not in("","-"))
        y=r.get("Tahun","0") if r.get("Tahun","").isdigit() else "0"
        tds="".join(f'<td data-l="{E(c)}">{cell(c,r.get(c,""))}</td>' for c in heads)
        btn=wa(f"Halo admin Bandar Alat, saya mau tanya unit {r['Kode Unit']} ({nm}) kategori {n}. Mohon info harga dan jadwal survey.")
        tr+=f'<tr data-m="{E(r.get("Merk",""))}" data-y="{y}">{tds}<td><a class="btn wa sm" href="{btn}" target="_blank" rel="noopener">Tanya unit ini</a></td></tr>'
    merks=sorted({r.get("Merk","") for r in rows if r.get("Merk","") not in("","-")})
    mo="".join(f'<option value="{E(m)}">{E(m)}</option>' for m in merks)
    tab=f'<div class="tools"><select id="fm" aria-label="Filter merk"><option value="">Semua merk</option>{mo}</select><select id="fs" aria-label="Urutkan"><option value="">Urutan default</option><option value="new">Tahun terbaru</option><option value="old">Tahun terlama</option></select></div><table class="ut" id="ut"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>' if rows else f'<div class="em"><p>Unit sedang diperbarui. Tanya admin untuk info terbaru.</p><a class="btn wa" href="{wa("Halo admin, saya cari "+n.lower()+" bekas. Ada unit tersedia?")}" target="_blank" rel="noopener">Tanya admin</a></div>'
    qa=[(f"Bisakah {n.lower()} bekas disurvey dulu?","Bisa. Atur jadwal lewat admin, lalu datang ke pool di Cimanggu, Bogor."),(f"Apakah {n.lower()} bisa dikirim ke luar Jawa?","Bisa. Pengiriman ke seluruh Indonesia memakai lowbed atau kapal. Biaya dan waktu tergantung tujuan.")]
    lk="".join(f'<a href="{U("/"+s2+"/")}">{E(n2)}</a>' for k2,n2,s2,c2,x2 in CATS if k2!=k)
    b=f"""<div class="ch"><div class="wrap"><nav class="bc" aria-label="Breadcrumb"><a href="{U('/')}" style="color:#d3d5d9">Beranda</a> / {E(n)}</nav><h1>{h1}</h1><p>Daftar {E(n.lower())} bekas yang tersedia dari berbagai merk, dijual as is maupun rekondisi. {x} Survey langsung di pool Bogor dan kirim ke seluruh Indonesia. Harga dan jadwal survey lewat admin.</p></div></div><section><div class="wrap">{tab}<p class="mu" style="margin-top:14px">Tidak menemukan yang dicari? <a href="{wa('Halo admin, saya cari '+n.lower()+' bekas dengan kriteria tertentu.')}" target="_blank" rel="noopener">Tanya admin</a>, kami bantu carikan.</p></div></section><section style="background:var(--card);padding:40px 0"><div class="wrap"><h2>Pertanyaan seputar {E(n.lower())} bekas</h2><div style="margin-top:16px">{faq(qa)}</div><p style="margin-top:22px"><b>Jenis alat lainnya</b></p><div class="lk">{lk}</div></div></section>"""
    il={"@context":"https://schema.org","@type":"ItemList","name":h1,"itemListElement":[{"@type":"ListItem","position":i+1,"name":(" ".join(r.get(c,"") for c in("Merk","Model","Tahun") if r.get(c,"") not in("","-")) or r["Kode Unit"])+" ("+r["Kode Unit"]+")"} for i,r in enumerate(rows)]}
    bc={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Beranda","item":S+"/"},{"@type":"ListItem","position":2,"name":h1,"item":f"{S}/{s}/"}]}
    return page(f"/{s}/",f"{h1}, As Is & Rekondisi, Bogor | Bandar Alat",f"Daftar {n.lower()} bekas tersedia: merk, tahun, hourmeter, dan kondisi. As is dan rekondisi, pool di Bogor, kirim seluruh Indonesia.",b,[BIZ,il,bc,faqld(qa)])
def w(p,t):
    os.makedirs(os.path.dirname(D+p),exist_ok=True);open(D+p,"w",encoding="utf-8").write(t)
if os.path.exists(D):shutil.rmtree(D)
shutil.copytree(R+"/assets",D+"/assets");w("/index.html",home())
for c in CATS:w(f"/{c[2]}/index.html",cat(*c))
td=datetime.date.today().isoformat()
w("/sitemap.xml",'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f"<url><loc>{S}{p}</loc><lastmod>{td}</lastmod></url>" for p in ["/"]+[f"/{c[2]}/" for c in CATS])+"</urlset>")
w("/robots.txt",f"User-agent: *\nAllow: /\nSitemap: {S}/sitemap.xml\n")
if C.get("domain"):w("/CNAME",C["domain"])
print("OK",len(CATS)+1,"halaman")
