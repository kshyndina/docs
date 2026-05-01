/* Triton docs custom JS.
 * Mintlify auto-loads any .js at the repo root globally.
 *
 * What this does:
 *   1. Replaces the tab dropdown ("Documentation / API reference /
 *      Guides / FAQs") inside the open mobile drawer with 4 real
 *      sibling buttons. Each button navigates to the first page of
 *      its tab (Documentation → /solana/welcome, etc.).
 *
 *   2. Re-opens the mobile drawer after a Next.js client-side
 *      navigation, if the user clicked a link from inside an open
 *      drawer. Lets Kate browse multiple tabs without the menu auto-
 *      collapsing each time. Uses sessionStorage as cross-route
 *      breadcrumb.
 *
 * Hamburger reposition is handled CSS-only via `position: fixed` on
 * the original Mintlify hamburger button (custom.css §23).
 */
(function () {
  'use strict';

  const HAMBURGER_SELECTOR = 'button[class*="lg:hidden"][class*="h-14"]';
  const FLAG = 'triton-drawer-was-open';

  // Mapping of tab label → first page URL. Add other chain dropdowns
  // here when they grow tabs. Right now only Solana has tabs.
  const TAB_DESTINATIONS = {
    Documentation: '/solana/welcome',
    'API reference': '/solana-api/api-overview',
    Guides: '/solana-guides/error-handling',
    FAQs: '/solana-faqs/general'
  };
  const TAB_LABELS = Object.keys(TAB_DESTINATIONS);
  const PROCESSED_FLAG = 'data-triton-tabs-replaced';

  function findHamburger() {
    return document.querySelector(HAMBURGER_SELECTOR);
  }

  function isOpenDrawer(el) {
    if (!el || !el.closest) return false;
    return Boolean(
      el.closest('[data-state="open"][role="dialog"]') ||
        el.closest('[data-radix-dialog-content][data-state="open"]')
    );
  }

  function findOpenDrawer() {
    return (
      document.querySelector('[data-state="open"][role="dialog"]') ||
      document.querySelector('[data-radix-dialog-content][data-state="open"]')
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

  function isTabTrigger(btn) {
    if (!btn) return false;
    const txt = (btn.textContent || '').trim();
    // Match if the trigger's text is one of the 4 known tab labels.
    return TAB_LABELS.indexOf(txt) !== -1;
  }

  function replaceTabTriggerInsideDrawer() {
    // Mobile only — at lg+ the sidebar shows the same trigger and we
    // leave it alone (Mintlify's tab pill row covers it).
    if (window.innerWidth >= 1024) return;
    const triggers = document.querySelectorAll(
      'button.nav-dropdown-trigger, button[aria-haspopup="menu"][class*="nav-dropdown"]'
    );
    triggers.forEach(function (btn) {
      if (btn.hasAttribute(PROCESSED_FLAG)) return;
      if (!isTabTrigger(btn)) return;
      const currentLabel = (btn.textContent || '').trim();
      const row = buildTabRow(currentLabel);
      btn.setAttribute(PROCESSED_FLAG, 'hidden');
      btn.style.display = 'none';
      // Insert the row right where the trigger sat
      btn.parentNode.insertBefore(row, btn);
    });
  }

  /* ---- Persist drawer across navigations ------------------------ */

  function flagDrawerNavClicks() {
    document.addEventListener(
      'click',
      function (e) {
        const link = e.target.closest('a[href]');
        if (!link) return;
        if (!isOpenDrawer(link)) return;
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
    replaceTabTriggerInsideDrawer();
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
      replaceTabTriggerInsideDrawer();
    });
  });
  obs.observe(document.documentElement, { childList: true, subtree: true });
})();
