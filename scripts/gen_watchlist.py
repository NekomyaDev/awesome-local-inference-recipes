#!/usr/bin/env python3
import json
from pathlib import Path
R = Path(__file__).resolve().parent.parent
SOURCES, WATCH = R/'data/sources.json', R/'docs/internal/watchlist.md'
TIER_ORDER = {'A': 0, 'B': 1, 'C': 2}
# Internal maintainer list. The source data (focus/why) is Chinese, so the whole page is Chinese.
HEADER = ('# 重点跟踪来源\n\n'
          '由 `scripts/gen_watchlist.py` 根据 `data/sources.json`（{updated}）生成。'
          'A 级 = 参数具体且可复现；B 级 = 有具体数字但条件不全；C 级 = 多为转述或覆盖面窄。\n\n'
          '| 等级 | 名称 | 平台 | 关注者 | 关注点 | 理由 | 示例 |\n'
          '|---|---|---|---|---|---|---|\n')

def cell(v):
    return str(v).replace('|', '\\|').replace('\n', ' ')

def link_target(url):
    return cell(url).replace(' ', '%20').replace('(', '%28').replace(')', '%29')

def row(s):
    followers = '—' if s.get('followers') is None else s['followers']
    return (f"| {cell(s['tier'])} | [{cell(s['name'])}]({link_target(s['url'])}) | {cell(s['platform'])} | {followers} | "
            f"{cell(s['focus'])} | {cell(s['why'])} | [示例帖]({link_target(s['sample_post'])}) |")

def render(sources):
    ordered = sorted(sources['sources'], key=lambda s: TIER_ORDER[s['tier']])
    return HEADER.format(updated=sources['updated']) + '\n'.join(row(s) for s in ordered) + '\n'

if __name__ == '__main__':
    WATCH.write_text(render(json.loads(SOURCES.read_text(encoding='utf-8'))), encoding='utf-8')
    print(f'written {WATCH.relative_to(R)}')
