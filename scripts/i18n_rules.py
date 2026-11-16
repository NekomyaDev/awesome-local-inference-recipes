"""Language-purity rules for the Chinese `metric` field.

The ZH metric uses 解码 / 预填充 / 智能体, not the English words. These stay English:
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
