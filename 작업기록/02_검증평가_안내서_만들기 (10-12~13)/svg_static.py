"""<style> 클래스를 각 요소의 style 속성으로 옮기고 애니메이션을 지운 정지 SVG를 만든다.
(claude.ai 슬라이드의 이미지 저장소는 <style>과 애니메이션을 지우기 때문)"""
import re, sys
from pathlib import Path

DROP = ("animation", "transform-origin", "transform-box")

def parse_rules(css):
    css = re.sub(r"@keyframes[^{]*\{(?:[^{}]*\{[^{}]*\})*[^{}]*\}", "", css)
    css = re.sub(r"@media[^{]*\{(?:[^{}]*\{[^{}]*\})*[^{}]*\}", "", css)
    rules = []
    for sel, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
        decls = [d.strip() for d in body.split(";") if d.strip() and not d.strip().startswith(DROP)]
        for s in sel.split(","):
            rules.append((s.strip(), decls))
    return rules

def convert(svg):
    m = re.search(r"<style>(.*?)</style>", svg, re.S)
    rules = parse_rules(m.group(1)) if m else []
    svg = re.sub(r"<style>.*?</style>\s*", "", svg, flags=re.S)
    # SMIL로 움직이는 요소는 정지 화면에서 엉뚱한 곳에 남으므로 지운다
    svg = re.sub(r"<circle[^>]*>\s*<animateMotion[^>]*/>\s*</circle>\s*", "", svg)
    svg = re.sub(r"<g>(?:(?!</?g[ >]).)*?<animateMotion[^>]*/>\s*</g>\s*", "", svg, flags=re.S)
    svg = re.sub(r"<g opacity=\"0\">.*?</g>\s*", "", svg, flags=re.S)

    def fix(mt):
        tag, attrs, close = mt.group(1), mt.group(2), mt.group(3)
        classes = re.search(r'\sclass="([^"]*)"', attrs)
        cls = classes.group(1).split() if classes else []
        decls = []
        for sel, d in rules:
            if sel == tag or (sel.startswith(".") and sel[1:] in cls):
                decls += d
        own = re.search(r'\sstyle="([^"]*)"', attrs)
        if own:
            decls += [x.strip() for x in own.group(1).split(";") if x.strip()]
        attrs = re.sub(r'\s(class|style)="[^"]*"', "", attrs)
        if decls:
            attrs += ' style="' + ";".join(decls).replace('"', "'") + '"'
        return f"<{tag}{attrs}{close}>"

    return re.sub(r"<(?!/)(\w+)((?:\s+[\w:-]+=\"[^\"]*\")*)\s*(/?)>", fix, svg)

src, out = Path(sys.argv[1]), Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
for name in sys.argv[3:]:
    t = convert((src / f"{name}.svg").read_text(encoding="utf-8"))
    (out / f"{name}.svg").write_text(t, encoding="utf-8")
    print(name, "class=" in t, "<style" in t, "animate" in t)
