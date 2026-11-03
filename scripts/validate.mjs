// Usage: node scripts/validate.mjs  — minimal validator against schema/recipe.schema.json (no deps)
import fs from 'fs';
const S=JSON.parse(fs.readFileSync(new URL('../schema/recipe.schema.json',import.meta.url)));
const D=JSON.parse(fs.readFileSync(new URL('../data/recipes.json',import.meta.url)));
let err=0;const ids=new Set();
const typeOk=(v,t)=>[].concat(t).some(x=>x==='null'?v===null:x==='number'?typeof v==='number':x==='array'?Array.isArray(v):typeof v===x);
const TAGS=new Set(['1bit','ternary','2bit','3bit','4bit','5bit','6bit','8bit','bf16','MoE','dense','long-context','speculative','MTP','multi-GPU','offload','few-step','abliterated','gpu-unlock']);
for(const r of D){
  const e=m=>{err++;console.error(`[${r.id}] ${m}`)};
  if(ids.has(r.id))e('duplicate id');ids.add(r.id);
  for(const k of S.required) if(r[k]==null||r[k]==='')e(`missing ${k}`);
  for(const k of Object.keys(r)){const p=S.properties[k];if(!p){e(`unknown field ${k}`);continue}
    if(p.enum&&!p.enum.includes(r[k]))e(`${k} not in enum: ${r[k]}`);
    if(p.type&&!typeOk(r[k],p.type))e(`${k} wrong type`);
    if(p.pattern&&typeof r[k]==='string'&&!new RegExp(p.pattern).test(r[k]))e(`${k} pattern`);
    if(p.items?.pattern&&Array.isArray(r[k]))for(const x of r[k])if(typeof x!=='string'||!new RegExp(p.items.pattern).test(x))e(`${k} item pattern: ${x}`);}
  if(Array.isArray(r.tags)){for(const t of r.tags)if(!TAGS.has(t))e(`unknown tag ${t}`);if(new Set(r.tags).size!==r.tags.length)e('duplicate tag');}
  if(/^其他|^同上$/.test(r.engine))e(`engine not normalized: ${r.engine}`);
  if(r.engine_note!=null&&r.engine_note===r.engine)e('engine_note equals engine');
  if(r.category!=='text'&&r.tags&&(r.tags.includes('MoE')||r.tags.includes('dense')))e('MoE/dense tag on non-text');
  if(r.hardware_cost_usd!=null&&r.hardware_cost_usd>30000)console.warn(`[${r.id}] warn: cost > $30k`);
}
const SRCF=JSON.parse(fs.readFileSync(new URL('../data/sources.json',import.meta.url)));const SRC=SRCF.sources;
if(!/^\d{4}-\d{2}-\d{2}$/.test(SRCF.updated||'')){err++;console.error('sources.json: updated must be YYYY-MM-DD')}
for(const s of SRC){
  const e=m=>{err++;console.error(`[source ${s.name}] ${m}`)};
  for(const k of ['name','platform','url','focus','why','sample_post']) if(typeof s[k]!=='string'||!s[k])e(`missing ${k}`);
  if(!['A','B','C'].includes(s.tier))e(`tier not in A/B/C: ${s.tier}`);
  if(s.followers!=null&&typeof s.followers!=='number')e('followers must be number or null');
}
console.log(err?`✗ ${err} errors`:`✓ ${D.length} recipes, ${SRC.length} sources valid`);process.exit(err?1:0);
