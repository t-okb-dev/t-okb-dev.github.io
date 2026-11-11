#!/usr/bin/env python3
"""
App Store & Web Marketing Asset Generator for IT Japanese Drill
Generates high-impact, bold, legible App Store screenshots, Hero banners, and promo banners
in 5 languages:
  - English (eng)
  - Indonesian (id)
  - Vietnamese (vi)
  - Korean (ko)
  - Chinese Simplified (zh)

Guarantees:
  1. Real phone mockups and screenshots are 100% untouched.
  2. Background gradient seamlessly matches original pixel values with zero visible boundary.
  3. Large, high-visibility typography designed specifically for App Store mobile browsing.
"""

import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = "/Users/ookubotomoakira/t-okb-dev/mobile_app/IT_Japanese"

FONTS = {
    'ja': {
        'heavy': "/System/Library/Fonts/ヒラギノ角ゴシック W8.ttc",
        'bold': "/System/Library/Fonts/ヒラギノ角ゴシック W7.ttc",
        'medium': "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc",
    },
    'eng': {
        'heavy': "/System/Library/Fonts/Helvetica.ttc",
        'bold': "/System/Library/Fonts/Helvetica.ttc",
        'medium': "/System/Library/Fonts/Helvetica.ttc",
    },
    'id': {
        'heavy': "/System/Library/Fonts/Helvetica.ttc",
        'bold': "/System/Library/Fonts/Helvetica.ttc",
        'medium': "/System/Library/Fonts/Helvetica.ttc",
    },
    'vi': {
        'heavy': "/Library/Fonts/Arial Unicode.ttf",
        'bold': "/Library/Fonts/Arial Unicode.ttf",
        'medium': "/Library/Fonts/Arial Unicode.ttf",
    },
    'ko': {
        'heavy': "/System/Library/Fonts/AppleSDGothicNeo.ttc",
        'bold': "/System/Library/Fonts/AppleSDGothicNeo.ttc",
        'medium': "/System/Library/Fonts/AppleSDGothicNeo.ttc",
    },
    'zh': {
        'heavy': "/System/Library/Fonts/Hiragino Sans GB.ttc",
        'bold': "/System/Library/Fonts/Hiragino Sans GB.ttc",
        'medium': "/System/Library/Fonts/Hiragino Sans GB.ttc",
    }
}

def get_font(lang, weight, size):
    path = FONTS[lang][weight]
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def draw_pill(draw, x, y, text, font, fill_color, text_color, border_color, dot_color=None, px=28, py=14):
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    dot_space = 28 if dot_color else 0
    w = tw + px * 2 + dot_space
    h = th + py * 2
    draw.rounded_rectangle([(x, y), (x + w, y + h)], radius=h // 2, fill=fill_color, outline=border_color, width=2)
    tx = x + px
    if dot_color:
        dot_r = 6
        dot_cy = y + h // 2
        dot_cx = x + px + dot_r
        draw.ellipse([(dot_cx - dot_r, dot_cy - dot_r), (dot_cx + dot_r, dot_cy + dot_r)], fill=dot_color)
        tx += dot_space
    draw.text((tx, y + py - 2), text, font=font, fill=text_color)
    return w, h

def draw_checkbox_item(draw, x, y, text, font, text_color, check_color=(56, 189, 248, 255)):
    box_size = 36
    draw.rounded_rectangle([(x, y), (x + box_size, y + box_size)], radius=8, fill=(30, 41, 65, 230), outline=(71, 85, 115, 200), width=2)
    draw.line([(x + 8, y + 18), (x + 16, y + 26)], fill=check_color, width=4)
    draw.line([(x + 16, y + 26), (x + 28, y + 10)], fill=check_color, width=4)
    draw.text((x + box_size + 20, y + 2), text, font=font, fill=text_color)

# Multilingual copy tuned for high CTR, urgency & clear value proposition
CONTENT = {
    'eng': {
        'slide1': {
            'badge': '4-CHOICE PRACTICAL DRILLS',
            'title_lines': ["Master IT Japanese", "with Real Drills!"],
            'sub': "Learn practical vocabulary & business phrases used on-site"
        },
        'slide2': {
            'badge': 'AI ROLE-PLAY CONVERSATIONS',
            'title_lines': ["Practice Live Dialogues", "with On-Device AI!"],
            'sub': "Code reviews, sprint standups & client meetings in Japanese"
        },
        'slide3': {
            'badge': 'SMART REVIEW & OFFLINE AI',
            'title_lines': ["Retain Everything &", "Generate New Drills!"],
            'sub': "Flashcards, mistakes review note & local AI auto-generation"
        },
        'hero': {
            'badge': 'FOR GLOBAL IT ENGINEERS & BrSE',
            'title': "IT Japanese Drill",
            'sub_bold': "Boost Your Tech Career in Japan",
            'lead1': "Master realistic business Japanese used in agile dev,",
            'lead2': "code reviews, and requirements definition.",
            'feat1': "Practical 4-Choice Tech Drills with native TTS audio",
            'feat2': "AI Interactive Role-Play Dialogues with Senior Leads",
            'feat3': "100% Offline On-Device AI • Zero Cloud Latency",
            'footer': "Requirements • Architecture • Code Review • Incident Handling"
        },
        'banner': {
            'badge': "100% OFFLINE • ON-DEVICE AI POWERED",
            'title': "IT Japanese Drill (BrSE)",
            'sub1': "Requirements • Architecture • Code Review • Incident Handling",
            'sub2': "Master on-site Japanese communication & IT knowledge simultaneously",
            'pill1': "4-Choice Drills",
            'pill2': "AI Roleplay",
            'pill3': "Smart Review",
            'footer': "Local LLM auto-generates unlimited practice questions offline"
        }
    },
    'id': {
        'slide1': {
            'badge': 'DRILL 4 PILIHAN PRAKTIS',
            'title_lines': ["Kuasai Bahasa Jepang IT", "dengan Drill Nyata!"],
            'sub': "Pelajari kosakata & frasa bisnis yang langsung dipakai di proyek"
        },
        'slide2': {
            'badge': 'LATIHAN ROLE-PLAY AI',
            'title_lines': ["Percakapan Nyata", "dengan AI On-Device!"],
            'sub': "Simulasi code review, daily standup, dan rapat dengan klien"
        },
        'slide3': {
            'badge': 'REVIEW PINTAR & AI OFFLINE',
            'title_lines': ["Ingat Lebih Kuat &", "Buat Soal Otomatis!"],
            'sub': "Kartu kosakata, catatan evaluasi, dan pembuatan soal oleh AI lokal"
        },
        'hero': {
            'badge': 'UNTUK ENGINEER IT ASING & BrSE',
            'title': "IT Japanese Drill",
            'sub_bold': "Tingkatkan Karier IT Anda di Jepang",
            'lead1': "Kuasai bahasa Jepang praktis di lingkungan kerja nyata,",
            'lead2': "mulai dari code review hingga definisi kebutuhan.",
            'feat1': "Drill 4 Pilihan Praktis disertai audio pelafalan TTS",
            'feat2': "Simulasi Role-Play Interaktif bersama Lead Engineer",
            'feat3': "Bekerja 100% Offline dengan AI On-Device yang aman",
            'footer': "Definisi Kebutuhan • Desain • Code Review • Penanganan Insiden"
        },
        'banner': {
            'badge': "100% OFFLINE • DIDUKUNG AI ON-DEVICE",
            'title': "IT Japanese Drill (BrSE)",
            'sub1': "Definisi Kebutuhan • Desain • Code Review • Penanganan Insiden",
            'sub2': "Kuasai komunikasi kerja & keahlian IT secara bersamaan",
            'pill1': "Drill 4 Pilihan",
            'pill2': "Role-Play AI",
            'pill3': "Review Pintar",
            'footer': "LLM lokal membuat soal latihan baru secara otomatis tanpa internet"
        }
    },
    'vi': {
        'slide1': {
            'badge': 'TRẮC NGHIỆM 4 LỰA CHỌN THỰC CHIẾN',
            'title_lines': ["Làm Chủ Tiếng Nhật IT", "Cùng Drill Thực Chiến!"],
            'sub': "Nắm vững thuật ngữ IT & tiếng Nhật thương mại tại dự án Nhật"
        },
        'slide2': {
            'badge': 'HỘI THOẠI ROLE-PLAY AI',
            'title_lines': ["Hội Thoại Thực Tế", "Cùng AI On-Device!"],
            'sub': "Luyện tập code review, họp báo cáo tiến độ và trao đổi khách hàng"
        },
        'slide3': {
            'badge': 'ÔN TẬP THÔNG MINH & AI OFFLINE',
            'title_lines': ["Ghi Nhớ Vững Vàng &", "Tự Động Tạo Đề Mới!"],
            'sub': "Flashcard từ vựng, sổ tay câu sai & AI nội bộ tự sinh bài tập"
        },
        'hero': {
            'badge': 'DÀNH RIÊNG CHO KỸ SƯ IT & BrSE',
            'title': "IT Japanese Drill",
            'sub_bold': "Bứt Phá Sự Nghiệp IT Tại Nhật Bản",
            'lead1': "Làm chủ tiếng Nhật thực tế trong phát triển phần mềm,",
            'lead2': "từ phân tích đặc tả yêu cầu đến review mã nguồn.",
            'feat1': 'Bài tập 4 lựa chọn sát thực tế kèm phát âm giọng bản xứ TTS',
            'feat2': 'Hội thoại nhập vai tương tác cùng Tiền bối & Quản lý dự án',
            'feat3': 'Hoạt động hoàn toàn Offline với công nghệ AI On-Device',
            'footer': 'Đặc tả yêu cầu • Thiết kế • Code Review • Xử lý sự cố'
        },
        'banner': {
            'badge': "HOÀN TOÀN OFFLINE • CÔNG NGHỆ AI ON-DEVICE",
            'title': "IT Japanese Drill (BrSE)",
            'sub1': "Đặc tả yêu cầu • Thiết kế • Code Review • Xử lý sự cố",
            'sub2': "Làm chủ giao tiếp hiện trường và kiến thức IT cùng lúc",
            'pill1': "Drill 4 Lựa chọn",
            'pill2': "Role-Play AI",
            'pill3': "Ôn Tập Tiện Lợi",
            'footer': "Mô hình LLM cục bộ tự động tạo câu hỏi mới hoàn toàn miễn phí"
        }
    },
    'ko': {
        'slide1': {
            'badge': '현장 밀착형 4지선다 실전 드릴',
            'title_lines': ["IT 실전 드릴로", "확실하게 마스터!"],
            'sub': "일본 IT 현장 실무 용어와 비즈니스 표현을 집중 훈련"
        },
        'slide2': {
            'badge': '실전 롤플레잉 AI 회화',
            'title_lines': ["온디바이스 AI와", "생생한 실전 대화!"],
            'sub': "선배 엔지니어와의 코드 리뷰, 스크럼 회의, 장애 보고 시뮬레이션"
        },
        'slide3': {
            'badge': '스마트 복습 & 오프라인 AI',
            'title_lines': ["약점 완벽 극복 &", "AI 문제 자동 생성!"],
            'sub': "단어 카드, 오답 복습 노트 및 로컬 LLM의 새로운 문제 생성"
        },
        'hero': {
            'badge': '외국인 IT 엔지니어·BrSE를 위한',
            'title': "IT 일본어 드릴",
            'sub_bold': "일본 IT 취업 및 커리어 성장의 지름길",
            'lead1': "실제 일본 개발 현장에서 매일 쓰는 실무 일본어를,",
            'lead2': "빠르고 확실하게 당신의 것으로 만드세요.",
            'feat1': "실전 감각을 키우는 4지선다 드릴 & 네이티브 음성 읽기",
            'feat2': "시니어 엔지니어·PM 페르소나와의 실시간 롤플레잉 대화",
            'feat3': "데이터 유출 걱정 없는 100% 오프라인 온디바이스 AI",
            'footer': "요구사항 정의 • 아키텍처 설계 • 코드 리뷰 • 장애 대응"
        },
        'banner': {
            'badge': "완전 오프라인 지원 • 온디바이스 AI 탑재",
            'title': "IT 일본어 드릴 (IT Japanese Drill)",
            'sub1': "요구사항 정의 • 아키텍처 설계 • 코드 리뷰 • 장애 대응",
            'sub2': "현장 비즈니스 회화와 IT 기술 지식을 동시에 습득",
            'pill1': "4지선다 드릴",
            'pill2': "AI 롤플레잉",
            'pill3': "스마트 복습",
            'footer': "로컬 LLM 탑재로 오프라인에서도 새로운 문제를 무제한 자동 생성"
        }
    },
    'zh': {
        'slide1': {
            'badge': '贴合开发现场 4选1实战题',
            'title_lines': ["攻克实战题目", "速成现场战力！"],
            'sub': "高频操练日本IT开发现场核心术语与商务交流表达"
        },
        'slide2': {
            'badge': '沉浸式角色扮演对话',
            'title_lines': ["与本地AI对话", "真实职场演练！"],
            'sub': "代码评审、敏捷早会报联相、需求确认全真模拟"
        },
        'slide3': {
            'badge': '端侧本地AI & 智能复习',
            'title_lines': ["高效温故知新 &", "AI自动生成新题！"],
            'sub': "专业单词卡、错题复习本与端侧大模型离线出题"
        },
        'hero': {
            'badge': '面向外籍IT工程师与BrSE',
            'title': "IT日语练习 (IT Japanese Drill)",
            'sub_bold': "助你快速融入日本IT开发现场",
            'lead1': "系统掌握需求定义、架构设计、代码评审等",
            'lead2': "高频实战技术日语与职场沟通。",
            'feat1': "4选1实战填空练习题，配备母语级TTS清晰发音",
            'feat2': "模拟资深前辈与项目经理的沉浸式角色扮演互动",
            'feat3': "完全离线运行的端侧本地AI，绝不上报隐私数据",
            'footer': "需求定义 • 架构设计 • 代码评审 • 故障排查"
        },
        'banner': {
            'badge': "完全离线支持 • 搭载端侧本地AI",
            'title': "IT日语练习 (IT Japanese Drill)",
            'sub1': "需求定义 • 架构设计 • 代码评审 • 故障排查",
            'sub2': "同步提升日本职场沟通技巧与IT工程实务能力",
            'pill1': "4选1实战题",
            'pill2': "AI情景对话",
            'pill3': "智能错题本",
            'footer': "本地端侧大模型无需联网，随时随地自动生成全新题目"
        }
    }
}

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE BUILDERS (1206 x 2622)
# ─────────────────────────────────────────────────────────────────────────────

def render_slide(orig_im, lang, slide_key, theme_colors):
    """
    Renders a slide with seamlessly reconstructed gradient in y=0..780.
    The phone below y=780 is 100% bit-for-bit unchanged.
    """
    out = orig_im.copy()
    W, H = out.size
    
    # 1. Perfectly rebuild top background gradient
    for y in range(780):
        c = orig_im.getpixel((50, y))
        for x in range(W):
            out.putpixel((x, y), c)
            
    d = ImageDraw.Draw(out)
    cfg = CONTENT[lang][slide_key]
    
    # Fonts
    f_badge = get_font(lang, 'bold', 32)
    f_title = get_font(lang, 'heavy', 94 if lang in ['eng', 'id'] else 96)
    f_sub   = get_font(lang, 'medium', 40)
    
    # Draw Badge
    badge_y = 130
    draw_pill(d, 80, badge_y, cfg['badge'], f_badge,
              fill_color=theme_colors['pill_bg'],
              text_color=theme_colors['pill_txt'],
              border_color=theme_colors['pill_border'],
              dot_color=theme_colors['pill_dot'],
              px=26, py=12)
    
    # Draw 2-line Title (Big & Punchy)
    title_y = 230
    line_spacing = 110 if lang in ['eng', 'id'] else 115
    for idx, line in enumerate(cfg['title_lines']):
        d.text((80, title_y + idx * line_spacing), line, font=f_title, fill=(255, 255, 255, 255))
        
    # Draw Subtitle
    sub_y = title_y + len(cfg['title_lines']) * line_spacing + 25
    d.text((80, sub_y), cfg['sub'], font=f_sub, fill=theme_colors['sub_color'])
    
    return out

# ─────────────────────────────────────────────────────────────────────────────
# HERO BUILDER (1920 x 1280)
# ─────────────────────────────────────────────────────────────────────────────

def render_hero(orig_im, lang):
    out = orig_im.copy()
    W, H = out.size
    
    # Seamless gradient recreation for left region x in 0..780, y in 120..1020
    for y in range(120, 1020):
        c_left = orig_im.getpixel((30, y))
        c_right = orig_im.getpixel((780, y))
        for x in range(0, 600):
            out.putpixel((x, y), c_left)
        for x in range(600, 780):
            t = (x - 600) / 180.0
            r = int(c_left[0]*(1-t) + c_right[0]*t)
            g = int(c_left[1]*(1-t) + c_right[1]*t)
            b = int(c_left[2]*(1-t) + c_right[2]*t)
            out.putpixel((x, y), (r, g, b))
            
    d = ImageDraw.Draw(out)
    cfg = CONTENT[lang]['hero']
    
    f_badge = get_font(lang, 'bold', 28)
    f_title = get_font(lang, 'heavy', 74 if lang != 'eng' else 68)
    f_sub_b = get_font(lang, 'bold', 34)
    f_lead  = get_font(lang, 'medium', 30)
    f_feat  = get_font(lang, 'medium', 28)
    f_foot  = get_font(lang, 'medium', 25)
    
    # Badge
    draw_pill(d, 80, 140, cfg['badge'], f_badge,
              fill_color=(30, 41, 75, 230), text_color=(147, 197, 253, 255),
              border_color=(71, 85, 125, 200), dot_color=(96, 165, 250, 255),
              px=24, py=10)
    
    # App Title & English Subtitle
    d.text((80, 220), cfg['title'], font=f_title, fill=(255, 255, 255, 255))
    d.text((82, 315), cfg['sub_bold'], font=f_sub_b, fill=(96, 165, 250, 255))
    
    # Value Leads
    d.text((82, 410), cfg['lead1'], font=f_lead, fill=(240, 245, 255, 255))
    d.text((82, 460), cfg['lead2'], font=f_lead, fill=(240, 245, 255, 255))
    
    # Key Features
    draw_checkbox_item(d, 82, 575, cfg['feat1'], f_feat, (240, 245, 255, 255), (56, 189, 248, 255))
    draw_checkbox_item(d, 82, 655, cfg['feat2'], f_feat, (240, 245, 255, 255), (192, 132, 252, 255))
    draw_checkbox_item(d, 82, 735, cfg['feat3'], f_feat, (240, 245, 255, 255), (45, 212, 191, 255))
    
    # Technical Scope Footer
    d.text((82, 875), cfg['footer'], font=f_foot, fill=(148, 163, 184, 255))
    
    return out

# ─────────────────────────────────────────────────────────────────────────────
# BANNER BUILDER (3840 x 1646)
# ─────────────────────────────────────────────────────────────────────────────

def render_banner(orig_im, lang):
    out = orig_im.copy()
    W, H = out.size
    
    # Seamless gradient recreation for left region x in 0..1760, y in 140..1200
    for y in range(140, 1200):
        c_left = orig_im.getpixel((30, y))
        c_right = orig_im.getpixel((1760, y))
        for x in range(0, 1500):
            out.putpixel((x, y), c_left)
        for x in range(1500, 1760):
            t = (x - 1500) / 260.0
            r = int(c_left[0]*(1-t) + c_right[0]*t)
            g = int(c_left[1]*(1-t) + c_right[1]*t)
            b = int(c_left[2]*(1-t) + c_right[2]*t)
            a = int(c_left[3]*(1-t) + c_right[3]*t)
            out.putpixel((x, y), (r, g, b, a))
            
    d = ImageDraw.Draw(out)
    cfg = CONTENT[lang]['banner']
    
    f_badge = get_font(lang, 'bold', 42)
    f_title = get_font(lang, 'heavy', 96 if lang != 'eng' else 86)
    f_sub1  = get_font(lang, 'bold', 50)
    f_sub2  = get_font(lang, 'medium', 46)
    f_pill  = get_font(lang, 'bold', 42)
    f_foot  = get_font(lang, 'medium', 40)
    
    # Top Badge
    draw_pill(d, 160, 170, cfg['badge'], f_badge,
              fill_color=(30, 41, 75, 230), text_color=(147, 197, 253, 255),
              border_color=(71, 85, 125, 200), dot_color=(96, 165, 250, 255),
              px=36, py=16)
    
    # Title
    d.text((160, 310), cfg['title'], font=f_title, fill=(255, 255, 255, 255))
    
    # Subtitles
    d.text((162, 480), cfg['sub1'], font=f_sub1, fill=(96, 165, 250, 255))
    d.text((162, 570), cfg['sub2'], font=f_sub2, fill=(235, 240, 250, 255))
    
    # Three Feature Badges Row
    w1, _ = draw_pill(d, 162, 750, cfg['pill1'], f_pill,
                      fill_color=(30, 41, 75, 230), text_color=(240, 245, 255, 255),
                      border_color=(71, 85, 125, 200), dot_color=None, px=36, py=18)
    w2, _ = draw_pill(d, 162 + w1 + 36, 750, cfg['pill2'], f_pill,
                      fill_color=(48, 28, 80, 230), text_color=(240, 245, 255, 255),
                      border_color=(90, 50, 130, 200), dot_color=None, px=36, py=18)
    w3, _ = draw_pill(d, 162 + w1 + 36 + w2 + 36, 750, cfg['pill3'], f_pill,
                      fill_color=(20, 50, 65, 230), text_color=(240, 245, 255, 255),
                      border_color=(40, 90, 105, 200), dot_color=None, px=36, py=18)
                      
    # Offline LLM Feature Footer
    d.text((162, 970), "● " + cfg['footer'], font=f_foot, fill=(148, 163, 184, 255))
    
    return out

# ─────────────────────────────────────────────────────────────────────────────
# MAIN EXECUTION
# ─────────────────────────────────────────────────────────────────────────────

def main():
    orig_s1 = Image.open(f"{BASE_DIR}/appstore_slide_01.png")
    orig_s2 = Image.open(f"{BASE_DIR}/appstore_slide_02.png")
    orig_s3 = Image.open(f"{BASE_DIR}/appstore_slide_03.png")
    orig_hero = Image.open(f"{BASE_DIR}/appstore_hero.png")
    orig_banner = Image.open(f"{BASE_DIR}/appstore_banner.png")
    
    themes = {
        'slide1': {
            'pill_bg': (30, 41, 75, 230),
            'pill_txt': (147, 197, 253, 255),
            'pill_border': (71, 85, 125, 200),
            'pill_dot': (96, 165, 250, 255),
            'sub_color': (200, 210, 225, 255)
        },
        'slide2': {
            'pill_bg': (48, 28, 80, 230),
            'pill_txt': (216, 180, 254, 255),
            'pill_border': (90, 50, 130, 200),
            'pill_dot': (192, 132, 252, 255),
            'sub_color': (210, 205, 230, 255)
        },
        'slide3': {
            'pill_bg': (20, 50, 65, 230),
            'pill_txt': (94, 234, 212, 255),
            'pill_border': (40, 90, 105, 200),
            'pill_dot': (45, 212, 191, 255),
            'sub_color': (205, 225, 235, 255)
        }
    }
    
    languages = ['eng', 'id', 'vi', 'ko', 'zh']
    
    for lang in languages:
        print(f"Generating high-legibility assets for: {lang}")
        
        # Slides
        s1 = render_slide(orig_s1, lang, 'slide1', themes['slide1'])
        s1.save(f"{BASE_DIR}/appstore_slide_01_{lang}.png", "PNG")
        
        s2 = render_slide(orig_s2, lang, 'slide2', themes['slide2'])
        s2.save(f"{BASE_DIR}/appstore_slide_02_{lang}.png", "PNG")
        
        s3 = render_slide(orig_s3, lang, 'slide3', themes['slide3'])
        s3.save(f"{BASE_DIR}/appstore_slide_03_{lang}.png", "PNG")
        
        # Hero & Banner
        hero = render_hero(orig_hero, lang)
        hero.save(f"{BASE_DIR}/appstore_hero_{lang}.png", "PNG")
        
        banner = render_banner(orig_banner, lang)
        banner.save(f"{BASE_DIR}/appstore_banner_{lang}.png", "PNG")
        
        print(f"  ✓ {lang} completed")

    print("\nAll 25 assets generated with seamless gradients and optimal App Store typography!")

if __name__ == "__main__":
    main()
