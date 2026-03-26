/* sw-verify.js - staging verification helper */
(async () => {
  const log = (...args) => console.log('[VERIFY]', ...args);
  const err = (...args) => console.error('[VERIFY]', ...args);
  try {
    if (!('serviceWorker' in navigator)) {
      return err('Service Worker not supported in this browser');
    }
    log('Waiting for Service Worker readiness...');
    const reg = await navigator.serviceWorker.ready;
    log('SW ready:', reg && reg.scope);

    const MANIFEST_URL = '/assets/cache-manifest.json';
    const res = await fetch(MANIFEST_URL, { cache: 'no-cache' });
    if (!res.ok) {
      return err('Failed to fetch cache-manifest.json:', res.status, res.statusText);
    }
    const manifest = await res.json();
    const expected = Array.isArray(manifest.staticFiles) ? manifest.staticFiles.length : 0;
    log('Manifest version:', manifest.version, 'files:', expected);

    const keys = await caches.keys();
    const staticKey = keys.find(k => /polytrack-static-v/.test(k));
    if (!staticKey) {
      return err('Static cache not found. Keys=', keys);
    }
    const cache = await caches.open(staticKey);
    const requests = await cache.keys();
    const cachedUrls = requests.map(r => r.url);
    log('Static cache:', staticKey, 'entries:', requests.length);

    // Check required entries
    const required = ['/', '/index.html', '/assets/styles.css', '/sw.js'];
    const missing = required.filter(p => !cachedUrls.some(u => u.endsWith(p)));
    if (missing.length) {
      err('Missing required cached files:', missing);
    } else {
      log('Required files cached ✓');
    }

    // Quick assets spot check (images/fonts if any)
    const spotList = ['/assets/logo.svg', '/assets/og-cover.jpg'];
    for (const p of spotList) {
      const hit = await cache.match(p);
      log('Cache match', p, Boolean(hit));
    }

    // Summary
    const okCount = requests.length >= expected;
    if (okCount) {
      log('Cache Storage contains >= manifest count ✓');
    } else {
      err('Cache Storage entries < manifest count:', requests.length, '<', expected);
    }
    log('To test offline: toggle DevTools Network → Offline, then reload and re-run verification.');
  } catch (e) {
    err('Verification failed:', e && e.message ? e.message : e);
  }
})();

