import re

# 1. Update script.js
with open(r'c:\Users\user\Desktop\verolite\script.js', 'r', encoding='utf-8') as f:
    sjs = f.read()

# Add helper function before initCategorySanityProducts
helper_fn = '''function renderEmergencyFallbackCard(grid) {
    if (!grid) return;
    grid.innerHTML = `
        <a class="ref-card ref-card-visible" href="product.html?slug=emergency-exit-sign" aria-label="Emergency Exit Sign VEROLITE Luminaire" data-product-url="product.html?slug=emergency-exit-sign">
            <div class="ref-card-img-box">
                <img src="images/emergency-hero-banner.jpg" alt="Emergency Exit Sign VEROLITE - VEROLITE Architectural Lighting" loading="lazy" width="400" height="400">
            </div>
            <div class="ref-card-info">
                <h3 class="ref-card-title">
                    <span class="prefix">VER-EMG-01</span>
                    <span class="name">Emergency Exit Sign</span>
                </h3>
                <div class="ref-card-link">
                    <span class="link-text">View Luminaire</span>
                    <span class="link-arrow">&rarr;</span>
                </div>
            </div>
        </a>
    `;
}

// Sync Sanity Products into Category Listing Grids - Pure Sanity Source of Truth'''

sjs = sjs.replace('// Sync Sanity Products into Category Listing Grids - Pure Sanity Source of Truth', helper_fn)

# In initCategorySanityProducts, handle empty or error
target_empty = '''            if (!data.result || !data.result.length) {
                grid.innerHTML = '<div style="grid-column: 1 / -1; text-align: center; padding: 60px 20px; font-family: inherit; font-size: 1.1rem; color: #888;">No products found in this category.</div>';
                return;
            }'''

replacement_empty = '''            if (!data.result || !data.result.length) {
                if (currentCat === 'emergency-lights' || filename === 'emergency-lights') {
                    renderEmergencyFallbackCard(grid);
                    return;
                }
                grid.innerHTML = '<div style="grid-column: 1 / -1; text-align: center; padding: 60px 20px; font-family: inherit; font-size: 1.1rem; color: #888;">No products found in this category.</div>';
                return;
            }'''

sjs = sjs.replace(target_empty, replacement_empty)

target_catch = '''        .catch(err => {
            console.error('Sanity category load error:', err);
            grid.innerHTML = '<div style="grid-column: 1 / -1; text-align: center; padding: 60px 20px; font-family: inherit; font-size: 1.1rem; color: #888;">Unable to load products. Please try again later.</div>';
        });'''

replacement_catch = '''        .catch(err => {
            console.error('Sanity category load error:', err);
            if (currentCat === 'emergency-lights' || filename === 'emergency-lights') {
                renderEmergencyFallbackCard(grid);
                return;
            }
            grid.innerHTML = '<div style="grid-column: 1 / -1; text-align: center; padding: 60px 20px; font-family: inherit; font-size: 1.1rem; color: #888;">Unable to load products. Please try again later.</div>';
        });'''

sjs = sjs.replace(target_catch, replacement_catch)

with open(r'c:\Users\user\Desktop\verolite\script.js', 'w', encoding='utf-8') as f:
    f.write(sjs)

print("script.js updated")

# 2. Update emergency-lights.html
# Clean up emergency-lights.html to match other pages: remove emg-spotlight, put the card in ref-products-grid
with open(r'c:\Users\user\Desktop\verolite\emergency-lights.html', 'r', encoding='utf-8') as f:
    elhtml = f.read()

# Replace the spotlight and empty grid with standard grid containing the product card
# Find from <!-- Product Grid Section --> to </main>
grid_pattern = re.compile(r'<!-- Product Grid Section -->.*?<\/main>', re.DOTALL)
standard_grid = '''<!-- Product Grid Section -->
    <main class="ref-grid-section">
        <h2 class="visually-hidden">Emergency Lights Collection</h2>
        <div class="ref-grid-container">
            <div class="ref-products-grid grid-centered">
                <a class="ref-card ref-card-visible" href="product.html?slug=emergency-exit-sign" aria-label="Emergency Exit Sign VER-EMG-01 Luminaire" data-product-url="product.html?slug=emergency-exit-sign">
                    <div class="ref-card-img-box">
                        <img src="images/emergency-hero-banner.jpg" alt="Emergency Exit Sign VER-EMG-01 - VEROLITE Architectural Lighting" loading="lazy" width="400" height="400">
                    </div>
                    <div class="ref-card-info">
                        <h3 class="ref-card-title">
                            <span class="prefix">VER-EMG-01</span>
                            <span class="name">Emergency Exit Sign</span>
                        </h3>
                        <div class="ref-card-link">
                            <span class="link-text">View Luminaire</span>
                            <span class="link-arrow">&rarr;</span>
                        </div>
                    </div>
                </a>
            </div>
            <noscript>
                <div class="noscript-products" style="padding: 30px 20px; text-align: center;">
                    <p style="font-size: 1.1rem; color: #333; margin-bottom: 16px;">Explore Emergency Lights in this collection:</p>
                    <ul style="list-style: none; padding: 0; display: flex; flex-wrap: wrap; gap: 12px; justify-content: center;">
                        <li><a href="product.html?slug=emergency-exit-sign" style="color: #111; text-decoration: underline;">Emergency Exit Sign</a></li>
                    </ul>
                </div>
            </noscript>
        </div>
    </main>'''

elhtml = grid_pattern.sub(standard_grid, elhtml)

# Also ensure the hero title uses recessed-hero-main-title
elhtml = elhtml.replace('outdoor-hero-main-title', 'recessed-hero-main-title')

with open(r'c:\Users\user\Desktop\verolite\emergency-lights.html', 'w', encoding='utf-8') as f:
    f.write(elhtml)

print("emergency-lights.html updated")
