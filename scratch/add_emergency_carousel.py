import re

with open(r'c:\Users\user\Desktop\verolite\index.html', 'rb') as f:
    content = f.read().decode('utf-8')

# Insert Emergency Lights card in Set 1 (before the Set 2 comment)
set1_card = (
    '                    <a href="emergency-lights.html" class="collection-card" tabindex="0">\r\n'
    '                        <div class="card-image-box">\r\n'
    '                            <img src="images/emergency-hero-banner.jpg?v=full" alt="Emergency Lights - Verolite Safety &amp; Exit Lighting Solutions" width="480" height="600" loading="lazy">\r\n'
    '                        </div>\r\n'
    '                        <div class="card-title">EMERGENCY LIGHTS</div>\r\n'
    '                    </a>\r\n'
)

marker1 = '                    <!-- Set 2 (for seamless continuous infinite looping) -->'
if marker1 in content:
    content = content.replace(marker1, set1_card + marker1, 1)
    print('Set 1 card inserted.')
else:
    print('ERROR: Set 1 marker not found.')

# Insert Emergency Lights card in Set 2 (aria-hidden, before closing carousel-track div)
set2_card = (
    '                    <a href="emergency-lights.html" class="collection-card" aria-hidden="true" tabindex="-1">\r\n'
    '                        <div class="card-image-box">\r\n'
    '                            <img src="images/emergency-hero-banner.jpg?v=full" alt="Emergency Lights">\r\n'
    '                        </div>\r\n'
    '                        <div class="card-title">EMERGENCY LIGHTS</div>\r\n'
    '                    </a>\r\n'
)

# Find the closing of carousel-track (last </div> before </div> of container)
marker2 = '                </div>\r\n            </div>\r\n\r\n        </div>\r\n    </section>'
if marker2 in content:
    content = content.replace(marker2, set2_card + marker2, 1)
    print('Set 2 card inserted.')
else:
    print('ERROR: Set 2 marker not found.')

with open(r'c:\Users\user\Desktop\verolite\index.html', 'wb') as f:
    f.write(content.encode('utf-8'))

print('index.html updated successfully.')

