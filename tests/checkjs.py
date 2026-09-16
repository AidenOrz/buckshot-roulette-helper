# -*- coding: utf-8 -*-
"""语法检查仓库内各页面的内联 <script>（需要 pip install esprima）。

用法：python tests/checkjs.py
结果写入 tests/syntax.log，全部通过时输出 ALL_OK。
"""
import io, os, re, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 仓库根目录
out = []
try:
    import esprima
except ImportError:
    out.append("NO_ESPRIMA")
    io.open(os.path.join(BASE, "tests", "syntax.log"), "w", encoding="utf-8").write("\n".join(out))
    sys.exit(2)

ok_all = True
for name in ("versus.html", "versus-ai.html", "tracker.html"):
    p = os.path.join(BASE, name)
    with io.open(p, encoding="utf-8") as f:
        s = f.read()
    blocks = re.findall(r"<script>([\s\S]*?)</script>", s)
    if not blocks:
        out.append("%s: NO SCRIPT BLOCK" % name)
        ok_all = False
        continue
    for i, code in enumerate(blocks):
        try:
            esprima.parseScript(code)
            out.append("%s [script %d]: OK (%d chars)" % (name, i, len(code)))
        except Exception as e:
            ok_all = False
            out.append("%s [script %d]: SYNTAX ERROR -> %s" % (name, i, e))

# 额外自查：ic() 用到的每个图标 key 必须在 ICONPATHS 里存在
for name in ("versus.html", "versus-ai.html"):
    with io.open(os.path.join(BASE, name), encoding="utf-8") as f:
        s = f.read()
    for k in ("cigarette", "pill", "cuff", "phone", "mag", "inv", "beer", "adr", "dtrg", "gear"):
        if ("ic('%s')" % k) in s and (k + ":'") not in s:
            ok_all = False
            out.append("%s: MISSING ICON for '%s'" % (name, k))
out.append("ALL_OK" if ok_all else "HAS_ERRORS")

with io.open(os.path.join(BASE, "tests", "syntax.log"), "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("checked")
