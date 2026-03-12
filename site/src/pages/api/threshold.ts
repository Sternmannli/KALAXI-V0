/**
 * POST /api/threshold — The Ninth Operator (server-side)
 *
 * Receives a word from the Threshold, runs the dignity predicate,
 * returns a witness mark + global count.
 *
 * Privacy: The word is witnessed and released. Only the count persists.
 * Storage: Cloudflare KV (KALAM_KV namespace).
 *
 * [V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
 */

import type { APIRoute } from 'astro';

// Server-rendered at runtime (not prerendered at build)
export const prerender = false;

const KV_KEY = 'witness-count';

// D = A × L × M — the dignity predicate
function checkDignity(content: string): { D: number; failed: string[] } {
  const failed: string[] = [];
  const A = content.trim().length > 0 ? 1.0 : 0.0;
  if (A === 0) failed.push('agency');
  const L = 1.0; // the donor chose to come here — legibility is given
  const M = 1.0; // sealed gate check is server-side in Phase 3
  return { D: A * L * M, failed };
}

// The witness mark — what witnessing adds to the word
function witnessMark(content: string): string {
  const words = content.trim().split(/\s+/).length;
  if (words <= 3) return 'Witnessed: a seed — small, complete.';
  if (words <= 20) return 'Witnessed: a held shape — clear enough to carry.';
  return 'Witnessed: a landscape — it took room to arrive.';
}

export const POST: APIRoute = async ({ request, locals }) => {
  const headers = {
    'Content-Type': 'application/json',
    'Cache-Control': 'no-store',
  };

  try {
    const body = await request.json();
    const content = typeof body.content === 'string' ? body.content : '';

    // Dignity check
    const dignity = checkDignity(content);
    if (dignity.D === 0) {
      return new Response(JSON.stringify({
        witnessed: false,
        sheltered: true,
        reason: `Dignity failed: ${dignity.failed.join(', ')}`,
        message: 'Your exchange has been held — not rejected, held.',
      }), { status: 200, headers });
    }

    // Witness the word
    const mark = witnessMark(content);

    // Increment global count via KV (the word itself is never stored)
    let count = 0;
    const runtime = (locals as any).runtime;
    if (runtime?.env?.KALAM_KV) {
      const kv = runtime.env.KALAM_KV;
      const current = await kv.get(KV_KEY);
      count = (parseInt(current || '0', 10)) + 1;
      await kv.put(KV_KEY, String(count));
    }

    // The word is witnessed and released. It does not persist.
    return new Response(JSON.stringify({
      witnessed: true,
      mark,
      count,
      receipt: 'It is here. You can come back.',
    }), { status: 200, headers });

  } catch {
    return new Response(JSON.stringify({
      error: 'The threshold could not receive your word.',
    }), { status: 400, headers });
  }
};

// GET /api/threshold — returns the global count only
export const GET: APIRoute = async ({ locals }) => {
  let count = 0;
  const runtime = (locals as any).runtime;
  if (runtime?.env?.KALAM_KV) {
    const kv = runtime.env.KALAM_KV;
    const current = await kv.get(KV_KEY);
    count = parseInt(current || '0', 10);
  }

  return new Response(JSON.stringify({ count }), {
    status: 200,
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': 'public, max-age=60',
    },
  });
};
