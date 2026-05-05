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
   Mermaid product-map clickability (welcome page)
   ============================================================
   Mintlify ships mermaid.js with the default `securityLevel: "strict"`,
   which silently rejects in-diagram `click NodeID "URL"` directives.
   To work around it: after each render, walk the rendered SVG, match
   each node's text label against a known product map, and bind a
   click handler on the node group. SPA-safe via MutationObserver.
   ============================================================ */
(function () {
  if (typeof window === 'undefined') return;

  var PRODUCT_LINKS = {
    'Standard RPC':              '/solana/reading-state/standard-rpc',
    'Steamboat':                 '/solana/streaming/steamboat/overview',
    'DAS API':                   '/solana/digital-assets/das-api/overview',
    'ZK Compression':            '/solana/digital-assets/zk-compression/overview',
    'Account Sync':              '/solana/reading-state/account-sync',
    'Dragons Mouth gRPC':        '/solana/streaming/dragons-mouth/overview',
    'Dragon’s Mouth gRPC':  '/solana/streaming/dragons-mouth/overview',
    'Whirligig':                 '/solana/streaming/whirligig/overview',
    'Fumarole':                  '/solana/streaming/fumarole/overview',
    'Hermes':                    '/solana/streaming/hermes/overview',
    'Pythnet':                   '/solana/streaming/pythnet/overview',
    'Hydrant':                   '/solana/history/hydrant/overview',
    'Old Faithful':              '/solana/history/old-faithful/overview',
    'Faithful Streams':          '/solana/history/faithful-streams/overview',
    'Yellowstone Jet':           '/solana/sending-transactions/yellowstone-jet/overview',
    'Priority Fees API':         '/solana/sending-transactions/priority-fees/overview',
    'Metis':                     '/solana/trading-apis/metis/overview',
    'Titan Prime':               '/solana/trading-apis/titan-prime/overview',
    'Jito Bundles':              '/solana/sending-transactions/jito-bundles/overview',
    'Dedicated gRPC node':       '/solana/reading-state/dedicated-grpc',
    'White-label validator':     '/solana/validators/white-label/overview',
    'Private trusted validator': '/solana/validators/private-trusted/overview'
  };

  function bindMermaidClicks() {
    var nodes = document.querySelectorAll('.mermaid svg g.node, [data-mermaid] svg g.node, svg.mermaid g.node');
    if (!nodes.length) return false;
    var bound = 0;
    nodes.forEach(function (node) {
      if (node.__tritonClickBound) return;
      var labelEl = node.querySelector('.nodeLabel, foreignObject span, text');
      if (!labelEl) return;
      var text = (labelEl.textContent || '').trim();
      if (!text) return;
      // Try exact match, then a normalised match (curly apostrophes etc)
      var url = PRODUCT_LINKS[text]
             || PRODUCT_LINKS[text.replace(/[’‘]/g, "'")]
             || PRODUCT_LINKS[text.replace(/'/g, '’')];
      if (!url) return;
      node.style.cursor = 'pointer';
      node.setAttribute('data-triton-link', url);
      node.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        // Mintlify is SPA — try History API first, fall back to assign
        try {
          if (window.history && window.history.pushState) {
            window.history.pushState({}, '', url);
            window.dispatchEvent(new PopStateEvent('popstate'));
          } else {
            window.location.href = url;
          }
        } catch (err) {
          window.location.href = url;
        }
      });
      node.__tritonClickBound = true;
      bound++;
    });
    return bound > 0;
  }

  // Initial pass (in case mermaid is already rendered)
  bindMermaidClicks();

  // Watch for SPA navigations + mermaid re-renders
  var scheduled = false;
  var obs = new MutationObserver(function () {
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(function () {
      scheduled = false;
      bindMermaidClicks();
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
    var simpleBlock = root.querySelector('[data-simple]');
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
      if (paygPanel) paygPanel.hidden = false;
      if (dediPanel) dediPanel.hidden = true;
      if (mode === 'simplified') {
        if (simpleBlock) simpleBlock.hidden = false;
        if (customBlock) customBlock.hidden = true;
        if (deposit) deposit.value = '125';
        recompute();
      } else if (mode === 'custom') {
        if (simpleBlock) simpleBlock.hidden = true;
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
      mode = mode ? mode.dataset.mode : 'simplified';
      if (mode === 'simplified') {
        var v = parseFloat(deposit && deposit.value) || 0;
        total = v;
      } else if (mode === 'custom') {
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
    var chainBtns = root.querySelectorAll('[data-chain]');
    var chainPriceEl = root.querySelector('[data-chain-price]');
    var chainFeaturesEl = root.querySelector('[data-chain-features]');
    var chainServicesEl = root.querySelector('[data-chain-services]');

    function setChain(key) {
      chainBtns.forEach(function (b) {
        b.classList.toggle('active', b.dataset.chain === key);
      });
      var c = chainData[key];
      if (!c) return;
      if (chainPriceEl) chainPriceEl.textContent = c.price;
      if (chainFeaturesEl) {
        chainFeaturesEl.innerHTML = c.features.map(function (f) { return '<li>' + f + '</li>'; }).join('');
      }
      if (chainServicesEl) {
        chainServicesEl.innerHTML = c.services.map(function (s) {
          return '<div class="triton-calc-row triton-calc-row-static">'
               +   '<div class="triton-calc-row-title">' + s[0] + '</div>'
               +   '<div class="triton-calc-row-rate">' + s[1] + '</div>'
               + '</div>';
        }).join('');
      }
    }
    chainBtns.forEach(function (b) {
      b.addEventListener('click', function () { setChain(b.dataset.chain); });
    });

    /* Initial state */
    setMode('simplified');
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
    slot: {
      label: 'Latest slot',
      method: 'getSlot',
      params: [],
      blurb: 'What slot is the network on right now?'
    },
    balance: {
      label: 'Wallet SOL balance',
      method: 'getBalance',
      params: ['86xCnPeV69n6t3DnyGvkKobf9FdN2H9oiVDdaMpo2MMY'],
      blurb: 'SOL balance for Anatoly Yakovenko\'s wallet.'
    },
    tokens: {
      label: 'Wallet tokens',
      method: 'getTokenAccountsByOwner',
      params: [
        '86xCnPeV69n6t3DnyGvkKobf9FdN2H9oiVDdaMpo2MMY',
        { programId: 'TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA' },
        { encoding: 'jsonParsed' }
      ],
      blurb: 'All SPL token accounts for this wallet.'
    },
    fees: {
      label: 'Priority fees right now',
      method: 'getRecentPrioritizationFees',
      params: [],
      blurb: 'Per-slot prioritization fees from the last few hundred slots.'
    },
    epoch: {
      label: 'Epoch info',
      method: 'getEpochInfo',
      params: [],
      blurb: 'Current epoch, slot, absolute slot, transaction count.'
    },
    version: {
      label: 'Cluster version',
      method: 'getVersion',
      params: [],
      blurb: 'What software is the cluster running?'
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
    var current = 'slot';

    function selectTask(key) {
      if (!TASKS[key]) return;
      current = key;
      tabs.forEach(function (t) {
        t.classList.toggle('active', t.dataset.task === key);
      });
      if (codeEl) codeEl.textContent = buildCurl(TASKS[key]);
      if (outputEl) outputEl.textContent = '// Click "Run on mainnet" to execute. ' + TASKS[key].blurb;
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
