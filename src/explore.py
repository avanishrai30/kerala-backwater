"""Explore Kerala: data-backed markup shared by the page generator and atlas."""
import json, html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPOTS = [
 ('bekal','Bekal','Coast',12.392,75.034,'Where the fort meets the sea.','Fort walls · Arabian Sea · Coastal walks'),
 ('kannur','Kannur','Culture',11.874,75.370,'A coast alive with stories and ritual.','Theyyam traditions · St. Angelo Fort · Beaches'),
 ('wayanad','Wayanad','Mountains',11.610,76.083,'Forest roads. Ancient stories. Cooler air.','Edakkal Caves · Banasura Sagar · Green hills'),
 ('kozhikode','Kozhikode','Culture',11.259,75.780,'Follow the flavour of the Malabar coast.','Beach sunsets · Malabar food · Heritage streets'),
 ('nilambur','Nilambur','Wild',11.279,76.225,'A green pause beside the Chaliyar.','Teak Museum · Forest country · River landscapes'),
 ('silent-valley','Silent Valley','Wild',11.093,76.427,'Step closer to the rainforest.','Evergreen forest · Guided nature visits · Kunthi River'),
 ('palakkad','Palakkad','Culture',10.787,76.655,'A gateway to another side of Kerala.','Palakkad Fort · Malampuzha · Paddy landscapes'),
 ('guruvayur','Guruvayur','Culture',10.595,76.041,'A temple town with its own rhythm.','Temple heritage · Living traditions · Local streets'),
 ('thrissur','Thrissur','Culture',10.527,76.214,'Find Kerala’s cultural heartbeat.','Vadakkunnathan Temple · Art · Festival traditions'),
 ('athirappilly','Athirappilly','Wild',10.286,76.570,'Let the sound of falling water lead you.','Waterfall viewpoints · Chalakudy River · Forest scenery','athirappilly.webp'),
 ('cherai','Cherai','Coast',10.142,76.178,'A little sand between bigger adventures.','Long beach · Coastal villages · Sunset walks'),
 ('fort-kochi','Fort Kochi','Culture',9.966,76.242,'Every street has another story.','Chinese fishing nets · Heritage lanes · Art cafés','fort-kochi.webp'),
 ('munnar','Munnar','Mountains',10.089,77.060,'Find yourself somewhere above the ordinary.','Tea country · Eravikulam · Mountain viewpoints','munnar.webp'),
 ('vattavada','Vattavada','Mountains',10.182,77.256,'Take the quiet road beyond Munnar.','Terraced farms · Cool valleys · Village scenery'),
 ('vaikom','Vaikom','Backwaters',9.748,76.396,'Our favourite way to slow down.','Village canals · Local crafts · Kerala lunch','vaikom-31-1.jpg'),
 ('kumarakom','Kumarakom','Backwaters',9.617,76.430,'Life unfolds along the water.','Vembanad Lake · Village experiences · Bird sanctuary'),
 ('vagamon','Vagamon','Mountains',9.686,76.905,'Long views. Deep breaths. No hurry.','Rolling meadows · Pine groves · Hill roads'),
 ('thekkady','Thekkady','Wild',9.603,77.161,'Trade the city noise for forest sounds.','Periyar landscape · Nature programmes · Spice country'),
 ('alappuzha','Alappuzha','Backwaters',9.499,76.339,'A thousand little reasons to drift.','Backwater cruises · Kuttanad · Canal life','alappuzha.webp'),
 ('gavi','Gavi','Wild',9.438,77.165,'Go a little deeper into the green.','Forest landscapes · Guided outings · Quiet water'),
 ('kollam','Kollam','Backwaters',8.894,76.615,'A softer pace on Ashtamudi.','Ashtamudi Lake · Munroe Island · Backwater life'),
 ('varkala','Varkala','Coast',8.737,76.716,'Clifftop days. Saltwater evenings.','Cliff walks · Papanasam Beach · Coastal cafés'),
 ('ponmudi','Ponmudi','Mountains',8.760,77.117,'Follow the bends into the clouds.','Hill viewpoints · Winding roads · Green valleys'),
 ('thiruvananthapuram','Thiruvananthapuram','Culture',8.524,76.937,'A capital with a creative soul.','Napier Museum · Temple heritage · City culture'),
 ('kovalam','Kovalam','Coast',8.399,76.978,'Stay for one more sunset.','Lighthouse Beach · Seaside walks · Sandy coves'),
 ('poovar','Poovar','Backwaters',8.317,77.070,'Where the waterways reach the coast.','Estuary scenery · Boat outings · Golden sand'),
]
DESTINATIONS = [dict(id=s[0],name=s[1],category=s[2],lat=s[3],lon=s[4],line=s[5],highlights=s[6].split(' · '),image='/assets/kerala/'+s[7] if len(s)>7 else None) for s in SPOTS]
CATEGORIES = ['All places','Mountains','Backwaters','Coast','Culture','Wild']

def render_explore():
 (ROOT/'dist/assets/atlas/destinations.json').write_text(json.dumps(DESTINATIONS,ensure_ascii=False,separators=(',',':')))
 filters=''.join(f'<button type="button" data-atlas-filter="{c}" aria-pressed="{str(i==0).lower()}">{c}</button>' for i,c in enumerate(CATEGORIES))
 spots=''.join(f'''<article class="atlas-place" data-place-id="{d['id']}" data-place-category="{d['category']}"><span class="place-no">{i+1:02}</span><div><span class="place-kind">{d['category']}</span><h3>{d['name']}</h3><p>{d['line']}</p><a href="#kerala-atlas" data-select-place="{d['id']}">Find on the atlas <span aria-hidden="true">↗</span></a></div></article>''' for i,d in enumerate(DESTINATIONS))
 pins=''.join(f'<button class="atlas-pin" type="button" data-pin="{d["id"]}" aria-label="Explore {d["name"]}" aria-pressed="false" hidden><span class="pin-dot"></span><span class="pin-name">{d["name"]}</span></button>' for d in DESTINATIONS)
 return '''<link rel="stylesheet" href="/explore.css"><script type="module" src="/explore.js"></script>
 <section class="atlas-shell" id="kerala-atlas" aria-labelledby="atlas-heading">
  <div class="atlas-kicker"><span>ARAFATH FIELD NOTES &nbsp; / &nbsp; 01</span><span>INDIA’S SOUTHWEST COAST</span></div>
  <div class="atlas-heading"><div><span class="atlas-overline">A DIFFERENT PERSPECTIVE</span><h1 id="atlas-heading">A whole world.<br><em>One Kerala.</em></h1><p>From cloud country to quiet canals.<br>Follow a pin. Find your kind of escape.</p></div><a href="#places" class="atlas-index-link">Explore all 26 places <span>↓</span></a></div>
  <div class="atlas-layout">
   <aside class="atlas-story" aria-label="Selected destination">
    <div class="story-photo"><img id="atlas-photo" src="/assets/kerala/munnar.webp" alt="Tea-covered hills in Munnar" width="520" height="350"><span id="story-photo-caption">MUNNAR, KERALA</span></div>
    <div class="story-copy"><div class="story-meta"><span id="atlas-category">Mountains</span><span id="atlas-number">13 / 26</span></div><h2 id="atlas-name" aria-live="polite" aria-atomic="true">Munnar</h2><p id="atlas-line">Find yourself somewhere above the ordinary.</p><ul id="atlas-highlights"><li>Tea country</li><li>Eravikulam</li><li>Mountain viewpoints</li></ul><a id="atlas-enquire" class="atlas-enquire" href="https://wa.me/919947478328?text=Hello%20Arafath%2C%20help%20me%20plan%20a%20Munnar%20journey.">Take me here <span>↗</span></a><div class="story-navigation"><button type="button" id="atlas-prev" aria-label="Previous destination">←</button><span id="atlas-coordinates">10.089° N &nbsp; 77.060° E</span><button type="button" id="atlas-next" aria-label="Next destination">→</button></div></div>
   </aside>
   <div class="atlas-world" id="atlas-world" data-lenis-prevent>
    <div class="world-backdrop" aria-hidden="true"><span>KERALA</span></div>
    <div id="atlas-stage" role="region" aria-label="Interactive three-dimensional Kerala atlas" tabindex="0" aria-describedby="atlas-help"><div class="atlas-static"><img src="/assets/kerala/munnar.webp" alt="Munnar’s green mountain landscape"><span>Discover Kerala through the places below.</span></div></div>
    <div id="atlas-labels" aria-label="Destination map pins">'''+pins+'''</div>
    <div class="atlas-view-controls" aria-label="Map views"><button id="atlas-reset" type="button" disabled>↺ <span>Full Kerala</span></button><button id="atlas-angle" type="button" aria-pressed="false" disabled>◇ <span>Top view</span></button></div>
    <div class="atlas-compass" aria-hidden="true"><span>N</span><i>↑</i><small>ARABIAN SEA</small></div>
    <div class="atlas-playbar"><button id="atlas-tour" type="button" aria-pressed="false" disabled><span id="tour-icon">▶</span><span id="tour-label">Take the scenic route</span></button><button id="atlas-motion" type="button" aria-pressed="false" disabled>Pause motion</button><div class="tour-progress" aria-hidden="true"><span></span></div></div>
    <div class="atlas-zoom" aria-label="Map zoom"><button id="atlas-zoom-in" type="button" aria-label="Zoom in" disabled>+</button><button id="atlas-zoom-out" type="button" aria-label="Zoom out" disabled>−</button></div>
    <p id="atlas-help" class="atlas-help">Choose a place below to explore.</p>
    <p id="atlas-status" class="sr-only" role="status"></p>
   </div>
  </div>
  <div class="atlas-footnote"><span><i></i> 26 PLACES. YOUR OWN WAY THROUGH.</span><details><summary>About this atlas ↗</summary><p>Geographic boundary from <a href="https://github.com/geohacker/kerala" target="_blank" rel="noopener">DataMeet / geohacker</a> (<a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener">CC BY 4.0</a>), simplified for this atlas. This is an illustrated landscape: relief is exaggerated and pins are approximate destination locations. Flight paths are visual connections, not driving routes. Explore destination information with <a href="https://www.keralatourism.org/destination/" target="_blank" rel="noopener">Kerala Tourism</a>. Forest visits and some activities require advance arrangements.</p></details></div>
 </section>
 <section class="atlas-directory wrap" id="places" aria-labelledby="places-heading">
  <div class="directory-heading"><div><span class="atlas-overline">LET CURIOSITY CHOOSE</span><h2 id="places-heading">Where will Kerala<br><em>take you?</em></h2></div><p>High in the hills or close to the water.<br>There’s a place for every pace.</p></div>
  <div class="directory-tools"><div class="atlas-filters" role="group" aria-label="Filter destinations">'''+filters+'''</div><label class="atlas-search"><span class="sr-only">Search destinations</span><input type="search" id="atlas-search" placeholder="Find your place…" autocomplete="off"><span aria-hidden="true">⌕</span></label></div>
  <div class="directory-count" role="status" id="atlas-count">26 places to discover</div><div class="atlas-place-grid">'''+spots+'''</div><p id="atlas-empty" hidden>No places match. Try another name or choose All places.</p>
 </section>
 <section class="atlas-chapters wrap" aria-labelledby="chapters-heading"><div class="chapter-heading"><span class="atlas-overline">SAME KERALA. DIFFERENT FEELING.</span><h2 id="chapters-heading">Find your <em>element.</em></h2></div><div class="chapter-grid">
 <a class="atlas-chapter" href="#kerala-atlas" data-select-place="munnar"><img src="/assets/kerala/munnar.webp" alt="Green tea-covered hills of Munnar" loading="lazy" width="720" height="960"><span class="chapter-no">01 / THE HIGHLANDS</span><div><h3>Above the<br><em>everyday.</em></h3><span>Munnar & the mountain country ↗</span></div></a>
 <a class="atlas-chapter" href="#kerala-atlas" data-select-place="alappuzha"><img src="/assets/kerala/alappuzha.webp" alt="Palm-lined Alappuzha backwaters" loading="lazy" width="720" height="960"><span class="chapter-no">02 / THE BACKWATERS</span><div><h3>Time moves<br><em>differently.</em></h3><span>Alappuzha & the waterways ↗</span></div></a>
 <a class="atlas-chapter" href="#kerala-atlas" data-select-place="fort-kochi"><img src="/assets/kerala/fort-kochi.webp" alt="Fort Kochi’s Chinese fishing nets" loading="lazy" width="720" height="960"><span class="chapter-no">03 / THE COAST</span><div><h3>A shore full<br>of <em>stories.</em></h3><span>Fort Kochi & the coastal life ↗</span></div></a>
 </div></section>'''
