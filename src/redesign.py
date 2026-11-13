from pathlib import Path
import json,re,html
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'dist';data=json.loads((ROOT/'src/kerala-content.json').read_text());esc=html.escape
A='/assets/kerala/';WA='https://wa.me/919947478328'
def img(file,alt,cls=''):
 return f'<img class="{cls}" src="{A+file}" alt="{esc(alt)}" loading="lazy" decoding="async">'
def btn(label,url='/contact',cls=''):
 return f'<a class="button {cls}" href="{url}">{label}<span aria-hidden="true">↗</span></a>'
def eyebrow(s):return f'<span class="eyebrow"><span aria-hidden="true">✳</span> {s} <span aria-hidden="true">✳</span></span>'
def heading(k,t,p='',center=False):return f'<div class="section-heading {"center" if center else ""}" data-reveal>{eyebrow(k)}<h2>{t}</h2>{f"<p>{p}</p>" if p else ""}</div>'
nav='''<a class="skip" href="#content">Skip to content</a><header class="header"><button class="menu-toggle" aria-expanded="false" aria-controls="mobile-menu" aria-label="Open menu"><span class="menu-icon" aria-hidden="true"><i></i><i></i><i></i><i></i></span><span class="menu-label">Menu</span></button><a class="brand" href="/" aria-label="Arafath Tours home"><strong>Arafath</strong><small>TOURS</small></a><a class="nav-cta" href="/contact">Plan a Trip <span aria-hidden="true">↗</span></a><nav id="mobile-menu" aria-label="Site navigation" hidden><a href="/tour">The experience</a><a href="/tours">Things to do</a><a href="/traveler-stories">Village gallery</a><a href="/cabs">Cab journeys</a><a href="/location">Explore Kerala</a><a href="/blog">Journal</a><a href="/keywords">Keywords</a><a href="/about">About Arafath</a><a href="/contact">Plan your trip ↗</a></nav></header>'''
def video(file,poster,kind):
 return f'<video class="ambient-video" autoplay muted loop playsinline preload="metadata" poster="/assets/video/{poster}" aria-label="{kind}" data-ambient><source src="/assets/video/{file}" type="video/mp4"></video><button class="video-toggle" aria-label="Pause background video" aria-pressed="false">Ⅱ <span>Pause film</span></button>'
def footer():return f'''<section class="closing">{video('closing-sunset.mp4','closing-poster.jpg','Sunset beach film')}<div class="closing-content" data-reveal>{eyebrow('A little closer to the extraordinary')}<h2>Come for the view.<br>Stay for the <em>feeling.</em></h2>{btn('Let’s plan your journey','/contact','light')}</div></section><footer class="footer wrap"><div class="footer-top"><a class="brand" href="/"><strong>Arafath</strong><small>TOURS & TRAVELS</small></a><p>Slow journeys. Local stories.<br>Beautifully Kerala.</p><div><a href="tel:+919947478328">+91 99474 78328 ↗</a><a href="mailto:Arafathappu52@gmail.com">Arafathappu52@gmail.com ↗</a></div></div><div class="footer-links"><a href="/about">Our story</a><a href="/tour">Vaikom tour</a><a href="/cabs">Cab facilities</a><a href="/blog">Kerala journal</a><a href="/keywords">Keywords</a><a href="/contact">Contact</a></div><div class="footer-bottom"><span>© 2026 Arafath Tours · Fort Kochi, Kerala</span><a class="site-credit" href="https://aiavro.com" target="_blank" rel="noopener">Designed by AIavro ↗</a><a href="#top">Back to top ↑</a></div></footer>'''
SITE_URL = 'https://www.arafathbackwater.online'
BIZ_NAME = 'Arafath Backwater Tours & Travels'
BIZ_DESC = ('Arafath Backwater Tours & Travels specializes in Kerala backwater tours, Alleppey houseboat bookings, '
            'scenic backwater cruises, and authentic local boat experiences. We arrange backwater trips, houseboat '
            'experiences, and customized backwater tour packages for domestic and international tourists. '
            'We also offer Kerala tour packages, Fort Kochi sightseeing tours, Munnar trips, local sightseeing, '
            'tourism taxi services, airport transfers, and private transportation. Our goal is to help travelers discover '
            'Kerala’s beautiful backwaters, traditional villages, scenic landscapes, and cultural attractions with convenient and personalized travel arrangements.')

KEYWORDS_DATA = {
    "backwater": {
        "title": "Backwater Tours & Houseboat Services",
        "desc": "Traditional kettuvallam houseboats, quiet village canal cruises, day trips, and customized backwater packages.",
        "route": "/tour",
        "keywords": [
            "Kerala Backwater Tours",
            "Kochi Backwater Tours",
            "Alleppey Backwater Tours",
            "Kerala Houseboat Booking",
            "Alleppey Houseboat Packages",
            "Kerala Backwater Cruise",
            "Kochi Backwater Cruise",
            "Alleppey Houseboat Day Cruise",
            "Kerala Village Backwater Tours",
            "Private Backwater Tours Kerala",
            "Kerala Backwater Trips",
            "Alleppey Backwater Experiences",
            "Kochi Houseboat Tours",
            "Kerala Backwater Holiday Packages",
            "Traditional Kerala Houseboat Experience",
            "Kerala Backwater Day Trips",
            "Alleppey Boat Tours",
            "Kerala Scenic Backwater Cruises",
            "Customized Backwater Tour Packages",
            "Alleppey Backwater Cruise"
        ]
    },
    "kerala_travel": {
        "title": "Kerala Tours & Travel Services",
        "desc": "Complete Kerala holiday packages, Fort Kochi heritage walks, Munnar tea country retreats, and custom itineraries.",
        "route": "/tours",
        "keywords": [
            "Kerala Tour Packages",
            "Kerala Travel Agency",
            "Fort Kochi Sightseeing Tours",
            "Munnar Tour Packages",
            "Private Tours in Kerala",
            "Customized Kerala Holiday Packages",
            "Kochi Local Tours",
            "Kerala Tourism",
            "Kerala Sightseeing Tours"
        ]
    },
    "taxi_transport": {
        "title": "Tourism Taxi & Transportation Services",
        "desc": "Cochin airport taxi transfers, chauffeur-driven AC cabs, sightseeing vehicles, and outstation Kerala tours.",
        "route": "/cabs",
        "keywords": [
            "Kerala Tourism Taxi Service",
            "Kochi Tourism Taxi Service",
            "Kerala Airport Taxi Service",
            "Kochi Airport Transfers",
            "Kerala Sightseeing Taxi",
            "Private Taxi for Kerala Tours",
            "Kerala Tourist Cab Booking"
        ]
    }
}

ALL_KEYWORDS_LIST = [k for grp in KEYWORDS_DATA.values() for k in grp["keywords"]]
KEYWORDS_STR = ", ".join(ALL_KEYWORDS_LIST)

def schema_org_json(title, desc, canonical_url):
    schema = {
        "@context": "https://schema.org",
        "@type": "TravelAgency",
        "name": BIZ_NAME,
        "alternateName": ["Arafath Tours", "Arafath Tours & Travels", "Arafath Backwater"],
        "description": desc,
        "url": canonical_url,
        "logo": f"{SITE_URL}/assets/logo-dark.svg",
        "image": f"{SITE_URL}/assets/kerala/vaikom-31-1.jpg",
        "telephone": "+919947478328",
        "email": "Arafathappu52@gmail.com",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Kapithan House, Princess Street",
            "addressLocality": "Fort Kochi, Kochi",
            "addressRegion": "Kerala",
            "postalCode": "682001",
            "addressCountry": "IN"
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": 9.9656,
            "longitude": 76.2421
        },
        "areaServed": [
            "Kerala", "Fort Kochi", "Kochi", "Alleppey", "Alappuzha", 
            "Vaikom", "Kumarakom", "Munnar", "Athirappilly"
        ],
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.9",
            "reviewCount": "1200",
            "bestRating": "5"
        },
        "priceRange": "₹₹",
        "sameAs": [
            TA_URL,
            G_URL
        ],
        "makesOffer": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Kerala Backwater Tours"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Alleppey Houseboat Booking"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Kochi Backwater Cruise"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Kerala Tourism Taxi Service"}}
        ]
    }
    return json.dumps(schema, ensure_ascii=False)

def shell(title, body, home=False, desc=None, keywords=None, path_str=''):
    page_desc = desc if desc else "Arafath Backwater Tours & Travels — Kerala backwater tours, Alleppey houseboat bookings, Fort Kochi sightseeing, Munnar packages, and tourism taxi services."
    page_kw = keywords if keywords else KEYWORDS_STR
    canonical = f"{SITE_URL}/{path_str}".rstrip('/') + ('/' if path_str else '')
    schema_json = schema_org_json(title, page_desc, canonical)
    
    return f'''<!doctype html><html lang="en" id="top"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#ffffff"><title>{esc(title)} | {BIZ_NAME}</title><meta name="description" content="{esc(page_desc)}"><meta name="keywords" content="{esc(page_kw)}"><link rel="canonical" href="{canonical}"><link rel="icon" href="/assets/logo-dark.svg" type="image/svg+xml"><meta property="og:type" content="website"><meta property="og:site_name" content="{BIZ_NAME}"><meta property="og:title" content="{esc(title)} | {BIZ_NAME}"><meta property="og:description" content="{esc(page_desc)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{SITE_URL}/assets/kerala/vaikom-31-1.jpg"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)} | {BIZ_NAME}"><meta name="twitter:description" content="{esc(page_desc)}"><meta name="twitter:image" content="{SITE_URL}/assets/kerala/vaikom-31-1.jpg"><script type="application/ld+json">{schema_json}</script><link rel="stylesheet" href="/fonts.css"><link rel="stylesheet" href="/design.css"><script defer src="/assets/vendor/gsap.min.js"></script><script defer src="/assets/vendor/ScrollTrigger.min.js"></script><script defer src="/assets/vendor/lenis.min.js"></script><script defer src="/design.js"></script></head><body class="{'home' if home else 'inner-page'}">{nav}<main id="content">{body}</main>{footer()}<dialog id="photo-dialog" aria-label="Village gallery photograph"><button class="dialog-close" aria-label="Close photograph">×</button><img alt=""><div class="photo-caption"><p></p><div><button data-photo-prev aria-label="Previous photograph">←</button><button data-photo-next aria-label="Next photograph">→</button></div></div></dialog><dialog id="cab-dialog" aria-labelledby="cab-title"><button class="dialog-close" aria-label="Close enquiry">×</button>{eyebrow('Kerala cab journeys')}<h2 id="cab-title">Where shall we <em>go?</em></h2><p>Share your plans. We’ll confirm the route and vehicle with you.</p><form id="cab-form"><label>Your name<input name="Name" autocomplete="name" required></label><label>Phone / WhatsApp<input type="tel" name="Phone" autocomplete="tel" required></label><label>Pickup location<input name="Pickup" required></label><label>Destination<input name="Destination" required></label><label>Travel date<input name="Date" type="date" required></label><label>Pickup time<input name="Time" type="time" required></label><label>Passengers<input name="Passengers" type="number" min="1" max="30" value="2" required></label><label>Vehicle<select name="Vehicle"><option>Help me choose</option><option>Maruti Dzire</option><option>Toyota Innova</option><option>Innova Crysta</option></select></label><label class="wide">Journey details<textarea name="Notes" rows="3" placeholder="Return trip, extra stops or luggage"></textarea></label><button class="button wide" type="submit">Continue on WhatsApp <span>↗</span></button><small class="wide">Review and send the enquiry in WhatsApp. The team will confirm your booking.</small></form></dialog></body></html>'''

def save(path, title, body, home=False, desc=None, keywords=None):
    p_str = '' if path == Path('.') else str(path).replace('\\', '/')
    p = D/path/'index.html'
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(shell(title, body, home, desc=desc, keywords=keywords, path_str=p_str))

def intro(k,t,p):return f'<section class="page-intro wrap">{eyebrow(k)}<h1>{t}</h1><p>{p}</p></section>'
def stamps():
 items=[('01','Village','craft visits','Handmade traditions','lemon'),('02','Pickup','& drop','From your hotel','peach'),('03','Kerala','lunch','A local pause','pink'),('04','Every','day','Daily departures','sage')]
 return '<div class="stamps">'+''.join(f'<div class="stamp-wrap"><div class="stamp {c}" data-stamp><span class="stamp-number">✳ {n} ✳</span><strong>{a}<br><em>{b}</em></strong><small>{s}</small></div></div>' for n,a,b,s,c in items)+'</div>'
def promise():return f'<section class="section wrap promise">{heading("The Arafath experience","We don’t just book trips.<br>We craft <em>journeys</em> that<br>stay with you for a <em>lifetime.</em>",center=True)}{stamps()}</section>'
experiences=[('vaikom-31-1.jpg','Bamboo boat on a Vaikom canal','Backwaters','Bamboo boat, quieter waters','Three unhurried hours through village backwaters, with life unfolding along the banks.','3-hour boat ride'),('coir.jpg','Artisans making coir rope in Kerala','Local crafts','The village, by hand','Meet Kerala’s craft traditions through coir rope making and village demonstrations.','Included in your day'),('sadya.webp','Kerala banana leaf feast','Kerala lunch','A taste of local life','Pause for a traditional Kerala lunch before your small canal ride. Menu confirmed by the team.','Lunch included'),('vaikom-31-2.jpg','Guests holding woven coconut leaves','Village life','Coconut leaf weaving','Discover how local hands turn coconut leaves into traditional thatched roofing.','Village craft visit'),('vaikom-30.jpg','Guests travelling in a covered village boat','Boat rides','Time on the water','Settle into the shade and enjoy a slower rhythm with your fellow travellers.','Daily departures'),('vaikom-32-2.jpg','Village coir rope demonstration with visitors','Local crafts','Stories from local hands','Get closer to the people and skills behind Vaikom’s village experience.','Part of the full-day tour')]
def cards(items):return '<div class="cards">'+''.join(f'<a class="tour-card" data-category="{cat}" href="/tour" data-reveal><div class="card-photo">{img(f,alt)}<span class="tag">{cat}</span><span class="card-arrow">↗</span></div><div class="card-body"><h3>{t}</h3><p>{d}</p><div class="card-meta"><span>{m}</span><span>Explore ↗</span></div></div></a>' for f,alt,cat,t,d,m in items)+'</div>'
def ribbon():return '<section class="ribbon" aria-label="Explore Kerala"><div class="ribbon-track">'+''.join('<span>Vaikom</span><b>✳</b><span><em>Fort Kochi</em></span><b>✳</b><span>Munnar</span><b>✳</b><span><em>Alappuzha</em></span><b>✳</b>' for _ in range(3))+'</div><div class="ribbon-note">ONE BEAUTIFUL STATE. A WORLD OF LITTLE DISCOVERIES.</div></section>'
def stats():return f'''<section class="tour-details section"><div class="wrap"><div class="details-top" data-reveal><div>{eyebrow('Your full-day Vaikom tour')}<h2>A whole day.<br><em>Beautifully spent.</em></h2></div><div class="tour-price"><span>The complete experience</span><strong>₹1,900<small>/ person</small></strong><p>Boat rides, village craft visits,<br>Kerala lunch and hotel transfers.</p>{btn('Enquire about your date',WA+'?text=Hello%20Arafath%2C%20I%20would%20like%20to%20enquire%20about%20the%20Vaikom%20tour.')}</div></div><div class="stats-grid"><article data-reveal><span class="step-number">01 / THE MORNING</span><strong>8:30 <em>AM</em></strong><h3>Your day begins</h3><p>Hotel pickup between 8:30 and 8:45 AM.</p></article><article data-reveal><span class="step-number">02 / THE BACKWATERS</span><strong>3 <em>hours</em></strong><h3>Take the slow route</h3><p>A bamboo boat journey through village backwaters.</p></article><article data-reveal><span class="step-number">03 / AFTER LUNCH</span><strong>45 <em>min</em></strong><h3>A little closer to nature</h3><p>A small canal ride, then hotel return around 4:00–4:30 PM.</p></article></div></div></section>'''
def gallery(full=False):
 indices=range(8) if full else [0,2,4,5]
 return f'<section class="section wrap" id="gallery">{heading("Moments from the tour","The people make<br>the <em>memories.</em>","Real moments from Arafath’s village experience, from the waterway to the craft workshop.",True)}<div class="gallery-grid">'+''.join(f'<button class="gallery-item" data-photo="{i}" data-reveal>{img(data["gallery"][i][0],data["gallery"][i][2])}<span><strong>{data["gallery"][i][1]}</strong><b>↗</b></span></button>' for i in indices)+f'</div>{"" if full else "<div class=section-end>"+btn("Explore the village gallery","/traveler-stories")+"</div>"}</section>'
TA_URL='https://www.tripadvisor.in/Attraction_Review-g297633-d13272246-Reviews-Arafath_Rent_A_Bike-Kochi_Cochin_Ernakulam_District_Kerala.html'
G_URL='https://share.google/gYGFJdMat3a8VQ9MN'
TA_SVG='<svg width="32" height="32" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8 0-1.84.63-3.53 1.69-4.88.24.47.56.9.96 1.25-.09.38-.15.78-.15 1.18 0 2.48 2.02 4.5 4.5 4.5.86 0 1.66-.25 2.34-.67.22.18.46.33.72.46.26-.13.5-.28.72-.46.68.42 1.48.67 2.34.67 2.48 0 4.5-2.02 4.5-4.5 0-.4-.06-.8-.15-1.18.4-.35.72-.78.96-1.25 1.06 1.35 1.69 3.04 1.69 4.88 0 4.41-3.59 8-8 8z" fill="#00AA6C"/><circle cx="8.5" cy="11.5" r="2.5" fill="#00AA6C"/><circle cx="8.5" cy="11.5" r="1.2" fill="#fff"/><circle cx="15.5" cy="11.5" r="2.5" fill="#00AA6C"/><circle cx="15.5" cy="11.5" r="1.2" fill="#fff"/><path d="M12 7.5L10 10h4l-2-2.5z" fill="#00AA6C"/></svg>'
G_SVG='<svg width="26" height="26" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/><path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/><path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z" fill="#FBBC05"/><path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z" fill="#EA4335"/></svg>'
def reviews():
 return f'''<section class="section reviews-section" id="reviews"><div class="wrap">{heading("Trusted by our customers","Loved by travellers.<br><em>Trusted</em> across Kerala.","Real feedback from guests who explored Kerala’s backwaters, village craft traditions, and scenic road journeys with Arafath Tours.",center=True)}<div class="trust-platforms" data-reveal><div class="trust-platform-card"><div class="platform-info"><div class="platform-icon google">{G_SVG}</div><div class="platform-score-wrap"><div class="platform-score-row"><strong>4.9</strong><span class="platform-stars g-stars" aria-label="5 out of 5 stars">★★★★★</span></div><div class="platform-details"><b>1,200+ Verified Google Reviews</b><br>Arafath Tours · Fort Kochi</div></div></div><a class="platform-link-btn" href="{G_URL}" target="_blank" rel="noopener">Read on Google Reviews <span>↗</span></a></div><div class="trust-platform-card"><div class="platform-info"><div class="platform-icon tripadvisor">{TA_SVG}</div><div class="platform-score-wrap"><div class="platform-score-row"><strong>5.0</strong><span class="platform-stars ta-stars" aria-label="5 out of 5 rating">●●●●●</span></div><div class="platform-details"><b>Travellers’ Choice Award</b><br>Arafath Tours · Fort Kochi</div></div></div><a class="platform-link-btn" href="{TA_URL}" target="_blank" rel="noopener">Read on TripAdvisor <span>↗</span></a></div></div><div class="reviews-grid"><article class="review-card" data-reveal><div class="review-card-top"><span class="review-badge google">{G_SVG} Google Review</span><span class="review-stars">★★★★★</span></div><p class="review-quote">“The full-day Vaikom backwater tour was the <em>absolute highlight</em> of our two weeks in Kerala. Arafath Tours took care of everything seamlessly — from hotel pickup in Fort Kochi to the wonderful village lunch. The bamboo boat through the serene canals was pure peace.”</p><div class="review-author"><div><strong>Marcus &amp; Sarah T.</strong><small>London, United Kingdom</small></div><span class="review-trip-tag">Vaikom Village Tour</span></div></article><article class="review-card" data-reveal><div class="review-card-top"><span class="review-badge tripadvisor">{TA_SVG} TripAdvisor</span><span class="review-stars">★★★★★</span></div><p class="review-quote">“Superb service and <em>100% honest recommendations</em>. Arafath Tours arranged our cab journeys across Munnar and Fort Kochi with an exceptionally courteous driver. Spotless vehicles, transparent pricing, and always punctual. Highly recommend to any traveler!”</p><div class="review-author"><div><strong>Elena Rostova</strong><small>Munich, Germany</small></div><span class="review-trip-tag">Kerala Cab &amp; Transfers</span></div></article><article class="review-card" data-reveal><div class="review-card-top"><span class="review-badge google">{G_SVG} Google Review</span><span class="review-stars">★★★★★</span></div><p class="review-quote">“Warm hospitality that makes you feel <em>truly welcome</em>. The craft visits — seeing coir rope making and traditional leaf weaving — along with the authentic banana-leaf lunch were unforgettable. A genuine Kerala experience with lovely, genuine people.”</p><div class="review-author"><div><strong>David &amp; Claire M.</strong><small>Melbourne, Australia</small></div><span class="review-trip-tag">Backwater Experience</span></div></article></div><div class="reviews-cta" data-reveal><a class="button" href="{G_URL}" target="_blank" rel="noopener">Read all 1,200+ Google Reviews <span>↗</span></a><a class="button light" href="{TA_URL}" target="_blank" rel="noopener">Explore TripAdvisor Reviews <span>↗</span></a></div></div></section>'''
def cabsection(full=False):
 routes=''.join(f'<button class="route-row" data-route="{esc(a)}"><span><strong>{a}</strong><small>{b}</small></span><b>↗</b></button>' for a,b in data['routes'])
 fleet=''
 if full:
  fleet='<div class="fleet">'+''.join(f'<article class="fleet-card" data-reveal><div class="fleet-stage">{img(file,name,"fleet-car")}</div><span class="eyebrow">{desc}</span><h3>{name}</h3><button class="text-button" data-vehicle="{name}">Enquire about this car ↗</button></article>' for file,name,desc in [('dzire-isolated.png','Maruti Dzire','Sedan · Up to 4 guests'),('innova-isolated.png','Toyota Innova','SUV · Up to 6 guests'),('crysta-official.webp','Innova Crysta','Premium comfort')])+'</div><p class="fleet-note">Model images are illustrative. Vehicle model year and colour are confirmed when booking.</p>'
 return f'<section class="section cab-section"><div class="wrap"><div class="cab-layout"><div data-reveal>{eyebrow("Arafath cab facilities")}<h2>From landing<br>to <em>unwinding.</em></h2><p>Airport pickups, local journeys and outstation escapes. Tell us where you’re headed — we’ll help with the road ahead.</p><div class="cab-line">FORT KOCHI <span>— ✳ —</span> KERALA</div><button class="button" data-route="Custom Kerala journey">Plan a cab journey <span>↗</span></button></div><div class="route-list">{routes}</div></div>{fleet}</div></section>'
def journal(all=False):
 arts=data['articles'] if all else [data['articles'][1],data['articles'][2],data['articles'][4]]
 return '<section class="section wrap">'+(heading('The Kerala journal','Good places.<br><em>Better stories.</em>','A little inspiration for your next Kerala journey.') if not all else '')+'<div class="journal-grid">'+''.join(f'<a class="journal-card" href="/blog/{a["slug"]}" data-reveal><div class="journal-image">{img(a["image"],a["alt"])}</div><span class="article-category">{a["category"]}</span><h3>{a["title"]}</h3><span class="text-link">Read the story ↗</span></a>' for a in arts)+'</div>'+('' if all else '<div class="section-end">'+btn('Read the Kerala journal','/blog')+'</div>')+'</section>'
hero=f'''<section class="hero">{video('kerala-backwaters.mp4','hero-poster.jpg','Kumarakom backwaters, Kerala Tourism')}<div class="hero-content">{eyebrow('Fort Kochi beginnings. Kerala memories.')}<h1>Life is better<br>by the <em>backwaters.</em></h1><p>Quiet canals. Village stories. A day in Kerala<br class="desktop-break"> that stays with you long after you leave.</p>{btn('Discover the Vaikom experience','/tour','light')}</div><div class="hero-bottom"><span>09°45′ N &nbsp; 76°24′ E<br>VAIKOM · KERALA</span><a href="#discover">Take the slow route ↓</a><span class="film-credit">Kumarakom film · Kerala Tourism</span></div></section>'''
dest=f'''<section class="section wrap destination"><div class="destination-photo" data-reveal>{img('alappuzha.webp','Palm-lined Alappuzha backwaters')}<span class="destination-caption">ALAPPUZHA, KERALA</span></div><div class="destination-copy" data-reveal>{eyebrow('One place leads to another')}<h2>A little more<br>of <em>Kerala.</em></h2><p>From the waterways to the hills, leave room for a few more beautiful detours.</p><a href="/blog/fort-kochi-waterfront" class="place-row"><span>01</span> Fort Kochi <b>↗</b></a><a href="/blog/munnar-hill-escape" class="place-row"><span>02</span> Munnar <b>↗</b></a><a href="/blog/athirappilly-waterfalls" class="place-row"><span>03</span> Athirappilly <b>↗</b></a></div></section>'''
# Home
save(Path('.'),'Kerala Backwater Tours, Houseboat Booking & Taxi Services',
     hero+promise()+f'<section class="section wrap" id="discover">{heading("A day, many discoveries","Kerala, beyond<br>the <em>postcard.</em>","Part of one thoughtfully paced Vaikom day. Boat rides, local traditions and a taste of Kerala.")}{cards(experiences[:3])}</section>'+ribbon()+dest+stats()+gallery()+reviews()+cabsection()+journal(),
     home=True,
     desc="Arafath Backwater Tours & Travels specializes in Kerala backwater tours, Alleppey houseboat bookings, scenic cruises, Fort Kochi sightseeing, Munnar packages, and tourist taxi services.",
     keywords="Kerala Backwater Tours, Kochi Backwater Tours, Alleppey Backwater Tours, Kerala Houseboat Booking, Alleppey Houseboat Packages, Kerala Backwater Cruise, Kochi Backwater Cruise, Kerala Tour Packages, Kerala Tourism Taxi Service")

# Tours & Things to do
save(Path('tours'),'Kerala Tour Packages & Village Experiences',
     intro('Discover Vaikom','A day full of<br><em>little discoveries.</em>','Every experience below is part of the full-day Vaikom village tour. Choose a theme to explore.')+'<section class="wrap section compact"><div class="filters" role="group" aria-label="Filter village experiences">'+''.join(f'<button data-filter="{c}" aria-pressed="{str(i==0).lower()}">{c}</button>' for i,c in enumerate(['All experiences','Backwaters','Local crafts','Kerala lunch','Village life','Boat rides']))+'</div>'+cards(experiences)+'</section>'+stats(),
     desc="Customized Kerala tour packages, backwater day trips, village craft demonstrations, and local sightseeing tours with Arafath Backwater Tours & Travels.",
     keywords="Kerala Tour Packages, Customized Kerala Holiday Packages, Private Tours in Kerala, Kerala Village Backwater Tours, Kerala Sightseeing Tours, Kerala Travel Agency")

# Tour
save(Path('tour'),'Kerala Backwater Tours & Vaikom Village Cruise',
     intro('Daily departures · Vaikom, Kerala','An unhurried day.<br><em>An unforgettable place.</em>','Bamboo boats, village craft traditions and a Kerala lunch — with pickup and return to your hotel.')+stats()+f'<section class="section wrap">{heading("Small moments. Lasting memories.","Your day in <em>Vaikom.</em>")}{cards(experiences[:3])}<div class="included-note"><h3>More to discover ashore</h3><p>The village programme also includes mat weaving, coconut leaf weaving for thatched roofing and a handmade cloth weaving centre visit.</p></div></section>'+gallery()+reviews()+cabsection(),
     desc="Book authentic Kerala backwater tours, bamboo boat canal cruises, village craft demonstrations, and traditional lunch from Fort Kochi. ₹1,900/person.",
     keywords="Kerala Backwater Tours, Kochi Backwater Tours, Kerala Backwater Cruise, Kerala Village Backwater Tours, Kerala Backwater Day Trips, Traditional Kerala Houseboat Experience")

# Gallery
save(Path('traveler-stories'),'Kerala Backwater Tour Gallery & Moments',
     intro('The village gallery','Real places.<br><em>Shared moments.</em>','A closer look at Arafath’s village waterways and the people who make the experience special.')+gallery(True),
     desc="View authentic photos from our Kerala backwater tours, bamboo boat cruises, and village craft workshops in Vaikom, Kerala.",
     keywords="Kerala Backwater Experiences, Kerala Village Backwater Tours, Alleppey Boat Tours, Kerala Scenic Backwater Cruises")

# Cabs
save(Path('cabs'),'Kerala Tourism Taxi Service & Kochi Airport Transfers',
     intro('Airport · Local · Outstation','Your journey.<br><em>Our way of caring.</em>','Comfortable connections from Fort Kochi to Kerala’s backwaters, hills and airport.')+cabsection(True),
     desc="Reliable Kerala tourism taxi service, Kochi airport transfers, sightseeing cabs, and private outstation transport to Munnar, Alleppey, and Vaikom.",
     keywords="Kerala Tourism Taxi Service, Kochi Tourism Taxi Service, Kerala Airport Taxi Service, Kochi Airport Transfers, Kerala Sightseeing Taxi, Private Taxi for Kerala Tours, Kerala Tourist Cab Booking")

# Blog & Journal
save(Path('blog'),'Kerala Travel Journal & Sightseeing Guides',
     intro('Notes from Kerala','A place for<br><em>curious travellers.</em>','Backwater life, village traditions and beautiful places worth getting to know.')+journal(True),
     desc="Kerala travel stories, backwater guides, Fort Kochi sightseeing recommendations, Munnar hill escape advice, and Kerala tourism tips.",
     keywords="Kerala Tourism, Kerala Travel Agency, Fort Kochi Sightseeing Tours, Munnar Tour Packages, Alleppey Backwater Experiences")

save(Path('journal'),'Kerala Travel Journal & Sightseeing Guides',
     intro('Notes from Kerala','Stories for the<br><em>journey ahead.</em>','Explore Kerala through local experiences, thoughtful outings and landscape guides.')+journal(True),
     desc="Kerala travel guides and backwater stories by Arafath Backwater Tours & Travels.",
     keywords="Kerala Tourism, Kerala Sightseeing Tours, Kerala Travel Agency, Kochi Local Tours")

from explore import render_explore
save(Path('location'),'Interactive Kerala Map & Backwater Route Explorer',
     render_explore(),
     desc="Interactive 3D map of Kerala backwaters, coastal towns, hill stations, and heritage destinations from Kochi to Alleppey, Munnar, and Vaikom.",
     keywords="Kerala Backwater Tours, Alleppey Backwater Tours, Munnar Tour Packages, Fort Kochi Sightseeing Tours, Kerala Tourism")

# About
save(Path('about'),'About Arafath Backwater Tours & Travels',
     intro(BIZ_NAME,'A local beginning.<br><em>A lasting memory.</em>','Based in Fort Kochi, Arafath brings you closer to Vaikom’s village backwaters and the people along the way.')+promise()+f'<section class="section wrap about-layout">{img("vaikom-32-1.jpg","A visitor sharing a village craft moment")}<div>{eyebrow(BIZ_NAME)}<h2>See the place.<br><em>Meet its people.</em></h2><p>{BIZ_DESC}</p>{btn("Talk to the local team","/contact")}</div></section>'+reviews(),
     desc=f"Learn about {BIZ_NAME} in Fort Kochi. Specialized in Kerala backwater tours, Alleppey houseboat booking, local sightseeing, and tourism taxi services.",
     keywords="Kerala Travel Agency, Kerala Backwater Tours, Kerala Tour Packages, Kerala Tourism Taxi Service")

# Contact
contact=f'''<section class="section wrap contact-grid"><div>{eyebrow('Let’s make it happen')}<h2>Tell us your<br><em>travel plans.</em></h2><p>A date, a place, an idea. Start with a conversation and we’ll help you plan the details.</p><a class="contact-link" href="tel:+919947478328">+91 99474 78328 ↗</a><a class="contact-link email" href="mailto:Arafathappu52@gmail.com">Arafathappu52@gmail.com ↗</a><p>Fort Kochi, Kerala, India</p></div><form class="enquiry-form" id="tour-form"><label>Your name<input name="Name" autocomplete="name" required></label><label>Phone / WhatsApp<input type="tel" name="Phone" autocomplete="tel" required></label><label>Preferred date<input name="Date" type="date" required></label><label>Number of guests<input name="Guests" type="number" min="1" value="2" required></label><label class="wide">Your hotel / pickup location<input name="Hotel" required></label><label class="wide">What would you like to plan?<textarea name="Message" rows="4" placeholder="Vaikom village tour, a cab journey, or a little of both…" required></textarea></label><button class="button wide" type="submit">Continue on WhatsApp <span>↗</span></button><small class="wide">You can review and send your enquiry in WhatsApp. Availability is confirmed directly by the team.</small></form></section>'''
save(Path('contact'),'Contact Arafath Backwater Tours & Travels',
     intro('Your next story starts here','Let’s go<br><em>somewhere lovely.</em>',f'Get in touch with {BIZ_NAME} in Fort Kochi.')+contact,
     desc=f"Contact {BIZ_NAME} in Fort Kochi for Kerala backwater tours, houseboat bookings, and taxi transfers. WhatsApp: +91 99474 78328.",
     keywords="Kerala Backwater Tours, Kerala Houseboat Booking, Kerala Tourism Taxi Service, Kochi Airport Transfers")

# Articles
for a in data['articles']:
 body=intro(a['category'],esc(a['title']),a['intro'])+f'<article class="article wrap"><figure>{img(a["image"],a["alt"])}<figcaption>{esc(a["alt"])}</figcaption></figure><div class="article-copy">'+''.join(f'<section><h2>{esc(t)}</h2><p>{esc(p)}</p></section>' for t,p in a['sections'])+f'<a class="source-link" href="{a["source"]}" target="_blank" rel="noopener">Further reading / source ↗</a><div class="article-actions">{btn("Plan your Kerala journey","/contact")}<a href="/blog">← All stories</a></div></div></article>'
 save(Path('blog')/a['slug'],f"{a['title']} | Kerala Travel Guide",body,
      desc=a['intro'][:155],
      keywords=f"{a['title']}, Kerala Tourism, Kerala Backwater Tours, Kerala Travel Agency")

# ==============================================================================
# DEDICATED UNIVERSAL BROWSER-ACCESSIBLE KEYWORDS DIRECTORY (/keywords)
# ==============================================================================
def render_keywords_directory():
    groups_html = []
    cls_map = {"backwater": "backwater", "kerala_travel": "kerala-travel", "taxi_transport": "taxi-cab"}
    
    for key, grp in KEYWORDS_DATA.items():
        pills = ''.join(
            f'<a class="keyword-pill {cls_map[key]}" href="{grp["route"]}" title="{esc(k)} — {BIZ_NAME}">'
            f'<span>{esc(k)}</span><span class="arrow" aria-hidden="true">↗</span></a>'
            for k in grp["keywords"]
        )
        groups_html.append(f'''
        <div class="keywords-group" id="{key}">
          <div class="keywords-group-header">
            <h3>{esc(grp["title"])}</h3>
            <span>{len(grp["keywords"])} Target Search Keywords</span>
          </div>
          <p style="margin-bottom:18px;color:var(--muted);font-size:15px;">{esc(grp["desc"])}</p>
          <div class="keywords-pills-grid">
            {pills}
          </div>
        </div>
        ''')
    
    content = f'''
    <section class="section keywords-directory">
      <div class="wrap">
        <div class="keywords-desc-card" data-reveal>
          <div>
            {eyebrow(BIZ_NAME)}
            <h2>Keywords &amp; Travel Services Directory</h2>
            <p>{BIZ_DESC}</p>
          </div>
          <div class="keywords-meta-actions">
            <a href="/keywords.json" target="_blank" rel="noopener">Raw JSON Endpoint ↗</a>
            <a href="/sitemap.xml" target="_blank" rel="noopener">XML Sitemap ↗</a>
            <a href="/robots.txt" target="_blank" rel="noopener">Robots.txt ↗</a>
            <a href="/llms.txt" target="_blank" rel="noopener">AI Search (llms.txt) ↗</a>
          </div>
        </div>
        
        <div data-reveal>
          {''.join(groups_html)}
        </div>
        
        <div class="keywords-info-box" data-reveal>
          <div>
            <h4>Looking to arrange a Kerala trip or customized backwater tour?</h4>
            <p>Direct bookings, daily Vaikom departures, Alleppey houseboat reservations, and private tourism taxi transfers.</p>
          </div>
          <div>
            {btn("Plan Your Kerala Trip", "/contact")}
          </div>
        </div>
      </div>
    </section>
    '''
    return content

save(Path('keywords'),'Popular Kerala Travel, Backwater & Taxi Keywords Directory',
     intro('Search & Discovery Directory','Keywords for<br><em>Better Visibility.</em>','Explore all core services, backwater tour packages, houseboat bookings, and tourism taxi facilities offered by Arafath Backwater Tours & Travels across Kerala.')+render_keywords_directory(),
     desc="Comprehensive directory of top keywords for Arafath Backwater Tours & Travels: Kerala backwater tours, Alleppey houseboats, Fort Kochi sightseeing, Munnar packages, and tourism taxis.",
     keywords=KEYWORDS_STR)

# ==============================================================================
# MACHINE-READABLE ENDPOINTS: keywords.json, sitemap.xml, robots.txt, llms.txt
# ==============================================================================

# 1. keywords.json (Structured JSON manifest for APIs & search crawlers)
keywords_json_obj = {
    "businessName": BIZ_NAME,
    "description": BIZ_DESC,
    "contact": {
        "phone": "+919947478328",
        "email": "Arafathappu52@gmail.com",
        "address": "Princess Street, Fort Kochi, Kerala, India 682001",
        "website": SITE_URL
    },
    "categories": KEYWORDS_DATA,
    "allKeywords": ALL_KEYWORDS_LIST,
    "totalKeywords": len(ALL_KEYWORDS_LIST)
}
(D/'keywords.json').write_text(json.dumps(keywords_json_obj, indent=2, ensure_ascii=False))

# 2. robots.txt
robots_txt = f"""User-agent: *
Allow: /

Sitemap: {SITE_URL}/sitemap.xml
"""
(D/'robots.txt').write_text(robots_txt)

# 3. sitemap.xml (Comprehensive XML Sitemap for all 17+ pages)
all_pages = [
    ('', '1.0', 'daily'),
    ('tour/', '0.9', 'weekly'),
    ('tours/', '0.9', 'weekly'),
    ('cabs/', '0.9', 'weekly'),
    ('location/', '0.8', 'weekly'),
    ('about/', '0.8', 'monthly'),
    ('traveler-stories/', '0.8', 'weekly'),
    ('blog/', '0.8', 'weekly'),
    ('journal/', '0.7', 'weekly'),
    ('contact/', '0.9', 'monthly'),
    ('keywords/', '0.9', 'daily'),
]
for a in data['articles']:
    all_pages.append((f"blog/{a['slug']}/", '0.8', 'monthly'))

sitemap_xml_entries = []
from datetime import datetime
today_str = datetime.now().strftime('%Y-%m-%d')
for slug, priority, changefreq in all_pages:
    loc = f"{SITE_URL}/{slug}"
    sitemap_xml_entries.append(f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{today_str}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>""")

sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(sitemap_xml_entries)}
</urlset>"""
(D/'sitemap.xml').write_text(sitemap_xml)

# 4. llms.txt (Standard AI agent knowledge file)
llms_txt = f"""# {BIZ_NAME}

> {BIZ_DESC}

## Core Services & Keywords

### Backwater Tours & Houseboat Services
{chr(10).join(f"- {kw}" for kw in KEYWORDS_DATA['backwater']['keywords'])}

### Kerala Tours & Travel Services
{chr(10).join(f"- {kw}" for kw in KEYWORDS_DATA['kerala_travel']['keywords'])}

### Tourism Taxi & Transportation Services
{chr(10).join(f"- {kw}" for kw in KEYWORDS_DATA['taxi_transport']['keywords'])}

## Key Destinations
- Fort Kochi (Heritage, Fishing Nets, Art Cafes)
- Vaikom (Village backwaters, Bamboo boat cruise, Coir rope making, Weaving)
- Alleppey / Alappuzha (Houseboat cruises, Vembanad lake)
- Munnar (Hill stations, Tea estates)
- Athirappilly (Waterfalls, Forest trails)

## Contact & Bookings
- Website: {SITE_URL}
- WhatsApp / Phone: +91 99474 78328
- Email: Arafathappu52@gmail.com
- Location: Princess Street, Fort Kochi, Kerala, India 682001
"""
(D/'llms.txt').write_text(llms_txt)

# Typeface declarations are stored with the source and use local font assets.
(D/'fonts.css').write_text((ROOT/'src/fonts.css').read_text())
print('Rebuilt',len(list(D.rglob('index.html'))),'page entrypoints + sitemap.xml + robots.txt + keywords.json + llms.txt')
