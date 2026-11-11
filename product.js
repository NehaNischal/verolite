/**
 * VEROLITE - Dynamic Master Product Page Loader
 * Connects directly to Sanity CMS Content Lake (Read-Only Public CDN API)
 * Sanity Project ID: 5nckxq6b
 * Dataset: production
 */

(function () {
    const SANITY_PROJECT_ID = '5nckxq6b';
    const SANITY_DATASET = 'production';
    const SANITY_API_VERSION = '2023-08-01';

    // Website Category Definitions & Page Mappings
    const CATEGORY_CONFIG = {
        'recessed-led-down-lights': { title: 'Recessed LED Down Lights', page: 'recessed-led-down-lights.html' },
        'led-surface-down-lights': { title: 'LED Surface Down Lights', page: 'led-surface-down-lights.html' },
        '3phase-track-lights': { title: '3-Phase Track Lights', page: '3phase-track-lights.html' },
        'led-garden-lights': { title: 'LED Garden Lights', page: 'led-garden-lights.html' },
        'led-strip-lights': { title: 'LED Strip Lights', page: 'led-strip-lights.html' },
        'led-outdoor-flexible-neon-light': { title: 'LED Outdoor Flexible Neon Light', page: 'led-outdoor-flexible-neon-light.html' },
        'led-magnetic-track-lights': { title: 'LED Magnetic Track Lights', page: 'led-magnetic-track-lights.html' },
        'office-linear-lights': { title: 'Office Linear Lights', page: 'office-linear-lights.html' },
        'led-strip-light-drivers': { title: 'LED Strip Light Drivers', page: 'led-strip-light-drivers.html' },
        'led-phase-cut-dimmer': { title: 'LED Phase Cut Dimmer', page: 'led-phase-cut-dimmer.html' },
        'led-sensor-switches': { title: 'LED Sensor Switches', page: 'led-sensor-switches.html' },
        'emergency-lights': { title: 'Emergency Lights', page: 'emergency-lights.html' },
    };

    function getCategoryInfo(rawCat) {
        if (!rawCat) return { title: 'Architectural Lighting', page: 'index.html#collections' };
        if (CATEGORY_CONFIG[rawCat]) return CATEGORY_CONFIG[rawCat];

        const key = rawCat.toLowerCase().replace(/\s+/g, '-');
        if (CATEGORY_CONFIG[key]) return CATEGORY_CONFIG[key];

        // Format slug to Title Case fallback
        const formattedTitle = rawCat
            .split(/[-_]/)
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
        return { title: formattedTitle, page: 'index.html#collections' };
    }

    // Extract slug from URL query param (?slug=heli) or pathname (/products/heli)
    function getProductSlug() {
        const urlParams = new URLSearchParams(window.location.search);
        let slug = urlParams.get('slug');

        if (!slug || slug === 'undefined' || slug === 'null') {
            const pathParts = window.location.pathname.split('/').filter(Boolean);
            if (pathParts.length >= 2 && (pathParts[0] === 'products' || pathParts[0] === 'product')) {
                slug = pathParts[1].replace('.html', '');
            }
        }

        if (slug === 'undefined' || slug === 'null') slug = null;

        return slug ? decodeURIComponent(slug).trim() : null;
    }

    // Convert Sanity Image Asset reference to direct CDN URL
    function buildImageUrl(imageObj) {
        if (!imageObj) return null;
        if (typeof imageObj === 'string') return imageObj;
        if (imageObj.asset && imageObj.asset.url) return imageObj.asset.url;
        if (imageObj.asset && imageObj.asset._ref) {
            const ref = imageObj.asset._ref;
            const parts = ref.split('-');
            if (parts.length >= 4) {
                const id = parts[1];
                const dimensions = parts[2];
                const extension = parts[3];
                return `https://cdn.sanity.io/images/${SANITY_PROJECT_ID}/${SANITY_DATASET}/${id}-${dimensions}.${extension}`;
            }
        }
        return null;
    }

    // Query Sanity API using GROQ
    async function fetchSanityProduct(slug) {
        if (!slug) return null;

        const cleanSlug = slug.trim();
        const groq = `*[_type == "product" && !(_id in path("drafts.**")) && slug.current == "${cleanSlug}"][0]{
            _id,
            name,
            model,
            slug,
            "category": coalesce(category->slug.current, category, categorySlug),
            "categoryTitle": coalesce(category->title, category),
            "primaryCategory": category->parentGroup->title,
            shortDescription,
            description,
            mainImage,
            "mainImageUrl": mainImage.asset->url,
            gallery,
            "galleryUrls": gallery[].asset->url,
            features,
            specifications,
            variantHeaders,
            variants[]{
                model,
                wattage,
                cct,
                body,
                size,
                cutOut,
                "pdfUrl": pdf.asset->url
            },
            datasheet,
            "datasheetUrl": datasheet.asset->url,
            seoTitle,
            seoDescription,
            seoImage,
            "seoImageUrl": seoImage.asset->url,
            canonicalUrl,
            noIndex
        }`;

        const encodedQuery = encodeURIComponent(groq);
        const endpoint = `https://${SANITY_PROJECT_ID}.api.sanity.io/v${SANITY_API_VERSION}/data/query/${SANITY_DATASET}?query=${encodedQuery}`;

        const response = await fetch(endpoint, { cache: 'no-store' });
        if (!response.ok) {
            throw new Error(`Sanity API error: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();
        return data.result;
    }

    // Populate the template with product data
    function renderProduct(product) {
        const loadingEl = document.getElementById('productLoadingState');
        const contentEl = document.getElementById('productContentState');
        const errorEl = document.getElementById('productErrorState');

        if (!product) {
            document.title = 'Product Not Found | VEROLITE Architectural Lighting';
            let metaRobots = document.querySelector('meta[name="robots"]');
            if (!metaRobots) {
                metaRobots = document.createElement('meta');
                metaRobots.name = 'robots';
                document.head.appendChild(metaRobots);
            }
            metaRobots.setAttribute('content', 'noindex, follow');

            let schemaScript = document.getElementById('productSchemaJsonLd');
            if (schemaScript) schemaScript.remove();

            if (loadingEl) loadingEl.style.display = 'none';
            if (contentEl) contentEl.style.display = 'none';
            if (errorEl) errorEl.style.display = 'block';
            return;
        }

        // 1. Titles & Metadata with sensible fallbacks
        const productName = (product.name || '').trim();
        const productModel = (product.model || '').trim();
        const catInfo = getCategoryInfo(product.category);
        const categoryName = catInfo.title;
        const defaultTitle = (productModel && productModel !== '-' && productModel !== productName)
            ? `${productName} (${productModel}) | VEROLITE Architectural Lighting`
            : `${productName} | VEROLITE Architectural Lighting`;
        const seoPageTitle = (product.seoTitle && product.seoTitle.trim())
            ? product.seoTitle.trim()
            : defaultTitle;

        document.title = seoPageTitle;

        // Meta Description Fallback
        const defaultMetaDesc = (product.shortDescription && product.shortDescription.trim())
            ? product.shortDescription.trim()
            : (product.description && product.description.trim())
                ? product.description.trim().substring(0, 155) + '...'
                : `Discover the ${productName} luminaire by VEROLITE. Precision architectural LED lighting with exceptional optical design and engineering excellence.`;
        const seoMetaDescription = (product.seoDescription && product.seoDescription.trim())
            ? product.seoDescription.trim()
            : defaultMetaDesc;

        let metaDesc = document.querySelector('meta[name="description"]');
        if (!metaDesc) {
            metaDesc = document.createElement('meta');
            metaDesc.name = 'description';
            document.head.appendChild(metaDesc);
        }
        metaDesc.setAttribute('content', seoMetaDescription);

        // Canonical URL Fallback
        const currentSlug = (product.slug && product.slug.current) ? product.slug.current : getProductSlug();
        const defaultCanonical = `https://verolite.co.uk/product.html?slug=${encodeURIComponent(currentSlug || '')}`;
        const canonicalHref = (product.canonicalUrl && product.canonicalUrl.trim())
            ? product.canonicalUrl.trim()
            : defaultCanonical;

        let canonicalLink = document.querySelector('link[rel="canonical"]');
        if (!canonicalLink) {
            canonicalLink = document.createElement('link');
            canonicalLink.rel = 'canonical';
            document.head.appendChild(canonicalLink);
        }
        canonicalLink.href = canonicalHref;

        // Robots Directive (noindex if flagged in Sanity)
        let robotsMeta = document.querySelector('meta[name="robots"]');
        if (!robotsMeta) {
            robotsMeta = document.createElement('meta');
            robotsMeta.name = 'robots';
            document.head.appendChild(robotsMeta);
        }
        robotsMeta.setAttribute('content', product.noIndex ? 'noindex, nofollow' : 'index, follow, max-image-preview:large');

        // Main Image URL resolution for Social & Schema
        const resolvedMainImgUrl = product.seoImageUrl || product.mainImageUrl || buildImageUrl(product.seoImage) || buildImageUrl(product.mainImage) || 'https://verolite.co.uk/images/recessed-hero-banner.jpg';

        // Helper to update or create meta tags
        function setMetaTag(selector, attr, attrVal, content) {
            let el = document.querySelector(selector);
            if (!el) {
                el = document.createElement('meta');
                el.setAttribute(attr, attrVal);
                document.head.appendChild(el);
            }
            el.setAttribute('content', content);
        }

        // Open Graph & Social Sharing Metadata
        setMetaTag('meta[property="og:title"]', 'property', 'og:title', seoPageTitle);
        setMetaTag('meta[property="og:description"]', 'property', 'og:description', seoMetaDescription);
        setMetaTag('meta[property="og:url"]', 'property', 'og:url', canonicalHref);
        setMetaTag('meta[property="og:image"]', 'property', 'og:image', resolvedMainImgUrl);
        setMetaTag('meta[property="og:type"]', 'property', 'og:type', 'product');
        setMetaTag('meta[property="og:site_name"]', 'property', 'og:site_name', 'VEROLITE');

        // Twitter Card Metadata
        setMetaTag('meta[name="twitter:card"]', 'name', 'twitter:card', 'summary_large_image');
        setMetaTag('meta[name="twitter:title"]', 'name', 'twitter:title', seoPageTitle);
        setMetaTag('meta[name="twitter:description"]', 'name', 'twitter:description', seoMetaDescription);
        setMetaTag('meta[name="twitter:image"]', 'name', 'twitter:image', resolvedMainImgUrl);

        // Structured Data: Schema.org Product & BreadcrumbList (JSON-LD)
        let schemaScript = document.getElementById('productSchemaJsonLd');
        if (!schemaScript) {
            schemaScript = document.createElement('script');
            schemaScript.id = 'productSchemaJsonLd';
            schemaScript.type = 'application/ld+json';
            document.head.appendChild(schemaScript);
        }

        const validVariants = (product.variants && Array.isArray(product.variants))
            ? product.variants.filter(v => v && (v.model || v.wattage || v.cct || v.body || v.size || v.cutOut))
            : [];
        const validSpecs = (product.specifications && Array.isArray(product.specifications))
            ? product.specifications.filter(s => s && s.label)
            : [];

        const schemaProductObj = {
            "@type": "Product",
            "@id": canonicalHref + "#product",
            "name": productName,
            "url": canonicalHref,
            "image": resolvedMainImgUrl ? [resolvedMainImgUrl] : [],
            "description": seoMetaDescription,
            "sku": (productModel && productModel !== '-') ? productModel : (currentSlug || productName),
            "mpn": (productModel && productModel !== '-') ? productModel : (currentSlug || productName),
            "brand": {
                "@type": "Brand",
                "name": "VEROLITE"
            },
            "manufacturer": {
                "@type": "Organization",
                "name": "VEROLITE",
                "url": "https://verolite.co.uk/"
            },
            "category": categoryName
        };

        if (validSpecs.length > 0) {
            schemaProductObj.additionalProperty = validSpecs.map(s => ({
                "@type": "PropertyValue",
                "name": s.label,
                "value": s.value || ""
            }));
        }

        if (validVariants.length > 0) {
            schemaProductObj.hasVariant = validVariants.map(v => ({
                "@type": "Product",
                "name": `${productName} ${v.model || ''}`.trim(),
                "sku": v.model || undefined,
                "description": [v.wattage, v.cct, v.body, v.size, v.cutOut].filter(Boolean).join(' | ') || undefined
            }));
        }

        const productJsonLd = {
            "@context": "https://schema.org",
            "@graph": [
                schemaProductObj,
                {
                    "@type": "BreadcrumbList",
                    "@id": canonicalHref + "#breadcrumb",
                    "itemListElement": [
                        {
                            "@type": "ListItem",
                            "position": 1,
                            "name": "Home",
                            "item": "https://verolite.co.uk/"
                        },
                        {
                            "@type": "ListItem",
                            "position": 2,
                            "name": "Collections",
                            "item": "https://verolite.co.uk/#collections"
                        },
                        {
                            "@type": "ListItem",
                            "position": 3,
                            "name": categoryName,
                            "item": "https://verolite.co.uk/" + catInfo.page
                        },
                        {
                            "@type": "ListItem",
                            "position": 4,
                            "name": productName,
                            "item": canonicalHref
                        }
                    ]
                }
            ]
        };
        schemaScript.textContent = JSON.stringify(productJsonLd);

        // Breadcrumbs
        const breadcrumbCat = document.getElementById('breadcrumbCategory');
        const breadcrumbTitle = document.getElementById('breadcrumbProduct');
        if (breadcrumbCat) {
            breadcrumbCat.textContent = categoryName;
            breadcrumbCat.href = catInfo.page;
        }
        if (breadcrumbTitle) {
            breadcrumbTitle.textContent = productName || 'Luminaire';
        }

        // Header Badges & Main Title
        const titleEl = document.getElementById('productMainTitle');
        const modelBadgeEl = document.getElementById('productModelBadge');
        const categoryTagEl = document.getElementById('productCategoryTag');

        if (titleEl) {
            titleEl.textContent = productName;
        }

        if (modelBadgeEl) {
            if (productModel) {
                modelBadgeEl.textContent = `MODEL: ${productModel}`;
                modelBadgeEl.style.display = 'inline-block';
            } else {
                modelBadgeEl.style.display = 'none';
            }
        }

        if (categoryTagEl) {
            categoryTagEl.textContent = categoryName;
        }

        // Short & Long Descriptions
        const shortDescEl = document.getElementById('productShortDesc');
        const fullDescEl = document.getElementById('productFullDesc');
        const fullDescBox = document.getElementById('productFullDescBox');

        if (shortDescEl) {
            if (product.shortDescription && product.shortDescription.trim()) {
                shortDescEl.textContent = product.shortDescription.trim();
                shortDescEl.style.display = 'block';
            } else {
                shortDescEl.style.display = 'none';
            }
        }

        if (fullDescEl && fullDescBox) {
            if (product.description && product.description.trim()) {
                fullDescEl.textContent = product.description.trim();
                fullDescBox.style.display = 'block';
            } else {
                fullDescBox.style.display = 'none';
            }
        }

        // 2. Images & Gallery
        const mainImgUrl = product.mainImageUrl || buildImageUrl(product.mainImage);
        const mainImgEl = document.getElementById('mainProductImage');
        const thumbsContainer = document.getElementById('galleryThumbsContainer');

        if (mainImgEl) {
            if (mainImgUrl) {
                mainImgEl.src = mainImgUrl;
                mainImgEl.alt = productName;
                mainImgEl.style.display = 'block';
            } else {
                mainImgEl.style.display = 'none';
            }
        }

        // Interactive gallery
        const allImages = [];
        if (mainImgUrl) allImages.push(mainImgUrl);

        if (product.galleryUrls && Array.isArray(product.galleryUrls)) {
            product.galleryUrls.forEach(url => {
                if (url && !allImages.includes(url)) allImages.push(url);
            });
        } else if (product.gallery && Array.isArray(product.gallery)) {
            product.gallery.forEach(img => {
                const builtUrl = buildImageUrl(img);
                if (builtUrl && !allImages.includes(builtUrl)) allImages.push(builtUrl);
            });
        }

        if (thumbsContainer) {
            thumbsContainer.innerHTML = '';
            if (allImages.length > 1) {
                allImages.forEach((imgUrl, idx) => {
                    const btn = document.createElement('button');
                    btn.className = `gallery-thumb-btn ${idx === 0 ? 'active' : ''}`;
                    btn.type = 'button';
                    btn.title = `${productName} Image ${idx + 1}`;
                    btn.innerHTML = `<img src="${imgUrl}" alt="${productName} thumbnail">`;
                    btn.addEventListener('click', () => {
                        if (mainImgEl) {
                            mainImgEl.style.opacity = '0.3';
                            setTimeout(() => {
                                mainImgEl.src = imgUrl;
                                mainImgEl.style.opacity = '1';
                            }, 120);
                        }
                        thumbsContainer.querySelectorAll('.gallery-thumb-btn').forEach(b => b.classList.remove('active'));
                        btn.classList.add('active');
                    });
                    thumbsContainer.appendChild(btn);
                });
                thumbsContainer.style.display = 'flex';
            } else {
                thumbsContainer.style.display = 'none';
            }
        }

        // 3. Key Features
        const featuresBox = document.getElementById('productFeaturesBox');
        const featuresGrid = document.getElementById('productFeaturesGrid');

        if (featuresBox && featuresGrid) {
            if (product.features && Array.isArray(product.features) && product.features.length > 0) {
                const validFeatures = product.features.filter(f => f && String(f).trim().length > 0);
                if (validFeatures.length > 0) {
                    featuresGrid.innerHTML = validFeatures.map(feat => `
                        <div class="feature-chip-item">
                            <span class="feature-dot"></span>
                            <span>${feat}</span>
                        </div>
                    `).join('');
                    featuresBox.style.display = 'flex';
                } else {
                    featuresBox.style.display = 'none';
                }
            } else {
                featuresBox.style.display = 'none';
            }
        }

        // 4. Technical Specifications Table (Lower Full-Width Section)
        const specsSection = document.getElementById('productSpecsSection');
        const specsTbody = document.getElementById('productSpecsBody');

        if (specsSection && specsTbody) {
            if (product.specifications && Array.isArray(product.specifications) && product.specifications.length > 0) {
                const validSpecs = product.specifications.filter(s => s && (s.label || s.value));
                if (validSpecs.length > 0) {
                    specsTbody.innerHTML = validSpecs.map(s => `
                        <tr>
                            <td class="spec-key">${s.label || 'Specification'}</td>
                            <td class="spec-val">${s.value || '—'}</td>
                        </tr>
                    `).join('');
                    specsSection.style.display = 'flex';
                } else {
                    specsSection.style.display = 'none';
                }
            } else {
                specsSection.style.display = 'none';
            }
        }

        // 5. Product Variants Table (Lower Full-Width Section)
        const variantsSection = document.getElementById('productVariantsSection');
        const variantsThead = document.getElementById('productVariantsHead');
        const variantsTbody = document.getElementById('productVariantsBody');

        if (variantsSection && variantsTbody) {
            if (product.variants && Array.isArray(product.variants) && product.variants.length > 0) {
                const validVariants = product.variants.filter(v => v && (v.model || v.wattage || v.cct || v.body || v.size || v.cutOut || v.pdfUrl));
                if (validVariants.length > 0) {
                    const defaultCols = [
                        { key: 'model', label: 'Model', colKey: 'col1' },
                        { key: 'wattage', label: 'Wattage', colKey: 'col2' },
                        { key: 'cct', label: 'CCT', colKey: 'col3' },
                        { key: 'body', label: 'Body', colKey: 'col4' },
                        { key: 'size', label: 'Size', colKey: 'col5' },
                        { key: 'cutOut', label: 'Cut-Out', colKey: 'col6' }
                    ];

                    const vh = product.variantHeaders || {};
                    const hasCustomHeaders = Object.keys(vh).length > 0;

                    // Determine active columns based on custom variantHeaders or default data presence
                    const activeCols = defaultCols.map(col => {
                        if (hasCustomHeaders && vh[col.colKey] !== undefined) {
                            const customLabel = (vh[col.colKey] || '').trim();
                            if (!customLabel || customLabel === '-') {
                                return null; // Hidden column
                            }
                            return { key: col.key, label: customLabel };
                        }

                        // If no custom headers set, show default if any variant has a value, or keep Model/Wattage
                        const hasAnyData = validVariants.some(v => v[col.key] && String(v[col.key]).trim() !== '');
                        if (hasAnyData || col.key === 'model' || col.key === 'wattage') {
                            return { key: col.key, label: col.label };
                        }
                        return null;
                    }).filter(Boolean);

                    const hasAnyPdf = validVariants.some(v => v.pdfUrl);

                    // Render dynamic <thead> headers
                    if (variantsThead) {
                        const headerHtml = activeCols.map(c => `<th>${c.label}</th>`).join('') +
                            (hasAnyPdf ? '<th>Datasheet</th>' : '');
                        variantsThead.innerHTML = `<tr>${headerHtml}</tr>`;
                    }

                    // Render dynamic <tbody> rows
                    variantsTbody.innerHTML = validVariants.map(v => {
                        const cellsHtml = activeCols.map(c => {
                            const val = v[c.key] ? String(v[c.key]).trim() : '';
                            if (c.key === 'model') {
                                return `<td><strong>${val || '—'}</strong></td>`;
                            }
                            return `<td>${val || '—'}</td>`;
                        }).join('');

                        const pdfCell = hasAnyPdf ? `
                            <td>
                                ${v.pdfUrl ? `
                                    <a href="${v.pdfUrl}" target="_blank" class="variant-pdf-btn">
                                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                                        PDF
                                    </a>
                                ` : '—'}
                            </td>
                        ` : '';

                        return `<tr>${cellsHtml}${pdfCell}</tr>`;
                    }).join('');

                    variantsSection.style.display = 'flex';
                } else {
                    variantsSection.style.display = 'none';
                }
            } else {
                variantsSection.style.display = 'none';
            }
        }

        // 6. Datasheet / PDF CTA Button
        const pdfBtn = document.getElementById('productDatasheetBtn');
        if (pdfBtn) {
            if (product.datasheetUrl) {
                pdfBtn.href = product.datasheetUrl;
                pdfBtn.style.display = 'inline-flex';
            } else {
                pdfBtn.style.display = 'none';
            }
        }

        // Show Content, Hide Loader
        if (loadingEl) loadingEl.style.display = 'none';
        if (errorEl) errorEl.style.display = 'none';
        if (contentEl) contentEl.style.display = 'block';
    }

    const FALLBACK_EMERGENCY_PRODUCT = {
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

    // Initialize on DOM ready
    async function initProductPage() {
        const slug = getProductSlug();
        const loadingEl = document.getElementById('productLoadingState');
        const contentEl = document.getElementById('productContentState');
        const errorEl = document.getElementById('productErrorState');

        if (!slug) {
            renderProduct(null);
            return;
        }

        try {
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
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initProductPage);
    } else {
        initProductPage();
    }
})();
