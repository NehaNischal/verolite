import os
from PIL import Image

fdir = r'c:\Users\user\Desktop\verolite\favicon'
master = Image.open(os.path.join(fdir, 'favicon-1024x1024.png'))

# 180x180 for Apple touch icon (iOS home screen / Safari bookmark)
apple_icon = master.resize((180, 180), Image.Resampling.LANCZOS)
apple_icon.save(os.path.join(fdir, 'apple-touch-icon.png'), format='PNG', optimize=True)
print("Created apple-touch-icon.png (180x180)")

# 192x192 for Android / Chrome Web App manifest
android_icon = master.resize((192, 192), Image.Resampling.LANCZOS)
android_icon.save(os.path.join(fdir, 'favicon-192x192.png'), format='PNG', optimize=True)
print("Created favicon-192x192.png (192x192)")

# Create site.webmanifest in favicon folder
manifest_path = os.path.join(fdir, 'site.webmanifest')
manifest_content = '''{
  "name": "VEROLITE Architectural Lighting",
  "short_name": "VEROLITE",
  "icons": [
    {
      "src": "favicon-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "favicon.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ],
  "theme_color": "#ffffff",
  "background_color": "#ffffff",
  "display": "standalone"
}
'''
with open(manifest_path, 'w', encoding='utf-8') as f:
    f.write(manifest_content)
print("Created site.webmanifest")

