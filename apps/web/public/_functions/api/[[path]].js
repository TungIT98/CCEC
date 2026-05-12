// Cloudflare Pages Function: HTTPS proxy → Fly.io API (HTTP)
// Intercepts /api/* paths and forwards to Fly.io

export async function onRequest(context) {
  const url = new URL(context.request.url);

  // Only handle /api/* paths
  if (!url.pathname.startsWith('/api/')) {
    return new Response(JSON.stringify({ error: 'Not Found', path: url.pathname }), {
      status: 404,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  // Forward the full path including /api prefix to Fly.io
  const targetUrl = `http://ccec-api.fly.dev${url.pathname}${url.search}`;
  const method = context.request.method;

  // Build headers object
  const headers = {};
  try {
    for (const [k, v] of context.request.headers.entries()) {
      headers[k] = v;
    }
  } catch (e) {
    // Ignore header iteration errors
  }

  // Only include body for non-GET/HEAD requests
  let fetchOptions = { method, headers };
  if (!['GET', 'HEAD'].includes(method)) {
    try {
      fetchOptions.body = await context.request.text();
    } catch (e) {
      fetchOptions.body = null;
    }
  }

  try {
    const response = await fetch(targetUrl, fetchOptions);
    const text = await response.text();

    return new Response(text, {
      status: response.status,
      headers: {
        'Content-Type': response.headers.get('content-type') || 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
    });
  } catch (err) {
    return new Response(JSON.stringify({ error: 'Proxy failed', message: err.message }), {
      status: 502,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}