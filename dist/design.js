(() => {
'use strict';
const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>Array.from(r.querySelectorAll(s));
const reduced=matchMedia('(prefers-reduced-motion: reduce)');
let lenis;
// Lenis controls document scrolling only; dialogs and mobile menus use native scrolling.
if(window.Lenis&&window.gsap&&!reduced.matches){lenis=new Lenis({duration:1.05,smoothWheel:true,syncTouch:false,anchors:true,prevent:node=>!!node.closest('dialog,#mobile-menu')});lenis.on('scroll',()=>window.ScrollTrigger?.update());gsap.ticker.add(time=>lenis.raf(time*1000));gsap.ticker.lagSmoothing(0)}
function lock(){document.body.classList.add('dialog-open');lenis?.stop()}
function unlock(){document.body.classList.remove('dialog-open');if(!document.body.classList.contains('menu-open'))lenis?.start()}
const menu=$('#mobile-menu'),toggle=$('.menu-toggle');
function setMenu(open){menu.hidden=!open;toggle.setAttribute('aria-expanded',String(open));toggle.setAttribute('aria-label',open?'Close menu':'Open menu');document.body.classList.toggle('menu-open',open);open?lenis?.stop():lenis?.start()}
toggle.addEventListener('click',()=>setMenu(menu.hidden));menu.addEventListener('click',e=>{if(e.target.closest('a'))setMenu(false)});document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!menu.hidden){setMenu(false);toggle.focus()}});document.addEventListener('click',e=>{if(!menu.hidden&&!e.target.closest('.header'))setMenu(false)});
const header=$('.header');const updateHeader=()=>header.classList.toggle('is-scrolled',scrollY>45);updateHeader();window.addEventListener('scroll',updateHeader,{passive:true});
// Video playback starts muted and inline, resumes on tab return, and can be paused.
$$('[data-ambient]').forEach(video=>{const control=$('.video-toggle',video.parentElement);let manualPause=reduced.matches;video.muted=true;video.defaultMuted=true;video.playsInline=true;video.loop=true;const label=()=>{const paused=video.paused;control.innerHTML=paused?'▶ <span>Play film</span>':'Ⅱ <span>Pause film</span>';control.setAttribute('aria-label',paused?'Play background video':'Pause background video');control.setAttribute('aria-pressed',String(paused))};const play=()=>{if(!manualPause&&!document.hidden)video.play().then(label).catch(label)};control.addEventListener('click',()=>{manualPause=!video.paused;if(video.paused){manualPause=false;video.play().then(label).catch(label)}else{video.pause();label()}});video.addEventListener('play',label);video.addEventListener('pause',label);video.addEventListener('loadeddata',play);if(manualPause)video.pause();else play();document.addEventListener('visibilitychange',()=>{if(document.hidden)video.pause();else play()});window.addEventListener('pageshow',play);reduced.addEventListener('change',e=>{manualPause=e.matches;if(e.matches)video.pause();else play()});});
// Native dialogs retain focus trapping and Escape behavior.
$$('dialog').forEach(d=>{d.setAttribute('data-lenis-prevent','');$('.dialog-close',d).addEventListener('click',()=>d.close());d.addEventListener('close',unlock);d.addEventListener('click',e=>{if(e.target===d){const r=d.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)d.close()}})});
const photos=$$('[data-photo]'),photoDialog=$('#photo-dialog');let currentPhoto=0;
function renderPhoto(index){currentPhoto=(index+photos.length)%photos.length;const button=photos[currentPhoto],source=$('img',button),im=$('img',photoDialog);im.src=source.src;im.alt=source.alt;$('.photo-caption p',photoDialog).textContent=`${currentPhoto+1} / ${photos.length} · ${$('strong',button).textContent}`}
photos.forEach((button,i)=>button.addEventListener('click',()=>{renderPhoto(i);photoDialog.showModal();lock()}));$('[data-photo-prev]').addEventListener('click',()=>renderPhoto(currentPhoto-1));$('[data-photo-next]').addEventListener('click',()=>renderPhoto(currentPhoto+1));photoDialog.addEventListener('keydown',e=>{if(e.key==='ArrowLeft'){e.preventDefault();renderPhoto(currentPhoto-1)}if(e.key==='ArrowRight'){e.preventDefault();renderPhoto(currentPhoto+1)}});
const cab=$('#cab-dialog'),cabForm=$('#cab-form');
function openCab(route='',vehicle=''){cabForm.reset();if(route.includes(' ↔ ')){const [from,to]=route.split(' ↔ ');cabForm.elements.Pickup.value=from;cabForm.elements.Destination.value=to}else cabForm.elements.Notes.value=route;if(vehicle)cabForm.elements.Vehicle.value=vehicle;cab.showModal();lock()}
$$('[data-route]').forEach(b=>b.addEventListener('click',()=>openCab(b.dataset.route)));$$('[data-vehicle]').forEach(b=>b.addEventListener('click',()=>openCab('',b.dataset.vehicle)));
$$('input[type=date]').forEach(i=>{const now=new Date();now.setMinutes(now.getMinutes()-now.getTimezoneOffset());i.min=now.toISOString().slice(0,10)});
[cabForm,$('#tour-form')].filter(Boolean).forEach(form=>form.addEventListener('submit',e=>{e.preventDefault();if(!form.reportValidity())return;const lines=[form===cabForm?'Arafath Tours — Cab Enquiry':'Arafath Tours — Vaikom Enquiry',''];for(const [key,value] of new FormData(form))if(String(value).trim())lines.push(`${key}: ${value}`);lines.push('','Please confirm availability and journey details.');window.open('https://wa.me/919947478328?text='+encodeURIComponent(lines.join('\n')),'_blank','noopener')}));
$$('[data-filter]').forEach(b=>b.addEventListener('click',()=>{$$('[data-filter]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));$$('[data-category]').forEach(card=>{card.hidden=b.dataset.filter!=='All experiences'&&card.dataset.category!==b.dataset.filter});window.ScrollTrigger?.refresh()}));
// Motion applies to complete content blocks. No fractured headings, pinning or giant stickers.
if(window.gsap&&window.ScrollTrigger){gsap.registerPlugin(ScrollTrigger);const mm=gsap.matchMedia();mm.add('(prefers-reduced-motion: no-preference)',()=>{
 const hero=$('.hero');if(hero){gsap.fromTo('.hero-content>*',{y:22,autoAlpha:0},{y:0,autoAlpha:1,duration:.95,stagger:.12,ease:'power3.out',clearProps:'transform,opacity,visibility'});gsap.to($('.ambient-video',hero),{yPercent:12,ease:'none',scrollTrigger:{trigger:hero,start:'top top',end:'bottom top',scrub:1}})}
 // Gentle continuous motion stays inside each vehicle display area.
 $$('.fleet-car').forEach((car,i)=>gsap.fromTo(car,{y:-3,scale:1,transformOrigin:'50% 50%'},{y:3,scale:1.008,duration:5+i,repeat:-1,yoyo:true,ease:'sine.inOut'}));
 // Original cloud artwork and the earlier 18-second drifting movement.
 $$('.cloud-left img,.cloud-center img').forEach(el=>gsap.to(el,{x:35,y:8,duration:18,repeat:-1,yoyo:true,ease:'sine.inOut'}));
 $$('.hero-cloud').forEach((el,i)=>gsap.to(el,{xPercent:i===0?-10:i===2?10:0,y: i===1?35:15,ease:'none',scrollTrigger:{trigger:'.hero',start:'top top',end:'bottom top',scrub:1.2}}));
 $$('[data-reveal]').forEach(el=>gsap.fromTo(el,{y:24},{y:0,duration:.85,ease:'power3.out',scrollTrigger:{trigger:el,start:'top 94%',once:true}}));
 $$('[data-stamp]').forEach((el,i)=>gsap.fromTo(el,{rotation:i%2?13:-13,y:14},{rotation:i%2?5:-5,y:-5,ease:'none',scrollTrigger:{trigger:el.parentElement,start:'top bottom',end:'bottom 35%',scrub:1.2}}));
 $$('.ribbon').forEach(el=>gsap.fromTo($('.ribbon-track',el),{x:-80},{x:-500,ease:'none',scrollTrigger:{trigger:el,start:'top bottom',end:'bottom top',scrub:1.1}}));
 const wipe=document.createElement('div');wipe.className='page-transition';wipe.setAttribute('aria-hidden','true');document.body.append(wipe);
 const reset=()=>{gsap.killTweensOf(wipe);gsap.set(wipe,{opacity:0});wipe.classList.remove('active')};window.addEventListener('pageshow',reset);document.addEventListener('visibilitychange',()=>{if(!document.hidden)reset()});
 document.addEventListener('click',e=>{const a=e.target.closest('a');if(!a||e.defaultPrevented||e.button!==0||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey||a.target==='_blank'||a.hasAttribute('download'))return;const url=new URL(a.href,location.href);if(url.origin!==location.origin||url.pathname===location.pathname||url.hash)return;e.preventDefault();wipe.classList.add('active');gsap.to(wipe,{opacity:1,duration:.18,ease:'power1.out',onComplete:()=>location.assign(url.href)});setTimeout(reset,1600)});
 return()=>wipe.remove();
 });
 const refresh=()=>ScrollTrigger.refresh();window.addEventListener('load',refresh,{once:true});document.fonts?.ready.then(refresh);
}
})();
