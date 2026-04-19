/**
 * 장윤이 게임 모음 — 루트 목록 페이지 스크립트
 *
 * 책임:
 *  1. games.json / menu.json 로드 (fetch 실패 대비 에러 표시)
 *  2. 게임 타일 그리드 렌더링
 *  3. 사이드바 메뉴 렌더링
 *
 * 모든 HTML은 document.createElement로 생성해 XSS를 원천 차단한다.
 */

(function () {
  'use strict';

  const ROOT = {
    grid: document.getElementById('gameGrid'),
    count: document.getElementById('gameCount'),
    sidebar: document.getElementById('sidebarNav'),
  };

  /** 안전한 JSON fetch — 실패 시 null 반환 */
  async function loadJSON(path) {
    try {
      const res = await fetch(path, { cache: 'no-cache' });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (err) {
      console.warn(`[games] Failed to load ${path}:`, err);
      return null;
    }
  }

  /** 게임 타일 생성 */
  function createGameTile(game) {
    const tile = document.createElement('a');
    tile.className = 'game-tile';
    tile.href = game.path || '#';
    tile.setAttribute('role', 'listitem');
    tile.setAttribute('aria-label', `${game.title_ko || game.title || '게임'} 플레이`);
    // 외부 링크면 새 탭
    if (/^https?:\/\//.test(game.path)) {
      tile.target = '_blank';
      tile.rel = 'noopener noreferrer';
    }

    const thumb = document.createElement('div');
    thumb.className = 'game-thumbnail';
    if (game.thumbnail) {
      thumb.style.backgroundImage = `url('${encodeURI(game.thumbnail)}')`;
    } else {
      thumb.classList.add('no-thumb');
      thumb.textContent = (game.title_ko || game.title || '?').charAt(0);
    }

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

    // 외부 링크 표시
    if (/^https?:\/\//.test(game.path)) {
      const badge = document.createElement('span');
      badge.className = 'external-badge';
      badge.textContent = '↗';
      badge.setAttribute('aria-label', '외부 링크');
      tile.appendChild(badge);
    }

    return tile;
  }

  /** 빈 상태 렌더링 */
  function renderEmpty(grid, message) {
    grid.innerHTML = '';
    const empty = document.createElement('p');
    empty.className = 'empty';
    empty.textContent = message;
    grid.appendChild(empty);
  }

  /** 게임 그리드 렌더링 */
  function renderGames(games) {
    const grid = ROOT.grid;
    grid.innerHTML = '';
    if (!games || games.length === 0) {
      renderEmpty(grid, '등록된 게임이 없습니다.');
      ROOT.count.textContent = '';
      return;
    }
    games.forEach(g => grid.appendChild(createGameTile(g)));
    ROOT.count.textContent = `총 ${games.length}개 게임`;
  }

  /** 사이드바 렌더링 */
  function renderSidebar(menu) {
    const nav = ROOT.sidebar;
    nav.innerHTML = '';
    if (!Array.isArray(menu) || menu.length === 0) return;

    menu.forEach(section => {
      const wrap = document.createElement('div');
      wrap.className = 'menu-section';
      if (section.label) {
        const h = document.createElement('h4');
        h.className = 'menu-section-title';
        h.textContent = section.label;
        wrap.appendChild(h);
      }
      const ul = document.createElement('ul');
      ul.className = 'menu-items';
      (section.items || []).forEach(item => {
        const li = document.createElement('li');
        const a = document.createElement('a');
        a.href = item.path || '#';
        a.textContent = item.label || item.id || '';
        if (/^https?:\/\//.test(item.path)) {
          a.target = '_blank';
          a.rel = 'noopener noreferrer';
        }
        li.appendChild(a);
        ul.appendChild(li);
      });
      wrap.appendChild(ul);
      nav.appendChild(wrap);
    });
  }

  /** 부팅 */
  async function boot() {
    const [games, menu] = await Promise.all([
      loadJSON('games.json'),
      loadJSON('menu.json')
    ]);
    renderGames(games);
    renderSidebar(menu);
  }

  // 페이지 로드 시 실행
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
