#!/usr/bin/env python3
"""Japanese renderings of recipe fields that otherwise fall back to English (metric_en, en.*).

The JA README, recipe pages and hardware pages prefer a Japanese metric: a curated
`metric_ja` if present, otherwise the Chinese `metric` with a glossary applied. English
`metric_en` is the last resort and is also run through the glossary so short labels such
as "public receipt" or "promo post" are not left in English."""
import re

# Longest phrases first. Applied to the Chinese metric (and to English as a fallback).
ZH_JA = [
    ('图像与', '画像と'), ('与 Q6', 'と Q6'),
    ('张的', '枚の'), ('张参考', '枚の参考'),
    ('预热相对', 'ウォームに対し'), ('预热', 'ウォーム'),
    ('文本编码', 'テキスト符号化'),
    ('无逐次原始文件', '逐次の生ファイルなし'), ('无逐次原始数据', '逐次の生データなし'),
    ('没有逐次原始数据', '逐次の生データなし'), ('无原始日志', '生ログなし'),
    ('同时处理的请求数未写', '同時リクエスト数は未記載'),
    ('显存是否常驻原文未写', '常駐かどうかは原文に記載なし'),
    ('同机同种子同分辨率对照', '同一マシン・同一シード・同一解像度の対照'),
    ('六项门槛全部通过', '6 つの基準をすべて満たす'),
    ('按启动文件原样启动服务器后跑', '起動ファイルどおりにサーバーを起動して測定'),
    ('和固定版本的启动文件', 'と固定版の起動ファイル'),
    ('提示能找回其中的代码', 'プロンプトからそのコードを復元できる'),
    ('与配方哈希一致', 'レシピのハッシュと一致'),
    ('在该注册表提了', 'そのレジストリに提出'),
    ('不作单流主值', 'シングルストリームの主値にしない'),
    ('峰值进程占用中位', 'ピークプロセス使用量の中央値'),
    ('峰值进程占用', 'ピークプロセス使用量'),
    ('受控测试中位', '管理テストの中央値'), ('受控测试', '管理テスト'),
    ('计时含文本编码', '計測にはテキスト符号化を含む'),
    ('仓库附', 'リポジトリに添付'),
    ('不另开行', '別行にしない'),
    ('手写提示', '手書きプロンプト'),
    ('无局部重绘', 'インペイントなし'), ('无放大', 'アップスケールなし'),
    ('单种子', '単一シード'),
    ('厂商宣称', 'ベンダー公称'), ('公开回执', '公開の領収'), ('宣传帖', '宣伝投稿'),
    ('整首歌', '曲全体'), ('基础模型', 'ベースモデル'),
    ('不完全一致', '完全には一致しない'),
    ('另一用户预热后', '別の利用者はウォームアップ後'),
    ('另一用户', '別の利用者'), ('预热后', 'ウォームアップ後'),
    ('预热墙钟', 'ウォーム時の実時間'),
    ('无绝对时间', '絶対時間の記載なし'),
    ('端到端', 'エンドツーエンド'), ('含音频', '音声あり'),
    ('带声音', '音声付き'), ('视频+音频', '動画+音声'),
    ('冷启动', 'コールドスタート'),
    ('一次生成', '一回で生成'), ('口型视频', 'リップシンク動画'),
    ('衔接片段', 'つなぎクリップ'),
    ('稠密基线', '密なベースライン'), ('无 CFG', 'CFG なし'),
    ('论文称', '論文の公称'),
    ('稳态，不含', '定常状態、含まず'), ('稳态', '定常状態'),
    ('峰值显存', 'ピーク VRAM'), ('峰值预留', 'ピーク予約'),
    ('峰值内存', 'ピークメモリ'),
    ('只作备注', '備考のみ'), ('作主值', 'を主値とする'),
    ('不作主值', '主値にしない'),
    ('记为宣称', '公称とする'), ('记为实测', '実測とする'),
    ('降为宣称', '公称に落とす'),
    ('源修订', 'ソースリビジョン'),
    ('原生精度', 'ネイティブ精度'), ('常驻原生', '常駐ネイティブ'),
    ('常驻', '常駐'), ('官方 cookbook', '公式 cookbook'),
    ('官方', '公式'), ('同表编辑', '同表の編集'),
    ('同表', '同じ表'), ('同卡', '同じカード'),
    ('同一对照里', 'その対照では'), ('主表', '主表'),
    ('需至少约', '少なくとも約'),
    ('可用（', '利用可能（'),
    ('单流', 'シングルストリーム'),
    ('投机解码', '投機的デコード'),
    ('思考关', '思考オフ'), ('思考开', '思考オン'),
    ('预填充', 'プリフィル'), ('预填约', 'プリフィル約'), ('预填', 'プリフィル'),
    ('解码约', 'デコード約'), ('解码中位', 'デコード中央値'), ('解码', 'デコード'),
    ('读入', '読み込み'), ('生成', '生成'),
    ('中位数', '中央値'), ('次中位数', '回の中央値'), ('次中位', '回の中央値'),
    ('中位', '中央値'),
    ('每张', '1 枚あたり'), ('张/小时', '枚/時'),
    (' / 张', ' / 枚'), ('/ 张', '/ 枚'), ('/张', '/枚'),
    ('张（', '枚（'),
    (' / 首', ' / 曲'), ('/ 首', '/ 曲'),
    ('功耗', '消費電力'), ('能耗', 'エネルギー'),
    ('分钟', '分'),
    (' 分 ', ' 分 '),  # keep
    ('约 ', '約 '),
    ('较弱 GPU', 'より弱い GPU'),
    ('含 MP4 导出', 'MP4 書き出しを含む'),
    ('不含 MP4 导出', 'MP4 書き出しを含まず'),
    ('导出', '書き出し'),
    ('基线', 'ベースライン'),
    ('作者表', '作者の表'),
    ('首跑', '初回'),
    ('同帖', '同じ投稿'),
    ('同机', '同じマシン'),
    ('权重', '重み'),
    ('合计超过', '合計で超える'),
    ('且该机 RAM 未写', 'かつそのマシンの RAM は未記載'),
    ('原文未写', '原文に未記載'),
    ('版本未写', 'バージョン未記載'),
    ('未写', '未記載'),
    ('未列出', '記載なし'),
    ('未合并', '未統合'),
    ('平均', '平均'),
    ('公布', '公表'),
    ('无 Sol', 'Sol なし'),
    ('质量 ', '品質 '),
    (' 胜', ' 勝ち'),
    ('快约', '約'),
    ('（快 ', '（'),
    ('共 ', '合計 '),
    ('共~', '合計約'),
    (' 段 ', ' セグメント '),
    (' 段×', ' セグメント ×'),
    (' 帧', ' フレーム'),
    ('帧：', 'フレーム：'),
    (' 步', ' ステップ'),
    ('步，', 'ステップ、'),
    ('步：', 'ステップ：'),
    ('步 ', 'ステップ '),
    ('步 CFG', 'ステップ CFG'),
    (' 步', ' ステップ'),
    ('限制', '制限'),
    ('对照', '対照'),
    ('构建', '構築'),
    ('草稿', 'ドラフト'),
    ('配方', 'レシピ'),
    ('请求', 'リクエスト'),
    ('输出', '出力'),
    ('配置', '構成'),
    ('合计', '合計'),
    ('用户', '利用者'),
    ('引擎', 'エンジン'),
    ('上下文', 'コンテキスト'),
    ('代码', 'コード'),
    ('提示', 'プロンプト'),
    ('散文', '散文'),
    ('计数', 'カウント'),
    ('贪心', '貪欲'),
    ('温度', '温度'),
    ('默认', 'デフォルト'),
    ('接受率', '受理率'),
    ('短提示', '短いプロンプト'),
    ('结构化', '構造化'),
    ('加载', '読み込み'),
    ('峰值', 'ピーク'),
    ('图像', '画像'),
    ('视频', '動画'),
    ('歌曲', '曲'),
    ('片段', 'クリップ'),
    ('表：', '表：'),
    ('降到', 'に低下'),
    ('接近', '近い'),
    ('相对', 'に対し'),
    ('去噪', 'デノイズ'),
    ('写 PNG', 'PNG 書き出し'),
    ('更早', 'より前の'),
    ('时间是', '時間は'),
    ('时间为', '時間は'),
    ('编码器', 'エンコーダ'),
    ('编辑', '編集'),
    ('约', '約'),
]

EN_JA = [
    ('public receipt', '公開の領収'),
    ('promo post', '宣伝投稿'),
    ('Whole song', '曲全体'),
    ('whole song', '曲全体'),
    ('vendor claim', 'ベンダー公称'),
    ('per image', '1 枚あたり'),
    (' / image', ' / 枚'),
    ('/ image', '/ 枚'),
    ('images per hour', '枚/時'),
    ('another user', '別の利用者'),
    ('after warm-up', 'ウォームアップ後'),
    ('no absolute times', '絶対時間の記載なし'),
    ('end-to-end', 'エンドツーエンド'),
    ('end to end', 'エンドツーエンド'),
    ('with audio', '音声あり'),
    ('cold start', 'コールドスタート'),
    ('first run', '初回'),
    ('warm wall time', 'ウォーム時の実時間'),
    ('steady state', '定常状態'),
    ('generated in one pass', '一回で生成'),
    ('lip-sync video', 'リップシンク動画'),
    ('per first', ' / 曲'),
    ('About 1 minute', '約 1 分'),
    ('about ', '約 '),
    (' minutes', ' 分'),
    (' minute', ' 分'),
    (' steps', ' ステップ'),
    (' step', ' ステップ'),
    (' peak ', ' ピーク '),
    ('peak ', 'ピーク '),
    (' clip', 'クリップ'),
    ('video', '動画'),
    (' faster', ' 高速'),
    ('without ', 'なし '),
    ('average ', '平均 '),
    ('quality: ', '品質：'),
    (' wins ', ' 勝ち '),
    ('base model', 'ベースモデル'),
    ('median of the last', '直近'),
    ('power ', '消費電力 '),
    ('energy ', 'エネルギー '),
    ('weaker GPU', 'より弱い GPU'),
    ('not listed', '記載なし'),
    ('frames', 'フレーム'),
    ('published ', '公表 '),
    ('Official ', '公式 '),
    ('cookbook', 'cookbook'),
]


def _apply(s, pairs):
    if not s:
        return s
    for a, b in sorted(pairs, key=lambda kv: len(kv[0]), reverse=True):
        s = s.replace(a, b)
    return s


_CJK = re.compile(r'[\u3400-\u9fff]')
# Leftover simplified-only characters that are not used in Japanese.
_SIMPLIFIED = set('这们说时实为对务从无与样产发进过还经开关见让认请读选显传标单张门问间题须记设试详语论谁调质运连适钟错长阅难页顺预领风飞马验级络统维缓据数码显卡张页')


# Same simplified-only set as tests/test_i18n.py: leftover characters on a JA page fail CI.
SIMPLIFIED_ONLY = set('这们说时实为对务从无与样产发进过还经开关见让认请读选显传标单张门问间题须记设试详语论谁调质运连适钟错长阅难页顺预领风飞马验级络统维缓据')
_KANA = re.compile(r'[\u3040-\u30ff]')
_EN_WORD = re.compile(r'\b[a-z]{4,}\b')


def has_simplified(s):
    return any(ch in SIMPLIFIED_ONLY for ch in (s or ''))


def needs_en_mark(s):
    """True when the string is still English prose (no kana, has a 4+ letter English word)."""
    if not s or s.endswith('（英語）') or _KANA.search(s) or has_simplified(s):
        return False
    return bool(_EN_WORD.search(s))


def metric(r):
    """Japanese metric text for README, recipe pages and hardware pages.

    Prefer metric_ja, then a fully converted Chinese metric (no simplified-only characters).
    If the glossary cannot finish the Chinese text, use metric_en (also glossary-applied) so
    JA pages stay language-pure; the caller may add the （英語） mark."""
    if r.get('metric_ja'):
        return r['metric_ja']
    zh = r.get('metric')
    if zh:
        out = _apply(zh, ZH_JA)
        if not has_simplified(out):
            return out
    en = r.get('metric_en')
    if en:
        return _apply(en, EN_JA)
    return None
