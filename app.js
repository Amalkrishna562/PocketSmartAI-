const $=id=>document.getElementById(id);
$("form").onsubmit=async e=>{e.preventDefault();$("analyze").disabled=true;$("result").textContent="PocketSmart AI is analyzing...";
try{let r=await fetch("/api/recommend",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({income:$("income").value,expenses:$("expenses").value,goal:$("goal").value,question:$("question").value})});let d=await r.json();if(!r.ok)throw Error(d.error);$("result").textContent=d.answer}catch(e){$("result").textContent="Error: "+e.message}finally{$("analyze").disabled=false}};
$("chat").onsubmit=async e=>{e.preventDefault();let q=$("chatInput").value.trim();if(!q)return;add("user",q);$("chatInput").value="";
try{let r=await fetch("/api/chat",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message:q})});let d=await r.json();if(!r.ok)throw Error(d.error);add("ai",d.answer)}catch(e){add("ai","Error: "+e.message)}};
function add(c,t){let x=document.createElement("div");x.className="msg "+c;x.textContent=t;$("messages").appendChild(x)}
$("reset").onclick=()=>location.reload();
