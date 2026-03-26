// Unified Cookie Consent initialization
(function () {
  var CONFIG = {
    gaMeasurementId: '',
    adsClientId: ''
  };

  function loadAnalytics() {
    if (CONFIG.gaMeasurementId) {
      var ga = document.createElement('script');
      ga.async = true;
      ga.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(CONFIG.gaMeasurementId);
      document.head.appendChild(ga);
      var gtagInit = document.createElement('script');
      gtagInit.innerHTML = "window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js', new Date());gtag('config','" + CONFIG.gaMeasurementId + "');";
      document.head.appendChild(gtagInit);
    }

    if (CONFIG.adsClientId) {
      var ads = document.createElement('script');
      ads.async = true;
      ads.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=' + encodeURIComponent(CONFIG.adsClientId);
      ads.setAttribute('crossorigin', 'anonymous');
      document.head.appendChild(ads);
    }

    if (!CONFIG.gaMeasurementId && !CONFIG.adsClientId) {
      console.info('[consent-init] No analytics IDs configured; skipping loaders.');
    }
  }

  function runConsent() {
    if (!window.CookieConsent) return;
    try {
      window.CookieConsent.run({
        categories: { necessary: true, analytics: false },
        language: {
          en: {
            consentModal: {
              title: 'We use cookies',
              acceptAllBtn: 'Accept all',
              acceptNecessaryBtn: 'Reject all'
            },
            preferencesModal: {
              title: 'Cookie settings',
              acceptAllBtn: 'Accept all',
              savePreferencesBtn: 'Save settings'
            }
          }
        },
        onAccept: function (ctx) {
          var cats = ctx && (ctx.categories || ctx.accepted || ctx.preferences) || [];
          if (Array.isArray(cats) ? cats.includes('analytics') : cats.analytics) {
            loadAnalytics();
          }
        }
      });
    } catch (e) {
      console.warn('[consent-init] failed:', e && e.message ? e.message : e);
    }
  }

  if (document.readyState === 'complete' || document.readyState === 'interactive') {
    setTimeout(runConsent, 0);
  } else {
    document.addEventListener('DOMContentLoaded', runConsent);
  }
})();
