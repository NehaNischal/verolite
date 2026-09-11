import fitz
import os

workspace = r"c:\Users\user\Desktop\verolite"
out_dir = os.path.join(workspace, "catalog_sheets")
os.makedirs(out_dir, exist_ok=True)

pdf_mappings = {
    "Recessed LED Down Light .pdf": {
        2: "vero-oliv",
        3: "vero-niko",
        4: "vero-raza",
        5: "vero-kia",
        6: "vero-luxa",
        7: "vero-vexo",
        8: "vero-talon",
        9: "vero-orbit",
        10: "vero-orbit-s",
        11: "vero-orbit-2",
        12: "vero-orbit-3",
        13: "vero-tera",
        14: "vero-syro",
        15: "vero-rivo-r",
        16: "vero-rivo-s",
        17: "vero-rivo-2"
    },
    "LED Surface-Down Light.pdf": {
        2: "vero-daxo",
        3: "vero-zivon",
        4: "vero-arco-7",
        5: "vero-arco-8",
        6: "vero-nova"
    },
    "3Phase Track Light.pdf": {
        2: "vero-lynx"
    },
    "Office Linear Lights.pdf": {
        2: "vero-lino",
        3: "vero-reo-linear",
        4: "vero-recta"
    },
    "Led Magnetic Track Lights.pdf": {
        2: "vero-magnetic-track-channel",
        3: "vero-xenon",
        4: "vero-linan",
        5: "vero-titan",
        6: "vero-vega",
        7: "vero-aero"
    },
    "LED Strip Lights (1).pdf": {
        2: "vero-nexo",
        3: "vero-nexo-cob",
        4: "vero-nexo-ip65"
    },
    "LED OUTDOOR FLEXIBLE  NEON LIGHT _LED Strip Light_LED Phace Cut Dimmer_ LED Sensor Switchs_LED Garden Lights.pdf": {
        2: "vero-reo-neon",
        4: "vero-driver-ip20",
        5: "vero-driver-ip65",
        6: "vero-dimming-driver-ip65",
        7: "vero-dimming-driver-ip20",
        8: "vero-constant-current-dimming",
        10: "vero-phase-cut-dimmer",
        12: "vero-cabinet-door-sensor",
        13: "vero-wireless-motion-sensor",
        14: "vero-wireless-door-sensor",
        15: "vero-partition-touch-hand-wave",
        17: "vero-zion",
        18: "vero-heli"
    }
}

generated = []
for pdf_name, pages in pdf_mappings.items():
    pdf_path = os.path.join(workspace, pdf_name)
    if not os.path.exists(pdf_path):
        continue
    doc = fitz.open(pdf_path)
    for page_num, slug in pages.items():
        if page_num <= len(doc):
            page = doc[page_num - 1]
            pix = page.get_pixmap(dpi=200)
            out_img = os.path.join(out_dir, f"{slug}-sheet.jpg")
            pix.save(out_img)
            generated.append((slug, out_img))

print(f"Generated {len(generated)} catalog sheet images in {out_dir}")
