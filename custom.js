/* Triton docs custom JS.
 * Mintlify auto-loads any .js at the repo root globally.
 *
 * What this does:
 *   1. Replaces the tab dropdown ("Documentation / API reference /
 *      Guides / FAQs") inside the open mobile drawer with 4 real
 *      sibling buttons positioned BELOW the Solana chain dropdown.
 *      Detection: any <button> on mobile whose textContent equals
 *      one of the 4 known tab labels. No class requirement.
 *
 *   2. Re-opens the mobile drawer after a Next.js client-side
 *      navigation, if the user clicked a link from inside an open
 *      drawer. Lets you browse multiple tabs without the menu
 *      auto-collapsing each time. Uses sessionStorage as the
 *      cross-route breadcrumb.
 *
 * Hamburger reposition is CSS-only via `position: fixed` on
 * Mintlify's `lg:hidden h-14` button (custom.css §23).
 */
(function () {
  'use strict';

  const HAMBURGER_SELECTOR = 'button[class*="lg:hidden"][class*="h-14"]';
  const FLAG = 'triton-drawer-was-open';

  // Inline lucide SVGs matching the icons set in docs.json tabs config.
  // Keep these in sync with the icon names assigned per tab so the
  // mobile buttons mirror the desktop top-bar.
  const ICON_SVG = {
    'book-open':
      '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>',
    code:
      '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>',
    compass:
      '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>',
    'messages-square':
      '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 9a2 2 0 0 1-2 2H6l-4 4V4c0-1.1.9-2 2-2h8a2 2 0 0 1 2 2z"/><path d="M18 9h2a2 2 0 0 1 2 2v11l-4-4h-6a2 2 0 0 1-2-2v-1"/></svg>'
  };

  // Tab config:
  //   key   = exact text of the Mintlify trigger button (what we
  //          match against in the drawer). DO NOT change without
  //          checking the Mintlify-rendered text.
  //   label = what we display in our replacement button (free to
  //          rename for UX).
  //   icon  = lucide icon name from ICON_SVG, mirrors docs.json
  //          tabs[].icon for the desktop top-bar.
  //   href  = first page of that tab.
  // Right now only Solana has tabs — other chains ship a single tab
  // so the dropdown doesn't appear for them.
  const TAB_CONFIG = [
    { key: 'Documentation', label: 'Docs', icon: 'book-open', href: '/solana/welcome' },
    { key: 'API reference', label: 'API methods', icon: 'code', href: '/solana-api/api-overview' },
    { key: 'Guides', label: 'Guides', icon: 'compass', href: '/solana-guides/error-handling' },
    { key: 'FAQs', label: 'FAQs', icon: 'messages-square', href: '/solana-faqs/general' }
  ];
  const TAB_LABELS = TAB_CONFIG.map(function (t) { return t.key; });

  // Labels of chain triggers — used to find the Solana button so we
  // can insert the tab buttons immediately after it.
  const CHAIN_LABELS = ['Solana', 'Pyth', 'SUI', 'Monad'];

  const PROCESSED_FLAG = 'data-triton-tabs-replaced';
  const DEBUG_MARKER = '__tritonCustomJsLoaded';
  window[DEBUG_MARKER] = (window[DEBUG_MARKER] || 0) + 1;

  function findHamburger() {
    return document.querySelector(HAMBURGER_SELECTOR);
  }

  function isOpenDrawer(el) {
    if (!el || !el.closest) return false;
    return Boolean(
      el.closest('[data-state="open"][role="dialog"]') ||
        el.closest('[data-radix-dialog-content][data-state="open"]') ||
        el.closest('[data-vaul-drawer][data-state="open"]') ||
        el.closest('[data-state="open"][aria-modal="true"]')
    );
  }

  /* ---- Tab-row replacement -------------------------------------- */

  function buildTabRow(currentKey) {
    const row = document.createElement('div');
    row.className = 'triton-mobile-tab-row';
    row.setAttribute(PROCESSED_FLAG, 'row');
    TAB_CONFIG.forEach(function (tab) {
      const a = document.createElement('a');
      a.href = tab.href;
      a.className = 'triton-mobile-tab-btn';
      a.setAttribute('data-tab-key', tab.key);
      const iconHtml = ICON_SVG[tab.icon] || '';
      a.innerHTML =
        '<span class="triton-mobile-tab-icon">' + iconHtml + '</span>' +
        '<span class="triton-mobile-tab-label">' + tab.label + '</span>';
      if (tab.key === currentKey) a.setAttribute('aria-current', 'page');
      a.addEventListener('click', function () {
        try {
          sessionStorage.setItem(FLAG, '1');
        } catch (_) {}
      });
      row.appendChild(a);
    });
    return row;
  }

  function isVisible(el) {
    if (!el) return false;
    if (el.offsetParent === null && getComputedStyle(el).position !== 'fixed') {
      return false;
    }
    const cs = getComputedStyle(el);
    return cs.display !== 'none' && cs.visibility !== 'hidden';
  }

  function findVisibleByText(textPredicate) {
    const buttons = document.querySelectorAll('button, a[role="button"], [role="button"]');
    for (let i = 0; i < buttons.length; i++) {
      const btn = buttons[i];
      if (btn.hasAttribute(PROCESSED_FLAG)) continue;
      const txt = (btn.textContent || '').trim();
      if (!textPredicate(txt)) continue;
      if (!isVisible(btn)) continue;
      return btn;
    }
    return null;
  }

  function findTabTrigger() {
    return findVisibleByText(function (t) {
      return TAB_LABELS.indexOf(t) !== -1;
    });
  }

  function findChainTrigger() {
    return findVisibleByText(function (t) {
      return CHAIN_LABELS.indexOf(t) !== -1;
    });
  }

  function findCommonAncestor(a, b) {
    const seen = new Set();
    let n = a;
    while (n) {
      seen.add(n);
      n = n.parentNode;
    }
    n = b;
    while (n) {
      if (seen.has(n)) return n;
      n = n.parentNode;
    }
    return null;
  }

  function findChildOfAncestor(node, ancestor) {
    while (node && node.parentNode && node.parentNode !== ancestor) {
      node = node.parentNode;
    }
    return node && node.parentNode === ancestor ? node : null;
  }

  function replaceTabTrigger() {
    if (window.innerWidth >= 1024) return;
    const tabBtn = findTabTrigger();
    if (!tabBtn) return;
    const currentLabel = (tabBtn.textContent || '').trim();
    const row = buildTabRow(currentLabel);

    // Mark + hide the original trigger so subsequent passes skip it
    tabBtn.setAttribute(PROCESSED_FLAG, 'hidden');
    tabBtn.style.display = 'none';

    // Place the row AFTER the chain (Solana) trigger's branch.
    // Falls back to in-place if no chain trigger or no common ancestor.
    const chainBtn = findChainTrigger();
    let placed = false;
    if (chainBtn) {
      const cca = findCommonAncestor(chainBtn, tabBtn);
      if (cca) {
        const chainBranch = findChildOfAncestor(chainBtn, cca);
        if (chainBranch) {
          cca.insertBefore(row, chainBranch.nextSibling);
          placed = true;
        }
      }
    }
    if (!placed) {
      tabBtn.parentNode.insertBefore(row, tabBtn);
    }
    window[DEBUG_MARKER + '_replacedAt'] = Date.now();
    window[DEBUG_MARKER + '_placedAfterChain'] = placed;
  }

  /* ---- Persist drawer across navigations ------------------------ */

  function flagDrawerNavClicks() {
    document.addEventListener(
      'click',
      function (e) {
        const link = e.target.closest('a[href]');
        if (!link) return;
        if (!isOpenDrawer(link) && window.innerWidth >= 1024) return;
        try {
          sessionStorage.setItem(FLAG, '1');
        } catch (_) {}
      },
      true
    );
  }

  function reopenDrawerIfFlagged() {
    let raised;
    try {
      raised = sessionStorage.getItem(FLAG);
    } catch (_) {
      return;
    }
    if (raised !== '1') return;
    try {
      sessionStorage.removeItem(FLAG);
    } catch (_) {}
    if (window.innerWidth >= 1024) return;
    let attempts = 0;
    const tick = function () {
      const h = findHamburger();
      if (h) {
        h.click();
        return;
      }
      if (++attempts < 30) setTimeout(tick, 80);
    };
    setTimeout(tick, 250);
  }

  /* ---- Init + observe ------------------------------------------- */

  function init() {
    flagDrawerNavClicks();
    reopenDrawerIfFlagged();
    replaceTabTrigger();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  let scheduled = false;
  const obs = new MutationObserver(function () {
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(function () {
      scheduled = false;
      replaceTabTrigger();
    });
  });
  obs.observe(document.documentElement, { childList: true, subtree: true });
})();
