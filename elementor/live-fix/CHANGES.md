# Kota Warisan landing page - live fixes

Page 4281 on lumieredental.com.my. Three kinds of change were made.

## 1. Page template - the landing page is now standalone

The page was on `page-template-default`, so it pulled the **site-wide**
Elementor Theme Builder header (template **100**) and footer (template **141**) -
the same ones the homepage and /contact/ use. It is now on **Elementor Canvas**,
which suppresses both on this page only.

Templates 100 and 141 were NOT edited or deleted. Other pages are unaffected.

The landing page's own header and footer are `header-widget.html` and
`footer-widget.html` in this folder, added as two HTML widgets: the first and
last containers on the page (`#lm-header`, `#lm-footer`). They reproduce the
mockup's fixed transparent nav (which turns cream on scroll), the burger drawer
under 1024px, and the four-column footer.

## 2. Container settings changed in Elementor (not CSS)

The mockup's content column is **1190px** wide. Elementor puts section padding
*outside* the boxed inner, so `Boxed 1250 + 30px padding` gives a 1250 inner -
60px wider than the mockup, which cascaded into every card. All content
sections are now **Boxed 1190**.

Also fixed: `panels` and `about` had **Width 105.878%** and **104.997%** set on
them, which pushed content past both edges of the viewport; `about`,
the doctor block and the stats row were **Full width with 10px padding**
instead of boxed. These are why the team photo bled off the left edge.

| Section | was | now |
|---|---|---|
| panels, about | Full, width 105/105% | Boxed 1190, pad 90/30/40/30 |
| doctor block, stats | Full / boxed 100%, pad 10 | Boxed 1190, pad 0/30/40/30 |
| facilities, reviews | Boxed, no padding | Boxed 1190, pad 90/30/40/30 |
| services, how, faq, contact | Boxed 1250 | Boxed 1190 |

## 3. Content fixes

- Service card 1 used `p110.png` (an unrelated 2024 upload). Now `general.png`.
- "clinicalorthodontics" -> "clinical orthodontics"
- "handled atthe front desk" -> "handled at the front desk"
- "WhatsAppUs" -> "WhatsApp Us"
- "Meet Your Dentist" eyebrow was 16px; every other eyebrow is 15px.

## Verified

At 1440x900 against the mockup: all 20 images match size and ratio
(service photos 531x398, team photo 522x391, pill icons 26x26), 121 matched
text nodes with no style differences, content column 1190 at L125.
Sticky card stack works at 1440, 390x844, 375x667 and 360x640.

---

# Round 2 — 12 Oct 2026

## 1. "Why Lumiere" cards wrapped 3 + 1

The four cards had a fixed **286.64px** width, sized for the wider
container the page used before the Boxed-1190 change. In the 1170px tray:

    4 x 286.64 + 3 x 9px gap = 1174px  ->  4px too wide

so the fourth card wrapped onto its own row. Section 12 of the CSS lets the
cards divide the row instead (`flex:1 1 0`), giving the mockup's ~285px each.
Scoped to `min-width:1025px`, so tablet (2x2) and phone (stacked) are untouched.

Cards 2, 3 and 4 also had padding `26/22/26/22` where card 1 and the mockup
use `28/26/30/26`. All four now match.

## 2. Images converted to WebP

All 26 non-WebP images on the page were converted and re-pointed.

| | before | after |
|---|---|---|
| Served image weight | 3.90 MB | **1.61 MB** |

**2.29 MB saved (58.7%).** Biggest wins: `hero-lobby` 637→222 KB,
`team-neon` 528→260 KB, `neon-wall` 391→156 KB.

- Photos: quality 82 (RMSE 1.5–3.5 — not visually distinguishable).
- Icons and logos: **lossless**, verified pixel-identical in every visible
  pixel with alpha preserved.
- Originals were left in the media library, so this is reversible.
- Source files: `elementor/webp/`.

Done by direct conversion (Pillow) + re-upload, NOT via LiteSpeed's optimizer —
that needs a QUIC.cloud account link and reported a quota of 0 images.

**Deliberately left as PNG** (they are site-wide, not page content, and should
not be WebP): `Retina-Logo-2.png` (Rank Math JSON-LD schema logo) and
`logo-300x300.png` (apple-touch-icon / MS tile).

### If you want this automatic for future uploads
Link the site to QUIC.cloud and turn on LiteSpeed Cache > Image Optimization.
That needs an account, so it is your call — it also means images are sent to
QUIC.cloud for conversion.

---

# Round 3 — 13 Oct 2026

## Nav clicks now show the section in the address bar

**Symptom:** clicking Home / About / Services / … scrolled to the right place
but the URL never changed, so there was nothing to copy as an ad destination.

**Cause:** ElementsKit binds a delegated jQuery handler to `a[href*="#"]` that
smooth-scrolls the page but never writes `location.hash`.

**Fix:** a small `lm-hash-sync` block at the end of the header widget's script.
It listens for clicks on any in-page `#` link and, after the scroll handler has
run, pushes the fragment onto the URL with `history.pushState`, keeping the
existing path and query string. `pushState` does not scroll, so the smooth
scroll is untouched, and Back still steps through the sections.

It skips `#elementor-action` links (lightboxes) and any `#` target that does not
exist on the page.

**Verified** — nav, mobile drawer, hero buttons and footer links all write the
fragment; all nine anchors land on the right section; `gclid` and `utm_*`
parameters survive both a direct load and every in-page click; Back works.

Destination URLs for the ads team: **AD-LINKS.md**.
