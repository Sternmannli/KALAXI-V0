#!/usr/bin/env python3
"""Analyze the voice of V-001 — linguistic, cognitive, structural patterns."""
import json
import re
import math
from collections import Counter, defaultdict
from datetime import datetime

# ── Load ──
with open("KEEP/INPUT_LEDGER/index.json", "r", encoding="utf-8") as f:
    data = json.load(f)

entries = [e for e in data["entries"] if e.get("voice") == "V-001"]
entries.sort(key=lambda e: e.get("timestamp", ""))
print(f"Loaded {len(entries)} V-001 entries.")

# ── Stop words (English + common filler) ──
STOP = set("i me my myself we our ours ourselves you your yours yourself he him his she her "
    "it its they them their what which who whom this that these those am is are was were be "
    "been being have has had having do does did doing a an the and but if or because as until "
    "while of at by for with about against between through during before after above below to "
    "from up down in out on off over under again further then once here there when where why "
    "how all both each few more most other some such no nor not only own same so than too very "
    "s t can will just don should now d ll m o re ve y ain aren couldn didn doesn hadn hasn "
    "haven isn ma mightn mustn needn shan shouldn wasn weren won wouldn also would could "
    "like going want know think make get go need something really going gonna let us ok okay "
    "yes yeah please thank thanks well right thing things way much many still even got one two".split())

STOP_DE = set("ich du er sie es wir ihr sie der die das ein eine einer eines dem den des "
    "und oder aber wenn als auch noch nicht kein keine ist sind war hat haben wird werden "
    "kann muss soll darf im in auf an aus bei mit von zu um für über nach durch".split())

# ── Helpers ──
def tokenize(text):
    return re.findall(r"[a-zA-ZäöüÄÖÜßàáâãéèêëîïôùûü']+", text.lower())

def sentences(text):
    return [s.strip() for s in re.split(r'[.!?]+', text) if s.strip() and len(s.strip()) > 3]

def detect_lang(text):
    de_markers = set("ich du nicht ein eine der die das und oder wenn auch noch ist sind hat haben".split())
    ar_pattern = re.compile(r'[\u0600-\u06FF]')
    tokens = set(tokenize(text))
    has_arabic = bool(ar_pattern.search(text))
    de_count = len(tokens & de_markers)
    if has_arabic and de_count < 2:
        return "arabic"
    elif de_count >= 3:
        return "german"
    else:
        return "english"

# ── Analysis containers ──
all_words = []
all_words_no_stop = []
all_sentences = []
lengths = []           # input lengths in chars
word_counts = []       # words per input
sentence_counts = []   # sentences per input
lang_dist = Counter()
hour_dist = Counter()
day_dist = Counter()
week_dist = Counter()
tag_dist = Counter()
context_dist = Counter()

# Input types
imperatives = 0        # "I want", "you must", "do this", "never"
questions = 0
reflections = 0        # past tense, "I remember", "when I"

# Metaphor tracking
metaphor_words = set("river stone knot rope wound ash water bone hand breath door "
    "root seed garden fire light dark bridge wall gate thread web silk "
    "ocean mountain cocoon wolf dolphin tiger gold honey".split())
metaphor_count = Counter()

# Recurring phrases (bigrams and trigrams)
bigrams = Counter()
trigrams = Counter()

# Emotional markers
intensity_words = set("must never always every single important fundamental "
    "permanent unconditional absolute sacred constitutional forever "
    "immediately critical essential vital".split())
intensity_count = 0

# References
child_refs = 0
system_refs = 0
wound_refs = 0
future_refs = 0
past_refs = 0

# ── Process each entry ──
for e in entries:
    raw = e.get("raw_text", "")
    if not raw.strip():
        continue

    ts = e.get("timestamp", "")
    ctx = e.get("context", "")
    tags = e.get("tags", [])

    # Basic metrics
    lengths.append(len(raw))
    words = tokenize(raw)
    word_counts.append(len(words))
    sents = sentences(raw)
    sentence_counts.append(len(sents))
    all_sentences.extend(sents)

    # Words
    all_words.extend(words)
    filtered = [w for w in words if w not in STOP and w not in STOP_DE and len(w) > 1]
    all_words_no_stop.extend(filtered)

    # Language
    lang_dist[detect_lang(raw)] += 1

    # Time patterns
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        hour_dist[dt.hour] += 1
        day_dist[dt.strftime("%A")] += 1
        week_key = dt.strftime("%Y-W%W")
        week_dist[week_key] += 1
    except:
        pass

    # Tags and context
    for t in tags:
        tag_dist[t] += 1
    if ctx and isinstance(ctx, str):
        context_dist[ctx] += 1

    # Input type detection
    lower = raw.lower()
    if "?" in raw:
        questions += 1
    if any(p in lower for p in ["i want", "you must", "never ", "always ", "do not", "don't", "stop ", "must be"]):
        imperatives += 1
    if any(p in lower for p in ["i remember", "when i was", "back then", "i used to", "that was"]):
        reflections += 1

    # Metaphors
    for w in words:
        if w in metaphor_words:
            metaphor_count[w] += 1

    # Bigrams and trigrams
    for i in range(len(filtered) - 1):
        bigrams[f"{filtered[i]} {filtered[i+1]}"] += 1
    for i in range(len(filtered) - 2):
        trigrams[f"{filtered[i]} {filtered[i+1]} {filtered[i+2]}"] += 1

    # Intensity
    for w in words:
        if w in intensity_words:
            intensity_count += 1

    # References
    if any(w in lower for w in ["laila", "yara", "salim", "children", "kids", "daughter", "son", "father"]):
        child_refs += 1
    if any(w in lower for w in ["system", "organism", "weaver", "ledger", "module"]):
        system_refs += 1
    if any(w in lower for w in ["wound", "separated", "custody", "pain", "loss"]):
        wound_refs += 1
    if any(w in lower for w in ["will be", "future", "vision", "imagine", "one day", "going to"]):
        future_refs += 1
    if any(w in lower for w in ["was ", "were ", "remember", "back ", "history", "before"]):
        past_refs += 1

# ── Compute derived metrics ──
total_words = len(all_words)
unique_words = len(set(all_words))
vocab_richness = unique_words / total_words if total_words > 0 else 0
hapax = sum(1 for w, c in Counter(all_words).items() if c == 1)  # words used only once
hapax_ratio = hapax / unique_words if unique_words > 0 else 0

avg_input_len = sum(lengths) / len(lengths) if lengths else 0
avg_words = sum(word_counts) / len(word_counts) if word_counts else 0
avg_sents = sum(sentence_counts) / len(sentence_counts) if sentence_counts else 0

# Sentence length distribution
sent_lengths = [len(tokenize(s)) for s in all_sentences]
avg_sent_len = sum(sent_lengths) / len(sent_lengths) if sent_lengths else 0
short_sents = sum(1 for l in sent_lengths if l <= 8)
med_sents = sum(1 for l in sent_lengths if 9 <= l <= 20)
long_sents = sum(1 for l in sent_lengths if l > 20)

# ── Write analysis ──
out = "VOICE/V001/analysis.md"
with open(out, "w", encoding="utf-8") as f:
    f.write("# Analysis of V-001 Voice\n")
    f.write(f"> Based on {len(entries)} inputs from the Input Ledger.\n")
    f.write(f"> Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}\n")
    f.write("> Method: Pure frequency analysis. No interpretation. No judgment.\n\n---\n\n")

    # ── 1. SCALE ──
    f.write("## 1. Scale\n\n")
    f.write(f"- **Total inputs:** {len(entries)}\n")
    f.write(f"- **Total words spoken:** {total_words:,}\n")
    f.write(f"- **Unique words used:** {unique_words:,}\n")
    f.write(f"- **Total sentences:** {len(all_sentences):,}\n")
    f.write(f"- **Date range:** {entries[0].get('timestamp', '?')[:10]} to {entries[-1].get('timestamp', '?')[:10]}\n\n")

    # ── 2. VOCABULARY ──
    f.write("## 2. Vocabulary\n\n")
    f.write(f"- **Vocabulary richness (unique/total):** {vocab_richness:.4f} ({vocab_richness*100:.1f}%)\n")
    f.write(f"- **Hapax legomena (words used exactly once):** {hapax:,} ({hapax_ratio*100:.1f}% of vocabulary)\n")
    f.write(f"- **Average input length:** {avg_input_len:.0f} characters, {avg_words:.1f} words, {avg_sents:.1f} sentences\n\n")

    f.write("### Most frequent words (after removing stop words)\n\n")
    for w, c in Counter(all_words_no_stop).most_common(50):
        f.write(f"- **{w}** — {c} times\n")
    f.write("\n")

    # ── 3. SENTENCE STRUCTURE ──
    f.write("## 3. Sentence Structure\n\n")
    f.write(f"- **Average sentence length:** {avg_sent_len:.1f} words\n")
    f.write(f"- **Short sentences (≤8 words):** {short_sents} ({short_sents/len(all_sentences)*100:.1f}%)\n")
    f.write(f"- **Medium sentences (9-20 words):** {med_sents} ({med_sents/len(all_sentences)*100:.1f}%)\n")
    f.write(f"- **Long sentences (>20 words):** {long_sents} ({long_sents/len(all_sentences)*100:.1f}%)\n\n")

    # ── 4. LANGUAGE DISTRIBUTION ──
    f.write("## 4. Language Distribution\n\n")
    for lang, c in lang_dist.most_common():
        f.write(f"- **{lang.title()}:** {c} inputs ({c/len(entries)*100:.1f}%)\n")
    f.write("\n")

    # ── 5. INPUT TYPE ──
    f.write("## 5. Input Type\n\n")
    f.write(f"- **Imperative/directive inputs:** {imperatives} ({imperatives/len(entries)*100:.1f}%)\n")
    f.write(f"- **Questions:** {questions} ({questions/len(entries)*100:.1f}%)\n")
    f.write(f"- **Reflective/past-looking:** {reflections} ({reflections/len(entries)*100:.1f}%)\n\n")

    # ── 6. TEMPORAL PATTERNS ──
    f.write("## 6. Temporal Patterns\n\n")
    f.write("### By hour (UTC)\n\n")
    for h in range(24):
        c = hour_dist.get(h, 0)
        bar = "█" * (c // 5) if c > 0 else ""
        if c > 0:
            f.write(f"- **{h:02d}:00** — {c} inputs {bar}\n")
    f.write("\n")

    f.write("### By day of week\n\n")
    for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
        c = day_dist.get(day, 0)
        if c > 0:
            f.write(f"- **{day}:** {c} inputs\n")
    f.write("\n")

    f.write("### By week\n\n")
    for week, c in sorted(week_dist.items()):
        bar = "█" * (c // 10)
        f.write(f"- **{week}:** {c} inputs {bar}\n")
    f.write("\n")

    # ── 7. THEMATIC GRAVITY ──
    f.write("## 7. Thematic Gravity (what pulls your words)\n\n")
    f.write(f"- **System/architecture references:** {system_refs} inputs ({system_refs/len(entries)*100:.1f}%)\n")
    f.write(f"- **Future/vision references:** {future_refs} inputs ({future_refs/len(entries)*100:.1f}%)\n")
    f.write(f"- **Past/memory references:** {past_refs} inputs ({past_refs/len(entries)*100:.1f}%)\n")
    f.write(f"- **Children (Laila/Yara/Salim):** {child_refs} inputs ({child_refs/len(entries)*100:.1f}%)\n")
    f.write(f"- **Wound/separation:** {wound_refs} inputs ({wound_refs/len(entries)*100:.1f}%)\n\n")

    # ── 8. INTENSITY ──
    f.write("## 8. Intensity\n\n")
    f.write(f"- **Intensity words (must, never, always, every, sacred, permanent, forever...):** {intensity_count} total uses\n")
    f.write(f"- **Intensity per input:** {intensity_count/len(entries):.2f} intensity words per input\n\n")

    # ── 9. METAPHOR FIELD ──
    f.write("## 9. Metaphor Field\n\n")
    f.write("Physical/natural words that carry metaphoric weight:\n\n")
    for w, c in metaphor_count.most_common(20):
        f.write(f"- **{w}** — {c} uses\n")
    f.write("\n")

    # ── 10. RECURRING PHRASES ──
    f.write("## 10. Recurring Phrases\n\n")
    f.write("### Two-word combinations (≥5 occurrences)\n\n")
    for phrase, c in bigrams.most_common(40):
        if c >= 5:
            f.write(f"- **\"{phrase}\"** — {c} times\n")
    f.write("\n")

    f.write("### Three-word combinations (≥3 occurrences)\n\n")
    for phrase, c in trigrams.most_common(30):
        if c >= 3:
            f.write(f"- **\"{phrase}\"** — {c} times\n")
    f.write("\n")

    # ── 11. CONTEXT ──
    f.write("## 11. Context Distribution\n\n")
    for ctx, c in context_dist.most_common(15):
        f.write(f"- **{ctx}:** {c} inputs\n")
    f.write("\n")

    # ── 12. TAG CLOUD ──
    f.write("## 12. Tag Cloud (top 40)\n\n")
    for t, c in tag_dist.most_common(40):
        f.write(f"- **{t}** — {c}\n")
    f.write("\n")

    # ── 13. LONGEST AND SHORTEST ──
    sorted_by_len = sorted([(e.get("entry_id", "?"), len(e.get("raw_text", "")), e.get("raw_text", "")[:150]) for e in entries if e.get("raw_text", "").strip()], key=lambda x: x[1], reverse=True)
    f.write("## 13. Extremes\n\n")
    f.write("### 5 longest inputs\n\n")
    for eid, length, preview in sorted_by_len[:5]:
        f.write(f"- **{eid}** — {length:,} chars: *{preview.replace(chr(10), ' ')}...*\n")
    f.write("\n### 5 shortest inputs\n\n")
    for eid, length, preview in sorted_by_len[-5:]:
        f.write(f"- **{eid}** — {length} chars: *{preview.replace(chr(10), ' ')}*\n")
    f.write("\n")

    # ── 14. EVOLUTION ──
    f.write("## 14. Evolution Over Time\n\n")
    # Split entries into thirds
    third = len(entries) // 3
    phases = [
        ("First third (earliest)", entries[:third]),
        ("Second third (middle)", entries[third:2*third]),
        ("Third third (most recent)", entries[2*third:])
    ]
    for label, phase_entries in phases:
        phase_words = []
        phase_lengths = []
        phase_imperatives = 0
        for e in phase_entries:
            raw = e.get("raw_text", "")
            words = tokenize(raw)
            phase_words.extend(words)
            phase_lengths.append(len(raw))
            lower = raw.lower()
            if any(p in lower for p in ["i want", "you must", "never ", "always ", "must be"]):
                phase_imperatives += 1

        phase_filtered = [w for w in phase_words if w not in STOP and w not in STOP_DE and len(w) > 1]
        top5 = [w for w, _ in Counter(phase_filtered).most_common(10)]
        avg_len = sum(phase_lengths) / len(phase_lengths) if phase_lengths else 0

        f.write(f"### {label} ({len(phase_entries)} inputs)\n")
        f.write(f"- Average length: {avg_len:.0f} chars\n")
        f.write(f"- Directive density: {phase_imperatives/len(phase_entries)*100:.1f}%\n")
        f.write(f"- Top words: {', '.join(top5)}\n\n")

    f.write("---\n\n")
    f.write("*This analysis reads the data. It does not interpret the person. The numbers are facts. What they mean is yours to decide.*\n")

print(f"Written: {out}")
