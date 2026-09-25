#!/usr/bin/env python3
"""Writes elementor/steps.html — the printable Elementor build guide.

Rule: every container and widget that appears in a tree diagram must ALSO get a
full Tab / Setting / Value table. Nothing is left in prose only, and nothing is
cross-referenced as "same as step N".
"""
import html, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'steps.html')
IMG = 'guide-img/'
e = html.escape

WA = 'https://wa.me/601116083188?text=Hi%20Lumiere%20Dental%20Kota%20Warisan%2C%20I%27d%20like%20to%20book%20an%20appointment.'
WAPANEL = 'https://wa.me/601116083188?text=Hi%2C%20could%20you%20check%20if%20my%20insurance%20panel%20is%20accepted%3F'

def dev(d, t=None, m=None, unit=''):
    if t is None and m is None:
        return f'{d}{unit}'
    parts = [f'<b>Desktop</b> {d}{unit}']
    if t is not None: parts.append(f'<b>Tablet</b> {t}{unit}')
    if m is not None: parts.append(f'<b>Mobile</b> {m}{unit}')
    return ' &nbsp;&middot;&nbsp; '.join(parts)

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
    return (f'<div class="block"><h4><span class="kind">{kind}</span> {name}</h4>'
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

def shell(name, cssid):
    return block('Container', name, [
      ('Layout', 'Container Layout', 'Flexbox'),
      ('Layout', 'Content Width', 'Boxed'),
      ('Layout', 'Width', '1250'),
      ('Layout', 'Direction', 'Column'),
      ('Layout', 'Align Items', 'Center'),
      ('Layout', 'Gap', '0'),
      ('Advanced', 'Padding', dev(pad(90,30,40,30), pad(90,30,40,30), pad(64,20,28,20))),
      ('Advanced', 'Overflow', 'Default'),
      ('Advanced', 'CSS ID', f'<code>{cssid}</code>'),
    ], note='The CSS ID is what the header menu links jump to. Type it without the #.')

def sechead(eyebrow, h2, sub, centered=True):
    al = 'Center' if centered else 'Start'
    ta = 'Center' if centered else 'Left'
    out = block('Container', 'sec-head', [
      ('Layout', 'Container Layout', 'Flexbox'),
      ('Layout', 'Direction', 'Column'),
      ('Layout', 'Align Items', al),
      ('Layout', 'Width', 'Custom &rarr; <b>640</b> PX' if centered else '<b>100</b> %'),
      ('Layout', 'Gap', '0'),
      ('Advanced', 'Padding', pad(0,0,0,0)),
      ('Advanced', 'Margin', pad(0,0,38,0)),
    ])
    out += block('Heading', 'eyebrow', [
      ('Content', 'Title', f'&#9670; {eyebrow}'),
      ('Content', 'HTML Tag', 'p'),
      ('Style', 'Alignment', ta),
      ('Style', 'Text Color', '<code>#8F702A</code>'),
      ('Style', 'Typography &rsaquo; Family', 'Inter'),
      ('Style', 'Typography &rsaquo; Size', '15 PX'),
      ('Style', 'Typography &rsaquo; Weight', '500'),
      ('Advanced', 'Margin', pad(0,0,14,0)),
    ], note='&#9670; is a typed character &mdash; copy it from this line, then a space, then the words.')
    out += block('Heading', 'h2', [
      ('Content', 'Title', h2),
      ('Content', 'HTML Tag', 'h2'),
      ('Style', 'Alignment', ta),
      ('Style', 'Text Color', '<code>#1F2833</code>'),
      ('Style', 'Typography &rsaquo; Family', 'Inter'),
      ('Style', 'Typography &rsaquo; Size', dev('46', '38', '29', ' PX')),
      ('Style', 'Typography &rsaquo; Weight', '600'),
      ('Style', 'Typography &rsaquo; Line Height', '1.22 EM'),
      ('Style', 'Typography &rsaquo; Letter Spacing', dev('&minus;0.9', '&minus;0.8', '&minus;0.6', ' PX')),
      ('Advanced', 'Margin', pad(0,0,0,0)),
    ], note='Type the <code>&lt;br&gt;</code> into the Title field exactly where it appears above.')
    if sub:
        out += block('Heading', 'sub', [
          ('Content', 'Title', sub),
          ('Content', 'HTML Tag', 'p'),
          ('Style', 'Alignment', ta),
          ('Style', 'Text Color', '<code>#5A6270</code>'),
          ('Style', 'Typography &rsaquo; Family', 'Inter'),
          ('Style', 'Typography &rsaquo; Size', '16 PX'),
          ('Style', 'Typography &rsaquo; Weight', '400'),
          ('Style', 'Typography &rsaquo; Line Height', '1.4 EM'),
          ('Advanced', 'Margin', pad(16,0,0,0)),
        ])
    return out

def icontile(label, picker, cls):
    return block('Icon', label, [
      ('Content', 'Icon', f'search <b>{picker}</b> &nbsp;(<code>{cls}</code>)'),
      ('Content', 'View', '<b>Stacked</b>'),
      ('Content', 'Shape', '<b>Square</b>'),
      ('Style', 'Alignment', 'Left'),
      ('Style', 'Primary Color', '<code>#8F702A</code>'),
      ('Style', 'Secondary Color', '<code>rgba(212,178,96,.16)</code>'),
      ('Style', 'Size', '24 PX'),
      ('Style', 'Padding', '12 PX'),
      ('Style', 'Border Radius', '12 PX'),
      ('Advanced', 'Margin', pad(0,0,0,0)),
    ], note='With View: Stacked the tile background is <b>Secondary Color</b> and the glyph is <b>Primary Color</b>.')

def para(name, text, size='15', color='#5A6270', lh='1.6', mt=0, mb=12, weight='400', align='Left'):
    return block('Heading', name, [
      ('Content', 'Title', text),
      ('Content', 'HTML Tag', 'p'),
      ('Style', 'Alignment', align),
      ('Style', 'Text Color', f'<code>{color}</code>'),
      ('Style', 'Typography &rsaquo; Family', 'Inter'),
      ('Style', 'Typography &rsaquo; Size', f'{size} PX'),
      ('Style', 'Typography &rsaquo; Weight', weight),
      ('Style', 'Typography &rsaquo; Line Height', f'{lh} EM'),
      ('Advanced', 'Margin', pad(mt,0,mb,0)),
    ])

pages = []

# ------------------------------------------------------------------ cover
pages.append(f"""
<section class="cover">
<p class="kicker">Lumiere Dental Clinic &middot; Kota Warisan</p>
<h1>Landing page build steps for Elementor</h1>
<p class="lead">One page, fourteen sections, top to bottom. Every container and every widget
below has its own settings table. Nothing is left for you to guess, and nothing says
"same as an earlier step" &mdash; work straight through in order.</p>

<div class="facts">
  <div><b>Built for</b>Elementor Pro 4.1.2</div>
  <div><b>Steps</b>14</div>
  <div><b>Content width</b>1250 boxed</div>
  <div><b>Font</b>Inter (Google Fonts)</div>
  <div><b>Page background</b>#FAF9F5</div>
  <div><b>Images to upload</b>31</div>
</div>

<p class="note">Keep the finished page open on a second screen while you build:
<code>mysense-my.github.io/lumiere-dental-kota-warisan</code>. If a value here ever looks
wrong, that page is the truth.</p>

<h3>How to read a settings table</h3>
<table class="set"><thead><tr><th>Tab</th><th>Setting</th><th>Value</th></tr></thead><tbody>
<tr><td class="tab">Layout</td><td>Width</td><td>1250</td></tr>
<tr><td class="tab">Advanced</td><td>Padding</td><td>Top 90 &nbsp; Right 30 &nbsp; Bottom 40 &nbsp; Left 30</td></tr>
<tr><td class="tab">Style</td><td>Typography &rsaquo; Size</td><td><b>Desktop</b> 46 PX &nbsp;&middot;&nbsp; <b>Tablet</b> 38 PX &nbsp;&middot;&nbsp; <b>Mobile</b> 29 PX</td></tr>
</tbody></table>
<p class="cap">Column one is the panel tab to open. Padding and margin are always written per
side in that order. Where a row lists Desktop / Tablet / Mobile, switch device view with the
icons at the bottom of the panel and set each one &mdash; a mobile value never touches desktop.
Where a row says <b>PX</b>, <b>EM</b> or <b>%</b>, that is the unit selector beside the field.</p>

<h3>What you are building</h3>
<table class="overview"><thead><tr><th>Step</th><th>Section</th><th>How</th></tr></thead><tbody>
<tr><td>1</td><td>Page setup, menu, fonts, global CSS</td><td>Settings only</td></tr>
<tr><td>2</td><td>Header, including the mobile drawer</td><td>Widgets + CSS</td></tr>
<tr><td>3</td><td>Hero</td><td>Widgets + 1 paste</td></tr>
<tr><td>4</td><td>Our Panels</td><td>Widgets</td></tr>
<tr><td>5</td><td>Why Lumiere</td><td>Widgets</td></tr>
<tr><td>6</td><td>Dr Tan biography</td><td>Widgets + CSS</td></tr>
<tr><td>7</td><td>Stats counters</td><td>Widgets</td></tr>
<tr><td>8</td><td>Services &times; 8</td><td>Widgets + CSS</td></tr>
<tr><td>9</td><td>Our Clinic</td><td>Widgets + CSS</td></tr>
<tr><td>10</td><td>How It Works</td><td>Widgets + CSS</td></tr>
<tr><td>11</td><td>Patient Stories</td><td>Widgets</td></tr>
<tr><td>12</td><td>FAQ</td><td>Widgets</td></tr>
<tr><td>13</td><td>Contact</td><td>Widgets + 1 paste</td></tr>
<tr><td>14</td><td>Footer, WhatsApp button, animations</td><td>Widgets</td></tr>
</tbody></table>

<h3>Four rules that apply everywhere</h3>
<ul class="do">
<li><b>No Site Settings globals.</b> Every colour and font is typed in per widget from these
tables. Do not create global colours or global fonts.</li>
<li><b>Name every container</b> in the Structure panel the moment you create it, using the name
from the tree diagram. Right-click the container &rarr; Rename.</li>
<li><b>Build one, then duplicate.</b> Where a card repeats, finish the first completely, then
right-click &rarr; Duplicate and change only the content.</li>
<li><b>Leave Advanced &rsaquo; Overflow on Default</b> unless a table says Hidden. Three
sections depend on CSS sticky, and one parent set to Hidden silently kills it.</li>
</ul>
</section>
""")

# ------------------------------------------------------------------ reference
pages.append("""
<section class="step newpage"><div class="stephead"><span class="num">Before you start</span>
<h2>Images, colours, type</h2></div>

<h3 class="sub">Upload the images</h3>
<p>All 31 files are in <b>1 - Upload to Media Library</b>. Select everything, including what is
inside the <code>icons</code> and <code>panels</code> subfolders, and drop it into
<b>Media &rsaquo; Add New</b>. WordPress ignores the folders; they exist only so the filenames
match this guide.</p>
<p class="note">Whenever you place an image set <b>Image Resolution: Full</b>. Every file is
already cropped and compressed for its slot. Do not resize, and do not let Elementor serve a
smaller size &mdash; that is what makes a photo look soft.</p>

<h3 class="sub">The palette</h3>
<table class="overview"><thead><tr><th>Hex</th><th>Used for</th></tr></thead><tbody>
<tr><td><code>#1F2833</code></td><td>Every H1, H2, H3, and body text inside white cards</td></tr>
<tr><td><code>#5A6270</code></td><td>Every paragraph and secondary line</td></tr>
<tr><td><code>#33485C</code></td><td>Button fill &mdash; hover <code>#26394B</code></td></tr>
<tr><td><code>#8F702A</code></td><td>Eyebrow text, icon glyphs, pill text</td></tr>
<tr><td><code>rgba(212,178,96,.16)</code></td><td>Icon tile and pill background</td></tr>
<tr><td><code>#E8D397</code></td><td>Hero button hover, the ring on Dr Tan's portrait</td></tr>
<tr><td><code>#FAF9F5</code></td><td>Page background, social icon circles</td></tr>
<tr><td><code>#FFFFFF</code></td><td>Every white card, the footer band</td></tr>
<tr><td><code>#E9E6DD</code></td><td>The grey tray behind each group of cards</td></tr>
<tr><td><code>#E6E2D6</code></td><td>Hairline borders, the How It Works spine</td></tr>
<tr><td><code>#EFECE3</code></td><td>Dividers inside white cards, the quote watermark</td></tr>
<tr><td><code>#F0B428</code></td><td>Review stars</td></tr>
<tr><td><code>#25D366</code></td><td>Floating WhatsApp button</td></tr>
<tr><td><code>rgba(16,28,42,.8)</code></td><td>Photo caption scrim in Step 9</td></tr>
</tbody></table>

<h3 class="sub">Type scale</h3>
<table class="overview"><thead><tr><th>Element</th><th>Desktop</th><th>Tablet</th><th>Mobile</th><th>Weight</th><th>Line</th><th>Letter spacing</th></tr></thead><tbody>
<tr><td>H1 hero</td><td>56</td><td>46</td><td>33</td><td>600</td><td>1.2</td><td>&minus;2.5 / &minus;2.1 / &minus;1.5</td></tr>
<tr><td>H2 section</td><td>46</td><td>38</td><td>29</td><td>600</td><td>1.22</td><td>&minus;0.9 / &minus;0.8 / &minus;0.6</td></tr>
<tr><td>H2 service card</td><td>41</td><td>25</td><td>23</td><td>600</td><td>1.22</td><td>&minus;0.9</td></tr>
<tr><td>Featured quote</td><td>26</td><td>23</td><td>19.5</td><td>600</td><td>1.35</td><td>&minus;0.4</td></tr>
<tr><td>How-step H3</td><td>27</td><td>27</td><td>24</td><td>600</td><td>1.3</td><td>&minus;0.3</td></tr>
<tr><td>Dr Tan name</td><td>23</td><td>23</td><td>20</td><td>600</td><td>1.3</td><td>&minus;0.3</td></tr>
<tr><td>Card H3</td><td>19.5&ndash;22</td><td>same</td><td>same</td><td>600</td><td>1.3</td><td>0</td></tr>
<tr><td>Body / paragraph</td><td>15&ndash;16</td><td>same</td><td>same</td><td>400</td><td>1.4&ndash;1.6</td><td>0</td></tr>
<tr><td>Eyebrow</td><td>15</td><td>15</td><td>15</td><td>500</td><td>1.4</td><td>0</td></tr>
</tbody></table>
<p class="note">Elementor writes letter spacing in <b>px</b>, not em. The values above are
already converted &mdash; type them as shown, including the minus sign.</p>

<h3 class="sub">About the fonts</h3>
<p><b>Inter</b> is a Google Font. The first time you pick it in any Typography control,
Elementor loads it for the whole page. There is nothing to install.</p>
<p>The original design uses <b>Satoshi</b> for the four big stat numbers. Satoshi is not a
Google Font and is almost certainly not on this site. <b>Use Inter at weight 500 for those
numbers.</b> Do not go hunting for Satoshi; the difference is invisible at a glance.</p>
</section>
""")

# ------------------------------------------------------------------ 1
pages.append(step(1, 'Page setup, menu, and the global CSS', f"""
<p>Four things before a single widget goes down. The last one fixes a problem that is very
annoying to diagnose later.</p>

<h3 class="sub">1a &middot; Build the menu first</h3>
<p>The header links jump to anchors on this one page, so the menu is made of Custom Links.
<b>Appearance &rsaquo; Menus</b> &rarr; create a menu named <b>Lumiere Landing</b> &rarr; open
the <b>Custom Links</b> panel and add these six in order.</p>
<table class="overview"><thead><tr><th>URL</th><th>Link Text</th></tr></thead><tbody>
<tr><td><code>#home</code></td><td>Home</td></tr>
<tr><td><code>#about</code></td><td>About</td></tr>
<tr><td><code>#services</code></td><td>Services</td></tr>
<tr><td><code>#reviews</code></td><td>Reviews</td></tr>
<tr><td><code>#faq</code></td><td>FAQ</td></tr>
<tr><td><code>#contact</code></td><td>Contact</td></tr>
</tbody></table>
<p class="note">Leave every <b>Display location</b> checkbox unticked, then Save Menu. This
menu is only ever pulled in by the Nav Menu widget in Step 2. Tick a location and it also
appears in the theme header, which this page does not use.</p>

<h3 class="sub">1b &middot; Create the page</h3>
<p><b>Pages &rsaquo; Add New</b>. Title:
<b>Dental Pain? Get Expert Care in Kota Warisan</b>. Publish, then <b>Edit with Elementor</b>.</p>
<p>Open <b>Page Settings</b> &mdash; the gear icon at the bottom-left of the Elementor panel:</p>
{table([
  ('Settings', 'Page Layout', '<b>Elementor Canvas</b>'),
  ('Settings', 'Hide Title', 'On'),
  ('Style', 'Background Type', 'Classic'),
  ('Style', 'Background Color', '<code>#FAF9F5</code>'),
])}
<p class="note"><b>Elementor Canvas</b> removes the theme's own header and footer. That is
deliberate: this page carries its own header (Step 2) and footer (Step 14), which is what
makes it work as a standalone ads landing page.</p>

<h3 class="sub">1c &middot; SEO title, description, site icon</h3>
<p>In the WordPress editor, not Elementor, open your SEO plugin's panel for this page:</p>
<table class="overview"><thead><tr><th>Field</th><th>Value</th></tr></thead><tbody>
<tr><td>SEO title</td><td>Dental Pain? Get Expert Care in Kota Warisan &ndash; Lumiere Dental</td></tr>
<tr><td>Meta description</td><td>Experiencing dental pain? Our Kota Warisan dental clinic provides gentle care to help restore your smile. General dentistry, whitening, implants, braces and more at KIPMall Kota Warisan, Sepang.</td></tr>
</tbody></table>
<p>For the browser-tab icon: <b>Appearance &rsaquo; Customize &rsaquo; Site Identity &rsaquo;
Site Icon</b> &rarr; <code>favicon.png</code>. This is site-wide, so only do it if the clinic
is happy for it to change everywhere.</p>

<h3 class="sub">1d &middot; The global CSS block</h3>
<p>Still in <b>Page Settings</b>, open the <b>Advanced</b> tab &rarr; <b>Custom CSS</b> and
paste this. Two lines, both necessary.</p>
{css('''
html{scroll-behavior:smooth}
#home,#panels,#about,#services,#facilities,#how,#reviews,#faq,#contact{scroll-margin-top:110px}
''')}
<table class="overview"><thead><tr><th>Line</th><th>What it does</th></tr></thead><tbody>
<tr><td><code>scroll-behavior</code></td><td>Makes the menu links glide instead of snapping.</td></tr>
<tr><td><code>scroll-margin-top</code></td><td><b>Without this the sticky header covers the heading you just jumped to.</b> The header is about 92px tall, so every anchor stops 110px early. If you ever change the header height, change this number to match.</td></tr>
</tbody></table>
<div class="donebox"><b>Done when:</b> an empty canvas on warm off-white, a "Lumiere Landing"
menu saved under Appearance &rsaquo; Menus, and two lines in the page's Custom CSS.</div>
""", BUILD))

# ------------------------------------------------------------------ 2 header
pages.append(step(2, 'Header', f"""
{shot('01-header.jpg', 'Transparent over the hero photo, then a solid white bar once you scroll past it.')}
{tree('''
Container   header            Full width - sticky - z-index 100
 |- Container  header-inner    Boxed 1250 - row - space-between
    |- Container  brand        row - gap 13
    |   |- Image     logo
    |   |- Heading   brand-name
    |- Nav Menu   main-nav
    |- Button     nav-cta
''')}

{block('Container', 'header', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Content Width', 'Full Width'),
  ('Layout', 'Direction', 'Column'),
  ('Layout', 'Gap', '0'),
  ('Advanced', 'Padding', pad(0,0,0,0)),
  ('Advanced', 'Margin', pad(0,0,0,0)),
  ('Advanced', 'Z-Index', '100'),
  ('Advanced', 'Motion Effects &rsaquo; Sticky', '<b>Top</b>'),
  ('Advanced', 'Motion Effects &rsaquo; Sticky On', 'Desktop, Tablet, Mobile'),
  ('Advanced', 'Motion Effects &rsaquo; Offset', '0'),
], note='This is the ONE place in the build where Elementor&rsquo;s own Sticky is correct. It adds the class <code>elementor-sticky--effects</code> once the header starts sticking, and the CSS at the end of this step uses that class to swap the colours.')}

{block('Container', 'header-inner', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Content Width', 'Boxed'),
  ('Layout', 'Width', '1250'),
  ('Layout', 'Direction', 'Row'),
  ('Layout', 'Justify Content', 'Space Between'),
  ('Layout', 'Align Items', 'Center'),
  ('Layout', 'Gap', '30'),
  ('Advanced', 'Padding', dev(pad(18,30,18,30), pad(18,30,18,30), pad(13,20,13,20))),
])}

{block('Container', 'brand', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Direction', 'Row'),
  ('Layout', 'Align Items', 'Center'),
  ('Layout', 'Gap', '13'),
  ('Layout', 'Width', 'leave empty so it hugs its content'),
  ('Advanced', 'Padding', pad(0,0,0,0)),
])}

{block('Image', 'logo', [
  ('Content', 'Choose Image', '<code>logo-gold.png</code>'),
  ('Content', 'Image Resolution', '<b>Full</b>'),
  ('Content', 'Caption', 'None'),
  ('Content', 'Link', 'Custom URL &rarr; <code>#home</code>'),
  ('Style', 'Width', dev('56', '48', '44', ' PX')),
  ('Style', 'Max Width', '100 %'),
  ('Advanced', 'Margin', pad(0,0,0,0)),
])}

{block('Heading', 'brand-name', [
  ('Content', 'Title', 'Lumiere Dental'),
  ('Content', 'Link', 'Custom URL &rarr; <code>#home</code>'),
  ('Content', 'HTML Tag', 'p'),
  ('Style', 'Alignment', 'Left'),
  ('Style', 'Text Color', '<code>#FFFFFF</code>'),
  ('Style', 'Typography &rsaquo; Family', 'Inter'),
  ('Style', 'Typography &rsaquo; Size', dev('21', '19', '17.5', ' PX')),
  ('Style', 'Typography &rsaquo; Weight', '600'),
  ('Advanced', 'Margin', pad(0,0,0,0)),
])}

{block('Nav Menu', 'main-nav', [
  ('Content', 'Menu', '<b>Lumiere Landing</b>'),
  ('Content', 'Layout', 'Horizontal'),
  ('Content', 'Align', 'Center'),
  ('Content', 'Pointer', '<b>None</b>'),
  ('Content', 'Breakpoint', '<b>Tablet (&le; 1024)</b>'),
  ('Style', 'Main Menu &rsaquo; Typography &rsaquo; Family', 'Inter'),
  ('Style', 'Main Menu &rsaquo; Typography &rsaquo; Size', '16.5 PX'),
  ('Style', 'Main Menu &rsaquo; Typography &rsaquo; Weight', '400'),
  ('Style', 'Main Menu &rsaquo; Text Color (Normal)', '<code>rgba(255,255,255,.86)</code>'),
  ('Style', 'Main Menu &rsaquo; Text Color (Hover)', '<code>#FFFFFF</code>'),
  ('Style', 'Main Menu &rsaquo; Horizontal Padding', '15'),
  ('Style', 'Main Menu &rsaquo; Vertical Padding', '0'),
  ('Style', 'Toggle Button &rsaquo; Align', 'Right'),
  ('Style', 'Toggle Button &rsaquo; Color (Normal)', '<code>#FFFFFF</code>'),
  ('Style', 'Toggle Button &rsaquo; Size', '22'),
], note='<b>Pointer: None</b> removes Elementor&rsquo;s default underline-on-hover, which this design does not have.')}

<h3 class="sub">The mobile drawer</h3>
<p>Below 1024px the menu collapses to a hamburger and the links drop into a panel. Style that
panel too, or it inherits theme colours and looks broken. Same widget, Style tab, Dropdown
section.</p>
{block('Nav Menu', 'main-nav &mdash; Dropdown section', [
  ('Style', 'Dropdown &rsaquo; Text Color (Normal)', '<code>#1F2833</code>'),
  ('Style', 'Dropdown &rsaquo; Background (Normal)', '<code>#FAF9F5</code>'),
  ('Style', 'Dropdown &rsaquo; Text Color (Hover)', '<code>#8F702A</code>'),
  ('Style', 'Dropdown &rsaquo; Background (Hover)', '<code>#FFFFFF</code>'),
  ('Style', 'Dropdown &rsaquo; Typography &rsaquo; Family', 'Inter'),
  ('Style', 'Dropdown &rsaquo; Typography &rsaquo; Size', '16.5 PX'),
  ('Style', 'Dropdown &rsaquo; Typography &rsaquo; Weight', '500'),
  ('Style', 'Dropdown &rsaquo; Divider', 'Solid &middot; 1 &middot; <code>#EFECE3</code>'),
  ('Style', 'Dropdown &rsaquo; Item Padding', pad(12,20,12,20)),
  ('Style', 'Dropdown &rsaquo; Full Width', '<b>Off</b>'),
], note='Leave <b>Full Width</b> off. Turned on, the dropdown stretches past the sticky header and the first link ends up sitting under the logo.')}

{block('Button', 'nav-cta', [
  ('Content', 'Text', 'Book An Appointment'),
  ('Content', 'Link', f'<code>{WA}</code>'),
  ('Content', 'Link &rsaquo; Open in new window', 'On'),
  ('Content', 'Icon', 'search <b>Arrow Right</b> &nbsp;(<code>fas fa-arrow-right</code>)'),
  ('Content', 'Icon Position', '<b>After</b>'),
  ('Content', 'Icon Spacing', '9'),
  ('Style', 'Button &rsaquo; Position', '<b>Right</b>'),
  ('Style', 'Typography &rsaquo; Family', 'Inter'),
  ('Style', 'Typography &rsaquo; Size', '15.5 PX'),
  ('Style', 'Typography &rsaquo; Weight', '500'),
  ('Style', 'Text Color (Normal)', '<code>#33485C</code>'),
  ('Style', 'Background (Normal)', '<code>#FFFFFF</code>'),
  ('Style', 'Text Color (Hover)', '<code>#1F2833</code>'),
  ('Style', 'Background (Hover)', '<code>#E8D397</code>'),
  ('Style', 'Border Radius', '8 PX'),
  ('Style', 'Padding', pad(13,24,13,24)),
  ('Advanced', 'Responsive &rsaquo; Hide On Tablet', '<b>On</b>'),
  ('Advanced', 'Responsive &rsaquo; Hide On Mobile', '<b>On</b>'),
], note='Button alignment is <b>Style &rsaquo; Button &rsaquo; Position</b> in Elementor 4.x, not the Content tab. The button hides below 1024 because the hamburger needs that space, and the hero already carries the same call to action.')}

<h3 class="sub">The scrolled state</h3>
<p>Select the <b>header</b> container &rarr; <b>Advanced &rsaquo; Custom CSS</b> and paste all
of this. It is the entire "turns white on scroll" behaviour.</p>
{css('''
selector.elementor-sticky--effects{
  background:rgba(250,249,245,.93);
  backdrop-filter:blur(12px);
  box-shadow:0 1px 0 #E6E2D6, 0 8px 24px -18px rgba(31,40,51,.25);
}
selector.elementor-sticky--effects .elementor-heading-title{color:#1F2833}
selector.elementor-sticky--effects .elementor-item{color:#5A6270}
selector.elementor-sticky--effects .elementor-item:hover{color:#1F2833}
selector.elementor-sticky--effects .elementor-button{background:#33485C;color:#fff}
selector.elementor-sticky--effects .elementor-menu-toggle{color:#1F2833}
''')}
<div class="donebox"><b>Done when:</b> the header is invisible against the hero, then fades
into a white bar with dark links as you scroll. Under 1024px the hamburger opens a cream
panel with dark links.</div>
""", BUILD))

# ------------------------------------------------------------------ 3 hero
pages.append(step(3, 'Hero', f"""
{shot('02-hero.jpg', 'Exactly one screen tall on every device. Dark gradient over the lobby photo so white type stays readable.')}
{tree('''
Container   hero              Full width - 100dvh - bg photo + overlay
 |- Container  hero-inner      Boxed 1250 - column - align start - z-index 2
    |- Container  hero-badges  row - wrap - gap 8
    |   |- Heading  badge-trusted
    |   |- Heading  badge-place
    |- Heading   hero-h1
    |- Heading   hero-sub
    |- Container hero-actions  row - gap 12
    |   |- Button   btn-book
    |   |- Button   btn-services
    |- HTML      hero-proof    <-- paste file
''')}

{block('Container', 'hero', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Content Width', 'Full Width'),
  ('Layout', 'Direction', 'Column'),
  ('Layout', 'Justify Content', 'Center'),
  ('Layout', 'Align Items', 'Center'),
  ('Layout', 'Min Height', '100 <b>VH</b>'),
  ('Style', 'Background Type', 'Classic'),
  ('Style', 'Background Image', '<code>hero-lobby.jpg</code>'),
  ('Style', 'Background Position', 'Center Center'),
  ('Style', 'Background Repeat', 'No-repeat'),
  ('Style', 'Background Size', 'Cover'),
  ('Style', 'Background Overlay &rsaquo; Type', '<b>Gradient</b>'),
  ('Style', 'Overlay &rsaquo; Color', '<code>rgba(16,28,42,.93)</code> at <b>0%</b>'),
  ('Style', 'Overlay &rsaquo; Second Color', '<code>rgba(16,28,42,.45)</code> at <b>70%</b>'),
  ('Style', 'Overlay &rsaquo; Gradient Type', 'Linear'),
  ('Style', 'Overlay &rsaquo; Angle', '<b>102</b>'),
  ('Advanced', 'Padding', pad(0,0,0,0)),
  ('Advanced', 'Margin', pad(0,0,0,0)),
  ('Advanced', 'CSS ID', '<code>home</code>'),
], note='Set <b>Min Height 100 VH</b> in the panel first, then paste the CSS below. The first rule upgrades it to <code>dvh</code>, which tracks the real viewport on phones &mdash; with plain <code>vh</code> you get a gap where the address bar used to be. The second rule adds the soft darkening along the bottom edge.',
after=css('''
selector{min-height:100dvh}
selector::after{
  content:"";position:absolute;inset:0;pointer-events:none;
  background:linear-gradient(0deg, rgba(16,28,42,.55) 0%, rgba(16,28,42,0) 26%);
}
'''))}

{block('Container', 'hero-inner', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Content Width', 'Boxed'),
  ('Layout', 'Width', '1250'),
  ('Layout', 'Direction', 'Column'),
  ('Layout', 'Align Items', '<b>Start</b>'),
  ('Layout', 'Gap', '0'),
  ('Advanced', 'Padding', dev(pad(124,30,64,30), pad(112,30,56,30), pad(104,20,44,20))),
  ('Advanced', 'Z-Index', '2'),
], note='Z-Index 2 lifts the text above the bottom-fade layer that the CSS added to the hero.')}

{block('Container', 'hero-badges', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Direction', 'Row'),
  ('Layout', 'Align Items', 'Center'),
  ('Layout', 'Wrap', '<b>Wrap</b>'),
  ('Layout', 'Gap', '8'),
  ('Layout', 'Width', 'leave empty'),
  ('Advanced', 'Padding', pad(0,0,0,0)),
  ('Advanced', 'Margin', pad(0,0,26,0)),
])}

{block('Heading', 'badge-trusted', [
  ('Content', 'Title', 'Trusted'),
  ('Content', 'HTML Tag', 'p'),
  ('Style', 'Alignment', 'Center'),
  ('Style', 'Text Color', '<code>#1F2833</code>'),
  ('Style', 'Typography &rsaquo; Family', 'Inter'),
  ('Style', 'Typography &rsaquo; Size', '13.5 PX'),
  ('Style', 'Typography &rsaquo; Weight', '400'),
  ('Style', 'Typography &rsaquo; Line Height', '1.3 EM'),
  ('Advanced', 'Background &rsaquo; Color', '<code>#FFFFFF</code>'),
  ('Advanced', 'Border Radius', '100 PX'),
  ('Advanced', 'Padding', pad(6,13,6,13)),
  ('Advanced', 'Margin', pad(0,0,0,0)),
], note='For a Heading widget, Background and Border Radius are on the <b>Advanced</b> tab, not Style.')}

{block('Heading', 'badge-place', [
  ('Content', 'Title', 'KIPMall Kota Warisan &middot; Sepang'),
  ('Content', 'HTML Tag', 'p'),
  ('Style', 'Alignment', 'Center'),
  ('Style', 'Text Color', '<code>rgba(255,255,255,.92)</code>'),
  ('Style', 'Typography &rsaquo; Family', 'Inter'),
  ('Style', 'Typography &rsaquo; Size', '13.5 PX'),
  ('Style', 'Typography &rsaquo; Weight', '400'),
  ('Style', 'Typography &rsaquo; Line Height', '1.3 EM'),
  ('Advanced', 'Background &rsaquo; Color', '<code>rgba(255,255,255,.14)</code>'),
  ('Advanced', 'Border Type / Width / Color', 'Solid &middot; 1 &middot; <code>rgba(255,255,255,.2)</code>'),
  ('Advanced', 'Border Radius', '100 PX'),
  ('Advanced', 'Padding', pad(6,13,6,13)),
  ('Advanced', 'Margin', pad(0,0,0,0)),
], note='The &middot; between the words is a typed middle dot &mdash; copy it from this line.')}

{block('Heading', 'hero-h1', [
  ('Content', 'Title', 'Dental Pain? Get Expert&lt;br&gt;Care in Kota Warisan'),
  ('Content', 'HTML Tag', '<b>h1</b>'),
  ('Style', 'Alignment', 'Left'),
  ('Style', 'Text Color', '<code>#FFFFFF</code>'),
  ('Style', 'Typography &rsaquo; Family', 'Inter'),
  ('Style', 'Typography &rsaquo; Size', dev('56', '46', '33', ' PX')),
  ('Style', 'Typography &rsaquo; Weight', '600'),
  ('Style', 'Typography &rsaquo; Line Height', '1.2 EM'),
  ('Style', 'Typography &rsaquo; Letter Spacing', dev('&minus;2.5', '&minus;2.1', '&minus;1.5', ' PX')),
  ('Advanced', 'Width', dev('Custom &rarr; 740 PX', 'Custom &rarr; 740 PX', '100 %')),
  ('Advanced', 'Margin', pad(0,0,0,0)),
], note='Type the <code>&lt;br&gt;</code> straight into the Title field. This is the only h1 on the page &mdash; no other heading may use that tag.')}

{block('Heading', 'hero-sub', [
  ('Content', 'Title', 'Experiencing dental pain? Our Kota Warisan dental clinic provides gentle care to help restore your smile.'),
  ('Content', 'HTML Tag', 'p'),
  ('Style', 'Alignment', 'Left'),
  ('Style', 'Text Color', '<code>rgba(255,255,255,.82)</code>'),
  ('Style', 'Typography &rsaquo; Family', 'Inter'),
  ('Style', 'Typography &rsaquo; Size', '17 PX'),
  ('Style', 'Typography &rsaquo; Weight', '400'),
  ('Style', 'Typography &rsaquo; Line Height', '1.4 EM'),
  ('Advanced', 'Width', dev('Custom &rarr; 480 PX', 'Custom &rarr; 480 PX', '100 %')),
  ('Advanced', 'Margin', pad(22,0,0,0)),
])}

{block('Container', 'hero-actions', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Direction', dev('Row', 'Row', '<b>Column</b>')),
  ('Layout', 'Align Items', dev('Center', 'Center', '<b>Stretch</b>')),
  ('Layout', 'Wrap', 'Wrap'),
  ('Layout', 'Gap', '12'),
  ('Layout', 'Width', dev('leave empty', 'leave empty', '<b>100 %</b>')),
  ('Advanced', 'Padding', pad(0,0,0,0)),
  ('Advanced', 'Margin', pad(34,0,0,0)),
], note='Switch to Mobile view for the bold values &mdash; that is what makes the two buttons stack full width on a phone.')}

{block('Button', 'btn-book', [
  ('Content', 'Text', 'Book An Appointment'),
  ('Content', 'Link', f'<code>{WA}</code>'),
  ('Content', 'Link &rsaquo; Open in new window', 'On'),
  ('Content', 'Icon', 'Arrow Right &nbsp;(<code>fas fa-arrow-right</code>) &middot; After &middot; spacing 9'),
  ('Style', 'Button &rsaquo; Position', dev('Left', 'Left', '<b>Stretch</b>')),
  ('Style', 'Typography &rsaquo; Family', 'Inter'),
  ('Style', 'Typography &rsaquo; Size', '15 PX'),
  ('Style', 'Typography &rsaquo; Weight', '500'),
  ('Style', 'Text Color (Normal)', '<code>#1F2833</code>'),
  ('Style', 'Background (Normal)', '<code>#FFFFFF</code>'),
  ('Style', 'Text Color (Hover)', '<code>#1F2833</code>'),
  ('Style', 'Background (Hover)', '<code>#E8D397</code>'),
  ('Style', 'Border Radius', '8 PX'),
  ('Style', 'Padding', pad(12,22,12,22)),
])}

{block('Button', 'btn-services', [
  ('Content', 'Text', 'Our Services'),
  ('Content', 'Link', '<code>#services</code>'),
  ('Content', 'Icon', 'Arrow Right &middot; After &middot; spacing 9'),
  ('Style', 'Button &rsaquo; Position', dev('Left', 'Left', '<b>Stretch</b>')),
  ('Style', 'Typography', 'Inter &middot; 15 PX &middot; weight 500'),
  ('Style', 'Text Color (Normal)', '<code>#FFFFFF</code>'),
  ('Style', 'Background (Normal)', '<b>Transparent</b> &mdash; clear the colour swatch'),
  ('Style', 'Border Type / Width / Color', 'Solid &middot; 1 &middot; <code>rgba(255,255,255,.55)</code>'),
  ('Style', 'Border Color (Hover)', '<code>#FFFFFF</code>'),
  ('Style', 'Background (Hover)', '<code>rgba(255,255,255,.08)</code>'),
  ('Style', 'Border Radius', '8 PX'),
  ('Style', 'Padding', pad(12,22,12,22)),
])}

<h3 class="sub">The rating row</h3>
{block('HTML', 'hero-proof', [
  ('Content', 'HTML Code', 'paste the whole of <b>Step 03 - Hero proof.html</b>'),
  ('Advanced', 'Padding', pad(0,0,0,0)),
  ('Advanced', 'Margin', pad(0,0,0,0)),
], note='Add this as the last child of <b>hero-inner</b>. It is the four overlapping initial circles plus five stars and "Rated 5.0 on Google Reviews". It is a paste because overlapping circles need a negative margin on each one, which is slow and fragile to build by hand. The file carries its own styling and its own mobile spacing.')}
<div class="donebox"><b>Done when:</b> the hero fills exactly one screen on your laptop and in
a phone preview, with no scrollbar inside it and no gap underneath.</div>
""", PASTE))

# ------------------------------------------------------------------ 4 panels
pages.append(step(4, 'Our Panels', f"""
{shot('03-panels.jpg', 'Grey tray, one white card per insurer.')}
{tree('''
Container   panels             Boxed 1250 - column - align center   (CSS ID: panels)
 |- Container  sec-head         column - align center - width 640
 |   |- Heading  eyebrow
 |   |- Heading  h2
 |   |- Heading  sub
 |- Container  panel-tray       row - bg #E9E6DD - radius 16 - pad 10
 |   |- Container panel-item x5   bg #FFF - radius 12 - centred
 |        |- Image  panel-logo
 |- Container  panel-note       row - align center - gap 14 - width 640
      |- Icon         shield
      |- Text Editor  note
''')}
{shell('panels', 'panels')}
{sechead('Our Panels', "Chances Are, You're&lt;br&gt;Already Covered",
         'We are a panel clinic for the major insurers and benefit providers below, and claims are handled at the front desk.')}

{block('Container', 'panel-tray', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Direction', 'Row'),
  ('Layout', 'Align Items', 'Stretch'),
  ('Layout', 'Wrap', dev('No wrap', '<b>Wrap</b>', '<b>Wrap</b>')),
  ('Layout', 'Gap', '10'),
  ('Layout', 'Width', '100 %'),
  ('Style', 'Background Type', 'Classic'),
  ('Style', 'Background Color', '<code>#E9E6DD</code>'),
  ('Advanced', 'Border Radius', '16 PX'),
  ('Advanced', 'Padding', pad(10,10,10,10)),
  ('Advanced', 'Margin', pad(0,0,0,0)),
])}

{block('Container', 'panel-item', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Direction', 'Column'),
  ('Layout', 'Justify Content', 'Center'),
  ('Layout', 'Align Items', 'Center'),
  ('Layout', 'Min Height', dev('132', '118', '104', ' PX')),
  ('Layout', 'Width', dev('20', '33.33', '50', ' %')),
  ('Layout', 'Gap', '0'),
  ('Style', 'Background Color', '<code>#FFFFFF</code>'),
  ('Advanced', 'Border Radius', '12 PX'),
  ('Advanced', 'Padding', dev(pad(26,22,26,22), pad(26,22,26,22), pad(20,16,20,16))),
])}

{block('Image', 'panel-logo', [
  ('Content', 'Choose Image', 'one of the five in <code>panels/</code>'),
  ('Content', 'Image Resolution', '<b>Full</b>'),
  ('Content', 'Link', 'None'),
  ('Style', 'Width', dev('132', '112', '100', ' PX')),
  ('Style', 'Max Width', '100 %'),
  ('Style', 'Height', dev('58', '50', '44', ' PX')),
  ('Style', 'Object Fit', '<b>Contain</b>'),
  ('Advanced', 'Margin', pad(0,0,0,0)),
], note='<b>Object Fit: Contain</b> is what lets five logos of totally different shapes sit on one optical line. AIA is nearly square and three others are wide; without Contain the wide ones tower over AIA.')}

<p>Build one <b>panel-item</b> with its image, then right-click &rarr; Duplicate four times
and swap the logo. Left to right:</p>
<table class="overview"><thead><tr><th>#</th><th>File</th><th>Image Alt text</th></tr></thead><tbody>
<tr><td>1</td><td><code>panels/pmcare.png</code></td><td>PMCare</td></tr>
<tr><td>2</td><td><code>panels/mednefits.png</code></td><td>Mednefits</td></tr>
<tr><td>3</td><td><code>panels/aia.png</code></td><td>AIA</td></tr>
<tr><td>4</td><td><code>panels/healthmetrics.png</code></td><td>HealthMetrics</td></tr>
<tr><td>5</td><td><code>panels/medkad.png</code></td><td>MedKad</td></tr>
</tbody></table>
<p class="note">On <b>Mobile view only</b>, select the fifth panel-item and set Layout &rsaquo;
Width to <b>100 %</b>, so it centres on its own row instead of sitting alone at half width.</p>

{block('Container', 'panel-note', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Direction', dev('Row', 'Row', '<b>Column</b>')),
  ('Layout', 'Align Items', 'Center'),
  ('Layout', 'Gap', dev('14', '14', '10')),
  ('Layout', 'Width', 'Custom &rarr; <b>640</b> PX'),
  ('Advanced', 'Padding', pad(0,0,0,0)),
  ('Advanced', 'Margin', pad(22,0,0,0)),
])}

{icontile('shield', 'Shield Alt', 'fas fa-shield-alt')}

{block('Text Editor', 'note', [
  ('Content', 'Text', 'Not sure if your plan is on the list? <b>WhatsApp us your card</b> and we&rsquo;ll confirm before your visit.'),
  ('Content', 'Link on the bold words', f'<code>{WAPANEL}</code>'),
  ('Style', 'Alignment', dev('Left', 'Left', 'Center')),
  ('Style', 'Text Color', '<code>#5A6270</code>'),
  ('Style', 'Typography &rsaquo; Family', 'Inter'),
  ('Style', 'Typography &rsaquo; Size', dev('15', '14.5', '14.5', ' PX')),
  ('Style', 'Typography &rsaquo; Line Height', '1.5 EM'),
  ('Advanced', 'Margin', pad(0,0,0,0)),
], note='Use a <b>Text Editor</b> widget here, not a Heading &mdash; only Text Editor lets you link a few words inside a sentence. Select "WhatsApp us your card", click the link button, paste the URL, tick open in new tab, then colour just those words <code>#8F702A</code> with the editor&rsquo;s text-colour button.')}
""", BUILD))

# ------------------------------------------------------------------ 5 why
pages.append(step(5, 'Why Lumiere', f"""
{shot('04-about.jpg', 'Four benefit cards across the full tray.')}
{tree('''
Container   about              Boxed 1250 - column - align center   (CSS ID: about)
 |- Container  sec-head         column - align center - width 640
 |   |- Heading  eyebrow / h2 / sub
 |- Container  vision-tray      row - bg #E9E6DD - radius 16 - pad 10
 |   |- Container vision-card x4  bg #FFF - radius 12 - column
 |        |- Icon     icon-tile
 |        |- Heading  card-title
 |        |- Heading  card-text
 |- (Step 6 adds doc-block here)
 |- (Step 7 adds stats-tray here)
''')}
{shell('about', 'about')}
{sechead('Why Lumiere', 'A Different Kind of&lt;br&gt;Dental Visit',
         'One resident dentist, a calm modern space, and care that puts comfort before everything else.')}

{block('Container', 'vision-tray', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Direction', 'Row'),
  ('Layout', 'Align Items', '<b>Stretch</b>'),
  ('Layout', 'Wrap', dev('No wrap', '<b>Wrap</b>', '<b>Wrap</b>')),
  ('Layout', 'Gap', '10'),
  ('Layout', 'Width', '100 %'),
  ('Style', 'Background Color', '<code>#E9E6DD</code>'),
  ('Advanced', 'Border Radius', '16 PX'),
  ('Advanced', 'Padding', pad(10,10,10,10)),
  ('Advanced', 'Margin', pad(0,0,0,0)),
], note='Align Items: Stretch makes all four cards match the tallest one, so their bottoms line up even though the text lengths differ.')}

{block('Container', 'vision-card', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Direction', 'Column'),
  ('Layout', 'Justify Content', 'Start'),
  ('Layout', 'Align Items', 'Start'),
  ('Layout', 'Width', dev('25', '50', '100', ' %')),
  ('Layout', 'Gap', '0'),
  ('Style', 'Background Color', '<code>#FFFFFF</code>'),
  ('Advanced', 'Border Radius', '12 PX'),
  ('Advanced', 'Padding', pad(28,26,30,26)),
])}

{icontile('icon-tile', 'see the table below', 'one per card')}

{block('Heading', 'card-title', [
  ('Content', 'Title', 'see the table below'),
  ('Content', 'HTML Tag', '<b>h3</b>'),
  ('Style', 'Alignment', 'Left'),
  ('Style', 'Text Color', '<code>#1F2833</code>'),
  ('Style', 'Typography &rsaquo; Family', 'Inter'),
  ('Style', 'Typography &rsaquo; Size', '19.5 PX'),
  ('Style', 'Typography &rsaquo; Weight', '600'),
  ('Style', 'Typography &rsaquo; Line Height', '1.3 EM'),
  ('Advanced', 'Margin', pad(30,0,0,0)),
], note='That 30px top margin pushes the title away from the icon tile. Do not use the container Gap for it &mdash; a gap would also space the paragraph.')}

{para('card-text', 'see the table below', size='15', lh='1.4', mt=10, mb=0)}

<p>Build card one completely, then right-click <b>vision-card</b> &rarr; Duplicate three times
and fill in the rest:</p>
<table class="overview"><thead><tr><th>#</th><th>Icon (search this in the picker)</th><th>Title</th><th>Text</th></tr></thead><tbody>
<tr><td>1</td><td><b>Tooth</b><br><code>fas fa-tooth</code></td><td>Painless-first dentistry</td><td>Gentle techniques from airflow scaling to careful extractions, so treatment stays calm from start to finish.</td></tr>
<tr><td>2</td><td><b>User</b><br><code>fas fa-user</code></td><td>Led by Dr Tan Mei-Wen</td><td>DDS from MAHSA University with Distinction, plus a postgraduate diploma in clinical orthodontics.</td></tr>
<tr><td>3</td><td><b>Heart</b><br><code>fas fa-heart</code></td><td>Family-friendly clinic</td><td>A dedicated kids corner and unhurried appointments make first visits easy for the little ones.</td></tr>
<tr><td>4</td><td><b>Shield Alt</b><br><code>fas fa-shield-alt</code></td><td>Insurance panel clinic</td><td>A panel clinic for major insurers including AIA, PMCare and Mednefits, with claims handled at the front desk.</td></tr>
</tbody></table>
""", BUILD))

# ------------------------------------------------------------------ 6 dr tan
pages.append(step(6, 'Dr Tan biography', f"""
{shot('05-drtan.jpg', 'The photo is shorter than the bio, so it travels down with you as you read.')}
{tree('''
Container   doc-block          row - align START - bg #FFF - radius 16 - pad 10
 |- Container  doc-photo        width 45% - radius 12 - overflow hidden - STICKY
 |   |- Image     team-neon
 |- Container  doc-body         width 55% - column
     |- Heading    eyebrow
     |- Container  doc-id       row - align center - gap 15
     |    |- Image      dr-tan
     |    |- Container  doc-id-text   column
     |         |- Heading  doc-name
     |         |- Heading  doc-role
     |- Heading    bio-1
     |- Heading    bio-2
     |- Heading    bio-3
     |- Heading    bio-fun
''')}
<p>This whole block is a new child of the <b>about</b> container from Step 5, sitting directly
under <b>vision-tray</b>.</p>

{block('Container', 'doc-block', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Direction', dev('Row', '<b>Column</b>', '<b>Column</b>')),
  ('Layout', 'Align Items', '<b>Start</b>'),
  ('Layout', 'Gap', '10'),
  ('Layout', 'Width', '100 %'),
  ('Style', 'Background Color', '<code>#FFFFFF</code>'),
  ('Style', 'Box Shadow', 'Horizontal 0 &nbsp; Vertical 10 &nbsp; Blur 30 &nbsp; Spread &minus;18 &nbsp; <code>rgba(31,40,51,.25)</code>'),
  ('Advanced', 'Border Radius', '16 PX'),
  ('Advanced', 'Padding', pad(10,10,10,10)),
  ('Advanced', 'Margin', pad(16,0,0,0)),
  ('Advanced', 'Overflow', 'Default'),
], note='<b>Align Items must be Start, not Stretch.</b> On Stretch the photo is pulled to the full height of the bio column, and then the aspect-ratio rule below works out a width from that tall height &mdash; the photo balloons sideways and overlaps the text. This exact bug cost an afternoon when the mockup was built.')}

{block('Container', 'doc-photo', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Width', dev('45', '100', '100', ' %')),
  ('Layout', 'Min Height', 'leave empty'),
  ('Advanced', 'Border Radius', '12 PX'),
  ('Advanced', 'Overflow', '<b>Hidden</b>'),
  ('Advanced', 'Padding', pad(0,0,0,0)),
], note='Hidden is correct here &mdash; it clips the photo to the rounded corners. Its parents stay on Default.',
after=css('''
selector{aspect-ratio:4/3; position:sticky; top:112px}

@media(max-width:1080px){
  selector{aspect-ratio:16/9; position:static}
}
'''))}

{block('Image', 'team-neon', [
  ('Content', 'Choose Image', '<code>team-neon.jpg</code>'),
  ('Content', 'Image Resolution', '<b>Full</b>'),
  ('Content', 'Link', 'None'),
  ('Style', 'Width', '100 %'),
  ('Style', 'Height', '100 %'),
  ('Style', 'Object Fit', '<b>Cover</b>'),
  ('Advanced', 'Margin', pad(0,0,0,0)),
])}

{block('Container', 'doc-body', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Direction', 'Column'),
  ('Layout', 'Align Items', 'Start'),
  ('Layout', 'Width', dev('55', '100', '100', ' %')),
  ('Layout', 'Gap', '0'),
  ('Advanced', 'Padding', dev(pad(30,34,30,26), pad(26,28,30,28), pad(22,20,26,20))),
])}

{block('Heading', 'eyebrow', [
  ('Content', 'Title', '&#9670; Meet Your Dentist'),
  ('Content', 'HTML Tag', 'p'),
  ('Style', 'Alignment', 'Left'),
  ('Style', 'Text Color', '<code>#8F702A</code>'),
  ('Style', 'Typography &rsaquo; Family', 'Inter'),
  ('Style', 'Typography &rsaquo; Size', '15 PX'),
  ('Style', 'Typography &rsaquo; Weight', '500'),
  ('Advanced', 'Margin', pad(0,0,4,0)),
])}

{block('Container', 'doc-id', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Direction', 'Row'),
  ('Layout', 'Align Items', 'Center'),
  ('Layout', 'Gap', '15'),
  ('Layout', 'Width', '100 %'),
  ('Advanced', 'Padding', pad(0,0,0,0)),
  ('Advanced', 'Margin', pad(0,0,20,0)),
])}

{block('Image', 'dr-tan', [
  ('Content', 'Choose Image', '<code>dr-tan.jpg</code>'),
  ('Content', 'Image Resolution', '<b>Full</b>'),
  ('Content', 'Link', 'None'),
  ('Style', 'Width', dev('68', '68', '58', ' PX')),
  ('Style', 'Height', dev('68', '68', '58', ' PX')),
  ('Style', 'Object Fit', '<b>Cover</b>'),
  ('Style', 'Border Type / Width / Color', 'Solid &middot; 2 &middot; <code>#E8D397</code>'),
  ('Style', 'Border Radius', '50 %'),
  ('Advanced', 'Margin', pad(0,0,0,0)),
], note='This is the only low-resolution file in the pack &mdash; 180&times;180 is all the group website has. At 68px it is sharp. <b>Do not scale it up</b>; ask the clinic for a bigger portrait if they want it featured larger.')}

{block('Container', 'doc-id-text', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Direction', 'Column'),
  ('Layout', 'Align Items', 'Start'),
  ('Layout', 'Gap', '0'),
  ('Layout', 'Width', 'leave empty'),
  ('Advanced', 'Padding', pad(0,0,0,0)),
])}

{block('Heading', 'doc-name', [
  ('Content', 'Title', 'Dr Tan Mei-Wen'),
  ('Content', 'HTML Tag', '<b>h3</b>'),
  ('Style', 'Alignment', 'Left'),
  ('Style', 'Text Color', '<code>#1F2833</code>'),
  ('Style', 'Typography &rsaquo; Family', 'Inter'),
  ('Style', 'Typography &rsaquo; Size', dev('23', '23', '20', ' PX')),
  ('Style', 'Typography &rsaquo; Weight', '600'),
  ('Style', 'Typography &rsaquo; Line Height', '1.3 EM'),
  ('Style', 'Typography &rsaquo; Letter Spacing', '&minus;0.3 PX'),
  ('Advanced', 'Margin', pad(0,0,0,0)),
])}

{para('doc-role', 'Resident Dentist &middot; Lumiere Dental Kota Warisan', size='14.5', lh='1.4', mt=3, mb=0)}

<h3 class="sub">The four bio paragraphs</h3>
<p>Four separate <b>Heading</b> widgets, all HTML Tag <b>p</b>. The first three are identical;
the fourth changes colour only.</p>
{block('Heading', 'bio-1, bio-2, bio-3', [
  ('Content', 'Title', 'see the table below'),
  ('Content', 'HTML Tag', 'p'),
  ('Style', 'Alignment', 'Left'),
  ('Style', 'Text Color', '<code>#5A6270</code>'),
  ('Style', 'Typography &rsaquo; Family', 'Inter'),
  ('Style', 'Typography &rsaquo; Size', '15 PX'),
  ('Style', 'Typography &rsaquo; Weight', '400'),
  ('Style', 'Typography &rsaquo; Line Height', '1.6 EM'),
  ('Advanced', 'Width', dev('Custom &rarr; 620 PX', '100 %', '100 %')),
  ('Advanced', 'Margin', pad(0,0,12,0)),
])}
{block('Heading', 'bio-fun', [
  ('Content', 'Title', 'see the table below'),
  ('Content', 'HTML Tag', 'p'),
  ('Style', 'Text Color', '<b><code>#8F702A</code></b> &mdash; the only difference'),
  ('Style', 'Typography', 'Inter &middot; 15 PX &middot; weight 400 &middot; line 1.6 EM'),
  ('Advanced', 'Width', dev('Custom &rarr; 620 PX', '100 %', '100 %')),
  ('Advanced', 'Margin', pad(0,0,0,0)),
])}

<table class="bio"><tbody>
<tr><td class="k">bio-1</td><td>Dr Tan graduated with a Doctor of Dental Surgery from MAHSA University in 2016, with Distinction in Conservative Dentistry. She began her career in the government sector at Klinik Pergigian Taman Medan, and chose to extend her time in public service before moving into private practice. She also holds a Postgraduate Diploma in Clinical Orthodontics.</td></tr>
<tr><td class="k">bio-2</td><td>With a strong interest in preserving natural teeth, Dr Tan believes dentistry goes beyond simply treating teeth. She takes a holistic and individualised approach, taking time to understand each patient's concerns, expectations and overall wellbeing when planning treatment.</td></tr>
<tr><td class="k">bio-3</td><td>Her approach centres on clear communication, thoughtful treatment planning and a high standard of care, because building trust and helping patients understand their treatment is what achieves good long-term oral health.</td></tr>
<tr><td class="k">bio-fun</td><td>Outside of dentistry she is a home barista with a love for a good cuppa. A fun fact: she is a left-handed dentist working with a right-handed dental chair, something she has happily adapted to throughout her career.</td></tr>
</tbody></table>
<p class="note">This is the clinic's own supplied biography. Copy it exactly &mdash; do not
shorten it, reword it, or tidy the phrasing.</p>
""", BUILD))

# ------------------------------------------------------------------ 7 stats
pages.append(step(7, 'Stats counters', f"""
{shot('06-stats.jpg', 'Four numbers that count up when they scroll into view.')}
{tree('''
Container   stats-tray         row - bg #E9E6DD - radius 16 - pad 10
 |- Container  stat-card x4     bg #FFF - radius 12 - column
      |- Icon     icon-tile
      |- Counter  counter
''')}
<p>Also a child of the <b>about</b> container, directly below the Dr Tan block.</p>

{block('Container', 'stats-tray', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Direction', 'Row'),
  ('Layout', 'Align Items', 'Stretch'),
  ('Layout', 'Wrap', dev('No wrap', '<b>Wrap</b>', '<b>Wrap</b>')),
  ('Layout', 'Gap', '10'),
  ('Layout', 'Width', '100 %'),
  ('Style', 'Background Color', '<code>#E9E6DD</code>'),
  ('Advanced', 'Border Radius', '16 PX'),
  ('Advanced', 'Padding', pad(10,10,10,10)),
  ('Advanced', 'Margin', pad(16,0,0,0)),
])}

{block('Container', 'stat-card', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Direction', 'Column'),
  ('Layout', 'Justify Content', 'Start'),
  ('Layout', 'Align Items', 'Start'),
  ('Layout', 'Width', dev('25', '50', '100', ' %')),
  ('Layout', 'Gap', '0'),
  ('Style', 'Background Color', '<code>#FFFFFF</code>'),
  ('Advanced', 'Border Radius', '12 PX'),
  ('Advanced', 'Padding', pad(26,26,22,26)),
])}

{icontile('icon-tile', 'see the table below', 'one per card')}

{block('Counter', 'counter', [
  ('Content', 'Starting Number', '0'),
  ('Content', 'Ending Number', 'see the table below'),
  ('Content', 'Number Prefix', 'leave empty'),
  ('Content', 'Number Suffix', 'see the table below'),
  ('Content', 'Animation Duration', '1800'),
  ('Content', 'Thousand Separator', 'Off'),
  ('Content', 'Title', 'see the table below'),
  ('Style', 'Counter &rsaquo; Alignment', '<b>Left</b>'),
  ('Style', 'Counter &rsaquo; Title Position', '<b>Bottom</b>'),
  ('Style', 'Number &rsaquo; Text Color', '<code>#1F2833</code>'),
  ('Style', 'Number &rsaquo; Typography &rsaquo; Family', 'Inter'),
  ('Style', 'Number &rsaquo; Typography &rsaquo; Size', '34 PX'),
  ('Style', 'Number &rsaquo; Typography &rsaquo; Weight', '500'),
  ('Style', 'Title &rsaquo; Text Color', '<code>#5A6270</code>'),
  ('Style', 'Title &rsaquo; Typography &rsaquo; Family', 'Inter'),
  ('Style', 'Title &rsaquo; Typography &rsaquo; Size', '14.5 PX'),
  ('Style', 'Title &rsaquo; Typography &rsaquo; Weight', '400'),
  ('Advanced', 'Margin', pad(26,0,0,0)),
], note='Alignment, Title Position and Number Position are all under <b>Style &rsaquo; Counter</b> in Elementor 4.x.')}

<table class="overview"><thead><tr><th>#</th><th>Icon</th><th>Ending</th><th>Suffix</th><th>Title</th></tr></thead><tbody>
<tr><td>1</td><td><b>Clock</b><br><code>far fa-clock</code></td><td>9</td><td><code>+</code></td><td>Years of Clinical Practice</td></tr>
<tr><td>2</td><td><b>Clinic Medical</b><br><code>fas fa-clinic-medical</code></td><td>8</td><td>leave empty</td><td>Lumiere Branches in Malaysia</td></tr>
<tr><td>3</td><td><b>Tooth</b><br><code>fas fa-tooth</code></td><td>8</td><td>leave empty</td><td>Treatments Offered</td></tr>
<tr><td>4</td><td><b>Star</b><br><code>fas fa-star</code></td><td>5</td><td><code>.0</code></td><td>Google Review Rating</td></tr>
</tbody></table>
<p class="note"><b>Why 5 with a ".0" suffix.</b> Elementor's Counter only counts whole
numbers. Ending Number 5 plus suffix <code>.0</code> animates 0.0 up to 5.0 and reads exactly
like the design. Typing 5.0 into Ending Number just rounds it.</p>
<p class="note"><b>Two of these four are unconfirmed.</b> "9+ years" is worked out from
Dr Tan's 2016 graduation, and "5.0" comes from the review screenshots. Get the clinic to
confirm both before this page goes live.</p>
""", BUILD))

# ------------------------------------------------------------------ 8 services
pages.append(step(8, 'Services &mdash; the sticky stack', f"""
{shot('07-services.jpg', 'Eight cards that pin at the top and let the next slide over them. This is the signature effect of the page.')}
{tree('''
Container   services           Boxed 1250 - column - align center   (CSS ID: services)
 |- Container  sec-head         column - align center - width 640
 |- Container  svc-stack        column - gap 0 - overflow DEFAULT
     |- Container svc-card x8   bg #FFF - radius 24 - row - STICKY
          |- Container  svc-media   width 50% - radius 12 - overflow hidden
          |    |- Image      svc-photo
          |- Container  svc-body    width 50% - column
               |- Container  pill   row - gold wash - radius 100
               |    |- Image    pill-icon
               |    |- Heading  pill-label
               |- Heading    svc-h2
               |- Heading    svc-p
               |- Icon List  checklist
               |- Button     svc-cta
''')}
<p class="note"><b>Read this first.</b> The stacking is plain CSS
<code>position: sticky</code>. <b>Do not</b> use Motion Effects &rsaquo; Sticky here &mdash;
that is a different, JavaScript-driven feature and it will not stack. Sticky also stops
working if any ancestor has Overflow set to Hidden, so <b>services</b> and <b>svc-stack</b>
must both stay on Default.</p>

{shell('services', 'services')}
{sechead('Our Services', 'Complete Dental Care&lt;br&gt;Under One Roof',
         'From routine checkups to a full smile makeover, handled in-clinic by Dr Tan and her team.')}

{block('Container', 'svc-stack', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Direction', 'Column'),
  ('Layout', 'Align Items', 'Stretch'),
  ('Layout', 'Gap', '<b>0</b>'),
  ('Layout', 'Width', '100 %'),
  ('Advanced', 'Padding', pad(0,0,0,0)),
  ('Advanced', 'Margin', pad(0,0,0,0)),
  ('Advanced', 'Overflow', '<b>Default</b>'),
], note='Gap is 0 on purpose. The space between cards comes from each card&rsquo;s own bottom margin &mdash; a flex gap would push the cards apart as they pin and break the overlap.')}

{block('Container', 'svc-card', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Direction', dev('Row', '<b>Column</b>', '<b>Column</b>')),
  ('Layout', 'Align Items', 'Center'),
  ('Layout', 'Gap', dev('48', '18', '18')),
  ('Layout', 'Width', '100 %'),
  ('Style', 'Background Color', '<code>#FFFFFF</code>'),
  ('Style', 'Box Shadow', 'Horizontal 0 &nbsp; Vertical 10 &nbsp; Blur 30 &nbsp; Spread &minus;18 &nbsp; <code>rgba(31,40,51,.25)</code>'),
  ('Advanced', 'Border Radius', '24 PX'),
  ('Advanced', 'Padding', dev(pad(40,40,40,40), pad(22,22,22,22), pad(22,22,22,22))),
  ('Advanced', 'Margin', dev(pad(0,0,28,0), pad(0,0,24,0), pad(0,0,24,0))),
  ('Advanced', 'Overflow', 'Default'),
], after=css('''
selector{position:sticky; top:100px}

/* phones: only stack when the screen is tall enough for a whole card */
@media(max-width:860px) and (min-height:700px){
  selector{position:sticky; top:80px}
}
@media(max-width:860px) and (max-height:699px){
  selector{position:relative; top:auto}
}
'''))}

{block('Container', 'svc-media', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Width', dev('50', '100', '100', ' %')),
  ('Advanced', 'Border Radius', '12 PX'),
  ('Advanced', 'Overflow', '<b>Hidden</b>'),
  ('Advanced', 'Padding', pad(0,0,0,0)),
], after=css('''
selector{aspect-ratio:4/3}
@media(max-width:860px){ selector{aspect-ratio:16/10} }
'''))}

{block('Image', 'svc-photo', [
  ('Content', 'Choose Image', 'see the content table overleaf'),
  ('Content', 'Image Resolution', '<b>Full</b>'),
  ('Content', 'Link', 'None'),
  ('Style', 'Width', '100 %'),
  ('Style', 'Height', '100 %'),
  ('Style', 'Object Fit', '<b>Cover</b>'),
  ('Advanced', 'Margin', pad(0,0,0,0)),
])}

{block('Container', 'svc-body', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Direction', 'Column'),
  ('Layout', 'Align Items', 'Start'),
  ('Layout', 'Width', dev('50', '100', '100', ' %')),
  ('Layout', 'Gap', '0'),
  ('Advanced', 'Padding', pad(0,0,0,0)),
])}

{block('Container', 'pill', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Direction', 'Row'),
  ('Layout', 'Align Items', 'Center'),
  ('Layout', 'Gap', '9'),
  ('Layout', 'Width', '<b>leave empty</b> so it hugs its content'),
  ('Style', 'Background Color', '<code>rgba(212,178,96,.16)</code>'),
  ('Advanced', 'Border Radius', '100 PX'),
  ('Advanced', 'Padding', dev(pad(8,16,8,10), pad(6,13,6,8), pad(6,13,6,8))),
  ('Advanced', 'Margin', dev(pad(0,0,18,0), pad(0,0,14,0), pad(0,0,14,0))),
], note='If the pill stretches the whole column width, its Layout &rsaquo; Width has a value in it. Clear the field.')}

{block('Image', 'pill-icon', [
  ('Content', 'Choose Image', 'the matching file from <code>icons/</code>'),
  ('Content', 'Image Resolution', '<b>Full</b>'),
  ('Content', 'Link', 'None'),
  ('Style', 'Width', dev('26', '22', '22', ' PX')),
  ('Style', 'Object Fit', 'Contain'),
  ('Advanced', 'Margin', pad(0,0,0,0)),
], note='These are the clinic group&rsquo;s own service icons, so they match Lumiere branding everywhere else. Use the image files, not Font Awesome.')}

{block('Heading', 'pill-label', [
  ('Content', 'Title', 'see the content table'),
  ('Content', 'HTML Tag', 'p'),
  ('Style', 'Alignment', 'Left'),
  ('Style', 'Text Color', '<code>#8F702A</code>'),
  ('Style', 'Typography &rsaquo; Family', 'Inter'),
  ('Style', 'Typography &rsaquo; Size', dev('15', '14', '14', ' PX')),
  ('Style', 'Typography &rsaquo; Weight', '400'),
  ('Advanced', 'Margin', pad(0,0,0,0)),
])}

{block('Heading', 'svc-h2', [
  ('Content', 'Title', 'see the content table'),
  ('Content', 'HTML Tag', '<b>h2</b>'),
  ('Style', 'Alignment', 'Left'),
  ('Style', 'Text Color', '<code>#1F2833</code>'),
  ('Style', 'Typography &rsaquo; Family', 'Inter'),
  ('Style', 'Typography &rsaquo; Size', dev('41', '25', '23', ' PX')),
  ('Style', 'Typography &rsaquo; Weight', '600'),
  ('Style', 'Typography &rsaquo; Line Height', '1.22 EM'),
  ('Style', 'Typography &rsaquo; Letter Spacing', '&minus;0.9 PX'),
  ('Advanced', 'Margin', pad(0,0,0,0)),
])}

{para('svc-p', 'see the content table', size='15.5', lh='1.4', mt=15, mb=0)}

{block('Icon List', 'checklist', [
  ('Content', 'Layout', 'Default (vertical)'),
  ('Content', 'Items', 'five &mdash; from the content table'),
  ('Content', 'Item &rsaquo; Icon (each one)', '<b>Check</b> &nbsp;<code>fas fa-check</code>'),
  ('Content', 'Item &rsaquo; Link', 'leave empty'),
  ('Style', 'List &rsaquo; Space Between', dev('12', '8', '8', ' PX')),
  ('Style', 'List &rsaquo; Alignment', 'Left'),
  ('Style', 'List &rsaquo; Divider', '<b>Off</b>'),
  ('Style', 'Icon &rsaquo; Color', '<code>#8F702A</code>'),
  ('Style', 'Icon &rsaquo; Size', '13 PX'),
  ('Style', 'Icon &rsaquo; Gap', '12 PX'),
  ('Style', 'Text &rsaquo; Text Color', '<code>#1F2833</code>'),
  ('Style', 'Text &rsaquo; Typography &rsaquo; Family', 'Inter'),
  ('Style', 'Text &rsaquo; Typography &rsaquo; Size', dev('15.5', '14.5', '14.5', ' PX')),
  ('Style', 'Text &rsaquo; Typography &rsaquo; Weight', '400'),
  ('Advanced', 'Margin', dev(pad(22,0,0,0), pad(16,0,0,0), pad(16,0,0,0))),
], note='Icon List has no Text Indent control in 4.x. The gap between the tick and the text is <b>Style &rsaquo; Icon &rsaquo; Gap</b>.')}

{block('Button', 'svc-cta', [
  ('Content', 'Text', 'Book This Treatment'),
  ('Content', 'Link', 'one per treatment &mdash; see the content table'),
  ('Content', 'Link &rsaquo; Open in new window', 'On'),
  ('Content', 'Icon', 'Arrow Right &middot; After &middot; spacing 9'),
  ('Style', 'Button &rsaquo; Position', 'Left'),
  ('Style', 'Typography &rsaquo; Family', 'Inter'),
  ('Style', 'Typography &rsaquo; Size', dev('15', '14.5', '14.5', ' PX')),
  ('Style', 'Typography &rsaquo; Weight', '500'),
  ('Style', 'Text Color (Normal)', '<code>#FFFFFF</code>'),
  ('Style', 'Background (Normal)', '<code>#33485C</code>'),
  ('Style', 'Background (Hover)', '<code>#26394B</code>'),
  ('Style', 'Border Radius', '8 PX'),
  ('Style', 'Padding', dev(pad(12,22,12,22), pad(11,18,11,18), pad(11,18,11,18))),
  ('Advanced', 'Margin', dev(pad(26,0,0,0), pad(18,0,0,0), pad(18,0,0,0))),
])}

<h3 class="sub">Then duplicate seven times</h3>
<p>Finish card 1, then right-click <b>svc-card</b> &rarr; Duplicate, seven times. Change only
the content, from the table on the next page.</p>
<p>On cards <b>2, 4, 6 and 8</b> set <b>Layout &rsaquo; Direction</b> to <b>Row Reversed</b>
&mdash; <b>Desktop view only</b> &mdash; so the photo alternates sides. Leave Tablet and
Mobile on <b>Column</b>. Row Reversed on a phone would put the photo below the text on half
the cards.</p>
""", BUILD))

rows = [
  ('general.png', 'svc-scaling.jpg', 'General Dentistry', 'Everyday Care That Keeps Problems Away',
   'Routine checkups, cleaning and fillings that catch small problems before they turn into painful ones.',
   'Checkups and full oral examination / Airflow scaling and polishing / Tooth-coloured fillings / Extractions and minor oral surgery / Clear explanation of your teeth condition',
   'General%20Dentistry'),
  ('whitening.png', 'svc-whitening.jpg', 'Teeth Whitening', 'A Brighter Smile, Safely Done',
   'Professional whitening that lifts years of coffee, tea and teh tarik stains without damaging your enamel.',
   'Shade assessment before we start / In-clinic professional whitening / Take-home whitening kits / Enamel-safe, dentist-supervised / Advice on keeping the result',
   'Teeth%20Whitening'),
  ('implants.png', 'svc-implants.jpg', 'Dental Implants', 'Replace Missing Teeth for Good',
   'An implant restores a missing tooth from the root up, so you can bite and speak normally again.',
   'X-ray assessment and planning / Single and multiple tooth implants / Natural-looking implant crowns / Step-by-step timeline explained upfront / Follow-up care after placement',
   'Dental%20Implants'),
  ('invisalign.png', 'svc-invisalign.jpg', 'Invisalign / Clear Correct', 'Straighten Your Teeth Without Braces',
   'Clear removable aligners that move your teeth quietly, so most people never notice you are in treatment.',
   'Digital assessment and treatment plan / Nearly invisible custom aligners / Removable for meals and brushing / Fewer clinic visits than fixed braces / Retainers to hold the final result',
   'Invisalign%20or%20Clear%20Correct'),
  ('braces.png', 'svc-braces.jpg', 'Braces', 'Classic Braces, Expertly Fitted',
   'Fixed braces remain the most reliable way to correct crowding and bite problems, planned by a dentist with postgraduate orthodontic training.',
   'Orthodontic assessment and records / Metal and ceramic bracket options / Crowding, spacing and bite correction / Regular adjustment appointments / Retainers once braces come off',
   'Braces'),
  ('rootcanal.png', 'svc-rootcanal.jpg', 'Root Canal Treatment', 'Save the Tooth Instead of Losing It',
   "Dr Tan's focus is preserving natural teeth. Root canal treatment here is methodical, explained clearly, and painless.",
   'Assessment and honest advice first / Treatment focused on saving the tooth / Proper numbing and a patient pace / Every step explained as it happens / Crown options to protect the result',
   'Root%20Canal%20Treatment'),
  ('crowns.png', 'svc-crowns.jpg', 'Crown &amp; Bridges', 'Restore Damaged Teeth to Full Strength',
   'Crowns protect what remains and bridges close the gaps, matched in shade so the repair disappears into your smile.',
   'Crowns for cracked or weakened teeth / Bridges to replace missing teeth / Shade matching to your natural teeth / Precise fitting over multiple visits / Care advice to make them last',
   'Crown%20and%20Bridges'),
  ('makeover.png', 'svc-makeover.jpg', 'Smile Makeover', 'A Complete Plan for the Smile You Want',
   'When more than one thing needs fixing, a makeover combines the right treatments into a single plan with one clear outcome.',
   'Full smile assessment and goals / Combines whitening, veneers and alignment / Treatment sequenced in the right order / Costs and timeline agreed upfront / Reviews at every stage',
   'a%20Smile%20Makeover'),
]
svc_rows = ''.join(
  f'<tr><td class="n">{i+1}</td>'
  f'<td><b>{p}</b><br><code>icons/{ic}</code><br><code>{im}</code>'
  f'{"<br><span class=rev>Row Reversed</span>" if i%2 else ""}</td>'
  f'<td><b>{h}</b><p>{d}</p><span class="li">{li}</span>'
  f'<p class="wa"><code>&hellip;about%20{wa}%20at%20Lumiere%20Kota%20Warisan.</code></p></td></tr>'
  for i,(ic,im,p,h,d,li,wa) in enumerate(rows))
pages.append(f"""
<section class="step newpage"><div class="stephead"><span class="num">Step 8</span>
<h2>Services &mdash; content for all eight cards</h2></div>
<p>Pill label, icon file and photo on the left. Heading, description, the five checklist items
(split on <code>/</code>) and the button link on the right.</p>
<p class="note">Every button URL begins
<code>https://wa.me/601116083188?text=Hi%2C%20I%27d%20like%20to%20ask%20</code> &mdash; the
table shows the tail of each one. <code>%20</code> is a space; never type a real space into
a URL.</p>
<table class="svc"><thead><tr><th>#</th><th>Pill / files</th><th>Copy and link tail</th></tr></thead>
<tbody>{svc_rows}</tbody></table>
</section>
""")

# ------------------------------------------------------------------ 9 facilities
pages.append(step(9, 'Our Clinic', f"""
{shot('08-facilities.jpg', 'Two columns. Each has one landscape and one portrait card, which is why both finish level.')}
{tree('''
Container   facilities         Boxed 1250 - column - align center   (CSS ID: facilities)
 |- Container  sec-head         column - align center - width 640
 |- Container  fac-grid         row - gap 14
     |- Container  fac-col-1    column - gap 14 - width 50%
     |    |- Container  card-lobby     4:3
     |    |    |- Container caption
     |    |         |- Heading  cap-title
     |    |         |- Heading  cap-text
     |    |- Container  card-kids      3:4  (same children)
     |- Container  fac-col-2    column - gap 14 - width 50%
          |- Container  card-reception 4:3  (same children)
          |- Container  card-neon      3:4  (same children)
''')}
{shell('facilities', 'facilities')}
{sechead('Our Clinic', 'A Space Designed to&lt;br&gt;Put You at Ease', '')}

{block('Container', 'fac-grid', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Direction', dev('Row', '<b>Column</b>', '<b>Column</b>')),
  ('Layout', 'Align Items', 'Start'),
  ('Layout', 'Gap', '14'),
  ('Layout', 'Width', '100 %'),
  ('Advanced', 'Padding', pad(0,0,0,0)),
])}

{block('Container', 'fac-col-1 and fac-col-2', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Direction', 'Column'),
  ('Layout', 'Align Items', 'Stretch'),
  ('Layout', 'Gap', '14'),
  ('Layout', 'Width', dev('50', '100', '100', ' %')),
  ('Advanced', 'Padding', pad(0,0,0,0)),
], note='Both columns take identical settings. Build the first, duplicate it, then fill the second with its two cards.')}

{block('Container', 'card-lobby / card-kids / card-reception / card-neon', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Direction', 'Column'),
  ('Layout', 'Justify Content', '<b>End</b>'),
  ('Layout', 'Align Items', 'Stretch'),
  ('Layout', 'Width', '100 %'),
  ('Layout', 'Gap', '0'),
  ('Style', 'Background Type', 'Classic'),
  ('Style', 'Background Image', 'see the table below'),
  ('Style', 'Background Position', 'Center Center'),
  ('Style', 'Background Repeat', 'No-repeat'),
  ('Style', 'Background Size', 'Cover'),
  ('Advanced', 'Border Radius', '16 PX'),
  ('Advanced', 'Overflow', '<b>Hidden</b>'),
  ('Advanced', 'Padding', pad(0,0,0,0)),
], note='Justify Content: End pins the caption to the bottom. The photo is a container <b>background</b>, not an Image widget, so the caption can sit over it.',
after=css('''
/* landscape cards - card-lobby and card-reception */
selector{aspect-ratio:4/3}

/* portrait cards - card-kids and card-neon - use this instead */
selector{aspect-ratio:3/4}
'''))}

{block('Container', 'caption', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Direction', 'Column'),
  ('Layout', 'Align Items', 'Start'),
  ('Layout', 'Width', '100 %'),
  ('Layout', 'Gap', '0'),
  ('Style', 'Background Type', '<b>Gradient</b>'),
  ('Style', 'Color', '<code>rgba(16,28,42,.8)</code> at <b>0%</b>'),
  ('Style', 'Second Color', '<code>rgba(16,28,42,0)</code> at <b>100%</b>'),
  ('Style', 'Gradient Type', 'Linear'),
  ('Style', 'Gradient Angle', '<b>0</b>'),
  ('Advanced', 'Padding', pad(90,28,26,28)),
], note='Angle 0 runs the gradient bottom-to-top, so the dark end sits under the text and the photo is untouched higher up. The 90px top padding gives the fade room to blend.')}

{block('Heading', 'cap-title', [
  ('Content', 'Title', 'see the table below'),
  ('Content', 'HTML Tag', '<b>h3</b>'),
  ('Style', 'Alignment', 'Left'),
  ('Style', 'Text Color', '<code>#FFFFFF</code>'),
  ('Style', 'Typography &rsaquo; Family', 'Inter'),
  ('Style', 'Typography &rsaquo; Size', '22 PX'),
  ('Style', 'Typography &rsaquo; Weight', '600'),
  ('Style', 'Typography &rsaquo; Line Height', '1.3 EM'),
  ('Advanced', 'Margin', pad(0,0,0,0)),
])}

{para('cap-text', 'see the table below', size='15', color='rgba(255,255,255,.85)', lh='1.4', mt=7, mb=0)}

<table class="overview"><thead><tr><th>Col</th><th>Card</th><th>Image</th><th>Ratio CSS</th><th>Title</th><th>Text</th></tr></thead><tbody>
<tr><td>1</td><td>card-lobby</td><td><code>lobby-reverse.jpg</code></td><td><code>4/3</code></td><td>A calm, open lobby</td><td>Double-height ceilings, soft seating and natural light, closer to a lounge than a clinic.</td></tr>
<tr><td>1</td><td>card-kids</td><td><code>kids-corner.jpg</code></td><td><code>3/4</code></td><td>A corner just for kids</td><td>A play tent and soft mats keep young visitors happy while they wait their turn.</td></tr>
<tr><td>2</td><td>card-reception</td><td><code>reception.jpg</code></td><td><code>4/3</code></td><td>Qualified and certified</td><td>Our team's credentials are framed on the wall behind reception, not hidden in a drawer.</td></tr>
<tr><td>2</td><td>card-neon</td><td><code>neon-wall.jpg</code></td><td><code>3/4</code></td><td>The smile wall</td><td>Lighting up your smile is the promise on our wall, and the standard for every visit.</td></tr>
</tbody></table>
<p class="note"><b>Do not change the ratios.</b> One landscape plus one portrait per column is
what makes the two columns end at the same height. If the clinic swaps a photo later, keep the
new one the same shape, or set that card's <code>aspect-ratio</code> to match it.</p>
""", BUILD))

# ------------------------------------------------------------------ 10 how
pages.append(step(10, 'How It Works', f"""
{shot('09-how.jpg', 'The left panel holds still while the four steps scroll past it.')}
{tree('''
Container   how                Boxed 1250 - column   (CSS ID: how)
 |- Container  how-grid         row - gap 70
     |- Container  how-left     width 50%
     |    |- Container how-sticky   column - STICKY
     |         |- Heading  eyebrow
     |         |- Heading  h2
     |         |- Heading  sub
     |- Container  how-steps    column - width 50% - gap 0
          |- Container how-step x4   row - gap 28 - pad-bottom 92
               |- Icon      icon-tile
               |- Container step-text   column
                    |- Heading  step-title
                    |- Heading  step-body
''')}
{shell('how', 'how')}

{block('Container', 'how-grid', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Direction', dev('Row', '<b>Column</b>', '<b>Column</b>')),
  ('Layout', 'Align Items', 'Start'),
  ('Layout', 'Gap', dev('70', '44', '44')),
  ('Layout', 'Width', '100 %'),
  ('Advanced', 'Padding', pad(0,0,0,0)),
])}

{block('Container', 'how-left', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Direction', 'Column'),
  ('Layout', 'Align Items', 'Start'),
  ('Layout', 'Width', dev('50', '100', '100', ' %')),
  ('Layout', 'Gap', '0'),
  ('Advanced', 'Padding', pad(0,0,0,0)),
  ('Advanced', 'Overflow', 'Default'),
], note='This wrapper exists purely to give the sticky child something taller to travel inside. Do not merge it with how-sticky.')}

{block('Container', 'how-sticky', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Direction', 'Column'),
  ('Layout', 'Align Items', 'Start'),
  ('Layout', 'Width', '100 %'),
  ('Layout', 'Gap', '0'),
  ('Advanced', 'Padding', pad(0,0,0,0)),
], after=css('''
selector{position:sticky; top:130px}
@media(max-width:1080px){ selector{position:static} }
'''))}

{sechead('How It Works', 'From WhatsApp to Follow-Up, Made Simple.',
         'Four steps from your first message to a healthy smile, guided the whole way.',
         centered=False)}
<p class="note">This is the one section whose heading block is <b>left-aligned</b> &mdash; the
tables above already carry the correct Alignment values. Put these three widgets inside
<b>how-sticky</b>, not in a sec-head of their own, and set the <b>sub</b> widget's
Advanced &rsaquo; Width to Custom <b>340</b> PX so it wraps the way the design does.</p>

{block('Container', 'how-steps', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Direction', 'Column'),
  ('Layout', 'Align Items', 'Stretch'),
  ('Layout', 'Width', dev('50', '100', '100', ' %')),
  ('Layout', 'Gap', '<b>0</b>'),
  ('Advanced', 'Padding', pad(10,0,10,0)),
], note='Gap 0 again &mdash; the spacing comes from each step&rsquo;s bottom padding, because the hairline is drawn inside that padding.')}

{block('Container', 'how-step', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Direction', 'Row'),
  ('Layout', 'Align Items', 'Start'),
  ('Layout', 'Gap', '28'),
  ('Layout', 'Width', '100 %'),
  ('Advanced', 'Padding', pad(0,0,92,0)),
], note='On the <b>fourth</b> step only, change Padding Bottom to <b>10</b>, so the column does not end with a long empty tail.',
after=css('''
selector{position:relative}
selector::before{
  content:"";position:absolute;left:24px;top:54px;bottom:6px;
  width:1px;background:#E6E2D6;
}
'''))}
<p class="note">Paste that CSS on steps <b>1, 2 and 3</b> only. <b>Leave it off step 4</b>, or
a hairline dangles below the last icon with nothing to join.</p>

{icontile('icon-tile', 'see the table below', 'one per step')}

{block('Container', 'step-text', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Direction', 'Column'),
  ('Layout', 'Align Items', 'Start'),
  ('Layout', 'Width', '100 %'),
  ('Layout', 'Gap', '0'),
  ('Advanced', 'Padding', pad(0,0,0,0)),
])}

{block('Heading', 'step-title', [
  ('Content', 'Title', 'see the table below'),
  ('Content', 'HTML Tag', '<b>h3</b>'),
  ('Style', 'Alignment', 'Left'),
  ('Style', 'Text Color', '<code>#1F2833</code>'),
  ('Style', 'Typography &rsaquo; Family', 'Inter'),
  ('Style', 'Typography &rsaquo; Size', dev('27', '27', '24', ' PX')),
  ('Style', 'Typography &rsaquo; Weight', '600'),
  ('Style', 'Typography &rsaquo; Line Height', '1.3 EM'),
  ('Style', 'Typography &rsaquo; Letter Spacing', '&minus;0.3 PX'),
  ('Advanced', 'Margin', pad(0,0,0,0)),
])}

{para('step-body', 'see the table below', size='15.5', lh='1.4', mt=12, mb=0)}

<table class="overview"><thead><tr><th>#</th><th>Icon</th><th>Title</th><th>Text</th></tr></thead><tbody>
<tr><td>1</td><td><b>Comment Dots</b><br><code>far fa-comment-dots</code></td><td>WhatsApp Us</td><td>Message 011-1608 3188 and the front desk will find a slot that fits you. The clinic fills up fast, so booking ahead beats walking in.</td></tr>
<tr><td>2</td><td><b>User</b><br><code>fas fa-user</code></td><td>Consultation</td><td>Dr Tan checks your teeth, listens to your concerns and explains what she finds in plain language before anything is decided.</td></tr>
<tr><td>3</td><td><b>Tooth</b><br><code>fas fa-tooth</code></td><td>Treatment</td><td>Gentle, unhurried treatment with proper numbing and a running explanation. Most patients are surprised when it's already over.</td></tr>
<tr><td>4</td><td><b>Envelope</b><br><code>far fa-envelope</code></td><td>Follow-Up</td><td>Aftercare instructions to take home and a reminder when your next checkup is due, so good habits actually stick.</td></tr>
</tbody></table>
""", BUILD))

# ------------------------------------------------------------------ 11 reviews
pages.append(step(11, 'Patient Stories', f"""
{shot('10-reviews.jpg', 'One featured review with a photo, then four shorter ones two-up.')}
{tree('''
Container   reviews            Boxed 1250 - column - align center   (CSS ID: reviews)
 |- Container  sec-head
 |- Container  testi-tray       column - bg #E9E6DD - radius 24 - pad 10 - gap 10
     |- Container  testi-featured   row - gap 10
     |    |- Container  testi-photo   width 38% - 4:3 - radius 12
     |    |    |- Image       team-reception
     |    |- Container  quote-card    width 62% - bg #FFF - radius 12
     |         |- Heading     quote-mark   (watermark, absolute)
     |         |- Heading     big-quote
     |         |- Container   testi-meta   row - space-between - align end
     |              |- Container  meta-text  column
     |              |    |- Heading  t-name
     |              |    |- Heading  t-role
     |              |- Star Rating  rating
     |- Container  testi-grid       row - wrap - gap 10
          |- Container  testi-card x4   width 50% - bg #FFF - radius 12
               |- Star Rating  rating
               |- Heading      t-quote
               |- Divider      t-divider
               |- Container    t-user   column
                    |- Heading  t-name
                    |- Heading  t-role
''')}
{shell('reviews', 'reviews')}
{sechead('Patient Stories', 'Hear From the People&lt;br&gt;Who Visit Lumiere', '')}

{block('Container', 'testi-tray', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Direction', 'Column'),
  ('Layout', 'Align Items', 'Stretch'),
  ('Layout', 'Gap', '10'),
  ('Layout', 'Width', '100 %'),
  ('Style', 'Background Color', '<code>#E9E6DD</code>'),
  ('Advanced', 'Border Radius', '24 PX'),
  ('Advanced', 'Padding', pad(10,10,10,10)),
  ('Advanced', 'Margin', pad(0,0,0,0)),
])}

{block('Container', 'testi-featured', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Direction', dev('Row', '<b>Column</b>', '<b>Column</b>')),
  ('Layout', 'Align Items', 'Stretch'),
  ('Layout', 'Gap', '10'),
  ('Layout', 'Width', '100 %'),
  ('Advanced', 'Padding', pad(0,0,0,0)),
])}

{block('Container', 'testi-photo', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Width', dev('38', '100', '100', ' %')),
  ('Advanced', 'Border Radius', '12 PX'),
  ('Advanced', 'Overflow', '<b>Hidden</b>'),
  ('Advanced', 'Padding', pad(0,0,0,0)),
], after=css('selector{aspect-ratio:4/3}'))}

{block('Image', 'team-reception', [
  ('Content', 'Choose Image', '<code>team-reception.jpg</code>'),
  ('Content', 'Image Resolution', '<b>Full</b>'),
  ('Content', 'Link', 'None'),
  ('Style', 'Width', '100 %'),
  ('Style', 'Height', '100 %'),
  ('Style', 'Object Fit', '<b>Cover</b>'),
])}

{block('Container', 'quote-card', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Direction', 'Column'),
  ('Layout', 'Justify Content', 'Start'),
  ('Layout', 'Align Items', 'Start'),
  ('Layout', 'Width', dev('62', '100', '100', ' %')),
  ('Layout', 'Gap', '0'),
  ('Style', 'Background Color', '<code>#FFFFFF</code>'),
  ('Advanced', 'Border Radius', '12 PX'),
  ('Advanced', 'Overflow', '<b>Hidden</b>'),
  ('Advanced', 'Padding', dev(pad(40,44,34,44), pad(30,30,28,30), pad(26,26,26,26))),
], note='Overflow Hidden stops the quote watermark spilling past the rounded corner.')}

{block('Heading', 'quote-mark', [
  ('Content', 'Title', '&rdquo;'),
  ('Content', 'HTML Tag', 'p'),
  ('Style', 'Text Color', '<code>#EFECE3</code>'),
  ('Style', 'Typography &rsaquo; Family', 'Inter'),
  ('Style', 'Typography &rsaquo; Size', dev('190', '150', '110', ' PX')),
  ('Style', 'Typography &rsaquo; Weight', '600'),
  ('Style', 'Typography &rsaquo; Line Height', '1 EM'),
  ('Advanced', 'Z-Index', '0'),
  ('Advanced', 'Margin', pad(0,0,0,0)),
], note='Make this the <b>first</b> child of quote-card so it sits behind the text. It is purely decorative &mdash; if it fights you, delete it and move on, the section reads fine without it.',
after=css('selector{position:absolute; top:-30px; right:28px; pointer-events:none}'))}

{block('Heading', 'big-quote', [
  ('Content', 'Title', 'the featured quote from the table below'),
  ('Content', 'HTML Tag', 'p'),
  ('Style', 'Alignment', 'Left'),
  ('Style', 'Text Color', '<code>#1F2833</code>'),
  ('Style', 'Typography &rsaquo; Family', 'Inter'),
  ('Style', 'Typography &rsaquo; Size', dev('26', '23', '19.5', ' PX')),
  ('Style', 'Typography &rsaquo; Weight', '600'),
  ('Style', 'Typography &rsaquo; Line Height', '1.35 EM'),
  ('Style', 'Typography &rsaquo; Letter Spacing', '&minus;0.4 PX'),
  ('Advanced', 'Z-Index', '1'),
  ('Advanced', 'Margin', pad(0,0,40,0)),
])}

{block('Container', 'testi-meta', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Direction', 'Row'),
  ('Layout', 'Justify Content', 'Space Between'),
  ('Layout', 'Align Items', '<b>End</b>'),
  ('Layout', 'Gap', '20'),
  ('Layout', 'Width', '100 %'),
  ('Advanced', 'Margin', 'Top <b>auto</b> &mdash; type the word <i>auto</i>, so it pins to the card bottom'),
  ('Advanced', 'Padding', pad(0,0,0,0)),
  ('Advanced', 'Z-Index', '1'),
])}

{block('Container', 'meta-text and t-user', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Direction', 'Column'),
  ('Layout', 'Align Items', 'Start'),
  ('Layout', 'Gap', '0'),
  ('Layout', 'Width', 'leave empty'),
  ('Advanced', 'Padding', pad(0,0,0,0)),
], note='Identical settings in both places &mdash; the featured card and each of the four small cards.')}

{block('Heading', 't-name', [
  ('Content', 'Title', 'the reviewer name from the table below'),
  ('Content', 'HTML Tag', 'p'),
  ('Style', 'Alignment', 'Left'),
  ('Style', 'Text Color', '<code>#1F2833</code>'),
  ('Style', 'Typography &rsaquo; Family', 'Inter'),
  ('Style', 'Typography &rsaquo; Size', '16 PX'),
  ('Style', 'Typography &rsaquo; Weight', '600'),
  ('Advanced', 'Margin', pad(0,0,0,0)),
])}
{para('t-role', 'the role line from the table below', size='14', lh='1.4', mt=3, mb=0)}

{block('Star Rating', 'rating', [
  ('Content', 'Rating Scale', '<b>0-5</b>'),
  ('Content', 'Rating', '5'),
  ('Content', 'Icon', 'Star'),
  ('Content', 'Unmarked Style', 'Solid'),
  ('Style', 'Alignment', 'Left'),
  ('Style', 'Size', '15 PX'),
  ('Style', 'Spacing Between', '3 PX'),
  ('Style', 'Star Color', '<code>#F0B428</code>'),
  ('Style', 'Unmarked Color', '<code>#F0B428</code>'),
  ('Advanced', 'Margin', pad(0,0,0,0)),
], note='All five reviews are five stars, so Unmarked Color never actually shows &mdash; set it the same to be safe. This same widget appears once in the featured card and once at the top of each small card.')}

<h3 class="sub">The four small cards</h3>
{block('Container', 'testi-grid', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Direction', 'Row'),
  ('Layout', 'Align Items', 'Stretch'),
  ('Layout', 'Wrap', '<b>Wrap</b>'),
  ('Layout', 'Gap', '10'),
  ('Layout', 'Width', '100 %'),
  ('Advanced', 'Padding', pad(0,0,0,0)),
])}

{block('Container', 'testi-card', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Direction', 'Column'),
  ('Layout', 'Justify Content', 'Start'),
  ('Layout', 'Align Items', 'Start'),
  ('Layout', 'Width', dev('50', '100', '100', ' %')),
  ('Layout', 'Gap', '0'),
  ('Style', 'Background Color', '<code>#FFFFFF</code>'),
  ('Advanced', 'Border Radius', '12 PX'),
  ('Advanced', 'Padding', pad(26,28,26,28)),
], note='Two cards at 50% plus a 10px gap overflows very slightly, which is why Wrap is on. Elementor absorbs it and the cards still sit two-up on desktop.')}

{para('t-quote', 'the quote from the table below', size='15.5', color='#1F2833', lh='1.55', mt=18, mb=0)}

{block('Divider', 't-divider', [
  ('Content', 'Style', 'Solid'),
  ('Content', 'Weight', '1 PX'),
  ('Content', 'Color', '<code>#EFECE3</code>'),
  ('Content', 'Width', '100 %'),
  ('Content', 'Align', 'Center'),
  ('Content', 'Add Element', '<b>None</b>'),
  ('Style', 'Gap', '20 PX'),
  ('Advanced', 'Margin', pad(0,0,0,0)),
])}

<table class="overview"><thead><tr><th>Card</th><th>Quote</th><th>Name</th><th>Role line</th></tr></thead><tbody>
<tr><td><b>Featured</b></td><td>"Two other clinics had suggested surgical removal. Dr Tan managed to remove it without any cutting. Truly painless, gentle, and very professional."</td><td>NSRN AMR</td><td>Google Review &middot; Local Guide</td></tr>
<tr><td>1</td><td>"The airflow scaling is almost no pain. Great explanation from the dentist on my teeth condition. Most importantly it's near to where I stay."</td><td>Thomas Teh</td><td>Scaling patient</td></tr>
<tr><td>2</td><td>"I personally named her my tooth fairy. Honestly don't wait on it. It's painless if you are done at Lumiere Dental, Kota Warisan!"</td><td>Izzati Azahar</td><td>Root canal patient</td></tr>
<tr><td>3</td><td>"They accept all insurance companies, so no worries as they are most likely your panel clinic. Do make an appointment before coming in."</td><td>Allan Manan</td><td>Scaling patient</td></tr>
<tr><td>4</td><td>"Dr Tan Mei Wen is so thorough and informative, and lets us know every step of the way what's going on. Personalized, comfortable and stress-free."</td><td>Noorhafizah Abd Samat</td><td>Local Guide &middot; 73 reviews</td></tr>
</tbody></table>
<p class="note">These are real Google reviews, retyped from the clinic's own screenshots.
Keep the wording, punctuation and names exactly as they are. <b>Do not fix the grammar</b>
&mdash; edited reviews stop reading as real, and altering a named person's words is not ours
to do.</p>
""", BUILD))

# ------------------------------------------------------------------ 12 faq
pages.append(step(12, 'FAQ', f"""
{shot('11-faq.jpg', 'Six questions in a narrow tray, the first one open.')}
{tree('''
Container   faq                Boxed 1250 - column - align center   (CSS ID: faq)
 |- Container  sec-head
 |- Container  faq-tray         bg #E9E6DD - radius 24 - pad 10 - width 620
      |- Accordion  faq-items   6 items
''')}
{shell('faq', 'faq')}
{sechead('FAQ', 'Frequently Asked&lt;br&gt;Questions', '')}

{block('Container', 'faq-tray', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Direction', 'Column'),
  ('Layout', 'Align Items', 'Stretch'),
  ('Layout', 'Width', dev('Custom &rarr; 620 PX', 'Custom &rarr; 620 PX', '100 %')),
  ('Layout', 'Gap', '0'),
  ('Style', 'Background Color', '<code>#E9E6DD</code>'),
  ('Advanced', 'Border Radius', '24 PX'),
  ('Advanced', 'Padding', pad(10,10,10,10)),
])}

{block('Accordion', 'faq-items', [
  ('Content', 'Items', 'six &mdash; from the table below'),
  ('Content', 'Layout &rsaquo; Default State', '<b>First item expanded</b>'),
  ('Content', 'Layout &rsaquo; Icon &rsaquo; Closed', 'Plus &nbsp;<code>fas fa-plus</code>'),
  ('Content', 'Layout &rsaquo; Icon &rsaquo; Opened', 'Minus &nbsp;<code>fas fa-minus</code>'),
  ('Content', 'Layout &rsaquo; Icon Position', 'End'),
  ('Content', 'Layout &rsaquo; FAQ Schema', '<b>On</b>'),
  ('Content', 'Layout &rsaquo; Title HTML Tag', 'h3'),
  ('Style', 'Items &rsaquo; Space Between', '10 PX'),
  ('Style', 'Header &rsaquo; Background (Normal)', '<code>#FFFFFF</code>'),
  ('Style', 'Header &rsaquo; Background (Active)', '<code>#FFFFFF</code>'),
  ('Style', 'Header &rsaquo; Border Radius', '12 PX'),
  ('Style', 'Header &rsaquo; Padding', pad(21,22,21,22)),
  ('Style', 'Header &rsaquo; Title Color (Normal)', '<code>#1F2833</code>'),
  ('Style', 'Header &rsaquo; Title Typography', 'Inter &middot; 16.5 PX &middot; weight 500'),
  ('Style', 'Header &rsaquo; Icon Color', '<code>#1F2833</code>'),
  ('Style', 'Header &rsaquo; Icon Size', '16 PX'),
  ('Style', 'Content &rsaquo; Background', '<code>#FFFFFF</code>'),
  ('Style', 'Content &rsaquo; Text Color', '<code>#5A6270</code>'),
  ('Style', 'Content &rsaquo; Typography', 'Inter &middot; 15.5 PX &middot; weight 400 &middot; line 1.5 EM'),
  ('Style', 'Content &rsaquo; Padding', pad(0,22,21,22)),
  ('Style', 'Content &rsaquo; Border Radius', '12 PX'),
], note='Icon settings, Default State and the FAQ Schema toggle are all on <b>Content &rsaquo; Layout</b> in Elementor 4.x. <b>Turn the schema on</b> &mdash; it makes this page eligible for Google&rsquo;s expandable FAQ results, which is free visibility for a page whose whole job is search and ads traffic.')}

<table class="faqt"><thead><tr><th>#</th><th>Question and answer</th></tr></thead><tbody>
<tr><td class="k">1</td><td><b>How do I book an appointment?</b><p>WhatsApp us at 011-1608 3188 and the front desk will confirm your slot, usually within the hour. You can also call the same number or walk in, though appointments are strongly recommended.</p></td></tr>
<tr><td class="k">2</td><td><b>Are you a panel clinic for my insurance?</b><p>We are a panel clinic for AIA, PMCare, Mednefits, HealthMetrics and MedKad. Message us your insurer and policy details and we will confirm your coverage before your visit.</p></td></tr>
<tr><td class="k">3</td><td><b>Can I just walk in?</b><p>Walk-ins are welcome when there is a free slot, but the clinic is fully booked most days. A quick WhatsApp before you come saves you the wait.</p></td></tr>
<tr><td class="k">4</td><td><b>What should I bring for my first visit?</b><p>Bring your IC or passport, your insurance or panel card if you have one, and any previous dental records or X-rays. That's all we need to get you started.</p></td></tr>
<tr><td class="k">5</td><td><b>Do you treat children?</b><p>Yes. The clinic has a dedicated kids corner, and Dr Tan paces every appointment around the child rather than the clock.</p></td></tr>
<tr><td class="k">6</td><td><b>Where exactly is the clinic?</b><p>G02 &amp; M03A, KIPMall Kota Warisan, Jalan Warisan Sentral 3, 43900 Sepang, Selangor. We are on the ground floor of KIPMall, with plenty of parking outside.</p></td></tr>
</tbody></table>
<p class="note">The original design animates the icon from three bars into an &times;.
Elementor's accordion has its own icon set, so Plus / Minus is the right call. Do not write
custom code for it.</p>
""", BUILD))

# ------------------------------------------------------------------ 13 contact
pages.append(step(13, 'Contact', f"""
{shot('12-contact.jpg', 'Details on the left, live Google map on the right.')}
{tree('''
Container   contact            Boxed 1250 - column - align center   (CSS ID: contact)
 |- Container  sec-head
 |- Container  contact-grid     row - bg #E9E6DD - radius 24 - pad 10 - gap 14
     |- Container  contact-info  width 48% - bg #FFF - radius 12 - column
     |    |- Icon Box  ct-row x4
     |    |- Button    contact-cta
     |- Container  contact-map   width 52% - radius 12 - overflow hidden
          |- HTML       map   <-- paste file
''')}
{shell('contact', 'contact')}
{sechead('Contact Us', 'Come See Us in&lt;br&gt;Kota Warisan',
         'Inside KIPMall, a few minutes from Salak Tinggi and Bandar Baru Salak Tinggi.')}

{block('Container', 'contact-grid', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Direction', dev('Row', '<b>Column</b>', '<b>Column</b>')),
  ('Layout', 'Align Items', 'Stretch'),
  ('Layout', 'Gap', '14'),
  ('Layout', 'Width', '100 %'),
  ('Style', 'Background Color', '<code>#E9E6DD</code>'),
  ('Advanced', 'Border Radius', '24 PX'),
  ('Advanced', 'Padding', pad(10,10,10,10)),
])}

{block('Container', 'contact-info', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Direction', 'Column'),
  ('Layout', 'Justify Content', 'Start'),
  ('Layout', 'Align Items', 'Start'),
  ('Layout', 'Width', dev('48', '100', '100', ' %')),
  ('Layout', 'Gap', '6'),
  ('Style', 'Background Color', '<code>#FFFFFF</code>'),
  ('Advanced', 'Border Radius', '12 PX'),
  ('Advanced', 'Padding', dev(pad(34,34,32,34), pad(28,28,28,28), pad(24,20,26,20))),
])}

{block('Icon Box', 'ct-row', [
  ('Content', 'Icon', 'see the table below'),
  ('Content', 'Title', 'see the table below'),
  ('Content', 'Description', 'see the table below'),
  ('Content', 'Link', 'see the table below'),
  ('Content', 'Title HTML Tag', 'p'),
  ('Style', 'Box &rsaquo; Icon Position', '<b>Left</b>'),
  ('Style', 'Box &rsaquo; Vertical Alignment', '<b>Top</b>'),
  ('Style', 'Box &rsaquo; Icon Spacing', '16 PX'),
  ('Style', 'Icon &rsaquo; View', '<b>Stacked</b>'),
  ('Style', 'Icon &rsaquo; Shape', 'Square'),
  ('Style', 'Icon &rsaquo; Primary Color', '<code>#8F702A</code>'),
  ('Style', 'Icon &rsaquo; Secondary Color', '<code>rgba(212,178,96,.16)</code>'),
  ('Style', 'Icon &rsaquo; Size', dev('22', '22', '19', ' PX')),
  ('Style', 'Icon &rsaquo; Padding', '11 PX'),
  ('Style', 'Icon &rsaquo; Border Radius', '12 PX'),
  ('Style', 'Content &rsaquo; Alignment', 'Left'),
  ('Style', 'Content &rsaquo; Title Color', '<code>#1F2833</code>'),
  ('Style', 'Content &rsaquo; Title Typography', 'Inter &middot; 15.5 PX &middot; weight 600'),
  ('Style', 'Content &rsaquo; Title Spacing', '3 PX'),
  ('Style', 'Content &rsaquo; Description Color', '<code>#5A6270</code>'),
  ('Style', 'Content &rsaquo; Description Typography', 'Inter &middot; 15 PX &middot; line 1.5 EM'),
  ('Advanced', 'Padding', pad(14,10,14,10)),
], note='Icon Position, Vertical Alignment and Icon Spacing all live under <b>Style &rsaquo; Box</b> in Elementor 4.x. Build one, then duplicate three times.')}

<table class="overview"><thead><tr><th>#</th><th>Icon</th><th>Title</th><th>Description</th><th>Link</th></tr></thead><tbody>
<tr><td>1</td><td><b>Map Marker Alt</b><br><code>fas fa-map-marker-alt</code></td><td>Visit the clinic</td><td>G02 &amp; M03A, KIPMall, Jalan Warisan Sentral 3,<code>&lt;br&gt;</code>Kota Warisan, 43900 Sepang, Selangor</td><td><code>https://maps.app.goo.gl/7LfYX7xw62fKfRQy7</code></td></tr>
<tr><td>2</td><td><b>Comment Dots</b><br><code>far fa-comment-dots</code></td><td>WhatsApp or call</td><td>011-1608 3188</td><td>the booking WhatsApp URL</td></tr>
<tr><td>3</td><td><b>Envelope</b><br><code>far fa-envelope</code></td><td>Email us</td><td>lumieredentalclinics@gmail.com</td><td><code>mailto:lumieredentalclinics@gmail.com</code></td></tr>
<tr><td>4</td><td><b>Clock</b><br><code>far fa-clock</code></td><td>Opening hours</td><td>Mon, Wed, Thu, Fri, Sat &nbsp;9:00am &ndash; 7:30pm<code>&lt;br&gt;</code>Tue &amp; Sun &nbsp;9:00am &ndash; 6:00pm</td><td><b>leave empty</b></td></tr>
</tbody></table>
<p class="note">The Description field accepts <code>&lt;br&gt;</code> &mdash; type it where
the table shows it, so the address and the hours break onto two lines.</p>
<p class="note"><b>Confirm the hours before this page is published.</b> They come from
Lumiere's own group website, but two directory listings disagree. It is the single fact on
this page most likely to be wrong, and the most irritating to a patient who turns up to a
closed door.</p>

{block('Button', 'contact-cta', [
  ('Content', 'Text', 'Book On WhatsApp'),
  ('Content', 'Link', f'<code>{WA}</code>'),
  ('Content', 'Link &rsaquo; Open in new window', 'On'),
  ('Content', 'Icon', 'Arrow Right &middot; After &middot; spacing 9'),
  ('Style', 'Button &rsaquo; Position', 'Left'),
  ('Style', 'Typography', 'Inter &middot; 15 PX &middot; weight 500'),
  ('Style', 'Text Color (Normal)', '<code>#FFFFFF</code>'),
  ('Style', 'Background (Normal)', '<code>#33485C</code>'),
  ('Style', 'Background (Hover)', '<code>#26394B</code>'),
  ('Style', 'Border Radius', '8 PX'),
  ('Style', 'Padding', pad(12,22,12,22)),
  ('Advanced', 'Margin', pad(18,0,0,0)),
])}

{block('Container', 'contact-map', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Width', dev('52', '100', '100', ' %')),
  ('Layout', 'Min Height', dev('420', '320', '320', ' PX')),
  ('Advanced', 'Border Radius', '12 PX'),
  ('Advanced', 'Overflow', '<b>Hidden</b>'),
  ('Advanced', 'Padding', pad(0,0,0,0)),
])}

{block('HTML', 'map', [
  ('Content', 'HTML Code', 'paste <b>Step 13 - Map.html</b>'),
  ('Advanced', 'Padding', pad(0,0,0,0)),
  ('Advanced', 'Margin', pad(0,0,0,0)),
], note='A plain Google Maps embed &mdash; no API key and no billing account needed. Elementor&rsquo;s own Google Maps widget asks for a key on some setups, which is why this is a paste.')}
""", PASTE))

# ------------------------------------------------------------------ 14 footer
pages.append(step(14, 'Footer, WhatsApp button, animations', f"""
{shot('13-footer.jpg', 'Full-bleed white band, content still held to 1250.')}
{tree('''
Container   footer             FULL WIDTH - bg #FFF - border-top
 |- Container  footer-card      Boxed 1250 - row - gap 44
 |    |- Container  f-brand     width 32% - column
 |    |    |- Image      f-logo
 |    |    |- Heading    f-line
 |    |    |- Container  f-social   row - gap 9
 |    |         |- Icon x4
 |    |- Container  f-links     width 18% - column
 |    |    |- Heading    col-title
 |    |    |- Icon List  col-links
 |    |- Container  f-treat     width 20% - column  (same children)
 |    |- Container  f-contact   width 30% - column  (same children)
 |- Container  footer-bar       Boxed 1250 - row - space-between
      |- Heading   copyright
      |- Heading   f-alt
''')}

{block('Container', 'footer', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Content Width', '<b>Full Width</b>'),
  ('Layout', 'Direction', 'Column'),
  ('Layout', 'Align Items', 'Center'),
  ('Layout', 'Gap', '0'),
  ('Style', 'Background Type', 'Classic'),
  ('Style', 'Background Color', '<code>#FFFFFF</code>'),
  ('Style', 'Border Type', 'Solid'),
  ('Style', 'Border Width', 'Top <b>1</b> &nbsp; Right 0 &nbsp; Bottom 0 &nbsp; Left 0'),
  ('Style', 'Border Color', '<code>#E6E2D6</code>'),
  ('Advanced', 'Padding', pad(0,0,0,0)),
  ('Advanced', 'Margin', pad(70,0,0,0)),
], note='<b>Full Width</b> is what makes the white band run edge to edge. Both its children are Boxed, which keeps the text aligned with the rest of the page.')}

{block('Container', 'footer-card', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Content Width', 'Boxed'),
  ('Layout', 'Width', '1250'),
  ('Layout', 'Direction', dev('Row', 'Row', '<b>Column</b>')),
  ('Layout', 'Align Items', 'Start'),
  ('Layout', 'Wrap', dev('No wrap', '<b>Wrap</b>', 'Wrap')),
  ('Layout', 'Gap', dev('44', '34', '34')),
  ('Advanced', 'Padding', dev(pad(64,30,48,30), pad(36,30,36,30), pad(36,20,36,20))),
])}

{block('Container', 'f-brand / f-links / f-treat / f-contact', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Direction', 'Column'),
  ('Layout', 'Align Items', 'Start'),
  ('Layout', 'Gap', '0'),
  ('Layout', 'Width', 'Desktop <b>32 / 18 / 20 / 30</b> % &nbsp;&middot;&nbsp; Tablet <b>50</b> % each &nbsp;&middot;&nbsp; Mobile <b>100</b> %'),
  ('Advanced', 'Padding', pad(0,0,0,0)),
], note='Four containers, same settings, only the Width differs. Build f-brand, duplicate it three times, then set each Width and swap the contents.')}

{block('Image', 'f-logo', [
  ('Content', 'Choose Image', '<code>logo-gold.png</code>'),
  ('Content', 'Image Resolution', '<b>Full</b>'),
  ('Content', 'Link', 'Custom URL &rarr; <code>#home</code>'),
  ('Style', 'Height', '74 PX'),
  ('Style', 'Width', 'leave empty so it scales'),
  ('Advanced', 'Margin', pad(0,0,0,0)),
])}

{para('f-line', 'Lighting up your smile at KIPMall Kota Warisan, Sepang.', size='15.5', lh='1.4', mt=20, mb=0)}

{block('Container', 'f-social', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Direction', 'Row'),
  ('Layout', 'Align Items', 'Center'),
  ('Layout', 'Gap', '9'),
  ('Layout', 'Width', 'leave empty'),
  ('Advanced', 'Padding', pad(0,0,0,0)),
  ('Advanced', 'Margin', pad(22,0,0,0)),
])}

{block('Icon', 'f-social icons &times; 4', [
  ('Content', 'Icon', 'see the table below'),
  ('Content', 'Link', 'see the table below &middot; open in new window'),
  ('Content', 'View', '<b>Stacked</b>'),
  ('Content', 'Shape', '<b>Circle</b>'),
  ('Style', 'Primary Color (Normal)', '<code>#5A6270</code>'),
  ('Style', 'Secondary Color (Normal)', '<code>#FAF9F5</code>'),
  ('Style', 'Primary Color (Hover)', '<code>#FFFFFF</code>'),
  ('Style', 'Secondary Color (Hover)', '<code>#33485C</code>'),
  ('Style', 'Size', '18 PX'),
  ('Style', 'Padding', '9 PX'),
  ('Advanced', 'Margin', pad(0,0,0,0)),
], note='With View: Stacked, Primary is the glyph and Secondary is the circle behind it. The Hover rows are what turn the circle navy.')}

<table class="overview"><thead><tr><th>Icon</th><th>Link</th></tr></thead><tbody>
<tr><td><b>Facebook F</b> <code>fab fa-facebook-f</code></td><td><code>https://www.facebook.com/lumieredentalsepang</code></td></tr>
<tr><td><b>Instagram</b> <code>fab fa-instagram</code></td><td><code>https://www.instagram.com/lumieredentalsepang</code></td></tr>
<tr><td><b>WhatsApp</b> <code>fab fa-whatsapp</code></td><td><code>https://wa.me/601116083188</code></td></tr>
<tr><td><b>Map Marker Alt</b> <code>fas fa-map-marker-alt</code></td><td><code>https://maps.app.goo.gl/7LfYX7xw62fKfRQy7</code></td></tr>
</tbody></table>

<h3 class="sub">The three link columns</h3>
{block('Heading', 'col-title', [
  ('Content', 'Title', 'Quick Links / Treatments / Contact Us'),
  ('Content', 'HTML Tag', '<b>h3</b>'),
  ('Style', 'Alignment', 'Left'),
  ('Style', 'Text Color', '<code>#1F2833</code>'),
  ('Style', 'Typography &rsaquo; Family', 'Inter'),
  ('Style', 'Typography &rsaquo; Size', '16.5 PX'),
  ('Style', 'Typography &rsaquo; Weight', '600'),
  ('Advanced', 'Margin', pad(0,0,20,0)),
])}
{block('Icon List', 'col-links', [
  ('Content', 'Items', 'see the table below'),
  ('Content', 'Item &rsaquo; Icon', '<b>None</b> for Quick Links and Treatments &mdash; delete the default icon on each item'),
  ('Content', 'Item &rsaquo; Link', 'per the table'),
  ('Style', 'List &rsaquo; Space Between', '12 PX'),
  ('Style', 'List &rsaquo; Alignment', 'Left'),
  ('Style', 'List &rsaquo; Divider', 'Off'),
  ('Style', 'Text &rsaquo; Text Color (Normal)', '<code>#5A6270</code>'),
  ('Style', 'Text &rsaquo; Text Color (Hover)', '<code>#1F2833</code>'),
  ('Style', 'Text &rsaquo; Typography &rsaquo; Family', 'Inter'),
  ('Style', 'Text &rsaquo; Typography &rsaquo; Size', '15.5 PX'),
  ('Style', 'Text &rsaquo; Typography &rsaquo; Weight', '400'),
  ('Advanced', 'Margin', pad(0,0,0,0)),
], note='For the <b>Contact Us</b> column, keep icons: Envelope, Phone Alt and Map Marker Alt &mdash; Style &rsaquo; Icon &rsaquo; Color <code>#8F702A</code>, Size 19 PX, Gap 11 PX.')}

<table class="overview"><thead><tr><th>Column</th><th>Items</th></tr></thead><tbody>
<tr><td>Quick Links</td><td>Home &rarr; <code>#home</code> &middot; About &rarr; <code>#about</code> &middot; Services &rarr; <code>#services</code> &middot; Reviews &rarr; <code>#reviews</code></td></tr>
<tr><td>Treatments</td><td>General Dentistry &middot; Teeth Whitening &middot; Dental Implants &middot; Braces &amp; Aligners &mdash; all four link to <code>#services</code></td></tr>
<tr><td>Contact Us</td><td>lumieredentalclinics@gmail.com &rarr; <code>mailto:</code> &middot; 011-1608 3188 &rarr; <code>tel:+601116083188</code> &middot; G02 &amp; M03A, KIPMall, Jalan Warisan Sentral 3, Kota Warisan, 43900 Sepang, Selangor &rarr; no link</td></tr>
</tbody></table>

{block('Container', 'footer-bar', [
  ('Layout', 'Container Layout', 'Flexbox'),
  ('Layout', 'Content Width', 'Boxed'),
  ('Layout', 'Width', '1250'),
  ('Layout', 'Direction', dev('Row', '<b>Column</b>', '<b>Column</b>')),
  ('Layout', 'Justify Content', 'Space Between'),
  ('Layout', 'Align Items', 'Center'),
  ('Layout', 'Gap', '16'),
  ('Style', 'Border Type', 'Solid'),
  ('Style', 'Border Width', 'Top <b>1</b> &nbsp; Right 0 &nbsp; Bottom 0 &nbsp; Left 0'),
  ('Style', 'Border Color', '<code>#EFECE3</code>'),
  ('Advanced', 'Padding', dev(pad(22,30,28,30), pad(18,30,88,30), pad(18,20,88,20))),
], note='The big Bottom padding on tablet and mobile is deliberate &mdash; it keeps this line clear of the floating WhatsApp button, which sits over the bottom-right corner.')}

{block('Heading', 'copyright', [
  ('Content', 'Title', '&copy; 2026 Lumiere Dental Clinic Kota Warisan. All rights reserved.'),
  ('Content', 'HTML Tag', 'p'),
  ('Style', 'Alignment', dev('Left', 'Center', 'Center')),
  ('Style', 'Text Color', '<code>#5A6270</code>'),
  ('Style', 'Typography', 'Inter &middot; 14.5 PX &middot; weight 400'),
  ('Advanced', 'Margin', pad(0,0,0,0)),
])}
{block('Heading', 'f-alt', [
  ('Content', 'Title', 'Klinik Pergigian Lumiere &middot; &#20048;&#32654;&#29273;&#31185;&#35786;&#25152;'),
  ('Content', 'HTML Tag', 'p'),
  ('Style', 'Alignment', dev('Right', 'Center', 'Center')),
  ('Style', 'Text Color', '<code>#5A6270</code>'),
  ('Style', 'Typography', 'Inter &middot; 14.5 PX &middot; weight 400'),
  ('Advanced', 'Padding', dev('Top 0 &nbsp; Right <b>74</b> &nbsp; Bottom 0 &nbsp; Left 0', pad(0,0,0,0), pad(0,0,0,0))),
  ('Advanced', 'Margin', pad(0,0,0,0)),
], note='That 74px right padding on desktop stops the Chinese clinic name running underneath the floating button.')}

<h3 class="sub">The floating WhatsApp button</h3>
<p>Elementor Pro has this built in, as its own template type.
<b>Templates &rsaquo; Add New &rsaquo; Floating Buttons</b> &rarr; choose <b>WhatsApp</b>.</p>
{table([
  ('Content', 'Platform', 'WhatsApp'),
  ('Content', 'Number', '<code>601116083188</code>'),
  ('Content', 'Message', "Hi Lumiere Dental Kota Warisan, I'd like to book an appointment."),
  ('Content', 'Click Action', 'WhatsApp'),
  ('Style', 'Button &rsaquo; Size', 'Custom &rarr; <b>58</b> PX'),
  ('Style', 'Button &rsaquo; Background (Normal)', '<code>#25D366</code>'),
  ('Style', 'Button &rsaquo; Icon Color', '<code>#FFFFFF</code>'),
  ('Advanced', 'Position &rsaquo; Horizontal', 'Right &nbsp; Offset ' + dev('24', '16', '16', ' PX')),
  ('Advanced', 'Position &rsaquo; Vertical', 'Bottom &nbsp; Offset ' + dev('24', '16', '16', ' PX')),
])}
<p>Publish it, then set its <b>Display Conditions</b> to this page only, unless the clinic
wants the button across the whole site.</p>

<h3 class="sub">Last: the scroll animations</h3>
<p>The finished page fades each block up as it comes into view. Select the container named in
the left column and set <b>Advanced &rsaquo; Motion Effects</b>:</p>
{table([
  ('Advanced', 'Entrance Animation', '<b>Fade In Up</b>'),
  ('Advanced', 'Animation Duration', '<b>Slow</b>'),
  ('Advanced', 'Animation Delay', 'see the table below, in ms'),
])}
<table class="overview"><thead><tr><th>Apply to</th><th>Animation Delay</th></tr></thead><tbody>
<tr><td>Every <code>sec-head</code> (7 of them)</td><td>0</td></tr>
<tr><td>Hero: badges, h1, sub, actions, proof</td><td>50, 150, 300, 420, 540</td></tr>
<tr><td>The 5 <code>panel-item</code> cards</td><td>40, 100, 160, 220, 280</td></tr>
<tr><td>The 4 <code>vision-card</code> cards</td><td>50, 130, 210, 290</td></tr>
<tr><td>The 4 <code>stat-card</code> cards</td><td>50, 150, 250, 350</td></tr>
<tr><td><code>doc-block</code>, <code>faq-tray</code>, <code>contact-grid</code></td><td>0 each</td></tr>
<tr><td>The 4 facilities cards</td><td>50, 150, 100, 200</td></tr>
<tr><td>The 4 <code>how-step</code> rows</td><td>0 each</td></tr>
<tr><td><code>testi-featured</code>, then the 4 <code>testi-card</code></td><td>0, then 50, 120, 190, 260</td></tr>
</tbody></table>
<p class="note"><b>Do not</b> put an entrance animation on <code>svc-card</code>. It fights
the sticky positioning and the cards visibly jump as they pin.</p>
<div class="donebox"><b>Done when:</b> the page runs from a full-height hero to a full-width
footer, the service cards stack as you scroll, and the green WhatsApp button floats above
everything.</div>
""", BUILD))

# ------------------------------------------------------------------ QA
pages.append("""
<section class="step newpage"><div class="stephead"><span class="num">Finally</span>
<h2>Check these before you hand it over</h2></div>

<table class="check"><tbody>
<tr><td>&#9744;</td><td><b>The hero is exactly one screen tall</b> on a laptop and on a phone. A gap underneath on mobile means the <code>100dvh</code> line did not save.</td></tr>
<tr><td>&#9744;</td><td><b>The eight service cards stack.</b> If they scroll past each other normally, a parent has Overflow: Hidden &mdash; check <code>services</code> and <code>svc-stack</code>.</td></tr>
<tr><td>&#9744;</td><td><b>The Dr Tan photo travels</b> with the bio on desktop and sits still on mobile.</td></tr>
<tr><td>&#9744;</td><td><b>The How It Works left panel holds still</b> while the four steps pass it.</td></tr>
<tr><td>&#9744;</td><td><b>All six menu links land correctly</b> &mdash; the heading must not be hidden behind the header. If it is, the <code>scroll-margin-top</code> rule from Step 1d is missing.</td></tr>
<tr><td>&#9744;</td><td><b>The header turns white</b> past the hero, and the hamburger panel is cream with dark links under 1024px.</td></tr>
<tr><td>&#9744;</td><td><b>No sideways scrolling at 390px wide.</b> Usually one container left on a fixed px width instead of 100%.</td></tr>
<tr><td>&#9744;</td><td><b>Every WhatsApp link opens with its message pre-filled</b>, and each of the eight service buttons names its own treatment.</td></tr>
<tr><td>&#9744;</td><td><b>Nothing is cropped.</b> Compare each card with the live mockup &mdash; the 4:3 and 3:4 ratios are deliberate.</td></tr>
<tr><td>&#9744;</td><td><b>The four counters animate</b> and land on 9+, 8, 8 and 5.0.</td></tr>
<tr><td>&#9744;</td><td><b>The FAQ schema toggle is on</b> and the first item is open on load.</td></tr>
<tr><td>&#9744;</td><td><b>Opening hours confirmed with the clinic</b>, not taken from this guide.</td></tr>
<tr><td>&#9744;</td><td><b>The two inferred stats confirmed</b> &mdash; "9+ years" and "5.0".</td></tr>
</tbody></table>

<h3 class="sub">Every link on the page, in one place</h3>
<table class="overview"><thead><tr><th>What</th><th>Value</th></tr></thead><tbody>
<tr><td>WhatsApp, plain</td><td><code>https://wa.me/601116083188</code></td></tr>
<tr><td>WhatsApp, booking</td><td><code>https://wa.me/601116083188?text=Hi%20Lumiere%20Dental%20Kota%20Warisan%2C%20I%27d%20like%20to%20book%20an%20appointment.</code></td></tr>
<tr><td>WhatsApp, panel check</td><td><code>https://wa.me/601116083188?text=Hi%2C%20could%20you%20check%20if%20my%20insurance%20panel%20is%20accepted%3F</code></td></tr>
<tr><td>Phone</td><td><code>tel:+601116083188</code></td></tr>
<tr><td>Email</td><td><code>mailto:lumieredentalclinics@gmail.com</code></td></tr>
<tr><td>Google Maps</td><td><code>https://maps.app.goo.gl/7LfYX7xw62fKfRQy7</code></td></tr>
<tr><td>Facebook</td><td><code>https://www.facebook.com/lumieredentalsepang</code></td></tr>
<tr><td>Instagram</td><td><code>https://www.instagram.com/lumieredentalsepang</code></td></tr>
<tr><td>Group website</td><td><code>https://www.lumieredental.com.my/</code></td></tr>
<tr><td>Live mockup</td><td><code>https://mysense-my.github.io/lumiere-dental-kota-warisan/</code></td></tr>
</tbody></table>

<h3 class="sub">If something misbehaves</h3>
<table class="overview"><thead><tr><th>Symptom</th><th>Cause</th><th>Fix</th></tr></thead><tbody>
<tr><td>Cards do not stack</td><td>Overflow: Hidden on a parent</td><td>Set every ancestor to Default</td></tr>
<tr><td>Sticky jumps instead of sliding</td><td>Motion Effects &rsaquo; Sticky was used</td><td>Turn it off; use the Custom CSS</td></tr>
<tr><td>Photo overflows its column</td><td>Parent Align Items on Stretch</td><td>Set the parent to Align Items: Start</td></tr>
<tr><td>Menu link lands under the header</td><td>Missing <code>scroll-margin-top</code></td><td>Add the Step 1d CSS</td></tr>
<tr><td>Pill stretches the full width</td><td>A width value is set on it</td><td>Clear Layout &rsaquo; Width</td></tr>
<tr><td>Image looks soft</td><td>Resolution left on Large</td><td>Set Image Resolution to Full</td></tr>
<tr><td>Cards jump while pinning</td><td>Entrance Animation on svc-card</td><td>Remove it from those eight</td></tr>
<tr><td>Counter shows 5 not 5.0</td><td>Suffix field empty</td><td>Put <code>.0</code> in Number Suffix</td></tr>
<tr><td>Two columns end at different heights</td><td>A photo ratio was changed</td><td>Restore 4:3 + 3:4 per column</td></tr>
<tr><td>A control is not where this guide says</td><td>Elementor version difference</td><td>Send a screenshot of that panel</td></tr>
</tbody></table>
</section>
""")

CSS = """
@page{size:A4;margin:14mm 14mm 16mm}
*{box-sizing:border-box}
body{font-family:Inter,system-ui,sans-serif;color:#1F2833;font-size:10.5px;line-height:1.5;margin:0}
h1,h2,h3,h4{margin:0;font-weight:600;letter-spacing:-.02em}
code{font-family:Menlo,monospace;font-size:.92em;background:#F3F1EA;padding:1px 5px;border-radius:4px;color:#6b5210;word-break:break-all}
b{font-weight:600}
.cover h1{font-size:30px;line-height:1.15;margin:4px 0 12px;max-width:520px}
.kicker{font-weight:600;color:#8F702A;margin:0}
.lead{font-size:13px;color:#5A6270;max-width:560px;margin:0 0 18px}
.facts{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:20px}
.facts div{background:#F3F1EA;border-radius:10px;padding:10px 12px;display:grid;gap:2px}
.facts b{font-size:9.5px;color:#5A6270;font-weight:600}
.cover h3{font-size:14px;margin:16px 0 8px}
.cap{font-size:10px;color:#5A6270;margin:5px 0 0}
table{border-collapse:collapse;width:100%}
.overview th,.overview td{padding:7px 9px;border-bottom:1px solid #E6E2D6;text-align:left;font-size:10.2px;vertical-align:top}
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
.shot img{width:100%;max-height:225px;object-fit:cover;object-position:top;border-radius:8px;border:1px solid #E6E2D6;display:block}
.shot figcaption{font-size:9.5px;color:#5A6270;margin-top:3px}
.tree{font-family:Menlo,monospace;font-size:8.8px;line-height:1.55;background:#1F2833;color:#EDEAE0;border-radius:8px;padding:10px 12px;margin:0 0 10px;white-space:pre;break-inside:avoid}
.note{background:#F7F5EE;border-left:3px solid #C9A64D;padding:6px 9px;margin:6px 0;border-radius:0 6px 6px 0;color:#3a3f48}
.donebox{background:#EDF3EC;border-left:3px solid #4F6B3C;padding:8px 10px;border-radius:0 6px 6px 0;margin-top:10px}
.do{margin:6px 0 10px;padding-left:18px}
.do li{margin:4px 0}
.block{margin:0 0 12px;break-inside:avoid}
.block h4{font-size:12px;margin:0 0 5px;display:flex;align-items:center;gap:7px;flex-wrap:wrap}
.block h4 .kind{background:#8F702A;color:#fff;border-radius:5px;padding:2px 7px;font-size:10px;font-weight:600}
.set th{background:#F3F1EA;text-align:left;font-size:9.5px;color:#5A6270;padding:5px 8px;font-weight:600}
.set td{padding:5px 8px;border-bottom:1px solid #E6E2D6;vertical-align:top}
.set td.tab{width:58px;color:#5A6270;font-weight:600}
.set td:nth-child(2){width:172px;font-weight:600}
.code{font-family:Menlo,monospace;font-size:9.2px;line-height:1.5;background:#F3F1EA;border:1px solid #E6E2D6;border-radius:6px;padding:8px 10px;margin:6px 0 0;white-space:pre-wrap;word-break:break-word;color:#2a2f38}
h3.sub{font-size:13.5px;margin:16px 0 8px;padding-top:6px;border-top:1px dashed #D8D3C4;break-after:avoid}
.svc th{background:#1F2833;color:#fff;text-align:left;padding:6px 9px;font-size:10px}
.svc td{padding:6px 9px;border-bottom:1px solid #E6E2D6;vertical-align:top;font-size:10px}
.svc td.n{width:16px;color:#8F702A;font-weight:600}
.svc td:nth-child(2){width:128px}
.svc p{margin:3px 0;color:#5A6270}
.svc .li{display:block;margin-top:4px;color:#5A6270;font-size:9.2px}
.svc .wa{margin-top:4px;font-size:8.4px}
.svc .rev{display:inline-block;margin-top:3px;background:#E9E6DD;border-radius:4px;padding:1px 5px;font-size:8.8px;font-weight:600;color:#4a5462}
.faqt th{background:#F3F1EA;text-align:left;padding:6px 9px;font-size:10px;color:#5A6270}
.faqt td{padding:6px 9px;border-bottom:1px solid #E6E2D6;vertical-align:top}
.faqt td.k{width:22px;color:#8F702A;font-weight:600}
.faqt p{margin:3px 0 0;color:#5A6270}
.bio td{padding:6px 9px;border-bottom:1px solid #E6E2D6;vertical-align:top;font-size:10.2px}
.bio td.k{width:54px;color:#8F702A;font-weight:600;font-family:Menlo,monospace;font-size:9.2px}
.check td{padding:7px 9px;border-bottom:1px solid #E6E2D6;vertical-align:top}
.check td:first-child{width:20px;font-size:13px}
"""

doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Lumiere Dental Kota Warisan &middot; Elementor build steps</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>{''.join(pages)}</body></html>"""
open(OUT, 'w', encoding='utf-8').write(doc)
print('wrote', OUT, len(doc) // 1024, 'KB')
