const state={character:"mi",mode:"chat",history:[],busy:false};
const info={
 mi:{name:"Mị",welcome:"Em đến Hồng Ngài tìm tôi à? Nếu muốn hiểu câu chuyện của tôi, em cứ hỏi. Có những điều phải kể từ những ngày tôi còn trẻ...",suggestions:["Vì sao Mị không bỏ trốn?","Đêm mùa xuân đã làm Mị thay đổi thế nào?","Vì sao Mị cắt dây trói cho A Phủ?"]},
 aphu:{name:"A Phủ",welcome:"Tôi là A Phủ. Cuộc đời tôi chẳng mấy khi được tự mình lựa chọn, nhưng tôi vẫn muốn sống theo cách của mình. Em muốn hỏi chuyện gì?",suggestions:["Vì sao A Phủ đánh A Sử?","A Phủ sống ở nhà Pá Tra thế nào?","A Phủ nghĩ gì khi được Mị cứu?"]}
};
const $=s=>document.querySelector(s), $$=s=>document.querySelectorAll(s);
function show(id){$$(".screen").forEach(x=>x.classList.remove("active"));$("#"+id).classList.add("active")}
function add(role,text,extra=""){const d=document.createElement("div");d.className=`msg ${role} ${extra}`;const b=document.createElement("div");b.className="bubble";b.textContent=text;d.appendChild(b);$("#messages").appendChild(d);$("#messages").scrollTop=$("#messages").scrollHeight;return d}
function renderSuggestions(){const box=$("#suggestions");box.innerHTML="";info[state.character].suggestions.forEach(t=>{const b=document.createElement("button");b.className="suggestion";b.textContent=t;b.onclick=()=>send(t);box.appendChild(b)})}
function startCharacter(c){state.character=c;state.mode="chat";state.history=[];$("#characterName").textContent=info[c].name;$$(".mode").forEach(x=>x.classList.toggle("active",x.dataset.mode==="chat"));$("#messages").innerHTML="";add("bot",info[c].welcome);renderSuggestions();show("chat")}
async function send(text){text=(text||"").trim();if(!text||state.busy)return;state.busy=true;$("#sendBtn").disabled=true;add("user",text);state.history.push({role:"user",content:text});const typing=add("bot","Đang suy nghĩ…","typing");
 try{const r=await fetch("/api/chat",{method:"POST",headers:{"content-type":"application/json"},body:JSON.stringify({character:state.character,mode:state.mode,message:text,history:state.history.slice(-10,-1)})});const data=await r.json();if(!r.ok)throw new Error(data.error||"Không thể kết nối AI.");typing.remove();add("bot",data.reply);state.history.push({role:"assistant",content:data.reply})}
 catch(e){typing.remove();add("bot","Có lỗi kết nối: "+e.message+"\nEm thử lại sau một chút nhé.")}
 finally{state.busy=false;$("#sendBtn").disabled=false;$("#messageInput").focus()}
}
$$(".character-card").forEach(b=>b.onclick=()=>startCharacter(b.dataset.character));
$("#backBtn").onclick=()=>show("home");$("#resetBtn").onclick=()=>startCharacter(state.character);
$$(".mode").forEach(b=>b.onclick=()=>{state.mode=b.dataset.mode;$$(".mode").forEach(x=>x.classList.toggle("active",x===b));const label={chat:"Trò chuyện",interview:"Phỏng vấn",debate:"Tranh biện"}[state.mode];add("bot",`Được, mình chuyển sang chế độ ${label}. ${state.mode==="interview"?"Em là người phỏng vấn, hãy đặt câu hỏi cho tôi.":state.mode==="debate"?"Em hãy nêu một quan điểm về tôi hoặc một sự việc trong truyện. Tôi sẽ cùng em xem xét bằng chứng.":"Em cứ hỏi điều em đang tò mò."}`)});
$("#chatForm").onsubmit=e=>{e.preventDefault();const i=$("#messageInput");const t=i.value;i.value="";send(t)};
$("#messageInput").addEventListener("keydown",e=>{if(e.key==="Enter"&&!e.shiftKey){e.preventDefault();$("#chatForm").requestSubmit()}});
