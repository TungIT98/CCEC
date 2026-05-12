// Cloudflare Pages Function: HTTPS proxy → Fly.io API (HTTP)
// Catches ALL /api/* requests at the edge and forwards to Fly.io

export async function onRequest(context) {
  const url = new URL(context.request.url);

  if (!url.pathname.startsWith('/api/')) {
    return new Response('Not Found', { status: 404 });
  }

  const targetUrl = `http://ccec-api.fly.dev${url.pathname}${url.search}`;
  const method = context.request.method;

  const headers = {};
  for (const [k, v] of context.request.headers.entries()) {
    headers[k] = v;
  }

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
