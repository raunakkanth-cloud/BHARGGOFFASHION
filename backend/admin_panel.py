ADMIN_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bharggo Fashion - Admin Panel</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f5f5f5;color:#1c1c1e}
.login-container{display:flex;justify-content:center;align-items:center;min-height:100vh;background:linear-gradient(135deg,#0a0a0a 0%,#1a1a2e 100%)}
.login-card{background:#fff;padding:40px;border-radius:16px;width:400px;max-width:90vw;box-shadow:0 20px 60px rgba(0,0,0,0.3)}
.login-card h1{color:#AE2448;font-size:24px;margin-bottom:8px;text-align:center}
.login-card p{color:#666;text-align:center;margin-bottom:24px;font-size:14px}
.login-card input{width:100%;padding:14px 16px;border:1px solid #e0e0e0;border-radius:10px;font-size:15px;margin-bottom:14px;background:#f5f5f5}
.login-card input:focus{outline:none;border-color:#AE2448}
.login-card button{width:100%;padding:14px;background:#AE2448;color:#fff;border:none;border-radius:10px;font-size:16px;font-weight:600;cursor:pointer}
.login-card button:hover{background:#952040}
.login-error{color:#ff3b30;text-align:center;margin-bottom:12px;font-size:14px}
.dashboard{display:none}
.sidebar{position:fixed;left:0;top:0;bottom:0;width:240px;background:#1c1c2e;color:#fff;padding:20px 0;overflow-y:auto}
.sidebar-logo{padding:0 20px 20px;border-bottom:1px solid #333;margin-bottom:16px;text-align:center}
.sidebar-logo h2{color:#AE2448;font-size:20px}
.sidebar-logo p{color:#888;font-size:11px}
.nav-item{padding:12px 24px;cursor:pointer;font-size:14px;color:#aaa;transition:all 0.2s;display:flex;align-items:center;gap:10px}
.nav-item:hover,.nav-item.active{background:#AE244815;color:#AE2448;border-right:3px solid #AE2448}
.main{margin-left:240px;padding:24px}
.topbar{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px}
.topbar h1{font-size:24px}
.topbar button{padding:8px 20px;background:#AE2448;color:#fff;border:none;border-radius:8px;cursor:pointer;font-size:14px}
.stats-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px;margin-bottom:24px}
.stat-card{background:#fff;padding:20px;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,0.06)}
.stat-card .label{font-size:13px;color:#888;margin-bottom:4px}
.stat-card .value{font-size:28px;font-weight:700;color:#1c1c1e}
.stat-card .value.primary{color:#AE2448}
.stat-card .value.green{color:#138808}
table{width:100%;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.06);border-collapse:collapse}
th{background:#f8f8f8;padding:12px 16px;text-align:left;font-size:13px;color:#888;font-weight:600}
td{padding:12px 16px;border-top:1px solid #f0f0f0;font-size:14px}
tr:hover td{background:#fafafa}
.badge{padding:4px 10px;border-radius:12px;font-size:12px;font-weight:600;display:inline-block}
.badge-green{background:#e8f5e9;color:#138808}
.badge-red{background:#fde8e8;color:#AE2448}
.badge-blue{background:#e3f2fd;color:#1976d2}
.badge-orange{background:#fff3e0;color:#e65100}
.section-title{font-size:18px;font-weight:700;margin-bottom:16px}
.tab-content{display:none}.tab-content.active{display:block}
@media(max-width:768px){.sidebar{width:0;display:none}.main{margin-left:0}}
</style>
</head>
<body>
<div class="login-container" id="loginPage">
<div class="login-card">
<h1>Bharggo Admin</h1>
<p>Admin Panel - Bharggo FFashion India Pvt. Ltd.</p>
<div class="login-error" id="loginError" style="display:none"></div>
<input type="email" id="adminEmail" placeholder="Admin Email" value="admin@bharggo.com">
<input type="password" id="adminPass" placeholder="Password" value="admin123">
<button onclick="adminLogin()">Login to Admin Panel</button>
</div>
</div>
<div class="dashboard" id="dashboardPage">
<div class="sidebar">
<div class="sidebar-logo"><h2>Bharggo</h2><p>Admin Panel</p></div>
<div class="nav-item active" onclick="showTab('dashboard')">📊 Dashboard</div>
<div class="nav-item" onclick="showTab('products')">🛍️ Products</div>
<div class="nav-item" onclick="showTab('orders')">📦 Orders</div>
<div class="nav-item" onclick="showTab('users')">👥 Users</div>
<div class="nav-item" onclick="showTab('commissions')">💰 Commissions</div>
</div>
<div class="main">
<div class="topbar"><h1 id="pageTitle">Dashboard</h1><button onclick="adminLogout()">Logout</button></div>
<!-- Dashboard Tab -->
<div class="tab-content active" id="tab-dashboard">
<div class="stats-grid" id="statsGrid"></div>
<div class="section-title">Recent Orders</div>
<table><thead><tr><th>Order ID</th><th>User</th><th>Total</th><th>Status</th><th>Date</th></tr></thead><tbody id="recentOrdersBody"></tbody></table>
</div>
<!-- Products Tab -->
<div class="tab-content" id="tab-products">
<div class="section-title">All Products (<span id="productCount">0</span>)</div>
<table><thead><tr><th>Image</th><th>Name</th><th>Category</th><th>Price</th><th>Discount</th><th>Rating</th><th>Action</th></tr></thead><tbody id="productsBody"></tbody></table>
</div>
<!-- Orders Tab -->
<div class="tab-content" id="tab-orders">
<div class="section-title">All Orders (<span id="orderCount">0</span>)</div>
<table><thead><tr><th>Order ID</th><th>User ID</th><th>Items</th><th>Total</th><th>Payment</th><th>Status</th><th>Date</th></tr></thead><tbody id="ordersBody"></tbody></table>
</div>
<!-- Users Tab -->
<div class="tab-content" id="tab-users">
<div class="section-title">All Users (<span id="userCount">0</span>)</div>
<table><thead><tr><th>Name</th><th>Email</th><th>Mobile</th><th>Referral ID</th><th>Subscriber</th><th>Wallet</th><th>Joined</th></tr></thead><tbody id="usersBody"></tbody></table>
</div>
<!-- Commissions Tab -->
<div class="tab-content" id="tab-commissions">
<div class="section-title">Commission Transactions</div>
<table><thead><tr><th>User ID</th><th>Amount</th><th>Level</th><th>Status</th><th>Expiry</th><th>Date</th></tr></thead><tbody id="commissionsBody"></tbody></table>
</div>
</div>
</div>
<script>
const BASE='/api';let TOKEN='';
async function api(path,opts={}){
const h={'Content-Type':'application/json',...(TOKEN?{'Authorization':'Bearer '+TOKEN}:{})};
const r=await fetch(BASE+path,{...opts,headers:h});
if(!r.ok)throw new Error(await r.text());
return r.json();
}
async function adminLogin(){
try{
const e=document.getElementById('adminEmail').value;
const p=document.getElementById('adminPass').value;
const d=await api('/admin/login',{method:'POST',body:JSON.stringify({email:e,password:p})});
TOKEN=d.token;
document.getElementById('loginPage').style.display='none';
document.getElementById('dashboardPage').style.display='block';
loadDashboard();
}catch(e){
document.getElementById('loginError').textContent='Invalid credentials';
document.getElementById('loginError').style.display='block';
}}
function adminLogout(){TOKEN='';document.getElementById('loginPage').style.display='flex';document.getElementById('dashboardPage').style.display='none';}
function showTab(t){
document.querySelectorAll('.tab-content').forEach(e=>e.classList.remove('active'));
document.querySelectorAll('.nav-item').forEach(e=>e.classList.remove('active'));
document.getElementById('tab-'+t).classList.add('active');
event.target.classList.add('active');
const titles={dashboard:'Dashboard',products:'Products',orders:'Orders',users:'Users',commissions:'Commissions'};
document.getElementById('pageTitle').textContent=titles[t]||t;
if(t==='products')loadProducts();
if(t==='orders')loadOrders();
if(t==='users')loadUsers();
if(t==='commissions')loadCommissions();
if(t==='dashboard')loadDashboard();
}
async function loadDashboard(){
try{
const d=await api('/admin/dashboard');
document.getElementById('statsGrid').innerHTML=`
<div class="stat-card"><div class="label">Total Products</div><div class="value primary">${d.total_products}</div></div>
<div class="stat-card"><div class="label">Total Users</div><div class="value">${d.total_users}</div></div>
<div class="stat-card"><div class="label">Total Orders</div><div class="value">${d.total_orders}</div></div>
<div class="stat-card"><div class="label">Subscribers</div><div class="value green">${d.total_subscribers}</div></div>
<div class="stat-card"><div class="label">Revenue</div><div class="value primary">₹${d.total_revenue.toFixed(0)}</div></div>
<div class="stat-card"><div class="label">Commissions Paid</div><div class="value green">₹${d.total_commissions.toFixed(0)}</div></div>`;
const tb=document.getElementById('recentOrdersBody');
tb.innerHTML=d.recent_orders.map(o=>`<tr><td>${o.order_id}</td><td>${o.user_id.slice(0,8)}...</td><td>₹${o.total.toFixed(0)}</td><td><span class="badge badge-${o.order_status==='delivered'?'green':o.order_status==='cancelled'?'red':'blue'}">${o.order_status}</span></td><td>${new Date(o.created_at).toLocaleDateString()}</td></tr>`).join('')||'<tr><td colspan="5" style="text-align:center;color:#888">No orders yet</td></tr>';
}catch(e){console.error(e)}}
async function loadProducts(){
try{
const d=await api('/admin/products');
document.getElementById('productCount').textContent=d.total;
document.getElementById('productsBody').innerHTML=d.products.map(p=>`<tr><td><img src="${p.image_url||''}" style="width:50px;height:50px;object-fit:cover;border-radius:6px" onerror="this.style.display='none'"></td><td><strong>${p.name}</strong></td><td><span class="badge badge-blue">${p.category}</span></td><td>₹${p.price}</td><td><span class="badge badge-green">${p.discount}%</span></td><td>⭐ ${p.rating||0}</td><td><button onclick="deleteProduct('${p._id}')" style="padding:4px 12px;background:#ff3b30;color:#fff;border:none;border-radius:6px;cursor:pointer;font-size:12px">Delete</button></td></tr>`).join('');
}catch(e){console.error(e)}}
async function deleteProduct(id){
if(!confirm('Delete this product?'))return;
try{await api('/admin/products/'+id,{method:'DELETE'});loadProducts();}catch(e){alert('Failed to delete')}}
async function loadOrders(){
try{
const d=await api('/admin/orders');
document.getElementById('orderCount').textContent=d.total;
document.getElementById('ordersBody').innerHTML=d.orders.map(o=>`<tr><td>${o.order_id}</td><td>${o.user_id.slice(0,8)}...</td><td>${o.items?.length||0} items</td><td>₹${o.total.toFixed(0)}</td><td><span class="badge badge-${o.payment_status==='completed'?'green':'orange'}">${o.payment_status}</span></td><td><span class="badge badge-${o.order_status==='delivered'?'green':o.order_status==='cancelled'?'red':'blue'}">${o.order_status}</span></td><td>${new Date(o.created_at).toLocaleDateString()}</td></tr>`).join('')||'<tr><td colspan="7" style="text-align:center;color:#888">No orders yet</td></tr>';
}catch(e){console.error(e)}}
async function loadUsers(){
try{
const d=await api('/admin/users');
document.getElementById('userCount').textContent=d.total;
document.getElementById('usersBody').innerHTML=d.users.map(u=>`<tr><td><strong>${u.name}</strong></td><td>${u.email}</td><td>${u.mobile||'-'}</td><td style="font-family:monospace;font-size:12px">${u.referral_id}</td><td>${u.subscription_status?'<span class="badge badge-green">Premium</span>':'<span class="badge badge-orange">Free</span>'}</td><td>₹${(u.wallet_balance||0).toFixed(0)}</td><td>${new Date(u.created_at).toLocaleDateString()}</td></tr>`).join('');
}catch(e){console.error(e)}}
async function loadCommissions(){
try{
const d=await api('/admin/commissions');
document.getElementById('commissionsBody').innerHTML=d.commissions.map(c=>`<tr><td>${c.user_id.slice(0,8)}...</td><td>₹${c.amount.toFixed(2)}</td><td>${c.description}</td><td><span class="badge badge-${c.status==='active'?'green':'red'}">${c.status}</span></td><td>${c.expiry_date?new Date(c.expiry_date).toLocaleDateString():'-'}</td><td>${new Date(c.created_at).toLocaleDateString()}</td></tr>`).join('')||'<tr><td colspan="6" style="text-align:center;color:#888">No commissions yet</td></tr>';
}catch(e){console.error(e)}}
</script>
</body>
</html>"""
