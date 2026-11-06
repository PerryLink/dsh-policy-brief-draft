#!/usr/bin/env python3
"""README visuals for dsh-policy-brief-draft — read off the plugin's real pipeline.

Two figures, both derived from the shipped material:

  hero 1440x576  (Pillow -> webp; zh/en x light/dark = 4 files)
      One element checklist (header + row 1 of the PB-001 fixture) with its empty
      point cell, the three evidence-kind ceilings the rule pack enforces
      (direct <= error, derived-from-principle <= warn, institutional-configuration
      <= info), and the finding slip that a real quickstart run prints:
      PB-001 / row 1 / point blank, skipped 2 (PB-005 unset maxDays, PB-006 no
      triggering row).

  flow 1100x660  (hand-written SVG; light/dark = 2 files)
      The check bench, not a five-box chain: two input scopes (header / rows[])
      feed 8 rules stacked under their three severity ceilings, and the report
      leaves on two channels — issues[] located by row + column, and skipped[]
      with a reason. Command-surface tokens only, so all five READMEs share it.

Every value below is quoted from the repository, never invented:
  samples/quickstart/input/PB-001-unsafe.json   title, recipient, row 1 values
  samples/quickstart/expected/result.json       1 issue, error 1, skipped 2
  tests/fixtures/PB-001/PB-001-unsafe.json      same register shape
  rules/policy-brief-draft.yaml                 8 rules, their kind and severity
  a run of lib/index.mjs on the quickstart      skipped reasons PB-005 / PB-006

Run once:  python scripts/gen-readme-assets.py
Requires:  Pillow + Windows fonts msyh.ttc / msyhbd.ttc / consola.ttf.
"""
from __future__ import annotations

import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "assets")

FONT_CJK = r"C:\Windows\Fonts\msyh.ttc"
FONT_CJK_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"
FONT_MONO = r"C:\Windows\Fonts\consola.ttf"
FONT_MONO_BOLD = r"C:\Windows\Fonts\consolab.ttf"
for _p in (FONT_CJK, FONT_CJK_BOLD, FONT_MONO, FONT_MONO_BOLD):
    if not os.path.exists(_p):
        raise SystemExit(f"FATAL: font missing: {_p}")

FONT_FILES = {"cjk": FONT_CJK, "cjk_bold": FONT_CJK_BOLD,
              "mono": FONT_MONO, "mono_bold": FONT_MONO_BOLD}
_SCRATCH = ImageDraw.Draw(Image.new("RGB", (8, 8)))

RADIUS = 20
SHADOW = 24

SKIN = {
    "light": dict(
        bg_from="#f9f6fd", bg_to="#e4eaf8",
        card="#ffffff", edge="#e6e2ef",
        text="#141419", sub="#4d5261", faint="#8f94a4",
        accent="#4B67B4", band="#f5f2fb", pill="#ece7f9",
        grid="#e7e4f0", mark="#b45309", mark_bg="#fdf3e9",
        err="#b3261e", err_bg="#fdeceb",
        warn="#b45309", warn_bg="#fdf3e9",
        info="#4B67B4", info_bg="#ecebf9",
        shadow=(32, 26, 64), shadow_hex="#16122c", glow="#7a68c9",
    ),
    "dark": dict(
        bg_from="#131a2a", bg_to="#0c1016",
        card="#1b2231", edge="#2e374b",
        text="#f0f3f9", sub="#a8b1c4", faint="#737b8d",
        accent="#8496f5", band="#202839", pill="#242d42",
        grid="#262f42", mark="#d9a441", mark_bg="#2a2216",
        err="#ff7b72", err_bg="#2c1b1b",
        warn="#d29922", warn_bg="#2a2216",
        info="#8496f5", info_bg="#242d42",
        shadow=(0, 0, 0), shadow_hex="#000000", glow="#8496f5",
    ),
}


# --------------------------------------------------------------------- helpers --
def font(size: int, kind: str = "cjk") -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_FILES[kind], int(size))


def hx(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def tw(text: str, size: int, kind: str = "cjk") -> float:
    return _SCRATCH.textlength(text, font=font(size, kind))


def fit(text: str, kind: str, maxw: float, hi: int, lo: int, label: str) -> int:
    """Largest integer size in [lo, hi] whose single line fits maxw."""
    for size in range(hi, lo - 1, -1):
        if tw(text, size, kind) <= maxw:
            return size
    raise SystemExit(f"FATAL: {label} does not fit {maxw:.0f}px even at {lo}px: {text!r}")


def fit_lines(lines, kind: str, maxw: float, hi: int, lo: int, label: str) -> int:
    for size in range(hi, lo - 1, -1):
        if all(tw(line, size, kind) <= maxw for line in lines):
            return size
    raise SystemExit(f"FATAL: {label} does not fit {maxw:.0f}px even at {lo}px")


def require_w(text: str, size: int, kind: str, maxw: float, label: str) -> None:
    width = tw(text, size, kind)
    if width > maxw:
        raise SystemExit(f"FATAL: {label} overflows ({width:.0f} > {maxw:.0f}px): {text!r}")


def truncate(text: str, size: int, kind: str, maxw: float) -> str:
    if tw(text, size, kind) <= maxw:
        return text
    cut = text
    while cut and tw(cut + "…", size, kind) > maxw:
        cut = cut[:-1]
    if " " in cut:
        head = cut.rsplit(" ", 1)[0].rstrip(" ,;、，：:")
        if head and tw(head + "…", size, kind) <= maxw:
            return head + "…"
    return cut + "…"


def gradient(w: int, h: int, c1: str, c2: str) -> Image.Image:
    base = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(base)
    a, b = hx(c1), hx(c2)
    for y in range(h):
        t = 0.18 * (y / h) + 0.82 * (y / h) ** 1.35
        draw.line([(0, y), (w, y)],
                  fill=tuple(int(p + (q - p) * t) for p, q in zip(a, b)))
    return base


def glow(img: Image.Image, cx: int, cy: int, r: int, color: tuple, alpha: int = 40) -> Image.Image:
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    for i in range(9, 0, -1):
        rr = r * i / 9
        draw.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                     fill=color + (int(alpha * (1 - i / 10)),))
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")


def card(img: Image.Image, box, s: dict, radius: int = RADIUS, shadow: int = SHADOW,
         fill: str | None = None) -> Image.Image:
    x0, y0, x1, y1 = box
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    for i in range(shadow, 0, -3):
        sd.rounded_rectangle([x0 - i // 5, y0 + i // 2, x1 + i // 5, y1 + i],
                             radius=radius + i // 5,
                             fill=s["shadow"] + (int(9 * (1 - i / shadow)),))
    base = Image.alpha_composite(img.convert("RGBA"), sh.filter(ImageFilter.GaussianBlur(10)))
    draw = ImageDraw.Draw(base)
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius,
                           fill=hx(fill or s["card"]), outline=hx(s["edge"]), width=1)
    return base.convert("RGB")


def pill(img: Image.Image, xy, text: str, s: dict, size: int = 17,
         fg: str | None = None, bg: str | None = None) -> int:
    x, y = xy
    w = tw(text, size, "cjk") + size * 1.25
    h = size + 18
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([x, y, x + w, y + h], radius=h / 2,
                           fill=hx(bg or s["pill"]), outline=hx(s["edge"]), width=1)
    draw.text((x + size * 0.625, y + 8), text, font=font(size, "cjk"), fill=hx(fg or s["accent"]))
    return int(w)


def chip(img: Image.Image, xy, text: str, s: dict, size: int = 11,
         fg: str | None = None, bg: str | None = None) -> int:
    x, y = xy
    w = tw(text, size, "cjk") + 18
    h = size + 14
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([x, y, x + w, y + h], radius=h / 2,
                           fill=hx(bg or s["band"]), outline=hx(s["edge"]), width=1)
    draw.text((x + 9, y + 6), text, font=font(size, "cjk"), fill=hx(fg or s["sub"]))
    return int(w)


def runs(draw: ImageDraw.ImageDraw, xy, parts, s: dict) -> int:
    """Draw (text, size, kind, colour) runs left to right; return the width used."""
    x, y = xy
    start = x
    for text, size, kind, color in parts:
        draw.text((x, y), text, font=font(size, kind), fill=hx(color or s["text"]))
        x += tw(text, size, kind)
    return int(x - start)


# ------------------------------------------------------------------------ hero --
# Sample row 1 and the finding are from the PB-001 fixture + a real quickstart run.
HERO = {
    "zh": dict(
        kicker="DeepSeek Harness 插件 · 核对器",
        value=["要素齐备与日期自洽，", "差异落到行号与栏名。"],
        sub=["读入专报要素核对表（JSON / YAML），套用 PB-001…PB-008 规则包；",
             "只列材料内部能指认的差异；结论留给审核人。"],
        meta="8 条规则 · 3 error / 4 warn / 1 info · 逐字引文与依据类型封顶",
        foot="Apache-2.0 · PerryLink DSH 插件家族 · 社区插件，与 DeepSeek 官方无关",
        reg_title="要素核对表 · rows[]",
        reg_chip="只读",
        reg_head="title · recipient · draftedAt · classification",
        cols=["序号", "章节", "核心观点", "支撑依据", "数据截止"],
        col_w=[38, 76, 122, 232, 112],
        row=["1", "一、现状", "（空）",
             "全国固定资产投资统计月报（2026 年 2 月）显示本领域投资同比增长 3.1%",
             "2026-02-28"],
        empty_idx=2,
        bars=[
            dict(kind="direct", count="4 条", ceiling="封顶 error", key="err",
                 rules=[("PB-001", "核心观点"), ("PB-003", "出处"),
                        ("PB-004", "数据截止"), ("PB-007", "表头两栏")]),
            dict(kind="derived-from-principle", count="3 条", ceiling="封顶 warn", key="warn",
                 rules=[("PB-002", "支撑依据"), ("PB-006", "建议→主体"),
                        ("PB-008", "序号唯一")]),
            dict(kind="institutional-configuration", count="1 条", ceiling="封顶 info", key="info",
                 rules=[("PB-005", "新鲜度窗口")], note="maxDays = 0 ⇒ skipped"),
        ],
        slip=dict(rule="PB-001", sev="error",
                  locator="locator · 第 1 行 / point",
                  found="找到：第 1 行「point」为空",
                  expected="应填：「point」应填写；补填核心观点",
                  skip_head="skipped[] 2",
                  skip=["PB-005 · maxDays 未配置", "PB-006 · 无触发行"],
                  skip_note="空清单 ≠ 没问题"),
    ),
    "en": dict(
        kicker="DeepSeek Harness plugin · checker",
        value=["Every element, every date —", "pinned to row and column."],
        sub=["Reads the element checklist (JSON / YAML) with rule pack PB-001…PB-008;",
             "lists locatable gaps only — no verdict, no network, no model."],
        meta="8 rules · 3 error / 4 warn / 1 info · severity capped by evidence kind",
        foot="Apache-2.0 · PerryLink DSH plugin family · community plugin, not official",
        reg_title="Element checklist · rows[]",
        reg_chip="read-only",
        reg_head="title · recipient · draftedAt · classification",
        cols=["No.", "Section", "Key point", "Evidence", "Data as of"],
        col_w=[38, 86, 122, 222, 112],
        row=["1", "I. Status", "(blank)",
             "National fixed-asset investment monthly report (Feb 2026), investment up 3.1% y/y",
             "2026-02-28"],
        empty_idx=2,
        bars=[
            dict(kind="direct", count="4 rules", ceiling="cap error", key="err",
                 rules=[("PB-001", "point"), ("PB-003", "source"),
                        ("PB-004", "dataAsOf"), ("PB-007", "header")]),
            dict(kind="derived-from-principle", count="3 rules", ceiling="cap warn", key="warn",
                 rules=[("PB-002", "evidence"), ("PB-006", "rec.→owner"),
                        ("PB-008", "sectionNo")]),
            dict(kind="institutional-configuration", count="1 rule", ceiling="cap info", key="info",
                 rules=[("PB-005", "freshness")], note="maxDays = 0 ⇒ skipped"),
        ],
        slip=dict(rule="PB-001", sev="error",
                  locator="locator · row 1 / point",
                  found="Found: row 1 “point” is blank",
                  expected="Expected: “point” should be filled",
                  skip_head="skipped[] 2",
                  skip=["PB-005 · maxDays unset", "PB-006 · no trigger row"],
                  skip_note="empty list ≠ nothing wrong"),
    ),
}


def hero(lang: str, skin: str) -> None:
    s = SKIN[skin]
    Hh = HERO[lang]
    img = gradient(1440, 576, s["bg_from"], s["bg_to"])
    img = glow(img, 1180, 16, 430, hx(s["glow"]), 24 if skin == "light" else 38)
    img = glow(img, 70, 566, 300, hx(s["glow"]), 10 if skin == "light" else 16)
    d = ImageDraw.Draw(img)
    m, col, col_text = 64, 620, 600

    # ---- left column: kicker / title / value / sub / meta / footer -----------
    pill(img, (m, 52), Hh["kicker"], s, size=17)
    d = ImageDraw.Draw(img)
    title_size = fit("dsh-policy-brief-draft", "mono_bold", col, 58, 46, "hero title")
    d.text((m - 2, 114), "dsh-policy-brief-draft",
           font=font(title_size, "mono_bold"), fill=hx(s["text"]))

    value_size = fit_lines(Hh["value"], "cjk_bold", col_text, 40, 30, "hero value")
    for i, line in enumerate(Hh["value"]):
        d.text((m, 204 + i * 58), line, font=font(value_size, "cjk_bold"),
               fill=hx(s["text"]))

    sub_size = fit_lines(Hh["sub"], "cjk", col_text, 22, 16, "hero sub")
    for i, line in enumerate(Hh["sub"]):
        d.text((m + 1, 338 + i * 34), line, font=font(sub_size, "cjk"),
               fill=hx(s["sub"]))

    meta_size = fit(Hh["meta"], "cjk", col_text, 19, 15, "hero meta")
    d.text((m + 1, 432), Hh["meta"], font=font(meta_size, "cjk"), fill=hx(s["faint"]))
    d.line([m + 1, 476, m + col_text - 4, 476], fill=hx(s["grid"]), width=2)
    foot_size = fit(Hh["foot"], "cjk", col_text, 16, 12, "hero footer")
    d.text((m + 1, 490), Hh["foot"], font=font(foot_size, "cjk"), fill=hx(s["faint"]))

    # ---- right: register card ------------------------------------------------
    img = card(img, (704, 44, 1376, 184), s)
    d = ImageDraw.Draw(img)
    d.text((728, 60), Hh["reg_title"], font=font(15, "cjk_bold"), fill=hx(s["accent"]))
    cw = tw(Hh["reg_chip"], 11, "cjk") + 22
    chip(img, (1352 - cw, 56), Hh["reg_chip"], s, size=11)
    d = ImageDraw.Draw(img)
    d.text((728, 88), Hh["reg_head"], font=font(11, "mono"), fill=hx(s["sub"]))

    x0, xs = 728, []
    for width in Hh["col_w"]:
        xs.append(x0)
        x0 += width
    for i, name in enumerate(Hh["cols"]):
        d.text((xs[i] + 4, 112), name, font=font(11, "cjk"), fill=hx(s["faint"]))
    d.line([728, 130, 1308, 130], fill=hx(s["grid"]), width=1)
    d.rounded_rectangle([720, 133, 1320, 171], radius=8, fill=hx(s["band"]))
    empty_i = Hh["empty_idx"]
    d.rounded_rectangle([xs[empty_i], 133, xs[empty_i] + Hh["col_w"][empty_i], 171],
                        radius=8, fill=hx(s["mark_bg"]), outline=hx(s["mark"]), width=1)
    for i, value in enumerate(Hh["row"]):
        if i == empty_i:
            continue
        text = truncate(value, 12, "cjk", Hh["col_w"][i] - 12)
        require_w(text, 12, "cjk", Hh["col_w"][i] - 10, f"hero row cell {i}")
        d.text((xs[i] + 5, 140), text, font=font(12, "cjk"), fill=hx(s["text"]))
    empty_text = Hh["row"][empty_i]
    ew = tw(empty_text, 12, "cjk")
    d.text((xs[empty_i] + (Hh["col_w"][empty_i] - ew) / 2, 140), empty_text,
           font=font(12, "cjk"), fill=hx(s["mark"]))

    # ---- right: three evidence-kind shelves ---------------------------------
    sev_of = {"err": s["err"], "warn": s["warn"], "info": s["info"]}
    bg_of = {"err": s["err_bg"], "warn": s["warn_bg"], "info": s["info_bg"]}
    for i, bar in enumerate(Hh["bars"]):
        y = 196 + i * 82
        color = sev_of[bar["key"]]
        img = card(img, (704, y, 1376, y + 72), s, radius=18, shadow=16)
        d = ImageDraw.Draw(img)
        d.rounded_rectangle([712, y + 14, 716, y + 58], radius=2, fill=hx(color))
        kind_w = runs(d, (728, y + 14),
                      [(f"kind: {bar['kind']}", 13, "mono_bold", color),
                       (f" · {bar['count']}", 12, "cjk", s["sub"])], s)
        if kind_w > 520:
            raise SystemExit(f"FATAL: hero kind label overflows: {bar['kind']!r}")
        pill_text = bar["ceiling"]
        pw = tw(pill_text, 11, "cjk") + 22
        d.rounded_rectangle([1352 - pw, y + 10, 1352, y + 34], radius=12,
                            fill=hx(bg_of[bar["key"]]), outline=hx(color), width=1)
        d.text((1352 - pw + 11, y + 14), pill_text, font=font(11, "cjk"), fill=hx(color))
        rules = bar["rules"]
        gap = 8
        cw_ = 250 if len(rules) == 1 else (624 - gap * (len(rules) - 1)) / len(rules)
        for j, (rule_id, field) in enumerate(rules):
            cx = 728 + j * (cw_ + gap)
            dashed = rule_id == "PB-005"
            d.rounded_rectangle([cx, y + 32, cx + cw_, y + 66], radius=10,
                                fill=hx(s["band"]), outline=hx(color if dashed else s["edge"]),
                                width=1)
            if dashed:
                # skipped by default: a dashed outline says so without a legend
                d.rounded_rectangle([cx + 4, y + 36, cx + cw_ - 4, y + 62], radius=8,
                                    outline=hx(s["edge"]), width=1)
            require_w(rule_id + " · " + field, 12, "mono", cw_ - 12, "hero rule chip")
            runs(d, (cx + 10, y + 41),
                 [(rule_id, 12, "mono_bold", s["text"]),
                  (" · ", 11, "cjk", s["faint"]),
                  (field, 11, "cjk", s["sub"])], s)
        if bar.get("note"):
            d.text((728 + cw_ + 16, y + 43), bar["note"], font=font(11, "cjk"),
                   fill=hx(s["faint"]))

    # dashed link: empty cell -> the direct-ceiling shelf that reports it (PB-001)
    for yy in range(174, 192, 6):
        d.line([903, yy, 903, yy + 3], fill=hx(s["mark"]), width=2)
    d.polygon([(903, 196), (897, 187), (909, 187)], fill=hx(s["mark"]))

    # ---- right: finding slip (real quickstart output) -----------------------
    img = card(img, (704, 444, 1376, 538), s, radius=20)
    d = ImageDraw.Draw(img)
    S = Hh["slip"]
    d.text((728, 456), S["rule"], font=font(14, "mono_bold"), fill=hx(s["text"]))
    sw = tw(S["sev"], 11, "cjk") + 22
    d.rounded_rectangle([728 + tw(S["rule"], 14, "mono_bold") + 12, 454,
                         728 + tw(S["rule"], 14, "mono_bold") + 12 + sw, 476],
                        radius=11, fill=hx(s["err_bg"]), outline=hx(s["err"]), width=1)
    d.text((728 + tw(S["rule"], 14, "mono_bold") + 23, 458), S["sev"],
           font=font(11, "cjk"), fill=hx(s["err"]))
    d.text((728, 484), S["locator"], font=font(11, "cjk"), fill=hx(s["faint"]))
    d.text((728, 500), S["found"], font=font(12, "cjk"), fill=hx(s["text"]))
    require_w(S["found"], 12, "cjk", 340, "hero slip found")
    d.text((728, 520), S["expected"], font=font(11, "cjk"), fill=hx(s["sub"]))
    require_w(S["expected"], 11, "cjk", 340, "hero slip expected")
    d.line([1082, 456, 1082, 526], fill=hx(s["grid"]), width=1)
    d.text((1102, 456), S["skip_head"], font=font(11, "mono_bold"), fill=hx(s["accent"]))
    d.text((1102, 482), S["skip"][0], font=font(11, "cjk"), fill=hx(s["sub"]))
    d.text((1102, 500), S["skip"][1], font=font(11, "cjk"), fill=hx(s["sub"]))
    d.text((1102, 520), S["skip_note"], font=font(11, "cjk"), fill=hx(s["faint"]))
    for line in S["skip"]:
        require_w(line, 11, "cjk", 250, "hero slip skipped")

    # ---- rail: the shelves feed the slip -----------------------------------
    d.line([692, 232, 692, 436], fill=hx(s["accent"]), width=2)
    for yy in (232, 314, 396):
        d.line([692, yy, 704, yy], fill=hx(s["accent"]), width=2)
    d.line([692, 436, 714, 436], fill=hx(s["accent"]), width=2)
    d.polygon([(714, 444), (708, 435), (720, 435)], fill=hx(s["accent"]))

    name = f"dsh-policy-brief-draft-hero-{lang}-{skin}.webp"
    img.save(os.path.join(OUT, name), "WEBP", quality=90, method=6)


# ------------------------------------------------------------------ flow (SVG) --
FONT_CJK = "'Microsoft YaHei','PingFang SC','Noto Sans CJK SC','Source Han Sans SC',sans-serif"
FONT_MONO = "'Consolas','SFMono-Regular','Menlo',ui-monospace,monospace"

FLOW_TIERS = [
    dict(kind="direct", count="4 条", ceiling="封顶 error", key="err",
         rules=[("PB-001", "核心观点"), ("PB-003", "出处"),
                ("PB-004", "数据截止"), ("PB-007", "表头两栏")], note=None),
    dict(kind="derived-from-principle", count="3 条", ceiling="封顶 warn", key="warn",
         rules=[("PB-002", "支撑依据"), ("PB-006", "建议→主体"),
                ("PB-008", "序号唯一")], note=None),
    dict(kind="institutional-configuration", count="1 条", ceiling="封顶 info", key="info",
         rules=[("PB-005", "新鲜度窗口")], note="maxDays = 0 ⇒ skipped"),
]

FLOW_HDR = {
    "input": [("核心观点", "point"), ("支撑依据", "evidence"), ("出处", "sourceRef"),
              ("数据截止", "dataAsOf"), ("建议事项", "recommendation"),
              ("实施主体", "implementer"), ("序号", "sectionNo"), ("章节", "section"),
              ("风险提示", "risk"), ("撰稿人", "drafter")],
    "header": ["title", "recipient", "draftedAt", "classification"],
}


def esc(text: str) -> str:
    return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def est(text: str, size: float, mono: bool = False) -> float:
    width = 0.0
    for ch in text:
        width += (0.60 if mono else 0.53) * size if ord(ch) < 128 else size
    return width


PARTS: list[str] = []


def guard(label: str, text: str, size: float, limit: float, mono: bool = False) -> None:
    width = est(text, size, mono)
    if width > limit:
        raise SystemExit(f"FATAL: {label} overflows ({width:.0f} > {limit:.0f}px): {text!r}")


def tx(x: float, y: float, text: str, size: float, fill: str, mono: bool = False,
       bold: bool = False, anchor: str | None = None, opacity: float | None = None) -> None:
    weight = ' font-weight="700"' if bold else ""
    extra = f' text-anchor="{anchor}"' if anchor else ""
    op = f' opacity="{opacity}"' if opacity is not None else ""
    PARTS.append(
        f'<text x="{x:.1f}" y="{y:.1f}" fill="{fill}" font-family="{FONT_MONO if mono else FONT_CJK}"'
        f' font-size="{size}"{weight}{extra}{op}>{esc(text)}</text>')


def mix(x: float, y: float, parts, anchor: str | None = None) -> None:
    """parts: (text, size, fill, mono[, bold])."""
    norm = []
    for part in parts:
        text, size, fill, mono = part[:4]
        bold = bool(part[4]) if len(part) > 4 else False
        norm.append((text, size, fill, mono, bold))
    total = sum(est(t, s, m) for (t, s, _f, m, _b) in norm)
    if anchor == "middle":
        x -= total / 2
    elif anchor == "end":
        x -= total
    spans = []
    for text, size, fill, mono, bold in norm:
        weight = ' font-weight="700"' if bold else ""
        spans.append(f'<tspan font-family="{FONT_MONO if mono else FONT_CJK}"'
                     f' font-size="{size}"{weight} fill="{fill}">{esc(text)}</tspan>')
    PARTS.append(f'<text x="{x:.1f}" y="{y:.1f}">{"".join(spans)}</text>')


def svg_pill(x: float, y: float, w: float, h: float, text: str, size: float,
         fg: str, bg: str, stroke: str | None = None, mono: bool = False,
         bold: bool = False) -> None:
    stroke_attr = f' stroke="{stroke}" stroke-width="1"' if stroke else ""
    PARTS.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}"'
                 f' rx="{h / 2:.1f}" fill="{bg}"{stroke_attr}/>')
    tx(x + w / 2, y + h / 2 + size * 0.35, text, size, fg, mono=mono, bold=bold,
       anchor="middle")


def flow_svg(skin: str) -> str:
    s = SKIN[skin]
    global PARTS
    PARTS = []
    err, warn, info = s["err"], s["warn"], s["info"]
    sev = {"err": err, "warn": warn, "info": info}
    sev_bg = {"err": s["err_bg"], "warn": s["warn_bg"], "info": s["info_bg"]}
    W, H = 1100, 660

    PARTS.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" role="img" aria-labelledby="fig-title fig-desc">')
    PARTS.append('<title id="fig-title">dsh-policy-brief-draft 结构：表头与 rows[] 两路输入，'
                 '8 条规则按依据类型封顶，报告分 issues 与 skipped 两路输出</title>')
    PARTS.append('<desc id="fig-desc">左侧输入是一份要素核对表：表头 title/recipient/draftedAt/'
                 'classification 与 rows[] 的核心观点、支撑依据、出处、数据截止、建议事项、实施主体、'
                 '序号、章节、风险提示、撰稿人。中间是 rules/policy-brief-draft.yaml 的 8 条规则，'
                 '按 kind 分三层：direct 封顶 error（PB-001/003/004/007）、'
                 'derived-from-principle 封顶 warn（PB-002/006/008）、'
                 'institutional-configuration 封顶 info（PB-005，maxDays=0 时自报 skipped）。'
                 '右侧报告含 summary、issues[]（定位到行与栏）与 skipped[]（含原因）；'
                 '原件只读，报告不作定性结论。</desc>')
    PARTS.append('<defs>')
    PARTS.append(f'<linearGradient id="bg" x1="0" y1="0" x2="0.28" y2="1">'
                 f'<stop offset="0" stop-color="{s["bg_from"]}"/>'
                 f'<stop offset="1" stop-color="{s["bg_to"]}"/></linearGradient>')
    PARTS.append(f'<radialGradient id="halo" cx="0.5" cy="0.5" r="0.5">'
                 f'<stop offset="0" stop-color="{s["accent"]}" stop-opacity="0.13"/>'
                 f'<stop offset="1" stop-color="{s["accent"]}" stop-opacity="0"/></radialGradient>')
    PARTS.append('<filter id="soft" x="-8%" y="-14%" width="116%" height="140%">'
                 f'<feDropShadow dx="0" dy="7" stdDeviation="9" flood-color="{s["shadow_hex"]}"'
                 f' flood-opacity="{0.10 if skin == "light" else 0.42}"/></filter>')
    PARTS.append('</defs>')
    PARTS.append(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
    PARTS.append(f'<ellipse cx="600" cy="300" rx="430" ry="300" fill="url(#halo)"/>')

    # ---- header -------------------------------------------------------------
    tx(40, 44, "dsh-policy-brief-draft", 26, s["text"], mono=True, bold=True)
    guard("flow title", "dsh-policy-brief-draft", 26, 700, mono=True)
    tx(40, 71, "一份要素核对表 → 三档依据天花板 → 差异清单与未执行清单", 12.5, s["sub"])
    guard("flow subtitle", "一份要素核对表 → 三档依据天花板 → 差异清单与未执行清单", 12.5, 760)
    hdr_pill = "只读 · 不联网 · 不调用模型"
    hw = est(hdr_pill, 11) + 26
    svg_pill(1060 - hw, 24, hw, 28, hdr_pill, 11, s["accent"], s["pill"], s["edge"])
    PARTS.append(f'<line x1="40" y1="90" x2="1060" y2="90" stroke="{s["edge"]}" stroke-width="1.2"/>')

    # ---- input card ---------------------------------------------------------
    PARTS.append(f'<rect x="40" y="104" width="292" height="448" rx="20" fill="{s["card"]}"'
                 f' stroke="{s["edge"]}" stroke-width="1.2" filter="url(#soft)"/>')
    tx(56, 128, "输入 · 要素核对表", 14, s["text"], bold=True)
    svg_pill(316 - 100, 110, 100, 24, "JSON / YAML", 11, s["accent"], s["pill"], s["edge"], mono=True)
    tx(56, 148, "file 或 material（二选一）", 11, s["sub"])
    guard("input sub", "file 或 material（二选一）", 11, 240)
    PARTS.append(f'<line x1="56" y1="160" x2="316" y2="160" stroke="{s["grid"]}" stroke-width="1"/>')

    mix(56, 180, [("header", 13, s["accent"], True, True), (" · 表头", 13, s["accent"], False, True)])
    for i, field in enumerate(FLOW_HDR["header"]):
        cx = 56 + (i % 2) * 132
        cy = 192 + (i // 2) * 30
        PARTS.append(f'<rect x="{cx}" y="{cy}" width="128" height="26" rx="9" fill="{s["band"]}"'
                     f' stroke="{s["edge"]}" stroke-width="1"/>')
        tx(cx + 9, cy + 17, field, 13, s["sub"], mono=True)
        guard("header chip", field, 13, 110, mono=True)
    tx(56, 268, "checkedAt = 运行时钟 · 日期按墙上时钟比较", 11, s["faint"])
    guard("input clock note", "checkedAt = 运行时钟 · 日期按墙上时钟比较", 11, 250)
    PARTS.append(f'<line x1="56" y1="280" x2="316" y2="280" stroke="{s["grid"]}" stroke-width="1"/>')

    mix(56, 300, [("rows[]", 13, s["accent"], True, True),
                  (" · 每节一行", 13, s["accent"], False, True)])
    for i, (label, field) in enumerate(FLOW_HDR["input"]):
        cx = 56 + (i % 2) * 134
        cy = 310 + (i // 2) * 38
        PARTS.append(f'<rect x="{cx}" y="{cy}" width="126" height="32" rx="10" fill="{s["band"]}"'
                     f' stroke="{s["edge"]}" stroke-width="1"/>')
        tx(cx + 9, cy + 16, label, 13, s["text"])
        tx(cx + 9, cy + 28, field, 11, s["faint"], mono=True)
        guard("input field chip", field, 11, 106, mono=True)
    tx(56, 512, "栏目名归一（忽略大小写、空格、下划线、连字符）", 11, s["faint"])
    guard("input note 1", "栏目名归一（忽略大小写、空格、下划线、连字符）", 11, 256)
    tx(56, 530, "无法执行的检查写进 skipped，不静默通过", 11, s["faint"])
    guard("input note 2", "无法执行的检查写进 skipped，不静默通过", 11, 256)

    # ---- middle: rule pack under three ceilings -----------------------------
    mix(360, 138, [("规则包", 13, s["accent"], False, True),
                   (" rules/policy-brief-draft.yaml", 13, s["sub"], True, False)])
    guard("rule pack heading", "规则包 rules/policy-brief-draft.yaml", 13, 400)
    mix(808, 138, [("8 条 · 版本 ", 11, s["faint"], False),
                   ("2026.1", 11, s["faint"], True)], anchor="end")

    tier_y = [152, 256, 360]
    for i, tier in enumerate(FLOW_TIERS):
        y = tier_y[i]
        color = sev[tier["key"]]
        PARTS.append(f'<rect x="360" y="{y}" width="448" height="92" rx="16" fill="{s["card"]}"'
                     f' stroke="{s["edge"]}" stroke-width="1.2" filter="url(#soft)"/>')
        PARTS.append(f'<rect x="366" y="{y + 14}" width="3" height="64" rx="1.5" fill="{color}"/>')
        mix(378, y + 26, [(f"kind: {tier['kind']}", 13, color, True, True),
                          (f" · {tier['count']}", 12.5, s["sub"], False, False)])
        guard("tier kind", f"kind: {tier['kind']} · {tier['count']}", 13, 320, mono=True)
        cw_ceiling = est(tier["ceiling"], 11.5) + 24
        svg_pill(792 - cw_ceiling, y + 10, cw_ceiling, 24, tier["ceiling"], 11.5,
             color, sev_bg[tier["key"]], color)
        rules = tier["rules"]
        gap = 6
        cw = 250 if len(rules) == 1 else (416 - gap * (len(rules) - 1)) / len(rules)
        for j, (rid, field) in enumerate(rules):
            cx = 376 + j * (cw + gap)
            dash = ' stroke-dasharray="4 3"' if rid == "PB-005" else ""
            PARTS.append(f'<rect x="{cx:.1f}" y="{y + 38}" width="{cw:.1f}" height="46" rx="11"'
                         f' fill="{s["band"]}" stroke="{color if rid == "PB-005" else s["edge"]}"'
                         f' stroke-width="1"{dash}/>')
            tx(cx + 9, y + 57, rid, 13, s["text"], mono=True, bold=True)
            tx(cx + 9, y + 72, field, 11, s["sub"])
            guard("tier rule id", rid, 13, cw - 16, mono=True)
            guard("tier rule field", field, 11, cw - 16)
        if tier["note"]:
            tx(376 + cw + 14, y + 62, tier["note"], 11, s["faint"], mono=True)
            guard("tier note", tier["note"], 11, 792 - (376 + cw + 14), mono=True)

    tx(360, 480, "8 条规则 = 7 条读行 + 1 条读表头；rules/*.yaml 是数据。", 11.5, s["faint"])
    guard("legend 1", "8 条规则 = 7 条读行 + 1 条读表头；rules/*.yaml 是数据。", 11.5, 448)
    tx(360, 500, "加载期校验 excerpt 逐字引文（≥ 8 字），夸大依据即失败。", 11.5, s["faint"])
    guard("legend 2", "加载期校验 excerpt 逐字引文（≥ 8 字），夸大依据即失败。", 11.5, 448)
    tx(360, 520, "PB-005 出厂 maxDays=0，因此自报 skipped，而非静默通过。", 11.5, s["faint"])
    guard("legend 3", "PB-005 出厂 maxDays=0，因此自报 skipped，而非静默通过。", 11.5, 448)

    # ---- output card --------------------------------------------------------
    PARTS.append(f'<rect x="836" y="104" width="224" height="448" rx="20" fill="{s["card"]}"'
                 f' stroke="{s["edge"]}" stroke-width="1.2" filter="url(#soft)"/>')
    tx(852, 128, "输出 · 报告", 14, s["text"], bold=True)
    svg_pill(1044 - 76, 110, 76, 24, "只列差异", 11, s["accent"], s["pill"], s["edge"])
    tx(852, 148, "buildView → markdown + JSON", 11, s["sub"], mono=True)
    guard("output sub", "buildView → markdown + JSON", 11, 190, mono=True)
    PARTS.append(f'<line x1="852" y1="160" x2="1044" y2="160" stroke="{s["grid"]}" stroke-width="1"/>')
    tx(852, 182, "summary", 11.5, s["faint"], mono=True)
    counts = [("error", "1", "err"), ("warn", "0", "warn"), ("info", "0", "info")]
    for i, (name, value, key) in enumerate(counts):
        pw = 60
        cx = 852 + i * (pw + 6)
        PARTS.append(f'<rect x="{cx}" y="190" width="{pw}" height="26" rx="9" fill="{sev_bg[key]}"'
                     f' stroke="{sev[key]}" stroke-width="1"/>')
        tx(cx + pw / 2, 208, f"{name} {value}", 11, sev[key], mono=True, anchor="middle")
        guard("summary pill", f"{name} {value}", 11, pw - 6, mono=True)
    PARTS.append(f'<line x1="852" y1="228" x2="1044" y2="228" stroke="{s["grid"]}" stroke-width="1"/>')

    mix(852, 250, [("issues[]", 13, s["text"], True, True), (" · 差异清单", 13, s["text"], False, True)])
    PARTS.append(f'<rect x="852" y="258" width="192" height="128" rx="12" fill="{s["band"]}"'
                 f' stroke="{s["edge"]}" stroke-width="1"/>')
    tx(866, 282, "PB-001", 13, s["text"], mono=True, bold=True)
    svg_pill(1044 - 12 - 56, 266, 56, 20, "error", 11, err, s["err_bg"], err, mono=True)
    tx(866, 302, "row 1 · point", 11, s["faint"], mono=True)
    tx(866, 324, "第 1 行「point」为空", 12.5, s["text"])
    guard("issue found", "第 1 行「point」为空", 12.5, 172)
    tx(866, 344, "应填：「point」应填写", 11.5, s["sub"])
    guard("issue expected", "应填：「point」应填写", 11.5, 172)
    tx(866, 364, "补填核心观点；只核是否写明", 11, s["faint"])
    guard("issue fix", "补填核心观点；只核是否写明", 11, 172)

    mix(852, 412, [("skipped[]", 13, s["text"], True, True), (" · 未执行", 13, s["text"], False, True)])
    PARTS.append(f'<rect x="852" y="420" width="192" height="82" rx="12" fill="{s["band"]}"'
                 f' stroke="{s["edge"]}" stroke-width="1"/>')
    tx(866, 442, "PB-005 maxDays 未配置", 11.5, s["sub"])
    tx(866, 462, "PB-006 无触发条件的行", 11.5, s["sub"])
    tx(866, 482, "2 条 · 空清单 ≠ 没问题", 11, s["faint"])
    guard("skipped a", "PB-005 maxDays 未配置", 11.5, 168)
    guard("skipped b", "PB-006 无触发条件的行", 11.5, 168)
    guard("skipped note", "2 条 · 空清单 ≠ 没问题", 11, 168)

    tx(852, 522, "免责声明随报告携带", 11, s["faint"])
    tx(852, 540, "不改原件，不联网，不调用模型", 11, s["faint"])
    guard("output foot", "不改原件，不联网，不调用模型", 11, 192)

    # ---- wiring: input bus -> shelves -> output bus ------------------------
    accent = s["accent"]
    PARTS.append(f'<path d="M332 328 H346 V198 H356 M346 302 H356 M346 406 H356"'
                 f' fill="none" stroke="{accent}" stroke-width="2.2" opacity="0.75"/>')
    for yy in (198, 302, 406):
        PARTS.append(f'<path d="M356 {yy - 4.5} L360 {yy} L356 {yy + 4.5} z" fill="{accent}"/>')
    PARTS.append(f'<path d="M808 198 H822 M808 302 H822 M808 406 H822 M822 198 V406"'
                 f' fill="none" stroke="{accent}" stroke-width="2.2" opacity="0.75"/>')
    PARTS.append(f'<path d="M822 302 H830 M830 298 L836 302 L830 306 z" fill="{accent}"/>')

    # ---- read-only loop back to the material -------------------------------
    PARTS.append(f'<path d="M938 552 V568 H162 V560" fill="none" stroke="{s["accent"]}"'
                 f' stroke-width="1.8" stroke-dasharray="5 5" opacity="0.72"/>')
    PARTS.append(f'<path d="M162 552 L157 560 L167 560 z" fill="{s["accent"]}"/>')
    loop_text = "原件只读 · 永不修改（writes: []）"
    lw = est(loop_text, 11) + 24
    svg_pill(550 - lw / 2, 557, lw, 22, loop_text, 11, s["accent"], s["card"], s["edge"])

    # ---- footer -------------------------------------------------------------
    tx(40, 596, "严重级跟着依据走：kind 决定上限——direct 可 error，"
                "derived-from-principle 封顶 warn，institutional-configuration 封顶 info。",
       11.5, s["sub"])
    guard("footer 1", "严重级跟着依据走：kind 决定上限——direct 可 error，"
          "derived-from-principle 封顶 warn，institutional-configuration 封顶 info。", 11.5, 1020)
    tx(40, 618, "不判定观点是否正确、依据是否充分、建议是否可行、数据是否可靠——结论留给审核人。",
       11.5, s["sub"])
    guard("footer 2", "不判定观点是否正确、依据是否充分、建议是否可行、数据是否可靠——结论留给审核人。", 11.5, 1020)
    tx(40, 640, "报告字段：summary · issues[]（locator.row / locator.column）· skipped[] · disclaimer。",
       11, s["faint"])
    guard("footer 3", "报告字段：summary · issues[]（locator.row / locator.column）· skipped[] · disclaimer。", 11, 1020)

    PARTS.append('</svg>')
    return "\n".join(PARTS) + "\n"


# ------------------------------------------------------------------------ main --
def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    for lang in ("zh", "en"):
        for skin in ("light", "dark"):
            hero(lang, skin)
    for skin in ("light", "dark"):
        name = f"dsh-policy-brief-draft-flow-v5-{skin}.svg"
        with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(flow_svg(skin))
    written = sorted(f for f in os.listdir(OUT)
                     if f.startswith("dsh-policy-brief-draft-hero-")
                     or f.startswith("dsh-policy-brief-draft-flow-v5-"))
    for name in written:
        size = os.path.getsize(os.path.join(OUT, name))
        print(f"wrote {name} ({size} bytes)")


if __name__ == "__main__":
    main()
