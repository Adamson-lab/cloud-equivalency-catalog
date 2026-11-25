"""Generate a single-file, dependency-free searchable HTML site from the catalog."""
from __future__ import annotations

import json
from pathlib import Path

from .loader import PROVIDER_LABELS, PROVIDERS

TEMPLATE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Cloud Equivalency Catalog: AWS / Azure / GCP / OCI</title>
<style>
:root{--bg:#fff;--fg:#14181f;--mut:#5b6472;--line:#d9dee6;--card:#f6f8fb;--exact:#0a7d3b;--close:#1f5fbf;--partial:#a15c00;--none:#b3261e}
@media (prefers-color-scheme:dark){:root{--bg:#0f1319;--fg:#e8ecf2;--mut:#9aa5b5;--line:#2a3340;--card:#171d26;--exact:#4cd98a;--close:#7fb2ff;--partial:#ffb454;--none:#ff8a80}}
*{box-sizing:border-box}body{margin:0;font:15px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;background:var(--bg);color:var(--fg)}
header,main{max-width:1200px;margin:0 auto;padding:16px}
h1{font-size:22px;margin:8px 0 4px}p.sub{color:var(--mut);margin:0 0 12px}
.controls{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0}
input,select{padding:8px 10px;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--fg);font:inherit}
input{flex:1;min-width:220px}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:8px;margin:12px 0}
.stat{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px}.stat b{font-size:20px}
.wrap{overflow-x:auto;border:1px solid var(--line);border-radius:10px}
table{border-collapse:collapse;width:100%;min-width:900px}th,td{padding:8px 10px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
th{background:var(--card);position:sticky;top:0}
.tag{display:inline-block;font-size:11px;font-weight:600;border:1px solid currentColor;border-radius:999px;padding:0 6px;margin-left:6px}
.exact{color:var(--exact)}.close{color:var(--close)}.partial{color:var(--partial)}.none{color:var(--none)}
.note{display:block;color:var(--mut);font-size:12px;margin-top:2px}.cat{color:var(--mut);font-size:12px}
footer{color:var(--mut);font-size:12px;padding:16px;max-width:1200px;margin:0 auto}
</style></head><body>
<header><h1>Cloud Equivalency Catalog</h1>
<p class="sub">Vendor-neutral mapping of AWS, Azure, Google Cloud and Oracle Cloud services. Fit labels are text, not just color: exact / close / partial / none.</p>
<div class="controls"><input id="q" type="search" placeholder="Search a capability or any service name (e.g. S3, BigQuery, Key Vault)" aria-label="Search">
<select id="cat" aria-label="Category"><option value="">All categories</option></select>
<select id="fit" aria-label="Filter by fit"><option value="">Any fit</option><option value="gap">Has a gap (partial/none)</option><option value="none">Has no equivalent</option></select></div>
<div class="stats" id="stats"></div></header>
<main><div class="wrap"><table><thead><tr><th>Capability</th>__HEAD__<th>Lock-in / Migration</th></tr></thead><tbody id="rows"></tbody></table></div></main>
<footer>Generated from YAML in <code>catalog/</code>. Product names and availability change; verify against vendor documentation before decisions. Not affiliated with any cloud vendor.</footer>
<script>
const DATA=__DATA__,P=__PROVIDERS__,L=__LABELS__;
const $=id=>document.getElementById(id);
const cats=[...new Map(DATA.map(e=>[e.category,e.category_title]))];
cats.forEach(([k,v])=>{const o=document.createElement('option');o.value=k;o.textContent=v;$('cat').appendChild(o)});
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function stats(){const w={exact:1,close:.75,partial:.4,none:0};
 $('stats').innerHTML=P.map(p=>{const s=DATA.reduce((a,e)=>a+w[e.offerings[p].fit],0)/DATA.length*100;
 return `<div class="stat"><div>${L[p]}</div><b>${s.toFixed(1)}</b> parity/100</div>`}).join('')+`<div class="stat"><div>Capabilities</div><b>${DATA.length}</b></div>`}
function render(){const q=$('q').value.toLowerCase(),c=$('cat').value,f=$('fit').value;
 const rows=DATA.filter(e=>{
  if(c&&e.category!==c)return false;
  const hay=(e.name+' '+e.description+' '+P.map(p=>e.offerings[p].service).join(' ')).toLowerCase();
  if(q&&!hay.includes(q))return false;
  const fits=P.map(p=>e.offerings[p].fit);
  if(f==='gap'&&!fits.some(x=>x==='partial'||x==='none'))return false;
  if(f==='none'&&!fits.includes('none'))return false;return true});
 $('rows').innerHTML=rows.map(e=>`<tr><td><b>${esc(e.name)}</b><span class="cat">${esc(e.category_title)}</span><span class="note">${esc(e.description)}</span></td>`+
  P.map(p=>{const o=e.offerings[p];return `<td>${esc(o.service)}<span class="tag ${o.fit}">${o.fit}</span>${o.notes?`<span class="note">${esc(o.notes)}</span>`:''}</td>`}).join('')+
  `<td>Lock-in: <b>${e.lock_in_risk}</b><br>Migration: <b>${e.migration_complexity}</b>${e.exec_note?`<span class="note">${esc(e.exec_note)}</span>`:''}</td></tr>`).join('')||'<tr><td colspan="6">No matches.</td></tr>'}
['q','cat','fit'].forEach(id=>$(id).addEventListener('input',render));stats();render();
</script></body></html>
"""


def build_site(entries: list[dict], out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    head = "".join(f"<th>{PROVIDER_LABELS[p]}</th>" for p in PROVIDERS)
    # Escape "</" so catalog text can never terminate the inline <script>.
    data = json.dumps(entries, ensure_ascii=False).replace("</", "<\\/")
    html = (
        TEMPLATE.replace("__HEAD__", head)
        .replace("__DATA__", data)
        .replace("__PROVIDERS__", json.dumps(list(PROVIDERS)))
        .replace("__LABELS__", json.dumps(PROVIDER_LABELS))
    )
    index = out_dir / "index.html"
    index.write_text(html, encoding="utf-8")
    (out_dir / "catalog.json").write_text(json.dumps(entries, indent=2, ensure_ascii=False), encoding="utf-8")
    (out_dir / ".nojekyll").write_text("", encoding="utf-8")
    return index
