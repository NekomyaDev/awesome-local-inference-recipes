"""Language-purity rules for the Chinese prose fields (ZH_FIELDS; `metric` is the main one).

Chinese text uses 解码 / 预填充 / 智能体, not the English words. These stay English:
capitalised names (Hermes Agent, Prefill Accelerator), hyphen/underscore compounds
(agent-trace, --prefill-pipe, ds4-agent), Latin pairs joined by a slash (prompt/decode,
chat/agent), and text inside backticks, URLs or quotes (「Decode (New C++20)」)."""
import re

TERMS = {'decode': '解码', 'prefill': '预填充', 'agent': '智能体', 'agents': '智能体'}
WORD = re.compile(r'(?<![A-Za-z0-9_\-])(decode|prefill|agents?)(?![A-Za-z0-9_\-])')
PROTECTED = re.compile(r'`[^`]*`|https?://\S+|「[^」]*」|“[^”]*”|"[^"]*"')


def bare_en_terms(s):
    """Return the (start, word) of each English term that should have been written in Chinese."""
    if not s: return []
    spans = [m.span() for m in PROTECTED.finditer(s)]
    out = []
    for m in WORD.finditer(s):
        a, b = m.span()
        if any(x <= a < y for x, y in spans): continue
        if a > 1 and s[a-1] == '/' and s[a-2].isascii() and s[a-2].isalpha(): continue
        if b + 1 < len(s) and s[b] == '/' and s[b+1].isascii() and s[b+1].isalpha(): continue
        out.append((a, m.group(1)))
    return out


# Fields that hold Chinese prose. engine_raw and launch_command keep the source's own wording.
# engine_note is derived from engine_raw by normalize_engines.py and keeps the source's own wording,
# same as engine_raw and launch_command, so it is not in this list.
ZH_FIELDS = ('metric', 'source_note', 'quant', 'hardware', 'hardware_cost_text', 'context', 'concurrency', 'model')
QUOTE = re.compile(r'原文[:：]')
URL_FULLSTOP = re.compile(r'(?:https?://|(?<![\w.@/-])(?:[a-z0-9-]+\.)+[a-z]{2,}/)[\x21-\x7e]*。', re.I)


def own_text(s):
    """The Chinese part of a field: everything before a verbatim 原文: quote."""
    return QUOTE.split(s, 1)[0] if s else s


def zh_field_problems(r):
    """Return (field, problem) pairs for the Chinese prose fields of one recipe: a bare decode / prefill /
    agent, the word 并发 (write 同时处理 N 个请求 or 多请求), or 。 straight after a URL (put a space
    between them, or end the sentence before the link)."""
    out = []
    for f in ZH_FIELDS:
        v = r.get(f)
        if not isinstance(v, str): continue
        if URL_FULLSTOP.search(v): out.append((f, 'URL followed by 。'))
        t = own_text(v)
        if '并发' in t: out.append((f, '并发'))
        out += [(f, w) for _, w in bare_en_terms(t)]
    return out
