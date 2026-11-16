(function(){
var $=function(s,r){return (r||document).querySelector(s)},$$=function(s,r){return [].slice.call((r||document).querySelectorAll(s))};
var still=matchMedia('(prefers-reduced-motion: reduce)').matches,root=document.documentElement,say=$('#say');
function seen(el,fn,th){if(!('IntersectionObserver' in window)){fn();return}var o=new IntersectionObserver(function(e){if(e[0].isIntersecting){o.disconnect();fn()}},{threshold:th||.35});o.observe(el)}

/* theme */
var tt=$('#theme-t');function setTheme(t){root.setAttribute('data-theme',t);tt.textContent=t==='dark'?'Light':'Dark';try{localStorage.setItem('theme',t)}catch(e){}
  var m=$('meta[name=theme-color]');if(m)m.content=t==='dark'?'#111110':'#f3f1eb'}
setTheme(root.getAttribute('data-theme')||'light');
function flip(){setTheme(root.getAttribute('data-theme')==='dark'?'light':'dark')}
$('#theme').onclick=flip;

/* top bar + scroll spy */
var bar=$('#topbar'),navs=$$('.nav a'),secs=navs.map(function(a){return $(a.getAttribute('href'))});
function spy(){bar.classList.toggle('stuck',scrollY>8);var y=scrollY+innerHeight*.35,cur=-1;secs.forEach(function(s,i){if(s&&s.offsetTop<=y)cur=i});
  navs.forEach(function(a,i){a.classList.toggle('on',i===cur)})}
addEventListener('scroll',spy,{passive:true});spy();

/* data flow */
var sts=$$('.st'),pns=$$('.pn'),timer=null,stageBox=$('#stages');
function pick(i,quiet){sts.forEach(function(b,j){var on=j===i;b.setAttribute('aria-expanded',on);pns[j].hidden=!on});
  if(!quiet&&say)say.textContent=sts[i].querySelector('b').textContent+' selected'}
function stop(){if(timer){clearTimeout(timer);timer=null}sts.forEach(function(b){b.classList.remove('pulse')})}
function run(){stop();if(still){pick(3,true);return}var i=0;(function step(){sts.forEach(function(b){b.classList.remove('pulse')});
  if(i>=sts.length){pick(3,true);timer=null;return}sts[i].classList.add('pulse');pick(i,true);i++;timer=setTimeout(step,850)})()}
sts.forEach(function(b,i){b.onclick=function(){stop();pick(i)}});
pick(0,true);$('#run').onclick=run;if(innerWidth>1000)seen(stageBox,run,.5);

/* 25 workbooks fold into one refresh */
var icons=$$('#grid25 .x'),model=$('.model'),folding=false;
function fold(){if(folding)return;if(still){return}folding=true;model.classList.add('wait');icons.forEach(function(x){x.classList.remove('sent')});
  icons.forEach(function(x,i){setTimeout(function(){x.classList.add('sent')},200+i*45)});
  setTimeout(function(){model.classList.remove('wait');model.classList.add('hit');setTimeout(function(){model.classList.remove('hit')},260)},200+25*45+250);
  setTimeout(function(){icons.forEach(function(x,i){setTimeout(function(){x.classList.remove('sent')},i*18)});folding=false},200+25*45+1500)}
$('#replay').onclick=fold;seen($('#fold'),fold,.6);

/* close-speed bars grow from zero */
var sp=$('#speed');if(!still){sp.classList.add('wait');seen(sp,function(){setTimeout(function(){sp.classList.remove('wait')},150)},.5)}

/* the night it broke / now */
var night=$('#night');$$('.tog button',night).forEach(function(b){b.onclick=function(){night.setAttribute('data-s',b.dataset.s);
  $$('.tog button',night).forEach(function(c){c.setAttribute('aria-pressed',c===b)})}});

/* live BreakoutAI status: read only the first 400 bytes of each public file */
var base='https://raw.githubusercontent.com/Bhavanmehta/BreakoutAI-data/main/';
function head(path){return fetch(base+path,{headers:{Range:'bytes=0-399'}}).then(function(r){if(!r.ok)throw 0;return r.text()}).then(function(t){
  t=t.slice(0,1200);var g=/"generated_at":\s*"([^"]+)"/.exec(t),a=/"as_of_date":\s*"([^"]+)"/.exec(t),c=/"count":\s*(\d+)/.exec(t);if(!c||!a)throw 0;return {g:g&&g[1],a:a[1],c:+c[1]}})}
function num(n){return n.toLocaleString('en-US')}
Promise.all([head('us/breakouts.json'),head('breakouts.json')]).then(function(r){
  $('#lv-us').textContent=num(r[0].c);$('#lv-us-d').textContent='as of '+r[0].a;$('#lv-in').textContent=num(r[1].c);$('#lv-in-d').textContent='as of '+r[1].a;
  if(r[0].g)$('#lv-g').textContent='Generated '+r[0].g.slice(0,16).replace('T',' ')+' UTC. This card reads the first 400 bytes of the public output file.';
  var s=$('#live-s');s.textContent='Live';s.classList.add('on')}).catch(function(){});

/* copy email, print */
var cp=$('#copy');function copy(){var done=function(){cp.textContent='Copied';if(say)say.textContent='Email copied';setTimeout(function(){cp.textContent='Copy email'},1600)};
  if(navigator.clipboard)navigator.clipboard.writeText('bhavanmehtap@gmail.com').then(done,function(){});}
cp.onclick=copy;$('#print').onclick=function(){print()};

/* command menu */
var pal=$('#pal'),q=$('#pal-q'),list=$('#pal-l'),sel=0,last=null;
function go(h){return function(){location.hash=h}}
var cmds=[['Data flow','Section',go('#flow')],['Before and after','Section',go('#results')],['Experience','Section',go('#experience')],['Off the clock: BreakoutAI and Ledger','Section',go('#personal')],
 ['How I work','Section',go('#how')],['Toolkit and education','Section',go('#skills')],['Contact','Section',go('#contact')],['Back to top','Section',go('#top')],
 ['Copy email','Action',copy],['Switch colour theme','Action',flip],['Run the data flow','Action',function(){location.hash='#flow';setTimeout(run,400)}],
 ['Open resume (PDF)','Link',function(){location.href='resume.pdf'}],['Open GitHub','Link',function(){open('https://github.com/Bhavanmehta')}],['Open LinkedIn','Link',function(){open('https://www.linkedin.com/in/bhavan-mehta')}],
 ['Print or save as PDF','Action',function(){print()}]],shown=cmds;
function draw(){var v=q.value.trim().toLowerCase();shown=cmds.filter(function(c){return c[0].toLowerCase().indexOf(v)>-1});if(sel>=shown.length)sel=0;
  list.innerHTML=shown.map(function(c,i){return '<li role="option" data-i="'+i+'" aria-selected="'+(i===sel)+'">'+c[0]+'<small>'+c[1]+'</small></li>'}).join('')||'<li>No match</li>';
  var s=list.querySelector('[aria-selected=true]');if(s)s.scrollIntoView({block:'nearest'})}
function openPal(){last=document.activeElement;pal.hidden=false;q.value='';sel=0;draw();q.focus()}
function closePal(){pal.hidden=true;if(last&&last.focus)last.focus()}
function fire(i){var c=shown[i];if(!c)return;closePal();c[2]()}
$('#kbtn').onclick=openPal;pal.onclick=function(e){if(e.target===pal)closePal()};q.oninput=function(){sel=0;draw()};
list.onclick=function(e){var li=e.target.closest('li[data-i]');if(li)fire(+li.dataset.i)};
addEventListener('keydown',function(e){
  if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='k'){e.preventDefault();pal.hidden?openPal():closePal();return}
  if(pal.hidden)return;
  if(e.key==='Escape'){closePal()}else if(e.key==='ArrowDown'){e.preventDefault();sel=(sel+1)%Math.max(shown.length,1);draw()}
  else if(e.key==='ArrowUp'){e.preventDefault();sel=(sel-1+shown.length)%Math.max(shown.length,1);draw()}
  else if(e.key==='Enter'){e.preventDefault();fire(sel)}else if(e.key==='Tab'){e.preventDefault();q.focus()}});
if(/Mac|iPhone|iPad/.test(navigator.platform||'')){var k=$('#kbtn kbd');if(k)k.textContent='Cmd K'}
})();
