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

  // Tab config:
  //   key   = exact text of the Mintlify trigger button (what we
  //          match against in the drawer). DO NOT change without
  //          checking the Mintlify-rendered text.
  //   label = what we display in our replacement button (free to
  //          rename for UX).
  //   href  = first page of that tab.
  // Right now only Solana has tabs — other chains ship a single tab
  // so the dropdown doesn't appear for them.
  const TAB_CONFIG = [
    { key: 'Documentation', label: 'Docs', href: '/solana/welcome' },
    { key: 'API reference', label: 'API methods', href: '/solana-api/api-overview' },
    { key: 'Guides', label: 'Guides', href: '/solana-guides/error-handling' },
    { key: 'FAQs', label: 'FAQs', href: '/solana-faqs/general' }
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
      a.textContent = tab.label;
      a.setAttribute('data-tab-key', tab.key);
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
