import cv2
import numpy as np

def generate_dimmer_wide_banner():
    # Load dimmer
    dimmer = cv2.imread(r"images\dimmer\phase-cut-dimmer.jpg")
    dh, dw, _ = dimmer.shape # 753 x 798
    
    # Target banner dimensions: 2000 x 850 (aspect ratio ~ 2.35:1 ultra-wide banner)
    bw, bh = 2000, 850
    banner = np.zeros((bh, bw, 3), dtype=np.uint8)
    
    # Fill with smooth vertical gradient matching dimmer image's background
    # Top color: [193, 192, 194], Bottom color: [203, 202, 204]
    top_col = np.array([193, 192, 194], dtype=np.float32)
    bot_col = np.array([203, 202, 204], dtype=np.float32)
    
    for y in range(bh):
        alpha = y / (bh - 1)
        col = (1 - alpha) * top_col + alpha * bot_col
        banner[y, :] = col.astype(np.uint8)
    
    # Resize dimmer slightly to fit comfortably inside 850px height with ~80px padding top/bottom
    # Target dimmer height = 690px
    target_dh = 690
    target_dw = int(dw * (target_dh / dh))
    dimmer_resized = cv2.resize(dimmer, (target_dw, target_dh), interpolation=cv2.INTER_LANCZOS4)
    
    # Position in center of banner
    start_x = (bw - target_dw) // 2
    start_y = (bh - target_dh) // 2
    
    # Create smooth alpha blend at dimmer bounding box edges so there is zero hard seam
    blend_w = 40
    # Create a 2D alpha mask for the dimmer block
    alpha_mask = np.ones((target_dh, target_dw), dtype=np.float32)
    for i in range(blend_w):
        factor = i / blend_w
        alpha_mask[i, :] *= factor
        alpha_mask[target_dh - 1 - i, :] *= factor
        alpha_mask[:, i] *= factor
        alpha_mask[:, target_dw - 1 - i] *= factor
        
    alpha_mask_3d = np.repeat(alpha_mask[:, :, np.newaxis], 3, axis=2)
    
    # Blend dimmer into banner
    bg_roi = banner[start_y : start_y + target_dh, start_x : start_x + target_dw].astype(np.float32)
    fg_roi = dimmer_resized.astype(np.float32)
    
    blended = (fg_roi * alpha_mask_3d + bg_roi * (1 - alpha_mask_3d)).astype(np.uint8)
    banner[start_y : start_y + target_dh, start_x : start_x + target_dw] = blended
    
    # Add subtle soft ambient studio lighting vignette
    # Studio spotlight on center dimmer
    y_coords, x_coords = np.ogrid[:bh, :bw]
    center_x, center_y = bw // 2, bh // 2
    dist = np.sqrt((x_coords - center_x)**2 + (y_coords - center_y)**2)
    max_dist = np.sqrt((bw//2)**2 + (bh//2)**2)
    
    # Vignette factor
    vignette = 1.0 - 0.08 * (dist / max_dist)**1.5
    banner_float = banner.astype(np.float32) * vignette[:, :, np.newaxis]
    banner = np.clip(banner_float, 0, 255).astype(np.uint8)
    
    # Save
    out_path = r"images\dimmer\dimmer-hero-banner.jpg"
    cv2.imwrite(out_path, banner, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
    print("Created ultra-clean wide studio dimmer-hero-banner.jpg successfully!")

generate_dimmer_wide_banner()
