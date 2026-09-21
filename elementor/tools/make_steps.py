#!/usr/bin/env python3
"""Writes elementor/steps.html — the printable Elementor build guide for the
Lumiere Dental Kota Warisan landing page. Print to PDF with headless Chrome."""
import html, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'steps.html')
IMG = 'guide-img/'
e = html.escape

# ---------------------------------------------------------------- helpers
def dev(d, t=None, m=None, unit=''):
    if t is None and m is None:
        return f'{d}{unit}'
    parts = [f'<b>Desktop</b> {d}{unit}']
    if t is not None: parts.append(f'<b>Tablet</b> {t}{unit}')
    if m is not None: parts.append(f'<b>Mobile</b> {m}{unit}')
    return ' &nbsp;·&nbsp; '.join(parts)

def pad(t, r, b, l):
    return f'Top {t} &nbsp; Right {r} &nbsp; Bottom {b} &nbsp; Left {l}'

def table(rows):
    out = ['<table class="set"><thead><tr><th>Tab</th><th>Setting</th><th>Value</th></tr></thead><tbody>']
    for tab, setting, value in rows:
        out.append(f'<tr><td class="tab">{tab}</td><td>{setting}</td><td>{value}</td></tr>')
    out.append('</tbody></table>')
    return ''.join(out)

def block(kind, name, rows, note='', after=''):
    rank = {'Layout': 0, 'Content': 0, 'Style': 1, 'Advanced': 2}
    rows = sorted(rows, key=lambda r: rank.get(r[0], 0))
    label = f'<span class="kind">{kind}</span> {name}'
    return (f'<div class="block"><h4>{label}</h4>'
            + (f'<p class="note">{note}</p>' if note else '')
            + table(rows) + after + '</div>')

def tree(s):
    return f'<pre class="tree">{e(s.strip())}</pre>'

def shot(f, cap):
    return f'<figure class="shot"><img src="{IMG}{f}"><figcaption>{cap}</figcaption></figure>'

def css(s):
    return f'<pre class="code">{e(s.strip())}</pre>'

def step(n, title, body, badge=''):
    b = f'<span class="badge {badge[0]}">{badge[1]}</span>' if badge else ''
    return (f'<section class="step newpage"><div class="stephead">'
            f'<span class="num">Step {n}</span><h2>{title}</h2>{b}</div>{body}</section>')

BUILD = ('build', 'Build with widgets')
PASTE = ('paste', 'Paste code')

pages = []

# ---------------------------------------------------------------- cover
pages.append(f"""
<section class="cover">
<p class="kicker">Lumiere Dental Clinic &middot; Kota Warisan</p>
<h1>Landing page build steps for Elementor</h1>
<p class="lead">One page, fourteen sections, top to bottom. Every value below is the exact
number from the approved design. Follow the steps in order &mdash; each one finishes a
section you can see on the page before you move on.</p>

<div class="facts">
  <div><b>Built for</b>Elementor Pro 4.1.2</div>
  <div><b>Steps</b>14</div>
  <div><b>Content width</b>1250 boxed</div>
  <div><b>Font</b>Inter (Google Fonts)</div>
  <div><b>Page background</b>#FAF9F5</div>
  <div><b>Images to upload</b>22</div>
</div>

<p class="note">This rebuilds the approved static mockup inside the clinic's WordPress. The
mockup itself is live at <code>mysense-my.github.io/lumiere-dental-kota-warisan</code> &mdash;
keep it open on a second screen while you build, it is the reference for anything this
guide does not spell out.</p>

<h3>What you are building</h3>
<table class="overview"><thead><tr><th>Step</th><th>Section</th><th>How</th></tr></thead><tbody>
<tr><td>1</td><td>Page setup and menu</td><td>Page settings</td></tr>
<tr><td>2</td><td>Header</td><td>Widgets + 6 lines CSS</td></tr>
<tr><td>3</td><td>Hero</td><td>Widgets + 1 paste</td></tr>
<tr><td>4</td><td>Our Panels</td><td>Widgets</td></tr>
<tr><td>5</td><td>Why Lumiere</td><td>Widgets</td></tr>
<tr><td>6</td><td>Dr Tan biography</td><td>Widgets + 1 line CSS</td></tr>
<tr><td>7</td><td>Stats counters</td><td>Counter widget</td></tr>
<tr><td>8</td><td>Services &times; 8</td><td>Widgets + 1 line CSS</td></tr>
<tr><td>9</td><td>Our Clinic</td><td>Widgets + 1 line CSS</td></tr>
<tr><td>10</td><td>How It Works</td><td>Widgets + CSS</td></tr>
<tr><td>11</td><td>Patient Stories</td><td>Widgets</td></tr>
<tr><td>12</td><td>FAQ</td><td>Accordion widget</td></tr>
<tr><td>13</td><td>Contact</td><td>Widgets + 1 paste</td></tr>
<tr><td>14</td><td>Footer + WhatsApp button</td><td>Widgets</td></tr>
</tbody></table>

<h3>Three rules that apply to every step</h3>
<ul class="do">
<li><b>No Site Settings globals.</b> Every widget is styled directly, with the hex values
written in these tables. Nothing depends on a global colour or font.</li>
<li><b>Name every container</b> in the Structure panel the moment you create it, using the
name in the tree diagram. Nested containers are impossible to re-target otherwise.</li>
<li><b>Build one, then duplicate.</b> Where a block repeats, build the first one completely,
then right-click &rarr; Duplicate and change only the content.</li>
</ul>
</section>
""")

# ---------------------------------------------------------------- assets page
pages.append("""
<section class="step newpage"><div class="stephead"><span class="num">Before you start</span>
<h2>Upload the images</h2></div>

<p>All 22 files are in <code>Lumiere Kota Warisan / assets</code>. Upload them to
<b>Media &rsaquo; Add New</b> in one go. They are already cropped and compressed &mdash;
do not resize them, and always pick <b>Image Resolution: Full</b> when you place one.</p>

<table class="overview"><thead><tr><th>File</th><th>Size</th><th>Used in</th></tr></thead><tbody>
<tr><td><code>logo-gold.png</code></td><td>734&times;746</td><td>Header, footer</td></tr>
<tr><td><code>favicon.png</code></td><td>128&times;128</td><td>Site icon</td></tr>
<tr><td><code>hero-lobby.jpg</code></td><td>2000&times;1500</td><td>Hero background</td></tr>
<tr><td><code>panels/pmcare.png</code> + 4 more</td><td>various</td><td>Step 4 panel logos</td></tr>
<tr><td><code>team-neon.jpg</code></td><td>1400&times;1050</td><td>Step 6 Dr Tan block</td></tr>
<tr><td><code>dr-tan.jpg</code></td><td>180&times;180</td><td>Step 6 portrait circle</td></tr>
<tr><td><code>icons/general.png</code> + 7 more</td><td>95&times;95</td><td>Step 8 service pills</td></tr>
<tr><td><code>svc-scaling.jpg</code> + 7 more</td><td>1600&times;1200</td><td>Step 8 service photos</td></tr>
<tr><td><code>lobby-reverse.jpg</code>, <code>reception.jpg</code></td><td>1400&times;1050</td><td>Step 9 landscape cards</td></tr>
<tr><td><code>kids-corner.jpg</code>, <code>neon-wall.jpg</code></td><td>1050&times;1400</td><td>Step 9 portrait cards</td></tr>
<tr><td><code>team-reception.jpg</code></td><td>1400&times;1049</td><td>Step 11 featured review</td></tr>
</tbody></table>

<p class="note"><b>Why the sizes matter.</b> Every card in this design is shaped to its
image's own ratio so nothing is cropped. The service photos are all exactly 4:3 and the
Step 9 cards are 4:3 or 3:4 on purpose. If you swap in a differently shaped photo later,
change that card's <code>aspect-ratio</code> to match it.</p>

<h3 class="sub">The palette, in one place</h3>
<table class="overview"><thead><tr><th>Use</th><th>Hex</th><th>Where</th></tr></thead><tbody>
<tr><td>Headings</td><td><code>#1F2833</code></td><td>Every H1 / H2 / H3</td></tr>
<tr><td>Body text</td><td><code>#5A6270</code></td><td>Every paragraph</td></tr>
<tr><td>Buttons</td><td><code>#33485C</code> &rarr; hover <code>#26394B</code></td><td>All primary buttons</td></tr>
<tr><td>Eyebrows, icons</td><td><code>#8F702A</code></td><td>Section labels, icon glyphs</td></tr>
<tr><td>Icon tile / pill fill</td><td><code>rgba(212,178,96,.16)</code></td><td>Behind every icon</td></tr>
<tr><td>Page background</td><td><code>#FAF9F5</code></td><td>Page, footer bottom</td></tr>
<tr><td>Cards</td><td><code>#FFFFFF</code></td><td>All white cards</td></tr>
<tr><td>Card trays</td><td><code>#E9E6DD</code></td><td>The grey frame behind card groups</td></tr>
<tr><td>Hairlines</td><td><code>#E6E2D6</code></td><td>Borders and dividers</td></tr>
<tr><td>Stars</td><td><code>#F0B428</code></td><td>Review ratings</td></tr>
<tr><td>WhatsApp green</td><td><code>#25D366</code></td><td>Floating button</td></tr>
</tbody></table>

<h3 class="sub">Type scale</h3>
<table class="overview"><thead><tr><th>Element</th><th>Desktop</th><th>Tablet</th><th>Mobile</th><th>Weight / spacing</th></tr></thead><tbody>
<tr><td>H1 (hero)</td><td>56</td><td>46</td><td>33</td><td>600 &middot; line 1.2 &middot; letter &minus;2.5px</td></tr>
<tr><td>H2 (sections)</td><td>46</td><td>38</td><td>29</td><td>600 &middot; line 1.22 &middot; letter &minus;0.9px</td></tr>
<tr><td>H3 (cards)</td><td>20</td><td>20</td><td>20</td><td>600 &middot; line 1.3</td></tr>
<tr><td>Body</td><td>16</td><td>16</td><td>16</td><td>400 &middot; line 1.4</td></tr>
<tr><td>Eyebrow</td><td>15</td><td>15</td><td>15</td><td>500 &middot; colour #8F702A</td></tr>
</tbody></table>
<p class="note">Elementor writes letter-spacing in px, not em. The values above are already
converted &mdash; type them exactly as shown.</p>
</section>
""")

# ---------------------------------------------------------------- 1 page setup
pages.append(step(1, 'Page setup and the nav menu', f"""
<p>Two prerequisites before any widget goes on the page.</p>

<h3 class="sub">1a &middot; Create the menu</h3>
<p>The header links jump to anchors on this one page, so the menu is built from Custom Links.
Go to <b>Appearance &rsaquo; Menus</b>, create a menu called <b>Lumiere Landing</b>, and add six
Custom Links. Leave every "Navigation Label" exactly as written.</p>
<table class="overview"><thead><tr><th>URL</th><th>Navigation Label</th></tr></thead><tbody>
<tr><td><code>#home</code></td><td>Home</td></tr>
<tr><td><code>#about</code></td><td>About</td></tr>
<tr><td><code>#services</code></td><td>Services</td></tr>
<tr><td><code>#reviews</code></td><td>Reviews</td></tr>
<tr><td><code>#faq</code></td><td>FAQ</td></tr>
<tr><td><code>#contact</code></td><td>Contact</td></tr>
</tbody></table>
<p class="note">Do not tick any Display Location. This menu is only ever pulled in by the
Nav Menu widget in Step 2.</p>

<h3 class="sub">1b &middot; Create the page</h3>
<p><b>Pages &rsaquo; Add New</b>, title it <b>Dental Pain? Get Expert Care in Kota Warisan</b>,
then <b>Edit with Elementor</b>.</p>
<p>Open <b>Page Settings</b> (the gear at the bottom-left of the panel):</p>
{table([
  ('Settings', 'Page Layout', '<b>Elementor Canvas</b>'),
  ('Settings', 'Hide Title', 'On'),
  ('Style', 'Background Type', 'Classic'),
  ('Style', 'Background Color', '<code>#FAF9F5</code>'),
])}
<p class="note"><b>Elementor Canvas</b> drops the theme's own header and footer. That is
deliberate &mdash; this page carries its own header (Step 2) and footer (Step 14), which is
what makes it work as an ads landing page.</p>

<h3 class="sub">1c &middot; One setting that saves you later</h3>
<p>Three sections in this build use CSS <code>position: sticky</code>. Sticky dies the moment
any parent container has its overflow set to hidden. So as a habit, whenever you create a
container in this build, check <b>Advanced &rsaquo; Layout &rsaquo; Overflow</b> is left on
<b>Default</b> unless a step explicitly tells you to set Hidden.</p>
<div class="donebox"><b>Done when:</b> an empty canvas with a warm off-white background, and
a "Lumiere Landing" menu sitting in Appearance &rsaquo; Menus.</div>
""", BUILD))

# ---------------------------------------------------------------- 2 header
pages.append(step(2, 'Header', f"""
{shot('01-header.jpg', 'The header sits over the hero photo, transparent, and turns solid white once you scroll past the hero.')}
{tree('''
Container   header            Full width · sticky
 └ Container  header-inner    Boxed 1250 · row · space-between
    ├ Container  brand        row · gap 13
    │   ├ Image     logo
    │   └ Heading   brand-name
    ├ Nav Menu   main-nav
    └ Button     nav-cta
''')}

{block('Container', 'header', [
  ('Layout', 'Content Width', 'Full Width'),
  ('Layout', 'Direction', 'Column'),
  ('Advanced', 'Padding', pad(0,0,0,0)),
  ('Advanced', 'Z-Index', '100'),
  ('Advanced', 'Motion Effects &rsaquo; Sticky', '<b>Top</b>'),
  ('Advanced', 'Sticky On', 'Desktop, Tablet, Mobile'),
], note='Elementor adds the class <code>elementor-sticky--effects</code> once it starts sticking. The CSS at the bottom of this step uses that to swap the colours.')}

{block('Container', 'header-inner', [
  ('Layout', 'Content Width', 'Boxed'),
  ('Layout', 'Width', '1250'),
  ('Layout', 'Direction', 'Row'),
  ('Layout', 'Justify Content', 'Space Between'),
  ('Layout', 'Align Items', 'Center'),
  ('Advanced', 'Padding', dev(pad(18,30,18,30), pad(18,30,18,30), pad(13,20,13,20))),
])}

{block('Image', 'logo', [
  ('Content', 'Choose Image', '<code>logo-gold.png</code>'),
  ('Content', 'Image Resolution', '<b>Full</b>'),
  ('Content', 'Link', 'Custom URL &rarr; <code>#home</code>'),
  ('Style', 'Width', dev('56', '48', '44', 'px')),
])}

{block('Heading', 'brand-name', [
  ('Content', 'Title', 'Lumiere Dental'),
  ('Content', 'HTML Tag', 'p'),
  ('Content', 'Link', 'Custom URL &rarr; <code>#home</code>'),
  ('Style', 'Text Color', '<code>#FFFFFF</code>'),
  ('Style', 'Typography', 'Inter &middot; ' + dev('21', '19', '17.5', 'px') + ' &middot; weight 600'),
])}

{block('Nav Menu', 'main-nav', [
  ('Content', 'Menu', '<b>Lumiere Landing</b>'),
  ('Content', 'Layout', 'Horizontal'),
  ('Content', 'Breakpoint', 'Tablet (&le;1024)'),
  ('Style', 'Main Menu &rsaquo; Typography', 'Inter &middot; 16.5px &middot; weight 400'),
  ('Style', 'Main Menu &rsaquo; Text Color (Normal)', '<code>#FFFFFF</code> at 86% opacity'),
  ('Style', 'Main Menu &rsaquo; Text Color (Hover)', '<code>#FFFFFF</code>'),
  ('Style', 'Main Menu &rsaquo; Pointer', '<b>None</b>'),
  ('Style', 'Main Menu &rsaquo; Horizontal Padding', '15'),
  ('Style', 'Dropdown &rsaquo; Text Color', '<code>#1F2833</code>'),
  ('Style', 'Dropdown &rsaquo; Background', '<code>#FAF9F5</code>'),
  ('Style', 'Toggle Button &rsaquo; Color (Normal)', '<code>#FFFFFF</code>'),
], note='"Pointer: None" removes Elementor&rsquo;s default underline-on-hover, which this design does not use.')}

{block('Button', 'nav-cta', [
  ('Content', 'Text', 'Book An Appointment'),
  ('Content', 'Link', 'The WhatsApp URL on the last page of this guide'),
  ('Content', 'Icon', 'Arrow Right &middot; Position <b>After</b>'),
  ('Style', 'Typography', 'Inter &middot; 15.5px &middot; weight 500'),
  ('Style', 'Text Color (Normal)', '<code>#33485C</code>'),
  ('Style', 'Background (Normal)', '<code>#FFFFFF</code>'),
  ('Style', 'Text Color (Hover)', '<code>#1F2833</code>'),
  ('Style', 'Background (Hover)', '<code>#E8D397</code>'),
  ('Style', 'Border Radius', '8'),
  ('Style', 'Padding', pad(13,24,13,24)),
], note='Button alignment lives in <b>Style &rsaquo; Button &rsaquo; Position</b> in Elementor 4.x, not on the Content tab.')}

<h3 class="sub">The scrolled state</h3>
<p>Select the <b>header</b> container &rarr; <b>Advanced &rsaquo; Custom CSS</b> and paste
this. It is the whole "turns white on scroll" behaviour.</p>
{css('''
selector.elementor-sticky--effects{
  background:rgba(250,249,245,.93);
  backdrop-filter:blur(12px);
  box-shadow:0 1px 0 #E6E2D6, 0 8px 24px -18px rgba(31,40,51,.25);
}
selector.elementor-sticky--effects .elementor-heading-title,
selector.elementor-sticky--effects .elementor-item{color:#1F2833!important}
selector.elementor-sticky--effects .elementor-button{background:#33485C!important;color:#fff!important}
''')}
<div class="donebox"><b>Done when:</b> the header is invisible against the page until you
scroll, then fades into a white bar with dark links.</div>
""", BUILD))

# ---------------------------------------------------------------- 3 hero
pages.append(step(3, 'Hero', f"""
{shot('02-hero.jpg', 'Full-height hero. The photo is the clinic lobby with a dark gradient washed across it so white type stays readable.')}
{tree('''
Container   hero              Full width · min-height 100dvh · bg photo
 └ Container  hero-inner      Boxed 1250 · column · align start
    ├ Container  hero-badges  row · gap 8
    │   ├ Heading  badge-trusted
    │   └ Heading  badge-place
    ├ Heading   hero-h1
    ├ Heading   hero-sub
    ├ Container hero-actions  row · gap 12
    │   ├ Button   btn-book
    │   └ Button   btn-services
    └ HTML      hero-proof    ← paste file
''')}

{block('Container', 'hero', [
  ('Layout', 'Content Width', 'Full Width'),
  ('Layout', 'Direction', 'Column'),
  ('Layout', 'Justify Content', 'Center'),
  ('Layout', 'Min Height', '100 <b>VH</b>'),
  ('Style', 'Background Type', 'Classic'),
  ('Style', 'Background Image', '<code>hero-lobby.jpg</code>'),
  ('Style', 'Background Position', 'Center Center'),
  ('Style', 'Background Size', 'Cover'),
  ('Style', 'Background Overlay &rsaquo; Type', 'Gradient'),
  ('Style', 'Overlay &rsaquo; Color', '<code>rgba(16,28,42,.93)</code> at <b>0%</b>'),
  ('Style', 'Overlay &rsaquo; Second Color', '<code>rgba(16,28,42,.45)</code> at <b>70%</b>'),
  ('Style', 'Overlay &rsaquo; Angle', '<b>102</b>'),
  ('Advanced', 'Padding', pad(0,0,0,0)),
  ('Advanced', 'CSS ID', '<code>home</code>'),
], note='Set <b>Min Height 100 VH</b> in the panel, then the one-liner below upgrades it to <code>dvh</code> so mobile browsers do not leave a gap where the address bar was.',
after=css('selector{min-height:100dvh}'))}

{block('Container', 'hero-inner', [
  ('Layout', 'Content Width', 'Boxed'),
  ('Layout', 'Width', '1250'),
  ('Layout', 'Direction', 'Column'),
  ('Layout', 'Align Items', 'Start'),
  ('Advanced', 'Padding', dev(pad(124,30,64,30), pad(112,30,56,30), pad(104,20,44,20))),
])}

{block('Heading', 'badge-trusted', [
  ('Content', 'Title', 'Trusted'),
  ('Content', 'HTML Tag', 'p'),
  ('Style', 'Text Color', '<code>#1F2833</code>'),
  ('Style', 'Typography', 'Inter &middot; 13.5px &middot; weight 400'),
  ('Advanced', 'Background Color', '<code>#FFFFFF</code>'),
  ('Advanced', 'Border Radius', '100'),
  ('Advanced', 'Padding', pad(6,13,6,13)),
], note='Then right-click &rarr; Duplicate for <b>badge-place</b>: title <b>KIPMall Kota Warisan · Sepang</b>, text colour <code>#FFFFFF</code> at 92%, background <code>rgba(255,255,255,.14)</code>, plus a 1px border in <code>rgba(255,255,255,.2)</code>.')}

{block('Heading', 'hero-h1', [
  ('Content', 'Title', 'Dental Pain? Get Expert<br>Care in Kota Warisan'),
  ('Content', 'HTML Tag', 'h1'),
  ('Style', 'Text Color', '<code>#FFFFFF</code>'),
  ('Style', 'Typography &rsaquo; Size', dev('56', '46', '33', 'px')),
  ('Style', 'Typography &rsaquo; Weight', '600'),
  ('Style', 'Typography &rsaquo; Line Height', '1.2'),
  ('Style', 'Typography &rsaquo; Letter Spacing', dev('&minus;2.5', '&minus;2.1', '&minus;1.5', 'px')),
  ('Advanced', 'Margin', pad(26,0,0,0)),
], note='Type the <code>&lt;br&gt;</code> straight into the Title field &mdash; the Heading widget renders it.')}

{block('Heading', 'hero-sub', [
  ('Content', 'Title', 'Experiencing dental pain? Our Kota Warisan dental clinic provides gentle care to help restore your smile.'),
  ('Content', 'HTML Tag', 'p'),
  ('Style', 'Text Color', '<code>#FFFFFF</code> at 82%'),
  ('Style', 'Typography', 'Inter &middot; 17px &middot; weight 400 &middot; line 1.4'),
  ('Advanced', 'Margin', pad(22,0,0,0)),
  ('Advanced', 'Width', 'Custom &rarr; <b>480px</b>'),
])}

{block('Button', 'btn-book', [
  ('Content', 'Text', 'Book An Appointment'),
  ('Content', 'Link', 'WhatsApp URL (last page)'),
  ('Content', 'Icon', 'Arrow Right &middot; After'),
  ('Style', 'Background (Normal)', '<code>#FFFFFF</code>'),
  ('Style', 'Text Color (Normal)', '<code>#1F2833</code>'),
  ('Style', 'Background (Hover)', '<code>#E8D397</code>'),
  ('Style', 'Border Radius', '8'),
  ('Style', 'Padding', pad(12,22,12,22)),
  ('Style', 'Typography', 'Inter &middot; 15px &middot; weight 500'),
])}

{block('Button', 'btn-services', [
  ('Content', 'Text', 'Our Services'),
  ('Content', 'Link', '<code>#services</code>'),
  ('Content', 'Icon', 'Arrow Right &middot; After'),
  ('Style', 'Background (Normal)', 'Transparent'),
  ('Style', 'Text Color (Normal)', '<code>#FFFFFF</code>'),
  ('Style', 'Border Type / Width / Color', 'Solid &middot; 1px &middot; <code>rgba(255,255,255,.55)</code>'),
  ('Style', 'Border Radius', '8'),
  ('Style', 'Padding', pad(12,22,12,22)),
])}

<h3 class="sub">The rating row</h3>
<p>Drop an <b>HTML</b> widget under the buttons and paste
<b>Step 03 - Hero proof.html</b> into it. It is the four initial circles plus the five stars
and "Rated 5.0 on Google Reviews" &mdash; six lines, and far quicker than stacking overlapping
widgets by hand.</p>

<h3 class="sub">Mobile</h3>
<p>Switch to the <b>Mobile</b> device view and set <b>hero-actions</b> &rarr;
Layout &rsaquo; Direction to <b>Column</b>, and Align Items to <b>Stretch</b>, so the two
buttons go full width and stack. This does not affect desktop.</p>
<div class="donebox"><b>Done when:</b> the hero fills exactly one screen height on your
laptop and on a phone, with no scrollbar inside it.</div>
""", PASTE))

# ---------------------------------------------------------------- 4 panels
pages.append(step(4, 'Our Panels', f"""
{shot('03-panels.jpg', 'The grey tray with one white card per insurer is the pattern repeated in Steps 5, 7, 11, 12 and 13. Build it carefully once.')}
{tree('''
Container   panels             Boxed 1250 · column · align center
 ├ Container  sec-head         column · align center · max 640
 │   ├ Heading  eyebrow
 │   ├ Heading  h2
 │   └ Heading  sub
 ├ Container  panel-tray       row · bg #E9E6DD · radius 16 · pad 10 · gap 10
 │   └ Container panel-item ×5 bg #FFF · radius 12 · centred
 │        └ Image  logo
 └ Container  panel-note       row · align center · gap 14
      ├ Icon     shield
      └ Heading  note text
''')}

{block('Container', 'panels', [
  ('Layout', 'Content Width', 'Boxed'),
  ('Layout', 'Width', '1250'),
  ('Layout', 'Direction', 'Column'),
  ('Layout', 'Align Items', 'Center'),
  ('Advanced', 'Padding', dev(pad(90,30,40,30), pad(90,30,40,30), pad(64,20,28,20))),
  ('Advanced', 'CSS ID', '<code>panels</code>'),
], note='<b>Every section container from here on uses exactly these Layout and Padding values.</b> Only the CSS ID changes. Build this one, then duplicate it as the shell for Steps 5 and 8 to 13.')}

{block('Container', 'sec-head', [
  ('Layout', 'Direction', 'Column'),
  ('Layout', 'Align Items', 'Center'),
  ('Layout', 'Width', 'Custom &rarr; <b>640px</b>'),
  ('Advanced', 'Margin', pad(0,0,38,0)),
])}

{block('Heading', 'eyebrow', [
  ('Content', 'Title', '&#9670; Our Panels'),
  ('Content', 'HTML Tag', 'p'),
  ('Style', 'Alignment', 'Center'),
  ('Style', 'Text Color', '<code>#8F702A</code>'),
  ('Style', 'Typography', 'Inter &middot; 15px &middot; weight 500'),
], note='The &#9670; is a typed character, not an icon widget. Copy it from here. Heading alignment is on the <b>Style</b> tab in Elementor 4.x.')}

{block('Heading', 'h2', [
  ('Content', 'Title', "Chances Are, You're<br>Already Covered"),
  ('Content', 'HTML Tag', 'h2'),
  ('Style', 'Alignment', 'Center'),
  ('Style', 'Text Color', '<code>#1F2833</code>'),
  ('Style', 'Typography &rsaquo; Size', dev('46', '38', '29', 'px')),
  ('Style', 'Typography &rsaquo; Weight', '600'),
  ('Style', 'Typography &rsaquo; Line Height', '1.22'),
  ('Style', 'Typography &rsaquo; Letter Spacing', dev('&minus;0.9', '&minus;0.8', '&minus;0.6', 'px')),
  ('Advanced', 'Margin', pad(14,0,0,0)),
])}

{block('Heading', 'sub', [
  ('Content', 'Title', 'We are a panel clinic for the major insurers and benefit providers below, and claims are handled at the front desk.'),
  ('Content', 'HTML Tag', 'p'),
  ('Style', 'Alignment', 'Center'),
  ('Style', 'Text Color', '<code>#5A6270</code>'),
  ('Style', 'Typography', 'Inter &middot; 16px &middot; line 1.4'),
  ('Advanced', 'Margin', pad(16,0,0,0)),
])}

{block('Container', 'panel-tray', [
  ('Layout', 'Direction', 'Row'),
  ('Layout', 'Width', '100%'),
  ('Layout', 'Gap', '10'),
  ('Style', 'Background Color', '<code>#E9E6DD</code>'),
  ('Advanced', 'Border Radius', '16'),
  ('Advanced', 'Padding', pad(10,10,10,10)),
])}

{block('Container', 'panel-item', [
  ('Layout', 'Direction', 'Column'),
  ('Layout', 'Justify Content', 'Center'),
  ('Layout', 'Align Items', 'Center'),
  ('Layout', 'Min Height', '132'),
  ('Layout', 'Width', '20%'),
  ('Style', 'Background Color', '<code>#FFFFFF</code>'),
  ('Advanced', 'Border Radius', '12'),
  ('Advanced', 'Padding', pad(26,22,26,22)),
], note='Inside it, one <b>Image</b> widget: Resolution <b>Full</b>, Style &rsaquo; Width <b>132px</b>, Style &rsaquo; Max Height <b>58px</b>, Object Fit <b>Contain</b>. Then duplicate <code>panel-item</code> four times and swap the logo in each: PMCare, Mednefits, AIA, HealthMetrics, MedKad.')}

{block('Container', 'panel-note', [
  ('Layout', 'Direction', 'Row'),
  ('Layout', 'Align Items', 'Center'),
  ('Layout', 'Gap', '14'),
  ('Layout', 'Width', 'Custom &rarr; <b>640px</b>'),
  ('Advanced', 'Margin', pad(22,0,0,0)),
], note='Icon widget: shield-check, View <b>Stacked</b>, Primary Color <code>#8F702A</code>, Background <code>rgba(212,178,96,.16)</code>, Size 22, Padding 11, Border Radius 12. Beside it a Heading (tag p, 15px): <i>Not sure if your plan is on the list?</i> then a linked <b>WhatsApp us your card</b> then <i>and we&rsquo;ll confirm before your visit.</i>')}

<h3 class="sub">Responsive</h3>
<p><b>Tablet:</b> panel-tray stays a Row, set each panel-item Width to <b>33.33%</b> and turn
on Layout &rsaquo; <b>Wrap</b>. &nbsp; <b>Mobile:</b> panel-item Width <b>50%</b>, and on the
fifth one set Advanced &rsaquo; Width to <b>100%</b> so it centres on its own row.</p>
""", BUILD))

# ---------------------------------------------------------------- 5 why lumiere
pages.append(step(5, 'Why Lumiere', f"""
{shot('04-about.jpg', 'Same tray pattern as Step 4, four cards instead of five.')}
{tree('''
Container   about              Boxed 1250 · column   (CSS ID: about)
 ├ Container  sec-head         duplicate from Step 4
 └ Container  vision-tray      row · bg #E9E6DD · radius 16 · pad 10 · gap 10
     └ Container vision-card ×4  bg #FFF · radius 12 · column
          ├ Icon     icon-tile
          ├ Heading  h3
          └ Heading  p
''')}
<p>Duplicate the whole <b>panels</b> container from Step 4, rename it <b>about</b>, set its
CSS ID to <code>about</code>, then change the head copy and rebuild the tray contents.</p>

{block('Heading', 'sec-head copy', [
  ('Content', 'eyebrow', '&#9670; Why Lumiere'),
  ('Content', 'h2', 'A Different Kind of<br>Dental Visit'),
  ('Content', 'sub', 'One resident dentist, a calm modern space, and care that puts comfort before everything else.'),
])}

{block('Container', 'vision-card', [
  ('Layout', 'Direction', 'Column'),
  ('Layout', 'Width', '25%'),
  ('Style', 'Background Color', '<code>#FFFFFF</code>'),
  ('Advanced', 'Border Radius', '12'),
  ('Advanced', 'Padding', pad(28,26,30,26)),
])}

{block('Icon', 'icon-tile', [
  ('Content', 'View', '<b>Stacked</b>'),
  ('Content', 'Shape', 'Square'),
  ('Style', 'Primary Color', '<code>#8F702A</code>'),
  ('Style', 'Background Color', '<code>rgba(212,178,96,.16)</code>'),
  ('Style', 'Size', '24'),
  ('Style', 'Padding', '12'),
  ('Style', 'Border Radius', '12'),
], note='Icon alignment sits on the <b>Style</b> tab. Set it to Left.')}

<p>The card heading is <b>Inter 19.5px / 600 / #1F2833</b> with Margin
<b>Top 30 &nbsp;Right 0 &nbsp;Bottom 0 &nbsp;Left 0</b>; the paragraph is
<b>Inter 15px / #5A6270</b> with Margin <b>Top 10 &nbsp;Right 0 &nbsp;Bottom 0 &nbsp;Left 0</b>.
Build card one, duplicate three times, then fill in:</p>

<table class="overview"><thead><tr><th>Icon</th><th>Heading</th><th>Text</th></tr></thead><tbody>
<tr><td>Tooth</td><td>Painless-first dentistry</td><td>Gentle techniques from airflow scaling to careful extractions, so treatment stays calm from start to finish.</td></tr>
<tr><td>User</td><td>Led by Dr Tan Mei-Wen</td><td>DDS from MAHSA University with Distinction, plus a postgraduate diploma in clinical orthodontics.</td></tr>
<tr><td>Heart</td><td>Family-friendly clinic</td><td>A dedicated kids corner and unhurried appointments make first visits easy for the little ones.</td></tr>
<tr><td>Shield-check</td><td>Insurance panel clinic</td><td>A panel clinic for major insurers including AIA, PMCare and Mednefits, with claims handled at the front desk.</td></tr>
</tbody></table>

<h3 class="sub">Responsive</h3>
<p><b>Tablet:</b> vision-card Width <b>50%</b> with Wrap on. &nbsp; <b>Mobile:</b> Width <b>100%</b>.</p>
""", BUILD))

# ---------------------------------------------------------------- 6 dr tan
pages.append(step(6, 'Dr Tan biography', f"""
{shot('05-drtan.jpg', 'The photo is shorter than the bio column, so it travels down with you as you read instead of leaving a gap.')}
{tree('''
Container   doc-block          row · bg #FFF · radius 16 · pad 10 · gap 10
 ├ Container  doc-photo        radius 12 · overflow hidden · STICKY
 │   └ Image     team-neon
 └ Container  doc-body         column · pad 30/34/30/26
     ├ Heading    eyebrow
     ├ Container  doc-id       row · align center · gap 15
     │    ├ Image    dr-tan   (circle)
     │    └ Container column
     │         ├ Heading  name
     │         └ Heading  role
     └ Heading    bio ×4
''')}
<p>This block sits inside the same <b>about</b> section container, directly under the tray
from Step 5.</p>

{block('Container', 'doc-block', [
  ('Layout', 'Direction', 'Row'),
  ('Layout', 'Align Items', '<b>Start</b>'),
  ('Layout', 'Gap', '10'),
  ('Layout', 'Width', '100%'),
  ('Style', 'Background Color', '<code>#FFFFFF</code>'),
  ('Style', 'Box Shadow', '0 10 30 &minus;18 &nbsp;<code>rgba(31,40,51,.25)</code>'),
  ('Advanced', 'Border Radius', '16'),
  ('Advanced', 'Padding', pad(10,10,10,10)),
  ('Advanced', 'Margin', pad(16,0,0,0)),
], note='<b>Align Items must be Start</b>, not Stretch. On Stretch the photo would be pulled to the full height of the bio and the sticky travel would have nowhere to go.')}

{block('Container', 'doc-photo', [
  ('Layout', 'Width', '45%'),
  ('Advanced', 'Border Radius', '12'),
  ('Advanced', 'Overflow', '<b>Hidden</b>'),
], note='This is the one container in the build that <i>should</i> be Hidden &mdash; it clips the photo to the rounded corner. Its parents stay on Default.',
after=css('selector{aspect-ratio:4/3; position:sticky; top:112px}'))}

<p>Inside it, an <b>Image</b> widget: <code>team-neon.jpg</code>, Resolution <b>Full</b>,
Style &rsaquo; Width <b>100%</b>, Height <b>100%</b>, Object Fit <b>Cover</b>.</p>

{block('Container', 'doc-body', [
  ('Layout', 'Direction', 'Column'),
  ('Layout', 'Width', '55%'),
  ('Advanced', 'Padding', dev(pad(30,34,30,26), pad(26,28,30,28), pad(22,20,26,20))),
])}

{block('Image', 'dr-tan portrait', [
  ('Content', 'Choose Image', '<code>dr-tan.jpg</code>'),
  ('Content', 'Image Resolution', '<b>Full</b>'),
  ('Style', 'Width', '68px'),
  ('Style', 'Height', '68px'),
  ('Style', 'Object Fit', 'Cover'),
  ('Style', 'Border Radius', '50%'),
  ('Style', 'Border Type / Width / Color', 'Solid &middot; 2px &middot; <code>#E8D397</code>'),
], note='This is the only file in the pack that is low resolution (180&times;180 &mdash; it is all the group website has). At 68px it is sharp. Do not scale it up.')}

<p>Then: name = <b>Heading h3, Inter 23px / 600 / #1F2833</b>; role =
<b>p, 14.5px / #5A6270</b>, text <i>Resident Dentist · Lumiere Dental Kota Warisan</i>.
Below the doc-id container, four Heading widgets (tag <b>p</b>, Inter 15px, line-height 1.6,
colour #5A6270, Margin Bottom 12). The fourth one &mdash; the barista / left-handed line &mdash;
takes colour <code>#8F702A</code>.</p>

<p class="note">Bio copy is in <code>CONTENT-NOTES.md</code> and on the live mockup. It is the
client's own supplied biography &mdash; do not paraphrase it.</p>

<h3 class="sub">Responsive</h3>
<p><b>Tablet and Mobile:</b> set doc-block Direction to <b>Column</b>, both children to Width
<b>100%</b>, and on <b>doc-photo</b> change the Custom CSS to
<code>selector{{aspect-ratio:16/9; position:static}}</code>. Once the block is stacked there is
no taller neighbour for the photo to travel against, so sticky must be switched off.</p>
""", BUILD))

# ---------------------------------------------------------------- 7 stats
pages.append(step(7, 'Stats counters', f"""
{shot('06-stats.jpg', 'Four counters that animate up when they scroll into view.')}
{tree('''
Container   stats-tray         row · bg #E9E6DD · radius 16 · pad 10 · gap 10
 └ Container  stat-card ×4     bg #FFF · radius 12 · column
      ├ Icon     icon-tile
      └ Counter  counter
''')}
<p>Same tray as Step 4. Each card is <b>Padding Top 26 Right 26 Bottom 22 Left 26</b>,
Width <b>25%</b>, and holds the same stacked Icon tile from Step 5 plus one Counter widget.</p>

{block('Counter', 'counter', [
  ('Content', 'Starting Number', '0'),
  ('Content', 'Ending Number', 'see table'),
  ('Content', 'Number Suffix', 'see table'),
  ('Content', 'Animation Duration', '1800'),
  ('Content', 'Title', 'see table'),
  ('Style', 'Number &rsaquo; Typography', '<b>Satoshi</b> or Inter &middot; 34px &middot; weight 500'),
  ('Style', 'Number &rsaquo; Text Color', '<code>#1F2833</code>'),
  ('Style', 'Title &rsaquo; Typography', 'Inter &middot; 14.5px &middot; weight 400'),
  ('Style', 'Title &rsaquo; Text Color', '<code>#5A6270</code>'),
  ('Style', 'Counter &rsaquo; Alignment', '<b>Left</b>'),
], note='Alignment, Title Position and Number Position are all on <b>Style &rsaquo; Counter</b> in Elementor 4.x. Satoshi is not a Google Font &mdash; if it is not installed on the site, use Inter 500 and nobody will notice.')}

<table class="overview"><thead><tr><th>Ending</th><th>Suffix</th><th>Title</th></tr></thead><tbody>
<tr><td>9</td><td><code>+</code></td><td>Years of Clinical Practice</td></tr>
<tr><td>8</td><td>&mdash;</td><td>Lumiere Branches in Malaysia</td></tr>
<tr><td>8</td><td>&mdash;</td><td>Treatments Offered</td></tr>
<tr><td>5</td><td><code>.0</code></td><td>Google Review Rating</td></tr>
</tbody></table>

<p class="note"><b>The 5.0 trick.</b> Elementor's Counter only counts whole numbers. Setting
Ending Number <b>5</b> with the suffix <b>.0</b> gives you a clean 0 &rarr; 5.0 count and reads
exactly like the mockup.</p>
<p class="note"><b>Two of these four numbers are unconfirmed.</b> "9+ years" is inferred from
Dr Tan's 2016 graduation and "5.0" from the review screenshots. Both are flagged in
<code>CONTENT-NOTES.md</code> &mdash; get the clinic to confirm before this page goes live.</p>

<h3 class="sub">Responsive</h3>
<p><b>Tablet:</b> stat-card Width <b>50%</b>, Wrap on. &nbsp; <b>Mobile:</b> <b>100%</b>.</p>
""", BUILD))

# ---------------------------------------------------------------- 8 services
pages.append(step(8, 'Services &mdash; the sticky stack', f"""
{shot('07-services.jpg', 'Eight cards that pin at the top and let the next one slide over them. This is the signature effect of the page.')}
{tree('''
Container   services           Boxed 1250 · column   (CSS ID: services)
 ├ Container  sec-head         duplicate from Step 4
 └ Container  svc-stack        column · gap 0
     └ Container svc-card ×8   bg #FFF · radius 24 · row · gap 48 · STICKY
          ├ Container  svc-media   radius 12 · overflow hidden
          │    └ Image
          └ Container  svc-body    column
               ├ Container  pill   row · gold wash · radius 100
               │    ├ Image    icon (26px)
               │    └ Heading  label
               ├ Heading    h2
               ├ Heading    p
               ├ Icon List  checklist
               └ Button     cta
''')}

<p class="note"><b>Read this before you build.</b> The stacking is plain CSS
<code>position: sticky</code> &mdash; <b>do not</b> use Motion Effects &rsaquo; Sticky, which is
a different, JavaScript-driven thing and will not stack. Sticky also breaks if any ancestor
has Overflow set to Hidden, so leave <b>services</b> and <b>svc-stack</b> on Default.</p>

{block('Container', 'svc-card', [
  ('Layout', 'Direction', 'Row'),
  ('Layout', 'Align Items', 'Center'),
  ('Layout', 'Gap', '48'),
  ('Layout', 'Width', '100%'),
  ('Style', 'Background Color', '<code>#FFFFFF</code>'),
  ('Style', 'Box Shadow', '0 10 30 &minus;18 &nbsp;<code>rgba(31,40,51,.25)</code>'),
  ('Advanced', 'Border Radius', '24'),
  ('Advanced', 'Padding', dev(pad(40,40,40,40), pad(22,22,22,22), pad(22,22,22,22))),
  ('Advanced', 'Margin', dev(pad(0,0,28,0), pad(0,0,24,0), pad(0,0,24,0))),
  ('Advanced', 'Overflow', 'Default'),
], after=css('selector{position:sticky; top:100px}'))}

{block('Container', 'svc-media', [
  ('Layout', 'Width', '50%'),
  ('Advanced', 'Border Radius', '12'),
  ('Advanced', 'Overflow', '<b>Hidden</b>'),
], note='Image widget inside: Resolution <b>Full</b>, Width 100%, Height 100%, Object Fit <b>Cover</b>.',
after=css('selector{aspect-ratio:4/3}'))}

{block('Container', 'pill', [
  ('Layout', 'Direction', 'Row'),
  ('Layout', 'Align Items', 'Center'),
  ('Layout', 'Gap', '9'),
  ('Layout', 'Width', 'Custom &rarr; fit the content'),
  ('Style', 'Background Color', '<code>rgba(212,178,96,.16)</code>'),
  ('Advanced', 'Border Radius', '100'),
  ('Advanced', 'Padding', pad(8,16,8,10)),
  ('Advanced', 'Margin', pad(0,0,18,0)),
], note='Image inside = the matching file from <code>assets/icons</code>, Width <b>26px</b>. Heading beside it = tag p, Inter 15px, colour <code>#8F702A</code>.')}

{block('Icon List', 'checklist', [
  ('Content', 'Layout', 'Default (vertical)'),
  ('Content', 'Items', 'Five, from the table overleaf'),
  ('Content', 'Icon (each item)', 'Check'),
  ('Style', 'List &rsaquo; Space Between', '12'),
  ('Style', 'Icon &rsaquo; Color', '<code>#8F702A</code>'),
  ('Style', 'Icon &rsaquo; Size', '13'),
  ('Style', 'Icon &rsaquo; Gap', '12'),
  ('Style', 'Text &rsaquo; Typography', 'Inter &middot; 15.5px'),
  ('Style', 'Text &rsaquo; Color', '<code>#1F2833</code>'),
], note='Icon List has no Text Indent control in 4.x &mdash; the spacing you want is <b>Style &rsaquo; Icon &rsaquo; Gap</b>.')}

{block('Button', 'cta', [
  ('Content', 'Text', 'Book This Treatment'),
  ('Content', 'Link', 'WhatsApp URL with that treatment named &mdash; see overleaf'),
  ('Content', 'Icon', 'Arrow Right &middot; After'),
  ('Style', 'Background (Normal)', '<code>#33485C</code>'),
  ('Style', 'Background (Hover)', '<code>#26394B</code>'),
  ('Style', 'Text Color', '<code>#FFFFFF</code>'),
  ('Style', 'Border Radius', '8'),
  ('Style', 'Padding', pad(12,22,12,22)),
  ('Advanced', 'Margin', pad(26,0,0,0)),
])}

<h3 class="sub">Then duplicate seven times</h3>
<p>Build card 1 completely, then right-click <b>svc-card</b> &rarr; Duplicate &times; 7 and
change only the content. On cards <b>2, 4, 6 and 8</b> set Layout &rsaquo; Direction to
<b>Row Reversed</b> so the photo alternates sides.</p>
<p><b>Mobile:</b> set svc-card Direction to <b>Column</b> for all eight, Gap <b>18</b>, and
both children to Width <b>100%</b>. Row Reversed on mobile would put the photo below the
text, so on the reversed cards set Direction to <b>Column</b> too (not Column Reversed).</p>
""", BUILD))

# service content table
rows = [
  ('general.png', 'svc-scaling.jpg', 'General Dentistry', 'Everyday Care That Keeps Problems Away',
   'Routine checkups, cleaning and fillings that catch small problems before they turn into painful ones.',
   'Checkups and full oral examination / Airflow scaling and polishing / Tooth-coloured fillings / Extractions and minor oral surgery / Clear explanation of your teeth condition'),
  ('whitening.png', 'svc-whitening.jpg', 'Teeth Whitening', 'A Brighter Smile, Safely Done',
   'Professional whitening that lifts years of coffee, tea and teh tarik stains without damaging your enamel.',
   'Shade assessment before we start / In-clinic professional whitening / Take-home whitening kits / Enamel-safe, dentist-supervised / Advice on keeping the result'),
  ('implants.png', 'svc-implants.jpg', 'Dental Implants', 'Replace Missing Teeth for Good',
   'An implant restores a missing tooth from the root up, so you can bite and speak normally again.',
   'X-ray assessment and planning / Single and multiple tooth implants / Natural-looking implant crowns / Step-by-step timeline explained upfront / Follow-up care after placement'),
  ('invisalign.png', 'svc-invisalign.jpg', 'Invisalign / Clear Correct', 'Straighten Your Teeth Without Braces',
   'Clear removable aligners that move your teeth quietly, so most people never notice you are in treatment.',
   'Digital assessment and treatment plan / Nearly invisible custom aligners / Removable for meals and brushing / Fewer clinic visits than fixed braces / Retainers to hold the final result'),
  ('braces.png', 'svc-braces.jpg', 'Braces', 'Classic Braces, Expertly Fitted',
   'Fixed braces remain the most reliable way to correct crowding and bite problems, planned by a dentist with postgraduate orthodontic training.',
   'Orthodontic assessment and records / Metal and ceramic bracket options / Crowding, spacing and bite correction / Regular adjustment appointments / Retainers once braces come off'),
  ('rootcanal.png', 'svc-rootcanal.jpg', 'Root Canal Treatment', 'Save the Tooth Instead of Losing It',
   "Dr Tan's focus is preserving natural teeth. Root canal treatment here is methodical, explained clearly, and painless.",
   'Assessment and honest advice first / Treatment focused on saving the tooth / Proper numbing and a patient pace / Every step explained as it happens / Crown options to protect the result'),
  ('crowns.png', 'svc-crowns.jpg', 'Crown &amp; Bridges', 'Restore Damaged Teeth to Full Strength',
   'Crowns protect what remains and bridges close the gaps, matched in shade so the repair disappears into your smile.',
   'Crowns for cracked or weakened teeth / Bridges to replace missing teeth / Shade matching to your natural teeth / Precise fitting over multiple visits / Care advice to make them last'),
  ('makeover.png', 'svc-makeover.jpg', 'Smile Makeover', 'A Complete Plan for the Smile You Want',
   'When more than one thing needs fixing, a makeover combines the right treatments into a single plan with one clear outcome.',
   'Full smile assessment and goals / Combines whitening, veneers and alignment / Treatment sequenced in the right order / Costs and timeline agreed upfront / Reviews at every stage'),
]
svc_rows = ''.join(
  f'<tr><td class="n">{i+1}</td><td><b>{p}</b><br><code>{ic}</code><br><code>{im}</code></td>'
  f'<td><b>{h}</b><p>{d}</p><span class="li">{li}</span></td></tr>'
  for i,(ic,im,p,h,d,li) in enumerate(rows))
pages.append(f"""
<section class="step newpage"><div class="stephead"><span class="num">Step 8</span>
<h2>Services &mdash; content for all eight cards</h2></div>
<p>Pill label, icon file and photo on the left; heading, description and the five checklist
items on the right (separated by <code>/</code>).</p>
<table class="svc"><thead><tr><th>#</th><th>Pill / files</th><th>Copy</th></tr></thead>
<tbody>{svc_rows}</tbody></table>
<p class="note">Each button links to WhatsApp with the treatment pre-written into the message,
so the front desk knows what the enquiry is about before they reply. Pattern:<br>
<code>https://wa.me/601116083188?text=Hi%2C%20I%27d%20like%20to%20ask%20about%20TREATMENT%20at%20Lumiere%20Kota%20Warisan.</code><br>
Replace <code>TREATMENT</code> with the pill label, using <code>%20</code> for each space.</p>
</section>
""")

# ---------------------------------------------------------------- 9 facilities
pages.append(step(9, 'Our Clinic', f"""
{shot('08-facilities.jpg', 'Two columns. Each column has one landscape card and one portrait card, so both columns end level.')}
{tree('''
Container   facilities         Boxed 1250 · column   (CSS ID: facilities)
 ├ Container  sec-head
 └ Container  fac-grid         row · gap 14
     ├ Container  fac-col-1    column · gap 14 · width 50%
     │    ├ Container  card-lobby   4:3
     │    └ Container  card-kids    3:4
     └ Container  fac-col-2    column · gap 14 · width 50%
          ├ Container  card-reception  4:3
          └ Container  card-neon       3:4
''')}

{block('Container', 'card-lobby', [
  ('Layout', 'Direction', 'Column'),
  ('Layout', 'Justify Content', '<b>End</b>'),
  ('Layout', 'Width', '100%'),
  ('Style', 'Background Image', '<code>lobby-reverse.jpg</code>'),
  ('Style', 'Background Size', 'Cover'),
  ('Style', 'Background Position', 'Center Center'),
  ('Advanced', 'Border Radius', '16'),
  ('Advanced', 'Overflow', '<b>Hidden</b>'),
  ('Advanced', 'Padding', pad(0,0,0,0)),
], after=css('selector{aspect-ratio:4/3}'))}

<p>Inside each card, one <b>caption</b> container pinned to the bottom:</p>
{block('Container', 'caption', [
  ('Layout', 'Direction', 'Column'),
  ('Layout', 'Width', '100%'),
  ('Style', 'Background Type', 'Gradient'),
  ('Style', 'Color', '<code>rgba(16,28,42,.8)</code> at <b>0%</b>'),
  ('Style', 'Second Color', '<code>rgba(16,28,42,0)</code> at <b>100%</b>'),
  ('Style', 'Gradient Angle', '<b>0</b>'),
  ('Advanced', 'Padding', pad(90,28,26,28)),
], note='Heading inside: h3, Inter 22px / 600 / <code>#FFFFFF</code>. Paragraph: tag p, 15px, <code>#FFFFFF</code> at 85%, Margin Top 7.')}

<p>Then duplicate the card three times and set:</p>
<table class="overview"><thead><tr><th>Card</th><th>Image</th><th>Ratio CSS</th><th>Heading</th></tr></thead><tbody>
<tr><td>1</td><td><code>lobby-reverse.jpg</code></td><td><code>4/3</code></td><td>A calm, open lobby</td></tr>
<tr><td>2</td><td><code>kids-corner.jpg</code></td><td><code>3/4</code></td><td>A corner just for kids</td></tr>
<tr><td>3</td><td><code>reception.jpg</code></td><td><code>4/3</code></td><td>Qualified and certified</td></tr>
<tr><td>4</td><td><code>neon-wall.jpg</code></td><td><code>3/4</code></td><td>The smile wall</td></tr>
</tbody></table>
<p class="note">Cards 1 and 3 go in column one and two respectively; cards 2 and 4 sit beneath
them. The 4:3 / 3:4 pairing is why the two columns finish at the same height &mdash; if you
swap a photo, keep the ratio or the grid goes lopsided.</p>

<h3 class="sub">Responsive</h3>
<p><b>Tablet and Mobile:</b> fac-grid Direction <b>Column</b>, both columns Width <b>100%</b>.
The four cards then run in one stream and keep their own ratios.</p>
""", BUILD))

# ---------------------------------------------------------------- 10 how
pages.append(step(10, 'How It Works', f"""
{shot('09-how.jpg', 'The left panel holds still while the four steps scroll past it.')}
{tree('''
Container   how                Boxed 1250   (CSS ID: how)
 └ Container  how-grid         row · gap 70
     ├ Container  how-left     width 50%
     │    └ Container how-sticky   STICKY
     │         ├ Heading  eyebrow
     │         ├ Heading  h2
     │         └ Heading  sub
     └ Container  how-steps    column · width 50%
          └ Container how-step ×4   row · gap 28
               ├ Icon      tile
               └ Container column
                    ├ Heading  h3
                    └ Heading  p
''')}

{block('Container', 'how-sticky', [
  ('Layout', 'Direction', 'Column'),
  ('Layout', 'Width', '100%'),
], after=css('selector{position:sticky; top:130px}'))}

<p>Heading copy: eyebrow <b>&#9670; How It Works</b>, h2 <b>From WhatsApp to Follow-Up, Made
Simple.</b>, sub <i>Four steps from your first message to a healthy smile, guided the whole
way.</i> &mdash; all left-aligned this time, not centred.</p>

{block('Container', 'how-step', [
  ('Layout', 'Direction', 'Row'),
  ('Layout', 'Gap', '28'),
  ('Layout', 'Width', '100%'),
  ('Advanced', 'Padding', pad(0,0,92,0)),
], note='The step heading is 27px / 600; the paragraph 15.5px / #5A6270 with Margin Top 12. On the fourth step set Padding Bottom to <b>10</b>.',
after=css('''
selector{position:relative}
selector::before{content:"";position:absolute;left:24px;top:54px;bottom:6px;
  width:1px;background:#E6E2D6}
selector:last-child::before{display:none}
'''))}

<table class="overview"><thead><tr><th>Icon</th><th>Heading</th><th>Text</th></tr></thead><tbody>
<tr><td>Comment</td><td>WhatsApp Us</td><td>Message 011-1608 3188 and the front desk will find a slot that fits you. The clinic fills up fast, so booking ahead beats walking in.</td></tr>
<tr><td>User</td><td>Consultation</td><td>Dr Tan checks your teeth, listens to your concerns and explains what she finds in plain language before anything is decided.</td></tr>
<tr><td>Tooth</td><td>Treatment</td><td>Gentle, unhurried treatment with proper numbing and a running explanation. Most patients are surprised when it's already over.</td></tr>
<tr><td>Envelope</td><td>Follow-Up</td><td>Aftercare instructions to take home and a reminder when your next checkup is due, so good habits actually stick.</td></tr>
</tbody></table>

<h3 class="sub">Responsive</h3>
<p><b>Tablet and Mobile:</b> how-grid Direction <b>Column</b>, gap <b>44</b>, both columns
Width <b>100%</b>, and change the how-sticky CSS to
<code>selector{{position:static}}</code>.</p>
""", BUILD))

# ---------------------------------------------------------------- 11 reviews
pages.append(step(11, 'Patient Stories', f"""
{shot('10-reviews.jpg', 'One featured review with a photo, then four shorter ones in a 2 × 2 grid.')}
{tree('''
Container   reviews            Boxed 1250   (CSS ID: reviews)
 ├ Container  sec-head
 └ Container  testi-tray       column · bg #E9E6DD · radius 24 · pad 10 · gap 10
     ├ Container  testi-featured   row · gap 10
     │    ├ Container  testi-photo    4:3 · radius 12
     │    └ Container  quote-card     bg #FFF · radius 12 · column
     │         ├ Heading    big quote
     │         └ Container  meta   row · space-between · align end
     │              ├ Container  name + role
     │              └ Star Rating
     └ Container  testi-grid       row · wrap · gap 10
          └ Container  testi-card ×4   bg #FFF · radius 12 · width 50%
               ├ Star Rating
               ├ Heading    quote
               ├ Divider
               └ Container  name + role
''')}

{block('Container', 'testi-photo', [
  ('Layout', 'Width', '38%'),
  ('Advanced', 'Border Radius', '12'),
  ('Advanced', 'Overflow', 'Hidden'),
], note='Image: <code>team-reception.jpg</code>, Full, 100% &times; 100%, Object Fit Cover.',
after=css('selector{aspect-ratio:4/3}'))}

{block('Container', 'quote-card', [
  ('Layout', 'Direction', 'Column'),
  ('Layout', 'Width', '62%'),
  ('Style', 'Background Color', '<code>#FFFFFF</code>'),
  ('Advanced', 'Border Radius', '12'),
  ('Advanced', 'Padding', dev(pad(40,44,34,44), pad(30,30,28,30), pad(26,26,26,26))),
], note='The big quote is a Heading, tag <b>p</b>, Inter <b>26px / 600</b>, line-height 1.35, letter-spacing &minus;0.4px, colour <code>#1F2833</code>. Tablet 23px, Mobile 19.5px.')}

{block('Star Rating', 'rating', [
  ('Content', 'Rating Scale', '5'),
  ('Content', 'Rating', '5'),
  ('Content', 'Unmarked Style', 'Solid'),
  ('Style', 'Size', '15'),
  ('Style', 'Star Color', '<code>#F0B428</code>'),
  ('Style', 'Spacing Between', '3'),
])}

<h3 class="sub">The five reviews</h3>
<table class="overview"><thead><tr><th>Quote</th><th>Name</th><th>Role line</th></tr></thead><tbody>
<tr><td><b>Featured &mdash;</b> "Two other clinics had suggested surgical removal. Dr Tan managed to remove it without any cutting. Truly painless, gentle, and very professional."</td><td>NSRN AMR</td><td>Google Review &middot; Local Guide</td></tr>
<tr><td>"The airflow scaling is almost no pain. Great explanation from the dentist on my teeth condition. Most importantly it's near to where I stay."</td><td>Thomas Teh</td><td>Scaling patient</td></tr>
<tr><td>"I personally named her my tooth fairy. Honestly don't wait on it. It's painless if you are done at Lumiere Dental, Kota Warisan!"</td><td>Izzati Azahar</td><td>Root canal patient</td></tr>
<tr><td>"They accept all insurance companies, so no worries as they are most likely your panel clinic. Do make an appointment before coming in."</td><td>Allan Manan</td><td>Scaling patient</td></tr>
<tr><td>"Dr Tan Mei Wen is so thorough and informative, and lets us know every step of the way what's going on. Personalized, comfortable and stress-free."</td><td>Noorhafizah Abd Samat</td><td>Local Guide &middot; 73 reviews</td></tr>
</tbody></table>
<p class="note">These are real Google reviews, retyped from the client's screenshots. Keep the
wording and the names exactly as they are &mdash; do not tidy the grammar.</p>

<p>Small card: Star Rating, then quote (tag p, 15.5px, line 1.55, <code>#1F2833</code>,
Margin Top 18), then a <b>Divider</b> (Weight 1, Color <code>#EFECE3</code>, Gap 20), then
name (15px / 600 / <code>#1F2833</code>) and role (14px / <code>#5A6270</code>).</p>

<h3 class="sub">Responsive</h3>
<p><b>Tablet and Mobile:</b> testi-featured Direction <b>Column</b> with both children at
100%, and testi-card Width <b>100%</b>.</p>
""", BUILD))

# ---------------------------------------------------------------- 12 faq
pages.append(step(12, 'FAQ', f"""
{shot('11-faq.jpg', 'Six questions, the first one open.')}
{tree('''
Container   faq                Boxed 1250 · column · align center   (CSS ID: faq)
 ├ Container  sec-head
 └ Container  faq-tray         bg #E9E6DD · radius 24 · pad 10 · max-width 620
      └ Accordion  faq-items   6 items
''')}

{block('Container', 'faq-tray', [
  ('Layout', 'Width', 'Custom &rarr; <b>620px</b>'),
  ('Style', 'Background Color', '<code>#E9E6DD</code>'),
  ('Advanced', 'Border Radius', '24'),
  ('Advanced', 'Padding', pad(10,10,10,10)),
])}

{block('Accordion', 'faq-items', [
  ('Content', 'Items', 'Six, from the table below'),
  ('Content', 'Layout &rsaquo; Icon', 'Plus / Minus (or Chevron)'),
  ('Content', 'Layout &rsaquo; FAQ Schema', '<b>On</b>'),
  ('Style', 'Header &rsaquo; Background', '<code>#FFFFFF</code>'),
  ('Style', 'Header &rsaquo; Typography', 'Inter &middot; 16.5px &middot; weight 500'),
  ('Style', 'Header &rsaquo; Text Color', '<code>#1F2833</code>'),
  ('Style', 'Header &rsaquo; Padding', pad(21,22,21,22)),
  ('Style', 'Header &rsaquo; Border Radius', '12'),
  ('Style', 'Content &rsaquo; Background', '<code>#FFFFFF</code>'),
  ('Style', 'Content &rsaquo; Typography', 'Inter &middot; 15.5px'),
  ('Style', 'Content &rsaquo; Text Color', '<code>#5A6270</code>'),
  ('Style', 'Content &rsaquo; Padding', pad(0,22,21,22)),
  ('Style', 'Items &rsaquo; Space Between', '10'),
], note='Icon settings and the FAQ Schema toggle are both on <b>Content &rsaquo; Layout</b> in Elementor 4.x. Turn the schema on &mdash; it is free rich-result eligibility for a page whose whole job is search and ads traffic.')}

<table class="faqt"><thead><tr><th>#</th><th>Question and answer</th></tr></thead><tbody>
<tr><td class="k">1</td><td><b>How do I book an appointment?</b><p>WhatsApp us at 011-1608 3188 and the front desk will confirm your slot, usually within the hour. You can also call the same number or walk in, though appointments are strongly recommended.</p></td></tr>
<tr><td class="k">2</td><td><b>Are you a panel clinic for my insurance?</b><p>We are a panel clinic for AIA, PMCare, Mednefits, HealthMetrics and MedKad. Message us your insurer and policy details and we will confirm your coverage before your visit.</p></td></tr>
<tr><td class="k">3</td><td><b>Can I just walk in?</b><p>Walk-ins are welcome when there is a free slot, but the clinic is fully booked most days. A quick WhatsApp before you come saves you the wait.</p></td></tr>
<tr><td class="k">4</td><td><b>What should I bring for my first visit?</b><p>Bring your IC or passport, your insurance or panel card if you have one, and any previous dental records or X-rays. That's all we need to get you started.</p></td></tr>
<tr><td class="k">5</td><td><b>Do you treat children?</b><p>Yes. The clinic has a dedicated kids corner, and Dr Tan paces every appointment around the child rather than the clock.</p></td></tr>
<tr><td class="k">6</td><td><b>Where exactly is the clinic?</b><p>G02 &amp; M03A, KIPMall Kota Warisan, Jalan Warisan Sentral 3, 43900 Sepang, Selangor. We are on the ground floor of KIPMall, with plenty of parking outside.</p></td></tr>
</tbody></table>
<p class="note">The mockup animates the icon from three bars to an &times;. Elementor's accordion
has its own icon set &mdash; use Plus / Minus and accept the difference, it is not worth custom
code.</p>
""", BUILD))

# ---------------------------------------------------------------- 13 contact
pages.append(step(13, 'Contact', f"""
{shot('12-contact.jpg', 'Details on the left, live Google map on the right.')}
{tree('''
Container   contact            Boxed 1250   (CSS ID: contact)
 ├ Container  sec-head
 └ Container  contact-grid     row · bg #E9E6DD · radius 24 · pad 10 · gap 14
     ├ Container  contact-info  bg #FFF · radius 12 · column · width 48%
     │    ├ Icon Box  ×4
     │    └ Button    Book On WhatsApp
     └ Container  contact-map   radius 12 · overflow hidden · width 52%
          └ HTML       map   ← paste file
''')}

{block('Icon Box', 'contact row', [
  ('Content', 'Icon', 'Map marker / Comment / Envelope / Clock'),
  ('Content', 'Title', 'see table'),
  ('Content', 'Description', 'see table'),
  ('Content', 'Link', 'see table'),
  ('Style', 'Box &rsaquo; Icon Position', '<b>Left</b>'),
  ('Style', 'Box &rsaquo; Vertical Alignment', '<b>Top</b>'),
  ('Style', 'Box &rsaquo; Icon Spacing', '16'),
  ('Style', 'Icon &rsaquo; View', 'Stacked'),
  ('Style', 'Icon &rsaquo; Primary Color', '<code>#8F702A</code>'),
  ('Style', 'Icon &rsaquo; Background', '<code>rgba(212,178,96,.16)</code>'),
  ('Style', 'Icon &rsaquo; Size', '22'),
  ('Style', 'Icon &rsaquo; Padding', '11'),
  ('Style', 'Icon &rsaquo; Border Radius', '12'),
  ('Style', 'Content &rsaquo; Title Typography', 'Inter &middot; 15.5px &middot; 600 &middot; <code>#1F2833</code>'),
  ('Style', 'Content &rsaquo; Description Typography', 'Inter &middot; 15px &middot; <code>#5A6270</code>'),
], note='Icon Position, Vertical Alignment and Icon Spacing all live under <b>Style &rsaquo; Box</b> in Elementor 4.x, not on the Content tab.')}

<table class="overview"><thead><tr><th>Title</th><th>Description</th><th>Link</th></tr></thead><tbody>
<tr><td>Visit the clinic</td><td>G02 &amp; M03A, KIPMall, Jalan Warisan Sentral 3,<br>Kota Warisan, 43900 Sepang, Selangor</td><td><code>maps.app.goo.gl/7LfYX7xw62fKfRQy7</code></td></tr>
<tr><td>WhatsApp or call</td><td>011-1608 3188</td><td>WhatsApp URL</td></tr>
<tr><td>Email us</td><td>lumieredentalclinics@gmail.com</td><td><code>mailto:</code> the same</td></tr>
<tr><td>Opening hours</td><td>Mon, Wed, Thu, Fri, Sat &nbsp;9:00am &ndash; 7:30pm<br>Tue &amp; Sun &nbsp;9:00am &ndash; 6:00pm</td><td>none</td></tr>
</tbody></table>
<p class="note"><b>Check the hours before publishing.</b> These come from the clinic's own
group website, but two directory listings disagree with them. It is the one fact on this page
most likely to be wrong, and the most annoying to a patient who turns up to a closed door.</p>

<h3 class="sub">The map</h3>
<p><b>contact-map</b>: Border Radius 12, Overflow <b>Hidden</b>, Min Height <b>420</b>.
Drop an <b>HTML</b> widget inside and paste <b>Step 13 - Map.html</b>. It is a plain Google
Maps embed &mdash; no API key needed.</p>

<h3 class="sub">Responsive</h3>
<p><b>Tablet and Mobile:</b> contact-grid Direction <b>Column</b>, both children Width
<b>100%</b>, contact-map Min Height <b>320</b>.</p>
""", PASTE))

# ---------------------------------------------------------------- 14 footer
pages.append(step(14, 'Footer and the WhatsApp button', f"""
{shot('13-footer.jpg', 'Full-bleed white band, content still held to 1250.')}
{tree('''
Container   footer             Full width · bg #FFF · border-top
 ├ Container  footer-card      Boxed 1250 · row · gap 44
 │    ├ Container  f-brand     logo · line · social icons
 │    ├ Container  f-links     Quick Links
 │    ├ Container  f-treat     Treatments
 │    └ Container  f-contact   Contact Us
 └ Container  footer-bar       Boxed 1250 · row · space-between
''')}

{block('Container', 'footer', [
  ('Layout', 'Content Width', 'Full Width'),
  ('Layout', 'Direction', 'Column'),
  ('Style', 'Background Color', '<code>#FFFFFF</code>'),
  ('Style', 'Border Type / Width / Color', 'Solid &middot; Top 1px &middot; <code>#E6E2D6</code>'),
  ('Advanced', 'Margin', pad(70,0,0,0)),
  ('Advanced', 'Padding', pad(0,0,0,0)),
], note='Full Width is what makes the white run edge to edge; the two Boxed children keep the text at 1250.')}

{block('Container', 'footer-card', [
  ('Layout', 'Content Width', 'Boxed'),
  ('Layout', 'Width', '1250'),
  ('Layout', 'Direction', 'Row'),
  ('Layout', 'Gap', '44'),
  ('Advanced', 'Padding', dev(pad(64,30,48,30), pad(36,30,36,30), pad(36,20,36,20))),
])}

<p>Column widths, left to right: <b>32% / 18% / 20% / 30%</b>. Column headings are
<b>16.5px / 600 / #1F2833</b> with Margin Bottom 20; links are <b>15.5px / #5A6270</b>,
hover <code>#1F2833</code>, Padding Top and Bottom 6.</p>

<table class="overview"><thead><tr><th>Column</th><th>Contents</th></tr></thead><tbody>
<tr><td>f-brand</td><td>Logo image (74px tall) &middot; "Lighting up your smile at KIPMall Kota Warisan, Sepang." &middot; four round social icons (Facebook, Instagram, WhatsApp, Google Maps) &mdash; 36px circles, background <code>#FAF9F5</code>, hover background <code>#33485C</code> with white glyph</td></tr>
<tr><td>f-links</td><td><b>Quick Links</b> &mdash; Home, About, Services, Reviews</td></tr>
<tr><td>f-treat</td><td><b>Treatments</b> &mdash; General Dentistry, Teeth Whitening, Dental Implants, Braces &amp; Aligners (all link to <code>#services</code>)</td></tr>
<tr><td>f-contact</td><td><b>Contact Us</b> &mdash; email, phone, address, each with a small gold icon</td></tr>
</tbody></table>

{block('Container', 'footer-bar', [
  ('Layout', 'Content Width', 'Boxed'),
  ('Layout', 'Width', '1250'),
  ('Layout', 'Direction', 'Row'),
  ('Layout', 'Justify Content', 'Space Between'),
  ('Style', 'Border Type / Width / Color', 'Solid &middot; Top 1px &middot; <code>#EFECE3</code>'),
  ('Advanced', 'Padding', dev(pad(22,30,28,30), pad(18,30,88,30), pad(18,20,88,20))),
], note='Left: &copy; 2026 Lumiere Dental Clinic Kota Warisan. All rights reserved. Right: Klinik Pergigian Lumiere &middot; &#20048;&#32654;&#29273;&#31185;&#35786;&#25152;. Both 14.5px / <code>#5A6270</code>. The big Bottom padding on tablet and mobile keeps this line clear of the floating button.')}

<h3 class="sub">The floating WhatsApp button</h3>
<p>Elementor Pro has this built in. <b>Templates &rsaquo; Add New &rsaquo; Floating Buttons</b>,
choose the WhatsApp type:</p>
{table([
  ('Content', 'Platform', 'WhatsApp'),
  ('Content', 'Number', '<code>601116083188</code>'),
  ('Content', 'Message', "Hi Lumiere Dental Kota Warisan, I'd like to book an appointment."),
  ('Style', 'Background Color', '<code>#25D366</code>'),
  ('Style', 'Icon Color', '<code>#FFFFFF</code>'),
  ('Style', 'Size', '58'),
  ('Advanced', 'Position', 'Bottom Right &middot; offset 24 / 24'),
])}
<p>Then set its Display Conditions to this page only, unless the clinic wants it site-wide.</p>

<h3 class="sub">Last: the entrance animations</h3>
<p>The mockup fades each block up as it comes into view. Select each section's first-level
container and set <b>Advanced &rsaquo; Motion Effects &rsaquo; Entrance Animation</b> to
<b>Fade In Up</b>, Duration <b>Slow</b>. On grouped cards, add
<b>Animation Delay</b> in steps of <b>100ms</b> across the row so they arrive one after another.</p>
<div class="donebox"><b>Done when:</b> the page scrolls from a full-height hero to a full-width
footer, the service cards stack as you scroll, and the WhatsApp button floats above
everything.</div>
""", BUILD))

# ---------------------------------------------------------------- QA
pages.append("""
<section class="step newpage"><div class="stephead"><span class="num">Finally</span>
<h2>Check these before you hand it over</h2></div>

<table class="check"><tbody>
<tr><td>&#9744;</td><td><b>The hero is exactly one screen tall</b> on a laptop and on a phone. If there is a gap under it on mobile, the <code>100dvh</code> line did not save.</td></tr>
<tr><td>&#9744;</td><td><b>The service cards stack.</b> If they scroll past each other normally, a parent container has Overflow set to Hidden &mdash; check <b>services</b> and <b>svc-stack</b>.</td></tr>
<tr><td>&#9744;</td><td><b>The Dr Tan photo travels</b> with the bio on desktop, and sits still on mobile.</td></tr>
<tr><td>&#9744;</td><td><b>No sideways scrolling</b> at 390px wide. Usually one container left at a fixed px width instead of 100%.</td></tr>
<tr><td>&#9744;</td><td><b>Every WhatsApp link opens with the message pre-filled</b>, and the eight service buttons each name their own treatment.</td></tr>
<tr><td>&#9744;</td><td><b>The six menu links jump</b> to the right section, and the header does not cover the heading when they land.</td></tr>
<tr><td>&#9744;</td><td><b>Nothing is cropped.</b> Compare each card against the live mockup &mdash; the ratios are deliberate.</td></tr>
<tr><td>&#9744;</td><td><b>Opening hours confirmed</b> with the clinic, not taken from this guide.</td></tr>
<tr><td>&#9744;</td><td><b>The two stat numbers confirmed</b> &mdash; "9+ years" and "5.0".</td></tr>
</tbody></table>

<h3 class="sub">Links you will need</h3>
<table class="overview"><thead><tr><th>What</th><th>Value</th></tr></thead><tbody>
<tr><td>WhatsApp (plain)</td><td><code>https://wa.me/601116083188</code></td></tr>
<tr><td>WhatsApp (booking)</td><td><code>https://wa.me/601116083188?text=Hi%20Lumiere%20Dental%20Kota%20Warisan%2C%20I%27d%20like%20to%20book%20an%20appointment.</code></td></tr>
<tr><td>Phone</td><td><code>tel:+601116083188</code></td></tr>
<tr><td>Email</td><td><code>lumieredentalclinics@gmail.com</code></td></tr>
<tr><td>Google Maps</td><td><code>https://maps.app.goo.gl/7LfYX7xw62fKfRQy7</code></td></tr>
<tr><td>Facebook</td><td><code>https://www.facebook.com/lumieredentalsepang</code></td></tr>
<tr><td>Instagram</td><td><code>https://www.instagram.com/lumieredentalsepang</code></td></tr>
<tr><td>Live mockup</td><td><code>https://mysense-my.github.io/lumiere-dental-kota-warisan/</code></td></tr>
</tbody></table>

<h3 class="sub">If something does not behave</h3>
<table class="overview"><thead><tr><th>Symptom</th><th>Cause</th><th>Fix</th></tr></thead><tbody>
<tr><td>Cards do not stack</td><td>Overflow: Hidden on a parent</td><td>Set every ancestor to Default</td></tr>
<tr><td>Sticky jumps instead of sliding</td><td>Motion Effects &rsaquo; Sticky was used</td><td>Turn it off, use the Custom CSS</td></tr>
<tr><td>Photo overflows its column</td><td>Container Align Items on Stretch</td><td>Set the parent to Align Items: Start</td></tr>
<tr><td>Image looks soft</td><td>Resolution left on Large</td><td>Set Image Resolution to Full</td></tr>
<tr><td>A control is not where this guide says</td><td>Elementor version difference</td><td>Send a screenshot of that panel</td></tr>
</tbody></table>
</section>
""")

CSS = """
@page{size:A4;margin:14mm 14mm 16mm}
*{box-sizing:border-box}
body{font-family:Inter,system-ui,sans-serif;color:#1F2833;font-size:10.5px;line-height:1.5;margin:0}
h1,h2,h3,h4{margin:0;font-weight:600;letter-spacing:-.02em}
code{font-family:Menlo,monospace;font-size:.92em;background:#F3F1EA;padding:1px 5px;border-radius:4px;color:#6b5210}
b{font-weight:600}
.cover h1{font-size:30px;line-height:1.15;margin:4px 0 12px;max-width:520px}
.kicker{font-weight:600;color:#8F702A;margin:0}
.lead{font-size:13px;color:#5A6270;max-width:560px;margin:0 0 18px}
.facts{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:20px}
.facts div{background:#F3F1EA;border-radius:10px;padding:10px 12px;display:grid;gap:2px}
.facts b{font-size:9.5px;color:#5A6270;font-weight:600}
.cover h3{font-size:14px;margin:14px 0 8px}
table{border-collapse:collapse;width:100%}
.overview th,.overview td{padding:7px 9px;border-bottom:1px solid #E6E2D6;text-align:left;font-size:10.5px;vertical-align:top}
.overview th{color:#5A6270;font-weight:600;font-size:10px;background:#F3F1EA}
.overview p{margin:3px 0 0;color:#5A6270}
.newpage{break-before:page}
.step{margin-bottom:18px}
.stephead{display:flex;align-items:center;gap:10px;flex-wrap:wrap;padding-bottom:8px;margin-bottom:10px;border-bottom:2px solid #1F2833}
.stephead .num{background:#33485C;color:#fff;border-radius:6px;padding:3px 9px;font-weight:600;font-size:12px}
.stephead h2{font-size:19px}
.badge{margin-left:auto;border-radius:20px;padding:3px 10px;font-weight:600;font-size:10.5px}
.badge.paste{background:#FFF3CF;color:#6b4e00}
.badge.build{background:#E9E6DD;color:#4a5462}
.shot{margin:0 0 10px;break-inside:avoid}
.shot img{width:100%;max-height:238px;object-fit:cover;object-position:top;border-radius:8px;border:1px solid #E6E2D6;display:block}
.shot figcaption{font-size:9.5px;color:#5A6270;margin-top:3px}
.tree{font-family:Menlo,monospace;font-size:9.2px;line-height:1.55;background:#1F2833;color:#EDEAE0;border-radius:8px;padding:10px 12px;margin:0 0 10px;white-space:pre;break-inside:avoid}
.note{background:#F7F5EE;border-left:3px solid #C9A64D;padding:6px 9px;margin:6px 0;border-radius:0 6px 6px 0;color:#3a3f48}
.donebox{background:#EDF3EC;border-left:3px solid #4F6B3C;padding:8px 10px;border-radius:0 6px 6px 0;margin-top:10px}
.do{margin:6px 0 10px;padding-left:18px}
.do li{margin:4px 0}
.block{margin:0 0 12px;break-inside:avoid}
.block h4{font-size:12px;margin:0 0 5px;display:flex;align-items:center;gap:7px;flex-wrap:wrap}
.block h4 .kind{background:#8F702A;color:#fff;border-radius:5px;padding:2px 7px;font-size:10px;font-weight:600}
.set th{background:#F3F1EA;text-align:left;font-size:9.5px;color:#5A6270;padding:5px 8px;font-weight:600}
.set td{padding:5px 8px;border-bottom:1px solid #E6E2D6;vertical-align:top}
.set td.tab{width:62px;color:#5A6270;font-weight:600}
.set td:nth-child(2){width:158px;font-weight:600}
.code{font-family:Menlo,monospace;font-size:9.3px;line-height:1.5;background:#F3F1EA;border:1px solid #E6E2D6;border-radius:6px;padding:8px 10px;margin:6px 0 0;white-space:pre-wrap;word-break:break-word;color:#2a2f38}
h3.sub{font-size:13.5px;margin:16px 0 8px;padding-top:6px;border-top:1px dashed #D8D3C4;break-after:avoid}
.svc th{background:#1F2833;color:#fff;text-align:left;padding:6px 9px;font-size:10px}
.svc td{padding:6px 9px;border-bottom:1px solid #E6E2D6;vertical-align:top;font-size:10px}
.svc td.n{width:18px;color:#8F702A;font-weight:600}
.svc td:nth-child(2){width:150px}
.svc p{margin:3px 0;color:#5A6270}
.svc .li{display:block;margin-top:4px;color:#5A6270;font-size:9.4px}
.faqt th{background:#F3F1EA;text-align:left;padding:6px 9px;font-size:10px;color:#5A6270}
.faqt td{padding:6px 9px;border-bottom:1px solid #E6E2D6;vertical-align:top}
.faqt td.k{width:22px;color:#8F702A;font-weight:600}
.faqt p{margin:3px 0 0;color:#5A6270}
.check td{padding:7px 9px;border-bottom:1px solid #E6E2D6;vertical-align:top}
.check td:first-child{width:20px;font-size:13px}
"""

doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Lumiere Dental Kota Warisan &middot; Elementor build steps</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>{''.join(pages)}</body></html>"""
open(OUT, 'w', encoding='utf-8').write(doc)
print('wrote', OUT, len(doc) // 1024, 'KB')
