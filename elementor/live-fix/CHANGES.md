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
