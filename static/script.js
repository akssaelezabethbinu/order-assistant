const $ = (id) => document.getElementById(id);
let signupMode = false;
let userName = 'Store Admin';
const authScreen = $('auth-screen'), appScreen = $('app-screen');
function setMode(signup) {
  signupMode = signup;
  $('auth-eyebrow').textContent = signup ? 'GET STARTED' : 'WELCOME';
  $('auth-title').textContent = signup ? 'Create your workspace' : 'Sign in to your workspace';
  $('auth-subtitle').textContent = signup ? 'A simple place to manage your store activity.' : 'Use the demo account to explore the dashboard.';
  $('name-label').classList.toggle('hidden', !signup); $('full-name').classList.toggle('hidden', !signup); $('full-name').required = signup;
  $('auth-submit').innerHTML = signup ? 'Create workspace <span>→</span>' : 'Sign in <span>→</span>';
  $('switch-copy').textContent = signup ? 'Already have a workspace?' : 'New to OrderDesk?';
  $('switch-mode').textContent = signup ? 'Sign in' : 'Create an account';
}
$('switch-mode').addEventListener('click', () => setMode(!signupMode));
$('auth-form').addEventListener('submit', e => {
  e.preventDefault();
  userName = signupMode && $('full-name').value.trim() ? $('full-name').value.trim().split(' ')[0] : ($('email').value.split('@')[0] || 'Store Admin');
  $('profile-name').textContent = userName; $('profile-avatar').textContent = userName.charAt(0).toUpperCase(); $('greeting-name').textContent = `, ${userName}`;
  authScreen.classList.add('hidden'); appScreen.classList.remove('hidden');
  toast(signupMode ? 'Demo workspace ready.' : 'Welcome to your workspace.');
});
function signOut(){appScreen.classList.add('hidden');authScreen.classList.remove('hidden');$('password').value='';setMode(false)}
$('sign-out').addEventListener('click', signOut);
function toast(message){const t=$('toast');t.textContent=message;t.classList.add('show');clearTimeout(window.__toastTimer);window.__toastTimer=setTimeout(()=>t.classList.remove('show'),2500)}
function openAssistant(){ $('assistant-panel').scrollIntoView({behavior:'smooth',block:'center'}); $('question').focus(); }
$('top-assistant').addEventListener('click',openAssistant);$('help-ask').addEventListener('click',openAssistant);
$('view-orders').addEventListener('click',()=>{ $('page-crumb').textContent='Orders';$('page-title').textContent='Your orders';$('page-description').textContent='Review recent activity and order status.';$('today-label').textContent='ORDER MANAGEMENT';$('orders-panel').scrollIntoView({behavior:'smooth',block:'start'}); });
document.querySelectorAll('.nav-item').forEach(btn=>btn.addEventListener('click',()=>{document.querySelectorAll('.nav-item').forEach(b=>b.classList.remove('active'));btn.classList.add('active');const s=btn.dataset.section;if(s==='overview'){ $('page-crumb').textContent='Overview';$('page-title').textContent='Good morning';$('greeting-name').textContent=`, ${userName}`;$('page-description').textContent='Here’s what’s happening with your store today.';$('today-label').textContent='STORE OVERVIEW';}else if(s==='orders'){ $('page-crumb').textContent='Orders';$('page-title').textContent='Your orders';$('page-description').textContent='Review recent activity and order status.';$('today-label').textContent='ORDER MANAGEMENT';$('orders-panel').scrollIntoView({behavior:'smooth',block:'start'});}else{ $('page-crumb').textContent='Customers';$('page-title').textContent='Customer activity';$('page-description').textContent='Ask the assistant to find customer trends and top spenders.';$('today-label').textContent='CUSTOMER OVERVIEW';openAssistant();}}));
$('export-btn').addEventListener('click',()=>{const rows=[['Order','Customer','Product','Amount','Status'],['ORD-1001','Rahul Sharma','Wireless Mouse','1598','Delivered'],['ORD-1002','Ananya Menon','USB-C Hub','2499','Shipped'],['ORD-1003','Vivek Kumar','Notebook Stand','1199','Pending'],['ORD-1004','Priya Das','Wireless Keyboard','3299','Cancelled']];const csv=rows.map(r=>r.map(v=>'"'+v.replaceAll('"','""')+'"').join(',')).join('\r\n');const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([csv],{type:'text/csv'}));a.download='orderdesk-report.csv';a.click();URL.revokeObjectURL(a.href);toast('Report exported.');});
function addMessage(type,who,text){const box=$('chat-messages');const empty=box.querySelector('.chat-empty');if(empty)empty.remove();const item=document.createElement('div');item.className='chat-message '+type;const name=document.createElement('div');name.className='who';name.textContent=who;const answer=document.createElement('div');answer.className='answer';answer.textContent=text;item.append(name,answer);box.append(item);box.scrollTop=box.scrollHeight;return answer;}
async function ask(question){if(!question.trim())return;addMessage('user','YOU',question);const waiting=addMessage('assistant','ORDER ASSISTANT','Checking your order data…');$('question').value='';$('question').disabled=true;try{const response=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question})});const data=await response.json();if(!response.ok)throw new Error(data.detail||'Could not process that question.');waiting.textContent=data.answer||'I could not find an answer in the available order data.';}catch(err){waiting.textContent='I could not connect to the assistant. Check that the server is running, then try again.';console.error(err);}finally{$('question').disabled=false;$('question').focus();}}
$('chat-form').addEventListener('submit',e=>{e.preventDefault();ask($('question').value)});
document.querySelectorAll('[data-question]').forEach(btn=>btn.addEventListener('click',()=>ask(btn.dataset.question)));
