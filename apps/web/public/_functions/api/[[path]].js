export async function onRequest({ request }) {
  const url = new URL(request.url);
  if (!url.pathname.startsWith('/api/')) {
    return new Response('Not Found', { status: 404 });
  }
  const target = `http://ccec-api.fly.dev${url.pathname}${url.search}`;
  let opts = { method: request.method, headers: {} };
  for (const [k, v] of request.headers.entries()) opts.headers[k] = v;
  if (!['GET', 'HEAD'].includes(request.method)) {
    try { opts.body = await request.text(); } catch {}
  }
  const res = await fetch(target, opts);
  return new Response(await res.text(), {
    status: res.status,
    headers: {
      'Content-Type': res.headers.get('content-type') || 'application/json',
      'Access-Control-Allow-Origin': '*',
    },
  });
}
