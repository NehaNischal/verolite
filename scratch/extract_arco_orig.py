import subprocess, cv2, numpy as np

for fname in ["arco-7.jpg", "arco-8.jpg"]:
    data = subprocess.check_output(["git", "show", f"457410b:images/surface/{fname}"])
    nparr = np.frombuffer(data, np.uint8)
    orig = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    h, w, _ = orig.shape
    
    # Save original to scratch for inspection
    cv2.imwrite(rf"scratch\original_{fname}", orig)
    print(f"Saved original_{fname}: {w}x{h}")
