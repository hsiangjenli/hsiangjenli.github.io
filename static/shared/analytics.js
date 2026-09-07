(() => {
  const body = document.body;
  const measurementId = body.dataset.analyticsId;
  if (!measurementId || body.dataset.development === 'true' || window.__ga4Loaded) return;
  window.__ga4Loaded = true;
  const script = document.createElement('script');
  script.async = true;
  script.src = `https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(measurementId)}`;
  document.head.append(script);
  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function gtag() { window.dataLayer.push(arguments); };
  window.gtag('js', new Date());
  window.gtag('config', measurementId);
})();
