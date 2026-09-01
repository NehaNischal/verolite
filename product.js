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

        if (!slug) {
            const pathParts = window.location.pathname.split('/').filter(Boolean);
            if (pathParts.length >= 2 && (pathParts[0] === 'products' || pathParts[0] === 'product')) {
                slug = pathParts[1].replace('.html', '');
            }
        }

        return slug ? slug.trim() : null;
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
        const cleanSlug = slug.toLowerCase();
        const baseSlug = cleanSlug.replace(/-sample$/, '');
        const sampleSlug = `${baseSlug}-sample`;

        const groq = `*[_type == "product" && (
            slug.current == "${cleanSlug}" ||
            slug.current == "${baseSlug}" ||
            slug.current == "${sampleSlug}" ||
            lower(name) == "${cleanSlug}" ||
            lower(model) == "${cleanSlug}"
        )][0]{
            _id,
            name,
            model,
            slug,
            category,
            shortDescription,
            description,
            mainImage,
            "mainImageUrl": mainImage.asset->url,
            gallery,
            "galleryUrls": gallery[].asset->url,
            features,
            specifications,
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
            "datasheetUrl": datasheet.asset->url
        }`;

        const encodedQuery = encodeURIComponent(groq);
        const endpoint = `https://${SANITY_PROJECT_ID}.apicdn.sanity.io/v${SANITY_API_VERSION}/data/query/${SANITY_DATASET}?query=${encodedQuery}`;

        const response = await fetch(endpoint);
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
            if (loadingEl) loadingEl.style.display = 'none';
            if (contentEl) contentEl.style.display = 'none';
            if (errorEl) errorEl.style.display = 'block';
            return;
        }

        // 1. Titles & Metadata
        const productName = (product.name || '').trim();
        const productModel = (product.model || '').trim();
        const catInfo = getCategoryInfo(product.category);
        const categoryName = catInfo.title;
        const displayTitle = productModel ? `${productName} (${productModel})` : productName;

        document.title = `${displayTitle} | VEROLITE Architectural Lighting`;

        // Update Meta Description for SEO
        const metaDesc = document.querySelector('meta[name="description"]');
        if (metaDesc && product.shortDescription) {
            metaDesc.setAttribute('content', product.shortDescription);
        }

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
        const variantsTbody = document.getElementById('productVariantsBody');

        if (variantsSection && variantsTbody) {
            if (product.variants && Array.isArray(product.variants) && product.variants.length > 0) {
                const validVariants = product.variants.filter(v => v && (v.model || v.wattage || v.cct || v.size));
                if (validVariants.length > 0) {
                    variantsTbody.innerHTML = validVariants.map(v => `
                        <tr>
                            <td><strong>${v.model || '—'}</strong></td>
                            <td>${v.wattage || '—'}</td>
                            <td>${v.cct || '—'}</td>
                            <td>${v.body || '—'}</td>
                            <td>${v.size || '—'}</td>
                            <td>${v.cutOut || '—'}</td>
                            <td>
                                ${v.pdfUrl ? `
                                    <a href="${v.pdfUrl}" target="_blank" class="variant-pdf-btn">
                                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                                        PDF
                                    </a>
                                ` : '—'}
                            </td>
                        </tr>
                    `).join('');
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

    // Initialize on DOM ready
    async function initProductPage() {
        const slug = getProductSlug();
        const loadingEl = document.getElementById('productLoadingState');
        const contentEl = document.getElementById('productContentState');
        const errorEl = document.getElementById('productErrorState');

        if (!slug) {
            if (loadingEl) loadingEl.style.display = 'none';
            if (contentEl) contentEl.style.display = 'none';
            if (errorEl) errorEl.style.display = 'block';
            return;
        }

        try {
            const product = await fetchSanityProduct(slug);
            renderProduct(product);
        } catch (err) {
            console.error('Error fetching product from Sanity:', err);
            if (loadingEl) loadingEl.style.display = 'none';
            if (contentEl) contentEl.style.display = 'none';
            if (errorEl) errorEl.style.display = 'block';
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initProductPage);
    } else {
        initProductPage();
    }
})();
