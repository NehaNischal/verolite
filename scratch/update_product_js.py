import re

# 1. Update product.js
with open(r'c:\Users\user\Desktop\verolite\product.js', 'r', encoding='utf-8') as f:
    pjs = f.read()

fallback_code = '''    const FALLBACK_EMERGENCY_PRODUCT = {
        name: 'Emergency Exit Sign',
        model: 'VER-EMG-01',
        slug: { current: 'emergency-exit-sign' },
        category: 'emergency-lights',
        shortDescription: 'Architectural LED emergency exit sign with long-life LiFePO4 battery backup, crisp laser-etched green pictogram panels, and ISO 7010 compliance.',
        description: 'Engineered specifically for safety-critical architectural and commercial environments, the VEROLITE Emergency Exit Sign delivers instant, dependable illumination during emergency power failures. Constructed with a precision anodised aluminium housing and crystal-clear high-efficiency optical acrylic diffuser, it ensures maximum visibility and legibility up to 24 metres. Fully certified to BS EN 60598-2-22, BS 5266-1, and ISO 7010 international standards.',
        mainImageUrl: 'images/emergency-hero-banner.jpg',
        features: [
            'Ultra-reliable high-efficiency LED light source with 50,000+ hour operational lifespan',
            'Maintained and non-maintained operation modes selectable via onboard DIP switch',
            'Integrated 3-hour emergency battery backup with self-testing diagnostics',
            'Surface wall, ceiling, or semi-recessed mounting options included',
            'ISO 7010 and BS EN 1838 compliant optical pictogram panel (Running Man with Arrow)',
            'Robust IP42 rated aluminium architectural body with anti-corrosion finish'
        ],
        specifications: [
            { label: 'Type', value: 'Architectural LED Emergency Exit Luminaire' },
            { label: 'Emergency Duration', value: '3 Hours' },
            { label: 'Mode of Operation', value: 'Maintained / Non-Maintained Selectable' },
            { label: 'Input Voltage', value: 'AC 220-240V, 50/60Hz' },
            { label: 'Battery Type', value: 'LiFePO4 3.2V 1500mAh High Temperature' },
            { label: 'Viewing Distance', value: '24 Metres (ISO 7010)' },
            { label: 'Housing Material', value: 'Anodised Aluminium + Optical Grade Acrylic' },
            { label: 'IP Rating', value: 'IP42' },
            { label: 'Compliance Standards', value: 'BS EN 60598-2-22, BS 5266-1, ISO 7010' }
        ],
        variantHeaders: {
            col1: 'Model',
            col2: 'Wattage',
            col3: 'Direction',
            col4: 'Finish',
            col5: 'Mounting',
            col6: 'Emergency Duration'
        },
        variants: [
            { model: 'VER-EMG-01-D', wattage: '3W', cct: 'Arrow Down (Exit)', body: 'Silver Anodised Aluminium', size: 'Wall / Ceiling Surface', cutOut: '3 Hours LiFePO4' },
            { model: 'VER-EMG-01-L', wattage: '3W', cct: 'Arrow Left', body: 'Silver Anodised Aluminium', size: 'Wall / Ceiling Surface', cutOut: '3 Hours LiFePO4' },
            { model: 'VER-EMG-01-R', wattage: '3W', cct: 'Arrow Right', body: 'Silver Anodised Aluminium', size: 'Wall / Ceiling Surface', cutOut: '3 Hours LiFePO4' }
        ]
    };

    // Initialize on DOM ready'''

pjs = pjs.replace('    // Initialize on DOM ready', fallback_code)

target_fetch = '''        try {
            const product = await fetchSanityProduct(slug);
            renderProduct(product);
        } catch (err) {
            console.error('Error fetching product from Sanity:', err);
            renderProduct(null);
        }'''

replacement_fetch = '''        try {
            let product = await fetchSanityProduct(slug);
            if (!product && (slug === 'emergency-exit-sign' || slug === 'emergency-lights')) {
                product = FALLBACK_EMERGENCY_PRODUCT;
            }
            renderProduct(product);
        } catch (err) {
            console.error('Error fetching product from Sanity:', err);
            if (slug === 'emergency-exit-sign' || slug === 'emergency-lights') {
                renderProduct(FALLBACK_EMERGENCY_PRODUCT);
            } else {
                renderProduct(null);
            }
        }'''

pjs = pjs.replace(target_fetch, replacement_fetch)

with open(r'c:\Users\user\Desktop\verolite\product.js', 'w', encoding='utf-8') as f:
    f.write(pjs)

print("product.js updated")
