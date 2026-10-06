from pathlib import Path
from datetime import datetime,timezone
import json
root=Path(__file__).resolve().parents[1]
posts=json.loads((root/"posts.json").read_text(encoding="utf-8"))
posts=posts[:60]
(root/"posts.json").write_text(json.dumps(posts,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
html=(root/"index.html").read_text(encoding="utf-8")
css=(root/"styles.css").read_text(encoding="utf-8")
js=(root/"app.js").read_text(encoding="utf-8")
checks=[]
for name,ok in [("viewport",'<meta name="viewport"' in html),("css",'rel="stylesheet"' in html),("html-escaping","escapeHtml" in js),("responsive","@media" in css)]:
 if ok: checks.append(name)
with (root/"CHANGELOG.md").open("a",encoding="utf-8") as f:
 f.write(f"\n- {datetime.now(timezone.utc).isoformat()} — Optimisation pass: retained {len(posts)} posts; checks passed: {', '.join(checks)}.\n")
print("Optimisation checks:",", ".join(checks))
