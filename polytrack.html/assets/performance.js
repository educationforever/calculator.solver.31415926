// Performance monitoring and analytics
class PerformanceMonitor {
  constructor() {
    this.metrics = {};
    this.init();
  }

  init() {
    // Wait for page load
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.collectMetrics());
    } else {
      this.collectMetrics();
    }

    // Collect metrics after window load
    window.addEventListener('load', () => {
      setTimeout(() => this.collectAdvancedMetrics(), 1000);
    });
  }

  collectMetrics() {
    // Core Web Vitals
    this.measureCLS();
    this.measureFID();
    this.measureLCP();
    
    // Navigation timing
    this.measureNavigationTiming();
    
    // Resource timing
    this.measureResourceTiming();
  }

  collectAdvancedMetrics() {
    // Paint timing
    this.measurePaintTiming();
    
    // Memory usage (if available)
    this.measureMemoryUsage();
    
    // Send metrics to analytics
    this.sendMetrics();
  }

  measureCLS() {
    // Cumulative Layout Shift
    let clsValue = 0;
    let clsEntries = [];

    const observer = new PerformanceObserver((entryList) => {
      for (const entry of entryList.getEntries()) {
        if (!entry.hadRecentInput) {
          clsValue += entry.value;
          clsEntries.push(entry);
        }
      }
      this.metrics.cls = clsValue;
    });

    observer.observe({ type: 'layout-shift', buffered: true });
  }

  measureFID() {
    // First Input Delay
    const observer = new PerformanceObserver((entryList) => {
      for (const entry of entryList.getEntries()) {
        this.metrics.fid = entry.processingStart - entry.startTime;
        break;
      }
    });

    observer.observe({ type: 'first-input', buffered: true });
  }

  measureLCP() {
    // Largest Contentful Paint
    const observer = new PerformanceObserver((entryList) => {
      const entries = entryList.getEntries();
      const lastEntry = entries[entries.length - 1];
      this.metrics.lcp = lastEntry.startTime;
    });

    observer.observe({ type: 'largest-contentful-paint', buffered: true });
  }

  measureNavigationTiming() {
    const navigation = performance.getEntriesByType('navigation')[0];
    if (navigation) {
      this.metrics.navigationTiming = {
        dns: navigation.domainLookupEnd - navigation.domainLookupStart,
        tcp: navigation.connectEnd - navigation.connectStart,
        request: navigation.responseStart - navigation.requestStart,
        response: navigation.responseEnd - navigation.responseStart,
        domProcessing: navigation.domContentLoadedEventStart - navigation.responseEnd,
        domComplete: navigation.domComplete - navigation.domContentLoadedEventStart,
        loadComplete: navigation.loadEventEnd - navigation.loadEventStart,
        ttfb: navigation.responseStart - navigation.requestStart
      };
    }
  }

  measureResourceTiming() {
    const resources = performance.getEntriesByType('resource');
    const resourceMetrics = {
      css: [],
      js: [],
      images: [],
      fonts: []
    };

    resources.forEach(resource => {
      const timing = {
        name: resource.name,
        duration: resource.duration,
        size: resource.transferSize || 0,
        cached: resource.transferSize === 0 && resource.decodedBodySize > 0
      };

      if (resource.name.includes('.css')) {
        resourceMetrics.css.push(timing);
      } else if (resource.name.includes('.js')) {
        resourceMetrics.js.push(timing);
      } else if (resource.name.match(/\.(jpg|jpeg|png|gif|webp|svg)$/i)) {
        resourceMetrics.images.push(timing);
      } else if (resource.name.match(/\.(woff|woff2|ttf|otf)$/i)) {
        resourceMetrics.fonts.push(timing);
      }
    });

    this.metrics.resources = resourceMetrics;
  }

  measurePaintTiming() {
    const paintEntries = performance.getEntriesByType('paint');
    paintEntries.forEach(entry => {
      this.metrics[entry.name.replace('-', '_')] = entry.startTime;
    });
  }

  measureMemoryUsage() {
    if ('memory' in performance) {
      this.metrics.memory = {
        used: performance.memory.usedJSHeapSize,
        total: performance.memory.totalJSHeapSize,
        limit: performance.memory.jsHeapSizeLimit
      };
    }
  }

  sendMetrics() {
    // Send to Google Analytics 4 if available
    if (typeof gtag !== 'undefined') {
      // Core Web Vitals
      if (this.metrics.lcp) {
        gtag('event', 'web_vitals', {
          event_category: 'Performance',
          event_label: 'LCP',
          value: Math.round(this.metrics.lcp)
        });
      }

      if (this.metrics.fid) {
        gtag('event', 'web_vitals', {
          event_category: 'Performance',
          event_label: 'FID',
          value: Math.round(this.metrics.fid)
        });
      }

      if (this.metrics.cls) {
        gtag('event', 'web_vitals', {
          event_category: 'Performance',
          event_label: 'CLS',
          value: Math.round(this.metrics.cls * 1000)
        });
      }

      // Navigation timing
      if (this.metrics.navigationTiming) {
        gtag('event', 'page_timing', {
          event_category: 'Performance',
          event_label: 'TTFB',
          value: Math.round(this.metrics.navigationTiming.ttfb)
        });
      }
    }

    // Console log for development
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
      console.group('🚀 Performance Metrics');
      console.log('Core Web Vitals:', {
        LCP: this.metrics.lcp ? `${Math.round(this.metrics.lcp)}ms` : 'N/A',
        FID: this.metrics.fid ? `${Math.round(this.metrics.fid)}ms` : 'N/A',
        CLS: this.metrics.cls ? Math.round(this.metrics.cls * 1000) / 1000 : 'N/A'
      });
      console.log('Navigation Timing:', this.metrics.navigationTiming);
      console.log('Paint Timing:', {
        FCP: this.metrics.first_contentful_paint ? `${Math.round(this.metrics.first_contentful_paint)}ms` : 'N/A',
        FP: this.metrics.first_paint ? `${Math.round(this.metrics.first_paint)}ms` : 'N/A'
      });
      if (this.metrics.memory) {
        console.log('Memory Usage:', {
          used: `${Math.round(this.metrics.memory.used / 1024 / 1024)}MB`,
          total: `${Math.round(this.metrics.memory.total / 1024 / 1024)}MB`
        });
      }
      console.groupEnd();
    }
  }

  // Public method to get current metrics
  getMetrics() {
    return this.metrics;
  }
}

// Initialize performance monitoring
const performanceMonitor = new PerformanceMonitor();

// Game interaction tracking
function trackGameInteraction(action) {
  if (typeof gtag !== 'undefined') {
    gtag('event', 'game_interaction', {
      event_category: 'Game',
      event_label: action,
      value: 1
    });
  }
}

// Fullscreen tracking
function trackFullscreen(isEntering) {
  if (typeof gtag !== 'undefined') {
    gtag('event', 'fullscreen_toggle', {
      event_category: 'Game',
      event_label: isEntering ? 'enter' : 'exit',
      value: 1
    });
  }
}

// Export for use in other scripts
window.performanceMonitor = performanceMonitor;
window.trackGameInteraction = trackGameInteraction;
window.trackFullscreen = trackFullscreen;