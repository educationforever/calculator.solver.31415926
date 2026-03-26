// Initialize Web Vitals reporting (requires /assets/web-vitals.iife.js)
(function () {
  function sendToGA(metric) {
    if (typeof window.gtag === 'function') {
      var name = metric.name || metric.id || 'metric';
      var value = metric.value || 0;
      window.gtag('event', 'web_vitals', {
        event_category: 'Performance',
        event_label: name,
        value: Math.round(name === 'CLS' ? value * 1000 : value)
      });
    }
  }

  function init() {
    if (!window.webVitals) return;
    try {
      window.webVitals.getCLS(sendToGA);
      window.webVitals.getFID(sendToGA);
      window.webVitals.getLCP(sendToGA);
      // Optional: FCP/TTFB
      if (window.webVitals.getFCP) window.webVitals.getFCP(sendToGA);
      if (window.webVitals.getTTFB) window.webVitals.getTTFB(sendToGA);
    } catch (e) {
      console.warn('[perf-init] web-vitals failed:', e && e.message ? e.message : e);
    }
  }

  if (document.readyState === 'complete' || document.readyState === 'interactive') {
    setTimeout(init, 0);
  } else {
    document.addEventListener('DOMContentLoaded', init);
  }
})();

