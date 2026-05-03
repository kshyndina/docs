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

  // Mapping of tab label → first page URL. Right now only Solana has
  // tabs; other chains (Pyth/SUI/Monad) ship a single tab so the
  // dropdown doesn't appear for them.
  const TAB_DESTINATIONS = {
    Documentation: '/solana/welcome',
    'API reference': '/solana-api/api-overview',
    Guides: '/solana-guides/error-handling',
    FAQs: '/solana-faqs/general'
  };
  const TAB_LABELS = Object.keys(TAB_DESTINATIONS);

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

  function buildTabRow(currentLabel) {
    const row = document.createElement('div');
    row.className = 'triton-mobile-tab-row';
    row.setAttribute(PROCESSED_FLAG, 'row');
    TAB_LABELS.forEach(function (label) {
      const a = document.createElement('a');
      a.href = TAB_DESTINATIONS[label];
      a.className = 'triton-mobile-tab-btn';
      a.textContent = label;
      if (label === currentLabel) a.setAttribute('aria-current', 'page');
      a.addEventListener('click', function () {
        try {
          sessionStorage.setItem(FLAG, '1');
        } catch (_) {}
      });
      row.appendChild(a);
    });
    return row;
  }

  function findTabTrigger() {
    // Match any <button> at mobile whose plain text equals a tab
    // label. No class requirement — Mintlify's mobile drawer trigger
    // doesn't always carry `nav-dropdown-trigger`.
    const buttons = document.querySelectorAll('button');
    for (let i = 0; i < buttons.length; i++) {
      const btn = buttons[i];
      if (btn.hasAttribute(PROCESSED_FLAG)) continue;
      const txt = (btn.textContent || '').trim();
      if (TAB_LABELS.indexOf(txt) !== -1) return btn;
    }
    return null;
  }

  function findChainTrigger() {
    // The chain selector ("Solana") sits above the tab selector in
    // the drawer. We anchor the new button row immediately after it.
    const buttons = document.querySelectorAll('button');
    for (let i = 0; i < buttons.length; i++) {
      const txt = (buttons[i].textContent || '').trim();
      if (CHAIN_LABELS.indexOf(txt) !== -1) return buttons[i];
    }
    return null;
  }

  function findInsertionAnchor(tabBtn) {
    // Walk up from the tab trigger to find a sibling-group ancestor
    // — the wrapper that contains both the chain selector and the
    // tab selector. We want to insert the row inside that wrapper,
    // after the chain trigger's row.
    const chain = findChainTrigger();
    if (!chain) return null;
    // Find the closest common ancestor of chain + tabBtn.
    let node = chain;
    while (node && node !== document.body) {
      if (node.contains(tabBtn)) {
        // node is the common ancestor. Find the chain's direct child
        // of `node` and insert after it.
        let chainChild = chain;
        while (chainChild.parentNode && chainChild.parentNode !== node) {
          chainChild = chainChild.parentNode;
        }
        return { parent: node, after: chainChild };
      }
      node = node.parentNode;
    }
    return null;
  }

  function replaceTabTrigger() {
    if (window.innerWidth >= 1024) return;
    const tabBtn = findTabTrigger();
    if (!tabBtn) return;
    const currentLabel = (tabBtn.textContent || '').trim();
    const row = buildTabRow(currentLabel);

    // Hide the original trigger
    tabBtn.setAttribute(PROCESSED_FLAG, 'hidden');
    tabBtn.style.display = 'none';

    // Insert the 4-button row AFTER the Solana chain trigger (Kate's
    // requested order). Fallback: in-place where the tab trigger sat.
    const anchor = findInsertionAnchor(tabBtn);
    if (anchor) {
      anchor.parent.insertBefore(row, anchor.after.nextSibling);
    } else {
      tabBtn.parentNode.insertBefore(row, tabBtn);
    }
    window[DEBUG_MARKER + '_replacedAt'] = Date.now();
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
