import glob
import re

new_dropdown = '''<div class="dropdown-menu mega-menu" role="menu">
                        <div class="mega-menu-primary" role="tablist" aria-label="Product Categories">
                            <button type="button" class="primary-cat-item is-active" role="tab" aria-selected="true" data-category="indoor" id="tab-indoor">
                                <span class="cat-label">Indoor Lights</span>
                                <svg class="cat-chevron" width="6" height="10" viewBox="0 0 6 10" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                                    <polyline points="1.5 1.5 5 5 1.5 8.5"></polyline>
                                </svg>
                            </button>
                            <button type="button" class="primary-cat-item" role="tab" aria-selected="false" data-category="outdoor" id="tab-outdoor">
                                <span class="cat-label">Outdoor Lights</span>
                                <svg class="cat-chevron" width="6" height="10" viewBox="0 0 6 10" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                                    <polyline points="1.5 1.5 5 5 1.5 8.5"></polyline>
                                </svg>
                            </button>
                            <button type="button" class="primary-cat-item" role="tab" aria-selected="false" data-category="drivers" id="tab-drivers">
                                <span class="cat-label">Drivers &amp; Controllers</span>
                                <svg class="cat-chevron" width="6" height="10" viewBox="0 0 6 10" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                                    <polyline points="1.5 1.5 5 5 1.5 8.5"></polyline>
                                </svg>
                            </button>
                        </div>
                        <div class="mega-menu-subpanels">
                            <div class="mega-subpanel is-active" data-panel="indoor" role="tabpanel" aria-labelledby="tab-indoor">
                                <div class="subpanel-header">Indoor Lights</div>
                                <div class="subpanel-links">
                                    <a href="recessed-led-down-lights.html" class="dropdown-item">Recessed LED Down Lights</a>
                                    <a href="led-surface-down-lights.html" class="dropdown-item">LED Surface Down Lights</a>
                                    <a href="3phase-track-lights.html" class="dropdown-item">3-Phase Track Lights</a>
                                    <a href="office-linear-lights.html" class="dropdown-item">Office Lights</a>
                                    <a href="led-strip-lights.html" class="dropdown-item">LED Strip Lights</a>
                                    <a href="led-magnetic-track-lights.html" class="dropdown-item">LED Magnetic Track Lights</a>
                                </div>
                            </div>
                            <div class="mega-subpanel" data-panel="outdoor" role="tabpanel" aria-labelledby="tab-outdoor">
                                <div class="subpanel-header">Outdoor Lights</div>
                                <div class="subpanel-links">
                                    <a href="led-garden-lights.html" class="dropdown-item">LED Garden Lights</a>
                                    <a href="led-outdoor-flexible-neon-light.html" class="dropdown-item">LED Outdoor Flexible Neon Light</a>
                                </div>
                            </div>
                            <div class="mega-subpanel" data-panel="drivers" role="tabpanel" aria-labelledby="tab-drivers">
                                <div class="subpanel-header">Drivers &amp; Controllers</div>
                                <div class="subpanel-links">
                                    <a href="led-strip-light-drivers.html" class="dropdown-item">LED Strip Light Drivers</a>
                                    <a href="led-phase-cut-dimmer.html" class="dropdown-item">LED Phase Cut Dimmer</a>
                                    <a href="led-sensor-switches.html" class="dropdown-item">LED Sensor Switches</a>
                                </div>
                            </div>
                        </div>
                    </div>'''

files = sorted(glob.glob('*.html'))
pattern = re.compile(r'<div class="dropdown-menu">[\s\S]*?</div>(\s*</div>)')

updated_count = 0
for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        content = fp.read()
    
    match = pattern.search(content)
    if match:
        # replace the <div class="dropdown-menu">...</div> with new_dropdown
        new_content = pattern.sub(new_dropdown + r'\1', content, count=1)
        with open(f, 'w', encoding='utf-8') as fp:
            fp.write(new_content)
        updated_count += 1
        print(f"Updated {f}")
    else:
        print(f"Pattern NOT found in {f}")

print(f"Total updated: {updated_count}/{len(files)}")
