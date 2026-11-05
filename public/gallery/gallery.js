(()=>{
const galleries={
 billboards:[["billboard-awareness.jpg","Community fentanyl-awareness billboard: it only takes one time"],["billboard-candy.jpg","Check your candy: a billboard featuring James and other young lives"],["billboard-justice.jpg","Justice for James Jolley: forever 17"]],
 bond:[["bond-first-kiss.jpg","A father and son, a lifetime of love"],["bond-recording-studio.jpg","James in the recording studio"],["bond-cat.jpg","James holding his cat"],["bond-doorway.jpg","James during his teenage years"],["bond-childhood-fun.jpg","A joyful childhood memory"],["bond-young-james.jpg","Young James"],["bond-childhood-pet.jpg","James and a beloved family pet"],["bond-poolside.jpg","James enjoying a summer day"],["bond-father-son-smile.jpg","A happy memory together"],["bond-father-son.jpg","Father and son together"]]
};
for(const [name,photos] of Object.entries(galleries)){
const wrap=document.querySelector('[data-gallery="'+name+'"]');if(!wrap)continue;
const viewport=wrap.querySelector('.photo-stage'),dots=wrap.querySelector('.gallery-dots'),live=wrap.querySelector('.gallery-caption');
let current=0,timer=null,playing=true,inView=true;const motion=window.matchMedia('(prefers-reduced-motion: reduce)');
const slides=[];
photos.forEach(([filename,label],index)=>{
 const slide=document.createElement('figure');slide.className='gallery-slide';slide.hidden=index!==0;
 const img=document.createElement('img');img.src='/public/gallery/photos/'+filename;img.alt=label;img.loading=index===0?'eager':'lazy';img.decoding='async';
 img.onerror=()=>{img.hidden=true;slide.classList.add('photo-unavailable');const p=document.createElement('p');p.className='photo-notice';p.textContent='This photo is temporarily unavailable.';slide.appendChild(p);};
 const caption=document.createElement('figcaption');caption.textContent=label;slide.append(img,caption);viewport.appendChild(slide);slides.push(slide);
 const dot=document.createElement('button');dot.type='button';dot.setAttribute('aria-label','Show '+label);dot.className='gallery-dot';dot.addEventListener('click',()=>show(index,true));dots.appendChild(dot);
});
const dotButtons=[...dots.children];
function show(index,reset){
 current=(index+slides.length)%slides.length;
 slides.forEach((slide,i)=>{slide.hidden=i!==current;slide.setAttribute('aria-hidden',String(i!==current))});
 dotButtons.forEach((dot,i)=>{dot.classList.toggle('active',i===current);dot.setAttribute('aria-current',String(i===current))});
 live.textContent=photos[current][1];
 if(reset)restart();
}
function stop(){clearInterval(timer);timer=null;}
function play(){stop();if(playing&&inView&&!document.hidden&&!motion.matches)timer=setInterval(()=>show(current+1,false),5500)}
function restart(){if(playing)play()}
wrap.querySelector('.gallery-prev').addEventListener('click',()=>show(current-1,true));
wrap.querySelector('.gallery-next').addEventListener('click',()=>show(current+1,true));
const toggle=wrap.querySelector('.gallery-play');
toggle.addEventListener('click',()=>{playing=!playing;toggle.textContent=playing?'Pause':'Play';toggle.setAttribute('aria-label',playing?'Pause slideshow':'Play slideshow');playing?play():stop()});
let startX=null,startY=null;viewport.addEventListener('touchstart',e=>{startX=e.changedTouches[0].clientX;startY=e.changedTouches[0].clientY},{passive:true});
viewport.addEventListener('touchend',e=>{if(startX===null)return;const dx=e.changedTouches[0].clientX-startX,dy=e.changedTouches[0].clientY-startY;if(Math.abs(dx)>42&&Math.abs(dx)>Math.abs(dy)*1.25)show(current+(dx<0?1:-1),true);startX=null;startY=null},{passive:true});
let mouseX=null;viewport.addEventListener('pointerdown',e=>{if(e.pointerType==='mouse')mouseX=e.clientX});viewport.addEventListener('pointerup',e=>{if(mouseX===null)return;const dx=e.clientX-mouseX;if(Math.abs(dx)>60)show(current+(dx<0?1:-1),true);mouseX=null});
wrap.addEventListener('mouseenter',stop);wrap.addEventListener('mouseleave',play);
wrap.addEventListener('focusin',stop);wrap.addEventListener('focusout',play);
document.addEventListener('visibilitychange',()=>document.hidden?stop():play());
if('IntersectionObserver' in window){const observer=new IntersectionObserver(entries=>{inView=entries[0].isIntersecting;inView?play():stop()},{threshold:.15});observer.observe(wrap)}
if(motion.addEventListener)motion.addEventListener('change',()=>play());
show(0,false);play();
}
})();