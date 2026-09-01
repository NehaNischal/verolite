import shutil

# Copy square phase-cut-dimmer.jpg to collection-dimmer.jpg and collection-10.jpg
shutil.copy2(r"images\dimmer\phase-cut-dimmer.jpg", r"images\collection-dimmer.jpg")
shutil.copy2(r"images\dimmer\phase-cut-dimmer.jpg", r"images\collection-10.jpg")
print("Synced collection-dimmer.jpg as square dimmer")
