from PIL import Image

im1 = Image.open(r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\crop_capitoli_index.png")
im2 = Image.open(r"C:\Users\Ramy Fahmy\.gemini\antigravity\brain\e7065af7-148e-49c5-9b06-fabf7a80a8e1\crop_capitolo_01.png")

diff_cols = []
for x in range(im1.width):
    col_diff = False
    for y in range(im1.height):
        p1 = im1.getpixel((x, y))[:3]
        p2 = im2.getpixel((x, y))[:3]
        if max(abs(a - b) for a, b in zip(p1, p2)) > 15:
            col_diff = True
            break
    if col_diff:
        diff_cols.append(x)

print(f"Total diff cols: {len(diff_cols)} / {im1.width}")
if diff_cols:
    print(f"Diff X range: {min(diff_cols)} to {max(diff_cols)}")
    # Sample differences at a few X
    for x in diff_cols[::20]:
        for y in range(10, 60, 10):
            p1 = im1.getpixel((x, y))[:3]
            p2 = im2.getpixel((x, y))[:3]
            if p1 != p2:
                print(f"At ({x}, {y}): im1={p1}, im2={p2}")
