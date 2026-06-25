from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import Flowable

# ── Colour palette ──────────────────────────────────────────────────────────
NAVY      = colors.HexColor('#1A3A5C')
BLUE      = colors.HexColor('#2E6DA4')
LIGHT_BLUE= colors.HexColor('#E6F1FB')
DARK_BLUE = colors.HexColor('#0C447C')
GREEN     = colors.HexColor('#1D9E75')
LIGHT_GREEN=colors.HexColor('#E1F5EE')
DARK_GREEN= colors.HexColor('#085041')
AMBER     = colors.HexColor('#EF9F27')
LIGHT_AMBER=colors.HexColor('#FAEEDA')
DARK_AMBER= colors.HexColor('#633806')
RED       = colors.HexColor('#E24B4A')
LIGHT_RED = colors.HexColor('#FCEBEB')
DARK_RED  = colors.HexColor('#791F1F')
PURPLE    = colors.HexColor('#7F77DD')
LIGHT_PURPLE=colors.HexColor('#EEEDFE')
DARK_PURPLE=colors.HexColor('#3C3489')
GRAY_BG   = colors.HexColor('#F5F5F3')
GRAY_MID  = colors.HexColor('#888780')
GRAY_DARK = colors.HexColor('#444441')
WHITE     = colors.white
BLACK     = colors.HexColor('#1A1A1A')

W, H = A4

# ── Custom Flowables ─────────────────────────────────────────────────────────
class ColorBar(Flowable):
    """Full-width colored section header bar."""
    def __init__(self, text, bg=NAVY, fg=WHITE, height=11*mm):
        super().__init__()
        self.text = text
        self.bg = bg
        self.fg = fg
        self.barh = height
        self.width = 0
        self.height = height

    def wrap(self, availWidth, availHeight):
        self.width = availWidth
        return availWidth, self.barh

    def draw(self):
        c = self.canv
        c.setFillColor(self.bg)
        c.roundRect(0, 0, self.width, self.barh, 4, fill=1, stroke=0)
        c.setFillColor(self.fg)
        c.setFont('Helvetica-Bold', 11)
        c.drawString(8*mm, 3.5*mm, self.text)


class SideBar(Flowable):
    """Colored left-border info box."""
    def __init__(self, text, bar_color=BLUE, bg=LIGHT_BLUE, text_color=DARK_BLUE, min_height=8*mm):
        super().__init__()
        self.text = text
        self.bar_color = bar_color
        self.bg = bg
        self.text_color = text_color
        self._min_height = min_height
        self.width = 0
        self.height = min_height

    def wrap(self, availWidth, availHeight):
        self.width = availWidth
        # estimate height
        chars_per_line = int(availWidth / 3.5)
        lines = max(2, len(self.text) // chars_per_line + self.text.count('\n') + 1)
        self.height = max(self._min_height, lines * 4.5*mm + 4*mm)
        return availWidth, self.height

    def draw(self):
        c = self.canv
        c.setFillColor(self.bg)
        c.roundRect(0, 0, self.width, self.height, 3, fill=1, stroke=0)
        c.setFillColor(self.bar_color)
        c.rect(0, 0, 2.5*mm, self.height, fill=1, stroke=0)
        c.setFillColor(self.text_color)
        c.setFont('Helvetica', 8.5)
        text_x = 5.5*mm
        text_y = self.height - 5*mm
        # simple word-wrap
        words = self.text.replace('\n', ' \n ').split(' ')
        line = ''
        max_w = self.width - 7*mm
        for word in words:
            if word == '\n':
                c.drawString(text_x, text_y, line.strip())
                text_y -= 4.2*mm
                line = ''
                continue
            test = line + (' ' if line else '') + word
            if c.stringWidth(test, 'Helvetica', 8.5) > max_w:
                c.drawString(text_x, text_y, line.strip())
                text_y -= 4.2*mm
                line = word
            else:
                line = test
        if line:
            c.drawString(text_x, text_y, line.strip())


# ── Style helpers ─────────────────────────────────────────────────────────────
def make_styles():
    base = getSampleStyleSheet()
    s = {}

    s['title'] = ParagraphStyle('DocTitle',
        fontSize=26, textColor=WHITE, fontName='Helvetica-Bold',
        alignment=TA_CENTER, spaceAfter=2)

    s['subtitle'] = ParagraphStyle('DocSubtitle',
        fontSize=11, textColor=colors.HexColor('#B5D4F4'),
        fontName='Helvetica', alignment=TA_CENTER, spaceAfter=4)

    s['h1'] = ParagraphStyle('H1',
        fontSize=13, textColor=WHITE, fontName='Helvetica-Bold',
        spaceBefore=0, spaceAfter=0)

    s['h2'] = ParagraphStyle('H2',
        fontSize=11, textColor=NAVY, fontName='Helvetica-Bold',
        spaceBefore=8, spaceAfter=3)

    s['h3'] = ParagraphStyle('H3',
        fontSize=9.5, textColor=DARK_BLUE, fontName='Helvetica-Bold',
        spaceBefore=5, spaceAfter=2)

    s['body'] = ParagraphStyle('Body',
        fontSize=8.5, textColor=BLACK, fontName='Helvetica',
        leading=13, spaceAfter=3, alignment=TA_JUSTIFY)

    s['body_left'] = ParagraphStyle('BodyLeft',
        fontSize=8.5, textColor=BLACK, fontName='Helvetica',
        leading=13, spaceAfter=2)

    s['bullet'] = ParagraphStyle('Bullet',
        fontSize=8.5, textColor=BLACK, fontName='Helvetica',
        leading=13, spaceAfter=1.5,
        leftIndent=10, firstLineIndent=-8)

    s['small'] = ParagraphStyle('Small',
        fontSize=7.5, textColor=GRAY_DARK, fontName='Helvetica',
        leading=11, spaceAfter=2)

    s['code'] = ParagraphStyle('Code',
        fontSize=7.5, textColor=BLACK, fontName='Courier',
        leading=11, spaceAfter=2,
        backColor=GRAY_BG, leftIndent=6, rightIndent=6,
        borderPadding=(3,3,3,3))

    s['week_title'] = ParagraphStyle('WeekTitle',
        fontSize=9, textColor=NAVY, fontName='Helvetica-Bold',
        leading=12, spaceAfter=1)

    s['week_body'] = ParagraphStyle('WeekBody',
        fontSize=8, textColor=GRAY_DARK, fontName='Helvetica',
        leading=12, spaceAfter=2)

    s['resource_name'] = ParagraphStyle('ResName',
        fontSize=8.5, textColor=DARK_BLUE, fontName='Helvetica-Bold',
        leading=12, spaceAfter=1)

    s['resource_body'] = ParagraphStyle('ResBody',
        fontSize=8, textColor=GRAY_DARK, fontName='Helvetica',
        leading=12, spaceAfter=3)

    s['center'] = ParagraphStyle('Center',
        fontSize=8.5, textColor=BLACK, fontName='Helvetica',
        alignment=TA_CENTER, leading=12)

    s['tag'] = ParagraphStyle('Tag',
        fontSize=7, textColor=DARK_BLUE, fontName='Helvetica-Bold',
        alignment=TA_CENTER)

    return s

# ── Build helpers ─────────────────────────────────────────────────────────────
def sp(n=4): return Spacer(1, n*mm)
def hr(color=BLUE, thickness=0.5): return HRFlowable(width='100%', thickness=thickness, color=color, spaceAfter=3, spaceBefore=3)

def badge_table(badges):
    """Row of colored badge cells."""
    colors_map = {
        'blue':   (LIGHT_BLUE, DARK_BLUE),
        'green':  (LIGHT_GREEN, DARK_GREEN),
        'amber':  (LIGHT_AMBER, DARK_AMBER),
        'red':    (LIGHT_RED, DARK_RED),
        'purple': (LIGHT_PURPLE, DARK_PURPLE),
    }
    cells = []
    for text, c in badges:
        bg, fg = colors_map.get(c, (LIGHT_BLUE, DARK_BLUE))
        cells.append(Paragraph(f'<font color="#{fg.hexval()[1:]}"><b>{text}</b></font>', ParagraphStyle('b', fontSize=7, alignment=TA_CENTER, backColor=bg)))
    if not cells: return None
    col_w = 160 / len(cells) * mm
    t = Table([cells], colWidths=[col_w]*len(cells), rowHeights=[5*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (i,0),(i,0), colors_map.get(badges[i][1],(LIGHT_BLUE,))[0]) for i in range(len(badges))
    ] + [
        ('ROUNDEDCORNERS', [3]),
        ('GRID', (0,0),(-1,-1), 0, WHITE),
        ('LEFTPADDING', (0,0),(-1,-1), 4),
        ('RIGHTPADDING', (0,0),(-1,-1), 4),
        ('TOPPADDING', (0,0),(-1,-1), 2),
        ('BOTTOMPADDING', (0,0),(-1,-1), 2),
        ('VALIGN', (0,0),(-1,-1), 'MIDDLE'),
    ]))
    return t

def week_row(num, date, topic, detail, badge_color=BLUE):
    """A single week row as a table."""
    s = make_styles()
    num_para = Paragraph(f'<b>{num}</b><br/><font size="7" color="#888780">{date}</font>', s['week_title'])
    topic_para = Paragraph(f'<b>{topic}</b>', s['week_title'])
    detail_para = Paragraph(detail, s['week_body'])
    content = [topic_para, detail_para]
    t = Table([[num_para, content]], colWidths=[22*mm, 138*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,-1), WHITE),
        ('BOX', (0,0),(-1,-1), 0.5, colors.HexColor('#DDDDDD')),
        ('LEFTPADDING', (0,0),(0,0), 4),
        ('RIGHTPADDING', (0,0),(0,0), 4),
        ('LEFTPADDING', (1,0),(1,0), 6),
        ('RIGHTPADDING', (1,0),(1,0), 6),
        ('TOPPADDING', (0,0),(-1,-1), 4),
        ('BOTTOMPADDING', (0,0),(-1,-1), 4),
        ('VALIGN', (0,0),(-1,-1), 'TOP'),
        ('LINEBELOW', (0,0),(-1,0), 0.5, colors.HexColor('#EEEEEE')),
    ]))
    return t

def info_box(text, style='info'):
    configs = {
        'info':  (LIGHT_BLUE,   BLUE,   DARK_BLUE),
        'tip':   (LIGHT_GREEN,  GREEN,  DARK_GREEN),
        'warn':  (LIGHT_AMBER,  AMBER,  DARK_AMBER),
        'crit':  (LIGHT_RED,    RED,    DARK_RED),
    }
    bg, bar, tc = configs.get(style, configs['info'])
    return SideBar(text, bar_color=bar, bg=bg, text_color=tc)

def section_header(text, color=NAVY):
    return ColorBar(text, bg=color)

def two_col_table(left_items, right_items, s, col_ratio=(1,1)):
    """Two column layout from lists of Paragraphs."""
    rows = []
    maxl = max(len(left_items), len(right_items))
    for i in range(maxl):
        l = left_items[i] if i < len(left_items) else Paragraph('', s['body'])
        r = right_items[i] if i < len(right_items) else Paragraph('', s['body'])
        rows.append([l, r])
    total = 160*mm
    cw = [total * col_ratio[0]/(col_ratio[0]+col_ratio[1]),
          total * col_ratio[1]/(col_ratio[0]+col_ratio[1])]
    t = Table(rows, colWidths=cw)
    t.setStyle(TableStyle([
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('LEFTPADDING',(0,0),(-1,-1),0),
        ('RIGHTPADDING',(0,0),(0,-1),8),
        ('RIGHTPADDING',(1,0),(-1,-1),0),
        ('TOPPADDING',(0,0),(-1,-1),0),
        ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ]))
    return t

def bullet(text, s): return Paragraph(f'&#x2022;&#x2002;{text}', s['bullet'])

def skill_table(rows_data, s):
    """Skills table with label | value layout."""
    rows = []
    for label, value in rows_data:
        rows.append([
            Paragraph(f'<b>{label}</b>', s['small']),
            Paragraph(value, s['small'])
        ])
    t = Table(rows, colWidths=[35*mm, 125*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(0,-1), GRAY_BG),
        ('BACKGROUND',(1,0),(1,-1), WHITE),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('LEFTPADDING',(0,0),(-1,-1),5),
        ('RIGHTPADDING',(0,0),(-1,-1),5),
        ('TOPPADDING',(0,0),(-1,-1),3),
        ('BOTTOMPADDING',(0,0),(-1,-1),3),
        ('LINEBELOW',(0,0),(-1,-2),0.3,colors.HexColor('#E0E0E0')),
        ('BOX',(0,0),(-1,-1),0.5,colors.HexColor('#DDDDDD')),
    ]))
    return t

def q_and_a(q, a, s):
    """Interview Q&A block."""
    items = [
        Paragraph(f'<b>Q:</b> {q}', s['body_left']),
        Paragraph(f'<b>A:</b> {a}', s['small']),
        sp(1),
    ]
    return items

def month_header(month, theme, color):
    return ColorBar(f'{month}  —  {theme}', bg=color, fg=WHITE, height=9*mm)


# ═══════════════════════════════════════════════════════════════════════════════
# DOCUMENT BUILDER
# ═══════════════════════════════════════════════════════════════════════════════
def build_pdf(path):
    doc = SimpleDocTemplate(
        path, pagesize=A4,
        leftMargin=18*mm, rightMargin=18*mm,
        topMargin=15*mm, bottomMargin=15*mm,
        title='Embedded Systems & Firmware Engineering Roadmap — Yash Mehta',
        author='Claude / Anthropic'
    )
    s = make_styles()
    story = []

    # ── COVER ────────────────────────────────────────────────────────────────
    story.append(sp(12))
    # Cover background bar
    cover = Table([[
        Paragraph('<font color="white"><b>EMBEDDED SYSTEMS &amp; FIRMWARE</b><br/>ENGINEERING ROADMAP</font>', ParagraphStyle('CT', fontSize=22, textColor=WHITE, fontName='Helvetica-Bold', alignment=TA_CENTER, leading=28)),
    ]], colWidths=[160*mm], rowHeights=[38*mm])
    cover.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(0,0),NAVY),
        ('ROUNDEDCORNERS',[6]),
        ('VALIGN',(0,0),(0,0),'MIDDLE'),
        ('ALIGN',(0,0),(0,0),'CENTER'),
        ('TOPPADDING',(0,0),(0,0),8),
        ('BOTTOMPADDING',(0,0),(0,0),8),
    ]))
    story.append(cover)
    story.append(sp(4))

    sub_items = [
        Paragraph('<b>Yash Mehta</b>  |  VIT Vellore — ECE 4th Year  |  MSIL Intern, Gurgaon', ParagraphStyle('SI', fontSize=10, textColor=NAVY, fontName='Helvetica-Bold', alignment=TA_CENTER)),
        sp(1),
        Paragraph('June 2026 — November 2026  •  C Programming → STM32 → FreeRTOS → CAN Bus → Job-Ready', ParagraphStyle('SI2', fontSize=9, textColor=GRAY_DARK, fontName='Helvetica', alignment=TA_CENTER)),
    ]
    for it in sub_items: story.append(it)
    story.append(sp(6))

    # Stats row
    stats = [
        ['6\nMonths', '24\nWeeks', '2\nFlagship\nProjects', 'Job-Ready\nDec 2026'],
    ]
    st = Table(stats, colWidths=[40*mm]*4, rowHeights=[18*mm])
    st.setStyle(TableStyle([
        ('BACKGROUND',(i,0),(i,0), [LIGHT_BLUE, LIGHT_GREEN, LIGHT_AMBER, LIGHT_PURPLE][i]) for i in range(4)
    ] + [
        ('TEXTCOLOR',(i,0),(i,0), [DARK_BLUE, DARK_GREEN, DARK_AMBER, DARK_PURPLE][i]) for i in range(4)
    ] + [
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('FONTNAME',(0,0),(-1,-1),'Helvetica-Bold'),
        ('FONTSIZE',(0,0),(-1,-1),9),
        ('GRID',(0,0),(-1,-1),0.5,WHITE),
        ('ROUNDEDCORNERS',[4]),
    ]))
    story.append(st)
    story.append(sp(5))

    story.append(info_box(
        'HOW TO USE THIS DOCUMENT: This is your personal field manual for the next 6 months. '
        'Read the Career Map first (Chapter 1) to understand the destination. '
        'Then follow Chapter 7 (Semester 7 Plan) week by week. '
        'Use Chapters 2-6 as deep-dive references when you reach each topic. '
        'Chapter 8 is your placement preparation guide — start reading it from Month 5 onwards. '
        'Every single week: push code to GitHub, study one topic, answer 10 interview questions on paper.', 'info'))

    story.append(PageBreak())

    # ── TABLE OF CONTENTS ────────────────────────────────────────────────────
    story.append(section_header('TABLE OF CONTENTS'))
    story.append(sp(3))
    toc_data = [
        ('1.', 'Career Map — Embedded vs Firmware Engineering', '3'),
        ('2.', 'C Programming Mastery', '5'),
        ('3.', 'Embedded C — Bare-Metal Concepts', '7'),
        ('4.', 'STM32 Microcontroller Roadmap', '9'),
        ('5.', 'Communication Protocols (UART, SPI, I2C, CAN, Modbus)', '12'),
        ('6.', 'FreeRTOS — Real-Time Operating System', '15'),
        ('7.', 'Semester 7 Week-by-Week Plan (June–November 2026)', '17'),
        ('8.', 'Free Learning Resources', '23'),
        ('9.', 'Flagship Projects — Architecture & Resume Bullets', '25'),
        ('10.', 'Placement Preparation & Interview Questions', '28'),
        ('11.', 'Linux for Embedded Engineers', '32'),
        ('12.', 'Automotive Embedded Systems (CAN, UDS, AUTOSAR)', '34'),
        ('13.', 'Resume Transformation Guide', '36'),
    ]
    for num, title, page in toc_data:
        row_t = Table([[
            Paragraph(f'<b>{num}</b>', s['body']),
            Paragraph(title, s['body']),
            Paragraph(page, ParagraphStyle('tocpg', fontSize=8.5, alignment=TA_RIGHT, textColor=GRAY_DARK)),
        ]], colWidths=[8*mm, 138*mm, 14*mm])
        row_t.setStyle(TableStyle([
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('LEFTPADDING',(0,0),(-1,-1),2),
            ('TOPPADDING',(0,0),(-1,-1),2),
            ('BOTTOMPADDING',(0,0),(-1,-1),2),
            ('LINEBELOW',(0,0),(-1,0),0.3,colors.HexColor('#EEEEEE')),
        ]))
        story.append(row_t)

    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════════
    # CHAPTER 1 — CAREER MAP
    # ════════════════════════════════════════════════════════════════════════
    story.append(section_header('CHAPTER 1 — CAREER MAP: EMBEDDED vs FIRMWARE ENGINEERING'))
    story.append(sp(3))

    story.append(Paragraph('What is the difference between Embedded and Firmware roles?', s['h2']))
    diff_data = [
        [Paragraph('<b>Embedded Systems Engineer</b>', s['h3']),
         Paragraph('<b>Firmware Engineer</b>', s['h3'])],
        [Paragraph('Closer to hardware. Works on board bring-up, BSP (Board Support Package), peripheral drivers, bootloaders, power management. Needs to read schematics and understand hardware even without designing PCBs. Deep knowledge of MCU architecture required.', s['body']),
         Paragraph('Closer to software running on constrained hardware. Works on application firmware, state machines, communication stacks, OTA updates, diagnostics, and feature implementation. Needs strong C/C++, RTOS, and protocol knowledge.', s['body'])],
        [Paragraph('<b>Domains:</b> Industrial automation, Automotive ECU, Medical devices, Defence', s['small']),
         Paragraph('<b>Domains:</b> IoT products, Consumer electronics, Automotive ECU software, Robotics', s['small'])],
        [Paragraph('<b>Key skills:</b> C, CMSIS, HAL drivers, JTAG/SWD debug, linker scripts, memory map', s['small']),
         Paragraph('<b>Key skills:</b> C/C++, FreeRTOS, protocols, state machines, OTA, diagnostics', s['small'])],
    ]
    diff_t = Table(diff_data, colWidths=[80*mm, 80*mm])
    diff_t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(0,0), LIGHT_BLUE),
        ('BACKGROUND',(1,0),(1,0), LIGHT_GREEN),
        ('GRID',(0,0),(-1,-1),0.5,colors.HexColor('#DDDDDD')),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('LEFTPADDING',(0,0),(-1,-1),6),
        ('RIGHTPADDING',(0,0),(-1,-1),6),
        ('TOPPADDING',(0,0),(-1,-1),4),
        ('BOTTOMPADDING',(0,0),(-1,-1),4),
    ]))
    story.append(diff_t)
    story.append(sp(4))

    story.append(Paragraph('What companies expect from freshers — by sector', s['h2']))
    exp_data = [
        [Paragraph('<b>Company Type</b>', s['small']), Paragraph('<b>Minimum Bar</b>', s['small']), Paragraph('<b>Good to Have</b>', s['small'])],
        [Paragraph('Automotive (Bosch, Continental, Valeo, MSIL, Tata Elxsi)', s['small']),
         Paragraph('C, Embedded C, CAN, UART, basic AUTOSAR awareness', s['small']),
         Paragraph('UDS, CANdb++, MISRA-C, Vector tools', s['small'])],
        [Paragraph('Industrial (Honeywell, Siemens, Rockwell)', s['small']),
         Paragraph('C, Modbus/RS-485, bare-metal drivers, RTOS basics', s['small']),
         Paragraph('PLC awareness, IEC 61508 safety basics', s['small'])],
        [Paragraph('IoT / Consumer (Nordic, TI, startups)', s['small']),
         Paragraph('C/C++, BLE/Wi-Fi stack usage, FreeRTOS, OTA', s['small']),
         Paragraph('Zephyr RTOS, cloud integration, power optimization', s['small'])],
        [Paragraph('Semiconductor AE/FAE (STMicro, NXP, Microchip)', s['small']),
         Paragraph('C, peripheral drivers, debugger fluency', s['small']),
         Paragraph('Oscilloscope/LA usage, application notes literacy', s['small'])],
    ]
    exp_t = Table(exp_data, colWidths=[48*mm, 62*mm, 50*mm])
    exp_t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0), NAVY),
        ('TEXTCOLOR',(0,0),(-1,0), WHITE),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE, GRAY_BG]),
        ('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#DDDDDD')),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('LEFTPADDING',(0,0),(-1,-1),5),
        ('TOPPADDING',(0,0),(-1,-1),4),
        ('BOTTOMPADDING',(0,0),(-1,-1),4),
    ]))
    story.append(exp_t)
    story.append(sp(3))

    story.append(Paragraph('Salary expectations for freshers (India, 2025-26)', s['h2']))
    sal_data = [
        [Paragraph('<b>Role / Company Tier</b>', s['small']), Paragraph('<b>CTC Range</b>', s['small'])],
        [Paragraph('Automotive Tier-1 (Bosch, Continental, Valeo)', s['small']), Paragraph('10 – 18 LPA', s['small'])],
        [Paragraph('Service companies (Tata Elxsi, KPIT, L&T Technology)', s['small']), Paragraph('6 – 12 LPA', s['small'])],
        [Paragraph('Product / MNC India R&D (STMicro, NXP, Qualcomm IoT)', s['small']), Paragraph('14 – 25 LPA', s['small'])],
        [Paragraph('Industrial / mid-sized (Honeywell, Emerson, ABB)', s['small']), Paragraph('8 – 15 LPA', s['small'])],
        [Paragraph('IoT / Robotics startups', s['small']), Paragraph('6 – 14 LPA + equity', s['small'])],
    ]
    sal_t = Table(sal_data, colWidths=[120*mm, 40*mm])
    sal_t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0), DARK_BLUE),
        ('TEXTCOLOR',(0,0),(-1,0), WHITE),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE, GRAY_BG]),
        ('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#DDDDDD')),
        ('LEFTPADDING',(0,0),(-1,-1),6),
        ('TOPPADDING',(0,0),(-1,-1),4),
        ('BOTTOMPADDING',(0,0),(-1,-1),4),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ]))
    story.append(sal_t)
    story.append(sp(3))
    story.append(info_box('YOUR EDGE: Your MSIL internship is your biggest differentiator. A 4th-year student who has worked with Motor Test Bench systems at an automotive OEM is rare. Leverage this in every interview — it signals real-world industrial experience that most freshers simply do not have.', 'tip'))

    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════════
    # CHAPTER 2 — C PROGRAMMING
    # ════════════════════════════════════════════════════════════════════════
    story.append(section_header('CHAPTER 2 — C PROGRAMMING MASTERY'))
    story.append(sp(3))
    story.append(info_box('Master C before touching STM32. Most embedded interview failures happen at C fundamentals, not hardware knowledge. Budget 4 weeks (all of June) for this chapter.', 'warn'))
    story.append(sp(2))

    phases = [
        ('Phase 1 — Foundations (Week 1)', BLUE, [
            ('Data types & sizes', 'Know sizeof() result for every type on a 32-bit ARM MCU. char=1, short=2, int=4, long=4, long long=8. Always use stdint.h types: uint8_t, uint16_t, uint32_t, int32_t etc.'),
            ('Operators', 'Master all bitwise operators: & (AND), | (OR), ^ (XOR), ~ (NOT), << (left shift), >> (right shift). These are used in every register operation.'),
            ('Control flow', 'if/switch/for/while — know which the compiler optimizes better for embedded (switch over long if-else chains).'),
            ('Functions', 'Call stack mechanics, return values, pass by value vs pass by pointer. Understand that large structs should be passed by pointer, not by value.'),
        ]),
        ('Phase 2 — Pointers (Week 2) — MOST CRITICAL', RED, [
            ('Pointer arithmetic', 'What ptr++ actually does depends on the type. int *p; p++ moves 4 bytes, not 1. This is fundamental.'),
            ('Pointer to pointer, void pointer, function pointer', 'All three appear in real embedded code. Function pointers are used for state machines and callback registrations.'),
            ('const with pointers — 4 combinations', 'const int *p = read-only data. int * const p = fixed address. const int * const p = both fixed. int *p = mutable. Know all four cold.'),
            ('malloc/free', 'Understand heap fragmentation. In safety-critical embedded code (automotive MISRA-C), dynamic allocation is FORBIDDEN. Use static allocation only.'),
            ('Stack vs Heap vs BSS vs .data vs .text', 'Know what goes in each segment. Local variables = stack. Global initialized = .data. Global uninitialized = BSS. Constants = .rodata. Code = .text.'),
        ]),
        ('Phase 3 — Embedded-Specific C (Week 3)', AMBER, [
            ('volatile keyword', 'Tells the compiler: do NOT cache this variable in a register — re-read from memory every time. Required for ALL hardware registers and any variable modified in an ISR.'),
            ('const volatile', 'Read-only from software perspective but can still change by hardware. Used for read-only status registers.'),
            ('static — 3 meanings', '1) Static local variable: persists between function calls. 2) Static global/function: limits scope to that .c file (like private in C++). 3) In C++ classes: shared across all instances.'),
            ('Bit fields in structs', 'struct { uint8_t flag1:1; uint8_t flag2:3; uint8_t val:4; }; — use for register modeling. But be aware of alignment and endianness gotchas.'),
            ('Inline functions vs macros', 'Prefer inline for type safety and debuggability. Use macros only for register bit-mask definitions.'),
        ]),
        ('Phase 4 — Data Structures in C (Week 4)', GREEN, [
            ('Circular / ring buffer', 'THE most important data structure in embedded systems. Used for UART Rx buffers, sensor data queues, log buffers. Implement it from scratch: head index, tail index, size must be power of 2 for fast modulo.'),
            ('Linked list', 'Used in OS task lists, memory pool management. Implement singly and doubly linked list.'),
            ('State machine', 'Implement using either switch-case or function pointer table. Function pointer table is the professional approach. Every protocol parser and UI flow uses a state machine.'),
            ('Lookup tables', 'const arrays in flash (.rodata) for fast computation — sin/cos tables, CRC tables, ADC calibration curves.'),
        ]),
    ]

    phase_colors = [BLUE, RED, AMBER, GREEN]
    phase_bgs = [LIGHT_BLUE, LIGHT_RED, LIGHT_AMBER, LIGHT_GREEN]
    phase_fgs = [DARK_BLUE, DARK_RED, DARK_AMBER, DARK_GREEN]

    for i, (phase_name, pc, items) in enumerate(phases):
        bg = phase_bgs[i]; fg = phase_fgs[i]; bar = phase_colors[i]
        header_t = Table([[Paragraph(f'<font color="white"><b>{phase_name}</b></font>', s['h3'])]], colWidths=[160*mm], rowHeights=[7*mm])
        header_t.setStyle(TableStyle([('BACKGROUND',(0,0),(0,0),bar),('LEFTPADDING',(0,0),(0,0),6),('TOPPADDING',(0,0),(0,0),2),('BOTTOMPADDING',(0,0),(0,0),2)]))
        story.append(header_t)
        for topic, detail in items:
            row = Table([[Paragraph(f'<b>{topic}</b>', s['small']), Paragraph(detail, s['small'])]], colWidths=[42*mm, 118*mm])
            row.setStyle(TableStyle([
                ('BACKGROUND',(0,0),(0,0),bg),
                ('BACKGROUND',(1,0),(1,0),WHITE),
                ('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#DDDDDD')),
                ('VALIGN',(0,0),(-1,-1),'TOP'),
                ('LEFTPADDING',(0,0),(-1,-1),6),
                ('TOPPADDING',(0,0),(-1,-1),3),
                ('BOTTOMPADDING',(0,0),(-1,-1),3),
            ]))
            story.append(row)
        story.append(sp(3))

    story.append(Paragraph('Critical C code patterns for embedded interviews', s['h2']))
    code_snippets = [
        ('Bit manipulation — set, clear, toggle, check', '''// Set bit N
reg |= (1U << N);
// Clear bit N
reg &= ~(1U << N);
// Toggle bit N
reg ^= (1U << N);
// Check bit N
if (reg & (1U << N)) { /* bit is set */ }
// Always use 1U not 1 — avoids signed shift undefined behaviour'''),
        ('Memory-mapped register access pattern', '''#define GPIOA_BASE  0x40020000U
#define GPIOA_MODER (*(volatile uint32_t*)(GPIOA_BASE + 0x00))
#define GPIOA_ODR   (*(volatile uint32_t*)(GPIOA_BASE + 0x14))
// Set PA5 as output: MODER bits [11:10] = 01
GPIOA_MODER &= ~(0x3U << 10);
GPIOA_MODER |=  (0x1U << 10);'''),
        ('Circular buffer implementation', '''#define BUF_SIZE 64  // must be power of 2
volatile uint8_t  buf[BUF_SIZE];
volatile uint8_t  head = 0, tail = 0;
void buf_put(uint8_t d) { buf[head++ & (BUF_SIZE-1)] = d; }
uint8_t buf_get(void)   { return buf[tail++ & (BUF_SIZE-1)]; }
uint8_t buf_empty(void) { return head == tail; }'''),
    ]
    for title, code in code_snippets:
        story.append(Paragraph(title, s['h3']))
        story.append(Paragraph(code.replace('\n','<br/>').replace(' ','&nbsp;'), s['code']))
        story.append(sp(2))

    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════════
    # CHAPTER 3 — EMBEDDED C
    # ════════════════════════════════════════════════════════════════════════
    story.append(section_header('CHAPTER 3 — EMBEDDED C: BARE-METAL CONCEPTS'))
    story.append(sp(3))

    story.append(Paragraph('Memory segments on a Cortex-M MCU', s['h2']))
    seg_data = [
        [Paragraph('<b>Segment</b>',s['small']), Paragraph('<b>Location</b>',s['small']), Paragraph('<b>Contents</b>',s['small']), Paragraph('<b>Keyword</b>',s['small'])],
        [Paragraph('.text',s['small']), Paragraph('Flash ROM',s['small']), Paragraph('Compiled code, const strings',s['small']), Paragraph('—',s['small'])],
        [Paragraph('.rodata',s['small']), Paragraph('Flash ROM',s['small']), Paragraph('Read-only constants, lookup tables',s['small']), Paragraph('const',s['small'])],
        [Paragraph('.data',s['small']), Paragraph('RAM (copied from Flash on boot)',s['small']), Paragraph('Initialized global/static variables',s['small']), Paragraph('—',s['small'])],
        [Paragraph('.bss',s['small']), Paragraph('RAM (zeroed on boot)',s['small']), Paragraph('Uninitialized global/static variables',s['small']), Paragraph('—',s['small'])],
        [Paragraph('Stack',s['small']), Paragraph('RAM (grows downward)',s['small']), Paragraph('Local variables, function call frames',s['small']), Paragraph('auto (default)',s['small'])],
        [Paragraph('Heap',s['small']), Paragraph('RAM (grows upward)',s['small']), Paragraph('Dynamic allocation — AVOID in embedded',s['small']), Paragraph('malloc/free',s['small'])],
    ]
    seg_t = Table(seg_data, colWidths=[22*mm, 48*mm, 66*mm, 24*mm])
    seg_t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),NAVY), ('TEXTCOLOR',(0,0),(-1,0),WHITE),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE, GRAY_BG]),
        ('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#CCCCCC')),
        ('LEFTPADDING',(0,0),(-1,-1),5), ('TOPPADDING',(0,0),(-1,-1),3),
        ('BOTTOMPADDING',(0,0),(-1,-1),3), ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ]))
    story.append(seg_t)
    story.append(sp(3))

    story.append(Paragraph('Interrupt Service Routines — golden rules', s['h2']))
    isr_rules = [
        'ISRs must be FAST — set a flag or copy data, then return. Signal the main loop or an RTOS task to do the heavy work.',
        'Never call blocking functions in an ISR — no printf(), no malloc(), no HAL_Delay(), no RTOS APIs (except FromISR variants like xQueueSendFromISR).',
        'All variables shared between ISR and main code MUST be declared volatile. Without volatile, the compiler may cache the value in a register and never re-read it.',
        'Use critical sections (__disable_irq() / __enable_irq()) to protect multi-byte shared data from being partially updated during an interrupt.',
        'Understand NVIC (Nested Vectored Interrupt Controller) — priority levels 0 (highest) to 15 (lowest). Higher number = lower priority on Cortex-M.',
        'Every ISR on Cortex-M pushes 8 registers automatically onto the stack on entry and pops them on exit — this takes ~12 clock cycles.',
    ]
    for rule in isr_rules:
        story.append(bullet(rule, s))
    story.append(sp(3))

    story.append(Paragraph('MISRA-C key rules for automotive embedded code', s['h2']))
    misra_data = [
        [Paragraph('<b>Rule</b>',s['small']), Paragraph('<b>Requirement</b>',s['small']), Paragraph('<b>Why it matters</b>',s['small'])],
        [Paragraph('No dynamic allocation',s['small']), Paragraph('No malloc/calloc/free after init',s['small']), Paragraph('Prevents heap fragmentation, non-determinism',s['small'])],
        [Paragraph('No recursion',s['small']), Paragraph('Functions must not call themselves',s['small']), Paragraph('Stack depth becomes unbounded, unpredictable',s['small'])],
        [Paragraph('stdint types always',s['small']), Paragraph('Use uint8_t not unsigned char',s['small']), Paragraph('Portability across 8/16/32-bit architectures',s['small'])],
        [Paragraph('No unreachable code',s['small']), Paragraph('Every code path must be reachable',s['small']), Paragraph('Dead code indicates logic errors',s['small'])],
        [Paragraph('Explicit casts',s['small']), Paragraph('Never rely on implicit type conversion',s['small']), Paragraph('Prevents silent data truncation bugs',s['small'])],
    ]
    misra_t = Table(misra_data, colWidths=[38*mm, 64*mm, 58*mm])
    misra_t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),DARK_AMBER), ('TEXTCOLOR',(0,0),(-1,0),WHITE),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE, LIGHT_AMBER]),
        ('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#CCCCCC')),
        ('LEFTPADDING',(0,0),(-1,-1),5), ('TOPPADDING',(0,0),(-1,-1),3),
        ('BOTTOMPADDING',(0,0),(-1,-1),3), ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))
    story.append(misra_t)
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════════
    # CHAPTER 4 — STM32
    # ════════════════════════════════════════════════════════════════════════
    story.append(section_header('CHAPTER 4 — STM32 MICROCONTROLLER ROADMAP'))
    story.append(sp(3))

    story.append(info_box('RECOMMENDED BOARD: STM32F446RE Nucleo (~₹1,500–2,000 on Robu.in or Amazon). It has an onboard ST-Link debugger, CAN controller, 180 MHz Cortex-M4, FPU, and all major peripherals. Buy it at the START of July along with: 8-channel logic analyzer clone (~₹400), CP2102 USB-UART adapter (~₹150), MCP2551 CAN transceiver module (~₹200).', 'warn'))
    story.append(sp(2))

    story.append(Paragraph('Learning order — follow this EXACTLY, do not skip steps', s['h2']))
    stm_order = [
        ('1', 'GPIO — bare-metal', '3 days', 'Write to MODER and ODR registers directly. Blink LED WITHOUT HAL. Read button state from IDR. Enable RCC clock for GPIOA first.'),
        ('2', 'Clock tree (RCC)', '2 days', 'Understand HSI/HSE/PLL, AHB/APB1/APB2 prescalers. Every peripheral gets its clock from this tree. Wrong clock = peripheral not working.'),
        ('3', 'UART — polling → ISR → DMA', '5 days', 'Polling first, then ISR-driven Rx with circular buffer, then DMA. Implement printf retargeting so you can use printf() for debug output.'),
        ('4', 'Timers + PWM', '5 days', 'Basic timer interrupt, PWM output (LED fade), input capture (frequency measurement). Understand prescaler and ARR register calculations.'),
        ('5', 'ADC — single → multi-channel → DMA', '4 days', 'Single channel polling, scan mode, then continuous DMA. Software averaging filter. Foundation for Motor DAS project.'),
        ('6', 'SPI — bit-bang then hardware', '4 days', 'Bit-bang SPI first to understand CPOL/CPHA. Then hardware SPI to read MAX31855 thermocouple or similar sensor.'),
        ('7', 'I2C — scan + sensor', '4 days', 'I2C scanner to find device addresses. Read/write to OLED or IMU. Understand pull-up resistors, ACK/NACK, clock stretching.'),
        ('8', 'DMA — all peripherals', '5 days', 'Memory-to-memory copy, UART Tx/Rx with DMA, ADC continuous with DMA. This is critical for the Motor DAS project.'),
        ('9', 'CAN Bus', '7 days', 'Loopback mode first, then 2-node with MCP2551 transceivers. CAN filter configuration. Error frame handling. See Chapter 5.'),
        ('10', 'FreeRTOS on STM32', '10 days', 'Tasks, queues, semaphores, mutexes. See Chapter 6. Only start after being comfortable with all above peripherals.'),
        ('11', 'Watchdog + Power modes', '4 days', 'IWDG, WWDG independent/window watchdogs. Sleep/Stop/Standby power modes. Production firmware always has a watchdog.'),
    ]
    stm_t_data = [[Paragraph('<b>#</b>',s['small']), Paragraph('<b>Topic</b>',s['small']), Paragraph('<b>Time</b>',s['small']), Paragraph('<b>Key goal</b>',s['small'])]]
    for num, topic, time, goal in stm_order:
        stm_t_data.append([Paragraph(num,s['small']), Paragraph(f'<b>{topic}</b>',s['small']), Paragraph(time,s['small']), Paragraph(goal,s['small'])])
    stm_t = Table(stm_t_data, colWidths=[8*mm, 38*mm, 16*mm, 98*mm])
    stm_t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),NAVY), ('TEXTCOLOR',(0,0),(-1,0),WHITE),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE, GRAY_BG]),
        ('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#CCCCCC')),
        ('LEFTPADDING',(0,0),(-1,-1),5), ('TOPPADDING',(0,0),(-1,-1),3),
        ('BOTTOMPADDING',(0,0),(-1,-1),3), ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('ALIGN',(0,0),(0,-1),'CENTER'), ('ALIGN',(2,0),(2,-1),'CENTER'),
    ]))
    story.append(stm_t)
    story.append(sp(3))
    story.append(info_box('THE MOST IMPORTANT RULE: Start with bare-metal GPIO (no HAL, no CubeMX) before using the HAL library. When an interviewer asks "what does HAL_GPIO_WritePin() actually do?", you should answer: "It sets the corresponding bit in the BSRR register of the GPIO port." That one answer puts you ahead of 90% of candidates.', 'crit'))
    story.append(sp(2))

    story.append(Paragraph('Hard Fault handler — implement this on Day 1', s['h2']))
    hf_code = '''void HardFault_Handler(void) {
    __asm volatile (
        "TST LR, #4 \\n"
        "ITE EQ \\n"
        "MRSEQ R0, MSP \\n"   // Main Stack Pointer
        "MRSNE R0, PSP \\n"   // Process Stack Pointer
        "B HardFault_Decode \\n"
    );
}
void HardFault_Decode(uint32_t *stack) {
    volatile uint32_t pc   = stack[6]; // PC at time of fault
    volatile uint32_t cfsr = SCB->CFSR; // Cause of fault
    while(1); // Set breakpoint here — read pc in debugger, find in .map file
}'''
    story.append(Paragraph(hf_code.replace('\n','<br/>').replace(' ','&nbsp;').replace('<','&lt;').replace('>','&gt;'), s['code']))
    story.append(info_box('Add this Hard Fault handler to every STM32 project from day one. When your code crashes (and it will), this tells you exactly which line caused it. Finding the faulting PC in the .map file is a critical debug skill.', 'tip'))

    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════════
    # CHAPTER 5 — PROTOCOLS
    # ════════════════════════════════════════════════════════════════════════
    story.append(section_header('CHAPTER 5 — COMMUNICATION PROTOCOLS'))
    story.append(sp(3))

    protocols = [
        ('UART — Universal Asynchronous Receiver Transmitter', BLUE, LIGHT_BLUE, DARK_BLUE, [
            ('Theory', 'Asynchronous — no shared clock. Both sides agree on baud rate in advance. Frame: start bit + 8 data bits + optional parity + stop bit(s) = "8N1" most common. Baud rate error must be less than 2%. Full duplex — can transmit and receive simultaneously.'),
            ('Key parameters', 'Baud rate (9600, 115200, 921600), data bits (8), parity (none/even/odd), stop bits (1/2), flow control (none/RTS-CTS). 115200 baud is standard for debug output.'),
            ('STM32 usage', 'Three modes: polling (HAL_UART_Transmit), interrupt-driven (HAL_UART_Receive_IT + callback), DMA (HAL_UART_Receive_DMA). Use DMA for high-speed or continuous reception. Implement circular buffer for Rx.'),
            ('Interview questions', 'Why is UART asynchronous? What causes framing errors? Why use DMA for high-speed UART? What is baud rate error and acceptable tolerance? How does flow control work?'),
        ]),
        ('SPI — Serial Peripheral Interface', PURPLE, LIGHT_PURPLE, DARK_PURPLE, [
            ('Theory', '4 wires: MOSI (Master Out Slave In), MISO (Master In Slave Out), SCLK (clock), CS (chip select, active low). Full duplex. Multiple slaves possible with separate CS pins. No addressing — CS selects the device.'),
            ('CPOL and CPHA', 'CPOL (Clock Polarity): idle state of clock — 0=idle low, 1=idle high. CPHA (Clock Phase): 0=sample on first edge, 1=sample on second edge. Mode 0 (CPOL=0, CPHA=0) is most common. Always check your sensor datasheet.'),
            ('STM32 usage', 'HAL_SPI_TransmitReceive() for full duplex. Always bit-bang SPI once manually before using hardware SPI — this builds deep understanding. Typical sensors: MAX31855 (thermocouple), ADXL345 (accelerometer), W25Q (flash memory).'),
            ('Interview questions', 'SPI vs I2C — when to choose which? What is CPOL/CPHA? How do you handle multiple slaves? Why is SPI faster than I2C?'),
        ]),
        ('I2C — Inter-Integrated Circuit', GREEN, LIGHT_GREEN, DARK_GREEN, [
            ('Theory', '2 wires: SDA (data) and SCL (clock). Multi-master capable. 7-bit or 10-bit device addressing — up to 128 devices on one bus. Open-drain lines — MUST have pull-up resistors (typically 4.7kΩ for 100kHz, 2.2kΩ for 400kHz).'),
            ('Protocol flow', 'Write: START | ADDR+W | ACK | REG_ADDR | ACK | DATA | ACK | STOP. Read: START | ADDR+W | ACK | REG_ADDR | ACK | REPEATED_START | ADDR+R | ACK | DATA | NACK | STOP.'),
            ('STM32 usage', 'HAL_I2C_Mem_Write() and HAL_I2C_Mem_Read(). Always implement an I2C scanner first to verify device address. Common sensors: SSD1306 OLED, MPU6050 IMU, BMP280 pressure, DS3231 RTC.'),
            ('Interview questions', 'What is clock stretching? What causes I2C bus lockup and how do you recover? How to scan for I2C devices? When would you use I2C vs SPI?'),
        ]),
        ('CAN Bus — Controller Area Network', RED, LIGHT_RED, DARK_RED, [
            ('Theory', '2 wires: CANH and CANL (differential pair). Multi-master, message-based (no master/slave). 11-bit standard or 29-bit extended IDs. Lower ID = higher priority. Speed: 125kbps to 1Mbps. Built-in error detection: CRC, bit stuffing, ACK, form check.'),
            ('Arbitration', 'All nodes transmit simultaneously. Dominant bit (logic 0) overwrites recessive bit (logic 1). Node transmitting recessive but reading dominant loses arbitration and stops. This is non-destructive — the winning message continues without corruption.'),
            ('Error states', 'Error Active (normal) → Error Passive (too many errors, transmits passive error flag) → Bus Off (node removed from bus, 128 × 11 recessive bits to recover). Error counters: TEC and REC.'),
            ('STM32 + transceiver', 'STM32 has built-in CAN controller but needs external transceiver IC for physical layer. Use MCP2551 or TJA1050. Connect: STM32 CAN_TX → transceiver TXD, CAN_RX → RXD, CANH/CANL on bus.'),
            ('Interview questions', 'How does CAN arbitration work? What is bit stuffing? Explain error passive vs bus off. What is the maximum data payload? What is CAN FD?'),
        ]),
        ('RS-485 / Modbus RTU — Your MSIL context', AMBER, LIGHT_AMBER, DARK_AMBER, [
            ('RS-485 physical layer', 'Differential signaling like CAN but simpler. Half-duplex typical. Up to 32 nodes on one bus, up to 1200m cable length. Needs a direction-control pin (DE/RE) to switch between transmit and receive. Common in industrial automation.'),
            ('Modbus RTU', 'Application protocol running over RS-485. Master-slave architecture. Master sends request, slave responds. Key function codes: 0x03 Read Holding Registers, 0x06 Write Single Register, 0x10 Write Multiple Registers, 0x04 Read Input Registers.'),
            ('Frame structure', 'Slave Address (1 byte) | Function Code (1 byte) | Data (N bytes) | CRC-16 (2 bytes). Response has same structure. Silent interval of 3.5 character times marks start/end of frame.'),
            ('Your MSIL connection', 'Industrial test equipment at MSIL likely uses Modbus RTU over RS-485 to communicate with SCADA. Your Motor DAS project implements a Modbus slave — directly applicable to what you observed at MSIL.'),
        ]),
    ]

    for proto_name, bar_c, bg_c, text_c, items in protocols:
        ph = Table([[Paragraph(f'<font color="white"><b>{proto_name}</b></font>', s['h3'])]], colWidths=[160*mm], rowHeights=[7*mm])
        ph.setStyle(TableStyle([('BACKGROUND',(0,0),(0,0),bar_c),('LEFTPADDING',(0,0),(0,0),6),('TOPPADDING',(0,0),(0,0),2),('BOTTOMPADDING',(0,0),(0,0),2)]))
        story.append(ph)
        for label, detail in items:
            pr = Table([[Paragraph(f'<b>{label}</b>',s['small']), Paragraph(detail,s['small'])]], colWidths=[30*mm, 130*mm])
            pr.setStyle(TableStyle([
                ('BACKGROUND',(0,0),(0,0),bg_c),
                ('BACKGROUND',(1,0),(1,0),WHITE),
                ('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#DDDDDD')),
                ('LEFTPADDING',(0,0),(-1,-1),5), ('TOPPADDING',(0,0),(-1,-1),3),
                ('BOTTOMPADDING',(0,0),(-1,-1),3), ('VALIGN',(0,0),(-1,-1),'TOP'),
            ]))
            story.append(pr)
        story.append(sp(4))

    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════════
    # CHAPTER 6 — FREERTOS
    # ════════════════════════════════════════════════════════════════════════
    story.append(section_header('CHAPTER 6 — FREERTOS: REAL-TIME OPERATING SYSTEM'))
    story.append(sp(3))
    story.append(info_box('WHEN TO START: Only begin FreeRTOS after you can comfortably write STM32 peripheral code on your own — GPIO, UART, SPI, ADC without help. Without that foundation, RTOS concepts will not stick. Target: September (Month 4 of your plan).', 'warn'))
    story.append(sp(2))

    story.append(Paragraph('Core FreeRTOS concepts — learning order', s['h2']))
    rtos_concepts = [
        ('Tasks', 'Independent threads of execution. Each task has its own stack. Created with xTaskCreate(). Priority 0 = lowest, configMAX_PRIORITIES-1 = highest. Use vTaskDelay(pdMS_TO_TICKS(100)) for delays — never HAL_Delay() in RTOS.', 'Implement 2 tasks at different priorities. Use oscilloscope or UART timestamps to verify preemption.'),
        ('Scheduler', 'Preemptive by default. Tick interrupt (configTICK_RATE_HZ, usually 1000Hz = 1ms tick) triggers scheduler. Higher priority task always runs first. Equal priority tasks share CPU round-robin.', 'What is configMINIMAL_STACK_SIZE? What is the tick period? How does preemption work?'),
        ('Queues', 'THE correct way to pass data between tasks. Thread-safe. Can block sender when full, block receiver when empty. xQueueCreate(), xQueueSend(), xQueueReceive(). From ISR: xQueueSendFromISR().', 'Build ADC-task → queue → UART-task pipeline. This is the fundamental RTOS pattern.'),
        ('Binary Semaphores', 'Signalling mechanism — typically from ISR to task. ISR gives semaphore, task takes it and processes. xSemaphoreCreateBinary(), xSemaphoreGive(), xSemaphoreTake(). From ISR: xSemaphoreGiveFromISR().', 'Why not use a global flag instead of semaphore? What is the difference between binary semaphore and mutex?'),
        ('Mutexes', 'Mutual exclusion — protect shared resources (e.g. shared SPI bus, shared UART). xSemaphoreCreateMutex(). FreeRTOS mutex has priority inheritance to help avoid priority inversion. NEVER take mutex in ISR.', 'Explain priority inversion with a real example. What is priority inheritance? Why no mutex in ISR?'),
        ('Event Groups', 'Wait for multiple events simultaneously. xEventGroupCreate(), xEventGroupSetBits(), xEventGroupWaitBits(). Example: wait for SENSOR_READY AND COMMAND_RECEIVED before proceeding.', 'Event group vs multiple semaphores — when to prefer each?'),
        ('Software Timers', 'Execute a callback after a period. Does NOT block. Runs from timer daemon task. xTimerCreate(), xTimerStart(). Use for periodic telemetry, watchdog petting, LED blink.', 'Software timer vs hardware timer — what are the limitations of SW timers?'),
    ]
    for concept, detail, interview in rtos_concepts:
        ct = Table([[Paragraph(f'<b>{concept}</b>',s['small']), Paragraph(detail,s['small']), Paragraph(f'<i>{interview}</i>',s['small'])]],
                   colWidths=[24*mm, 88*mm, 48*mm])
        ct.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(0,0),LIGHT_GREEN),
            ('BACKGROUND',(1,0),(1,0),WHITE),
            ('BACKGROUND',(2,0),(2,0),LIGHT_BLUE),
            ('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#DDDDDD')),
            ('LEFTPADDING',(0,0),(-1,-1),5), ('TOPPADDING',(0,0),(-1,-1),3),
            ('BOTTOMPADDING',(0,0),(-1,-1),3), ('VALIGN',(0,0),(-1,-1),'TOP'),
        ]))
        story.append(ct)

    story.append(sp(3))
    story.append(Paragraph('Bare-metal vs FreeRTOS — when to use each', s['h2']))
    bm_rtos = [
        [Paragraph('<b>Use bare-metal when:</b>',s['h3']), Paragraph('<b>Use FreeRTOS when:</b>',s['h3'])],
        [Paragraph('Single main loop with ISR-driven events is sufficient',s['small']),
         Paragraph('Multiple concurrent activities with different timing requirements',s['small'])],
        [Paragraph('Fewer than 3 concurrent activities',s['small']),
         Paragraph('Need deterministic timing guarantees for multiple tasks',s['small'])],
        [Paragraph('Very small MCU (less than 8KB RAM)',s['small']),
         Paragraph('Complex state management across independent modules',s['small'])],
        [Paragraph('Ultra-low latency required (sub-microsecond response)',s['small']),
         Paragraph('TCP/IP stack, USB stack, filesystem (FatFS) present',s['small'])],
        [Paragraph('Simple sensor read + single output',s['small']),
         Paragraph('Your Motor Test Bench DAS project — use RTOS!',s['small'])],
    ]
    bm_t = Table(bm_rtos, colWidths=[80*mm, 80*mm])
    bm_t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(0,0),LIGHT_AMBER), ('BACKGROUND',(1,0),(1,0),LIGHT_GREEN),
        ('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#DDDDDD')),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE, GRAY_BG]),
        ('LEFTPADDING',(0,0),(-1,-1),6), ('TOPPADDING',(0,0),(-1,-1),3),
        ('BOTTOMPADDING',(0,0),(-1,-1),3), ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))
    story.append(bm_t)

    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════════
    # CHAPTER 7 — SEM 7 WEEK-BY-WEEK PLAN
    # ════════════════════════════════════════════════════════════════════════
    story.append(section_header('CHAPTER 7 — SEMESTER 7 WEEK-BY-WEEK PLAN (JUNE – NOVEMBER 2026)', DARK_GREEN))
    story.append(sp(3))

    # Stats
    plan_stats = [['6 Months', '24 Weeks', '~900 Hours', '2 Flagship\nProjects', 'Job-Ready\nDec 2026']]
    ps_t = Table(plan_stats, colWidths=[32*mm]*5, rowHeights=[14*mm])
    ps_t.setStyle(TableStyle([
        ('BACKGROUND',(i,0),(i,0),[LIGHT_BLUE,LIGHT_GREEN,LIGHT_AMBER,LIGHT_PURPLE,LIGHT_RED][i]) for i in range(5)
    ] + [
        ('TEXTCOLOR',(i,0),(i,0),[DARK_BLUE,DARK_GREEN,DARK_AMBER,DARK_PURPLE,DARK_RED][i]) for i in range(5)
    ] + [
        ('FONTNAME',(0,0),(-1,-1),'Helvetica-Bold'), ('FONTSIZE',(0,0),(-1,-1),8.5),
        ('ALIGN',(0,0),(-1,-1),'CENTER'), ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('GRID',(0,0),(-1,-1),1,WHITE), ('ROUNDEDCORNERS',[3]),
    ]))
    story.append(ps_t)
    story.append(sp(3))

    # Monthly sections
    months = [
        ('JUNE 2026 — C PROGRAMMING FOUNDATIONS', RED, [
            ('Week 1', 'June 1–7', 'C basics: data types, operators, control flow',
             'sizeof() on every type. Bitwise operators (&, |, ^, ~, <<, >>) until automatic. Write 10 programs daily. Focus: can you set/clear/toggle any bit in a register from memory?'),
            ('Week 2', 'June 8–14', 'Pointers — the most important week of the entire 6 months',
             'Pointer arithmetic, pointer to pointer, void pointer, function pointer. All 4 const+pointer combinations. If you understand this week cold, 50% of embedded interviews are already answered.'),
            ('Week 3', 'June 15–21', 'Memory model + Embedded-specific C keywords',
             'Stack vs heap vs BSS vs .data vs .text. volatile, static (3 uses), extern, const volatile. Packed structs, bit fields. Always use uint8_t not unsigned char.'),
            ('Week 4', 'June 22–30', 'Data structures + State machines — push to GitHub',
             'Implement circular buffer, linked list, queue, and a traffic light FSM using function pointer table. Create GitHub repo "c-embedded-practice" and push all exercises. This is your first GitHub content.'),
        ]),
        ('JULY 2026 — STM32 BARE-METAL (Sem 7 begins)', AMBER, [
            ('Week 5', 'July 1–7', 'STM32 architecture + Clock tree + GPIO BARE-METAL (no HAL!)',
             'Learn Cortex-M4 memory map and vector table. Enable GPIOA clock via RCC register. Blink LED by writing to MODER and ODR directly. Buy hardware: Nucleo board, logic analyzer, CAN transceiver.'),
            ('Week 6', 'July 8–14', 'UART — polling then ISR then DMA',
             'Implement UART transmit by polling first. Then ISR-driven receive with circular buffer. Retarget printf over UART. This UART logger is your debugging tool for every future project.'),
            ('Week 7', 'July 15–21', 'GPIO interrupts + EXTI + Button debounce',
             'Configure EXTI on button pin. Software debounce (time-based and state-based). NVIC priority configuration. Add Hard Fault handler to your project template.'),
            ('Week 8', 'July 22–31', 'Now use STM32CubeIDE + HAL (you have earned it)',
             'Generate code with CubeMX and READ every generated line — you should recognise it all. HAL UART with DMA. Project: UART command parser responding to "LED ON"/"LED OFF". Clean GitHub repo with README.'),
        ]),
        ('AUGUST 2026 — PERIPHERALS DEEP DIVE', BLUE, [
            ('Week 9', 'Aug 1–7', 'Timers + PWM output',
             'Basic timer interrupt at 1Hz. PWM on TIM3 — LED brightness with potentiometer. Timer input capture for frequency measurement. Understand prescaler and ARR calculations from first principles.'),
            ('Week 10', 'Aug 8–14', 'ADC — single channel → multi-channel → DMA continuous',
             'Single channel polling. Multi-channel scan mode. ADC with DMA in continuous mode — this is the Motor DAS foundation. Moving average filter. Log potentiometer + internal temperature simultaneously.'),
            ('Week 11', 'Aug 15–21', 'SPI — bit-bang first then hardware SPI',
             'Bit-bang SPI to understand CPOL/CPHA. Hardware SPI to read thermocouple or any sensor. CS pin management, mode configuration.'),
            ('Week 12', 'Aug 22–31', 'I2C + combined sensor showcase project',
             'I2C with OLED display or IMU. I2C scanner. Weekend project: combine SPI sensor + I2C OLED + ADC + UART logger in one project. Push to GitHub with wiring diagram photo. This is your August showcase.'),
        ]),
        ('SEPTEMBER 2026 — FREERTOS', GREEN, [
            ('Week 13', 'Sep 1–7', 'FreeRTOS basics — tasks and scheduler',
             'Create 2 tasks at different priorities. xTaskCreate, vTaskDelay, task stack sizing. Stack overflow hook. Understand tick interrupt and systick. Observe preemption via UART timestamps.'),
            ('Week 14', 'Sep 8–14', 'Queues — the right way to share data between tasks',
             'ADC task → queue → UART task pipeline at 100Hz. Never use global variables between tasks — always queues. Queue full/empty behavior, blocking timeouts.'),
            ('Week 15', 'Sep 15–21', 'Semaphores + Mutexes — understand deeply',
             'Binary semaphore from UART ISR to processing task. Mutex protecting shared SPI bus. Priority inversion example. This is the most-tested FreeRTOS interview topic.'),
            ('Week 16', 'Sep 22–30', 'FreeRTOS project — 4-task sensor hub',
             '4 tasks: sensor read (ADC+SPI), data processing, UART logger, LED status. Queues between them. Software watchdog timer. Push to GitHub with task architecture diagram in README.'),
        ]),
        ('OCTOBER 2026 — CAN BUS + MOTOR DAS FLAGSHIP PROJECT', PURPLE, [
            ('Week 17', 'Oct 1–7', 'CAN Bus theory — understand every bit',
             'CAN frame structure, arbitration mechanism, error frames, error states (active/passive/bus-off), baud rate calculation. Read the CAN chapter in STM32F446 reference manual cover to cover. No code yet.'),
            ('Week 18', 'Oct 8–14', 'CAN on STM32 — loopback then 2-node',
             'Loopback mode first (no hardware needed). Then wire 2 Nucleo boards with MCP2551 transceivers. Send sensor data between nodes. CAN filter configuration. Use logic analyzer to see frames.'),
            ('Weeks 19–20', 'Oct 15–31', 'BUILD: Motor Test Bench DAS (Flagship Project A)',
             'Two full weeks. Combine: ADC DMA (current), SPI (thermocouple), Timer input capture (RPM), FreeRTOS tasks, Modbus RTU over RS-485, FatFS SD card logging. Clean folder structure. Write resume bullet points AS you build.'),
        ]),
        ('NOVEMBER 2026 — CAN PROJECT + PLACEMENT', RED, [
            ('Weeks 21–22', 'Nov 1–14', 'BUILD: CAN Distributed Monitoring System (Flagship Project B)',
             '3-node CAN system: Node A (sensors), Node B (actuators/PWM), Node C (gateway + Python dashboard). Create .dbc file. Add UDS DiagnosticSessionControl (0x10) and ReadDataByIdentifier (0x22). Full documentation.'),
            ('Week 23', 'Nov 15–21', 'Interview preparation sprint',
             '20 C/embedded questions per day — written on paper, not typed. STM32, FreeRTOS, CAN deep dives. Practice answering each question out loud in under 2 minutes. This week determines your interview performance.'),
            ('Week 24', 'Nov 22–30', 'Applications + resume finalization',
             'Update LaTeX resume with both flagship projects. Polish all GitHub READMEs with architecture diagrams, wiring photos, demo recordings. Apply to: Bosch, Continental, Tata Elxsi, KPIT, STMicro India, NXP India, Honeywell.'),
        ]),
    ]

    month_bar_colors = [RED, AMBER, BLUE, GREEN, PURPLE, RED]
    for i, (month_name, mc, weeks) in enumerate(months):
        mh = Table([[Paragraph(f'<font color="white"><b>{month_name}</b></font>', s['h3'])]], colWidths=[160*mm], rowHeights=[8*mm])
        mh.setStyle(TableStyle([('BACKGROUND',(0,0),(0,0),month_bar_colors[i]),('LEFTPADDING',(0,0),(0,0),6),('TOPPADDING',(0,0),(0,0),2),('BOTTOMPADDING',(0,0),(0,0),2)]))
        story.append(mh)

        for wk_num, wk_date, wk_topic, wk_detail in weeks:
            wt = Table([[
                Paragraph(f'<b>{wk_num}</b><br/><font size="7" color="#888780">{wk_date}</font>', s['small']),
                [Paragraph(f'<b>{wk_topic}</b>', s['week_title']), Paragraph(wk_detail, s['week_body'])]
            ]], colWidths=[22*mm, 138*mm])
            wt.setStyle(TableStyle([
                ('BACKGROUND',(0,0),(0,0), GRAY_BG),
                ('BACKGROUND',(1,0),(1,0), WHITE),
                ('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#DDDDDD')),
                ('VALIGN',(0,0),(-1,-1),'TOP'),
                ('LEFTPADDING',(0,0),(-1,-1),5), ('TOPPADDING',(0,0),(-1,-1),4),
                ('BOTTOMPADDING',(0,0),(-1,-1),4),
                ('ALIGN',(0,0),(0,-1),'CENTER'),
            ]))
            story.append(wt)
        story.append(sp(4))

    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════════
    # CHAPTER 8 — FREE RESOURCES
    # ════════════════════════════════════════════════════════════════════════
    story.append(section_header('CHAPTER 8 — FREE LEARNING RESOURCES'))
    story.append(sp(3))

    resources = [
        ('YouTube Channels', BLUE, [
            ('Jacob Sorber', 'youtube.com/@jacobsorber', 'C for embedded: best explanations of volatile, pointers, memory. Start with his "volatile" video. Search: Jacob Sorber embedded C.'),
            ('Digi-Key Electronics', 'youtube.com/@digikey', 'Shawn Hymel FreeRTOS series on STM32 — 10 videos, covers everything. THE best free RTOS resource. Search: Digi-Key FreeRTOS STM32.'),
            ('Controllerstech', 'youtube.com/@controllerstech', 'Every STM32 peripheral has a dedicated tutorial video. GPIO, UART, SPI, I2C, ADC, DMA, FreeRTOS. Very clear and practical.'),
            ('CSS Electronics', 'youtube.com/@csselectronics', 'Best CAN Bus theory videos on YouTube. Their "CAN Bus Explained" video is the industry standard introduction.'),
            ('Embitel Technologies', 'youtube.com/@embitel', 'AUTOSAR, UDS, automotive ECU architecture. Good for Bosch/Continental/KPIT interview preparation.'),
            ('Low Level Learning', 'youtube.com/@lowlevellearning', 'C internals, memory, assembly, Linux systems. Great for deep understanding of how things work at hardware level.'),
        ]),
        ('Websites & Documentation', GREEN, [
            ('ST.com — STM32F446 Reference Manual', 'st.com (RM0390)', 'The official Bible for STM32F446. Free PDF. Open it every day during July-October. Every register is explained.'),
            ('FreeRTOS.org — Free Book', 'freertos.org/Documentation', '"Mastering the FreeRTOS Real Time Kernel" — free PDF on their website. 600+ pages. Read alongside your September project work.'),
            ('CSS Electronics — CAN Tutorial', 'csselectronics.com', 'Best written CAN bus tutorial on the internet. Completely free. Covers theory → practical → tools in one comprehensive page.'),
            ('Controllerstech.com', 'controllerstech.com', 'Written tutorials for every STM32 peripheral with CubeMX steps + complete code. Best complement to the YouTube channel.'),
            ('cppreference.com', 'cppreference.com', 'Definitive C/C++ reference. Bookmark and use daily when coding. Every standard library function documented.'),
            ('Beej\'s Guide to C', 'beej.us/guide/bgc/', 'Free online book — covers everything including pointers in plain English. Better than most paid textbooks.'),
            ('EmbeddedRelated.com', 'embeddedrelated.com', 'Deep technical articles on embedded topics by industry veterans. Read the "Introduction to Real-Time Programming" series.'),
        ]),
        ('Free Courses', AMBER, [
            ('CS50x — Harvard (edX)', 'cs50.harvard.edu', 'Best free C fundamentals course. Weeks 1-4 cover all of C you need. Completely free to audit. Very well taught.'),
            ('The Linux Command Line (book)', 'linuxcommand.org', 'Free PDF by William Shotts. Best Linux book for beginners. Covers all commands you need for embedded development.'),
            ('OverTheWire: Bandit', 'overthewire.org/wargames/bandit/', 'Learn Linux commands by playing a game. Fun and effective. Covers all essential command-line skills.'),
            ('ARM Cortex-M Architecture', 'developer.arm.com', 'Free official ARM documentation and Cortex-M technical reference manuals. Primary source for architecture details.'),
        ]),
        ('Paid (worth every rupee)', RED, [
            ('FastBit Embedded — STM32 bare-metal (Udemy)', 'Udemy — Kiran Nayak', 'Wait for sale (~₹399). His bare-metal GPIO and UART sections are exactly what you need for July. Best investment for embedded learning on Udemy.'),
            ('Embedded Systems Programming on ARM (Udemy)', 'Udemy — Kiran Nayak', 'Same instructor, deeper dive into Cortex-M internals, linker scripts, startup code. Buy on sale after completing the first course.'),
        ]),
    ]

    for category, bar_c, items in resources:
        cat_h = Table([[Paragraph(f'<font color="white"><b>{category}</b></font>', s['h3'])]], colWidths=[160*mm], rowHeights=[7*mm])
        cat_h.setStyle(TableStyle([('BACKGROUND',(0,0),(0,0),bar_c),('LEFTPADDING',(0,0),(0,0),6),('TOPPADDING',(0,0),(0,0),2),('BOTTOMPADDING',(0,0),(0,0),2)]))
        story.append(cat_h)
        for name, url, desc in items:
            rr = Table([[
                Paragraph(f'<b>{name}</b><br/><font size="7" color="#185FA5">{url}</font>', s['small']),
                Paragraph(desc, s['small'])
            ]], colWidths=[50*mm, 110*mm])
            rr.setStyle(TableStyle([
                ('BACKGROUND',(0,0),(0,0),GRAY_BG),
                ('BACKGROUND',(1,0),(1,0),WHITE),
                ('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#DDDDDD')),
                ('VALIGN',(0,0),(-1,-1),'TOP'),
                ('LEFTPADDING',(0,0),(-1,-1),5), ('TOPPADDING',(0,0),(-1,-1),3),
                ('BOTTOMPADDING',(0,0),(-1,-1),3),
            ]))
            story.append(rr)
        story.append(sp(4))

    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════════
    # CHAPTER 9 — PROJECTS
    # ════════════════════════════════════════════════════════════════════════
    story.append(section_header('CHAPTER 9 — FLAGSHIP PROJECTS: ARCHITECTURE & RESUME BULLETS'))
    story.append(sp(3))

    story.append(Paragraph('Project A — Motor Test Bench Data Acquisition System', s['h2']))
    story.append(info_box('This project directly leverages your MSIL internship. You have seen real motor test bench hardware — now you build the firmware for it. This is a story every automotive interviewer will ask about.', 'tip'))
    story.append(sp(2))

    proj_a_hardware = [
        ('MCU', 'STM32F446RE Nucleo'),
        ('Current sensing', 'ACS712 current sensor → STM32 ADC (12-bit, DMA, 1kHz)'),
        ('Temperature', 'MAX31855 thermocouple amplifier → STM32 SPI'),
        ('Speed/RPM', 'Encoder or tachometer → STM32 Timer input capture'),
        ('Industrial comm', 'RS-485 transceiver (MAX485) + Modbus RTU slave'),
        ('Data logging', 'SD card module (SPI) + FatFS library'),
        ('RTOS', 'FreeRTOS — 3 priority levels, queues between tasks'),
    ]
    story.append(Paragraph('Hardware & software components', s['h3']))
    hw_t = Table([[Paragraph(k,s['small']), Paragraph(v,s['small'])] for k,v in proj_a_hardware], colWidths=[35*mm, 125*mm])
    hw_t.setStyle(TableStyle([
        ('ROWBACKGROUNDS',(0,0),(-1,-1),[GRAY_BG,WHITE]),
        ('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#DDDDDD')),
        ('LEFTPADDING',(0,0),(-1,-1),6), ('TOPPADDING',(0,0),(-1,-1),3),
        ('BOTTOMPADDING',(0,0),(-1,-1),3), ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))
    story.append(hw_t)
    story.append(sp(2))

    story.append(Paragraph('Firmware module structure', s['h3']))
    folder_str = '''motor-das/
├── Core/
│   ├── Inc/
│   │   ├── adc_sampler.h     ← DMA ADC interface
│   │   ├── spi_sensors.h     ← MAX31855 driver
│   │   ├── encoder.h         ← RPM calculation
│   │   ├── modbus_rtu.h      ← Modbus slave
│   │   ├── fatfs_logger.h    ← SD card logging
│   │   └── freertos_tasks.h  ← task declarations
│   └── Src/  (matching .c files for each module)
├── Middlewares/
│   ├── FreeRTOS/
│   └── FatFS/
├── Docs/
│   ├── architecture.png
│   └── wiring_diagram.png
├── scripts/
│   └── flash.sh
└── README.md  ← screenshots, waveforms, architecture diagram'''
    story.append(Paragraph(folder_str.replace('\n','<br/>').replace(' ','&nbsp;'), s['code']))
    story.append(sp(2))

    story.append(Paragraph('Resume bullet points — copy these exactly', s['h3']))
    bullets_a = [
        'Designed multi-sensor DAS firmware on STM32F446RE sampling current (ACS712), temperature (MAX31855 via SPI), and RPM (encoder via timer input capture) at 1 kHz using DMA-driven ADC, reducing CPU load by ~60% vs. polling approach',
        'Implemented FreeRTOS task architecture with three priority levels: sensor acquisition (high), SD card logging via FatFS (medium), and Modbus RTU communication over RS-485 (low), achieving deterministic 1 ms sampling jitter',
        'Developed Modbus RTU slave driver with CRC-16 validation exposing 12 holding registers for real-time motor telemetry, enabling integration with SCADA systems consistent with industrial test environments at Maruti Suzuki',
    ]
    for b in bullets_a:
        story.append(bullet(b, s))
    story.append(sp(4))

    story.append(Paragraph('Project B — CAN-Based Distributed Monitoring System', s['h2']))
    proj_b = [
        ('Node A', 'Sensor node — temperature + humidity + encoder RPM, transmits on CAN at 500kbps'),
        ('Node B', 'Actuator node — receives CAN commands, controls DC motor PWM and relay'),
        ('Node C', 'Gateway node — bridges CAN bus to UART → Python dashboard on PC'),
        ('DBC file', 'CAN database defining 8 messages and 24 signals for system documentation'),
        ('UDS', 'DiagnosticSessionControl (0x10) and ReadDataByIdentifier (0x22) on gateway'),
        ('Python', 'PC-side decoder for CAN log files, live signal plotting'),
    ]
    pb_t = Table([[Paragraph(k,s['small']), Paragraph(v,s['small'])] for k,v in proj_b], colWidths=[22*mm, 138*mm])
    pb_t.setStyle(TableStyle([
        ('ROWBACKGROUNDS',(0,0),(-1,-1),[LIGHT_PURPLE,WHITE]),
        ('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#DDDDDD')),
        ('LEFTPADDING',(0,0),(-1,-1),6), ('TOPPADDING',(0,0),(-1,-1),3),
        ('BOTTOMPADDING',(0,0),(-1,-1),3), ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))
    story.append(pb_t)
    story.append(sp(2))

    story.append(Paragraph('Resume bullet points — copy these exactly', s['h3']))
    bullets_b = [
        'Architected 3-node CAN network at 500 kbps with custom bit-timing configuration, hardware message filtering, and bus-off recovery on STM32F446RE; validated frame timing using logic analyzer against ISO 11898 specification',
        'Created CAN DBC file defining 8 messages and 24 signals following automotive industry practice; implemented UDS DiagnosticSessionControl (0x10) and ReadDataByIdentifier (0x22) on gateway ECU per ISO 14229',
        'Built Python-based CAN log decoder for PC-side real-time signal visualization and automated regression testing of firmware behavior across software builds',
    ]
    for b in bullets_b:
        story.append(bullet(b, s))

    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════════
    # CHAPTER 10 — PLACEMENT PREP + INTERVIEW Q&A
    # ════════════════════════════════════════════════════════════════════════
    story.append(section_header('CHAPTER 10 — PLACEMENT PREPARATION & INTERVIEW QUESTIONS'))
    story.append(sp(3))

    story.append(Paragraph('Top C interview questions — write these answers on paper, not typed', s['h2']))
    c_qna = [
        ('What is the difference between volatile and const volatile?',
         'volatile tells the compiler not to cache the value — re-read from memory every access. Used for hardware registers and ISR-shared variables. const volatile means software cannot modify it but hardware/ISR still can. Example: a read-only status register that changes by hardware.'),
        ('What does the static keyword mean? Give all three uses.',
         '1) Static local variable: value persists across function calls (like a global, but scoped to function). 2) Static file-scope variable/function: limits visibility to that .c translation unit — like "private" in C++. 3) Static class member in C++: shared across all instances.'),
        ('What is the difference between stack and heap? Which do you prefer in embedded and why?',
         'Stack: automatic, LIFO, fast, fixed size, managed by compiler. Heap: dynamic, flexible, slower, fragmentation risk. In embedded, always prefer stack and static allocation. Heap fragmentation in long-running embedded systems causes unpredictable failures. MISRA-C forbids heap allocation.'),
        ('Why must hardware registers be declared volatile?',
         'Without volatile, the compiler may see that your code never modifies the variable and cache its value in a CPU register. For hardware registers, the hardware changes the value externally. If the compiler cached the old value, your read would return stale data. volatile forces a fresh memory read every time.'),
        ('Implement a function that checks if a number is a power of 2.',
         'bool isPow2(uint32_t n) { return (n > 0) && ((n & (n-1)) == 0); } Explanation: a power of 2 in binary has exactly one bit set. Subtracting 1 flips all bits below that bit. AND-ing gives 0 only if exactly one bit was set.'),
        ('What is endianness? How would you detect it at runtime?',
         'Big endian: most significant byte at lowest address. Little endian: least significant byte at lowest address. ARM Cortex-M is little endian by default. Detection: uint32_t val = 1; if (*(uint8_t*)&val == 1) then little endian. Important when sending multi-byte values over serial protocols.'),
        ('What is the difference between #define and const in embedded C?',
         '#define is preprocessor text substitution — no type, no scope, no debug symbol. const has type safety, scoping rules, and appears in debug symbols. In embedded, const variables can be placed in flash (.rodata section). Always prefer const for values; use #define only for register addresses and bit masks.'),
    ]
    for q, a in c_qna:
        qt = Table([[Paragraph(f'Q: {q}',s['small']), Paragraph(f'A: {a}',s['small'])]], colWidths=[68*mm, 92*mm])
        qt.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(0,0),LIGHT_BLUE),
            ('BACKGROUND',(1,0),(1,0),WHITE),
            ('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#DDDDDD')),
            ('LEFTPADDING',(0,0),(-1,-1),6), ('TOPPADDING',(0,0),(-1,-1),4),
            ('BOTTOMPADDING',(0,0),(-1,-1),4), ('VALIGN',(0,0),(-1,-1),'TOP'),
        ]))
        story.append(qt)
        story.append(sp(1))

    story.append(sp(3))
    story.append(Paragraph('FreeRTOS interview questions', s['h2']))
    rtos_qna = [
        ('What is priority inversion? How does FreeRTOS handle it?',
         'Low-priority task holds a mutex. High-priority task blocks waiting for it. Medium-priority task preempts low-priority task indefinitely — high-priority task starves. FreeRTOS mutexes implement priority inheritance: the low-priority task temporarily inherits the high-priority task\'s priority while holding the mutex.'),
        ('What is the difference between a binary semaphore and a mutex?',
         'Binary semaphore: purely a signalling mechanism — can be given from one task and taken by another. Used for ISR-to-task notification. Mutex: ownership concept — only the task that took it can give it. Has priority inheritance. Never take a mutex in an ISR. Use semaphores for ISR-to-task, mutexes for shared resource protection.'),
        ('What happens if a task stack overflows in FreeRTOS?',
         'Undefined behavior — corrupts adjacent memory. FreeRTOS provides stack overflow detection: configCHECK_FOR_STACK_OVERFLOW=1 (watermark check at task switch) or =2 (paints last N bytes with known pattern and checks them). Implement vApplicationStackOverflowHook() to catch it — log which task name overflowed and halt or reset.'),
        ('Why should you never call HAL_Delay() inside an RTOS task?',
         'HAL_Delay() uses SysTick in a busy-wait loop. Inside FreeRTOS, SysTick is used by the RTOS tick. Calling HAL_Delay() can corrupt RTOS timing. Always use vTaskDelay(pdMS_TO_TICKS(ms)) which yields CPU to other tasks during the delay.'),
    ]
    for q, a in rtos_qna:
        qt = Table([[Paragraph(f'Q: {q}',s['small']), Paragraph(f'A: {a}',s['small'])]], colWidths=[68*mm, 92*mm])
        qt.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(0,0),LIGHT_GREEN),
            ('BACKGROUND',(1,0),(1,0),WHITE),
            ('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#DDDDDD')),
            ('LEFTPADDING',(0,0),(-1,-1),6), ('TOPPADDING',(0,0),(-1,-1),4),
            ('BOTTOMPADDING',(0,0),(-1,-1),4), ('VALIGN',(0,0),(-1,-1),'TOP'),
        ]))
        story.append(qt)
        story.append(sp(1))

    story.append(sp(3))
    story.append(Paragraph('CAN Bus interview questions', s['h2']))
    can_qna = [
        ('Explain CAN bus arbitration.',
         'All nodes begin transmitting simultaneously. The bus is wired-AND: if any node drives dominant (0), the bus reads 0 regardless of what others transmit. Nodes compare what they transmit with what they read. If a node transmits recessive (1) but reads dominant (0), it has lost arbitration and stops transmitting immediately. Lower CAN ID = more leading zero bits = wins arbitration = higher bus priority.'),
        ('What is bit stuffing in CAN?',
         'CAN uses NRZ encoding with no clock. To prevent long sequences of the same bit (which would lose synchronization), CAN inserts a complementary stuff bit after every 5 consecutive identical bits. The receiver removes these stuff bits. A stuff error (6 consecutive same bits) is one of the CAN error types.'),
        ('What is the maximum data payload in a CAN 2.0 frame vs CAN FD?',
         'Classic CAN 2.0: maximum 8 bytes per frame. CAN FD (Flexible Data-rate): up to 64 bytes per frame, and the data phase can run at a higher bit rate (up to 8 Mbps) than the arbitration phase. CAN FD is mandatory knowledge for 2024+ automotive roles.'),
    ]
    for q, a in can_qna:
        qt = Table([[Paragraph(f'Q: {q}',s['small']), Paragraph(f'A: {a}',s['small'])]], colWidths=[68*mm, 92*mm])
        qt.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(0,0),LIGHT_RED),
            ('BACKGROUND',(1,0),(1,0),WHITE),
            ('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#DDDDDD')),
            ('LEFTPADDING',(0,0),(-1,-1),6), ('TOPPADDING',(0,0),(-1,-1),4),
            ('BOTTOMPADDING',(0,0),(-1,-1),4), ('VALIGN',(0,0),(-1,-1),'TOP'),
        ]))
        story.append(qt)
        story.append(sp(1))

    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════════
    # CHAPTER 11 — LINUX
    # ════════════════════════════════════════════════════════════════════════
    story.append(section_header('CHAPTER 11 — LINUX FOR EMBEDDED ENGINEERS'))
    story.append(sp(3))

    story.append(Paragraph('Essential commands — use terminal for EVERYTHING from now on', s['h2']))
    linux_cmds = [
        ('File operations', 'ls -la, find . -name "*.c", cp -r, mv, rm -rf, chmod 755, chown, tree'),
        ('Text processing', 'grep -rn "keyword" ./, sed \'s/old/new/g\' file, awk \'{print $2}\', cat, less, tail -f'),
        ('Process management', 'ps aux, top, htop, kill -9 PID, & (background), jobs, nohup command &'),
        ('Serial / UART debug', 'screen /dev/ttyUSB0 115200, minicom -D /dev/ttyUSB0 -b 115200, stty'),
        ('Build tools', 'make, cmake --build build/, gcc -Wall -Wextra -o out file.c'),
        ('Cross-compiler', 'arm-none-eabi-gcc, arm-none-eabi-objdump, arm-none-eabi-size'),
        ('Git daily', 'git log --oneline --graph, git diff HEAD~1, git stash, git bisect'),
        ('Networking', 'ssh user@host, scp file user@host:/path, ifconfig, netstat -tulpn'),
    ]
    for cmd_cat, cmd_list in linux_cmds:
        lrow = Table([[Paragraph(f'<b>{cmd_cat}</b>',s['small']), Paragraph(cmd_list,s['code'])]], colWidths=[32*mm, 128*mm])
        lrow.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(0,0),LIGHT_BLUE),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#DDDDDD')),
            ('LEFTPADDING',(0,0),(-1,-1),6), ('TOPPADDING',(0,0),(-1,-1),4),
            ('BOTTOMPADDING',(0,0),(-1,-1),4),
        ]))
        story.append(lrow)

    story.append(sp(3))
    story.append(Paragraph('CMake build system for STM32 — the professional approach', s['h2']))
    cmake_code = '''# CMakeLists.txt for STM32F446RE project
cmake_minimum_required(VERSION 3.16)
project(firmware C ASM)

set(CMAKE_C_COMPILER arm-none-eabi-gcc)
set(CMAKE_ASM_COMPILER arm-none-eabi-gcc)

add_executable(firmware.elf
    Core/Src/main.c
    Core/Src/uart_driver.c
    Core/Src/can_handler.c
)
target_compile_options(firmware.elf PRIVATE
    -mcpu=cortex-m4 -mthumb -mfpu=fpv4-sp-d16 -mfloat-abi=hard
    -O2 -Wall -Wextra -DSTM32F446xx
)
target_link_options(firmware.elf PRIVATE
    -T${CMAKE_SOURCE_DIR}/STM32F446RETx_FLASH.ld --specs=nano.specs
)'''
    story.append(Paragraph(cmake_code.replace('\n','<br/>').replace(' ','&nbsp;'), s['code']))

    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════════
    # CHAPTER 12 — AUTOMOTIVE
    # ════════════════════════════════════════════════════════════════════════
    story.append(section_header('CHAPTER 12 — AUTOMOTIVE EMBEDDED SYSTEMS'))
    story.append(sp(3))

    story.append(Paragraph('UDS — Unified Diagnostic Services (ISO 14229)', s['h2']))
    uds_services = [
        [Paragraph('<b>Service ID</b>',s['small']), Paragraph('<b>Name</b>',s['small']), Paragraph('<b>What it does</b>',s['small'])],
        [Paragraph('0x10',s['small']), Paragraph('DiagnosticSessionControl',s['small']), Paragraph('Switch between Default, Programming, and Extended sessions. Required for secure software updates.',s['small'])],
        [Paragraph('0x11',s['small']), Paragraph('ECUReset',s['small']), Paragraph('Hard reset, soft reset, or power-down ECU remotely. Used in manufacturing and field service.',s['small'])],
        [Paragraph('0x27',s['small']), Paragraph('SecurityAccess',s['small']), Paragraph('Seed-key challenge/response to unlock protected functions. Prevents unauthorized ECU access.',s['small'])],
        [Paragraph('0x22',s['small']), Paragraph('ReadDataByIdentifier',s['small']), Paragraph('Read any data identified by a 2-byte DID. E.g., read engine RPM, VIN, software version.',s['small'])],
        [Paragraph('0x2E',s['small']), Paragraph('WriteDataByIdentifier',s['small']), Paragraph('Write calibration data or configuration parameters to ECU.',s['small'])],
        [Paragraph('0x19',s['small']), Paragraph('ReadDTCInformation',s['small']), Paragraph('Read Diagnostic Trouble Codes. Foundation of vehicle fault diagnosis.',s['small'])],
        [Paragraph('0x34/0x36/0x37',s['small']), Paragraph('RequestDownload / TransferData / TransferExit',s['small']), Paragraph('OTA/flashing protocol. How new firmware is downloaded to an ECU in the field.',s['small'])],
    ]
    uds_t = Table(uds_services, colWidths=[14*mm, 52*mm, 94*mm])
    uds_t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),DARK_RED), ('TEXTCOLOR',(0,0),(-1,0),WHITE),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE, LIGHT_RED]),
        ('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#CCCCCC')),
        ('LEFTPADDING',(0,0),(-1,-1),5), ('TOPPADDING',(0,0),(-1,-1),3),
        ('BOTTOMPADDING',(0,0),(-1,-1),3), ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))
    story.append(uds_t)
    story.append(sp(3))

    story.append(Paragraph('AUTOSAR architecture overview (awareness level for freshers)', s['h2']))
    autosar_layers = [
        ('Application Layer (SWC)', 'Software Components — business logic. This is where firmware engineers write application code. SWCs communicate via ports and interfaces, not directly.'),
        ('RTE — Runtime Environment', 'Auto-generated glue code. Handles communication between SWCs and between SWCs and BSW. You do not write this — tools generate it from ARXML configuration.'),
        ('BSW — Basic Software', 'Pre-built software: AUTOSAR OS, COM stack, NvM, Diagnostics, Memory, Crypto. Think of it as the embedded Linux equivalent.'),
        ('MCAL — Microcontroller Abstraction Layer', 'Hardware drivers: ADC, SPI, I2C, CAN, UART — generated from configuration. This is where embedded engineers who work at Tier-1 suppliers spend time.'),
    ]
    for layer, desc in autosar_layers:
        al = Table([[Paragraph(f'<b>{layer}</b>',s['small']), Paragraph(desc,s['small'])]], colWidths=[48*mm, 112*mm])
        al.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(0,0),LIGHT_AMBER),
            ('BACKGROUND',(1,0),(1,0),WHITE),
            ('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#DDDDDD')),
            ('LEFTPADDING',(0,0),(-1,-1),6), ('TOPPADDING',(0,0),(-1,-1),3),
            ('BOTTOMPADDING',(0,0),(-1,-1),3), ('VALIGN',(0,0),(-1,-1),'TOP'),
        ]))
        story.append(al)
    story.append(sp(2))
    story.append(info_box('You do NOT need to master AUTOSAR as a fresher. You need AWARENESS — understand the architecture, know the layer names and what each does, be able to draw it on a whiteboard. Deep AUTOSAR expertise comes on the job. Simply mentioning "AUTOSAR architecture awareness" on your resume is sufficient for most fresher roles.', 'info'))

    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════════════
    # CHAPTER 13 — RESUME GUIDE
    # ════════════════════════════════════════════════════════════════════════
    story.append(section_header('CHAPTER 13 — RESUME TRANSFORMATION GUIDE'))
    story.append(sp(3))

    story.append(info_box('HONEST ASSESSMENT: Your current resume scores 3.5/10 for embedded roles. It reads like a generalist ECE student with VLSI/PCB/IoT signals. After following this guide and building the flagship projects, your projected score is 8/10.', 'warn'))
    story.append(sp(3))

    story.append(Paragraph('What to remove immediately', s['h2']))
    removes = [
        ('Verilog', 'You said no VLSI/FPGA. This directly signals the wrong track to embedded HRs.'),
        ('Vivado and ModelSim', 'FPGA tools. Zero relevance to embedded engineering. Remove both.'),
        ('KiCad (Schematic & PCB)', 'PCB design is not your target. Remove from skills section.'),
        ('JAVA', 'Irrelevant to embedded. Wastes resume space and confuses recruiters.'),
        ('Multisim', 'Simulation tool, not an embedded skill.'),
        ('LeetCode and CodeChef in skills', 'These are platforms, not skills. Never list platforms as technical skills.'),
        ('USB Hub 4-Port PCB project', 'PCB design project. Directly contradicts embedded track. Remove completely.'),
        ('Breadboard Supply PCB project', 'Beginner PCB exercise with no firmware. Remove completely.'),
        ('ISWDP Samsung/Synopsys/IISc certification', '"Device simulation, meshing, physical model extraction" = semiconductor physics/TCAD. Signals VLSI research interest. Remove for embedded roles.'),
        ('IEEE CAS — "FPGA Prototyping Summit"', 'FPGA mention hurts embedded positioning. Rewrite as "Embedded Systems Summit" or omit the event name.'),
    ]
    for item, reason in removes:
        rrow = Table([[
            Paragraph(f'<font color="#791F1F"><b>REMOVE</b></font><br/>{item}', s['small']),
            Paragraph(reason, s['small'])
        ]], colWidths=[40*mm, 120*mm])
        rrow.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(0,0),LIGHT_RED),
            ('BACKGROUND',(1,0),(1,0),WHITE),
            ('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#DDDDDD')),
            ('LEFTPADDING',(0,0),(-1,-1),6), ('TOPPADDING',(0,0),(-1,-1),3),
            ('BOTTOMPADDING',(0,0),(-1,-1),3), ('VALIGN',(0,0),(-1,-1),'TOP'),
        ]))
        story.append(rrow)
    story.append(sp(3))

    story.append(Paragraph('What to add to your skills section', s['h2']))
    story.append(skill_table([
        ('Languages', 'C (embedded, bare-metal), C++ (RAII, embedded patterns), Python, ARM Assembly (Cortex-M)'),
        ('MCU / RTOS', 'STM32F4xx (HAL + bare-metal register access), ESP32, FreeRTOS (tasks, queues, semaphores, mutexes)'),
        ('Protocols', 'CAN Bus (ISO 11898, CAN FD awareness), UART/SPI/I2C, RS-485, Modbus RTU, UDS (ISO 14229) basics'),
        ('Debugging', 'GDB/ST-Link, Logic Analyzer (sigrok/PulseView), UART logger, SWV/ITM trace, Hard Fault analysis'),
        ('Build & Tools', 'STM32CubeIDE, STM32CubeMX, Makefile, CMake, Git/GitHub, VS Code, Ubuntu/WSL'),
        ('Automotive', 'CAN DBC files, AUTOSAR architecture overview, OBD-II / UDS service IDs'),
    ], make_styles()))
    story.append(sp(3))

    story.append(Paragraph('The single most critical fix — add MSIL internship NOW', s['h2']))
    story.append(info_box('Your MSIL internship is completely absent from your current resume. This is the most valuable thing on your profile and it is invisible. Add it today — even before building any projects.', 'crit'))
    story.append(sp(2))
    story.append(Paragraph('Rewritten MSIL internship bullets:', s['h3']))
    msil_bullets = [
        'Worked with Motor Test Bench infrastructure at MSIL R&D, gaining hands-on exposure to industrial data acquisition hardware including torque sensors, encoders, thermocouples, and current transducers used in automotive drivetrain validation',
        'Analyzed sensor signal conditioning chains and real-time sampling methodologies for motor parameter monitoring (RPM, torque, temperature, current) in production automotive test environments',
        'Studied RS-485/Modbus RTU communication architecture in SCADA-integrated test cell environments, directly informing design of personal DAS firmware project on STM32',
    ]
    for b in msil_bullets:
        story.append(bullet(b, s))

    story.append(sp(3))
    story.append(Paragraph('LinkedIn headline to update immediately', s['h2']))
    li_box = Table([[Paragraph('"Embedded Firmware Engineer | STM32 | CAN Bus | FreeRTOS | Automotive | MSIL Intern | VIT Vellore ECE"', ParagraphStyle('LI', fontSize=9, textColor=DARK_BLUE, fontName='Helvetica-Bold', alignment=TA_CENTER))]], colWidths=[160*mm], rowHeights=[12*mm])
    li_box.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(0,0),LIGHT_BLUE),
        ('ROUNDEDCORNERS',[4]),
        ('VALIGN',(0,0),(0,0),'MIDDLE'),
        ('LEFTPADDING',(0,0),(0,0),10), ('RIGHTPADDING',(0,0),(0,0),10),
    ]))
    story.append(li_box)

    story.append(sp(4))

    # Final page — motivational summary
    story.append(PageBreak())
    story.append(section_header('FINAL WORDS — WHAT SEPARATES YOU FROM EVERY OTHER APPLICANT', DARK_GREEN))
    story.append(sp(4))

    final_points = [
        ('The MSIL story', 'You have touched real Motor Test Bench hardware at an automotive OEM as a 4th-year student. Nobody else applying for embedded roles at Bosch or Tata Elxsi can say that. That story — what you saw, what you learned, and the project you built because of it — is your strongest interview asset. Practice telling it in exactly 2 minutes.'),
        ('Bare-metal before HAL', 'While every other VIT student learned to call HAL_GPIO_WritePin(), you learned what the BSRR register does and WHY. That one fact demonstrates depth of understanding that senior engineers specifically look for in freshers.'),
        ('GitHub with real projects', 'Recruiters at embedded companies check GitHub before resume. Two complete projects with clean code, architecture diagrams, wiring photos, and professional READMEs put you ahead of 95% of applicants who have nothing to show.'),
        ('CAN Bus knowledge as a fresher', 'CAN Bus is considered "experienced engineer" territory. A fresher who can explain CAN arbitration, implement CAN on STM32, and has created a DBC file is extraordinary. Combined with your MSIL automotive context, this is a compelling story.'),
        ('Consistency over intensity', 'You do not need 10 hours every day. You need to push code to GitHub every single week without exception for 6 months. That consistency — 24 consecutive weeks of learning and building — is what transforms a student into an engineer.'),
    ]
    for title, desc in final_points:
        ft = Table([[
            Paragraph(f'<b>{title}</b>', s['h3']),
            Paragraph(desc, s['body'])
        ]], colWidths=[38*mm, 122*mm])
        ft.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(0,0),LIGHT_GREEN),
            ('BACKGROUND',(1,0),(1,0),WHITE),
            ('BOX',(0,0),(-1,-1),0.5,colors.HexColor('#CCCCCC')),
            ('LEFTPADDING',(0,0),(-1,-1),8), ('TOPPADDING',(0,0),(-1,-1),6),
            ('BOTTOMPADDING',(0,0),(-1,-1),6), ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('LINEBELOW',(0,0),(-1,0),0.3,colors.HexColor('#EEEEEE')),
        ]))
        story.append(ft)
        story.append(sp(2))

    story.append(sp(4))
    closing = Table([[
        Paragraph(
            '<font color="white"><b>Follow this plan with 80% consistency and you will be in the top 5% of ECE freshers '
            'for embedded roles in India by December 2026.\nThe board is ordered. The GitHub repo is created. Week 1 starts now.</b></font>',
            ParagraphStyle('CL', fontSize=10, textColor=WHITE, fontName='Helvetica-Bold',
                           alignment=TA_CENTER, leading=16))
    ]], colWidths=[160*mm], rowHeights=[28*mm])
    closing.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(0,0),NAVY),
        ('ROUNDEDCORNERS',[6]),
        ('VALIGN',(0,0),(0,0),'MIDDLE'),
        ('LEFTPADDING',(0,0),(0,0),16),
        ('RIGHTPADDING',(0,0),(0,0),16),
    ]))
    story.append(closing)

    doc.build(story)
    print(f"PDF generated: {path}")

build_pdf('/mnt/user-data/outputs/Yash_Mehta_Embedded_Roadmap.pdf')