/* Progressive enhancement: destination links and enquiry work without WebGL. */
const $ = (s) => document.querySelector(s);
const $$ = (s) => [...document.querySelectorAll(s)];
const reduced = matchMedia('(prefers-reduced-motion: reduce)');
const colors = {Mountains:0xd6e99b,Backwaters:0x88d9d0,Coast:0xf6d79b,Culture:0xf0ad87,Wild:0x9ecda0};
let destinations = [], selected = 'munnar', category = 'All places', query = '', sceneAPI;
let tour = false, paused = reduced.matches, tourElapsed = 0, tourStep = 0;
const itinerary = ['fort-kochi','munnar','thekkady','kumarakom','alappuzha','varkala','wayanad','bekal'];
const cleanName = (s) => s.toLocaleLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'');
const matching = () => destinations.filter(d => (category==='All places'||d.category===category) && cleanName(`${d.name} ${d.category} ${d.highlights.join(' ')}`).includes(query));

function setTour(value) {
 tour=value; tourElapsed=0;
 $('#atlas-tour').setAttribute('aria-pressed',String(tour));
 $('#tour-label').textContent=tour?'Pause scenic route':'Take the scenic route';
 $('#tour-icon').textContent=tour?'Ⅱ':'▶';
 $('.tour-progress span').style.transform='scaleX(0)';
}
function select(id,{flight=true,stopTour=true}={}) {
 const d=destinations.find(d=>d.id===id); if(!d)return;
 selected=id;if(stopTour)setTour(false);
 $('#atlas-name').textContent=d.name;$('#atlas-category').textContent=d.category;
 $('#atlas-line').textContent=d.line;$('#atlas-number').textContent=`${String(destinations.indexOf(d)+1).padStart(2,'0')} / ${destinations.length}`;
 $('#atlas-highlights').replaceChildren(...d.highlights.map(text=>{const li=document.createElement('li');li.textContent=text;return li;}));
 const photo=$('#atlas-photo');$('.story-photo').hidden=!d.image;$('.atlas-story').classList.toggle('no-photo',!d.image);
 if(d.image){photo.src=d.image;photo.alt=`${d.name}, Kerala`;$('#story-photo-caption').textContent=`${d.name.toUpperCase()}, KERALA`;}
 $('#atlas-enquire').href='https://wa.me/919947478328?text='+encodeURIComponent(`Hello Arafath, I’m exploring Kerala and would like to plan a journey to ${d.name}. Please help me with the itinerary and transport.`);
 $('#atlas-coordinates').textContent=`${d.lat.toFixed(3)}° N · ${d.lon.toFixed(3)}° E`;
 $$('[data-pin]').forEach(p=>p.setAttribute('aria-pressed',String(p.dataset.pin===id)));
 $$('.atlas-place').forEach(p=>p.classList.toggle('is-selected',p.dataset.placeId===id));
 sceneAPI?.select(d,flight);
}
function filter() {
 const visible=matching(), ids=new Set(visible.map(d=>d.id));
 $$('[data-atlas-filter]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.atlasFilter===category)));
 $$('.atlas-place').forEach(p=>p.hidden=!ids.has(p.dataset.placeId));
 $('#atlas-count').textContent=`${visible.length} ${visible.length===1?'place':'places'} to discover`;
 $('#atlas-empty').hidden=visible.length>0;sceneAPI?.filter(ids);
 if(visible.length&&!ids.has(selected))select(visible[0].id);
 window.ScrollTrigger?.refresh();
}
function startUI() {
 $$('[data-select-place]').forEach(b=>b.addEventListener('click',()=>{
  const d=destinations.find(d=>d.id===b.dataset.selectPlace);if(!d)return;
  if(!matching().some(x=>x.id===d.id)){category='All places';query='';$('#atlas-search').value='';filter();}
  select(d.id);$('#atlas-status').textContent=`Exploring ${d.name}. ${d.line}`;
 }));
 $$('[data-pin]').forEach(b=>b.addEventListener('click',()=>select(b.dataset.pin)));
 $$('[data-atlas-filter]').forEach(b=>b.addEventListener('click',()=>{setTour(false);category=b.dataset.atlasFilter;filter();}));
 $('#atlas-search').addEventListener('input',e=>{setTour(false);query=cleanName(e.target.value.trim());filter();});
 for(const [id,step] of [['atlas-prev',-1],['atlas-next',1]])$('#'+id).addEventListener('click',()=>{const ds=matching();if(!ds.length)return;const i=ds.findIndex(d=>d.id===selected);select(ds[(i+step+ds.length)%ds.length].id);});
 select('munnar',{flight:false});
}
function failure(message) {
 $('#atlas-help').textContent=message;$('#atlas-status').textContent=message;
 $('#atlas-world').classList.remove('atlas-ready');$$('[data-pin]').forEach(p=>p.hidden=true);
 $$('.atlas-view-controls button,.atlas-zoom button,.atlas-playbar button').forEach(b=>b.disabled=true);
}
async function init() {
 const response=await fetch('/assets/atlas/destinations.json');if(!response.ok)throw new Error('Destination data unavailable');
 destinations=await response.json();startUI();
 try {
  const [THREE,response]=await Promise.all([import('/assets/vendor/three.module.js'),fetch('/assets/atlas/kerala-terrain.json')]);
  if(!response.ok)throw new Error('Terrain unavailable');
  buildWorld(THREE,await response.json());
 } catch(error){console.warn('Kerala atlas:',error);failure('The 3D view is unavailable here. Explore every destination below.');}
}

function buildWorld(T, terrain) {
 const stage=$('#atlas-stage'),world=$('#atlas-world');
 const renderer=new T.WebGLRenderer({alpha:true,antialias:true,powerPreference:'low-power'});
 renderer.setPixelRatio(Math.min(devicePixelRatio,1.65));renderer.setClearColor(0x092723,0);
 renderer.outputColorSpace=T.SRGBColorSpace;renderer.toneMapping=T.ACESFilmicToneMapping;renderer.toneMappingExposure=1.26;
 renderer.domElement.setAttribute('aria-hidden','true');stage.append(renderer.domElement);
 const scene=new T.Scene();scene.fog=new T.FogExp2(0x092723,.014);
 const camera=new T.PerspectiveCamera(36,1,.1,130);
 const group=new T.Group();scene.add(group);
 scene.add(new T.HemisphereLight(0xe6f2d1,0x233c31,2.4));
 const sun=new T.DirectionalLight(0xffefca,3.1);sun.position.set(-8,15,3);scene.add(sun);
 const rim=new T.DirectionalLight(0xa2e3ce,1.6);rim.position.set(9,7,-12);scene.add(rim);
 const geo=(lon,lat)=>new T.Vector3((lon-76.15)*4.8,0,(10.50-lat)*4.8);
 const gaussian=(x,z,a,b,sx,sz)=>Math.exp(-((x-a)**2/sx**2+(z-b)**2/sz**2));
 function elevation(lon,lat){
  let h=1.7*gaussian(lon,lat,77.10,10.12,.34,.39)+1.18*gaussian(lon,lat,76.10,11.70,.31,.47)+1.08*gaussian(lon,lat,76.57,11.14,.29,.30)+1.0*gaussian(lon,lat,77.13,9.48,.25,.6)+.78*gaussian(lon,lat,77.14,8.79,.21,.3)+.44*gaussian(lon,lat,75.65,12.12,.32,.6);
  const ridge=.72+.18*Math.sin(lon*65+Math.sin(lat*33)*1.8)+.1*Math.sin(lat*99+lon*24);
  return .12+h*ridge+.025*Math.sin(lon*182)*Math.sin(lat*137);
 }
 const point=(lon,lat)=>{const p=geo(lon,lat);p.y=elevation(lon,lat);return p;};
 const coords=[],vertexColors=[];const low=new T.Color('#376947'),mid=new T.Color('#86a65c'),high=new T.Color('#cad492');
 terrain.vertices.forEach(([lon,lat])=>{const p=point(lon,lat);coords.push(p.x,p.y,p.z);const c=low.clone().lerp(mid,Math.min(1,p.y/.9));if(p.y>.9)c.lerp(high,Math.min(.8,(p.y-.9)*.65));const variation=.88+.12*Math.sin(lon*134+lat*197);c.multiplyScalar(variation);vertexColors.push(c.r,c.g,c.b);});
 const geometry=new T.BufferGeometry();geometry.setAttribute('position',new T.Float32BufferAttribute(coords,3));geometry.setAttribute('color',new T.Float32BufferAttribute(vertexColors,3));geometry.setIndex(terrain.triangles.flat());geometry.computeVertexNormals();
 const landMaterial=new T.MeshStandardMaterial({vertexColors:true,roughness:.9,metalness:0,side:T.DoubleSide});
 landMaterial.onBeforeCompile=shader=>{
  shader.vertexShader=shader.vertexShader.replace('#include <common>','#include <common>\nvarying float vElevation;').replace('#include <begin_vertex>','#include <begin_vertex>\nvElevation = position.y;');
  shader.fragmentShader=shader.fragmentShader.replace('#include <common>','#include <common>\nvarying float vElevation;').replace('#include <color_fragment>','#include <color_fragment>\nfloat band = abs(fract(vElevation * 11.0) - 0.5); float contour = 1.0-smoothstep(0.018,0.05,band); diffuseColor.rgb *= 1.0-contour*0.16;');
 };
 const land=new T.Mesh(geometry,landMaterial);group.add(land);
 // Continuous geographic shoreline and exposed relief sides.
 const sidePositions=[],sideColors=[],boundary=terrain.boundary.map(([a,b])=>point(a,b));
 for(let i=0;i<boundary.length-1;i++){
  const a=boundary[i],b=boundary[i+1],base=-.53;
  sidePositions.push(a.x,a.y,a.z,b.x,b.y,b.z,a.x,base,a.z,b.x,b.y,b.z,b.x,base,b.z,a.x,base,a.z);
  for(let k=0;k<6;k++){const c=new T.Color(k===0||k===1||k===3?'#65836a':'#182e29');sideColors.push(c.r,c.g,c.b);}
 }
 const sides=new T.BufferGeometry();sides.setAttribute('position',new T.Float32BufferAttribute(sidePositions,3));sides.setAttribute('color',new T.Float32BufferAttribute(sideColors,3));sides.computeVertexNormals();
 group.add(new T.Mesh(sides,new T.MeshStandardMaterial({vertexColors:true,roughness:.96,side:T.DoubleSide})));
 const outline=new T.BufferGeometry().setFromPoints(boundary.map(p=>p.clone().add(new T.Vector3(0,.018,0))));
 group.add(new T.Line(outline,new T.LineBasicMaterial({color:0xc8dda5,transparent:true,opacity:.40})));
 // Animated sea is a single inexpensive shader surface, not downloaded map tiles.
 const oceanMaterial=new T.ShaderMaterial({transparent:true,depthWrite:false,uniforms:{uTime:{value:0}},vertexShader:'varying vec3 vPos;void main(){vPos=position;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0);}',fragmentShader:`varying vec3 vPos;uniform float uTime;void main(){vec2 p=vPos.xy;float r=length(p/vec2(21.0,24.0));float fade=1.0-smoothstep(.35,1.0,r);float w=sin(p.y*4.3+sin(p.x*.8+uTime*.12)*1.4-uTime*.32);float w2=sin(p.y*7.2+p.x*.3-uTime*.2);float foam=pow(max(w,0.0),24.0)*.07+pow(max(w2,0.0),50.0)*.025;vec3 col=vec3(.065,.22,.195)+foam*vec3(.65,.88,.69);gl_FragColor=vec4(col,fade*.8);}`});
 const ocean=new T.Mesh(new T.PlaneGeometry(50,56),oceanMaterial);ocean.rotation.x=-Math.PI/2;ocean.position.y=-.64;scene.add(ocean);
 // A few translucent clouds use the website's existing photographic cloud artwork.
 const clouds=[];const texture=new T.TextureLoader().load('/assets/clouds/cloud-soft.png');texture.colorSpace=T.SRGBColorSpace;
 [[76.6,10.55,6.4],[75.95,11.85,5.7],[77.05,9.25,4.9]].forEach(([lon,lat,size],i)=>{
  const cloud=new T.Sprite(new T.SpriteMaterial({map:texture,transparent:true,opacity:.09,depthWrite:false,color:0xc7e3cd}));cloud.position.copy(point(lon,lat));cloud.position.y+=1.6;cloud.scale.set(size,size*.5,1);cloud.userData.baseX=cloud.position.x;cloud.userData.phase=i*2;clouds.push(cloud);group.add(cloud);
 });
 const pins=[],pickTargets=[];
 const pinGeometry=new T.SphereGeometry(.105,10,8),pickGeometry=new T.SphereGeometry(.32,8,6);
 destinations.forEach(d=>{
  const p=point(d.lon,d.lat);const stem=new T.BufferGeometry().setFromPoints([p,p.clone().add(new T.Vector3(0,.42,0))]);
  const color=colors[d.category];const line=new T.Line(stem,new T.LineBasicMaterial({color,transparent:true,opacity:.55}));group.add(line);
  const pin=new T.Mesh(pinGeometry,new T.MeshBasicMaterial({color}));pin.position.copy(p);pin.position.y+=.44;group.add(pin);
  const hit=new T.Mesh(pickGeometry,new T.MeshBasicMaterial({visible:false}));hit.position.copy(pin.position);hit.userData.id=d.id;group.add(hit);pickTargets.push(hit);
  pins.push({d,pin,line,hit,label:$(`[data-pin="${d.id}"]`)});
 });
 const ring=new T.Mesh(new T.RingGeometry(.25,.29,64),new T.MeshBasicMaterial({color:0xe5f7a2,transparent:true,opacity:.75,side:T.DoubleSide,depthWrite:false}));ring.rotation.x=-Math.PI/2;group.add(ring);
 const halo=ring.clone();halo.material=ring.material.clone();group.add(halo);
 let flightLine,flightDot,flightCurve,flightTime=1;
 function connect(from,to){
  if(flightLine){group.remove(flightLine,flightDot);flightLine.geometry.dispose();flightLine.material.dispose();flightDot.geometry.dispose();flightDot.material.dispose();}
  if(!from||from.distanceTo(to)<.2)return;
  const middle=from.clone().lerp(to,.5);middle.y+=Math.min(3,from.distanceTo(to)*.2+.6);
  flightCurve=new T.QuadraticBezierCurve3(from,middle,to);const g=new T.BufferGeometry().setFromPoints(flightCurve.getPoints(90));
  flightLine=new T.Line(g,new T.LineDashedMaterial({color:0xf2df9a,dashSize:.12,gapSize:.09,transparent:true,opacity:.65}));flightLine.computeLineDistances();group.add(flightLine);
  flightDot=new T.Mesh(new T.SphereGeometry(.075,10,8),new T.MeshBasicMaterial({color:0xfff8ce}));group.add(flightDot);flightTime=0;
 }
 let active=destinations.find(d=>d.id===selected),filtered=new Set(destinations.map(d=>d.id));
 let target=new T.Vector3(.15,.3,1.2),aim=target.clone(),yaw=-.25,pitch=.86,distance=34;
 let desiredYaw=yaw,desiredPitch=pitch,desiredDistance=distance,topView=false,overview=true;
 let width=0,height=0,visible=true,dead=false,lastTime=0,time=0,frameRequested=false;
 const mobile=()=>width<600;
 function fitDistance(){
  const small=mobile();desiredYaw=small?.45:-.25;desiredPitch=small?1.0:.86;
  const test=new T.PerspectiveCamera(36,width/height,.1,130),center=new T.Vector3(.15,.3,1.2);
  for(let d=26;d<=70;d+=.5){test.position.set(center.x+Math.sin(desiredYaw)*Math.cos(desiredPitch)*d,center.y+Math.sin(desiredPitch)*d,center.z+Math.cos(desiredYaw)*Math.cos(desiredPitch)*d);test.lookAt(center);test.updateMatrixWorld();
   if(boundary.every(p=>{const v=p.clone().project(test),x=(v.x*.5+.5)*width,y=(-v.y*.5+.5)*height;return x>30&&x<width-38&&y>64&&y<height-110;}))return d;
  }return 70;
 }
 const resize=()=>{width=stage.clientWidth;height=stage.clientHeight;camera.aspect=width/height;camera.updateProjectionMatrix();renderer.setSize(width,height,false);if(overview)desiredDistance=fitDistance();drawOnce();};
 const observer=new ResizeObserver(resize);observer.observe(stage);
 function setMotion(value){paused=value;$('#atlas-motion').textContent=paused?'Resume motion':'Pause motion';$('#atlas-motion').setAttribute('aria-pressed',String(paused));if(paused)setTour(false);lastTime=0;refreshLoop();drawOnce();}
 function reset(){setTour(false);overview=true;topView=false;target.set(.15,.3,1.2);desiredDistance=fitDistance();$('#atlas-angle').setAttribute('aria-pressed','false');drawOnce();}
 function selectDestination(d,fly){
  const previous=active?point(active.lon,active.lat).add(new T.Vector3(0,.5,0)):null;active=d;
  const p=point(d.lon,d.lat);ring.position.copy(p);ring.position.y+=.08;halo.position.copy(ring.position);
  pins.forEach(pin=>{const chosen=pin.d.id===d.id;pin.pin.scale.setScalar(chosen?1.5:1);pin.line.material.opacity=chosen?1:.45;});
  if(fly){overview=false;target.copy(p);target.y=.3;desiredDistance=mobile()?25:22;desiredPitch=topView?1.50:.88;connect(previous,p.clone().add(new T.Vector3(0,.5,0)));}
  drawOnce();
 }
 sceneAPI={select:selectDestination,filter(ids){filtered=ids;pins.forEach(p=>{p.pin.visible=ids.has(p.d.id);p.line.visible=p.pin.visible;p.hit.visible=p.pin.visible;});drawOnce();},reset};
 $('#atlas-reset').addEventListener('click',reset);
 $('#atlas-angle').addEventListener('click',()=>{setTour(false);topView=!topView;desiredPitch=topView?1.50:.82;$('#atlas-angle').setAttribute('aria-pressed',String(topView));drawOnce();});
 $('#atlas-zoom-in').addEventListener('click',()=>zoom(-3));$('#atlas-zoom-out').addEventListener('click',()=>zoom(3));
 function zoom(delta){overview=false;desiredDistance=T.MathUtils.clamp(desiredDistance+delta,14,45);drawOnce();}
 $('#atlas-motion').addEventListener('click',()=>setMotion(!paused));
 $('#atlas-tour').addEventListener('click',()=>{
  if(tour){setTour(false);return;}category='All places';query='';$('#atlas-search').value='';filter();
  if(paused)setMotion(false);setTour(true);tourStep=0;select(itinerary[0],{stopTour:false});
 });
 reduced.addEventListener('change',e=>setMotion(e.matches));
 // Vertical touch movement stays native; horizontal movement rotates the atlas.
 let drag=null;const canvas=renderer.domElement;
 canvas.addEventListener('pointerdown',e=>{if(e.button!==0)return;drag={id:e.pointerId,x:e.clientX,y:e.clientY,startX:e.clientX,startY:e.clientY,moved:false,type:e.pointerType};});
 canvas.addEventListener('pointermove',e=>{
  if(!drag||e.pointerId!==drag.id)return;const dx=e.clientX-drag.x,dy=e.clientY-drag.y,totalX=e.clientX-drag.startX,totalY=e.clientY-drag.startY;
  if(drag.type==='touch'&&!drag.moved&&Math.abs(totalY)>Math.abs(totalX)&&Math.abs(totalY)>6){drag=null;return;}
  if(Math.hypot(totalX,totalY)>5){drag.moved=true;setTour(false);canvas.setPointerCapture(e.pointerId);desiredYaw-=dx*.006;if(drag.type!=='touch')desiredPitch=T.MathUtils.clamp(desiredPitch+dy*.004,.45,1.52);overview=false;}
  drag.x=e.clientX;drag.y=e.clientY;drawOnce();
 });
 const raycaster=new T.Raycaster();
 canvas.addEventListener('pointerup',e=>{if(!drag)return;const moved=drag.moved;drag=null;if(canvas.hasPointerCapture(e.pointerId))canvas.releasePointerCapture(e.pointerId);if(moved)return;
  const rect=canvas.getBoundingClientRect();raycaster.setFromCamera(new T.Vector2((e.clientX-rect.left)/rect.width*2-1,-(e.clientY-rect.top)/rect.height*2+1),camera);
  const hit=raycaster.intersectObjects(pickTargets.filter(p=>filtered.has(p.userData.id)))[0];if(hit)select(hit.object.userData.id);
 });
 canvas.addEventListener('pointercancel',()=>drag=null);
 stage.addEventListener('keydown',e=>{if(!['ArrowLeft','ArrowRight','ArrowUp','ArrowDown','+','=','-','Home'].includes(e.key))return;e.preventDefault();setTour(false);if(e.key==='Home')reset();else if(e.key==='+'||e.key==='=')zoom(-3);else if(e.key==='-')zoom(3);else{overview=false;if(e.key==='ArrowLeft')desiredYaw-=.15;if(e.key==='ArrowRight')desiredYaw+=.15;if(e.key==='ArrowUp')desiredPitch=Math.min(1.5,desiredPitch+.12);if(e.key==='ArrowDown')desiredPitch=Math.max(.45,desiredPitch-.12);}drawOnce();});
 // Wheel remains document scrolling; explicit controls make map zoom deliberate.
 const projected=new T.Vector3();
 const major=new Set(['bekal','wayanad','kozhikode','athirappilly','fort-kochi','munnar','alappuzha','thekkady','varkala','kovalam']);
 function labels(){
  const occupied=[];
  const sorted=[...pins].sort((a,b)=>(b.d.id===selected?100:major.has(b.d.id)?10:0)-(a.d.id===selected?100:major.has(a.d.id)?10:0));
  for(const p of sorted){
   projected.copy(p.pin.position).project(camera);const x=(projected.x*.5+.5)*width,y=(-projected.y*.5+.5)*height;
   const off=!filtered.has(p.d.id)||projected.z>1||x<12||x>width-12||y<50||y>height-102;
   p.label.hidden=off;if(off)continue;
   const selectedPin=p.d.id===selected;const estimated=p.d.name.length*6.6+32;const flip=x+estimated>width-8;
   const left=flip?x-estimated:x;const box={x:left,y:y-18,w:estimated,h:40};
   const overlap=occupied.some(r=>box.x<r.x+r.w&&box.x+box.w>r.x&&box.y<r.y+r.h&&box.y+box.h>r.y);
   const show=selectedPin||(!overlap&&(major.has(p.d.id)||desiredDistance<25||category!=='All places'));
   p.label.classList.toggle('label-muted',!show);p.label.style.transform=`translate(${Math.round(x-10)}px,${Math.round(y-17)}px)`;
   p.label.style.flexDirection=flip&&show?'row-reverse':'row';p.label.style.marginLeft=flip&&show?`${-estimated+26}px`:'0';
   if(show)occupied.push(box);
  }
 }
 function render(dt=0){
  if(dead)return;const snap=paused||reduced.matches;
  const ease=snap?1:1-Math.exp(-Math.max(dt,.016)*4.1);aim.lerp(target,ease);yaw=T.MathUtils.lerp(yaw,desiredYaw,ease);pitch=T.MathUtils.lerp(pitch,desiredPitch,ease);distance=T.MathUtils.lerp(distance,desiredDistance,ease);
  const drift=!paused&&!drag?Math.sin(time*.13)*.018:0;
  camera.position.set(aim.x+Math.sin(yaw+drift)*Math.cos(pitch)*distance,aim.y+Math.sin(pitch)*distance,aim.z+Math.cos(yaw+drift)*Math.cos(pitch)*distance);camera.lookAt(aim);camera.updateMatrixWorld();
  oceanMaterial.uniforms.uTime.value=time;
  if(!paused){clouds.forEach(c=>c.position.x=c.userData.baseX+Math.sin(time*.07+c.userData.phase)*.5);const pulse=1+(Math.sin(time*1.5)+1)*.32;halo.scale.setScalar(pulse);halo.material.opacity=.5/pulse;}
  if(flightDot&&flightCurve){flightTime=Math.min(1,flightTime+(snap?1:dt*.42));flightDot.position.copy(flightCurve.getPoint(flightTime));flightDot.visible=flightTime<1;}
  renderer.render(scene,camera);labels();
  const north=aim.clone().add(new T.Vector3(0,0,-1)).project(camera),origin=aim.clone().project(camera);
  $('.atlas-compass i').style.transform=`rotate(${Math.atan2(north.x-origin.x,north.y-origin.y)}rad)`;
 }
 function drawOnce(){if(frameRequested||dead||!visible||document.hidden)return;frameRequested=true;requestAnimationFrame(()=>{frameRequested=false;render(0);});}
 function loop(ms){if(!visible||document.hidden||dead)return;const dt=lastTime?Math.min((ms-lastTime)/1000,.05):.016;lastTime=ms;if(!paused)time+=dt;
  if(tour&&!paused){tourElapsed+=dt;$('.tour-progress span').style.transform=`scaleX(${Math.min(tourElapsed/7,1)})`;if(tourElapsed>=7){tourElapsed=0;tourStep=(tourStep+1)%itinerary.length;select(itinerary[tourStep],{stopTour:false});}}
  render(dt);
 }
 function refreshLoop(){renderer.setAnimationLoop(!paused&&visible&&!document.hidden&&!dead?loop:null);drawOnce();}
 const intersection=new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;lastTime=0;refreshLoop();},{threshold:.01});intersection.observe(world);
 document.addEventListener('visibilitychange',()=>{lastTime=0;refreshLoop();});
 canvas.addEventListener('webglcontextlost',e=>{e.preventDefault();renderer.setAnimationLoop(null);dead=true;sceneAPI=null;setTour(false);failure('The 3D view paused. You can still explore every place below.');});
 window.addEventListener('pagehide',e=>{if(e.persisted){renderer.setAnimationLoop(null);return;}dead=true;renderer.setAnimationLoop(null);observer.disconnect();intersection.disconnect();scene.traverse(o=>{o.geometry?.dispose();const materials=Array.isArray(o.material)?o.material:[o.material];materials.filter(Boolean).forEach(m=>m.dispose());});texture.dispose();renderer.dispose();});
 window.addEventListener('pageshow',e=>{if(e.persisted){lastTime=0;refreshLoop();}});
 $$('.atlas-view-controls button,.atlas-zoom button,.atlas-playbar button').forEach(b=>b.disabled=false);
 world.classList.add('atlas-ready');$('#atlas-help').textContent=matchMedia('(pointer:coarse)').matches?'Swipe sideways to orbit · Tap a pin · Scroll to discover':'Drag to orbit · Choose a pin · Use + / − to zoom';
 $('#atlas-status').textContent='Interactive Kerala atlas ready. 26 destinations available.';
 selectDestination(active,false);resize();distance=desiredDistance;yaw=desiredYaw;pitch=desiredPitch;setMotion(paused);
}
init().catch(error=>{console.warn('Explore Kerala:',error);failure('Explore Kerala using the destination links below.');});
