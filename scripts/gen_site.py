#!/usr/bin/env python3
"""Static, crawlable parts of the Pages site (no JS needed to read them). Source of truth: data/recipes.json + recipes/*.md.
- explore.html: full static fallback table
- guides/<id>.html (+ zh-CN/ ja/): recipe guides from recipes/*.md; matching index.html per language; self-canonical + hreflang
- hw|model/{,zh-CN/,ja/}<slug>.html: landing pages
- sitemap.xml
Run: python3 scripts/gen_site.py"""
import json, re, html
from urllib.parse import quote
from pathlib import Path
import gen_readme, ja_text
from dataset_constants import DATA_ASOF
from hardware_index import HW, MIN_ROWS, selfrep, single, meas_text, COMPARE
R = Path(__file__).resolve().parent.parent
PAGES = 'https://raytone-lab.github.io/awesome-local-inference-recipes/'
REPO = 'https://github.com/raytone-lab/awesome-local-inference-recipes'
STATIC_ROWS_START = '<!--static:rows (scripts/gen_site.py)-->'
STATIC_ROWS_END = '<!--/static-->'
D = json.load(open(R/'data/recipes.json', encoding='utf-8'))
ASOF = DATA_ASOF
LV = {'官方':'Official','实测':'Measured','转述':'Relayed','宣称':'Claimed'}
HWF = {'NVIDIA 消费级':'NVIDIA consumer','二手数据中心卡':'Used datacenter','其他':'Other'}
e = lambda s: html.escape(str(s if s is not None else ''), quote=True)
def write(p, s):
    p.parent.mkdir(parents=True, exist_ok=True); p.write_text(s, encoding='utf-8')
def normalize_punct(s): return s.replace('；', '; ').replace('，', ', ')
def en(s):
    if not s: return s
    return gen_readme.en(normalize_punct(str(s)), cjk=gen_readme.CJK_CHAR, strip=' ·+/,;；') or s
def met_en(r): return r.get('metric_en') or en(r.get('metric'))
def ja_met(r):
    m = ja_text.metric(r) or ''
    return gen_readme.mark_ja_en(m) if ja_text.english_fallback(r) or ja_text.needs_en_mark(m) else m
def fen(r, k): return (r.get('en') or {}).get(k) or en(r.get(k))
def safe_url(u): return u if re.match(r'(https?:)?//|[\w./#?=&%-]+$', u) and not u.lower().startswith('javascript:') else '#'

def row(r):
    tok = '' if r.get('tok_s') is None else f"{r['tok_s']:g}"
    cost = f"{r['hardware_cost_usd']:,}" if r.get('hardware_cost_usd') is not None else e(fen(r, 'hardware_cost_text') or '')
    cpt = round(r['hardware_cost_usd']/r['tok_s']) if r.get('tok_s') and r.get('hardware_cost_usd') else ''
    met = met_en(r) or ''
    return (f'<tr data-id="{e(r["id"])}"><td></td><td>{e(fen(r, "model"))}</td><td>{e(fen(r, "quant") or "")}</td><td>{e(r["engine"])}</td>'
            f'<td>{e(fen(r, "hardware"))}</td><td class="n">{tok}</td><td>{e(met)}</td><td class="n">{cost}</td><td class="n">{cpt}</td>'
            f'<td>{e(fen(r, "context") or "")}</td><td><a href="{e(r["source_url"])}" rel="nofollow noopener">{LV.get(r["source_level"], e(r["source_level"]))}{" (self-reported)" if selfrep(r) else ""}</a> {e(r.get("date") or "")}</td></tr>')
def explore(links):
    p = R/'explore.html'; s = p.read_text(encoding='utf-8')
    rows = '\n'.join(row(r) for r in sorted(D, key=lambda r: (-(r.get('tok_s') or 0), r['id'])))
    s = re.sub(r'<tbody id="tb">.*?</tbody>', lambda m: f'<tbody id="tb">{STATIC_ROWS_START}\n{rows}\n{STATIC_ROWS_END}</tbody>', s, flags=re.S)
    nav = '<nav class="static-links" aria-label="Browse" data-i18n-al="nav_browse"><a href="guides/index.html" data-i18n="nav_guides">Guides &amp; hardware / model pages</a></nav>'
    blk = f'<!--static:links-->{nav}<!--/static:links-->'
    if '<!--static:links-->' in s: s = re.sub(r'<!--static:links-->.*?<!--/static:links-->', lambda m: blk, s, flags=re.S)
    else: s = s.replace('<div class="more" id="morew"', blk + '\n<div class="more" id="morew"', 1)
    write(p, s)

def inline(t, linkmap):
    out = []; i = 0
    for m in re.finditer(r'`([^`]+)`|\*\*([^*]+)\*\*|\[([^\]]+)\]\(([^)\s]+)\)', t):
        out.append(e(t[i:m.start()]))
        if m.group(1) is not None: out.append(f'<code>{e(m.group(1))}</code>')
        elif m.group(2) is not None: out.append(f'<b>{inline(m.group(2), linkmap)}</b>')
        else:
            u = safe_url(linkmap(m.group(4))); ext = u.startswith('http')
            out.append(f'<a href="{e(u)}"{" rel=\"nofollow noopener\"" if ext else ""}>{inline(m.group(3), linkmap)}</a>')
        i = m.end()
    out.append(e(t[i:])); return ''.join(out)
def md(src, linkmap):
    L = src.split('\n'); h = []; i = 0; lst = False
    def close():
        nonlocal lst
        if lst: h.append('</ul>'); lst = False
    while i < len(L):
        l = L[i]
        if l.startswith('```'):
            close(); j = i+1; buf = []
            while j < len(L) and not L[j].startswith('```'): buf.append(L[j]); j += 1
            h.append(f'<pre><code>{e(chr(10).join(buf))}</code></pre>'); i = j+1; continue
        m = re.match(r'(#{1,3}) (.*)', l)
        if m: close(); n = len(m.group(1)); h.append(f'<h{n}>{inline(m.group(2), linkmap)}</h{n}>')
        elif l.startswith('- '):
            if not lst: h.append('<ul>'); lst = True
            h.append(f'<li>{inline(l[2:], linkmap)}</li>')
        elif l.startswith('> '): close(); h.append(f'<blockquote>{inline(l[2:], linkmap)}</blockquote>')
        elif l.strip(): close(); h.append(f'<p>{inline(l, linkmap)}</p>')
        else: close()
        i += 1
    close(); return '\n'.join(h)

DISPLAY_VALUES = {'zh-CN': {'Unspecified': '未注明', 'Other': '其他'}, 'ja': {'Unspecified': '未指定', 'Other': 'その他'}}
SWITCH_LABEL = {'en': 'English', 'zh-CN': '简体中文', 'ja': '日本語'}
LVL = {'en': LV, 'zh-CN': {k: k for k in LV}, 'ja': {'官方': '公式', '实测': '実測', '转述': '伝聞', '宣称': '主張'}}
CHROME = {'en': ('Explore', 'Guides', 'Data as of', 'Local Inference Recipes', 'data CC BY 4.0'), 'zh-CN': ('配方库', '指南', '数据截至', '本地推理配方', '数据 CC BY 4.0'), 'ja': ('エクスプローラー', 'ガイド', 'データ時点', 'ローカル推論レシピ', 'データ CC BY 4.0')}
LANGS = [('en', '', '.md', 'en'), ('zh-CN', 'zh-CN/', '.zh-CN.md', 'zh-CN'), ('ja', 'ja/', '.ja.md', 'ja')]
PRE = {hl: pre for _, pre, _, hl in LANGS}
ORDER = [hl for *_, hl in LANGS]
SUF2PRE = {'': '', '.zh-CN': 'zh-CN/', '.ja': 'ja/'}
def shell(title, desc, canon, body, depth, lang='en', alts=None, noindex=False):
    up = '../'*depth
    gidx = 'guides/' + PRE[lang] + 'index.html'
    alt = ''.join(f'<link rel="alternate" hreflang="{hl}" href="{u}">' for hl, u in (alts or []))
    return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canon}">{alt}{'<meta name="robots" content="noindex,follow">' if noindex else ''}
<meta property="og:type" content="article"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{PAGES}docs/og.png"><meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="{up}style.css"><script src="{up}theme.js"></script></head><body>
<header class="site-hd"><div class="hd-in"><a class="brand" href="{up}index.html{'?lang='+lang}">⚡ {CHROME[lang][3]}</a><nav class="static-links"><a href="{up}explore.html{'?lang='+lang}">{CHROME[lang][0]}</a> · <a href="{up}{gidx}">{CHROME[lang][1]}</a> · <a href="{REPO}">GitHub</a></nav></div></header>
<main class="doc static-page">
{body}
</main><footer class="site-ft"><div class="ft-in">{CHROME[lang][2]} {ASOF} · <a href="{REPO}">GitHub</a> · {CHROME[lang][4]}</div></footer></body></html>
'''

def guides():
    ids = sorted({p.name.split('.')[0] for p in (R/'recipes').glob('*.md') if not p.name.startswith('README')})
    available = {rid: {hl for _, pre, suf, hl in LANGS if (R/'recipes'/f'{rid}{suf}').exists()} for rid in ids}
    urls = []
    for rid in ids:
        alts = [(hl, f'{PAGES}guides/{PRE[hl]}{rid}.html') for hl in ORDER if hl in available[rid]]
        alts.append(('x-default', f'{PAGES}guides/{rid}.html'))
        for lang, pre, suf, hl in LANGS:
            src = R/'recipes'/f'{rid}{suf}'
            if not src.exists(): continue
            depth = 1 + (1 if pre else 0)
            def lm(u, depth=depth):
                m = re.match(r'^([\w.-]+?)(\.zh-CN|\.ja)?\.md$', u)
                if m and not u.startswith('../'):
                    return '../'*depth + 'guides/' + SUF2PRE[m.group(2) or ''] + m.group(1) + '.html'
                if u.startswith('../README'):
                    sm = re.match(r'^\.\./README(\.zh-CN|\.ja)?\.md$', u)
                    return '../'*depth + 'guides/' + SUF2PRE[(sm.group(1) if sm else '') or ''] + 'index.html'
                if u.startswith('../'): return f'{REPO}/blob/main/' + u[3:]
                return u
            text = src.read_text(encoding='utf-8')
            title = re.match(r'# (.*)', text).group(1)
            r = next((x for x in D if x['id'] == rid), {})
            desc = {'en': 'How to run {t}. Hardware, engine, launch command, and sourced speed ({lv}).',
                    'zh-CN': '{t} 运行指南。硬件、引擎、启动命令与有出处的速度（{lv}）。',
                    'ja': '{t} の実行ガイド。ハードウェア、エンジン、起動コマンド、出典付きの速度（{lv}）。'}[lang].format(t=title, lv=LVL[lang].get(r.get('source_level'), ''))
            sf = {'en': 'Source file', 'zh-CN': '源文件', 'ja': 'ソースファイル'}[lang]
            body = md(text, lm) + f'\n<p class="na">{sf}: <a href="{REPO}/blob/main/recipes/{rid}{suf}">recipes/{rid}{suf}</a></p>'
            canon = f'{PAGES}guides/{pre}{rid}.html'
            write(R/'guides'/f'{pre}{rid}.html', shell(title, desc, canon, body, depth, hl, alts)); urls.append(canon)
    return ids, urls, available

def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
def landing(kind, key, name, rows, qterm=None):
    rows = sorted(rows, key=lambda r: (r['source_level'] != '实测', -(r.get('tok_s') or 0), r['id']))
    meas = [r for r in rows if meas_text(r) and single(r)]
    nmeas = sum(1 for r in rows if r['source_level'] == '实测' and not selfrep(r))
    dates = sorted(r['date'] for r in rows if r.get('date'))
    noidx = len(rows) < MIN_ROWS
    file = slug(key) if kind == 'model' else key
    best = max(meas, key=lambda r: (r['tok_s'], r['id'])) if meas else None
    all_media = all(r['category'] != 'text' for r in rows)
    LC = {
        'en': dict(
            nrec=lambda n: f'{n} recipe' + ('' if n == 1 else 's'),
            q=(f'{name}: local inference speed (tok/s), sourced' if kind == 'model'
               else f'Setups with {name}: local inference speed (tok/s), sourced'),
            th=('Model', 'Engine', 'Hardware', 'tok/s', 'Metric', 'Source level', 'Date', 'Source'),
            link='link', selfrep=' (self-reported)', filter_='Filter these in the explorer →',
            note='Numbers come from each source. This project did not measure them again. Models and settings differ between rows. Source levels: Official = project or vendor; Measured = the poster ran it (an engine or recipe author must also publish raw data and reproduction steps); Relayed = second-hand; Claimed = prediction or no reproduction details.',
            lab=lambda r, k: fen(r, k) if k != 'engine' else r.get('engine'),
            met=lambda r: met_en(r) or ''),
        'zh-CN': dict(
            nrec=lambda n: f'{n} 条配方',
            q=(f'{name}：本地推理速度（tok/s），均有出处' if kind == 'model'
               else f'{name} 相关配置：本地推理速度（tok/s），均有出处'),
            th=('模型', '引擎', '硬件', 'tok/s', '指标', '来源等级', '日期', '来源'),
            link='链接', selfrep='（自称）', filter_='在配方库中筛选这些 →',
            note='数字来自各条来源。本项目未复测。各行的模型与设置不同。来源等级：官方 = 项目方或厂商；实测 = 发帖人亲测（引擎或配方作者须公开原始数据和复现步骤）；转述 = 二手；宣称 = 预测或无复现细节。',
            lab=lambda r, k: r.get(k) or '',
            met=lambda r: r.get('metric') or ''),
        'ja': dict(
            nrec=lambda n: f'{n} 件',
            q=(f'{name}：ローカル推論速度（tok/s）、出典付き' if kind == 'model'
               else f'{name} の構成：ローカル推論速度（tok/s）、出典付き'),
            th=('モデル', 'エンジン', 'ハードウェア', 'tok/s', '指標', '出典レベル', '日付', '出典'),
            link='リンク', selfrep='（自己申告）', filter_='エクスプローラーで絞り込む →',
            note='数値は各出典のものです。本プロジェクトでは再計測していません。行ごとにモデルと設定が異なります。出典レベル：公式 = プロジェクトまたはベンダー、実測 = 投稿者が実行（エンジンまたはレシピの作者は生データと再現手順も公開する）、伝聞 = 二次情報、主張 = 予測または再現手順なし。',
            lab=lambda r, k: fen(r, k) if k != 'engine' else r.get('engine'),
            met=lambda r: ja_text.metric(r) or ''),
    }

    def summary(lang, n):
        if lang == 'en':
            if best:
                eng = '' if best['engine'] == 'Unspecified' else f' on {e(best["engine"])}'
                nmeas_s = '1 was measured by the poster' if nmeas == 1 else f'{nmeas} were measured by the poster'
                summ = (f'As of {ASOF}, this dataset has <b>{n}</b> for {e(name)}. {nmeas_s}. '
                        f'Fastest measured single-device, single-stream text result: <b>{best["tok_s"]:g} tok/s</b> with {e(fen(best, "model"))}{eng} ({e(fen(best, "hardware"))}; '
                        f'Measured{", " + e(best["date"]) if best.get("date") else ""}; <a href="{e(best["source_url"])}" rel="nofollow noopener">source</a>).')
            else:
                if nmeas:
                    nmeas_s = '1 was measured by the poster.' if nmeas == 1 else f'{nmeas} were measured by the poster.'
                    summ = f'As of {ASOF}, this dataset has <b>{n}</b> for {e(name)}. {nmeas_s}'
                else:
                    summ = (f'As of {ASOF}, this dataset has <b>{n}</b> for {e(name)}. '
                            f'None is first-hand yet. Treat the numbers below as official, claimed, or relayed.')
                if all_media:
                    summ += ' These are image, video, or audio results. Speed is in the metric column, not tok/s.'
            if dates:
                nd = len(dates); entry_s = 'entry has' if nd == 1 else 'entries have'
                summ += (f' {nd} {entry_s} a date' + (f' ({dates[0]}).' if dates[0] == dates[-1] else f', from {dates[0]} to {dates[-1]}.'))
            return summ
        if lang == 'zh-CN':
            if best:
                eng = '' if best['engine'] == 'Unspecified' else f'，引擎 {e(best["engine"])}'
                summ = (f'截至 {ASOF}，本数据集中 {e(name)} 有 <b>{n}</b>，其中发帖人实测 {nmeas} 条。'
                        f'单机单流文字最快实测：<b>{best["tok_s"]:g} tok/s</b>，模型 {e(best.get("model") or "")}{eng}（{e(best.get("hardware") or "")}；'
                        f"实测{'；' + e(best['date']) if best.get('date') else ''}；<a href=\"{e(best['source_url'])}\" rel=\"nofollow noopener\">来源</a>）。")
            else:
                summ = (f'截至 {ASOF}，本数据集中 {e(name)} 有 <b>{n}</b>，发帖人实测 {nmeas} 条'
                        + ('。' if nmeas else '。尚无一手实测，下列数字请按官方、宣称或转述理解。')
                        + ('这些是图像 / 视频 / 音频结果，速度见指标列，而非 tok/s。' if all_media else ''))
            if dates:
                summ += (f'其中 {len(dates)} 条有日期' + (f'（{dates[0]}）。' if dates[0] == dates[-1] else f'，从 {dates[0]} 到 {dates[-1]}。'))
            return summ
        if lang == 'ja':
            if best:
                eng = '' if best['engine'] == 'Unspecified' else f'、エンジン {e(best["engine"])}'
                summ = (f'{ASOF} 時点で、このデータセットには {e(name)} のレシピが <b>{n}</b>あります。投稿者実測は {nmeas} 件です。'
                        f'単一デバイス・シングルストリームのテキスト実測の最速は <b>{best["tok_s"]:g} tok/s</b>（{e(fen(best, "model"))}{eng}、{e(fen(best, "hardware"))}、'
                        f'実測{"、" + e(best["date"]) if best.get("date") else ""}、<a href="{e(best["source_url"])}" rel="nofollow noopener">出典</a>）。')
            else:
                if nmeas:
                    summ = f'{ASOF} 時点で、このデータセットには {e(name)} のレシピが <b>{n}</b>あります。投稿者実測は {nmeas} 件です。'
                else:
                    summ = (f'{ASOF} 時点で、このデータセットには {e(name)} のレシピが <b>{n}</b>あります。'
                            f'投稿者自身の実測はまだありません。以下は公式・主張・伝聞として読んでください。')
                if all_media:
                    summ += '画像・動画・音声の結果です。速度は tok/s ではなく指標列にあります。'
            if dates:
                summ += (f'日付のあるエントリは {len(dates)} 件' + (f'（{dates[0]}）。' if dates[0] == dates[-1] else f'（{dates[0]}〜{dates[-1]}）。'))
            return summ
        raise ValueError(f'unsupported lang: {lang}')

    canons = []
    for lang in ORDER:
        C = LC[lang]
        n = C['nrec'](len(rows))
        summ = summary(lang, n)
        depth = 1 if lang == 'en' else 2
        up = '../' * depth
        sw = []
        for hl in ORDER:
            href = (file + '.html') if hl == lang else ((('' if lang == 'en' else '../') + PRE[hl] + file + '.html'))
            sw.append(f'<b>{SWITCH_LABEL[hl]}</b>' if hl == lang else f'<a href="{href}">{SWITCH_LABEL[hl]}</a>')
        switch = '<p>' + ' | '.join(sw) + '</p>'
        thead = ''.join(f'<th>{h}</th>' for h in C['th'])
        t = [f'<table><thead><tr>{thead}</tr></thead><tbody>']
        uv = DISPLAY_VALUES.get(lang, {})
        for r in rows:
            tok = '' if r.get('tok_s') is None else f"{r['tok_s']:g}"
            model = C['lab'](r, 'model'); hw = C['lab'](r, 'hardware'); eng = C['lab'](r, 'engine')
            if uv:
                model, hw, eng = (uv.get(x, x) for x in (model, hw, eng))
            lv = LVL[lang].get(r['source_level'], '') + (C['selfrep'] if selfrep(r) else '')
            t.append(f'<tr><td>{e(model)}</td><td>{e(eng)}</td><td>{e(hw)}</td><td class="n">{tok}</td><td>{e(C["met"](r))}</td><td>{e(lv)}</td><td>{e(r.get("date") or "")}</td><td><a href="{e(r["source_url"])}" rel="nofollow noopener">{C["link"]}</a></td></tr>')
        t.append('</tbody></table>')
        base_q = {'hw': f'explore.html?q={quote(qterm or name)}', 'model': f'explore.html?family={quote(key)}'}[kind]
        base_q += f'&lang={lang}'
        qs = e(base_q)
        body = (switch + '<h1>' + e(C['q']) + '</h1>\n<p>' + summ + '</p>\n<p><a href="'
                + up + qs + '">' + C['filter_'] + '</a></p>\n' + ''.join(t)
                + '<p class="na">' + C['note'] + '</p>')
        canon = f'{PAGES}{kind}/{PRE[lang]}{file}.html'
        alts = [(hl, f'{PAGES}{kind}/{PRE[hl]}{file}.html') for hl in ORDER]
        alts.append(('x-default', f'{PAGES}{kind}/{file}.html'))
        desc = html.unescape(re.sub('<[^>]+>', '', summ))
        if len(desc) > 300:
            desc = desc[:300].rsplit(' ', 1)[0] or desc[:300]
        write(R/kind/f'{PRE[lang]}{file}.html', shell(C['q'], desc, canon, body, depth, lang, alts, noidx))
        canons.append(canon)
    return noidx, len(rows), canons

def main():
    for d in ('guides', 'hw', 'model'):
        for p in (R/d).rglob('*.html') if (R/d).exists() else []: p.unlink()
    ids, gurls, available = guides()
    pages = []
    for key, name, rx, qt in HW:
        rows = [r for r in D if re.search(rx, r['hardware'])]
        if rows:
            noidx, n, all_c = landing('hw', key, name, rows, qt)
            pages.append(('hw', key, name, all_c[0], noidx, n, all_c))
    fams = sorted({r['model_family'] for r in D if r['model_family'] != 'Other'})
    for f in fams:
        rows = [r for r in D if r['model_family'] == f]
        noidx, n, all_c = landing('model', f, f, rows)
        pages.append(('model', f, f, all_c[0], noidx, n, all_c))
    li = lambda items: '<ul>' + ''.join(items) + '</ul>'
    byid = {r['id']: r for r in D}
    LANG_LABEL = {'en': 'English', 'zh-CN': '中文', 'ja': '日本語'}
    def resolve_lang(rid, want):
        have = available.get(rid, set())
        if want in have: return want
        for hl in ORDER:
            if hl in have: return hl
        return None
    def index_rel_href(rid, cur, want):
        tgt = resolve_lang(rid, want)
        if tgt is None: return None
        prefix = '' if cur == 'en' else '../'
        if tgt == cur: return f'{rid}.html'
        return prefix + PRE[tgt] + f'{rid}.html'
    def index_switch(cur):
        parts = []
        for hl in ORDER:
            href = 'index.html' if hl == cur else (('' if cur == 'en' else '../') + PRE[hl] + 'index.html')
            parts.append(f'<b>{SWITCH_LABEL[hl]}</b>' if hl == cur else f'<a href="{href}">{SWITCH_LABEL[hl]}</a>')
        return '<p>' + ' | '.join(parts) + '</p>'
    def guide_alts(rid, cur):
        bits = []
        for hl in ORDER:
            if hl == cur or resolve_lang(rid, hl) != hl: continue
            href = index_rel_href(rid, cur, hl)
            bits.append(f'<a href="{href}">{LANG_LABEL[hl]}</a>')
        return ('(' + ' · '.join(bits) + ')') if bits else ''
    def guide_label(r, lang):
        if lang == 'zh-CN':
            return f'{e(r.get("model") or "")} · {e(r.get("hardware") or "")}'
        return f'{e(fen(r, "model"))} · {e(fen(r, "hardware"))}'
    IDX = {
        'en': dict(title='Recipe guides · Local Inference Recipes',
                   desc='Step-by-step recipe guides, plus hardware and model speed pages. Each number has a source.',
                   h1='Recipe guides, hardware pages, and model pages',
                   intro=f'Pages built from the dataset (as of {ASOF}). Each number links to its source.',
                   h_g='Recipe guides', h_hw='By hardware', h_m='By model family', n=lambda c: f'{c} recipes'),
        'zh-CN': dict(title='配方指南 · 本地推理配方',
                   desc='分步配方指南，以及按硬件、按模型的速度页面。每个数字都有出处。',
                   h1='配方指南、硬件页面与模型页面',
                   intro=f'由数据集生成的页面（截至 {ASOF}）。每个数字都链接到来源。',
                   h_g='配方指南', h_hw='按硬件', h_m='按模型系列', n=lambda c: f'{c} 条'),
        'ja': dict(title='レシピガイド · ローカル推論レシピ',
                   desc='手順付きレシピガイドと、ハードウェア別・モデル別の速度ページ。数値はすべて出典付きです。',
                   h1='レシピガイド、ハードウェアページ、モデルページ',
                   intro=f'データセットから生成したページ（{ASOF} 時点）。すべての数値に出典へのリンクがあります。',
                   h_g='レシピガイド', h_hw='ハードウェア別', h_m='モデル系列別', n=lambda c: f'{c} 件'),
    }
    idx_alts = [(hl, f'{PAGES}guides/{PRE[hl]}index.html') for hl in ORDER]
    idx_alts.append(('x-default', f'{PAGES}guides/index.html'))
    idx_urls = []
    for lang, meta in IDX.items():
        depth = 1 if lang == 'en' else 2
        up = '../' * depth
        g = []
        for rid in ids:
            if rid not in byid or not available.get(rid): continue
            href = index_rel_href(rid, lang, lang)
            if not href: continue
            g.append(f'<li><a href="{href}">{guide_label(byid[rid], lang)}</a> {guide_alts(rid, lang)}</li>')
        hwl = [f'<li><a href="{up}{k}/{PRE[lang]}{key}.html">{e(n)}</a> — {meta["n"](c)}</li>'
               for k, key, n, _, noidx, c, _ in pages if k == 'hw' and not noidx]
        ml = [f'<li><a href="{up}{k}/{PRE[lang]}{slug(key)}.html">{e(n)}</a> — {meta["n"](c)}</li>'
              for k, key, n, _, noidx, c, _ in pages if k == 'model' and not noidx]
        body = (index_switch(lang) + f'<h1>{meta["h1"]}</h1><p>{meta["intro"]}</p>'
                f'<h2>{meta["h_g"]}</h2>{li(g)}<h2 id="by-hardware">{meta["h_hw"]}</h2>{li(hwl)}<h2>{meta["h_m"]}</h2>{li(ml)}')
        canon = f'{PAGES}guides/{PRE[lang]}index.html'
        write(R/'guides'/f'{PRE[lang]}index.html', shell(meta['title'], meta['desc'], canon, body, depth, lang, idx_alts))
        idx_urls.append(canon)
    explore(None)
    land_urls = [u for *_, noidx, _n, all_c in pages if not noidx for u in all_c]
    urls = [PAGES, PAGES+'explore.html', PAGES+'speed.html', PAGES+'submit.html'] + idx_urls + gurls + land_urls
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm += [f'<url><loc>{e(u)}</loc><lastmod>{ASOF}</lastmod></url>' for u in urls]
    sm.append('</urlset>')
    write(R/'sitemap.xml', '\n'.join(sm) + '\n')
    print(f'{len(gurls)} guide pages, {sum(1 for p in pages if not p[4])} indexable landing pages ({sum(1 for p in pages if p[4])} noindex), {len(urls)} sitemap URLs')
if __name__ == '__main__': main()
