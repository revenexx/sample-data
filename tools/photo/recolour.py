"""Colour variants without AI: the model's finished photo, recoloured pixel by pixel.

    tools/photo/.venv/bin/python tools/photo/recolour.py <photo.jpg> <#rrggbb> <out.jpg>

The shape stays exactly the same; only the light plastic of the product changes colour.
- The product outline comes from a local background-removal model run on the photo itself.
- Inside the outline, light pixels are the plastic body: their brightness is kept as shading
  and mapped onto the new colour. Darker pixels (holes, gaps, metal contacts) stay as they are.
- Outside the outline (white backdrop, shadow) nothing changes.
"""
import sys

import numpy as np
from PIL import Image, ImageFilter


_session = None


def outline(img):
    """The product's outline in its photo, as 0..1 per pixel, from a local background-removal model
    (rembg, isnet-general-use; MIT). It finds white products on white, and leaves the shadow out."""
    global _session
    from rembg import new_session, remove
    _session = _session or new_session('isnet-general-use')
    return np.asarray(remove(img, session=_session, only_mask=True)).astype(np.float32) / 255


def dominant(pixels):
    """The most common colour among these pixels (coarse bins, then the mean of the winning bin)."""
    q = (pixels // 24).astype(np.int32)
    keys = q[:, 0] * 10000 + q[:, 1] * 100 + q[:, 2]
    values, counts = np.unique(keys, return_counts=True)
    return pixels[keys == values[counts.argmax()]].mean(axis=0)


def recolour(photo_path, colour, out_path):
    img = Image.open(photo_path).convert('RGB')
    rgb = np.asarray(img).astype(np.float32)
    lum = rgb @ np.array([0.299, 0.587, 0.114], np.float32)
    soft = outline(img)
    # Backdrop that the outline takes in (between a cable and its device), not lit spots on the product.
    from scipy import ndimage
    labels, _ = ndimage.label((rgb >= 254.5).all(axis=2))                  # the whitened backdrop is exactly white
    edge = np.unique(np.concatenate([labels[0], labels[-1], labels[:, 0], labels[:, -1]]))
    backdrop = np.isin(labels, edge[edge > 0]) & (soft < 0.9)            # ...reaches the border, and the cut-out is unsure
    soft = soft * ~backdrop
    mask = soft > 0.5
    target = np.array([int(colour[i:i + 2], 16) for i in (1, 3, 5)], np.float32)
    body_colour = dominant(rgb[mask & (lum > 25) & (lum < 252)])
    if np.abs(body_colour - target).max() < 28:                        # already this colour: the same photo
        img.save(out_path, 'JPEG', quality=85, optimize=True, progressive=True)
        return
    L0 = float(body_colour @ np.array([0.299, 0.587, 0.114], np.float32))
    if L0 > 170:
        # A white or light product: the light pixels are the body, their brightness is the shading.
        inside = lum[mask]
        lo, hi = 170.0, float(np.percentile(inside[inside > 170], 95)) if (inside > 170).any() else 250.0
        shade = np.clip((lum - lo) / max(hi - lo, 1), 0, 1.15)        # 0 = shaded side, 1 = lit face
        body = np.clip((lum - 150) / 35, 0, 1)                         # light plastic; dark parts stay
        dark, light = target * 0.55, target + (255 - target) * 0.18
        new = dark + (light - dark) * np.clip(shade, 0, 1)[..., None]
        new += (255 - new) * np.clip(shade - 1, 0, 0.15)[..., None] * 4   # keep the highlights
    else:
        # A coloured or dark product: the body is what has the body's hue; its brightness relative to
        # the body colour is the shading. Other colours (labels, pencils, metal) stay.
        chroma = rgb / (lum[..., None] + 8)
        c0 = body_colour / (L0 + 8)
        d = np.linalg.norm(chroma - c0, axis=2)
        body = np.clip(1 - d / 0.3, 0, 1) * ((lum > 0.25 * L0) & (lum < max(2.4 * L0, 60))).astype(np.float32)
        shade = lum / max(L0, 1)
        new = target * np.clip(shade, 0, 1)[..., None]
        new += (255 - target) * np.clip(shade - 1, 0, 1)[..., None] * 0.6
    weight = (soft * body)[..., None]
    out = rgb * (1 - weight) + new * weight
    Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(out_path, 'JPEG', quality=85, optimize=True, progressive=True)


if __name__ == '__main__':
    recolour(*sys.argv[1:4])
