export default { onRequest: async ({ request }) => {
  const url = new URL(request.url);
  // CF → Fly.io HTTP works (Fly accepts HTTP). HTTPS fails due to Fly.io
  // incomplete cert chain (SEC_E_INVALID_TOKEN). Use HTTP proxy.
  const target = `http://ccec-api.fly.dev${url.pathname}${url.search}`;
  const opts = { method: request.method, headers: {} };
  for (const [k, v] of request.headers.entries()) {
    // Normalize CF-Forwarded-* headers for Fly.io
    if (!['host','connection'].includes(k.toLowerCase())) opts.headers[k] = v;
  }
  if (!['GET', 'HEAD'].includes(request.method)) {
    try { opts.body = await request.text(); } catch {}
  }
  let res;
  try {
    res = await fetch(target, opts);
  } catch (e) {
    return new Response(JSON.stringify({ error: 'upstream_unavailable', detail: e.message }), {
      status: 502,
      headers: { 'Content-Type': 'application/json' },
    });
  }
  return new Response(await res.text(), {
    status: res.status,
    headers: {
      'Content-Type': res.headers.get('content-type') || 'application/json',
      'Access-Control-Allow-Origin': '*',
      'Cache-Control': 'no-store',
    },
  });
}}
