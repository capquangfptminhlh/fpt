
const toggle = document.querySelector('.mobile-toggle');
const navLinks = document.querySelector('.nav-links');
if (toggle && navLinks) toggle.addEventListener('click',()=>navLinks.classList.toggle('open'));
const form = document.querySelector('#advisor-form');
if(form){
  const map = {
    family: {id:'giga', text:'Gói GIGA phù hợp gia đình nhỏ, lướt web, xem phim HD và học tập online.'},
    game: {id:'sky', text:'Gói SKY phù hợp chơi game, ping ổn định và nhiều thiết bị hoạt động cùng lúc.'},
    camera: {id:'meta', text:'Gói META phù hợp nhà nhiều tầng, camera an ninh và hệ sinh thái smart home.'},
    office: {id:'meta', text:'Gói META phù hợp văn phòng nhỏ và không gian làm việc cường độ cao.'},
    cafe: {id:'sky', text:'Gói SKY phù hợp quán cafe cần kết nối ổn định cho nhiều khách cùng lúc.'}
  };
  form.addEventListener('submit', (e)=>{
    e.preventDefault();
    const need = document.querySelector('#need').value;
    const result = document.querySelector('#advisor-result');
    const picked = map[need] || map.family;
    result.innerHTML = `<div class="seo-box"><strong>Gợi ý nhanh:</strong> ${picked.text} <a href="./goi-cuoc/${picked.id}/" style="color:#1751c3;font-weight:800">Xem chi tiết →</a></div>`;
    result.scrollIntoView({behavior:'smooth', block:'nearest'});
  })
}
