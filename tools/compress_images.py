import os
from PIL import Image

images_dir = r"R:\Ramy\PATENTE\assets\images"

total_orig = 0
total_new = 0
count = 0

for root, _, files in os.walk(images_dir):
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        if ext in [".jpg", ".jpeg"]:
            fp = os.path.join(root, f)
            orig_sz = os.path.getsize(fp)
            total_orig += orig_sz
            count += 1
            try:
                with Image.open(fp) as img:
                    w, h = img.size
                    max_dim = 1440
                    if max(w, h) > max_dim:
                        scale = max_dim / max(w, h)
                        img = img.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
                    
                    # Save optimized temp
                    tmp_fp = fp + ".opt"
                    img.convert("RGB").save(tmp_fp, format="JPEG", quality=82, optimize=True)
                    new_sz = os.path.getsize(tmp_fp)
                    
                    if new_sz < orig_sz:
                        os.replace(tmp_fp, fp)
                        total_new += new_sz
                    else:
                        os.remove(tmp_fp)
                        total_new += orig_sz
            except Exception as e:
                total_new += orig_sz
                print(f"Error on {f}: {e}")

print(f"Processed {count} images.")
print(f"Original size: {total_orig / (1024*1024):.2f} MB")
print(f"New size: {total_new / (1024*1024):.2f} MB")
print(f"Total space saved: {(total_orig - total_new) / (1024*1024):.2f} MB ({(1 - total_new/total_orig)*100:.1f}%)")
