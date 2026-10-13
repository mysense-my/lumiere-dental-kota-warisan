# Kota Warisan landing page — destination URLs for ads

All nine sections have a working anchor. Clicking the nav now writes the
section into the address bar, so you can navigate to the part you want and
copy the URL straight out of the browser.

Base page: `https://www.lumieredental.com.my/kota-warisan/`

| Section | Destination URL | What the visitor lands on |
|---|---|---|
| Top of page | `https://www.lumieredental.com.my/kota-warisan/` | Hero + Book An Appointment |
| Insurance panels | `https://www.lumieredental.com.my/kota-warisan/#panels` | AIA, PMCare, Mednefits, HealthMetrics, MedKad |
| About | `https://www.lumieredental.com.my/kota-warisan/#about` | Why Lumiere + Dr Tan's bio |
| Treatments | `https://www.lumieredental.com.my/kota-warisan/#services` | All 8 treatments |
| Clinic | `https://www.lumieredental.com.my/kota-warisan/#facilities` | Clinic photos |
| How it works | `https://www.lumieredental.com.my/kota-warisan/#how` | 3-step process |
| Reviews | `https://www.lumieredental.com.my/kota-warisan/#reviews` | Patient reviews, 5.0 Google rating |
| FAQ | `https://www.lumieredental.com.my/kota-warisan/#faq` | 6 common questions |
| Contact | `https://www.lumieredental.com.my/kota-warisan/#contact` | Hours, phone, map, WhatsApp |

## Using these in Google Ads

Put the URL above in **Final URL**. Tracking parameters go on as normal and
are preserved — the fragment sits after the query string:

    https://www.lumieredental.com.my/kota-warisan/?utm_source=google&utm_medium=cpc&utm_campaign=kw_brand#services

Verified end to end: `gclid` and all `utm_*` parameters survive both a direct
load and every in-page nav click, so conversion tracking is unaffected.

## Suggested pairing

| Ad theme | Send to |
|---|---|
| "Dental pain / emergency" | base URL (hero CTA) |
| Braces / Invisalign / implants / whitening | `#services` |
| "Panel clinic", insurance-led ads | `#panels` |
| Trust / credibility ads | `#reviews` |
| "Where are you / opening hours" | `#contact` |

## Note

Only the page's own sections are linkable this way — this is a single landing
page, not separate pages per treatment. If you want a genuinely separate URL
per treatment (e.g. `/kota-warisan/braces/`) for tighter Quality Score and
per-treatment conversion tracking, that is a different build and worth
discussing before anyone starts.
