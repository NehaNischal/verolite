import cv2
import numpy as np

def create_square_card_images():
    # 1. Garden Light: fixture is at x=650..950, y=100..470 in 1024x546
    # Let's crop a 546x546 square from x = 450 to 996 (or x=478 to 1024)
    # This places the fixture at ~75% and the golden illuminated pool at ~35%
    garden = cv2.imread(r"images\garden-hero-banner.jpg")
    gh, gw, _ = garden.shape # 546, 1024
    # crop x: [1024-546, 1024] -> [478, 1024]
    garden_square = garden[:, 478:1024]
    cv2.imwrite(r"images\collection-garden.jpg", garden_square)
    cv2.imwrite(r"images\collection-4.jpg", garden_square)
    print("Created clean collection-garden.jpg centered on garden fixture!")

    # 2. Track Light: track spotlight is at x=550..720 in 1920x1080 (or similar)
    track = cv2.imread(r"images\track-hero-banner.jpg")
    th, tw, _ = track.shape
    # If height=1080, width=1920: spotlight is centered at ~1180
    track_center_x = int(tw * 0.62)
    t_start_x = max(0, min(tw - th, track_center_x - th // 2))
    track_square = track[:, t_start_x : t_start_x + th]
    cv2.imwrite(r"images\collection-track.jpg", track_square)
    cv2.imwrite(r"images\collection-3.jpg", track_square)
    print("Created clean collection-track.jpg centered on track fixture!")

    # 3. Drivers: drivers are at x=400..850 in 1920x1080
    driver = cv2.imread(r"images\drivers\driver-hero-banner.jpg")
    dh, dw, _ = driver.shape
    driver_center_x = int(dw * 0.61)
    d_start_x = max(0, min(dw - dh, driver_center_x - dh // 2))
    driver_square = driver[:, d_start_x : d_start_x + dh]
    cv2.imwrite(r"images\collection-driver.jpg", driver_square)
    cv2.imwrite(r"images\collection-9.jpg", driver_square)
    print("Created clean collection-driver.jpg centered on drivers!")

create_square_card_images()
