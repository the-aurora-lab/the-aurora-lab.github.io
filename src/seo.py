"""schema.org data for the tools pages (search engines read it; nothing is shown on the page).

Each tools generator calls software_ld() and puts the result in its <head>. Offers are the real store prices; no
ratings or reviews are claimed (there are none yet).
"""
import json

SITE = "https://the-aurora-lab.github.io/"

OFFERS = {  # tool -> [(name, price in USD)]; keep equal to the STORES / prices on each page
    "reference-verifier": [("Free core (MIT, PyPI)", "0"), ("Pro, personal", "24"), ("Pro, course", "99"),
                           ("Pro, lab", "149")],
    "paper-radar": [("Personal", "19")],
    "research-starter-kit": [("Pay what you want ($5 suggested)", "0")],
    "every-comment-answered": [("Personal", "19")],
    "local-transcripts": [("Personal", "29"), ("Lab (5 people)", "99")],
}


def software_ld(tool: str, title: str, description: str) -> str:
    url = f"{SITE}tools/{tool}/"
    data = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": title.split(":")[0].strip(),
        "alternateName": title,
        "description": description,
        "url": url,
        "image": f"{SITE}assets/img/{tool}.png",
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "macOS, Linux, Windows",
        "softwareRequirements": "Python 3",
        "publisher": {"@type": "Organization", "name": "Aurora Lab", "url": SITE},
        "offers": [{"@type": "Offer", "name": n, "price": p, "priceCurrency": "USD", "url": url}
                   for n, p in OFFERS[tool]],
    }
    body = json.dumps(data, ensure_ascii=False, indent=None, separators=(", ", ": ")).replace("</", "<\\/")
    return f'<script type="application/ld+json">{body}</script>'
