(function(){
"use strict";
var ROOT=location.pathname.indexOf("/mesflow-portfolio/")!==-1?"/mesflow-portfolio/":"/";
var ZALO="https://zalo.me/0942591888";
var GH="https://github.com/hungtranbkit";
var cats=[["all","Tất cả"],["operations","Vận hành"],["commerce","Sản phẩm web & bán lẻ"],["ai","AI & Dữ liệu"],["tools","Công cụ kỹ thuật"],["engineering","Kỹ thuật & R&D"]];
var icons={operations:"▦",commerce:"◈",ai:"✳",tools:"⌘",engineering:"⟁"};
function path(v){return ROOT+(v||"")}
function e(v){return String(v===null||v===undefined?"":v).replace(/[&<>"']/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]})}
function a(v){return e(v)}
function detailPath(p){return path("projects/"+p.slug+"/")}
function demoPath(p){return path("projects/"+p.slug+"/demo/")}
function external(p){
var w=p.website?'<a class="button-outline button-sm" href="'+a(p.website)+'" target="_blank" rel="noopener noreferrer">Website sản phẩm <span aria-hidden="true">↗</span></a>':"";
var g=p.sourceUrl?'<a class="button-outline button-sm" href="'+a(p.sourceUrl)+'" target="_blank" rel="noopener noreferrer">Mã nguồn GitHub <span aria-hidden="true">↗</span></a>':"";
return w+g;
}
function header(){
return '<a href="#main" class="skip-link">Bỏ qua điều hướng</a>'+
'<div class="header-note"><span class="dot"></span> INDEPENDENT SOFTWARE & ENGINEERING PORTFOLIO <span class="dot"></span></div>'+
'<header class="site-header"><div class="container nav">'+
'<a href="'+path("")+'" class="brand" aria-label="MESFlow Lab - trang chủ"><span class="brand-mark"><b>H.</b></span><span class="brand-copy"><strong>HUNG TRAN<span style="color:var(--blue)">.</span></strong><small>MESFLOW / PRODUCT LAB</small></span></a>'+
'<nav class="nav-links" id="nav-links" aria-label="Điều hướng chính"><a href="'+path("#work")+'">Dự án</a><a href="'+path("#approach")+'">Cách làm</a><a href="'+path("#about")+'">Giới thiệu</a><a href="'+GH+'" target="_blank" rel="noopener noreferrer">GitHub ↗</a></nav>'+
'<div class="nav-actions"><a class="circle-link" href="'+GH+'" target="_blank" rel="noopener noreferrer" aria-label="GitHub"><span style="font-size:17px;font-weight:800">gh</span></a><a class="button button-sm" href="'+path("#contact")+'">Kết nối <span class="arrow">↗</span></a><button class="menu-toggle" id="menu-toggle" aria-controls="nav-links" aria-expanded="false" aria-label="Mở menu">☰</button></div>'+
'</div></header>'}
function footer(){return '<footer class="site-footer"><div class="container footer-grid"><div><strong style="font:700 17px Space Grotesk">HUNG TRAN / MESFLOW LAB</strong><div style="margin-top:5px"><small>Portfolio sản phẩm, kỹ thuật và nghiên cứu · © '+new Date().getFullYear()+'</small></div></div>'+
'<div class="footer-links"><a href="'+path("#work")+'">Dự án</a><a href="'+path("#about")+'">Profile</a><a href="'+ZALO+'" target="_blank" rel="noopener noreferrer">Zalo liên hệ ↗</a><a href="'+GH+'" target="_blank" rel="noopener noreferrer">GitHub ↗</a></div></div></footer>'}
function art(p,index){
var screenshots=Array.isArray(p.screenshots)?p.screenshots:[];
if(screenshots.length){
  var shot=screenshots[0];
  var kind=shot.kind==="public_demo"?"WEBSITE PUBLIC":"BẰNG CHỨNG KIỂM THỬ";
  return '<div class="project-art ui-screenshot">'+
  '<img src="'+a(path(shot.src))+'" alt="'+a(shot.caption||("Ảnh giao diện "+p.name))+'" loading="eager" decoding="sync" fetchpriority="high">'+
  '<div class="ui-photo-tag"><span class="ui-photo-dot" aria-hidden="true"></span>Ảnh giao diện · '+kind+'</div></div>';
}
return '<div class="project-art ui-unavailable art--'+a(p.category)+'">'+
'<div class="ui-unavailable-grid" aria-hidden="true"></div>'+
'<div class="ui-unavailable-icon" aria-hidden="true">'+a(p.visual)+'</div>'+
'<div class="ui-unavailable-copy"><strong>Chưa có ảnh giao diện công khai</strong><small>Dự án '+a(p.phaseLabel.toLowerCase())+' · xem giới thiệu bên dưới</small></div></div>';
}

function projectCard(p,i,featured){
return '<article class="project-card '+(featured?'feature-card':'catalog-card')+'">'+
'<a href="'+detailPath(p)+'" aria-label="Chi tiết '+a(p.name)+'">'+art(p,i)+'</a>'+
'<div class="project-info"><div class="project-meta"><span class="project-category">'+a(p.categoryLabel)+'</span><span class="project-phase">'+a(p.phaseLabel)+'</span></div>'+
'<h3><a href="'+detailPath(p)+'">'+a(p.name)+'</a></h3><p class="project-tagline">'+a(p.tagline)+'</p>'+
'<div class="card-foot"><a class="text-link" href="'+detailPath(p)+'">Xem dự án <span>→</span></a><a class="demo-link" href="'+demoPath(p)+'">Thử demo ↗</a></div></div></article>'}
function approach(){var items=[["01","Hiểu bài toán","Tìm đúng nút thắt trong quy trình, dữ liệu và trải nghiệm thực tế."],["02","Thiết kế hệ thống","Chọn kiến trúc, module và luồng dữ liệu phù hợp với quy mô."],["03","Xây & kiểm thử","Tạo sản phẩm, thử nghiệm luồng sử dụng và đo chất lượng."],["04","Vận hành & cải tiến","Triển khai từng giai đoạn, theo dõi lỗi và hoàn thiện từ phản hồi."]];
return '<section class="section" id="approach"><div class="container"><div class="section-head"><div><div class="section-label eyebrow">THE PROCESS</div><h2>Từ vấn đề thật đến<br>sản phẩm dùng được.</h2></div><p>Mỗi dự án là một lời giải khác nhau — nhưng luôn đi theo tư duy kỹ thuật, bằng chứng và khả năng triển khai.</p></div><div class="approach-grid">'+items.map(function(x){return '<div class="approach-card"><div class="number">'+x[0]+'</div><h3>'+x[1]+'</h3><p>'+x[2]+'</p></div>'}).join("")+'</div></div></section>'}
function about(){return '<section id="about" style="padding:14px 0 55px"><div class="container"><div class="about-band"><div><div class="eyebrow">BEHIND THE WORK</div><h2>Kỹ thuật chuyên sâu.<br>Tư duy sản phẩm.</h2><p>Hùng Trần làm việc ở giao điểm giữa nghiên cứu cơ học, phát triển phần mềm và các bài toán vận hành. Danh mục này gồm sản phẩm web, ứng dụng desktop, hệ thống dữ liệu, tự động hóa AI và công cụ phục vụ kỹ thuật.</p><p>Mục tiêu không chỉ là một giao diện đẹp, mà là quy trình có thể dùng, kiểm tra và tiếp tục nâng cấp.</p></div><div class="about-side"><h3>Nền tảng chuyên môn</h3><ul><li>Tiến sĩ cơ học tính toán vật liệu và kết cấu composite</li><li>Nghiên cứu mô hình vật liệu dệt, tối ưu hóa topology và độ bền mỏi</li><li>Phát triển ứng dụng cho sản xuất, bán lẻ, dữ liệu và AI</li><li>Thiết kế giải pháp gắn với quy trình vận hành thực tế</li></ul></div></div></div></section>'}
function contact(){return '<section class="contact-section" id="contact"><div class="container"><div class="eyebrow">HAVE A PROBLEM WORTH SOLVING?</div><h2>Ý tưởng mới?<br>Hãy trao đổi từ bài toán.</h2><p>Từ bản demo đầu tiên đến hệ thống vận hành — cùng xác định nhu cầu, phạm vi và hướng triển khai phù hợp.</p><div class="contact-buttons"><a class="button" href="'+ZALO+'" target="_blank" rel="noopener noreferrer">Liên hệ Zalo: 0942 591 888 <span class="arrow">↗</span></a><a class="button-outline" href="'+GH+'" target="_blank" rel="noopener noreferrer">Xem GitHub <span class="arrow">↗</span></a></div></div></section>'}
function home(ps){
var feature=ps.filter(function(p){return p.featured});
var categories=cats.map(function(c){var count=c[0]==="all"?ps.length:ps.filter(function(p){return p.category===c[0]}).length;return '<button type="button" class="filter '+(c[0]==="all"?"active":"")+'" data-filter="'+c[0]+'" aria-pressed="'+(c[0]==="all")+'">'+c[1]+' <span style="opacity:.6">('+count+')</span></button>'}).join("");
var h='<main id="main"><section class="hero"><div class="container hero-grid"><div class="hero-left"><div class="hero-pill"><span class="bullet"></span> PRODUCT ENGINEERING / VIETNAM</div><h1>Biến bài toán<br>thực tế thành<br><span class="highlight">sản phẩm số.</span></h1><p class="hero-description">Portfolio của Hùng Trần: những sản phẩm đã xây dựng và đang phát triển trong sản xuất, bán lẻ, bất động sản, AI và kỹ thuật. Tập trung vào tính hữu ích, khả năng vận hành và chiều sâu công nghệ.</p><div class="hero-cta"><a class="button" href="#work">Khám phá dự án <span class="arrow">↗</span></a><a class="button-outline" href="#about">Hồ sơ năng lực <span class="arrow">↗</span></a></div><div class="hero-note"><strong>'+ps.length+' dự án chọn lọc</strong><span class="note-line"></span><span>5 nhóm giải pháp · Ảnh giao diện thật & demo</span></div></div>'+
'<div class="hero-stage" aria-label="Hình minh họa hệ sinh thái phần mềm"><div class="stage-grid"></div><div class="stage-top"><span>H / PRODUCT OPERATING SYSTEM</span><span class="online">BUILT TO SOLVE</span></div><div class="stage-main"><div class="stage-ui-top"><span class="stage-ui-title">Operations overview</span><span class="stage-dots"><i></i><i></i><i></i></span></div><div class="stage-controls"><div class="stage-metric"><small>WORKFLOWS</small><strong>08</strong></div><div class="stage-metric"><small>SYSTEMS</small><strong>05</strong></div><div class="stage-metric"><small>ITERATIONS</small><strong>∞</strong></div></div><div class="stage-graph">'+[28,47,37,64,49,73,62,94,72,83,69,99].map(function(h){return '<i style="height:'+h+'%"></i>'}).join("")+'</div></div><div class="stage-float"><small>PORTFOLIO / 2026</small><strong>Build what matters ↗</strong></div><div class="stage-side">SOFTWARE × AI × ENGINEERING</div></div></div></section>'+
'<div class="trust-strip"><div class="container trust-inner"><span class="micro">LĨNH VỰC TRIỂN KHAI</span><div class="trust-tags"><span>Sản xuất</span><span>Bán lẻ</span><span>PropertyTech</span><span>AI / Automation</span><span>R&D</span></div></div></div>'+
'<section class="section" id="featured"><div class="container"><div class="section-head"><div><div class="section-label eyebrow">SELECTED WORK / 01</div><h2>Các sản phẩm nổi bật.</h2></div><p>Những hướng đi chính trong hệ sinh thái — từ hệ thống nghiệp vụ đến hạ tầng AI và công cụ hỗ trợ.</p></div><div class="feature-grid">'+feature.map(function(p,i){return projectCard(p,i,true)}).join("")+'</div></div></section>'+
'<section class="section catalog-section" id="work"><div class="container"><div class="section-head"><div><div class="section-label eyebrow">PROJECT DIRECTORY / 02</div><h2>Khám phá toàn bộ dự án.</h2></div><p>Lọc theo lĩnh vực, xem câu chuyện của từng sản phẩm và thử demo mô phỏng ngay trên trình duyệt.</p></div><div class="catalog-toolbar"><div class="filters" role="group" aria-label="Lọc theo lĩnh vực">'+categories+'</div><label class="search-wrap"><span class="sr-only">Tìm dự án</span><input id="project-search" type="search" aria-label="Tìm dự án" placeholder="Tìm tên, lĩnh vực, công nghệ..." autocomplete="off"></label></div><div id="catalog-count" class="catalog-count" role="status"></div><div id="project-grid" class="catalog-grid"></div></div></section>'+approach()+about()+contact()+'</main>';
return header()+h+footer()
}
function screenshotGallery(p){
var shots=Array.isArray(p.screenshots)?p.screenshots:[];
if(!shots.length){
return '<section class="screen-gallery no-screenshots"><div class="container">'+
'<div class="section-label eyebrow">PRODUCT SCREENSHOTS</div>'+
'<h2 class="subheading">Ảnh giao diện thực tế</h2>'+
'<div class="screens-empty"><span class="screens-empty-icon" aria-hidden="true">▧</span>'+
'<div><strong>Chưa có ảnh giao diện được xác minh để công bố.</strong>'+
'<p>Dự án có thể đang phát triển, chạy nội bộ hoặc chưa có giao diện. Portfolio sẽ không dùng bản vẽ minh họa như ảnh sản phẩm thật.</p></div></div></div></section>';
}
var items=shots.map(function(shot,i){
var src=a(path(shot.src));
return '<figure class="screen-figure">'+
'<a href="'+src+'" target="_blank" rel="noopener noreferrer" title="Mở ảnh đầy đủ: '+a(shot.caption)+'">'+
'<img src="'+src+'" alt="'+a(shot.caption)+'" loading="lazy" decoding="async">'+
'<span class="screen-open" aria-hidden="true">↗ Xem ảnh đầy đủ</span></a>'+
'<figcaption><strong>'+a(shot.caption)+'</strong>'+
'<div class="screen-source">'+a(shot.source)+' · '+(shot.kind==="public_demo"?"Website public":"Ảnh kiểm thử")+'</div>'+
'<p>'+a(shot.note||"Ảnh chụp giao diện, không phải dữ liệu sản xuất.")+'</p></figcaption></figure>';
}).join("");
return '<section class="screen-gallery" id="screenshots"><div class="container">'+
'<div class="section-head"><div><div class="section-label eyebrow">REAL INTERFACE / SCREENSHOTS</div>'+
'<h2>Giao diện thật của dự án.</h2></div><p>'+shots.length+' ảnh từ website công khai hoặc bằng chứng kiểm thử. Chọn ảnh để xem nguyên bản.</p></div>'+
'<div class="screens-grid '+(shots.length===1?'screens-single':'')+'">'+items+'</div></div></section>';
}

function detail(p,ps){
var related=ps.filter(function(x){return x.category===p.category&&x.slug!==p.slug}).slice(0,3);
var tech=p.stack.map(function(x){return '<span>'+e(x)+'</span>'}).join("");
var timeline=p.steps.map(function(x,i){return '<div class="timeline-item"><span>0'+(i+1)+' / STEP</span><strong>'+e(x)+'</strong></div>'}).join("");
return header()+'<main id="main"><section class="detail-hero"><div class="container"><div class="detail-breadcrumb"><a href="'+path("")+'">Trang chủ</a><span>/</span><a href="'+path("#work")+'">Dự án</a><span>/</span><span>'+e(p.name)+'</span></div><div class="detail-grid"><div class="detail-copy"><div class="eyebrow">'+e(p.categoryLabel)+' / CASE STUDY</div><h1>'+e(p.name)+'<span style="color:var(--blue)">.</span></h1><p class="detail-tagline">'+e(p.tagline)+'</p><p class="detail-description">'+e(p.description)+'</p><div class="detail-badges"><span>'+e(p.phaseLabel)+'</span><span>'+e(p.categoryLabel)+'</span><span>Demo mẫu có thể thử</span></div><div class="detail-buttons"><a class="button" href="'+demoPath(p)+'">Trải nghiệm demo <span class="arrow">↗</span></a>'+(p.screenshots&&p.screenshots.length?'<a class="button-outline button-sm" href="#screenshots">Xem ảnh giao diện ('+p.screenshots.length+') ↓</a>':'')+external(p)+'</div></div><div class="detail-visual">'+art(p,0)+'</div></div></div></section>'+
screenshotGallery(p)+
'<section class="detail-sections"><div class="container"><div class="detail-columns"><div><div class="section-label eyebrow">THE CONTEXT</div><h2 class="subheading">Tại sao dự án này<br>được xây dựng?</h2><p>'+e(p.description)+'</p><div class="micro" style="margin-top:35px;color:#668071">NỀN TẢNG KỸ THUẬT</div><div class="tech-list">'+tech+'</div></div><div><div class="section-label eyebrow">THE SOLUTION</div><h2 class="subheading">Năng lực chính</h2><ul class="capability-list">'+p.capabilities.map(function(x){return '<li>'+e(x)+'</li>'}).join("")+'</ul></div></div><div style="margin-top:70px"><div class="section-label eyebrow">HOW IT WORKS</div><h2 class="subheading">Một luồng sử dụng điển hình</h2><p class="muted" style="font-size:13px">Các bước bên dưới là kịch bản minh họa để hiểu cách giải pháp hoạt động.</p><div class="timeline">'+timeline+'</div></div></div></section>'+
'<section class="detail-bottom"><div class="container"><div class="detail-bottom-inner"><div><div class="eyebrow" style="color:#c8d7ff">EXPERIENCE THE FLOW</div><h2>Đừng chỉ đọc. Hãy thử.</h2><p>Demo tương tác dùng dữ liệu giả lập và có nút đặt lại, không kết nối hệ thống hoặc dữ liệu khách hàng thật.</p></div><a class="button-light" href="'+demoPath(p)+'">Mở demo '+e(p.name)+' <span class="arrow">↗</span></a></div></div></section></main>'+
more(related)+footer()
}
function more(ps){
if(!ps.length)return "";
return '<section class="more-projects"><div class="container"><div class="section-label eyebrow">EXPLORE MORE</div><h2 class="subheading">Dự án cùng lĩnh vực</h2><div class="more-grid">'+ps.map(function(p){return '<a class="more-link" href="'+detailPath(p)+'"><span class="more-icon">'+e(p.visual)+'</span><div><strong>'+e(p.name)+'</strong><span>'+e(p.categoryLabel)+' · '+e(p.phaseLabel)+'</span></div><span style="margin-left:auto;color:var(--blue)">↗</span></a>'}).join("")+'</div></div></section>'
}
function demo(p){
var steps=p.steps.map(function(x,i){return '<button class="step-button '+(i===0?'active':'')+'" type="button" data-step="'+i+'" aria-label="Bước '+(i+1)+': '+a(x)+'"><span class="step-number">'+(i+1)+'</span><span class="step-text">'+e(x)+'</span></button>'}).join("");
return header()+'<main id="main"><section class="demo-page"><div class="container"><div class="detail-breadcrumb"><a href="'+path("")+'">Trang chủ</a><span>/</span><a href="'+detailPath(p)+'">'+e(p.name)+'</a><span>/</span><span>Demo</span></div><div class="demo-head"><div class="eyebrow" style="color:var(--blue)">INTERACTIVE SANDBOX / '+e(p.visual)+'</div><h1>Trải nghiệm '+e(p.name)+'<span style="color:var(--blue)">.</span></h1><p>'+e(p.tagline)+'. Một kịch bản minh họa giúp hình dung luồng sử dụng mà không cần tài khoản.</p></div><div class="demo-warning"><span style="font-size:19px">ⓘ</span><span><strong>Demo mô phỏng.</strong> Tất cả thông tin ở đây là dữ liệu mẫu trong trình duyệt. Không gọi API thật, không dùng dữ liệu khách hàng, và không đại diện cho trạng thái hoàn thiện của sản phẩm.</span></div><div class="demo-shell"><aside class="demo-sidebar"><span class="eyebrow">LUỒNG TRẢI NGHIỆM</span><div class="step-buttons" id="step-buttons">'+steps+'</div><div class="demo-sidebar-bottom"><span class="micro" style="color:#48725b">TIẾN ĐỘ MÔ PHỎNG</span><div class="progress-bar"><i id="demo-progress" style="width:0%"></i></div><p id="demo-progress-label">0 / '+p.steps.length+' bước đã hoàn thành</p></div></aside><section class="demo-main" aria-label="Khu vực demo"><div class="demo-appbar"><div><strong>'+e(p.name)+' / Sandbox</strong><br><small>LOCAL DEMO · không có backend</small></div><span class="demo-chip" id="demo-status">CHƯA BẮT ĐẦU</span></div><div class="demo-workspace"><div class="demo-pane"><div class="demo-pane-heading"><strong>Kịch bản</strong><span>01 / SAMPLE</span></div><div class="demo-pane-body"><div class="demo-label">DỮ LIỆU ĐẦU VÀO - CÓ THỂ SỬA</div><input class="demo-input" id="demo-input" type="text" maxlength="150" value="'+a(p.sample)+'" aria-label="Dữ liệu mô phỏng"><div class="demo-label">HÀNH ĐỘNG HIỆN TẠI</div><h2 id="demo-step-title" class="active-step-title">'+e(p.steps[0])+'</h2><p class="active-step-desc" id="demo-step-desc">Nhấn thực hiện để chạy bước mô phỏng. Các thay đổi chỉ nằm trong phiên trình duyệt này.</p><div class="demo-actions"><button class="button" id="demo-next">Thực hiện bước <span class="arrow">→</span></button><button class="button-outline" id="demo-reset">↺ Đặt lại dữ liệu mẫu</button></div></div></div><div class="demo-pane"><div class="demo-pane-heading"><strong>Bảng giám sát</strong><span>LIVE SIMULATION</span></div><div class="demo-pane-body"><div class="demo-metric"><small>Kịch bản</small><strong>'+e(p.visual)+'</strong></div><div class="demo-metric"><small>Bước hoàn tất</small><strong id="demo-metric">0 / '+p.steps.length+'</strong></div><div class="demo-metric"><small>Trạng thái</small><strong id="demo-metric-status">Sẵn sàng</strong></div><div class="demo-label" style="margin-top:23px">NHẬT KÝ HOẠT ĐỘNG</div><div class="demo-log" id="demo-log" aria-live="polite"><p class="log-empty">Chưa có hoạt động. Nhấn “Thực hiện bước” để bắt đầu.</p></div></div></div></div><div class="demo-outcome"><div><strong id="demo-outcome-title">Quy trình chờ thực hiện</strong><p id="demo-outcome-text">Thử từng bước và quan sát kết quả. Không có dữ liệu nào được gửi lên máy chủ.</p></div><span id="demo-percent" class="percent">0%</span></div><div class="demo-actions" style="justify-content:flex-end;margin-top:18px"><button class="button-outline button-sm" id="demo-export">↓ Xuất nhật ký JSON</button><a class="button-outline button-sm" href="'+detailPath(p)+'">← Trở lại giới thiệu</a>'+external(p)+'</div></section></div></div></section></main>'+footer()
}
function bindGlobal(){
var menu=document.getElementById("menu-toggle"),nav=document.getElementById("nav-links");
if(menu&&nav){menu.addEventListener("click",function(){var open=nav.classList.toggle("open");menu.setAttribute("aria-expanded",String(open))});nav.querySelectorAll("a").forEach(function(n){n.addEventListener("click",function(){nav.classList.remove("open");menu.setAttribute("aria-expanded","false")})})}
}
function bindHome(ps){
var grid=document.getElementById("project-grid"),count=document.getElementById("catalog-count"),search=document.getElementById("project-search"),current="all";
function draw(){
var q=search.value.trim().toLocaleLowerCase("vi");
var shown=ps.filter(function(p){return (current==="all"||p.category===current)&&[p.name,p.tagline,p.description,p.categoryLabel,p.stack.join(" ")].join(" ").toLocaleLowerCase("vi").includes(q)});
grid.innerHTML=shown.length?shown.map(function(p,i){return projectCard(p,i,false)}).join(""):'<div class="empty-state"><h3>Không tìm thấy dự án phù hợp</h3><p>Hãy thử từ khóa hoặc lĩnh vực khác.</p><button type="button" class="button-outline button-sm" id="clear-filter">Xóa bộ lọc</button></div>';
count.textContent="HIỂN THỊ "+shown.length+" / "+ps.length+" DỰ ÁN";
var clear=document.getElementById("clear-filter");if(clear)clear.addEventListener("click",function(){current="all";search.value="";document.querySelectorAll(".filter").forEach(function(b){b.classList.toggle("active",b.dataset.filter==="all");b.setAttribute("aria-pressed",String(b.dataset.filter==="all"))});draw()});
}
document.querySelectorAll(".filter").forEach(function(b){b.addEventListener("click",function(){current=b.dataset.filter;document.querySelectorAll(".filter").forEach(function(t){t.classList.toggle("active",t===b);t.setAttribute("aria-pressed",String(t===b))});draw()})});
search.addEventListener("input",draw);draw();
}
function bindDemo(p){
var step=0,logs=[],input=document.getElementById("demo-input");
var next=document.getElementById("demo-next"),reset=document.getElementById("demo-reset"),outcome=document.getElementById("demo-outcome-title");
function update(){
var total=p.steps.length,pct=Math.round(step/total*100);
document.querySelectorAll("[data-step]").forEach(function(b){var n=Number(b.dataset.step);b.classList.toggle("done",n<step);b.classList.toggle("active",n===step||(step===total&&n===total-1));b.querySelector(".step-number").textContent=n<step?"✓":String(n+1)});
document.getElementById("demo-progress").style.width=pct+"%";
document.getElementById("demo-progress-label").textContent=step+" / "+total+" bước đã hoàn thành";
document.getElementById("demo-step-title").textContent=step<total?p.steps[step]:"Hoàn tất quy trình mẫu";
document.getElementById("demo-step-desc").textContent=step<total?"Dữ liệu mẫu: "+(input.value||p.sample)+". Thao tác sẽ được ghi vào nhật ký mô phỏng.":"Đã hoàn thành tất cả bước. Có thể xuất nhật ký hoặc đặt lại kịch bản.";
document.getElementById("demo-status").textContent=step===0?"CHƯA BẮT ĐẦU":step===total?"HOÀN THÀNH":"ĐANG THỰC HIỆN";
document.getElementById("demo-metric").textContent=step+" / "+total;
document.getElementById("demo-metric-status").textContent=step===0?"Sẵn sàng":step===total?"Hoàn tất":"Đang xử lý";
document.getElementById("demo-percent").textContent=pct+"%";
document.getElementById("demo-outcome-title").textContent=step===0?"Quy trình chờ thực hiện":step===total?"Mô phỏng thành công":"Bước "+step+" đã ghi nhận";
document.getElementById("demo-outcome-text").textContent=step===total?"Bạn đã đi hết luồng sử dụng mẫu của "+p.name+". Đây không phải kết quả từ sản phẩm thật.":"Đang mô phỏng với dữ liệu: "+(input.value||p.sample);
next.disabled=step===total;next.style.opacity=step===total?".5":"1";next.innerHTML=step===total?"Đã hoàn tất ✓":"Thực hiện bước <span class=\"arrow\">→</span>";
document.getElementById("demo-log").innerHTML=logs.length?logs.map(function(x){return '<div class="log-item"><span><strong>'+e(x.name)+'</strong><br>'+e(x.subject)+'</span></div>'}).reverse().join(""):'<p class="log-empty">Chưa có hoạt động. Nhấn “Thực hiện bước” để bắt đầu.</p>'
}
function go(){if(step<p.steps.length){logs.push({name:p.steps[step],subject:input.value||p.sample,at:new Date().toISOString()});step++;update()}}
next.addEventListener("click",go);reset.addEventListener("click",function(){step=0;logs=[];input.value=p.sample;update()});input.addEventListener("input",update);
document.querySelectorAll("[data-step]").forEach(function(b){b.addEventListener("click",function(){var n=Number(b.dataset.step);if(n<=step){step=n;logs=logs.slice(0,n);update()}})});
document.getElementById("demo-export").addEventListener("click",function(){var data={project:p.name,mode:"browser_only_sample",sample:input.value,completed_steps:step,activity:logs};var blob=new Blob([JSON.stringify(data,null,2)],{type:"application/json"}),u=URL.createObjectURL(blob),anchor=document.createElement("a");anchor.href=u;anchor.download=p.slug+"-demo.json";document.body.appendChild(anchor);anchor.click();anchor.remove();setTimeout(function(){URL.revokeObjectURL(u)},1000)});
update();
}
async function main(){
var host=document.getElementById("app");if(!host)return;
try{
var response=await fetch(path("data/projects.json"),{cache:"no-store"});if(!response.ok)throw Error("Không tải được danh mục dự án");
var ps=await response.json();if(!Array.isArray(ps)||ps.length===0)throw Error("Dữ liệu dự án trống");
var view=document.body.getAttribute("data-view")||"home",slug=document.body.getAttribute("data-project"),p=ps.find(function(x){return x.slug===slug});
if(view==="home"){host.innerHTML=home(ps);bindHome(ps)}
else if(!p){host.innerHTML=header()+'<main id="main" class="container loading"><h1>Không tìm thấy dự án</h1><p><a href="'+path("")+'">← Trở lại trang chủ</a></p></main>'+footer()}
else if(view==="demo"){host.innerHTML=demo(p);bindDemo(p)}
else{host.innerHTML=detail(p,ps)}
bindGlobal();
if(location.hash){requestAnimationFrame(function(){var el=document.getElementById(location.hash.slice(1));if(el)el.scrollIntoView()})}
}catch(err){host.innerHTML='<main class="container loading"><h1>Không thể tải trang</h1><p>'+e(err.message||"Lỗi dữ liệu")+'</p><button class="button" onclick="location.reload()">Tải lại trang</button></main>';console.error(err)}
}
main()
})();
