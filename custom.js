/* Triton docs custom JS.
 * Mintlify auto-loads any .js at the repo root globally.
 *
 * What this does:
 *   1. Moves the mobile drawer-trigger ("hamburger") into the navbar so
 *      it sits on the far right next to search/AI, instead of taking
 *      its own row below the logo. Achieved by keeping the original
 *      Mintlify button in place (we still need its React click handler)
 *      and rendering a slim proxy button inside #navbar that
 *      programmatically clicks the original. The original wrapper row
 *      is hidden via custom.css.
 *
 *   2. Re-opens the mobile drawer after a Next.js client-side
 *      navigation, if the user clicked a link from inside an open
 *      drawer. Lets Kate browse multiple tabs without the menu auto-
 *      collapsing each time. Uses sessionStorage as the cross-route
 *      breadcrumb.
 *
 *   3. (Stretch, best-effort) If the mobile drawer contains a tab
 *      dropdown ("Documentation / API reference / Guides / FAQs"),
 *      mirror the current selection so the proxy buttons stay in sync.
 *      We do NOT replace the dropdown wholesale — Mintlify's Radix
 *      Select owns its internal state and CSS-targeting that DOM is
 *      brittle. Replacement is deferred to a follow-up pass once the
 *      drawer DOM is mapped from a real device.
 */
(function () {
  'use strict';

  const HAMBURGER_SELECTOR = 'button.lg\\:hidden.h-14';
  const NAVBAR_ID = 'navbar';
  const PROXY_CLASS = 'triton-mobile-menu-btn';
  const FLAG = 'triton-drawer-was-open';

  function findHamburger() {
    return document.querySelector(HAMBURGER_SELECTOR);
  }

  function buildProxyButton(originalBtn) {
    const proxy = document.createElement('button');
    proxy.className = PROXY_CLASS;
    proxy.type = 'button';
    proxy.setAttribute('aria-label', 'Open menu');
    proxy.innerHTML =
      '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" ' +
      'stroke="currentColor" stroke-width="2" stroke-linecap="round" ' +
      'stroke-linejoin="round" aria-hidden="true">' +
      '<line x1="3" y1="6" x2="21" y2="6"></line>' +
      '<line x1="3" y1="12" x2="21" y2="12"></line>' +
      '<line x1="3" y1="18" x2="21" y2="18"></line>' +
      '</svg>';
    proxy.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      const live = findHamburger();
      if (live) live.click();
    });
    return proxy;
  }

  function ensureNavbarHamburger() {
    const navbar = document.getElementById(NAVBAR_ID);
    if (!navbar) return;
    if (navbar.querySelector('.' + PROXY_CLASS)) return;
    const original = findHamburger();
    if (!original) return;
    navbar.appendChild(buildProxyButton(original));
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
    ensureNavbarHamburger();
    flagDrawerNavClicks();
    reopenDrawerIfFlagged();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  let mutationScheduled = false;
  const obs = new MutationObserver(function () {
    if (mutationScheduled) return;
    mutationScheduled = true;
    requestAnimationFrame(function () {
      mutationScheduled = false;
      ensureNavbarHamburger();
    });
  });
  obs.observe(document.documentElement, { childList: true, subtree: true });
})();
