async function loadPosts(){
 const el=document.querySelector("#posts");
 try{
  const posts=await fetch("posts.json?"+Date.now()).then(r=>r.json());
  el.innerHTML=posts.map(p=>'<article class="card"><span class="tag">'+escapeHtml(p.category||"NEWS")+'</span><h3>'+escapeHtml(p.title)+'</h3><p>'+escapeHtml(p.summary)+'</p><a href="'+safeUrl(p.url)+'" target="_blank" rel="noopener noreferrer">Read signal →</a></article>').join("");
  document.querySelector("#updated").textContent=posts[0]?.date?"Updated "+posts[0].date:"No update date";
 }catch(e){el.innerHTML="<p>Signals temporarily unavailable.</p>";}
}
function escapeHtml(s){return String(s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[c]))}
function safeUrl(s){try{const u=new URL(s,location.href);return ["http:","https:","file:"].includes(u.protocol)?u.href:"#"}catch{return "#"}}
loadPosts();
