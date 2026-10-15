"""Genererer profil-kortene i assets/ (lyst og mørkt tema).

Kør: python3 scripts/generate.py  (kræver Pillow og macOS-fonten Helvetica Neue til tekstmåling)
"""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
from PIL import ImageFont
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI','Helvetica Neue',Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
ACC = "#95BF47"; W = 1000; X = 64; IW = W - 2*X
_f = {}
def tw(t, size, bold=False):
    k=(size,bold)
    if k not in _f: _f[k]=ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", size, index=1 if bold else 0)
    return _f[k].getlength(t)*1.06
def wrap(t, size, width):
    lines, cur = [], ""
    for w in t.split():
        n = (cur+" "+w).strip()
        if tw(n,size) > width and cur: lines.append(cur); cur = w
        else: cur = n
    return lines+[cur]
def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def pal(dark): return dict(
    bg1="#0D0A15" if dark else "#FFFFFF", bg2="#1E1533" if dark else "#EEE6F8",
    fg="#F0F6FC" if dark else "#1F2328", mut="#9AA4AE" if dark else "#59636E",
    dot="#33284D" if dark else "#D9CBEE", card="#151020" if dark else "#FFFFFF",
    bd="#342950" if dark else "#D5C6EC", chip="#1A1429" if dark else "#F6F1FC",
    term="#0C0913" if dark else "#F7F3FC", css="#3D8EF0" if dark else "#1572B6")
def frame(p, h, body, dots=False, extra_style=""):
    d = f'<rect width="{W}" height="{h}" rx="16" fill="url(#dots)" mask="url(#m)"/>' if dots else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" font-family="{FONT}">
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{p['bg1']}"/><stop offset="1" stop-color="{p['bg2']}"/></linearGradient>
<pattern id="dots" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.3" fill="{p['dot']}"/></pattern>
<linearGradient id="fd" x1="0" x2="1"><stop offset=".45" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff"/></linearGradient>
<mask id="m"><rect width="{W}" height="{h}" fill="url(#fd)"/></mask><style>{extra_style}</style></defs>
<rect x=".5" y=".5" width="{W-1}" height="{h-1}" rx="16" fill="url(#bg)" stroke="{p['bd']}"/>{d}
{body}</svg>'''
def label(p, y, t):
    return f'<rect x="{X}" y="{y-13}" width="28" height="4" rx="2" fill="{ACC}"/><text x="{X+40}" y="{y-6}" font-size="15" font-weight="700" letter-spacing="2.2" fill="{p["mut"]}">{esc(t)}</text>'
def chips(p, x, y, items, fs=17, h=38):
    out=""
    for c in items:
        w = 32 + tw(c, fs)
        ai = c.startswith("AI")
        out += f'<rect x="{x}" y="{y}" width="{w:.0f}" height="{h}" rx="{h/2}" fill="{AI if ai else p["chip"]}" fill-opacity="{.14 if ai else 1}" stroke="{AI if ai else p["bd"]}" stroke-opacity="{.6 if ai else 1}"/><text x="{x+w/2:.0f}" y="{y+h/2+fs*0.36:.1f}" text-anchor="middle" font-size="{fs}" font-weight="{600 if ai else 500}" fill="{AI if ai else p["fg"]}">{esc(c)}</text>'
        x += w + 10
    return out
BODY = 18; LH = 30

def banner(p):
    li_t = "Connect på LinkedIn"; li_w = 64 + tw(li_t, 16, True) + 26
    li_x = W - X - li_w
    li = f'''<g><rect x="{li_x:.0f}" y="222" width="{li_w:.0f}" height="40" rx="20" fill="#3F1F6E"/>
<rect x="{li_x+14:.0f}" y="231" width="22" height="22" rx="5" fill="#FFFFFF"/><text x="{li_x+25:.0f}" y="248" text-anchor="middle" font-size="14" font-weight="800" fill="#3F1F6E">in</text>
<text x="{li_x+46:.0f}" y="247.5" font-size="16" font-weight="700" fill="#FFFFFF">{li_t}  →</text></g>'''
    b = f'''<rect x="{X}" y="56" width="40" height="4" rx="2" fill="{ACC}"/>
<text x="{X}" y="118" font-size="52" font-weight="700" letter-spacing="-1" fill="{p['fg']}">Mathias Liljeberg</text>
<text x="{X}" y="160" font-size="23" fill="{p['mut']}">Projektleder · Shopify, e-commerce &amp; teknisk rådgivning</text>
<text x="{X}" y="194" font-size="19" fill="{p['mut']}"><tspan fill="{ACC}" font-weight="600">ShopHelten</tspan>  —  Shopify Premier-bureau  ·  København</text>
{chips(p,X,224,["Shopify Plus","Løsningsdesign","CRO & UX","AI-agents"],fs=16,h=36)}
<g class="ring" fill="none" stroke="{ACC}"><circle cx="840" cy="118" r="84" stroke-opacity=".2" stroke-width="1.5" stroke-dasharray="4 10"/><circle cx="840" cy="118" r="60" stroke-opacity=".38" stroke-width="1.5"/></g>
<g transform="translate(840 118)" fill="none" stroke="{ACC}" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"><path d="M-25 -12 H25 L21 31 H-21 Z" fill="{ACC}" fill-opacity=".12"/><path d="M-12 -12 V-20 A12 12 0 0 1 12 -20 V-12"/></g>
{li}'''
    st = ".ring{transform-origin:840px 118px;animation:s 40s linear infinite}@keyframes s{to{transform:rotate(360deg)}}@media (prefers-reduced-motion:reduce){.ring{animation:none}}"
    return frame(p, 300, b, dots=True, extra_style=st)

def about(p):
    txt = ("Jeg er projektleder hos ShopHelten, et Shopify Premier-bureau, hvor jeg hjælper brands med at få mere ud af deres webshop – "
           "både forretningsmæssigt og teknisk. Jeg står midt imellem kunden, udvikleren og eksterne partnere: jeg afklarer behovet, "
           "skitserer en løsning og følger den hele vejen til noget, der virker i praksis. "
           "AI-agents og agent-workflows er en fast del af værktøjskassen – til research, QA, analyse og dokumentation.")
    lines = wrap(txt, BODY, IW)
    def hl(l):
        l = esc(l)
        return l
    t = "".join(f'<text x="{X}" y="{100+i*LH}" font-size="{BODY}" fill="{p["fg"]}">{hl(l)}</text>' for i,l in enumerate(lines))
    return frame(p, 100 + (len(lines)-1)*LH + 52, label(p,64,"OM MIG") + t)

def icon_src(name):
    s = open(os.path.join(HERE, "icons", f"{name}.svg")).read()
    return re.search(r' d="([^"]+)"', s).group(1)
def tools(p):
    items = [("Shopify Plus", ("si","shopify"), "#95BF47"), ("Liquid", ("c","liquid"), "#95BF47"), ("Shopify Flow", ("c","flow"), "#95BF47"),
             ("HTML5", ("si","html5"), "#E34F26"), ("CSS3", ("si","css3"), p["css"]), ("Git", ("si","git"), "#F05032"), ("Claude Code", ("si","claude"), "#D97757")]
    custom = {
      "liquid": '<defs><clipPath id="lqc"><circle cx="12" cy="12" r="11.2"/></clipPath></defs><circle cx="12" cy="12" r="11.6" fill="#FFFFFF" stroke="#1B1F9E" stroke-width=".6"/><g clip-path="url(#lqc)"><text x="12" y="11.2" text-anchor="middle" font-size="6.6" font-weight="900" letter-spacing=".2" fill="#1B1F9E" font-family="Arial Black,Arial,sans-serif">LIQUID</text><g fill="none" stroke="#1B1F9E" stroke-width=".75">' + "".join(f'<path d="M-2 {12.6+i*1.7} q1.5 -1 3 0 t3 0 t3 0 t3 0 t3 0 t3 0 t3 0 t3 0 t3 0"/>' for i in range(7)) + '</g></g>',
      "flow": '<g fill="none" stroke="C" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="7" height="6" rx="1.5"/><rect x="15" y="3" width="7" height="6" rx="1.5"/><rect x="15" y="15" width="7" height="6" rx="1.5"/><path d="M9 6 H15 M12 6 V18 H15"/></g>'}
    n = len(items); gap = 12; tw_ = (IW - gap*(n-1))/n; th = 112
    out = label(p,64,"VÆRKTØJER")
    for i,(name,(kind,key),col) in enumerate(items):
        x = X + i*(tw_+gap); y = 88
        ic = f'<path d="{icon_src(key)}" fill="{col}"/>' if kind=="si" else custom[key].replace('"C"', f'"{col}"')
        cl = name.startswith("Claude")
        out += f'''<rect x="{x:.1f}" y="{y}" width="{tw_:.1f}" height="{th}" rx="14" fill="{p['card']}" stroke="{AI if cl else p['bd']}" stroke-opacity="{.6 if cl else 1}"/>
<g transform="translate({x+tw_/2-17:.1f} {y+22}) scale(1.4167)">{ic}</g>
<text x="{x+tw_/2:.1f}" y="{y+88}" text-anchor="middle" font-size="15" font-weight="600" fill="{p['fg']}">{esc(name)}</text>'''
    return frame(p, 88+th+48, out)

ICONS = {
 "bag": '<path d="M-15 -6 H15 L12 20 H-12 Z"/><path d="M-7 -6 V-11 A7 7 0 0 1 7 -11 V-6"/>',
 "nodes": '<circle cx="-12" cy="-10" r="5"/><circle cx="12" cy="-10" r="5"/><circle cx="0" cy="13" r="5"/><path d="M-7 -10 H7 M-9 -6 L-3 9 M9 -6 L3 9"/>',
 "chart": '<path d="M-16 16 H16"/><path d="M-14 8 L-5 -1 L2 5 L14 -10"/><path d="M6 -10 H14 V-2"/>',
 "spark": '<path d="M0 -17 C2 -5 5 -2 17 0 C5 2 2 5 0 17 C-2 5 -5 2 -17 0 C-5 -2 -2 -5 0 -17 Z"/>'}
def focus(p):
    cards = [("bag","Shopify & Shopify Plus","Shops end-to-end, temaer & Liquid, Markets, produktdata og migreringer"),
             ("nodes","Løsningsdesign","Shopify Flow & automatisering, betalinger, fragt, fulfillment, apps og integrationer"),
             ("chart","CRO & UX","Kunderejse, konverteringsoptimering, A/B-tests og datadrevne forbedringer"),
             ("spark","AI, agents & workflows","AI-agents og agent-workflows til research, QA, analyse og dokumentation")]
    out = label(p,64,"FOKUSOMRÅDER"); cw = (IW-16)/2; ch = 172
    for i,(ic,title,desc) in enumerate(cards):
        x = X + (i%2)*(cw+16); y = 88 + (i//2)*(ch+16)
        d = "".join(f'<text x="{x+28:.1f}" y="{y+116+j*28}" font-size="17" fill="{p["mut"]}">{esc(s)}</text>' for j,s in enumerate(wrap(desc,17,cw-56)))
        out += f'''<rect x="{x:.1f}" y="{y}" width="{cw:.1f}" height="{ch}" rx="14" fill="{p['card']}" stroke="{AI if ic=='spark' else p['bd']}" stroke-opacity="{.55 if ic=='spark' else 1}"/>
<rect x="{x+28:.1f}" y="{y+24}" width="48" height="48" rx="12" fill="{AI if ic=='spark' else ACC}" fill-opacity=".14"/>
<g transform="translate({x+52:.1f} {y+48}) scale(.95)" fill="none" stroke="{AI if ic=='spark' else ACC}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">{ICONS[ic]}</g>
<text x="{x+92:.1f}" y="{y+56}" font-size="21" font-weight="650" fill="{p['fg']}">{esc(title)}</text>{d}'''
    return frame(p, 88+2*ch+16+48, out)

def experience(p):
    rows = [("3f9a2c1","HEAD -> main","Projektleder @ ShopHelten","Shopify Premier-bureau · teknisk rådgivning & løsningsdesign","2021 – nu"),
            ("b71e0d4",None,"Account Manager @ Twentyfour","Digitalt bureau (tidl. HTML24) · web- og e-commerce-projekter","2020 – 2021"),
            ("9c4d8e2",None,"Butikschef @ Solid","Ledelse af butik, team og drift","2017 – 2018"),
            ("1a2b3c4",None,"Salg @ Solid","Hvor det hele startede: kunder, salg og service","2014 – 2020")]
    out = label(p,64,"ERFARING")
    ty = 88; step = 76; th = 70 + step*len(rows)
    out += f'<rect x="{X}" y="{ty}" width="{IW}" height="{th}" rx="14" fill="{p["term"]}" stroke="{p["bd"]}"/>'
    out += "".join(f'<circle cx="{X+24+i*18}" cy="{ty+22}" r="5.5" fill="{c}"/>' for i,c in enumerate(["#FF5F57","#FEBC2E","#28C840"]))
    out += f'<text x="{X+28}" y="{ty+60}" font-family="{MONO}" font-size="16" fill="{p["mut"]}"><tspan fill="{ACC}">$</tspan> git log --career --graph</text>'
    gx = X+36; y0 = ty+104
    out += f'<line x1="{gx}" y1="{y0}" x2="{gx}" y2="{y0+step*(len(rows)-1)}" stroke="{ACC}" stroke-opacity=".45" stroke-width="2"/>'
    for i,(h,ref,msg,sub,yr) in enumerate(rows):
        y = y0 + i*step
        dot = f'<circle cx="{gx}" cy="{y-5}" r="9" fill="{ACC}" fill-opacity=".2"/><circle cx="{gx}" cy="{y-5}" r="5" fill="{ACC}"/>' if i==0 else f'<circle cx="{gx}" cy="{y-5}" r="5" fill="{p["term"]}" stroke="{ACC}" stroke-width="2"/>'
        hx = gx+26
        r = ""
        mx = hx + tw("0000000",15)*0.98 + 14
        if ref:
            rw = tw(ref,13,True)+20
            r = f'<rect x="{mx:.0f}" y="{y-20}" width="{rw:.0f}" height="24" rx="12" fill="{ACC}" fill-opacity=".16" stroke="{ACC}" stroke-opacity=".5"/><text x="{mx+rw/2:.0f}" y="{y-3.5}" text-anchor="middle" font-family="{MONO}" font-size="13" font-weight="700" fill="{ACC}">{esc(ref)}</text>'
            mx += rw + 12
        out += f'''{dot}<text x="{hx}" y="{y}" font-family="{MONO}" font-size="15" fill="#D29922">{h}</text>{r}
<text x="{mx:.0f}" y="{y}" font-size="19" font-weight="650" fill="{p['fg']}">{esc(msg)}</text>
<text x="{W-X-24}" y="{y}" text-anchor="end" font-family="{MONO}" font-size="14" fill="{p['mut']}">{esc(yr)}</text>
<text x="{hx + tw('0000000',15)*0.98 + 14:.0f}" y="{y+26}" font-size="16" fill="{p['mut']}">{esc(sub)}</text>'''
    return frame(p, ty+th+48, out)

def commits(p):
    cols, rows, cs, g = 52, 7, 13, 3
    gw = cols*(cs+g)-g; gx = (W-gw)/2; gy = 104
    empty = p["chip"]; lvl = ["#2E1F4D","#5B3A9E","#9479CC"] if p["bg1"]=="#0B0F14" else ["#DCD0F0","#8A6BC4","#4A1F73"]
    lit = {(51,3):2,(50,1):1,(49,5):0,(51,5):1}
    cells = ""
    for c in range(cols):
        for r in range(rows):
            f = lvl[lit[(c,r)]] if (c,r) in lit else empty
            cells += f'<rect x="{gx+c*(cs+g):.0f}" y="{gy+r*(cs+g)}" width="{cs}" height="{cs}" rx="3" fill="{f}" stroke="{p['bd']}" stroke-width=".6"/>'
    gb = gy + rows*(cs+g)
    weed = "".join(f'<path d="{d}"/>' for d in [
        "M-16 0 C-14 -12 6 -18 14 -6", "M-12 10 C-4 -14 12 -12 16 4", "M-6 -15 C10 -10 12 10 -2 15",
        "M-15 6 C-6 18 10 14 15 -2", "M4 -15 C-12 -8 -14 8 2 14", "M-10 -10 C0 -2 6 6 10 12", "M-14 -4 C-2 4 8 -6 12 -12"])
    ground = f'<line x1="{X}" y1="{gb+58}" x2="{W-X}" y2="{gb+58}" stroke="{p['bd']}" stroke-width="2" stroke-dasharray="2 8" stroke-linecap="round"/>'
    tw_ = ground + f'<g transform="translate(0 {gb+30})"><g class="roll"><g class="hop"><g transform="scale(1.6)"><g class="spin" fill="none" stroke="#B08A55" stroke-width="1.8" stroke-linecap="round">{weed}<circle r="16" stroke-opacity=".55"/></g></g></g></g></g>'
    dust = f'<g transform="translate(0 {gb+54})"><g class="roll"><g class="dust" fill="#B08A55" fill-opacity=".35"><circle cx="-22" cy="0" r="3"/><circle cx="-32" cy="-2" r="2"/><circle cx="-40" cy="1" r="1.5"/></g></g></g>'
    stats = [("Commits det seneste år","4"),("Møder om andres commits","~1.200"),("Shops sendt i luften","Masser"),("Kopper kaffe","∞")]
    sx = X; sy = gb + 92; sw = (IW - 3*12)/4; st = ""
    for i,(k,v) in enumerate(stats):
        x = sx + i*(sw+12)
        st += f'<rect x="{x:.1f}" y="{sy}" width="{sw:.1f}" height="76" rx="12" fill="{p['card']}" stroke="{p['bd']}"/><text x="{x+sw/2:.1f}" y="{sy+36}" text-anchor="middle" font-size="24" font-weight="700" fill="{ACC if i else p['fg']}">{esc(v)}</text><text x="{x+sw/2:.1f}" y="{sy+60}" text-anchor="middle" font-size="14" fill="{p['mut']}">{esc(k)}</text>'
    out = label(p,64,"COMMIT-HISTORIK") + f'<text x="{W-X}" y="58" text-anchor="end" font-size="15" font-style="italic" fill="{p["mut"]}">Her er der stille. Meget stille.</text>'
    out += cells + dust + tw_ + st
    out += f'<text x="{X}" y="{sy+76+44}" font-size="17" fill="{p["fg"]}">Jeg skriver ikke selv koden – jeg sørger for, at den bliver skrevet. <tspan fill="{p["mut"]}">Til gengæld har jeg nu en flot profil.</tspan></text>'
    css = f""".roll{{animation:roll 11s linear infinite}}.hop{{animation:hop .9s ease-in-out infinite}}.spin{{transform-box:fill-box;transform-origin:center;animation:spin 1.1s linear infinite}}
.dust{{animation:dust .9s ease-out infinite}}
@keyframes roll{{0%{{transform:translateX(-60px)}}100%{{transform:translateX({W+60}px)}}}}
@keyframes hop{{0%,100%{{transform:translateY(-4px)}}50%{{transform:translateY(-22px)}}}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
@keyframes dust{{0%{{opacity:.9;transform:scale(.6)}}100%{{opacity:0;transform:scale(1.4) translateX(-10px)}}}}
@media (prefers-reduced-motion:reduce){{.roll,.hop,.spin,.dust{{animation:none}}.roll{{transform:translateX(780px)}}}}"""
    return frame(p, sy+76+80, out, extra_style=css)

def quote(p):
    steps = [("01","Forstå","Afklar behovet sammen med kunden – forretningen først, teknikken bagefter."),
             ("02","Oversæt","Skitsér en konkret løsning, som udviklere og partnere kan bygge på."),
             ("03","Implementér","Følg løsningen hele vejen til noget, der virker i praksis.")]
    out = label(p,64,"MIN TILGANG")
    ag = 36; cw = (IW - 2*ag)/3; ch = 190; y = 88
    for i,(n,t,d) in enumerate(steps):
        x = X + i*(cw+ag)
        lines = wrap(d, 16, cw-48)
        dd = "".join(f'<text x="{x+24:.1f}" y="{y+112+j*24}" font-size="16" fill="{p["mut"]}">{esc(l)}</text>' for j,l in enumerate(lines))
        out += f'''<rect x="{x:.1f}" y="{y}" width="{cw:.1f}" height="{ch}" rx="14" fill="{p['card']}" stroke="{p['bd']}"/>
<text x="{x+24:.1f}" y="{y+46}" font-family="{MONO}" font-size="15" font-weight="700" fill="{ACC}">{n}</text>
<text x="{x+24:.1f}" y="{y+80}" font-size="22" font-weight="700" fill="{p['fg']}">{t}</text>{dd}'''
        if i < 2:
            ax = x + cw + ag/2
            out += f'<path d="M{ax-6:.1f} {y+ch/2-9} l8 9 l-8 9" fill="none" stroke="{ACC}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>'
    cy = y + ch + 36
    out += f'<line x1="{X}" y1="{cy}" x2="{W-X}" y2="{cy}" stroke="{p["bd"]}"/>'
    out += f'<text x="{X}" y="{cy+44}" font-size="18" fill="{p["fg"]}">Har du en Shopify-shop, der skal løftes?</text>'
    out += f'<text x="{W-X}" y="{cy+44}" text-anchor="end" font-size="17" font-weight="700" fill="{ACC}">Skriv til mig på LinkedIn  →</text>'
    return frame(p, cy+80, out, dots=True)

os.chdir(ROOT)
os.makedirs("assets", exist_ok=True)
for f in os.listdir("assets"): os.remove("assets/"+f)
for mode in ("dark","light"):
    p = pal(mode=="dark"); ACC = "#9479CC" if mode=="dark" else "#4A1F73"; AI = ACC
    for name,fn in [("banner",banner),("about",about),("tools",tools),("focus",focus),("experience",experience),("activity",commits),("approach",quote)]:
        open(f"assets/{name}-{mode}-c.svg","w").write(fn(p))
