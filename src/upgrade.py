from pathlib import Path
from lxml import html,etree
from html import escape
import json,re,copy
ROOT=Path(__file__).resolve().parents[1];DIST=ROOT/'dist';A='/assets/kerala/'
DATA=json.loads((ROOT/'src/kerala-content.json').read_text());ART=DATA['articles'];GAL=DATA['gallery']
def fragment(s):return html.fragment_fromstring(s)
def img(file,alt,cls='',lazy=True):return f'<img src="{A+file}" alt="{escape(alt)}" class="{cls}" loading="{ "lazy" if lazy else "eager"}" decoding="async">'
def btn(text,href='/contact',attr=''):return f'<a class="k-button" href="{href}" {attr}><span>{text}</span><b aria-hidden="true">↗</b></a>'
def badge(t):return f'<span class="k-badge"><span aria-hidden="true">✳</span> {t} <span aria-hidden="true">✳</span></span>'
def heading(k,t,desc=''):return f'<div class="k-heading">{badge(k)}<h2 class="k-title" data-k-reveal>{t}</h2>{"<p>"+desc+"</p>" if desc else ""}</div>'
def blogcards(items):return '<div class="k-blog-grid">'+''.join(f'<a href="/blog/{a["slug"]}" class="k-blog-card" data-k-reveal><div class="k-image">{img(a["image"],a["alt"])}<span class="k-round-arrow">↗</span></div><div class="k-meta">{a["category"]}<span>Kerala journal</span></div><h3>{a["title"]}</h3></a>' for a in items)+'</div>'
def gallery():
 cards=''.join(f'<button type="button" class="k-gallery-card" data-gallery-index="{i}" aria-label="Open photograph: {escape(t)}"><div class="k-image">{img(f,t)}</div><span class="k-gallery-caption"><small>{i+1:02d} / VAIKOM</small><strong>{t}</strong><span aria-hidden="true">↗</span></span></button>' for i,(f,t,desc) in enumerate(GAL))
 return f'<section class="kerala-section k-gallery" id="village-gallery"><div class="k-container">{heading("From our village waterways","A little closer to<br><em>life in Vaikom.</em>","Eight moments from our own village backwater experience. Boats, local hands and the people along the way.")}<div class="k-gallery-window"><div class="k-gallery-track">{cards}</div></div><div class="k-gallery-nav"><span>Scroll through village life</span><div><button data-gallery-shift="-1" aria-label="Previous photographs">←</button><button data-gallery-shift="1" aria-label="Next photographs">→</button></div></div></div></section>'
def cabsection(full=False):
 rows=''.join(f'<button class="k-route" data-cab-route="{escape(r)}"><span><strong>{r}</strong><small>{d}</small></span><b aria-hidden="true">↗</b></button>' for r,d in DATA['routes'])
 vehicles=[('maruti_dzire_sedan.png','Maruti Dzire','Sedan · Up to 4 guests'),('toyota_innova_suv.png','Toyota Innova','SUV · Up to 6 guests'),('innova_crysta_premium.png','Innova Crysta','Premium SUV · Family journeys')]
 fleet=''.join(f'<button class="k-fleet-card" data-cab-vehicle="{n}">{img(f,n)}<small>{d}</small><h3>{n}</h3><span>Enquire about this ride ↗</span></button>' for f,n,d in vehicles)
 return f'<section class="kerala-section k-cabs" id="cab-facilities"><div class="k-container"><div class="k-cab-heading">{heading("Arafath Cabs & Transfers","Kerala, at<br><em>your own pace.</em>","From an airport pickup to a journey into the hills, tell us your route and we’ll help arrange the ride.")}<span class="k-stamp k-stamp-ticket" data-k-sticker>KOCHI<br><em>and beyond</em><small>YOUR ROUTE. YOUR RIDE.</small></span></div><div class="k-cab-layout"><div class="k-cab-photo">{img("fort-kochi.webp","Fishing nets at the Fort Kochi waterfront")}<div><span>YOUR JOURNEY STARTS HERE</span><h3>Local knowledge.<br>A familiar welcome.</h3></div></div><div class="k-routes">{rows}<p>Need a different route or extra stops? <button data-cab-route="Custom Kerala route">Ask about a custom journey ↗</button></p></div></div><div class="k-fleet">{fleet}</div><p class="k-footnote">Send your pickup, destination and travel date. The team will confirm vehicle availability and journey details directly.</p></div></section>'
def travelblog():return f'<section class="kerala-section k-journal" id="kerala-journal"><div class="k-container"><div class="k-heading-row">{heading("The Kerala journal","Stories from<br><em>God’s own country.</em>")}{btn("Explore the journal","/blog")}</div>{blogcards([ART[1],ART[2],ART[4]])}</div></section>'
def video():return f'<button class="k-video" type="button" data-kerala-video aria-label="Watch Kerala Tourism’s Alappuzha backwater film">{img("alappuzha.webp","Alappuzha backwaters in Kerala")}<span class="k-video-play">▶</span><span class="k-video-caption"><small>KERALA TOURISM FILM</small>Life on the backwaters</span></button>'
def textset(e,t):
 for c in list(e):e.remove(c)
 e.text=t
# Typography-only travel stamps: new local designs in reference pastel palette.
stamps=[('kerala-stamp.svg','#daf0c7','KERALA','TAKE IT SLOW'),('vaikom-stamp.svg','#ffdce7','VAIKOM','VILLAGE DAYS'),('boat-stamp.svg','#fff6c7','BACKWATERS','BOATS • CRAFTS • LUNCH'),('kochi-stamp.svg','#e4dff6','FORT KOCHI','YOUR JOURNEY STARTS HERE')]
for i,(f,col,t,sub) in enumerate(stamps):
 shape='<rect x="8" y="8" width="284" height="184" rx="90"/>' if i%2==0 else '<path d="M10 10 H290 V50 Q265 65 290 80 V120 Q265 135 290 150 V190 H10 V150 Q35 135 10 120 V80 Q35 65 10 50 Z"/>'
 (DIST/'assets'/f).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200"><g fill="{col}" stroke="#1a1a17" stroke-width="2">{shape}</g><rect x="24" y="25" width="252" height="150" rx="65" fill="none" stroke="#1a1a17" stroke-dasharray="4 5"/><text x="150" y="73" text-anchor="middle" fill="#1a1a17" font-family="Georgia,serif" font-size="24">✦</text><text x="150" y="111" text-anchor="middle" fill="#1a1a17" font-family="Georgia,serif" font-weight="bold" font-style="italic" font-size="{30 if len(t)<10 else 25}">{t}</text><text x="150" y="142" text-anchor="middle" fill="#1a1a17" font-family="Arial,sans-serif" font-size="10" letter-spacing="2">{sub}</text></svg>')
# Preserve a clean reference of customized layout for reproducible content edits.
BASE=ROOT/'src/layouts';BASE.mkdir(exist_ok=True)
for p in [DIST/x for x in ['index.html','about/index.html','tours/index.html','contact/index.html','location/index.html','traveler-stories/index.html','blog/index.html','tour/index.html','journal/index.html']]:
 rel=p.relative_to(DIST);target=BASE/rel
 if not target.exists():target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(p.read_bytes())

def choose_image(e,route,index):
 ancestors=list(e.iterancestors());a=next((x for x in ancestors if x.tag=='a'),None);text=a.text_content().lower() if a is not None else ''
 section=next((x for x in ancestors if x.tag=='section'),None);name=section.get('data-framer-name','') if section is not None else ''
 alt=e.get('alt','').lower()
 if 'sadya' in text or 'lunch' in text:return 'sadya.webp','Traditional Kerala banana-leaf meal'
 if 'coir' in text:return 'vaikom-32-2.jpg','Coir rope making in Vaikom village'
 if 'weav' in text or 'craft' in text:return 'vaikom-31-2.jpg','Local weaving demonstration during the Vaikom tour'
 if 'pickup' in text or 'fort kochi' in text:return 'fort-kochi.webp','Fort Kochi waterfront in Kerala'
 if 'munnar' in text:return 'munnar.webp','Green Munnar hill landscape in Kerala'
 if 'bamboo' in text:return 'vaikom-31-1.jpg','Traditional covered boat on Vaikom village backwaters'
 if 'canal' in text:return 'vaikom-31.jpg','Green village canal in Vaikom'
 if 'village life' in text:return 'vaikom-31-3.jpg','Village craft experience in Vaikom'
 if 'boat rides' in text or 'backwater' in text:return 'vaikom-31.jpg','Village boat on the Vaikom backwaters'
 if name=='Hero' or alt=='bg image':return ('vaikom-31.jpg','A boat on Vaikom’s green village waterway') if route=='' else ('alappuzha.webp','Palm-lined Kerala backwaters')
 if alt=='avatar':return 'vaikom-30.jpg','Guests on the Vaikom village boat'
 if alt=='step image':return 'vaikom-32.jpg','Village craft demonstration in Vaikom'
 if 'flag' in alt or alt=='falg':return ['vaikom-31.jpg','fort-kochi.webp','munnar.webp','alappuzha.webp','athirappilly.webp'][index%5],'Kerala destination'
 if route=='tour':return 'vaikom-31-1.jpg','Vaikom village backwater boat'
 files=['vaikom-31.jpg','fort-kochi.webp','munnar.webp','alappuzha.webp','vaikom-31-2.jpg','sadya.webp','athirappilly.webp','vaikom-30.jpg']
 return files[index%len(files)],'Kerala scenery and village experiences'

for p in BASE.rglob('index.html'):
 rel=p.relative_to(BASE);route=str(rel.parent).replace('.','');d=html.fromstring(p.read_text())
 for i,e in enumerate(d.xpath('//img')):
  src=e.get('src','');alt=e.get('alt','')
  if src.startswith('/assets/logo'):continue
  if alt=='Cloud Image':continue # neutral cloud overlays are part of the reference composition
  if alt=='Vector' or alt=='Globe':
   e.set('src','/assets/'+stamps[i%4][0]);e.set('alt','Kerala travel stamp');e.attrib.pop('srcset',None);e.set('data-k-sticker','')
  elif '.svg' in src and alt in ['Icon','Arrow','Back Arrow','Next Arrow','Rating Star Image','Social Icon']:continue
  else:
   file,desc=choose_image(e,route,i);e.set('src',A+file);e.set('alt',desc);e.attrib.pop('srcset',None);e.attrib.pop('sizes',None)
   if 'Flag' in alt or alt=='Falg':e.set('style',e.get('style','')+';border-radius:50%;object-fit:cover')
 # All template video footage is removed, including background video variants.
 for v in d.xpath('//video'):
  section=next((a for a in v.iterancestors() if a.tag=='section'),None)
  if section is not None and section.get('data-framer-name')=='Step':replacement=fragment(video())
  else:replacement=fragment(img('vaikom-31.jpg','Quiet village waterway in Vaikom','k-video-replacement'))
  v.getparent().replace(v,replacement)
 # Clear hidden foreign template metadata, not just visible copy.
 for e in d.iter():
  if not isinstance(e.tag,str):continue
  for k in list(e.attrib):
   if k.startswith('data-framer') and k not in ['data-framer-name','data-framer-appear-id','data-framer-hydrate-v2','data-framer-component-type']:continue
   if k in ['aria-label','title'] and re.search('Japan|Kyoto|Morocco|Maldives|Iceland|Tanzania|China|Travelio',e.attrib[k]):e.set(k,'Kerala travel experience')
 # Link destinations and journals to content whose image really matches the title.
 for e in d.xpath('//a[@href="/journal"]'):
  h=e.xpath('.//h2|.//h3');t=h[0].text_content() if h else ''
  a=ART[5] if 'Craft' in t else ART[0];e.set('href','/blog/'+a['slug'])
  if h:textset(h[0],a['title'])
  for im in e.xpath('.//img'):
   if '.svg' not in im.get('src',''):im.set('src',A+a['image']);im.set('alt',a['alt'])
 # Keep client branding / real travel terms in navigation.
 for menu in d.xpath('//*[@class="menu-links"]'):
  menu.append(fragment('<a href="/#village-gallery">Village Gallery</a>'));menu.append(fragment('<a href="/cabs">Cabs & Transfers</a>'))
 for e in d.xpath('//head'):
  e.append(html.Element('link',rel='stylesheet',href='/kerala.css'))
 for e in d.xpath('//script[@src="/client.js"]'):
  # Load local GSAP libraries before the Kerala motion code.
  body=e.getparent()
  for src in ['/assets/vendor/gsap.min.js','/assets/vendor/ScrollTrigger.min.js','/kerala.js']:
   body.append(html.Element('script',src=src,defer=''))
 # Remove leftover international themed testimonial cards instead of fictional identities.
 for sec in d.xpath('//section[@data-framer-name="Testimonials"]'):
  new=fragment(f'<section class="kerala-section k-stories" id="guest-stories"><div class="k-container">{heading("Moments from the tour","The people make<br><em>the memories.</em>","A glimpse of our village experience, from the boat to the craft workshop.")}<div class="k-story-grid"><figure data-k-reveal>{img("vaikom-30.jpg","Guests aboard the covered Vaikom village boat")}<figcaption>A shared journey on the water.</figcaption></figure><figure data-k-reveal>{img("vaikom-31-2.jpg","Visitors learning about village weaving")}<figcaption>A closer connection to village life.</figcaption></figure><div class="k-story-note" data-k-reveal><span class="k-stamp" data-k-sticker>VAIKOM<br><em>good company</em></span><p>Boat rides, local crafts and Kerala hospitality — the moments that fill a village day.</p>{btn("See the village gallery","/#village-gallery")}</div></div></div></section>')
  sec.getparent().replace(sec,new)
 if route=='':
  h1=d.xpath('//h1');words=['Kerala','Beyond','the','Ordinary']
  for e,t in zip(h1,words):
   em=e.find('em');textset(em if em is not None else e,t)
  # Main journal retains its location in the reference; imagery and content are replaced together.
  for old in d.xpath('//section[@data-framer-name="Blog"]'):old.getparent().replace(old,fragment(travelblog()))
  main=d.xpath('//main')[0];step=d.xpath('//section[@data-framer-name="Step"]')[0];main.insert(main.index(step)+1,fragment(gallery()))
  journal=d.xpath('//*[@id="kerala-journal"]')[0];main.insert(main.index(journal),fragment(cabsection()))
  for el in d.xpath('//section[@data-framer-name="CTA"]'):
   hs=el.xpath('.//h2');words=['Your','Next','Kerala','','','Memory','Starts','Here']
   for q,t in zip(hs,words):textset(q,t)
   for q in el.xpath('.//img[@alt="Kerala travel stamp"]')[:1]:q.set('src','/assets/kerala-stamp.svg')
 # New lightbox + cab dialog shared across the original routes.
 d.find('body').append(fragment('<div id="kerala-dialogs"></div>'))
 out=DIST/rel;out.write_text('<!doctype html>\n'+html.tostring(d,encoding='unicode'))

# Complete destination-specific journal pages, using the site's existing shared header and footer.
base=html.fromstring((DIST/'blog/index.html').read_text())
def savepage(path,content,title):
 d=copy.deepcopy(base);m=d.xpath('//main')[0]
 for c in list(m):m.remove(c)
 m.attrib.clear();m.set('class','k-custom-main')
 for child in html.fragments_fromstring(content):m.append(child)
 for e in d.xpath('//title'):e.text=title+' — Arafath Tours'
 for e in d.xpath('//meta[@name="description"]'):e.set('content',title+' | Kerala journeys, village experiences and local transfers with Arafath Tours.')
 out=DIST/path/'index.html';out.parent.mkdir(parents=True,exist_ok=True);out.write_text('<!doctype html>\n'+html.tostring(d,encoding='unicode'))
for a in ART:
 sections=''.join(f'<section><h2>{h}</h2><p>{p}</p></section>' for h,p in a['sections'])
 content=f'<article class="k-article"><header class="k-container k-page-heading">{badge(a["category"])}<h1 class="k-title" data-k-reveal>{a["title"]}</h1><p>{a["intro"]}</p></header><figure class="k-article-image">{img(a["image"],a["alt"],lazy=False)}<figcaption>{a["alt"]}</figcaption></figure><div class="k-article-body">{sections}<p class="k-source">Destination information & photograph: <a href="{a["source"]}" target="_blank" rel="noopener">{ "Arafath Tours" if "vercel" in a["source"] else "Kerala Tourism"}</a>.</p>{btn("Plan your Kerala journey","/contact")}</div><div class="kerala-section k-container">{heading("Keep exploring","More of <em>Kerala.</em>")}{blogcards([x for x in ART if x!=a][:3])}</div></article>'
 savepage(Path('blog')/a['slug'],content,a['title'])
savepage(Path('blog'),f'<section class="kerala-section"><div class="k-container k-page-heading">{heading("The Kerala journal","A place for<br><em>curious travellers.</em>","Village waterways, coastal heritage, hill country and the small details of a Kerala journey.")}{blogcards(ART)}</div></section>','The Kerala Journal')
savepage(Path('journal'),f'<section class="kerala-section"><div class="k-container k-page-heading">{heading("The Kerala journal","Your next <em>chapter.</em>")}{blogcards(ART)}</div></section>','Kerala Travel Stories')
savepage(Path('cabs'),cabsection(True),'Kerala Cabs & Transfers')
# Locations have proper names and matching photographs; no relabelled foreign destination pages.
locs=[('Vaikom','vaikom-31.jpg','Village waterways, boat rides and local craft experiences.','/tour'),('Fort Kochi','fort-kochi.webp','Fishing nets, waterfront walks and Kerala’s coastal heritage.','/blog/fort-kochi-waterfront'),('Munnar','munnar.webp','Green hills and a quieter inland escape.','/blog/munnar-hill-escape'),('Alappuzha','alappuzha.webp','Palm-lined backwaters and waterside village life.','/blog/alappuzha-backwater-guide'),('Athirappilly','athirappilly.webp','A waterfall landscape at the edge of the Sholayar forest ranges.','/blog/athirappilly-waterfalls')]
cards=''.join(f'<a class="k-destination" href="{u}" data-k-reveal>{img(f,n+", Kerala")}<div><h2>{n}</h2><p>{desc}</p><span>Explore this place ↗</span></div></a>' for n,f,desc,u in locs)
savepage(Path('location'),f'<section class="kerala-section"><div class="k-container k-page-heading">{heading("Only Kerala","Different landscapes.<br><em>One beautiful Kerala.</em>","Start in Vaikom, then discover the coast, hills and waterfall country at your own pace.")}<div class="k-location-grid">{cards}</div></div></section>','Places in Kerala')
savepage(Path('traveler-stories'),gallery(),'Vaikom Village Gallery')
savepage(Path('about'),f'<section class="kerala-section"><div class="k-container k-page-heading">{heading("Arafath Tours · Fort Kochi","A local welcome.<br><em>A slower journey.</em>","Arafath Rent a Bike Tours & Travels brings together a full-day Vaikom village experience and cab services across Kerala.")}<div class="k-about-layout">{img("vaikom-30.jpg","Guests on a Vaikom backwater boat")}<div><h2>Waterways. Village hands. Kerala hospitality.</h2><p>Our daily Vaikom programme pairs a three-hour bamboo boat ride with traditional craft visits, Kerala lunch and a 45-minute small canal ride.</p><p>Hotel pickup is between 8:30–8:45 AM, with drop-off between 4:00–4:30 PM. The full-day tour is ₹1,900 per person.</p>{btn("Discover the tour","/tour")}<p>For airport transfers, local sightseeing and outstation rides, our team can help arrange a vehicle and route.</p>{btn("Cabs & transfers","/cabs")}</div></div></div></section>'+gallery(),'About Arafath Tours')
(DIST/'kerala-content.json').write_text(json.dumps(DATA,ensure_ascii=False))
print('Kerala upgrade: existing layouts customized, six full articles, gallery, cabs and source-matched locations created.')
