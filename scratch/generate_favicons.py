import os
from PIL import Image

src_path = r'C:\Users\user\Desktop\verolite\favicon.png'
im = Image.open(src_path)
print(f"Original image size: {im.size}, mode: {im.mode}")

# First save a pristine backup of the user's uploaded original
backup_path = r'C:\Users\user\Desktop\verolite\favicon-original.png'
im.save(backup_path)
print("Saved pristine original backup.")

# Make sure public/ exists
public_dir = r'C:\Users\user\Desktop\verolite\public'
os.makedirs(public_dir, exist_ok=True)

# 1024x1024 master source
master_1024 = im.resize((1024, 1024), Image.Resampling.LANCZOS)
master_1024.save(os.path.join(public_dir, 'favicon-1024x1024.png'), format='PNG', optimize=True)

# 512x512 favicon.png
img_512 = master_1024.resize((512, 512), Image.Resampling.LANCZOS)

# 32x32 favicon-32x32.png
img_32 = master_1024.resize((32, 32), Image.Resampling.LANCZOS)

# 16x16 favicon-16x16.png
img_16 = master_1024.resize((16, 16), Image.Resampling.LANCZOS)

# 48x48 for ICO inclusion
img_48 = master_1024.resize((48, 48), Image.Resampling.LANCZOS)

# Locations: both public/ and root directory
targets = [public_dir, r'C:\Users\user\Desktop\verolite']

for target in targets:
    # favicon.png - 512x512
    img_512.save(os.path.join(target, 'favicon.png'), format='PNG', optimize=True)
    
    # favicon-32x32.png - 32x32
    img_32.save(os.path.join(target, 'favicon-32x32.png'), format='PNG', optimize=True)
    
    # favicon-16x16.png - 16x16
    img_16.save(os.path.join(target, 'favicon-16x16.png'), format='PNG', optimize=True)
    
    # favicon.ico - containing 16x16, 32x32, 48x48
    ico_path = os.path.join(target, 'favicon.ico')
    img_512.save(ico_path, format='ICO', sizes=[(16, 16), (32, 32), (48, 48)])
    print(f"Generated icons in: {target}")

print("All formats generated successfully.")

