// Cloudflare Pages Function: HTTPS proxy → Fly.io API (HTTP)
// Intercepts /api/* paths and forwards to Fly.io, stripping the /api prefix
// NOTE: If this file is not being called, Cloudflare Pages is serving
// index.html for these paths instead. The dist/functions/ directory must
// be deployed (not dist/_functions/).

export async function onRequest(context) {
  const url = new URL(context.request.url);

  // Only handle /api/* paths — return 404 for other routes
  // so Cloudflare serves static files (Astro index.html fallback)
  if (!url.pathname.startsWith('/api/')) {
    return new Response('Not Found', { status: 404 });
  }

  // Strip the /api prefix — Fly.io API uses /api/v1/* internally
  // /api/v1/health → /v1/health
  const pathWithoutApi = url.pathname.slice(4); // remove '/api'
  const targetUrl = `http://ccec-api.fly.dev${pathWithoutApi}${url.search}`;
  const method = context.request.method;

  // Filter Cloudflare-specific and hop-by-hop headers
  const skipHeaders = ['host', 'connection', 'cf-connecting-ip', 'cf-ray',
                       'cf-request-id', 'x-b3-traceid', 'b3'];
  const headers = {};
  for (const [k, v] of context.request.headers.entries()) {
    if (!skipHeaders.includes(k.toLowerCase())) {
      headers[k] = v;
    }
  }

  let body = null;
  if (!['GET', 'HEAD'].includes(method)) {
    body = context.request.body;
  }

  const response = await fetch(targetUrl, { method, headers, body });

  // Forward safe response headers
  const skipResHeaders = ['content-encoding', 'transfer-encoding',
                          'connection', 'cf-ray', 'x-b3-traceid'];
  const newHeaders = {};
  for (const [k, v] of response.headers.entries()) {
    if (!skipResHeaders.includes(k.toLowerCase())) {
      newHeaders[k] = v;
    }
  }

  // Read body
  const responseBody = await response.arrayBuffer();

  return new Response(responseBody, {
    status: response.status,
    headers: newHeaders,
  });
}