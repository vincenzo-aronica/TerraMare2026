from bs4 import BeautifulSoup
import json,re
from pathlib import Path
p=Path("index.html")
s=BeautifulSoup(p.read_text(encoding="utf-8"),"html.parser")
if s.title:s.title.string="TerraMare | Locazione stagionale e mensile a Maccarese 2027"
for m in s.select("meta[name=description],meta[property='og:description']"):
 m["content"]="TerraMare a Maccarese: casa arredata con giardino privato. Locazione stagionale dal 1 aprile al 30 ottobre 2027 o per uno o più mesi. Informazioni direttamente dalla proprietà."
for t in s.find_all("script",type="application/ld+json"):
 t.string=json.dumps({"@context":"https://schema.org","@type":"House","name":"TerraMare","description":"Casa arredata con giardino privato, disponibile per locazione stagionale o mensile, aprile-ottobre 2027.","address":{"@type":"PostalAddress","addressLocality":"Maccarese","addressCountry":"IT"}},ensure_ascii=False)
hero=s.select_one(".hero")
if hero:
 for selector,value in [(".hero-eyebrow","Maccarese — Stagione 2027"),("h1","La tua casa tra il verde di Maccarese e il mare di Fregene."),(".hero-sub","Locazione per l’intera stagione dal 1° aprile al 30 ottobre 2027 oppure per uno o più mesi. Contatta direttamente la proprietà.")]:
  x=hero.select_one(selector)
  if x:x.string=value
for a in s.select("nav a"):
 if a.get("href")=="#prezzi":a.string="Formule di locazione"
 if "prenota" in a.get_text(" ",strip=True).lower():a.string="Contatti";a["href"]="#contatti"
for a in s.select("a[href^='https://wa.me']"):
 a["href"]="mailto:vincenzo.aronica@gmail.com"
 if "whatsapp" in a.get_text(" ",strip=True).lower():a.string="Scrivi un’email"
section=s.select_one("#prezzi")
if section:
 new=BeautifulSoup("""<section id="prezzi" class="pricing"><div class="container"><div class="section-label">Formule di locazione</div><h2 class="section-title">Una casa, <em>due modi di viverla.</em></h2><p class="section-intro">TerraMare è disponibile dal <strong>1° aprile al 30 ottobre 2027</strong>. Priorità alla locazione dell’intero periodo, con possibilità di affitto per uno o più mesi secondo disponibilità.</p><div class="pricing-grid"><div class="price-card featured reveal"><div class="price-badge">Soluzione prioritaria</div><div class="price-period">Intera stagione</div><p>Dal 1° aprile al 30 ottobre 2027: la tua casa al mare per tutta la stagione.</p><a class="price-cta" href="#contatti">Richiedi informazioni</a></div><div class="price-card reveal"><div class="price-period">Uno o più mesi</div><p>Locazione mensile tra aprile e ottobre, secondo disponibilità e accordi.</p><a class="price-cta" href="#contatti">Contatta la proprietà</a></div></div><div class="deposit-note">Canone e condizioni sono comunicati direttamente dalla proprietà su richiesta.</div></div></section>""","html.parser").section
 section.replace_with(new)
for el in list(s.select(".service-card,.feature-pill")):
 if re.search(r"\b(?:spa|vasca|idromassaggio|piscina)\b",el.get_text(" ",strip=True),re.I):el.decompose()
for img in list(s.find_all("img")):
 if re.search(r"\b(?:spa|vasca|idromassaggio|piscina)\b",img.get("alt",""),re.I):
  parent=img.find_parent(class_=re.compile("gallery-item|outdoor-photo"))
  if parent:parent.decompose()
  else:img.decompose()
for node in list(s.find_all(string=True)):
 if node.parent and node.parent.name in ("script","style"):continue
 v=str(node)
 if re.search(r"\b(?:spa|vasca|idromassaggio|piscina)\b",v,re.I):
  par=node.parent
  if par and par.name in ("p","li","span") and not par.find(["p","li","div"]):par.decompose();continue
  v=re.sub(r"(?i)spa esterna riscaldata|vasca idromassaggio|spa riscaldata|spa esterna|vasca spa","giardino privato",v)
 for a,b in [("Estate & Autunno 2026","Stagione 2027"),("© 2026","© 2027"),("15 luglio al 30 ottobre","1° aprile al 30 ottobre 2027"),("15 luglio al 30 novembre","1° aprile al 30 ottobre 2027")]:v=v.replace(a,b)
 if node.parent and v!=str(node):node.replace_with(v)
conditions=s.select_one(".conditions")
if conditions:
 for n in list(conditions.select(".condition-item")):
  txt=n.get_text(" ",strip=True).lower()
  if any(w in txt for w in ("deposito cauzionale","spese di luce","caparra")):n.decompose()
  elif "15 luglio" in txt:
   n.clear();n.append("Disponibile dal 1° aprile al 30 ottobre 2027 per l’intera stagione o per uno o più mesi.")
faq=s.select_one(".faq")
if faq:
 for n in list(faq.select(".faq-item")):
  if re.search(r"deposito cauzionale|spese di luce|caparra|prezzi|settiman",n.get_text(" ",strip=True),re.I):n.decompose()
contact=s.select_one("#contatti")
if contact:
 h=contact.find("h2")
 if h:h.string="Contatta direttamente la proprietà"
 for n in contact.find_all("p"):
  if re.search(r"prezzi|caparra|settiman|disponibile da luglio",n.get_text(" ",strip=True),re.I):n.string="Per disponibilità e condizioni della locazione dal 1° aprile al 30 ottobre 2027, contatta direttamente la proprietà. Priorità all’intera stagione, oppure uno o più mesi."
 sel=contact.select_one("#period")
 if sel:
  sel.clear()
  for value,label in [("","Scegli la formula"),("stagione","Intera stagione: aprile–ottobre 2027"),("mensile","Uno o più mesi: aprile–ottobre 2027")]:
   op=s.new_tag("option",value=value);op.string=label;sel.append(op)
 for a in contact.select("a[href^='https://wa.me']"):a["href"]="mailto:vincenzo.aronica@gmail.com";a.string="Scrivi un’email"
for section in s.select(".final-cta"):
 for x in section.find_all("p"):x.string="Dal 1° aprile al 30 ottobre 2027: locazione dell’intera stagione o per uno o più mesi. Contatta la proprietà per disponibilità e condizioni."
for script in s.find_all("script"):
 body=script.string or script.get_text()
 if "function submitForm()" in body:
  a=body.find("function submitForm()")
  b=body.find("document.querySelectorAll('a[href^=\"#\"]')",a)
  if b>a:
   fn="""function submitForm(){
 const name=document.getElementById('name').value.trim();
 const phone=document.getElementById('phone').value.trim();
 const email=document.getElementById('email').value.trim();
 const period=document.getElementById('period').value;
 const guests=document.getElementById('guests').value;
 const message=document.getElementById('message').value.trim();
 if(!name||!email||!period){alert('Inserisci nome, email e formula di locazione.');return;}
 const body='Nome: '+name+'\\nTelefono: '+phone+'\\nEmail: '+email+'\\nFormula: '+period+'\\nOspiti: '+guests+'\\nNote e mesi richiesti: '+message;
 location.href='mailto:vincenzo.aronica@gmail.com?subject='+encodeURIComponent('Richiesta TerraMare 2027')+'&body='+encodeURIComponent(body);
}
"""
   script.string=body[:a]+fn+body[b:]
# Prevent accidental legacy text of 2026/weekly prices from appearing in visible sections
for node in list(s.find_all(string=True)):
 if node.parent and node.parent.name in ("script","style"):continue
 v=str(node)
 v=re.sub(r"\bspa\b","giardino",v,flags=re.I)
 v=re.sub(r"\b(?:vasca|idromassaggio|piscina)\b","giardino",v,flags=re.I)
 if "2026" in v:v=v.replace("2026","2027")
 if node.parent and v!=str(node):node.replace_with(v)
p.write_text("<!DOCTYPE html>\n"+str(s.html),encoding="utf-8")
text=s.get_text(" ",strip=True)
for bad in ("spa","vasca","piscina","2026","€"):
 if re.search(r"\b"+re.escape(bad)+r"\b",text,re.I):raise SystemExit("Still visible: "+bad)
print("TerraMare 2027 updated:",len(text),"visible characters")