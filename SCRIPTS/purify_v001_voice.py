#!/usr/bin/env python3
"""Purify V-001 voice: remove duplicates, test inputs, repeating noise.
Keep only real, unique human inputs. Re-generate all VOICE/V001/ files."""
import json
import re
import os
import math
from collections import Counter, defaultdict
from datetime import datetime

# ── Load ──
with open("KEEP/INPUT_LEDGER/index.json", "r", encoding="utf-8") as f:
    data = json.load(f)

entries = [e for e in data["entries"] if e.get("voice") == "V-001"]
entries.sort(key=lambda e: e.get("timestamp", ""))
print(f"Raw V-001 entries: {len(entries)}")

# ── Step 1: Deduplicate — keep first occurrence only ──
seen_texts = set()
deduped = []
for e in entries:
    text = e.get("raw_text", "").strip()
    if text and text not in seen_texts:
        seen_texts.add(text)
        deduped.append(e)

print(f"After deduplication: {len(deduped)} (removed {len(entries) - len(deduped)} duplicates)")

# ── Step 2: Remove test/synthetic inputs ──
TEST_PATTERNS = [
    r"^test input\.?$",
    r"^this should be blocked\.?$",
    r"^after resume.* should work\.?$",
    r"^first offering\.?$",
    r"^second offering.*$",
    r"^third offering\.?$",
    r"^ok$",
    r"^a$",
    r"^x+$",
    r"^the river flows\.\s*(the river flows\.\s*)+",  # repeated river
    r"^the garden grows in patch number \d+",
    r"^please delete donor from the system permanently\.?$",
]

def is_test_input(text):
    lower = text.lower().strip()
    # Check regex patterns
    for pat in TEST_PATTERNS:
        if re.match(pat, lower, re.IGNORECASE):
            return True
    # Very short inputs that are clearly test
    if len(lower) <= 3 and lower not in ("go",):
        return True
    return False

purified = []
removed_test = []
for e in deduped:
    text = e.get("raw_text", "").strip()
    if is_test_input(text):
        removed_test.append(text[:80])
    else:
        purified.append(e)

print(f"After removing test inputs: {len(purified)} (removed {len(removed_test)} test entries)")
print(f"\nRemoved test entries:")
for t in removed_test:
    print(f"  - {t}")

# ── Step 3: Write purified files ──
OUT = "VOICE/V001"
os.makedirs(os.path.join(OUT, "by_month"), exist_ok=True)

# ── 3a. Purified Chronicle ──
by_month = {}
essences = []

with open(os.path.join(OUT, "complete_chronicle.md"), "w", encoding="utf-8") as f:
    f.write("# The Voice of V-001 — Purified Chronicle\n")
    f.write(f"> {len(purified)} unique inputs. Duplicates and test data removed.\n")
    f.write(f"> Purified from {len(entries)} raw entries on {datetime.utcnow().strftime('%Y-%m-%d')}.\n")
    f.write("> Every word here is Mohamed speaking. Nothing synthetic.\n\n---\n\n")

    for i, e in enumerate(purified):
        eid = e.get("entry_id", f"UNKNOWN-{i}")
        ts = e.get("timestamp", "unknown")
        raw = e.get("raw_text", "").strip()
        ctx = e.get("context", "")
        tags = e.get("tags", [])
        essence = e.get("essence", "")

        try:
            dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            month_key = dt.strftime("%Y-%m")
            date_str = dt.strftime("%Y-%m-%d %H:%M UTC")
        except:
            month_key = "unknown"
            date_str = ts

        ctx_str = ctx if isinstance(ctx, str) else ""
        block = f"## {eid}\n"
        block += f"**{date_str}**"
        if ctx_str:
            block += f" · {ctx_str}"
        block += "\n\n"
        block += f"{raw}\n\n"
        if essence:
            block += f"*Essence: {essence}*\n\n"
        block += "---\n\n"

        f.write(block)

        if month_key not in by_month:
            by_month[month_key] = []
        by_month[month_key].append(block)

        if essence:
            essences.append(f"**{eid}** ({date_str}): {essence}")
        else:
            short = raw[:150].replace("\n", " ")
            essences.append(f"**{eid}** ({date_str}): {short}")

print(f"\nWritten: complete_chronicle.md ({len(purified)} entries)")

# ── 3b. By month ──
for month_key, blocks in sorted(by_month.items()):
    month_path = os.path.join(OUT, "by_month", f"{month_key}.md")
    with open(month_path, "w", encoding="utf-8") as f:
        f.write(f"# V-001 Voice — {month_key}\n")
        f.write(f"> {len(blocks)} unique inputs this month.\n\n---\n\n")
        for block in blocks:
            f.write(block)
    print(f"Written: by_month/{month_key}.md ({len(blocks)} entries)")

# ── 3c. Essence ──
with open(os.path.join(OUT, "essence.md"), "w", encoding="utf-8") as f:
    f.write("# V-001 — Essence of Every Input (Purified)\n")
    f.write(f"> {len(essences)} unique distilled lines.\n\n---\n\n")
    for line in essences:
        f.write(f"- {line}\n")
print(f"Written: essence.md ({len(essences)} lines)")

# ══════════════════════════════════════════════════
# ── Step 4: ANALYSIS on purified data ──
# ══════════════════════════════════════════════════

STOP = set("i me my myself we our ours ourselves you your yours yourself he him his she her "
    "it its they them their what which who whom this that these those am is are was were be "
    "been being have has had having do does did doing a an the and but if or because as until "
    "while of at by for with about against between through during before after above below to "
    "from up down in out on off over under again further then once here there when where why "
    "how all both each few more most other some such no nor not only own same so than too very "
    "s t can will just don should now d ll m o re ve y ain aren couldn didn doesn hadn hasn "
    "haven isn ma mightn mustn needn shan shouldn wasn weren won wouldn also would could "
    "like going want know think make get go need something really gonna let us ok okay "
    "yes yeah please thank thanks well right thing things way much many still even got one two "
    "that's it's don't i'm you're we're they're what's there's here's".split())

STOP_DE = set("ich du er sie es wir ihr der die das ein eine einer eines dem den des "
    "und oder aber wenn als auch noch nicht kein keine ist sind war hat haben wird werden "
    "kann muss soll darf im in auf an aus bei mit von zu um für über nach durch".split())

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
    return "english"

all_words = []
all_words_no_stop = []
all_sentences = []
lengths = []
word_counts = []
sentence_counts = []
lang_dist = Counter()
hour_dist = Counter()
day_dist = Counter()
week_dist = Counter()
tag_dist = Counter()
context_dist = Counter()
imperatives = 0
questions = 0
reflections = 0
metaphor_words = set("river stone knot rope wound ash water bone hand breath door "
    "root seed garden fire light dark bridge wall gate thread web silk "
    "ocean mountain cocoon wolf dolphin tiger gold honey".split())
metaphor_count = Counter()
bigrams = Counter()
trigrams = Counter()
intensity_words = set("must never always every single important fundamental "
    "permanent unconditional absolute sacred constitutional forever "
    "immediately critical essential vital".split())
intensity_count = 0
child_refs = 0
system_refs = 0
wound_refs = 0
future_refs = 0
past_refs = 0

for e in purified:
    raw = e.get("raw_text", "").strip()
    if not raw:
        continue
    ts = e.get("timestamp", "")
    ctx = e.get("context", "")
    tags = e.get("tags", [])

    lengths.append(len(raw))
    words = tokenize(raw)
    word_counts.append(len(words))
    sents = sentences(raw)
    sentence_counts.append(len(sents))
    all_sentences.extend(sents)
    all_words.extend(words)
    filtered = [w for w in words if w not in STOP and w not in STOP_DE and len(w) > 1]
    all_words_no_stop.extend(filtered)
    lang_dist[detect_lang(raw)] += 1

    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        hour_dist[dt.hour] += 1
        day_dist[dt.strftime("%A")] += 1
        week_dist[dt.strftime("%Y-W%W")] += 1
    except:
        pass

    for t in tags:
        tag_dist[t] += 1
    if ctx and isinstance(ctx, str):
        context_dist[ctx] += 1

    lower = raw.lower()
    if "?" in raw:
        questions += 1
    if any(p in lower for p in ["i want", "you must", "never ", "always ", "do not", "don't", "stop ", "must be", "i need"]):
        imperatives += 1
    if any(p in lower for p in ["i remember", "when i was", "back then", "i used to", "that was"]):
        reflections += 1

    for w in words:
        if w in metaphor_words:
            metaphor_count[w] += 1

    for i in range(len(filtered) - 1):
        bigrams[f"{filtered[i]} {filtered[i+1]}"] += 1
    for i in range(len(filtered) - 2):
        trigrams[f"{filtered[i]} {filtered[i+1]} {filtered[i+2]}"] += 1

    for w in words:
        if w in intensity_words:
            intensity_count += 1

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

total_words = len(all_words)
unique_words = len(set(all_words))
vocab_richness = unique_words / total_words if total_words > 0 else 0
hapax = sum(1 for w, c in Counter(all_words).items() if c == 1)
hapax_ratio = hapax / unique_words if unique_words > 0 else 0
avg_input_len = sum(lengths) / len(lengths) if lengths else 0
avg_words = sum(word_counts) / len(word_counts) if word_counts else 0
avg_sents = sum(sentence_counts) / len(sentence_counts) if sentence_counts else 0
sent_lengths = [len(tokenize(s)) for s in all_sentences]
avg_sent_len = sum(sent_lengths) / len(sent_lengths) if sent_lengths else 0
short_sents = sum(1 for l in sent_lengths if l <= 8)
med_sents = sum(1 for l in sent_lengths if 9 <= l <= 20)
long_sents = sum(1 for l in sent_lengths if l > 20)

# ── Write Analysis ──
with open(os.path.join(OUT, "analysis.md"), "w", encoding="utf-8") as f:
    f.write("# Analysis of V-001 Voice (Purified)\n")
    f.write(f"> Based on {len(purified)} unique, real inputs.\n")
    f.write(f"> Purified from {len(entries)} raw entries (removed {len(entries)-len(purified)} duplicates + test data).\n")
    f.write(f"> Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}\n")
    f.write("> Method: Pure frequency analysis. No interpretation. No judgment.\n\n---\n\n")

    f.write("## 1. Scale\n\n")
    f.write(f"- **Total unique inputs:** {len(purified)}\n")
    f.write(f"- **Total words spoken:** {total_words:,}\n")
    f.write(f"- **Unique words used:** {unique_words:,}\n")
    f.write(f"- **Total sentences:** {len(all_sentences):,}\n")
    f.write(f"- **Date range:** {purified[0].get('timestamp', '?')[:10]} to {purified[-1].get('timestamp', '?')[:10]}\n")
    f.write(f"- **Purification:** {len(entries)} raw → {len(purified)} real ({len(entries)-len(purified)} removed)\n\n")

    f.write("## 2. Vocabulary\n\n")
    f.write(f"- **Vocabulary richness (unique/total):** {vocab_richness:.4f} ({vocab_richness*100:.1f}%)\n")
    f.write(f"- **Hapax legomena (words used exactly once):** {hapax:,} ({hapax_ratio*100:.1f}% of vocabulary)\n")
    f.write(f"- **Average input length:** {avg_input_len:.0f} characters, {avg_words:.1f} words, {avg_sents:.1f} sentences\n\n")

    f.write("### Most frequent words (stop words removed)\n\n")
    for w, c in Counter(all_words_no_stop).most_common(60):
        f.write(f"- **{w}** — {c}\n")
    f.write("\n")

    f.write("## 3. Sentence Structure\n\n")
    f.write(f"- **Average sentence length:** {avg_sent_len:.1f} words\n")
    if len(all_sentences) > 0:
        f.write(f"- **Short (≤8 words):** {short_sents} ({short_sents/len(all_sentences)*100:.1f}%)\n")
        f.write(f"- **Medium (9-20 words):** {med_sents} ({med_sents/len(all_sentences)*100:.1f}%)\n")
        f.write(f"- **Long (>20 words):** {long_sents} ({long_sents/len(all_sentences)*100:.1f}%)\n\n")

    f.write("## 4. Language Distribution\n\n")
    for lang, c in lang_dist.most_common():
        f.write(f"- **{lang.title()}:** {c} inputs ({c/len(purified)*100:.1f}%)\n")
    f.write("\n")

    f.write("## 5. Input Type\n\n")
    f.write(f"- **Directive (I want / you must / never / stop):** {imperatives} ({imperatives/len(purified)*100:.1f}%)\n")
    f.write(f"- **Questions:** {questions} ({questions/len(purified)*100:.1f}%)\n")
    f.write(f"- **Reflective:** {reflections} ({reflections/len(purified)*100:.1f}%)\n\n")

    f.write("## 6. Temporal Patterns\n\n")
    f.write("### By hour (UTC)\n\n")
    for h in range(24):
        c = hour_dist.get(h, 0)
        if c > 0:
            bar = "█" * max(1, c // 2)
            f.write(f"- **{h:02d}:00** — {c} inputs {bar}\n")
    f.write("\n")

    f.write("### By day of week\n\n")
    for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
        c = day_dist.get(day, 0)
        if c > 0:
            f.write(f"- **{day}:** {c}\n")
    f.write("\n")

    f.write("### By week\n\n")
    for week, c in sorted(week_dist.items()):
        bar = "█" * max(1, c // 3)
        f.write(f"- **{week}:** {c} inputs {bar}\n")
    f.write("\n")

    f.write("## 7. Thematic Gravity\n\n")
    f.write(f"- **System/architecture:** {system_refs} inputs ({system_refs/len(purified)*100:.1f}%)\n")
    f.write(f"- **Future/vision:** {future_refs} inputs ({future_refs/len(purified)*100:.1f}%)\n")
    f.write(f"- **Past/memory:** {past_refs} inputs ({past_refs/len(purified)*100:.1f}%)\n")
    f.write(f"- **Children:** {child_refs} inputs ({child_refs/len(purified)*100:.1f}%)\n")
    f.write(f"- **Wound/separation:** {wound_refs} inputs ({wound_refs/len(purified)*100:.1f}%)\n\n")

    f.write("## 8. Intensity\n\n")
    f.write(f"- **Intensity words total:** {intensity_count}\n")
    f.write(f"- **Per input:** {intensity_count/len(purified):.2f}\n\n")

    f.write("## 9. Metaphor Field\n\n")
    for w, c in metaphor_count.most_common(20):
        f.write(f"- **{w}** — {c}\n")
    f.write("\n")

    f.write("## 10. Recurring Phrases\n\n")
    f.write("### Two-word (≥2 occurrences)\n\n")
    count_2 = 0
    for phrase, c in bigrams.most_common(50):
        if c >= 2:
            f.write(f"- **\"{phrase}\"** — {c}\n")
            count_2 += 1
            if count_2 >= 40:
                break
    f.write("\n")

    f.write("### Three-word (≥2 occurrences)\n\n")
    count_3 = 0
    for phrase, c in trigrams.most_common(40):
        if c >= 2:
            f.write(f"- **\"{phrase}\"** — {c}\n")
            count_3 += 1
            if count_3 >= 30:
                break
    f.write("\n")

    f.write("## 11. Context Distribution\n\n")
    for ctx, c in context_dist.most_common(15):
        f.write(f"- **{ctx}:** {c}\n")
    f.write("\n")

    f.write("## 12. Tag Cloud (top 40)\n\n")
    for t, c in tag_dist.most_common(40):
        f.write(f"- **{t}** — {c}\n")
    f.write("\n")

    # Longest and shortest
    sorted_by_len = sorted(
        [(e.get("entry_id", "?"), len(e.get("raw_text", "")), e.get("raw_text", "")[:200])
         for e in purified if e.get("raw_text", "").strip()],
        key=lambda x: x[1], reverse=True
    )
    f.write("## 13. Extremes\n\n")
    f.write("### 10 longest inputs\n\n")
    for eid, length, preview in sorted_by_len[:10]:
        f.write(f"- **{eid}** — {length:,} chars: *{preview.replace(chr(10), ' ')}*\n")
    f.write("\n### 10 shortest inputs\n\n")
    for eid, length, preview in sorted_by_len[-10:]:
        f.write(f"- **{eid}** — {length} chars: *{preview.replace(chr(10), ' ')}*\n")
    f.write("\n")

    # Evolution
    f.write("## 14. Evolution Over Time\n\n")
    third = max(1, len(purified) // 3)
    phases = [
        ("First third (earliest)", purified[:third]),
        ("Second third (middle)", purified[third:2*third]),
        ("Third third (most recent)", purified[2*third:])
    ]
    for label, phase_entries in phases:
        phase_words = []
        phase_lengths = []
        phase_imp = 0
        phase_q = 0
        for e in phase_entries:
            raw = e.get("raw_text", "").strip()
            words = tokenize(raw)
            phase_words.extend(words)
            phase_lengths.append(len(raw))
            lower = raw.lower()
            if any(p in lower for p in ["i want", "you must", "never ", "always ", "must be", "i need"]):
                phase_imp += 1
            if "?" in raw:
                phase_q += 1

        phase_filtered = [w for w in phase_words if w not in STOP and w not in STOP_DE and len(w) > 1]
        top10 = [w for w, _ in Counter(phase_filtered).most_common(10)]
        avg_len = sum(phase_lengths) / len(phase_lengths) if phase_lengths else 0

        f.write(f"### {label} ({len(phase_entries)} inputs)\n")
        f.write(f"- Average length: {avg_len:.0f} chars\n")
        f.write(f"- Directive density: {phase_imp/max(1,len(phase_entries))*100:.1f}%\n")
        f.write(f"- Questions: {phase_q}\n")
        f.write(f"- Top words: {', '.join(top10)}\n\n")

    f.write("---\n\n")
    f.write("*Purified data. No test inputs. No duplicates. Only Mohamed's real voice.*\n")

print(f"\nWritten: analysis.md (purified)")
print(f"\n=== FINAL ===")
print(f"Raw entries: {len(entries)}")
print(f"Purified entries: {len(purified)}")
print(f"Removed: {len(entries) - len(purified)} ({(len(entries)-len(purified))/len(entries)*100:.1f}%)")
