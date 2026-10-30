#!/usr/bin/env python3
"""
App Store & Web Marketing Asset Generator
Creates ultra-premium 3D-tilted device mockups, slides, hero images, and promo banners
with real unedited screenshots, titanium bezels, and multi-layer soft shadows.
Zero font glyph missing / Zero character corruption.
"""

import math
import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT_HEAVY = "/System/Library/Fonts/ヒラギノ角ゴシック W8.ttc"
FONT_BOLD = "/System/Library/Fonts/ヒラギノ角ゴシック W7.ttc"
FONT_MEDIUM = "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc"


def create_gradient_bg(width, height, top_color, bottom_color, radial_glow=None):
    bg = Image.new('RGBA', (width, height))
    d = ImageDraw.Draw(bg)
    for y in range(height):
        t = y / max(1, height - 1)
        r = int(top_color[0] * (1 - t) + bottom_color[0] * t)
        g = int(top_color[1] * (1 - t) + bottom_color[1] * t)
        b = int(top_color[2] * (1 - t) + bottom_color[2] * t)
        d.line([(0, y), (width, y)], fill=(r, g, b, 255))

    if radial_glow:
        gx, gy, gr, gcolor = radial_glow
        glow = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        for rad in range(gr, 0, -4):
            factor = (1.0 - (rad / gr)) ** 1.8
            alpha = int(gcolor[3] * factor)
            gd.ellipse(
                [(gx - rad, gy - rad), (gx + rad, gy + rad)],
                fill=(gcolor[0], gcolor[1], gcolor[2], alpha),
            )
        bg = Image.alpha_composite(bg, glow)

    return bg


def render_iphone_device(
    screen_img,
    scale=1.0,
    tilt_angle=0.0,
    shadow_blur=24,
    shadow_opacity=160,
    add_reflection=True,
):
    sw, sh = screen_img.size
    bezel = 10
    metal = 3
    pad = bezel + metal

    fw = sw + pad * 2
    fh = sh + pad * 2
    corner_r = 50

    canvas_pad = 50
    cw = fw + canvas_pad * 2
    ch = fh + canvas_pad * 2

    frame = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
    d = ImageDraw.Draw(frame)
    fx = canvas_pad
    fy = canvas_pad

    # Hardware buttons
    d.rounded_rectangle(
        [
            (fx + fw - 2, fy + int(fh * 0.22)),
            (fx + fw + 4, fy + int(fh * 0.35)),
        ],
        radius=3,
        fill=(70, 75, 88, 255),
    )
    d.rounded_rectangle(
        [(fx - 4, fy + int(fh * 0.13)), (fx + 2, fy + int(fh * 0.18))],
        radius=3,
        fill=(70, 75, 88, 255),
    )
    d.rounded_rectangle(
        [(fx - 4, fy + int(fh * 0.20)), (fx + 2, fy + int(fh * 0.28))],
        radius=3,
        fill=(70, 75, 88, 255),
    )
    d.rounded_rectangle(
        [(fx - 4, fy + int(fh * 0.30)), (fx + 2, fy + int(fh * 0.38))],
        radius=3,
        fill=(70, 75, 88, 255),
    )

    # Titanium border & dark bezel
    d.rounded_rectangle(
        [(fx, fy), (fx + fw, fy + fh)],
        radius=corner_r,
        fill=(28, 32, 42, 255),
        outline=(100, 110, 130, 255),
        width=2,
    )
    d.rounded_rectangle(
        [
            (fx + metal, fy + metal),
            (fx + fw - metal, fy + fh - metal),
        ],
        radius=corner_r - 2,
        fill=(8, 9, 12, 255),
    )

    # Paste unedited screen
    sx = fx + pad
    sy = fy + pad
    screen_mask = Image.new('L', (sw, sh), 0)
    smd = ImageDraw.Draw(screen_mask)
    smd.rounded_rectangle(
        [(0, 0), (sw, sh)], radius=corner_r - pad, fill=255
    )
    frame.paste(screen_img, (sx, sy), screen_mask)

    if add_reflection:
        sheen = Image.new('RGBA', (sw, sh), (0, 0, 0, 0))
        sd = ImageDraw.Draw(sheen)
        sd.polygon(
            [(0, 0), (int(sw * 0.55), 0), (0, int(sh * 0.42))],
            fill=(255, 255, 255, 14),
        )
        frame.paste(sheen, (sx, sy), screen_mask)

    if scale != 1.0:
        nw = max(10, int(cw * scale))
        nh = max(10, int(ch * scale))
        frame = frame.resize((nw, nh), Image.Resampling.LANCZOS)

    if tilt_angle != 0:
        frame = frame.rotate(tilt_angle, Image.Resampling.BICUBIC, expand=True)

    # 3D Soft drop shadow
    alpha = frame.split()[3]
    sp = int(shadow_blur * 2.0)
    shadow = Image.new(
        'RGBA', (frame.width + sp * 2, frame.height + sp * 2), (0, 0, 0, 0)
    )
    shadow_fill = Image.new('RGBA', frame.size, (0, 0, 0, shadow_opacity))
    shadow.paste(
        shadow_fill,
        (sp + int(tilt_angle * 1.2), sp + int(shadow_blur * 0.6)),
        alpha,
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(shadow_blur))

    composite = Image.new('RGBA', shadow.size, (0, 0, 0, 0))
    composite.paste(shadow, (0, 0))
    composite.paste(frame, (sp, sp), frame.split()[3])

    return composite


def draw_pill_badge_clean(
    draw, x, y, text, font, fill_color, text_color, border_color, dot_color=None
):
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    dot_space = 14 if dot_color else 0
    px, py = 14, 6
    w = tw + px * 2 + dot_space
    h = th + py * 2
    draw.rounded_rectangle(
        [(x, y), (x + w, y + h)],
        radius=h // 2,
        fill=fill_color,
        outline=border_color,
        width=1,
    )
    tx = x + px
    if dot_color:
        dot_r = 3
        dot_cy = y + h // 2
        dot_cx = x + px + dot_r
        draw.ellipse(
            [(dot_cx - dot_r, dot_cy - dot_r), (dot_cx + dot_r, dot_cy + dot_r)],
            fill=dot_color,
        )
        tx += dot_space
    draw.text((tx, y + py - 1), text, font=font, fill=text_color)
    return w, h


def draw_feature_item_clean(
    draw, x, y, text, font, text_color, check_color=(56, 189, 248, 255)
):
    box_size = 20
    draw.rounded_rectangle(
        [(x, y), (x + box_size, y + box_size)],
        radius=5,
        fill=(30, 41, 65, 230),
        outline=(71, 85, 115, 200),
        width=1,
    )
    draw.line(
        [(x + 5, y + 10), (x + 9, y + 14)], fill=check_color, width=2
    )
    draw.line(
        [(x + 9, y + 14), (x + 15, y + 6)], fill=check_color, width=2
    )
    draw.text((x + box_size + 12, y + 1), text, font=font, fill=text_color)
