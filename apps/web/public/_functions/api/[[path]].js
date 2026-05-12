// Cloudflare Pages Function: HTTPS proxy → Fly.io API (HTTP)
// Intercepts /api/* paths and forwards to Fly.io
// NOTE: If this file is not being called, Cloudflare Pages is serving
// index.html for these paths instead. The dist/functions/ directory must
// be deployed (not dist/_functions/).

export async function onRequest(context) {
  const url = new URL(context.request.url);
  const method = context.request.method;

  // Only handle /api/* paths
  if (!url.pathname.startsWith('/api/')) {
    // Return a clear "function matched but path is wrong" response
    return new Response(JSON.stringify({ error: 'Not Found', path: url.pathname }), {
      status: 404,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  // Forward the full path including /api prefix to Fly.io
  // Fly.io FastAPI uses /api/v1/* routes internally
  const targetUrl = `http://ccec-api.fly.dev${url.pathname}${url.search}`;

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