// 기본값 (fetch 실패 시 사용)
let gamesData = [];

async function loadJSON(path) {
  try {
    const res = await fetch(path);
    if (!res.ok) throw new Error('Fetch failed');
    return await res.json();
  } catch (e) {
    console.warn('Could not load', path, e);
    return null;
  }
}

function createGameTile(game) {
  const tile = document.createElement('a');
  tile.className = 'game-tile';
  tile.href = game.path || '#';
  tile.rel = 'noopener';

  const thumb = document.createElement('div');
  thumb.className = 'game-thumbnail';
  // 상대 경로가 있을 때 로드 가능하도록 처리
  thumb.style.backgroundImage = `url('${game.thumbnail || 'https://via.placeholder.com/320x180?text=No+Image'}')`;

  const info = document.createElement('div');
  info.className = 'game-info';

  const title = document.createElement('h3');
  title.className = 'game-title';
  title.textContent = game.title_ko || game.title || 'Untitled';

  const desc = document.createElement('p');
  desc.className = 'game-description';
  desc.textContent = game.description || '';

  info.appendChild(title);
  info.appendChild(desc);
  tile.appendChild(thumb);
  tile.appendChild(info);
  return tile;
}

function renderSidebar(menu) {
  const nav = document.querySelector('.sidebar');
  nav.innerHTML = '<h2>메뉴</h2>';
  if (!menu) return;
  menu.forEach(section => {
    const el = document.createElement('div');
    el.className = 'menu-section';
    const h = document.createElement('h4');
    h.textContent = section.label;
    el.appendChild(h);

    const ul = document.createElement('ul');
    ul.className = 'menu-items';
    if (section.items && section.items.length) {
      section.items.forEach(it => {
        const li = document.createElement('li');
        const link = document.createElement('a');
        link.textContent = it.label || it;
        link.href = it.path || '#';
        link.style.textDecoration = 'none';
        link.style.color = 'inherit';
        li.appendChild(link);
        ul.appendChild(li);
      });
    }

    el.appendChild(ul);
    nav.appendChild(el);
  });
}

async function renderGames() {
  const gameGrid = document.getElementById('gameGrid');
  gameGrid.innerHTML = '';

  // load data files
  const menu = await loadJSON('menu.json');
  renderSidebar(menu || [{id:'games', label:'게임', items:[]}]);

  const list = await loadJSON('games.json');
  gamesData = list || gamesData;

  if (!gamesData || !gamesData.length) {
    gameGrid.innerHTML = '<p class="empty">등록된 게임이 없습니다.</p>';
    return;
  }

  gamesData.forEach(g => {
    const tile = createGameTile(g);
    gameGrid.appendChild(tile);
  });
}

document.addEventListener('DOMContentLoaded', renderGames);
