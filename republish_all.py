#!/usr/bin/env python3
"""批量重新生成 18 期报告的 HTML（附录已删除后），并重建 index。"""
import sys
from pathlib import Path

ROOT = Path("/Users/maomao/code/web3/us-stock-blog")
sys.path.insert(0, str(ROOT))
import publish  # noqa

DATES = [
    "2026-09-21", "2026-09-22", "2026-09-23", "2026-09-24", "2026-09-25",
    "2026-09-26", "2026-09-27", "2026-09-28", "2026-09-29", "2026-09-30",
    "2026-10-01", "2026-10-02", "2026-10-03", "2026-10-04", "2026-10-05",
    "2026-10-06", "2026-10-07", "2026-10-08",
]

REPORTS_DIR = ROOT / "reports"

for d in DATES:
    md = REPORTS_DIR / f"{d}.md"
    if not md.exists():
        print("缺文件:", md)
        continue
    label = d.replace("-", ".")
    body = publish.render_report_md_to_html(md.read_text(encoding="utf-8"))
    html_path = REPORTS_DIR / f"{d}.html"
    html_path.write_text(publish.build_report_page(label, body), encoding="utf-8")
    print(f"重新生成 {d}.html  ({html_path.stat().st_size} bytes)")

# 重建 index
entries = []
for p in sorted(REPORTS_DIR.glob("*.html"), reverse=True):
    entries.append((p.stem.replace("-", "."), f"reports/{p.name}"))
publish.INDEX_PATH.write_text(publish.build_index_page(entries), encoding="utf-8")
print(f"\n索引重建完成：{len(entries)} 期")
