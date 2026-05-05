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

/* ============================================================
   Pricing calculator (plans-and-billing.mdx)
   ============================================================
   Drives the [data-triton-calc] block. Mode toggle (simple PAYG /
   custom PAYG / dedicated nodes), slider updates, total recompute,
   CTA enable/disable, dedicated-chain switcher.
   ============================================================ */
(function () {
  if (typeof window === 'undefined') return;

  function fmtUSD(n) {
    return '$' + n.toFixed(2);
  }
  function fmtBandwidth(v) {
    return v >= 1000 ? (v / 1000).toFixed(1) + 'K' : String(v);
  }
  function fmtMillions(v) {
    return v.toFixed(1) + 'M';
  }

  function initCalc(root) {
    if (root.__tritonCalcInit) return;
    root.__tritonCalcInit = true;

    var modeBtns = root.querySelectorAll('[data-mode]');
    var paygPanel = root.querySelector('[data-panel="payg"]');
    var dediPanel = root.querySelector('[data-panel="dedicated"]');
    var customBlock = root.querySelector('[data-custom]');
    var deposit = root.querySelector('[data-deposit]');
    var totalEl = root.querySelector('[data-total]');
    var ctaEl = root.querySelector('[data-panel="payg"] [data-cta]');
    var warnEl = root.querySelector('[data-warn]');

    var sliderRows = root.querySelectorAll('[data-slider]');

    function setMode(mode) {
      modeBtns.forEach(function (b) {
        b.classList.toggle('active', b.dataset.mode === mode);
      });
      if (mode === 'dedicated') {
        if (paygPanel) paygPanel.hidden = true;
        if (dediPanel) dediPanel.hidden = false;
        return;
      }
      // PAYG mode (Custom PAYG only -- the simplified mode was removed)
      if (paygPanel) paygPanel.hidden = false;
      if (dediPanel) dediPanel.hidden = true;
      if (customBlock) customBlock.hidden = false;
      sliderRows.forEach(function (row) {
        var input = row.querySelector('[data-input]');
        if (input) {
          input.value = '0';
          updateSliderRow(row);
        }
      });
      recompute();
    }

    function updateSliderRow(row) {
      var input = row.querySelector('[data-input]');
      var fill = row.querySelector('[data-fill]');
      var label = row.querySelector('[data-label]');
      var amount = row.querySelector('[data-amount]');
      if (!input) return;
      var val = parseFloat(input.value) || 0;
      var min = parseFloat(input.min) || 0;
      var max = parseFloat(input.max) || 100;
      var pct = ((val - min) / (max - min)) * 100;
      if (fill) fill.style.width = pct + '%';
      if (label) {
        if (val > min) {
          label.hidden = false;
          var fmt = row.dataset.format;
          label.textContent = fmt === 'millions' ? fmtMillions(val) : fmtBandwidth(val);
          label.style.left = 'calc(' + pct + '% + ' + (10 - pct * 0.2) + 'px)';
        } else {
          label.hidden = true;
        }
      }
      if (amount) {
        var price = parseFloat(row.dataset.price) || 0;
        amount.textContent = fmtUSD(val * price);
      }
    }

    function recompute() {
      var total = 0;
      var mode = root.querySelector('[data-mode].active');
      mode = mode ? mode.dataset.mode : 'custom';
      // PAYG (custom) mode: sum all sliders
      if (mode === 'custom') {
        sliderRows.forEach(function (row) {
          var input = row.querySelector('[data-input]');
          if (!input) return;
          var val = parseFloat(input.value) || 0;
          var price = parseFloat(row.dataset.price) || 0;
          total += val * price;
        });
        if (deposit) deposit.value = total.toFixed(2);
      }
      if (totalEl) totalEl.textContent = fmtUSD(total);
      if (ctaEl && warnEl) {
        if (total < 125) {
          ctaEl.classList.add('disabled');
          ctaEl.setAttribute('aria-disabled', 'true');
          warnEl.hidden = false;
        } else {
          ctaEl.classList.remove('disabled');
          ctaEl.removeAttribute('aria-disabled');
          warnEl.hidden = true;
        }
      }
    }

    modeBtns.forEach(function (b) {
      b.addEventListener('click', function () { setMode(b.dataset.mode); });
    });
    sliderRows.forEach(function (row) {
      var input = row.querySelector('[data-input]');
      if (input) input.addEventListener('input', function () {
        updateSliderRow(row);
        recompute();
      });
    });
    if (deposit) {
      deposit.addEventListener('input', recompute);
      deposit.addEventListener('blur', function () {
        var v = parseFloat(deposit.value) || 0;
        if (v < 125) deposit.value = '125';
        recompute();
      });
    }

    /* Dedicated-mode chain switcher */
    var chainData = {
      solana: {
        price: '$2,900+',
        features: [
          'Unmetered gRPC streaming',
          'Full access to Yellowstone suite and advanced APIs',
          'Custom geolocated deployment',
          'Isolated performance, dedicated to your traffic',
          'Advanced controls and tuning for your workload',
          'GeoDNS routing and automatic failover',
          '1-on-1 support from senior engineers'
        ],
        services: [
          ["gRPC streaming (Dragon's Mouth)", "Included in the node price, no overage fees"],
          ["Fumarole, Whirligig, WebSockets, other streaming", "$0.08 / GB bandwidth"],
          ["Standard RPC, indexed accounts, ledger queries", "$0.08 / GB bandwidth + $10 / million calls"],
          ["Metaplex, Photon APIs", "$0.08 / GB bandwidth + $50 / million calls"],
          ["Metis API", "$0.08 / GB bandwidth + $80 / million calls"],
          ["Titan API", "$0.08 / GB bandwidth + $80 / million calls"]
        ]
      },
      pythnet: {
        price: '$2,000+',
        features: [
          'Unmetered streaming services',
          'Custom geolocated deployment',
          'Isolated performance, dedicated to your traffic',
          'Advanced controls and tuning for your workload',
          'GeoDNS routing and automatic failover',
          '1-on-1 support from senior engineers'
        ],
        services: [
          ["Streaming services", "Included in the node price, no overage fees"],
          ["Standard RPC", "$0.08 / GB bandwidth + $10 / million calls"],
          ["Hermes REST API queries", "$0.08 / GB bandwidth + $10 / million calls"]
        ]
      },
      monad: {
        price: '$2,900+',
        features: [
          'Unmetered streaming services',
          'Custom geolocated deployment',
          'Isolated performance, dedicated to your traffic',
          'Advanced controls and tuning for your workload',
          'GeoDNS routing and automatic failover',
          '1-on-1 support from senior engineers'
        ],
        services: [
          ["Streaming services", "Included in the node price, no overage fees"],
          ["Standard RPC", "$0.08 / GB bandwidth + $10 / million calls"]
        ]
      },
      sui: {
        price: '$2,000+',
        features: [
          'Unmetered streaming services',
          'Complete access to Seal and Walrus',
          'Custom geolocated deployment',
          'Isolated performance, dedicated to your traffic',
          'Advanced controls and tuning for your workload',
          'GeoDNS routing and automatic failover',
          '1-on-1 support from senior engineers'
        ],
        services: [
          ["Streaming services", "Included in the node price, no overage fees"],
          ["Standard RPC", "$0.08 / GB bandwidth + $10 / million calls"]
        ]
      }
    };
    /* Chain switcher removed -- dedicated panel hardcoded to Solana
       (in MDX). The chainData map is kept above so we can re-add other
       chains later, but no buttons exist in the DOM anymore. */

    /* Initial state -- Custom PAYG is now the default (Simple PAYG removed) */
    setMode('custom');
    recompute();
  }

  function scan() {
    document.querySelectorAll('[data-triton-calc]').forEach(initCalc);
  }
  scan();

  var obs = new MutationObserver(function () {
    requestAnimationFrame(scan);
  });
  obs.observe(document.documentElement, { childList: true, subtree: true });
})();

/* ============================================================
   Try-it-out (welcome page Solana RPC playground)
   ============================================================
   Stripe-style: tabs across the top, code preview, Run button,
   live JSON-RPC POST against api.mainnet.solana.com (the public
   Solana Foundation endpoint, CORS-enabled, no key needed).
   ============================================================ */
(function () {
  if (typeof window === 'undefined') return;

  var ENDPOINT = 'https://api.mainnet.solana.com';

  var TASKS = {
    balance: {
      label: 'Wallet balance',
      method: 'getBalance',
      params: ['86xCnPeV69n6t3DnyGvkKobf9FdN2H9oiVDdaMpo2MMY'],
      blurb: 'SOL balance for any wallet on mainnet.'
    },
    accountInfo: {
      label: 'getAccountInfo for a token mint',
      method: 'getAccountInfo',
      params: [
        'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v',
        { encoding: 'jsonParsed', commitment: 'confirmed' }
      ],
      blurb: 'Full account state for a token mint -- here, USDC.'
    },
    history: {
      label: 'Address history',
      method: 'getSignaturesForAddress',
      params: [
        '86xCnPeV69n6t3DnyGvkKobf9FdN2H9oiVDdaMpo2MMY',
        { limit: 10 }
      ],
      blurb: 'Most recent transaction signatures for an address.'
    },
    fees: {
      label: 'Priority fee (with percentiles)',
      method: 'getRecentPrioritizationFees',
      params: [
        ['EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v']
      ],
      blurb: 'Per-slot prioritization fees from the last few hundred slots.'
    },
    sendTx: {
      label: 'Send a transaction',
      method: 'sendTransaction',
      params: [
        '<base64-encoded signed transaction>',
        { encoding: 'base64', skipPreflight: false, preflightCommitment: 'confirmed' }
      ],
      blurb: 'Submit a signed transaction. Replace the placeholder with your own base64 payload to actually run.'
    },
    streamAccounts: {
      label: 'Stream account changes',
      method: 'accountSubscribe',
      params: [
        'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v',
        { encoding: 'jsonParsed', commitment: 'confirmed' }
      ],
      blurb: 'WebSocket subscription that pushes account state updates as they land. (Requires a WS endpoint -- this curl shows the JSON-RPC shape.)'
    }
  };

  function buildBody(task) {
    return JSON.stringify({
      jsonrpc: '2.0',
      id: 1,
      method: task.method,
      params: task.params
    });
  }

  function buildCurl(task) {
    var body = buildBody(task);
    return 'curl ' + ENDPOINT + ' -X POST \\\n  -H "Content-Type: application/json" \\\n  -d \'' + body + '\'';
  }

  function pretty(json) {
    try { return JSON.stringify(json, null, 2); }
    catch (e) { return String(json); }
  }

  function initTry(root) {
    if (root.__tritonTryInit) return;
    root.__tritonTryInit = true;

    var tabs = root.querySelectorAll('[data-task]');
    var codeEl = root.querySelector('[data-code]');
    var runBtn = root.querySelector('[data-run]');
    var outputEl = root.querySelector('[data-output]');
    var statusEl = root.querySelector('[data-status]');
    var current = 'balance';

    function selectTask(key) {
      if (!TASKS[key]) return;
      current = key;
      tabs.forEach(function (t) {
        t.classList.toggle('active', t.dataset.task === key);
      });
      if (codeEl) codeEl.textContent = buildCurl(TASKS[key]);
      // Empty until the user clicks Run -- no placeholder note.
      if (outputEl) outputEl.textContent = '';
      if (statusEl) statusEl.textContent = '';
    }

    function runCurrent() {
      var task = TASKS[current];
      if (!task) return;
      if (statusEl) statusEl.textContent = 'sending...';
      if (outputEl) outputEl.textContent = '// requesting...';
      runBtn.disabled = true;
      var t0 = performance.now();
      fetch(ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: buildBody(task)
      })
        .then(function (r) { return r.json(); })
        .then(function (json) {
          var ms = Math.round(performance.now() - t0);
          if (statusEl) statusEl.textContent = '' + ms + ' ms · ' + ENDPOINT;
          if (outputEl) outputEl.textContent = pretty(json);
        })
        .catch(function (err) {
          if (statusEl) statusEl.textContent = 'error';
          if (outputEl) outputEl.textContent = '// error: ' + (err && err.message ? err.message : String(err));
        })
        .finally(function () {
          runBtn.disabled = false;
        });
    }

    tabs.forEach(function (t) {
      t.addEventListener('click', function () { selectTask(t.dataset.task); });
    });
    if (runBtn) runBtn.addEventListener('click', runCurrent);

    selectTask(current);
  }

  function scan() {
    document.querySelectorAll('[data-triton-try]').forEach(initTry);
  }
  scan();
  var obs = new MutationObserver(function () { requestAnimationFrame(scan); });
  obs.observe(document.documentElement, { childList: true, subtree: true });
})();


/* ============================================================
   Sidebar dropdowns: persist user-toggled state across pages
   ============================================================
   Mintlify auto-collapses sidebar groups that aren't on the active
   route. Kate wants groups to stay open once a user opens them, only
   closing when the user clicks the toggle again. This module:

   1. Watches the DOM for `<button aria-label="Toggle X section" ...>`.
   2. On first sight, reads localStorage for the saved set of opened
      groups; if a group is in the set but currently collapsed, it
      simulates a click to open it.
   3. On user click, writes the new state back to localStorage after
      the framework toggles aria-expanded.
   ============================================================ */
(function () {
  if (typeof window === 'undefined') return;

  var STORAGE_KEY = 'triton-sidebar-open-groups';

  function readState() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return new Set();
      return new Set(JSON.parse(raw));
    } catch (e) {
      return new Set();
    }
  }
  function writeState(set) {
    try {
      var arr = [];
      set.forEach(function (v) { arr.push(v); });
      localStorage.setItem(STORAGE_KEY, JSON.stringify(arr));
    } catch (e) {}
  }

  function bindToggles() {
    var btns = document.querySelectorAll('button[aria-label^="Toggle "][aria-label$=" section"]');
    if (!btns.length) return;
    var state = readState();

    btns.forEach(function (btn) {
      var label = btn.getAttribute('aria-label');
      if (!label) return;

      // Restore state if needed
      var isOpen = btn.getAttribute('aria-expanded') === 'true';
      var wantOpen = state.has(label);
      if (wantOpen && !isOpen && !btn.__tritonRestored) {
        btn.__tritonRestored = true;
        // Click without scroll-into-view side-effects
        try { btn.click(); } catch (e) {}
      }

      if (btn.__tritonStickyBound) return;
      btn.__tritonStickyBound = true;
      btn.addEventListener('click', function () {
        // Wait a tick for aria-expanded to flip, then save
        setTimeout(function () {
          var nowOpen = btn.getAttribute('aria-expanded') === 'true';
          var s = readState();
          if (nowOpen) s.add(label); else s.delete(label);
          writeState(s);
        }, 60);
      });
    });
  }

  bindToggles();
  var obs = new MutationObserver(function () {
    requestAnimationFrame(bindToggles);
  });
  obs.observe(document.documentElement, { childList: true, subtree: true });
})();
