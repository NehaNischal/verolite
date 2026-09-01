// Continuous Seamless Infinite Carousel & Animations for Verolite
document.addEventListener('DOMContentLoaded', () => {
    // Ensure Hero Video loads and plays fresh stream
    const heroVideo = document.querySelector('.hero-bg-video');
    if (heroVideo) {
        heroVideo.load();
        heroVideo.play().catch(() => {});
    }

    // Initialize Universal Letter-by-Letter Entrance Animation
    initLetterCascadeAnimation();

    // Initialize Product Cards Scroll Entrance Animation
    initProductCardScrollAnimations();

    // About Us Scroll Reveal & Letter Cascade
    const aboutSection = document.querySelector('.about-section');
    if (aboutSection) {
        const splitElements = aboutSection.querySelectorAll('.split-letters');
        splitElements.forEach((el, elIndex) => {
            const text = el.textContent.trim();
            el.innerHTML = '';
            const startDelay = 250 + (elIndex * 280);
            [...text].forEach((char, charIndex) => {
                const span = document.createElement('span');
                span.className = 'char';
                if (char === ' ') {
                    span.classList.add('space');
                    span.innerHTML = '&nbsp;';
                } else {
                    span.textContent = char;
                }
                const letterDelay = startDelay + (charIndex * 32);
                span.style.transitionDelay = `${letterDelay}ms`;
                el.appendChild(span);
            });
        });

        const observerOptions = { threshold: 0.15, rootMargin: '0px 0px -40px 0px' };
        const aboutObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    aboutSection.classList.add('is-visible');
                    const animItems = aboutSection.querySelectorAll('.animate-item');
                    animItems.forEach(item => {
                        const delay = item.getAttribute('data-delay') || '0';
                        item.style.transitionDelay = `${delay}ms`;
                    });
                    aboutObserver.unobserve(aboutSection);
                }
            });
        }, observerOptions);
        aboutObserver.observe(aboutSection);
    }

    // Initialize Recessed Downlights Page if active
    initRecessedMarqueePage();

    // Dynamically synchronize Sanity products into existing category grid layouts
    initCategorySanityProducts();
});

// Sync Sanity Products into Category Listing Grids without altering layout
function initCategorySanityProducts() {
    const grid = document.querySelector('.ref-products-grid');
    if (!grid) return;

    // Detect current category from page filename
    const path = window.location.pathname.toLowerCase();
    const filename = path.split('/').pop().replace('.html', '') || '';

    const categoryMap = {
        'recessed-led-down-lights': 'recessed-led-down-lights',
        'led-surface-down-lights': 'led-surface-down-lights',
        '3phase-track-lights': '3phase-track-lights',
        'led-garden-lights': 'led-garden-lights',
        'led-strip-lights': 'led-strip-lights',
        'led-outdoor-flexible-neon-light': 'led-outdoor-flexible-neon-light',
        'led-magnetic-track-lights': 'led-magnetic-track-lights',
        'office-linear-lights': 'office-linear-lights',
        'led-strip-light-drivers': 'led-strip-light-drivers',
        'led-phase-cut-dimmer': 'led-phase-cut-dimmer',
        'led-sensor-switches': 'led-sensor-switches',
    };

    const currentCat = categoryMap[filename];
    if (!currentCat) return;

    const SANITY_PROJECT_ID = '5nckxq6b';
    const SANITY_DATASET = 'production';
    const groq = encodeURIComponent(`*[_type == "product" && (category == "${currentCat}" || category == "${filename}") && !(name match "*test*") && !(name match "*TEST*") && !(name match "*Sample*")]{
        _id,
        name,
        model,
        "slug": slug.current,
        "imageUrl": mainImage.asset->url,
        category
    }`);

    const endpoint = `https://${SANITY_PROJECT_ID}.apicdn.sanity.io/v2023-08-01/data/query/${SANITY_DATASET}?query=${groq}`;

    fetch(endpoint)
        .then(res => res.json())
        .then(data => {
            if (!data.result || !data.result.length) return;

            // Existing product names in grid to prevent duplication
            const existingNames = Array.from(grid.querySelectorAll('.ref-card .name'))
                .map(el => el.textContent.trim().toLowerCase());

            data.result.forEach(prod => {
                const prodName = prod.name || prod.model || 'Luminaire';
                if (
                    prodName.toLowerCase().includes('test') || 
                    prodName.toLowerCase().includes('sample') ||
                    (prod.slug && prod.slug.toLowerCase().includes('sample')) ||
                    (prod.model && prod.model.toLowerCase().includes('test')) ||
                    prod._id === '0be29e83-8e27-4eb0-abc2-722a6d48fe47' ||
                    existingNames.includes(prodName.toLowerCase())
                ) return;

                const slug = prod.slug || prodName.toLowerCase().replace(/[^a-z0-9]+/g, '-');
                const imgUrl = prod.imageUrl || 'images/recessed/oliv.jpg';
                const modelBadge = prod.model ? prod.model : 'VEROLITE';

                const card = document.createElement('a');
                card.href = `product.html?slug=${encodeURIComponent(slug)}`;
                card.className = 'ref-card ref-card-visible';
                card.innerHTML = `
                    <div class="ref-card-img-box">
                        <img src="${imgUrl}" alt="${prodName}" loading="lazy">
                    </div>
                    <div class="ref-card-info">
                        <div class="ref-card-title">
                            <span class="prefix">${modelBadge}</span>
                            <span class="name">${prodName}</span>
                        </div>
                        <div class="ref-card-link">
                            <span class="link-text">View Luminaire</span>
                            <span class="link-arrow">&rarr;</span>
                        </div>
                    </div>
                `;
                grid.appendChild(card);
            });
        })
        .catch(err => {
            // Silently maintain existing static layout if offline or error
            console.debug('Sanity category sync skipped:', err);
        });
}

// Universal Letter-by-Letter Entrance Animation
function initLetterCascadeAnimation() {
    const titleSelectors = [
        '.hero-title',
        '.outdoor-hero-main-title',
        '.recessed-hero-main-title',
        '.surface-page-title',
        '.garden-page-title',
        '.about-page-title',
        '.ref-main-title'
    ];

    titleSelectors.forEach(selector => {
        const elements = document.querySelectorAll(selector);
        elements.forEach(el => {
            if (el.dataset.animatedLetters) return;
            el.dataset.animatedLetters = 'true';

            const childNodes = Array.from(el.childNodes);
            el.innerHTML = '';

            let charCounter = 0;
            let isLineStart = true;

            childNodes.forEach(node => {
                if (node.nodeType === Node.ELEMENT_NODE && node.tagName === 'BR') {
                    el.appendChild(document.createElement('br'));
                    isLineStart = true;
                } else if (node.nodeType === Node.TEXT_NODE || node.nodeType === Node.ELEMENT_NODE) {
                    let text = node.textContent;
                    if (isLineStart) {
                        text = text.replace(/^\s+/, '');
                    }
                    if (!text) return;

                    const parts = text.split(/(\s+)/);
                    parts.forEach(part => {
                        if (/^\s+$/.test(part)) {
                            if (!isLineStart) {
                                const spaceSpan = document.createElement('span');
                                spaceSpan.className = 'letter-char space';
                                spaceSpan.innerHTML = '&nbsp;';
                                el.appendChild(spaceSpan);
                            }
                        } else if (part.length > 0) {
                            isLineStart = false;
                            const wordSpan = document.createElement('span');
                            wordSpan.className = 'letter-word';
                            wordSpan.style.display = 'inline-block';
                            wordSpan.style.whiteSpace = 'nowrap';
                            [...part].forEach(char => {
                                const span = document.createElement('span');
                                span.className = 'letter-char';
                                span.textContent = char;
                                span.style.transitionDelay = `${140 + (charCounter * 85)}ms`;
                                wordSpan.appendChild(span);
                                charCounter++;
                            });
                            el.appendChild(wordSpan);
                        }
                    });
                }
            });

            requestAnimationFrame(() => {
                setTimeout(() => {
                    el.classList.add('letters-animated');
                    const heroContent = el.closest('.hero-content') || document.querySelector('.hero-content');
                    if (heroContent) {
                        heroContent.classList.add('hero-loaded');
                    }
                }, 60);
            });
        });
    });
}

// Universal Staggered Product Cards Scroll Entrance Animation
function initProductCardScrollAnimations() {
    const cards = document.querySelectorAll('.ref-card, .lumi-card, .collection-card');
    if (!cards.length) return;

    const cardObserverOptions = {
        root: null,
        rootMargin: '0px 0px -40px 0px',
        threshold: 0.08
    };

    const cardObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                const card = entry.target;
                const parent = card.parentElement;
                const siblings = Array.from(parent ? parent.children : []);
                const index = siblings.indexOf(card);
                const delay = ((index >= 0 ? index : 0) % 5) * 75;
                card.style.transitionDelay = `${delay}ms`;
                card.classList.add('ref-card-visible');
                cardObserver.unobserve(card);
            }
        });
    }, cardObserverOptions);

    cards.forEach(card => {
        cardObserver.observe(card);
    });

    // Enable seamless click navigation to the reusable product template
    document.querySelectorAll('.ref-card').forEach(card => {
        if (card.tagName !== 'A' && !card.closest('a')) {
            card.style.cursor = 'pointer';
            card.addEventListener('click', (e) => {
                if (e.target.closest('a') || e.target.tagName === 'A') return;
                const nameEl = card.querySelector('.name');
                if (nameEl && nameEl.textContent.trim()) {
                    const slug = nameEl.textContent.trim().toLowerCase().replace(/[^a-z0-9]+/g, '-');
                    window.location.href = `product.html?slug=${encodeURIComponent(slug)}`;
                }
            });
        }
    });
}

// ==========================================================================
// Recessed LED Down Lights Collection Data (16 Products)
// ==========================================================================================
const RECESSED_PRODUCTS = [
    {
        id: 'oliv',
        name: 'OLIV',
        subtitle: 'Deep Baffle Round Anti-Glare Downlight',
        category: 'round',
        categoryLabel: 'ROUND SINGLE-HEAD ARCHITECTURAL',
        image: 'images/recessed/oliv.jpg',
        badge: 'MODEL: OLIV',
        desc: 'Deep-set architectural reflector providing UGR < 19 glare control, optimal for luxury residential and hospitality environments. Features die-cast aluminium heatsink body and high CRI > 95 COB light engine.',
        cutout: 'Ø 75 mm',
        wattage: '7W / 12W / 15W',
        lumens: '750 lm – 1500 lm',
        beam: '15° Spot / 24° Medium / 38° Flood',
        cct: '2700K / 3000K / 4000K',
        cri: 'Ra > 95 / R9 > 80',
        ip: 'IP44 Splash Resistant',
        highlights: [
            'CRI > 95 / R9 > 80 true color rendering',
            'Deep Baffle Optics (UGR < 19 anti-glare)',
            '50,000+ Hours L80B10 rated lifespan',
            'Triac / Phase / DALI dimming compatible'
        ]
    },
    {
        id: 'niko',
        name: 'NIKO',
        subtitle: 'Ultra-Slim Architectural Recessed Spotlight',
        category: 'round',
        categoryLabel: 'ROUND SINGLE-HEAD ARCHITECTURAL',
        image: 'images/recessed/niko.jpg',
        badge: 'MODEL: NIKO',
        desc: 'Minimalist rim design with ultra-compact heatsink depth, tailored for low-plenum shallow ceiling installations requiring maximum lumens from a subtle aperture.',
        cutout: 'Ø 70 mm',
        wattage: '7W / 10W',
        lumens: '700 lm – 1050 lm',
        beam: '24° Medium / 36° Wide Flood',
        cct: '3000K / 4000K Neutral White',
        cri: 'Ra > 95 / R9 > 80',
        ip: 'IP40 Dust Resistant',
        highlights: [
            'Ultra-shallow mounting profile (< 55mm depth)',
            'High efficiency specular faceted reflector',
            'Solid die-cast aluminium housing',
            'Low thermal degradation engine'
        ]
    },
    {
        id: 'raza',
        name: 'RAZA',
        subtitle: 'Fully Adjustable Gimbal Recessed Downlight',
        category: 'round',
        categoryLabel: 'ROUND SINGLE-HEAD ARCHITECTURAL',
        image: 'images/recessed/raza.jpg',
        badge: 'MODEL: RAZA',
        desc: '360° horizontal rotation and 30° vertical tilt gimbal mechanism for precision accent illumination of artwork, sculptures, and architectural feature walls.',
        cutout: 'Ø 85 mm',
        wattage: '10W / 15W',
        lumens: '950 lm – 1550 lm',
        beam: '15° Spot / 24° Medium / 36° Flood',
        cct: '2700K / 3000K / 4000K',
        cri: 'Ra > 95 / R9 > 80',
        ip: 'IP20 Accent Rated',
        highlights: [
            '360° rotation & 30° smooth tilt action',
            'Zero beam distort gimbal suspension',
            'Ideal for gallery & feature lighting',
            'Precision optical lens system'
        ]
    },
    {
        id: 'kia',
        name: 'KIA',
        subtitle: 'Square Architectural Low-Glare Luminaire',
        category: 'square',
        categoryLabel: 'SQUARE SINGLE-HEAD ARCHITECTURAL',
        image: 'images/recessed/kia.jpg',
        badge: 'MODEL: KIA',
        desc: 'Clean geometric square bezel with micro-baffle optical reflector for crisp square ceiling layouts. Perfect for modern residential and corporate interiors.',
        cutout: '75 x 75 mm',
        wattage: '9W / 12W',
        lumens: '850 lm – 1250 lm',
        beam: '24° Medium / 38° Flood',
        cct: '3000K / 4000K',
        cri: 'Ra > 95 / R9 > 80',
        ip: 'IP44 Splash Resistant',
        highlights: [
            'Precision square die-cast bezel',
            'Anti-glare square reflector cone',
            'Seamless ceiling alignment frame',
            'Osram COB chip technology'
        ]
    },
    {
        id: 'luxa',
        name: 'LUXA',
        subtitle: 'Premium Darklight Anti-Glare Downlight',
        category: 'round',
        categoryLabel: 'ROUND SINGLE-HEAD ARCHITECTURAL',
        image: 'images/recessed/luxa.jpg',
        badge: 'MODEL: LUXA',
        desc: 'Darklight optical chamber hides the light source from direct visual field, achieving ultra-pure illumination with zero visual noise and supreme visual comfort.',
        cutout: 'Ø 90 mm',
        wattage: '12W / 18W',
        lumens: '1200 lm – 1850 lm',
        beam: '15° Spot / 24° Medium / 45° Wide',
        cct: '2700K / 3000K / 4000K',
        cri: 'Ra > 95 / R9 > 80',
        ip: 'IP44 Darklight',
        highlights: [
            'Invisible light source architecture',
            'UGR < 16 superior anti-glare rating',
            'Heavy-duty cooling fins for longevity',
            'Phase & DALI dimming options'
        ]
    },
    {
        id: 'vexo',
        name: 'VEXO',
        subtitle: 'High-Efficiency Architectural COB Downlight',
        category: 'round',
        categoryLabel: 'ROUND SINGLE-HEAD ARCHITECTURAL',
        image: 'images/recessed/vexo.jpg',
        badge: 'MODEL: VEXO',
        desc: 'High output COB LED engine with heavy-duty radial aluminium heat spreader designed for high-ceiling retail displays, car showrooms, and commercial lobbies.',
        cutout: 'Ø 95 mm',
        wattage: '15W / 20W / 25W',
        lumens: '1650 lm – 2600 lm',
        beam: '24° Medium / 36° Flood / 60° Wide',
        cct: '3000K / 4000K / 5000K',
        cri: 'Ra > 90 / R9 > 60',
        ip: 'IP44 High Lumens',
        highlights: [
            'Up to 2600 lm high lumen package',
            'Radial passive cooling heat engine',
            'High ceiling illumination capability',
            'Commercial grade longevity'
        ]
    },
    {
        id: 'talon',
        name: 'TALON',
        subtitle: 'Trimless Plaster-In Architectural Spotlight',
        category: 'round',
        categoryLabel: 'ROUND SINGLE-HEAD ARCHITECTURAL',
        image: 'images/recessed/talon.jpg',
        badge: 'MODEL: TALON',
        desc: 'Seamless plaster-in mounting frame creates a completely rimless transition into ceiling plasterboard for sleek minimalist architectural interiors.',
        cutout: 'Ø 80 mm',
        wattage: '8W / 12W',
        lumens: '800 lm – 1300 lm',
        beam: '15° Spot / 24° Medium / 36° Flood',
        cct: '2700K / 3000K / 4000K',
        cri: 'Ra > 95 / R9 > 80',
        ip: 'IP20 Trimless',
        highlights: [
            '100% frameless plaster-in mounting',
            'Flush ceiling aesthetic integration',
            'Deep recessed anti-glare module',
            'Easy push-click maintenance'
        ]
    },
    {
        id: 'orbit',
        name: 'ORBIT',
        subtitle: 'Precision Reflector Architectural Downlight',
        category: 'round',
        categoryLabel: 'ROUND SINGLE-HEAD ARCHITECTURAL',
        image: 'images/recessed/orbit.jpg',
        badge: 'MODEL: ORBIT',
        desc: 'Core flagship series featuring interchangeable faceted specular reflectors, magnetic twist-lock bezel trims, and ultra-high CRI light output.',
        cutout: 'Ø 75 mm',
        wattage: '7W / 10W / 14W',
        lumens: '750 lm – 1450 lm',
        beam: '15° Spot / 24° Medium / 36° Flood',
        cct: '2700K / 3000K / 4000K',
        cri: 'Ra > 95 / R9 > 80',
        ip: 'IP44 Flagship',
        highlights: [
            'Interchangeable precision optical cone',
            'Magnetic quick-connect front bezel',
            'Versatile 7W to 14W output range',
            'Luxury residential & hotel grade'
        ]
    },
    {
        id: 'orbit-s',
        name: 'ORBIT-S',
        subtitle: 'Square Single-Head Architectural Downlight',
        category: 'square',
        categoryLabel: 'SQUARE SINGLE-HEAD ARCHITECTURAL',
        image: 'images/recessed/orbit-s.jpg',
        badge: 'MODEL: ORBIT-S',
        desc: 'Square single-head variant of the Orbit modular engine with flush die-cast aluminium casing and precision square aperture control.',
        cutout: '75 x 75 mm',
        wattage: '7W / 10W / 14W',
        lumens: '750 lm – 1450 lm',
        beam: '15° Spot / 24° Medium / 36° Flood',
        cct: '2700K / 3000K / 4000K',
        cri: 'Ra > 95 / R9 > 80',
        ip: 'IP44 Flagship Square',
        highlights: [
            'Modular Orbit light engine core',
            'Die-cast square powder-coated rim',
            'Deep reflector glare elimination',
            'Phase cut & DALI compatible'
        ]
    },
    {
        id: 'orbit-2',
        name: 'ORBIT-2',
        subtitle: 'Double-Head Linear Recessed Spotlight Module',
        category: 'multi',
        categoryLabel: 'MULTI-HEAD LINEAR GRID',
        image: 'images/recessed/orbit-2.jpg',
        badge: 'MODEL: ORBIT-2',
        desc: 'Twin independently adjustable cardan spotlight modules housed in a sleek linear rectangular enclosure for flexible dual-beam directional lighting.',
        cutout: '145 x 75 mm',
        wattage: '2 x 7W / 2 x 10W (14W – 20W total)',
        lumens: '1500 lm – 2100 lm',
        beam: '15° Spot / 24° Medium / 36° Flood',
        cct: '2700K / 3000K / 4000K',
        cri: 'Ra > 95 / R9 > 80',
        ip: 'IP20 Dual Head',
        highlights: [
            'Dual independent multi-directional heads',
            'Architectural rectangular ceiling cutout',
            'High output 2100 lm combined capacity',
            'Perfect for corridors & focal walls'
        ]
    },
    {
        id: 'orbit-3',
        name: 'ORBIT-3',
        subtitle: 'Triple-Head Linear Recessed Spotlight Grid',
        category: 'multi',
        categoryLabel: 'MULTI-HEAD LINEAR GRID',
        image: 'images/recessed/orbit-3.jpg',
        badge: 'MODEL: ORBIT-3',
        desc: 'Three-head linear grid spotlight for high-end retail display galleries, executive boardrooms, and expansive focal wall accent lighting.',
        cutout: '215 x 75 mm',
        wattage: '3 x 7W / 3 x 10W (21W – 30W total)',
        lumens: '2250 lm – 3150 lm',
        beam: '15° Spot / 24° Medium / 36° Flood',
        cct: '2700K / 3000K / 4000K',
        cri: 'Ra > 95 / R9 > 80',
        ip: 'IP20 Triple Head',
        highlights: [
            'Triple independent adjustable optics',
            'Up to 3150 lm combined luminous flux',
            'Linear architectural lighting grid',
            'Gallery & exhibition display standard'
        ]
    },
    {
        id: 'tera',
        name: 'TERA',
        subtitle: 'Commercial High-Lumen Architectural Luminaire',
        category: 'round',
        categoryLabel: 'ROUND SINGLE-HEAD ARCHITECTURAL',
        image: 'images/recessed/tera.jpg',
        badge: 'MODEL: TERA',
        desc: 'Heavy-duty commercial downlight with deep passive cooling heat sink and high efficiency flicker-free driver for large public spaces and atrium ceilings.',
        cutout: 'Ø 150 mm',
        wattage: '25W / 35W / 45W',
        lumens: '2800 lm – 4800 lm',
        beam: '30° Medium / 60° Wide / 80° Extra Wide',
        cct: '3000K / 4000K / 5000K',
        cri: 'Ra > 90 / R9 > 60',
        ip: 'IP44 Commercial',
        highlights: [
            'Ultra high output up to 4800 lm',
            '150mm wide aperture commercial frame',
            'Flicker-free IEEE 1789 compliant driver',
            'DALI & 0-10V dimming ready'
        ]
    },
    {
        id: 'syro',
        name: 'SYRO',
        subtitle: 'Soft-Baffle Ultra-Low Glare Downlight',
        category: 'round',
        categoryLabel: 'ROUND SINGLE-HEAD ARCHITECTURAL',
        image: 'images/recessed/syro.jpg',
        badge: 'MODEL: SYRO',
        desc: 'Parabolic curved soft baffle profile directing light downwards while preserving complete visual comfort (UGR < 16) for executive office suites and luxury bedrooms.',
        cutout: 'Ø 85 mm',
        wattage: '10W / 14W',
        lumens: '1000 lm – 1450 lm',
        beam: '24° Medium / 36° Flood',
        cct: '2700K / 3000K / 4000K',
        cri: 'Ra > 95 / R9 > 80',
        ip: 'IP44 Soft Baffle',
        highlights: [
            'Curved parabolic soft-glare baffle',
            'UGR < 16 ultra visual comfort',
            'Smooth shadow-free light transition',
            'Premium micro-matt finish'
        ]
    },
    {
        id: 'rivo-r',
        name: 'RIVO R',
        subtitle: 'Round IP54 Splash-Proof Recessed Luminaire',
        category: 'waterproof',
        categoryLabel: 'WATERPROOF IP54 ARCHITECTURAL',
        image: 'images/recessed/rivo-r.jpg',
        badge: 'MODEL: RIVO R',
        desc: 'Sealed silicone gasketed round housing engineered for humid environments including luxury bathrooms, wellness spas, and covered exterior building soffits.',
        cutout: 'Ø 80 mm',
        wattage: '8W / 12W',
        lumens: '800 lm – 1250 lm',
        beam: '24° Medium / 36° Flood / 50° Wide',
        cct: '3000K / 4000K Neutral White',
        cri: 'Ra > 95 / R9 > 80',
        ip: 'IP54 Waterproof Sealed',
        highlights: [
            'IP54 full water splash & steam protection',
            'Toughened clear glass safety lens',
            'Silicone dual-gasket seal ring',
            'Anti-corrosion powder coating'
        ]
    },
    {
        id: 'rivo-s',
        name: 'RIVO S',
        subtitle: 'Square IP54 Splash-Proof Recessed Luminaire',
        category: 'waterproof',
        categoryLabel: 'WATERPROOF IP54 ARCHITECTURAL',
        image: 'images/recessed/rivo-s.jpg',
        badge: 'MODEL: RIVO S',
        desc: 'Square profile IP54 waterproof luminaire with tempered glass lens protective shield and anti-corrosion coating for outdoor balconies and wet zones.',
        cutout: '80 x 80 mm',
        wattage: '8W / 12W',
        lumens: '800 lm – 1250 lm',
        beam: '24° Medium / 36° Flood / 50° Wide',
        cct: '3000K / 4000K Neutral White',
        cri: 'Ra > 95 / R9 > 80',
        ip: 'IP54 Waterproof Sealed',
        highlights: [
            'Square IP54 moisture barrier',
            'Ideal for spa, bathroom & outdoor canopy',
            'High rendering Cree COB chip',
            'Rust resistant die-cast alloy'
        ]
    },
    {
        id: 'rivo-2',
        name: 'RIVO 2',
        subtitle: 'Double-Head IP54 Waterproof Recessed Luminaire',
        category: 'waterproof',
        categoryLabel: 'WATERPROOF IP54 ARCHITECTURAL',
        image: 'images/recessed/rivo-2.jpg',
        badge: 'MODEL: RIVO 2',
        desc: 'Twin-head sealed IP54 architectural spotlight module engineered for luxury wet room interiors, pool houses, and covered exterior terrace ceilings.',
        cutout: '155 x 80 mm',
        wattage: '2 x 8W / 2 x 12W (16W – 24W total)',
        lumens: '1600 lm – 2500 lm',
        beam: '24° Medium / 36° Flood / 50° Wide',
        cct: '3000K / 4000K Neutral White',
        cri: 'Ra > 95 / R9 > 80',
        ip: 'IP54 Twin Waterproof',
        highlights: [
            'Twin module IP54 waterproof rating',
            'High lumen output for wet environments',
            'Dual glass lens thermal protection',
            'Long-life exterior architectural build'
        ]
    }
];

function initRecessedMarqueePage() {
    const marqueeTrack = document.getElementById('recessedMarqueeTrack');
    const thumbnailsGrid = document.getElementById('modelThumbnailsGrid');
    const grid = document.getElementById('lumiProductsGrid');
    const matrixBody = document.getElementById('matrixTableBody');

    if (!marqueeTrack) return;

    let activeProductIndex = 0;

    // Helper to generate small card HTML
    function createSmallCardHTML(prod, index) {
        return `
            <div class="marquee-card ${index === activeProductIndex ? 'active' : ''}" data-index="${index}" onclick="selectProduct(${index}, true)">
                <div class="card-img-box">
                    <img src="${prod.image}" alt="${prod.name}" loading="lazy">
                    <span class="card-ip-tag">${prod.ip}</span>
                </div>
                <div class="card-title-box">
                    <span class="prefix">VERO</span>
                    <span class="name">${prod.name}</span>
                </div>
                <div class="card-spec-tag">${prod.wattage.split('/')[0]} | ${prod.cutout}</div>
            </div>
        `;
    }

    // 1. Render 16 Small Marquee Cards (Set 1 + Set 2 for 100% infinite loop)
    function renderMarqueeTrack() {
        const set1 = RECESSED_PRODUCTS.map((prod, i) => createSmallCardHTML(prod, i)).join('');
        const set2 = RECESSED_PRODUCTS.map((prod, i) => createSmallCardHTML(prod, i)).join('');
        marqueeTrack.innerHTML = set1 + set2;
    }

    // 2. Render Thumbnails Grid in Featured Section
    function renderThumbnails() {
        if (!thumbnailsGrid) return;
        thumbnailsGrid.innerHTML = RECESSED_PRODUCTS.map((prod, index) => `
            <button class="thumb-btn ${index === activeProductIndex ? 'active' : ''}" data-index="${index}" onclick="selectProduct(${index}, false)" title="${prod.name}">
                <img src="${prod.image}" alt="${prod.name}">
                <span class="thumb-name">${prod.name}</span>
            </button>
        `).join('');
    }

    // 3. Render 5-Column Grid
    function renderProductsGrid() {
        if (!grid) return;
        grid.innerHTML = RECESSED_PRODUCTS.map((prod, index) => `
            <div class="lumi-card" data-category="${prod.category}" onclick="selectProduct(${index}, true)">
                <div class="lumi-card-img">
                    <img src="${prod.image}" alt="${prod.name}" loading="lazy">
                </div>
                <div class="lumi-card-info">
                    <h3 class="lumi-card-title">
                        <span class="prefix">VERO</span>
                        <span class="name">${prod.name}</span>
                    </h3>
                    <div class="lumi-card-sublink">
                        <span class="sublink-text">${prod.wattage.split('/')[0]} | ${prod.cutout}</span>
                        <span class="sublink-arrow">&rarr;</span>
                    </div>
                </div>
            </div>
        `).join('');
    }

    // 4. Render Matrix Table
    function renderMatrix() {
        if (!matrixBody) return;
        matrixBody.innerHTML = RECESSED_PRODUCTS.map((prod, index) => `
            <tr class="${index === activeProductIndex ? 'active-row' : ''}">
                <td class="cell-model">
                    <img src="${prod.image}" class="matrix-thumb" alt="${prod.name}">
                    <strong>${prod.name}</strong>
                </td>
                <td>${prod.categoryLabel.split(' ')[0]}</td>
                <td>${prod.cutout}</td>
                <td>${prod.wattage}</td>
                <td>${prod.lumens}</td>
                <td>${prod.beam}</td>
                <td>${prod.cri}</td>
                <td><span class="matrix-ip-badge">${prod.ip}</span></td>
                <td>
                    <button class="matrix-select-btn" onclick="selectProduct(${index}, true)">Select</button>
                </td>
            </tr>
        `).join('');
    }

    // 5. Active Product Selection
    function selectProduct(index, shouldScroll = false) {
        if (index < 0 || index >= RECESSED_PRODUCTS.length) return;
        activeProductIndex = index;
        const prod = RECESSED_PRODUCTS[index];

        const img = document.getElementById('mainProductImg');
        const badge = document.getElementById('mainProductBadge');
        const cat = document.getElementById('mainProductCategory');
        const title = document.getElementById('mainProductTitle');
        const sub = document.getElementById('mainProductSubtitle');
        const desc = document.getElementById('mainProductDesc');
        const highlightsList = document.getElementById('mainProductHighlights');

        const specWattage = document.getElementById('specWattage');
        const specLumens = document.getElementById('specLumens');
        const specCutout = document.getElementById('specCutout');
        const specBeam = document.getElementById('specBeam');
        const specCct = document.getElementById('specCct');
        const specCri = document.getElementById('specCri');
        const specIp = document.getElementById('specIp');

        if (img) {
            img.style.opacity = '0.3';
            setTimeout(() => {
                img.src = prod.image;
                img.alt = prod.name;
                img.style.opacity = '1';
            }, 150);
        }

        if (badge) badge.textContent = prod.badge;
        if (cat) cat.textContent = prod.categoryLabel;
        if (title) title.textContent = prod.name;
        if (sub) sub.textContent = prod.subtitle;
        if (desc) desc.textContent = prod.desc;

        if (specWattage) specWattage.textContent = prod.wattage;
        if (specLumens) specLumens.textContent = prod.lumens;
        if (specCutout) specCutout.textContent = prod.cutout;
        if (specBeam) specBeam.textContent = prod.beam;
        if (specCct) specCct.textContent = prod.cct;
        if (specCri) specCri.textContent = prod.cri;
        if (specIp) specIp.textContent = prod.ip;

        if (highlightsList) {
            highlightsList.innerHTML = prod.highlights.map(hl => `
                <div class="highlight-item">
                    <span class="hl-dot"></span>
                    <span>${hl}</span>
                </div>
            `).join('');
        }

        // Highlight active cards in marquee
        if (marqueeTrack) {
            marqueeTrack.querySelectorAll('.marquee-card').forEach(card => {
                const i = parseInt(card.getAttribute('data-index'), 10);
                card.classList.toggle('active', i === index);
            });
        }

        if (thumbnailsGrid) {
            thumbnailsGrid.querySelectorAll('.thumb-btn').forEach((btn, i) => {
                btn.classList.toggle('active', i === index);
            });
        }

        if (matrixBody) {
            matrixBody.querySelectorAll('tr').forEach((row, i) => {
                row.classList.toggle('active-row', i === index);
            });
        }

        if (shouldScroll) {
            const section = document.getElementById('featuredProductSection');
            if (section) {
                section.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }
    }

    window.selectProduct = selectProduct;

    // Filter Buttons logic
    const filterPills = document.querySelectorAll('#lumiFilterBar .pill-tab');
    filterPills.forEach(btn => {
        btn.addEventListener('click', () => {
            filterPills.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const filter = btn.getAttribute('data-filter');

            if (grid) {
                const cards = grid.querySelectorAll('.lumi-card');
                cards.forEach(card => {
                    const cat = card.getAttribute('data-category');
                    if (filter === 'all' || cat === filter) {
                        card.style.display = 'flex';
                    } else {
                        card.style.display = 'none';
                    }
                });
            }
        });
    });

    renderMarqueeTrack();
    renderThumbnails();
    renderProductsGrid();
    renderMatrix();
    selectProduct(0, false);
}
