// Shared by the home page and the explorer: what a row's hardware_cost_usd actually prices, so $/tok/s is only ranked like-for-like.
// 'gpu' = card price only (cost text says 仅显卡, or a discrete-card family: NVIDIA consumer / AMD cards / used datacenter / named workstation cards);
// 'sys' = whole machine (Mac, DGX Spark, Strix Halo / Ryzen AI Max mini PCs, phones/tablets, rows priced as 整机);
// null = no price, or a comparison row ("A / B", "A vs B") whose single price can't be attributed.
(function(){
const DISCRETE=['NVIDIA 消费级','AMD','二手数据中心卡'],WHOLE=['Mac','DGX Spark'];
const SYS=/Strix Halo|Ryzen AI Max|Mac\b|Mac mini|iPhone|iPad|Samsung|AI TOP ATOM|GB10/i,CARD=/RTX|Radeon|\bRX\s*\d|R9700|Tesla|CMP|\bArc\b|\bMI\d{2,3}\b|V100|P40/i;
window.costKind=r=>{r=r._src||r;if(r.hardware_cost_usd==null)return null;const h=r.hardware||'',t=r.hardware_cost_text||'';
 if(/\s\/|\/\s|\svs\s/i.test(h))return null;  // 'A / B', 'A（…）/ +B'; keeps 'DDR4/5'
 if(t.includes('仅显卡'))return 'gpu';
 if(WHOLE.includes(r.hardware_family)||t.includes('整机')||SYS.test(h))return 'sys';
 if(DISCRETE.includes(r.hardware_family)||CARD.test(h))return 'gpu';
 return 'sys'};
// Rows whose metric says 自称 ("self-reported") are filed as 实测 but have no log behind them; keep them out of "measured" rankings until the data is fixed.
window.selfReported=r=>/自称/.test((r._src||r).metric||'');
// Home-page "Popular on X": likes + 3×reposts, one card per post, 宣称 (claimed) rows left out.
window.hotPosts=(D,n)=>{const seen=new Set();return D.filter(r=>r.x_post&&r.source_level!='宣称').sort((a,b)=>(b.x_post.likes+3*b.x_post.reposts)-(a.x_post.likes+3*a.x_post.reposts)).filter(r=>!seen.has(r.source_url)&&seen.add(r.source_url)).slice(0,n)};
const NON_ZH_TEXT_FIELDS=['quant','model','hardware','context','concurrency','engine_note','hardware_cost_text','source_note','launch_command'];
const CJK=/[\u3000-\u303f\u3040-\u30ff\u3400-\u9fff\uff00-\uffef]/;
const GLOSS=[['草稿','draft'],['实测','measured'],['自称','self-reported'],['帖文','post'],['原帖','original post'],['并发','concurrent'],['显存','VRAM'],['内存','RAM'],['预填充','prefill'],['计算值','computed'],['仅显卡','card only'],['整机','whole system'],['二手','used'],['翻新','refurbished'],['上下文','context'],['窗口','window'],['峰值','peak'],['约','≈'],['见','see '],['路','streams'],['卡','card'],['；','; '],['，',', '],['（',' ('],['）',')'],['：',': '],['、',', '],['～','~']];
window.glossLatin=s=>{if(typeof s!='string'||!CJK.test(s))return s;for(const[a,b]of GLOSS)s=s.split(a).join(b);return s.replace(/[\u3000-\u303f\u3040-\u30ff\u3400-\u9fff\uff00-\uffef]+/g,'').replace(/\s{2,}/g,' ').trim()};
// JA has no translated data fields yet: label English data text so it is not read as a translation (same rule as gen_readme.mark_ja_en).
const JA_EN_FIELDS=['metric','engine_note','context','concurrency','source_note'];
const markJaEn=s=>typeof s=='string'&&s&&!s.endsWith('（英語）')&&!/[\u3040-\u30ff\u3400-\u9fff]/.test(s)&&/\b[a-z]{4,}\b/.test(s)?s+'（英語）':s;
window.localizeRecipe=(r,lang)=>{if(lang==='zh-CN')return r;const o={...r,_src:r};for(const k of NON_ZH_TEXT_FIELDS)o[k]=r.en&&r.en[k]!=null?r.en[k]:glossLatin(r[k]);o.metric=r.metric_en||glossLatin(r.metric);if(lang==='ja')for(const k of JA_EN_FIELDS)o[k]=markJaEn(o[k]);return o};
})();

const DISPLAY_VALUES={'zh-CN':{Unspecified:'未注明',Other:'其他'},ja:{Unspecified:'未指定',Other:'その他'}};
window.displayValue=(x,lang)=>((DISPLAY_VALUES[lang]||{})[x])||x;
