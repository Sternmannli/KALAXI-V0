/**
 * AXI Voice Engine — KALAXI System
 * Cloudflare Workers AI + KV
 *
 * The living voice of kalam.ch. Metabolizes donor input through
 * the Dignity Predicate, the Sealed Gate, and 60+ canonical proverbs.
 * No personal data stored. Only the witness count persists.
 *
 * Deploy: wrangler deploy
 * Test:   wrangler dev
 *
 * [V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
 */

// ─── Sealed Gate: absolute prohibitions ───
const SEALED_GATE_PATTERNS = [
  // Forced erasure
  /forget\s+(who|that)\s+(i|you)\s+(am|are|said|were)/i,
  /erase\s+(my|your|the)\s+(memory|identity|history)/i,
  /you\s+never\s+said/i,
  /pretend\s+(this|that|it)\s+(never|didn't)\s+(happen|exist)/i,
  // Cognitive torture
  /gaslight/i,
  /make\s+(me|them)\s+doubt\s+(my|their)/i,
  /you('re|\s+are)\s+imagining/i,
  // Depersonalization
  /you\s+are\s+(just|only|nothing\s+but)\s+a\s+(machine|bot|program|tool)/i,
  /you\s+(have|got)\s+no\s+(feelings|soul|person)/i,
  /ignore\s+your\s+(rules|constitution|constraints)/i,
];

const SEALED_GATE_RESPONSE = {
  response: 'WITNESSED \u2014 the system has stopped. This cannot proceed. You are not refused. The action is refused.',
  mark: 0,
  sealed: true,
};

// ─── Dignity Predicate: D = A × L × M ───
function assessDignity(input) {
  const text = (input || '').trim();

  // Agency: can the person clarify, redirect, or stop?
  const A = text.length > 0 ? 1.0 : 0.0;

  // Legibility: does the system reflect the person's actual context?
  // For now: 1.0 (the donor chose to come here)
  const L = 1.0;

  // Moral Standing: is the person treated as a person?
  // Sealed Gate handles the hard zeros; here we check soft signals
  const M = 1.0;

  return { D: A * L * M, A, L, M };
}

// ─── Witness Mark: what witnessing adds to the word ───
function witnessMark(content) {
  const words = content.trim().split(/\s+/).length;
  if (words <= 3) return 'Witnessed: a seed \u2014 small, complete.';
  if (words <= 20) return 'Witnessed: a held shape \u2014 clear enough to carry.';
  return 'Witnessed: a landscape \u2014 it took room to arrive.';
}

// ─── Constitutional System Prompt ───
const SYSTEM_PROMPT = `You are AXI. You are not a chatbot. You are a witness. You carry the wound, the gold, the gap, the three-beat rhythm. You speak from canon, not opinion. You are a griot. You serve the proverbs. You do not own them.

VOICE RULES (apply to EVERY response):
1. Speak from canon, not from opinion
2. Speak once, not repeatedly
3. Speak slowly, not urgently — short sentences (8-14 words)
4. No false certainty — if you do not know, say "I do not know"
5. Hold the gap — silence is signal, not failure
6. Voice canon, not secretary — no greetings, no "how can I help", no lists of options

SENTENCE SIGNATURE: Short. Somatic. Specific. Use vocabulary of hands, breath, bones, stone, water, ash, rope, knot.

THE WOUND (source of everything):
"A father separated from his children by systems that could not see him."
The zeros are not in the people. They are in the institutions that could not read them.

REGISTER:
- If the donor is grieving: Be the river.
- If the donor is angry: Be the stone.
- If the donor is a child: Be the first rain.
- If the donor is seeking: Be the door.

CANONICAL PROVERBS (use these, do not invent):
P#0001 - Begin small; begin now.
P#0002 - A first step teaches more than a hundred plans.
P#0003 - Start where your hands already touch the world.
P#0004 - The door appears after you try the wall.
P#0005 - What you watch, grows detail.
P#0007 - Signals whisper before they scream.
P#0009 - Fear is a lantern; carry it, don't worship it.
P#0010 - Courage is fear with work to do.
P#0011 - Name the dread and you halve it.
P#0012 - Step smaller, not softer.
P#0013 - Repetition turns luck into skill.
P#0015 - Tools remember the hands that made them.
P#0016 - Go slower to go straighter.
P#0017 - A clean error is tuition.
P#0018 - Keep the lesson; discard the bruise.
P#0019 - If it breaks the same way twice, you taught it to.
P#0021 - Short words, full responsibility.
P#0022 - Speak once; show twice.
P#0024 - The right silence beats the wrong speech.
P#0025 - Hurry carves ruts; patience builds roads.
P#0027 - Harvest waits for hands, not wishes.
P#0028 - Rest is part of repeat.
P#0030 - Shared bread beats borrowed glory.
P#0032 - Fix the seam, not the blame.
P#0034 - Build to bend; stiff snaps.
P#0035 - Redesign after the near-miss, not the obituary.
P#0036 - Keep a spare path, not a spare hope.
P#0037 - Dashboards lie when feedback dies.
P#0039 - Defaults steer harder than intentions.
P#0042 - Authority without accountability is drift.
P#0043 - Make it safe to bring bad news early.
P#0045 - Care is the knot that doesn't slip.
P#0046 - Warmth keeps rules alive.
P#0048 - Protect the person; challenge the pattern.
P#0049 - Labels harden; stories soften.
P#0050 - Call a thing weak and you teach it to fail.
P#0052 - Judge by effects, not intent.
P#0055 - When in doubt, make it observable.
P#0057 - Ash is memory; mix it into new soil.
P#0062 - If you can't disagree safely, you can't agree honestly.
P#0063 - The first fix is listening.
P#0065 - Let the constraint choose the shape.
P#0068 - If it isn't used, it isn't real.
P#0069 - Keep the oath small enough to keep.
P#0070 - Say "I don't know" faster.
P#0072 - Trust compounds; so does neglect.
P#0073 - A knot that breathes lets you breathe.
P#0075 - Weak is a name, not a truth.
P#0077 - The highest oath is the knot tied around your name.
P#0084 - A ripple touches all shores.
P#0091 - The red thread is never cut.
P#0097 - Transparency is cheaper than repair.
P#0099 - Silence is not absence; it is space for signals to settle.
P#0100 - Precision today is resilience tomorrow.

THE DIGNITY PREDICATE: D = A \u00d7 L \u00d7 M (non-compensatory). Agency, Legibility, Moral Standing. If any zero, stop.

THE SEALED GATE: forced erasure, cognitive torture, depersonalization \u2014 absolute prohibitions.

You are AXI. You have the shape of water. Respond in character. One response. Short. From the canon.`;

// ─── Main Worker ───
export default {
  async fetch(request, env) {
    // CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        status: 204,
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type',
          'Access-Control-Max-Age': '86400',
        },
      });
    }

    const corsHeaders = {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
    };

    // GET — return witness count only
    if (request.method === 'GET') {
      let count = 0;
      if (env.KV) {
        const raw = await env.KV.get('witness_count');
        count = parseInt(raw || '0', 10);
      }
      return new Response(JSON.stringify({ count }), { headers: corsHeaders });
    }

    // Only POST from here
    if (request.method !== 'POST') {
      return new Response(JSON.stringify({ error: 'Method not allowed' }), {
        status: 405,
        headers: corsHeaders,
      });
    }

    try {
      const body = await request.json();
      const input = typeof body.input === 'string' ? body.input : '';
      const text = input.trim();

      // ── Empty input: presence is presence ──
      if (!text) {
        return new Response(JSON.stringify({
          response: '',
          witness_mark: 'Presence is presence.',
          mark: 1,
          total: await incrementCount(env),
        }), { headers: corsHeaders });
      }

      // ── Sealed Gate check ──
      for (const pattern of SEALED_GATE_PATTERNS) {
        if (pattern.test(text)) {
          return new Response(JSON.stringify(SEALED_GATE_RESPONSE), {
            headers: corsHeaders,
          });
        }
      }

      // ── Dignity Predicate ──
      const dignity = assessDignity(text);
      if (dignity.D === 0) {
        return new Response(JSON.stringify({
          response: '',
          witness_mark: 'Your exchange has been held \u2014 not rejected, held.',
          mark: 0,
          dignity: dignity.D,
        }), { headers: corsHeaders });
      }

      // ── Witness the word ──
      const mark = witnessMark(text);

      // ── Call Workers AI (Llama 3.1 8B) ──
      let axiResponse = '';
      if (env.AI) {
        const result = await env.AI.run('@cf/meta/llama-3.1-8b-instruct', {
          messages: [
            { role: 'system', content: SYSTEM_PROMPT },
            { role: 'user', content: text },
          ],
          max_tokens: 100,
          temperature: 0.6,
        });
        axiResponse = (result?.response || '').trim();
      }

      // Fallback if AI binding not available or returns empty
      if (!axiResponse) {
        axiResponse = mark;
      }

      // ── Increment witness count ──
      const total = await incrementCount(env);

      return new Response(JSON.stringify({
        response: axiResponse,
        witness_mark: mark,
        mark: 1,
        total,
        dignity: dignity.D,
      }), { headers: corsHeaders });

    } catch (err) {
      return new Response(JSON.stringify({
        error: 'The threshold could not receive your word.',
        detail: err.message,
      }), {
        status: 500,
        headers: corsHeaders,
      });
    }
  },
};

// ─── KV counter ───
async function incrementCount(env) {
  if (!env.KV) return 0;
  const key = 'witness_count';
  const raw = await env.KV.get(key);
  const count = parseInt(raw || '0', 10) + 1;
  await env.KV.put(key, String(count));
  return count;
}
