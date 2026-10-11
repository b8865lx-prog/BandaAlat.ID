(()=>{const q=s=>[...document.querySelectorAll(s)],W=document.body.dataset.wa,wa=t=>`https://wa.me/${W}?text=${encodeURIComponent(t)}`;
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target)}}),{threshold:.12});
q(".rv").forEach(e=>io.observe(e));
q("[data-tab]").forEach(b=>b.onclick=()=>{q("[data-tab]").forEach(x=>x.setAttribute("aria-selected",x===b));q("[data-panel]").forEach(p=>p.hidden=p.dataset.panel!==b.dataset.tab)});
const tb=document.querySelector("#ut tbody");
if(tb){const o=[...tb.rows],fm=document.getElementById("fm"),fs=document.getElementById("fs");
const ap=()=>{const r=o.filter(x=>!fm.value||x.dataset.m===fm.value);if(fs.value)r.sort((a,b)=>fs.value==="new"?b.dataset.y-a.dataset.y:a.dataset.y-b.dataset.y);o.forEach(x=>x.hidden=true);r.forEach(x=>{x.hidden=false;tb.append(x)})};
fm.onchange=fs.onchange=ap}
const f=document.getElementById("f");
if(f)f.onsubmit=e=>{e.preventDefault();const v=n=>f.elements[n].value.trim(),er=document.getElementById("err");
if(!v("nama")||!v("wa")||!v("unit")){er.textContent="Isi nama, nomor WhatsApp, dan alat yang diminati.";return}
if(v("wa").replace(/\D/g,"").length<9){er.textContent="Nomor WhatsApp belum lengkap.";return}
er.textContent="";
open(wa(`Halo admin Bandar Alat, saya mau tanya harga & survey.\nNama: ${v("nama")}\nWA: ${v("wa")}\nAlat: ${v("unit")}\nLokasi proyek: ${v("kota")||"-"}\nKebutuhan: ${v("butuh")}\nRencana beli: ${v("rencana")}\nCatatan: ${v("cat")||"-"}`),"_blank","noopener")}})();
