#!/usr/bin/env python3
"""
Relative Pitch Trainer (Piano) - App Store & Web Marketing Asset Generator
Creates ultra-premium 3D-tilted device mockups, slides, hero images, and promo banners
for both Japanese and English.
"""

import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PIL import Image, ImageDraw, ImageFont, ImageFilter
from generate_appstore_marketing_assets import (
    create_gradient_bg,
    draw_pill_badge_clean,
    draw_feature_item_clean,
)

BASE = "/Users/ookubotomoakira/t-okb-dev/mobile_app/relative_pitch"
SCREENSHOTS = {
    "home":         f"{BASE}/screenshot_home_ja.png",
    "simple":       f"{BASE}/screenshot_training_simple.png",
    "advanced":     f"{BASE}/screenshot_training_advanced.png",
    "settings":     f"{BASE}/screenshot_settings.png",
    # English versions
    "home_eng":     f"{BASE}/screenshot_home_en.png",
    "simple_eng":   f"{BASE}/screenshot_training_simple_eng.png",
    "advanced_eng": f"{BASE}/screenshot_training_advanced_eng.png",
    "settings_eng": f"{BASE}/screenshot_settings_eng.png",
}

OUT_HERO       = f"{BASE}/appstore_hero.jpg"
OUT_SLIDES = [
    f"{BASE}/appstore_slide_01.png",
    f"{BASE}/appstore_slide_02.png",
    f"{BASE}/appstore_slide_03.png",
    f"{BASE}/appstore_slide_04.png",
]
OUT_BANNER     = f"{BASE}/appstore_banner.png"

OUT_HERO_ENG   = f"{BASE}/appstore_hero_eng.jpg"
OUT_SLIDES_ENG = [
    f"{BASE}/appstore_slide_01_eng.png",
    f"{BASE}/appstore_slide_02_eng.png",
    f"{BASE}/appstore_slide_03_eng.png",
    f"{BASE}/appstore_slide_04_eng.png",
]
OUT_BANNER_ENG = f"{BASE}/appstore_banner_eng.png"

FONT_HEAVY  = "/System/Library/Fonts/ヒラギノ角ゴシック W8.ttc"
FONT_BOLD   = "/System/Library/Fonts/ヒラギノ角ゴシック W7.ttc"
FONT_MEDIUM = "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc"

def lf(p, s):
    try: return ImageFont.truetype(p, s)
    except: return ImageFont.load_default()

ASPECT        = 1284 / 2778
GRAD_TOP      = (15,  23,  42)
GRAD_BOT      = (30,  41,  80)
ACCENT_INDIGO = (129, 140, 248, 255)  # #818cf8
ACCENT_BLUE   = ( 96, 165, 250, 255)  # #60a5fa
WHITE         = (248, 250, 252, 255)
DIM           = (148, 163, 184, 255)


def render_phone(screen_key, target_device_h, tilt_deg, shadow_blur=28, shadow_opacity=140):
    theta  = math.radians(abs(tilt_deg))
    cos_t  = abs(math.cos(theta)); sin_t = abs(math.sin(theta))
    sp     = shadow_blur * 2
    overhead = 126
    rhs    = target_device_h - 2*sp - overhead*(cos_t+sin_t)
    sc_h   = max(80, int(rhs / (cos_t + ASPECT*sin_t)))
    sc_w   = int(sc_h * ASPECT)

    sc = Image.open(SCREENSHOTS[screen_key]).convert('RGB')\
              .resize((sc_w, sc_h), Image.Resampling.LANCZOS).convert('RGBA')

    bezel=10; metal=3; pad=bezel+metal; canvas_pad=50; corner_r=50
    fw=sc_w+pad*2; fh=sc_h+pad*2; cw=fw+canvas_pad*2; ch=fh+canvas_pad*2

    frame = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
    d = ImageDraw.Draw(frame)
    fx=canvas_pad; fy=canvas_pad

    # Side buttons
    d.rounded_rectangle([(fx+fw-2,fy+int(fh*0.22)),(fx+fw+4,fy+int(fh*0.35))],radius=3,fill=(70,75,88,255))
    d.rounded_rectangle([(fx-4,fy+int(fh*0.13)),(fx+2,fy+int(fh*0.18))],radius=3,fill=(70,75,88,255))
    d.rounded_rectangle([(fx-4,fy+int(fh*0.20)),(fx+2,fy+int(fh*0.28))],radius=3,fill=(70,75,88,255))
    d.rounded_rectangle([(fx-4,fy+int(fh*0.30)),(fx+2,fy+int(fh*0.38))],radius=3,fill=(70,75,88,255))
    # Frame body
    d.rounded_rectangle([(fx,fy),(fx+fw,fy+fh)],radius=corner_r,
                         fill=(28,32,42,255),outline=(100,110,130,255),width=2)
    d.rounded_rectangle([(fx+metal,fy+metal),(fx+fw-metal,fy+fh-metal)],
                         radius=corner_r-2, fill=(8,9,12,255))
    # Screen – paste with rounded-rect mask
    sx=fx+pad; sy=fy+pad
    scr_mask=Image.new('L',(sc_w,sc_h),0)
    smd=ImageDraw.Draw(scr_mask)
    smd.rounded_rectangle([(0,0),(sc_w,sc_h)],radius=max(1,corner_r-pad),fill=255)
    frame.paste(sc,(sx,sy),scr_mask)

    # Tilt
    if tilt_deg != 0:
        frame = frame.rotate(tilt_deg, Image.Resampling.BICUBIC, expand=True)

    # Shadow & frame composite
    frame_alpha = frame.split()[3]
    W2=frame.width+sp*2; H2=frame.height+sp*2

    shadow_layer = Image.new('RGBA',(W2,H2),(0,0,0,0))
    shadow_fill  = Image.new('RGBA',frame.size,(0,0,0,shadow_opacity))
    shadow_layer.paste(shadow_fill,(sp+int(tilt_deg*1.2),sp+int(shadow_blur*0.6)),frame_alpha)
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(shadow_blur))

    frame_layer = Image.new('RGBA',(W2,H2),(0,0,0,0))
    frame_layer.paste(frame,(sp,sp))

    return Image.alpha_composite(shadow_layer, frame_layer)


def place_phone(canvas, dev, cx, cy):
    dw,dh=dev.size; x=cx-dw//2; y=cy-dh//2
    tmp=Image.new('RGBA',canvas.size,(0,0,0,0))
    src_x=max(0,-x);  src_y=max(0,-y)
    dst_x=max(0,x);   dst_y=max(0,y)
    w=min(dw-src_x, canvas.width-dst_x)
    h=min(dh-src_y, canvas.height-dst_y)
    if w>0 and h>0:
        tmp.paste(dev.crop((src_x,src_y,src_x+w,src_y+h)),(dst_x,dst_y))
    return Image.alpha_composite(canvas, tmp)


def draw_badge_on_canvas(canvas, x, y, text, font, fill_color, text_color, border_color, dot_color=None):
    overlay = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    draw_pill_badge_clean(d, x, y, text, font, fill_color, text_color, border_color, dot_color)
    return Image.alpha_composite(canvas, overlay)


def draw_features_on_canvas(canvas, items, start_x, start_y, line_gap, font, text_color, check_color):
    overlay = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    for i, item in enumerate(items):
        draw_feature_item_clean(d, start_x, start_y + i * line_gap, item, font, text_color, check_color)
    return Image.alpha_composite(canvas, overlay)


# ─── HERO 1024x682 ───────────────────────────────────────────────────────────
def make_hero():
    W, H = 1024, 682
    bg = create_gradient_bg(W,H,GRAD_TOP,GRAD_BOT,
         radial_glow=(int(W*0.72),int(H*0.38),400,(99,102,241,65)))
    canvas = bg.convert('RGBA')

    dev_h = int(H * 0.94)
    dev_home   = render_phone("home",   dev_h, -10, 28, 140)
    dev_simple = render_phone("simple", dev_h,  10, 28, 140)
    print(f"  Hero JA: dev={dev_home.size}")

    canvas = place_phone(canvas, dev_simple, int(W*0.74), H//2+10)
    canvas = place_phone(canvas, dev_home,   int(W*0.47), H//2-10)

    fx = 44
    canvas = draw_badge_on_canvas(canvas, fx, 72, "Piano Ear Training", lf(FONT_MEDIUM,16),
        fill_color=(99,102,241,40), text_color=ACCENT_INDIGO,
        border_color=(99,102,241,120), dot_color=ACCENT_INDIGO)

    feats = ["ピアノ実音で音程を耳で覚える", "基礎から応用までステップアップ", "カレンダー機能で毎日の練習を継続"]
    canvas = draw_features_on_canvas(canvas, feats, fx, 370, 36, lf(FONT_MEDIUM,18), WHITE, ACCENT_INDIGO)

    draw = ImageDraw.Draw(canvas)
    draw.text((fx,116),"相対音感", font=lf(FONT_HEAVY,68), fill=WHITE)
    draw.text((fx,185),"Piano",   font=lf(FONT_BOLD,44),   fill=ACCENT_INDIGO)
    draw.text((fx,230),"Trainer", font=lf(FONT_BOLD,44),   fill=ACCENT_INDIGO)
    draw.text((fx,296),"すべての音楽家のための",  font=lf(FONT_MEDIUM,21), fill=DIM)
    draw.text((fx,322),"聴音・音感トレーニング",  font=lf(FONT_MEDIUM,21), fill=DIM)
    draw.text((fx,500),"Free on App Store",font=lf(FONT_MEDIUM,18),fill=ACCENT_BLUE)

    canvas.convert('RGB').save(OUT_HERO,'JPEG',quality=95)
    print(f"  Saved: {OUT_HERO}")


# ─── SLIDES 512x1024 ─────────────────────────────────────────────────────────
SLIDE_CONFIGS_JA = [
    {"key":"home",     "title":"相対音感を\n鍛えよう",           "subtitle":"カレンダーで毎日の練習を習慣化",           "badge":"ホーム画面",       "tilt":-6},
    {"key":"simple",   "title":"単音・インターバル\n聴音ドリル", "subtitle":"ピアノ実音で音と音の距離を聴き当てる",       "badge":"基礎トレーニング", "tilt": 6},
    {"key":"advanced", "title":"複数音当てで\nステップアップ",   "subtitle":"ルート音からの和音・音程を正確に判別",     "badge":"応用トレーニング", "tilt":-6},
    {"key":"settings", "title":"自分のレベルに\n合わせて設定",   "subtitle":"問題数や音名表記（ドレミ/CDE）を自由に変更", "badge":"設定・カスタマイズ", "tilt": 6},
]

SLIDE_CONFIGS_ENG = [
    {"key":"home_eng",     "title":"Master\nRelative Pitch",         "subtitle":"Track daily practice habits with calendar",              "badge":"Home",                "tilt":-6},
    {"key":"simple_eng",   "title":"Single Note &\nInterval Drills", "subtitle":"Listen to real piano tones and identify intervals",     "badge":"Basic Training",      "tilt": 6},
    {"key":"advanced_eng", "title":"Level Up with\nMulti-Note Drills","subtitle":"Identify chord roots and harmonic intervals",         "badge":"Advanced Training",   "tilt":-6},
    {"key":"settings_eng", "title":"Customize for\nYour Level",      "subtitle":"Adjust question count and note naming (CDE / Solfege)", "badge":"Settings & Options",  "tilt": 6},
]

def make_slides(configs=None, out_paths=None, is_eng=False):
    if configs is None: configs = SLIDE_CONFIGS_JA
    if out_paths is None: out_paths = OUT_SLIDES
    W, H = 512, 1024
    for idx, cfg in enumerate(configs):
        bg = create_gradient_bg(W,H,GRAD_TOP,GRAD_BOT,
             radial_glow=(int(W*0.65),int(H*0.40),280,(99,102,241,45)))
        canvas = bg.convert('RGBA')

        dev_h = int(H * 0.814)
        dev = render_phone(cfg["key"], dev_h, cfg["tilt"], 22, 130)
        print(f"  Slide {idx+1} ({'ENG' if is_eng else 'JA'}): dev={dev.size}")

        actual_dev_h = dev.size[1]
        cy_slide = H - actual_dev_h // 2 - 8
        canvas = place_phone(canvas, dev, int(W * 0.54), cy_slide)

        tx = 28
        canvas = draw_badge_on_canvas(canvas, tx, 44, cfg["badge"], lf(FONT_MEDIUM,15),
            fill_color=(99,102,241,35), text_color=ACCENT_INDIGO,
            border_color=(99,102,241,100), dot_color=ACCENT_INDIGO)

        draw = ImageDraw.Draw(canvas)
        ty = 88
        title_size = 36 if is_eng else 38
        line_h = 44 if is_eng else 46
        for line in cfg["title"].split("\n"):
            draw.text((tx,ty),line,font=lf(FONT_HEAVY,title_size),fill=WHITE)
            ty += line_h
        draw.text((tx,ty+4),cfg["subtitle"],font=lf(FONT_MEDIUM,15 if is_eng else 16),fill=DIM)

        canvas.save(out_paths[idx],'PNG')
        print(f"  Saved: {out_paths[idx]}")


# ─── BANNER 1024x438 ─────────────────────────────────────────────────────────
def make_banner():
    W_hero, H_hero   = 1024, 682
    H_banner = 438
    hero = Image.open(OUT_HERO)
    top    = (H_hero - H_banner) // 2
    banner = hero.crop((0, top, W_hero, top + H_banner))
    banner.save(OUT_BANNER, "PNG")
    print(f"  Saved (cropped from hero): {OUT_BANNER}")


# ─── HERO (English) 1024x682 ──────────────────────────────────────────────────
def make_hero_eng():
    W, H = 1024, 682
    bg = create_gradient_bg(W,H,GRAD_TOP,GRAD_BOT,
         radial_glow=(int(W*0.72),int(H*0.38),400,(99,102,241,65)))
    canvas = bg.convert('RGBA')

    dev_h = int(H * 0.94)
    dev_home   = render_phone("home_eng",   dev_h, -10, 28, 140)
    dev_simple = render_phone("simple_eng", dev_h,  10, 28, 140)
    print(f"  Hero ENG: dev={dev_home.size}")

    canvas = place_phone(canvas, dev_simple, int(W*0.74), H//2+10)
    canvas = place_phone(canvas, dev_home,   int(W*0.47), H//2-10)

    fx = 44
    canvas = draw_badge_on_canvas(canvas, fx, 72, "Piano Ear Training", lf(FONT_MEDIUM,16),
        fill_color=(99,102,241,40), text_color=ACCENT_INDIGO,
        border_color=(99,102,241,120), dot_color=ACCENT_INDIGO)

    feats = ["Identify intervals with real piano sounds", "Step-by-step from beginner to advanced", "Calendar history to build daily habits"]
    canvas = draw_features_on_canvas(canvas, feats, fx, 360, 36, lf(FONT_MEDIUM,18), WHITE, ACCENT_INDIGO)

    draw = ImageDraw.Draw(canvas)
    draw.text((fx,116),"Relative",    font=lf(FONT_HEAVY,56), fill=WHITE)
    draw.text((fx,173),"Piano",       font=lf(FONT_BOLD,48),  fill=ACCENT_INDIGO)
    draw.text((fx,222),"Trainer",     font=lf(FONT_BOLD,48),  fill=ACCENT_INDIGO)
    draw.text((fx,288),"Ear training for all musicians", font=lf(FONT_MEDIUM,20), fill=DIM)
    draw.text((fx,313),"with real piano tones",          font=lf(FONT_MEDIUM,20), fill=DIM)
    draw.text((fx,500),"Free on App Store",font=lf(FONT_MEDIUM,18),fill=ACCENT_BLUE)

    canvas.convert('RGB').save(OUT_HERO_ENG,'JPEG',quality=95)
    print(f"  Saved: {OUT_HERO_ENG}")


# ─── BANNER (English) ─────────────────────────────────────────────────────────
def make_banner_eng():
    W_hero, H_hero = 1024, 682
    H_banner = 438
    hero = Image.open(OUT_HERO_ENG)
    top    = (H_hero - H_banner) // 2
    banner = hero.crop((0, top, W_hero, top + H_banner))
    banner.save(OUT_BANNER_ENG, "PNG")
    print(f"  Saved (cropped from hero_eng): {OUT_BANNER_ENG}")


if __name__ == "__main__":
    print("=== Generating Relative Pitch (Piano) Assets (Japanese) ===")
    make_hero()
    make_slides(SLIDE_CONFIGS_JA, OUT_SLIDES, is_eng=False)
    make_banner()

    print("\n=== Generating Relative Pitch (Piano) Assets (English) ===")
    make_hero_eng()
    make_slides(SLIDE_CONFIGS_ENG, OUT_SLIDES_ENG, is_eng=True)
    make_banner_eng()

    print("\nAll assets generated successfully!")
