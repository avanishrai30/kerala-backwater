/* Arafath Kerala experience: local GSAP, accessible gallery and route enquiries. */
(() => {
'use strict';
const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
const reduced=window.matchMedia('(prefers-reduced-motion: reduce)');
const asset='/assets/kerala/';
const gallery=[['vaikom-31.jpg','The village waterway','A covered boat beneath Vaikom’s green canal canopy.'],['vaikom-31-1.jpg','A slower way to travel','A traditional boat on a quiet village canal.'],['vaikom-30.jpg','On board in Vaikom','Guests enjoying the covered village boat.'],['vaikom-32-2.jpg','The craft of coir','A village demonstration of coconut-fibre rope making.'],['vaikom-31-2.jpg','Woven by hand','Guests discovering local weaving traditions.'],['vaikom-32-1.jpg','Learning from local hands','Visitors taking part in a village craft activity.'],['vaikom-32.jpg','A moment ashore','A closer look at the craft demonstration.'],['vaikom-31-3.jpg','People behind the experience','Village crafts and shared moments during the tour.']];
const root=$('#kerala-dialogs')||document.body.appendChild(document.createElement('div'));
root.innerHTML=`<dialog id="k-photo-dialog" class="k-lightbox" aria-label="Vaikom village photo gallery"><button class="k-close" aria-label="Close photograph">×</button><img alt=""><div class="k-lightbox-caption"><div><h3></h3><p></p></div><div class="k-lightbox-controls"><button data-photo-prev aria-label="Previous photograph">←</button><button data-photo-next aria-label="Next photograph">→</button></div></div></dialog>
<dialog id="k-film-dialog" class="k-lightbox" aria-label="Kerala backwater film"><button class="k-close" aria-label="Close film">×</button><div class="k-film-mount"></div><a class="k-video-credit" href="https://www.keralatourism.org/video-gallery/journey-through-alappuzha-backwaters/1790/" target="_blank" rel="noopener">Journey Through Alappuzha Backwaters · Kerala Tourism</a></dialog>
<dialog id="k-cab-dialog" class="k-cab-dialog" aria-labelledby="k-cab-title"><button class="k-close" aria-label="Close cab enquiry">×</button><span class="k-badge">ARAFATH CABS · KERALA</span><h2 id="k-cab-title">Where are we taking you?</h2><p>Tell us your route. Our team will confirm the vehicle and journey details.</p><form class="k-cab-form"><label>Your name<input name="Name" autocomplete="name" required></label><label>Phone / WhatsApp<input name="Phone" type="tel" autocomplete="tel" required></label><label class="wide">Vehicle preference<select name="Vehicle"><option>Help me choose</option><option>Maruti Dzire</option><option>Toyota Innova</option><option>Innova Crysta</option></select></label><label>Pickup location<input name="Pickup" required></label><label>Destination<input name="Destination" required></label><label>Travel date<input name="Date" type="date" required></label><label>Pickup time<input name="Time" type="time" required></label><label>Passengers<input name="Passengers" type="number" min="1" max="30" value="2" required></label><label>Journey type<select name="Journey"><option>One way</option><option>Round trip</option><option>Local sightseeing</option><option>Custom itinerary</option></select></label><label class="wide">Stops or additional details<textarea name="Notes" rows="2"></textarea></label><button class="k-button wide" type="submit"><span>Continue on WhatsApp</span><b aria-hidden="true">↗</b></button><small class="wide">A prefilled enquiry opens in WhatsApp. Send it there to request your journey; your booking is confirmed directly by the team.</small></form></dialog>`;
const photo=$('#k-photo-dialog'),film=$('#k-film-dialog'),cab=$('#k-cab-dialog');
let photoIndex=0;
function show(d){d.showModal();document.body.style.overflow='hidden'}
function close(d){d.close()}
[photo,film,cab].forEach(d=>{$('.k-close',d).addEventListener('click',()=>close(d));d.addEventListener('close',()=>{document.body.style.overflow='';if(d===film)$('.k-film-mount',film).replaceChildren()});d.addEventListener('click',e=>{if(e.target===d){const b=d.getBoundingClientRect();if(e.clientX<b.left||e.clientX>b.right||e.clientY<b.top||e.clientY>b.bottom)close(d)}})});
function updatePhoto(n){photoIndex=(n+gallery.length)%gallery.length;const [file,title,description]=gallery[photoIndex];$('img',photo).src=asset+file;$('img',photo).alt=title;$('h3',photo).textContent=title;$('p',photo).textContent=`${photoIndex+1} / ${gallery.length} — ${description}`;}
$$('[data-gallery-index]').forEach(b=>b.addEventListener('click',()=>{updatePhoto(Number(b.dataset.galleryIndex));show(photo)}));
$('[data-photo-prev]',photo).addEventListener('click',()=>updatePhoto(photoIndex-1));$('[data-photo-next]',photo).addEventListener('click',()=>updatePhoto(photoIndex+1));photo.addEventListener('keydown',e=>{if(e.key==='ArrowLeft'){e.preventDefault();updatePhoto(photoIndex-1)}if(e.key==='ArrowRight'){e.preventDefault();updatePhoto(photoIndex+1)}});
$$('[data-gallery-shift]').forEach(b=>b.addEventListener('click',()=>{const section=b.closest('.k-gallery'),window=$('.k-gallery-window',section);window.scrollBy({left:Number(b.dataset.galleryShift)*365,behavior:reduced.matches?'instant':'smooth'})}));
$$('[data-kerala-video]').forEach(b=>b.addEventListener('click',()=>{const f=document.createElement('iframe');f.className='k-video-frame';f.title='Journey Through Alappuzha Backwaters — Kerala Tourism';f.src='https://www.youtube.com/embed/aKeqNBupeIg?autoplay=1&rel=0';f.allow='autoplay; encrypted-media; picture-in-picture';f.allowFullscreen=true;f.referrerPolicy='strict-origin-when-cross-origin';$('.k-film-mount',film).replaceChildren(f);show(film)}));
const current=new Date();const today=new Date(current.getTime()-current.getTimezoneOffset()*60000).toISOString().slice(0,10);$('input[type=date]',cab).min=today;
function openCab(route='',vehicle=''){
 const form=$('form',cab);if(route&&route.includes('↔')){const parts=route.split('↔').map(v=>v.trim());form.elements.Pickup.value=parts[0];form.elements.Destination.value=parts[1]}else if(route){form.elements.Pickup.value='';form.elements.Destination.value='';form.elements.Notes.value=route}if(vehicle)form.elements.Vehicle.value=vehicle;show(cab)
}
$$('[data-cab-route]').forEach(b=>b.addEventListener('click',()=>openCab(b.dataset.cabRoute)));$$('[data-cab-vehicle]').forEach(b=>b.addEventListener('click',()=>openCab('',b.dataset.cabVehicle)));
$('form',cab).addEventListener('submit',e=>{e.preventDefault();const f=e.currentTarget;if(!f.reportValidity())return;const lines=['Arafath Tours — Kerala Cab Enquiry',''];for(const [key,value] of new FormData(f))if(String(value).trim())lines.push(`${key}: ${value}`);lines.push('','Please confirm vehicle availability and journey details.');window.open('https://wa.me/919947478328?text='+encodeURIComponent(lines.join('\n')),'_blank','noopener')});
// Replace the previous static location labels and images as one consistent carousel.
const destinations=[['Vaikom','Quiet waterways, coconut palms and village life in Kerala.','vaikom-31.jpg','/tour'],['Fort Kochi','Traditional fishing nets and the heritage streets of Kerala’s coast.','fort-kochi.webp','/blog/fort-kochi-waterfront'],['Munnar','Green valleys and a slower journey through Kerala’s hill country.','munnar.webp','/blog/munnar-hill-escape'],['Alappuzha','Palm-lined waterways and everyday life along the backwaters.','alappuzha.webp','/blog/alappuzha-backwater-guide'],['Athirappilly','A broad waterfall set against the forested Kerala landscape.','athirappilly.webp','/blog/athirappilly-waterfalls']];
$$('section[data-framer-name="Tours"]').filter(s=>$('[data-framer-name="Arrow Left"]',s)).forEach(section=>{let idx=0;function choose(i){idx=(i+destinations.length)%destinations.length;const [name,desc,file,url]=destinations[idx];$$('a',section).filter(a=>$('h3',a)).forEach(a=>{const h=$('h3',a);h.textContent=name;const p=$$('p',a).find(p=>p.textContent.length>40);if(p)p.textContent=desc;a.href=url;const im=$('img',a);if(im){im.src=asset+file;im.alt=name+', Kerala';im.removeAttribute('srcset')}})}
$$('[data-framer-name="Arrow Left"],[data-framer-name="Arrow Right"]',section).forEach(old=>{const b=old.cloneNode(true);old.replaceWith(b);const fn=()=>choose(idx+(b.dataset.framerName==='Arrow Left'?-1:1));b.addEventListener('click',fn);b.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();fn()}})});choose(0);
});
// Correct the retained tour filters: original title elements are h2, not h3.
if(location.pathname.replace(/\/$/,'')==='/tours'){
 const labels=['All Tours','Village Life','Backwaters','Boat Rides','Kerala Lunch','Local Crafts'];
 const cards=$$('a[href="/tour"]').filter(a=>$('h2',a));
 $$('[role=button],button').filter(b=>labels.includes(b.textContent.trim())&&!b.closest('nav')).forEach(old=>{const b=old.cloneNode(true);old.replaceWith(b);b.addEventListener('click',e=>{e.preventDefault();const label=b.textContent.trim();cards.forEach(a=>{const text=a.textContent.toLowerCase();const show=label==='All Tours'||(label==='Kerala Lunch'?/lunch/.test(text):['Village Life','Local Crafts'].includes(label)?/craft|weav|coir|village/.test(text):/boat|canal|backwater/.test(text));a.closest('[class$="-container"]')?.classList.toggle('client-hidden',!show)})})})
}
// Real GSAP / ScrollTrigger timelines. Core content is visible if either library fails.
if(window.gsap&&window.ScrollTrigger){
 const gsap=window.gsap;gsap.registerPlugin(window.ScrollTrigger);const media=gsap.matchMedia();
 media.add('(prefers-reduced-motion: no-preference)',()=>{
  const hero=$('section[data-framer-name="Hero"]');
  if(hero){
   const words=$$('h1',hero);gsap.fromTo(words,{y:70,opacity:0},{y:0,opacity:1,duration:1.15,stagger:.11,ease:'power3.out',delay:.12});
   const intro=$$('[data-framer-appear-id]',hero).filter(e=>!$('h1',e));gsap.fromTo(intro,{y:30,opacity:0},{y:0,opacity:1,duration:.9,stagger:.08,ease:'power2.out',delay:.4});
   const backgrounds=$$('img',hero).filter(i=>i.src.includes('/assets/kerala/'));backgrounds.forEach(im=>gsap.to(im,{yPercent:12,scale:1.12,ease:'none',scrollTrigger:{trigger:hero,start:'top top',end:'bottom top',scrub:1}}));
   if(words.length)gsap.to(words,{y:55,opacity:.15,ease:'none',scrollTrigger:{trigger:hero,start:'20% top',end:'bottom top',scrub:.8}});
  }
  // Original word-by-word heading groups retain their serif/sans typographic design.
  $$('main section').filter(s=>s.dataset.framerName&&!s.closest('section section')&&s!==hero).forEach(s=>{
   const heads=$$('h2',s).filter(h=>!h.closest('a')&&h.textContent.trim());if(heads.length)gsap.fromTo(heads,{y:34,opacity:.2},{y:0,opacity:1,duration:.85,stagger:.045,ease:'power3.out',scrollTrigger:{trigger:heads[0],start:'top 90%',toggleActions:'play none none reverse'}});
  });
  $$('[data-k-reveal]').forEach((el,i)=>gsap.fromTo(el,{y:52,opacity:.12},{y:0,opacity:1,duration:1,ease:'power3.out',scrollTrigger:{trigger:el,start:'top 91%',toggleActions:'play none none reverse'}}));
  $$('[data-k-sticker]').forEach((el,i)=>{const base=Number(gsap.getProperty(el,'rotation'))||0;gsap.fromTo(el,{y:55,rotation:base+(i%2?22:-22),scale:.78},{y:-10,rotation:base+(i%2?-5:5),scale:1,ease:'none',scrollTrigger:{trigger:el,start:'top bottom',end:'bottom 25%',scrub:1.3}})});
  // Smoothly reveal full sections and scroll their image surfaces at a different pace.
  $$('.k-cab-photo>img,.k-destination>img,.k-article-image>img').forEach(im=>gsap.fromTo(im,{scale:1.12,yPercent:-4},{scale:1.02,yPercent:4,ease:'none',scrollTrigger:{trigger:im.parentElement,start:'top bottom',end:'bottom top',scrub:1.2}}));
  $$('.k-gallery').forEach(section=>{const track=$('.k-gallery-track',section);gsap.fromTo(track,{x:45},{x:0,ease:'none',scrollTrigger:{trigger:section,start:'top bottom',end:'top 25%',scrub:1}})});
  // Horizontal photo motion follows vertical scrolling on roomy screens; mobile keeps swipe.
  media.add('(min-width: 1000px) and (min-height: 720px)',()=>{$$('.k-gallery-window').forEach(view=>{const overflow=()=>Math.max(0,view.scrollWidth-view.clientWidth);if(!overflow())return;view.style.scrollSnapType='none';gsap.to(view,{scrollLeft:overflow,ease:'none',scrollTrigger:{trigger:view,start:'top 14%',end:()=>'+='+Math.min(2400,overflow()),pin:true,scrub:1,invalidateOnRefresh:true}})})});
  // Mobile fleet cards settle into a small stack, without locking the page scroll.
  media.add('(max-width: 700px)',()=>{$$('.k-fleet-card').forEach((card,i)=>{gsap.fromTo(card,{y:55,scale:.93},{y:0,scale:1,ease:'none',scrollTrigger:{trigger:card,start:'top 95%',end:'top 55%',scrub:1}})})});
  const wipe=document.createElement('div');wipe.className='k-transition';wipe.setAttribute('aria-hidden','true');document.body.append(wipe);
  document.addEventListener('click',e=>{const a=e.target.closest('a');if(!a||e.defaultPrevented||e.ctrlKey||e.metaKey||e.shiftKey||e.altKey||a.target==='_blank'||a.hasAttribute('download'))return;const url=new URL(a.href,location.href);if(url.origin!==location.origin||url.pathname===location.pathname||url.hash)return;e.preventDefault();gsap.to(wipe,{yPercent:-100,duration:.3,ease:'power2.inOut',onComplete:()=>location.assign(url.href)})});
  window.addEventListener('pageshow',()=>gsap.set(wipe,{yPercent:0}));
 });
 const refresh=()=>window.ScrollTrigger.refresh();window.addEventListener('load',refresh,{once:true});document.fonts?.ready.then(refresh);$$('img').filter(i=>!i.complete).forEach(i=>i.addEventListener('load',refresh,{once:true}));
}
// Keep the reference navigation readable as it crosses light sections.
let navTick=false;function updateNav(){navTick=false;const scrolled=scrollY>100;$$('nav').forEach(n=>{n.classList.toggle('k-nav-scrolled',scrolled);$$('img[alt="Arafath Tours"]',n).forEach(im=>{if(!im.dataset.initialSrc)im.dataset.initialSrc=im.getAttribute('src');im.src=scrolled?'/assets/logo-dark.svg':im.dataset.initialSrc})})}updateNav();window.addEventListener('scroll',()=>{if(!navTick){navTick=true;requestAnimationFrame(updateNav)}},{passive:true});
})();
