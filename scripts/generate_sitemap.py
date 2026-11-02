"""
VEROLITE - Dynamic XML Sitemap Generator with Google Image Sitemap Extension
Fetches all published products from Sanity CMS Content Lake and generates sitemap.xml.
Can be executed anytime new products are published or updated in Sanity Studio.
"""

import urllib.request
import urllib.parse
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime, timezone

SANITY_PROJECT_ID = '5nckxq6b'
SANITY_DATASET = 'production'
BASE_URL = 'https://verolite.co.uk'

STATIC_PAGES = [
    {
        'loc': f'{BASE_URL}/',
        'priority': '1.0',
        'changefreq': 'weekly',
        'images': [
            {
                'loc': f'{BASE_URL}/logo.png',
                'title': 'VEROLITE Architectural Lighting - Luxury Commercial and Residential Lighting Systems'
            }
        ]
    },
    {
        'loc': f'{BASE_URL}/about.html',
        'priority': '0.8',
        'changefreq': 'monthly',
        'images': [
            {
                'loc': f'{BASE_URL}/assets/about/factory.jpg',
                'title': 'VEROLITE Architectural Lighting Engineering and Manufacturing'
            }
        ]
    },
    {
        'loc': f'{BASE_URL}/contact.html',
        'priority': '0.8',
        'changefreq': 'monthly',
        'images': []
    },
]

CATEGORY_PAGES = [
    {
        'file': 'recessed-led-down-lights.html',
        'title': 'Architectural Recessed LED Downlights - VEROLITE'
    },
    {
        'file': 'led-surface-down-lights.html',
        'title': 'Architectural LED Surface Mounted Downlights - VEROLITE'
    },
    {
        'file': '3phase-track-lights.html',
        'title': 'Commercial 3-Phase LED Track Lights - VEROLITE'
    },
    {
        'file': 'led-garden-lights.html',
        'title': 'Architectural LED Garden and Landscape Lights - VEROLITE'
    },
    {
        'file': 'led-strip-lights.html',
        'title': 'High-CRI Architectural LED Strip Lights - VEROLITE'
    },
    {
        'file': 'led-outdoor-flexible-neon-light.html',
        'title': 'IP67 Waterproof Outdoor Flexible LED Neon Light - VEROLITE'
    },
    {
        'file': 'led-magnetic-track-lights.html',
        'title': 'Ultra-Slim Low-Voltage Magnetic LED Track Light System - VEROLITE'
    },
    {
        'file': 'office-linear-lights.html',
        'title': 'Commercial Architectural Office Linear Lighting Systems - VEROLITE'
    },
    {
        'file': 'led-strip-light-drivers.html',
        'title': 'Constant Voltage LED Strip Light Power Supplies and Drivers - VEROLITE'
    },
    {
        'file': 'led-phase-cut-dimmer.html',
        'title': 'Precision Triac Phase Cut Dimmers for LED Fixtures - VEROLITE'
    },
    {
        'file': 'led-sensor-switches.html',
        'title': 'Intelligent Microwave and PIR LED Sensor Switches - VEROLITE'
    },
]

def fetch_published_products():
    """Queries all published products from Sanity Content Lake."""
    groq = urllib.parse.quote(
        '*[_type == "product" && !(_id in path("drafts.**")) && defined(slug.current) && noIndex != true]{'
        '  "title": title, '
        '  "slug": slug.current, '
        '  _updatedAt, '
        '  canonicalUrl, '
        '  "mainImageUrl": mainImage.asset->url, '
        '  "seoImageUrl": seoImage.asset->url'
        '} | order(slug asc)'
    )
    url = f"https://{SANITY_PROJECT_ID}.apicdn.sanity.io/v2023-08-01/data/query/{SANITY_DATASET}?query={groq}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Verolite Sitemap Generator)'})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        return data.get('result', [])

def generate_sitemap(output_path='sitemap.xml'):
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    
    # Root with standard sitemap and image extensions
    urlset = ET.Element('urlset', {
        'xmlns': 'http://www.sitemaps.org/schemas/sitemap/0.9',
        'xmlns:image': 'http://www.google.com/schemas/sitemap-image/1.1',
        'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        'xsi:schemaLocation': 'http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd'
    })

    # 1. Main Static Pages
    for page in STATIC_PAGES:
        url_el = ET.SubElement(urlset, 'url')
        ET.SubElement(url_el, 'loc').text = page['loc']
        ET.SubElement(url_el, 'lastmod').text = today
        ET.SubElement(url_el, 'changefreq').text = page['changefreq']
        ET.SubElement(url_el, 'priority').text = page['priority']
        for img in page.get('images', []):
            img_el = ET.SubElement(url_el, 'image:image')
            ET.SubElement(img_el, 'image:loc').text = img['loc']
            if img.get('title'):
                ET.SubElement(img_el, 'image:title').text = img['title']

    # 2. Category Pages
    for cat in CATEGORY_PAGES:
        url_el = ET.SubElement(urlset, 'url')
        ET.SubElement(url_el, 'loc').text = f"{BASE_URL}/{cat['file']}"
        ET.SubElement(url_el, 'lastmod').text = today
        ET.SubElement(url_el, 'changefreq').text = 'weekly'
        ET.SubElement(url_el, 'priority').text = '0.9'

    # 3. Product Pages from Sanity
    try:
        products = fetch_published_products()
        print(f"Fetched {len(products)} published products from Sanity CMS.")
        for prod in products:
            slug = prod.get('slug')
            if not slug:
                continue
            
            canonical = prod.get('canonicalUrl')
            loc = canonical.strip() if canonical and canonical.strip() else f"{BASE_URL}/product.html?slug={urllib.parse.quote(slug)}"
            
            updated_at = prod.get('_updatedAt')
            lastmod = updated_at[:10] if updated_at and len(updated_at) >= 10 else today

            url_el = ET.SubElement(urlset, 'url')
            ET.SubElement(url_el, 'loc').text = loc
            ET.SubElement(url_el, 'lastmod').text = lastmod
            ET.SubElement(url_el, 'changefreq').text = 'weekly'
            ET.SubElement(url_el, 'priority').text = '0.8'

            # Product Image (main or custom SEO image)
            img_url = prod.get('seoImageUrl') or prod.get('mainImageUrl')
            if img_url:
                img_el = ET.SubElement(url_el, 'image:image')
                ET.SubElement(img_el, 'image:loc').text = img_url
                prod_title = prod.get('title') or slug.replace('-', ' ').title()
                ET.SubElement(img_el, 'image:title').text = f"{prod_title} - VEROLITE Architectural Lighting"
    except Exception as err:
        print(f"Warning: Could not fetch products from Sanity: {err}")

    # Pretty print XML
    xml_str = ET.tostring(urlset, encoding='utf-8')
    parsed = minidom.parseString(xml_str)
    pretty_xml = parsed.toprettyxml(indent="  ", encoding="UTF-8").decode('utf-8')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(pretty_xml)

    print(f"Successfully generated {output_path} with total {len(urlset)} URLs.")

if __name__ == '__main__':
    generate_sitemap('sitemap.xml')
