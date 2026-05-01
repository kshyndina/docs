/* Triton docs custom JS.
 * Mintlify auto-loads any .js at the repo root globally.
 *
 * What this does:
 *   Re-opens the mobile drawer after a Next.js client-side navigation,
 *   if the user clicked a link from inside an open drawer. Lets Kate
 *   browse multiple tabs without the menu auto-collapsing each time.
 *   Uses sessionStorage as the cross-route breadcrumb.
 *
 * The hamburger reposition (was previously injected as a #navbar
 * proxy) is now handled CSS-only via `position: fixed` on the
 * original Mintlify hamburger button. See custom.css §23.
 */
(function () {
  'use strict';

  const HAMBURGER_SELECTOR = 'button[class*="lg:hidden"][class*="h-14"]';
  const FLAG = 'triton-drawer-was-open';

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
      if (++attempts < 20) setTimeout(tick, 80);
    };
    setTimeout(tick, 250);
  }

  function init() {
    flagDrawerNavClicks();
    reopenDrawerIfFlagged();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
