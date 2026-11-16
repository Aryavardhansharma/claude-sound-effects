"""Draw the sound-effects plugin icon: a speaker with sound waves on a gradient.

Usage: python3 make_icon.py <output.png>
Draws at 4x and scales down for smooth edges. Output is 1024x1024.
"""
import math
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFilter

OUT = 1024
SS = 4                      # supersampling factor
S = OUT * SS


def px(v):
    """Design units (0..1024) to supersampled pixels."""
    return int(round(v * SS))


def gradient(c1, c2):
    """Diagonal gradient from c1 (top-left) to c2 (bottom-right)."""
    v = Image.linear_gradient("L").resize((S, S))
    h = v.rotate(90)
    mask = ImageChops.add(v, h, scale=2.0)
    return Image.composite(Image.new("RGB", (S, S), c2), Image.new("RGB", (S, S), c1), mask)


# Background: deep indigo to violet
bg = gradient((22, 18, 66), (124, 58, 237)).convert("RGBA")

# Soft violet glow behind the sound waves
glow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
ImageDraw.Draw(glow).ellipse([px(360), px(212), px(960), px(812)], fill=(192, 132, 252, 90))
glow = glow.filter(ImageFilter.GaussianBlur(px(110)))
bg = Image.alpha_composite(bg, glow)

# Artwork, centred: speaker spans x 236..516, waves reach x ~800
dx = -20
cy = 512
art = Image.new("RGBA", (S, S), (0, 0, 0, 0))
d = ImageDraw.Draw(art)
white = (255, 255, 255, 255)

# Speaker: box + cone, drawn as a mask, then corners rounded
mask = Image.new("L", (S, S), 0)
md = ImageDraw.Draw(mask)
md.rectangle([px(236 + dx), px(cy - 92), px(352 + dx), px(cy + 92)], fill=255)
cone = [(340 + dx, cy - 92), (516 + dx, cy - 222), (516 + dx, cy + 222), (340 + dx, cy + 92)]
md.polygon([(px(x), px(y)) for x, y in cone], fill=255)
mask = mask.filter(ImageFilter.GaussianBlur(px(14))).point(lambda a: 255 if a > 140 else 0)
mask = mask.filter(ImageFilter.GaussianBlur(SS / 2))   # soften the threshold edge
speaker = Image.new("RGBA", (S, S), white)
speaker.putalpha(mask)
art = Image.alpha_composite(art, speaker)

# Sound waves: three arcs with round ends, fading outward
ox = 540 + dx
stroke = 54
for radius, alpha in ((96, 255), (186, 210), (276, 150)):
    colour = (255, 255, 255, alpha)
    layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    outer = radius + stroke / 2
    ld.arc([px(ox - outer), px(cy - outer), px(ox + outer), px(cy + outer)],
           start=-46, end=46, fill=colour, width=px(stroke))
    for ang in (-46, 46):
        a = math.radians(ang)
        cx_, cy_ = ox + radius * math.cos(a), cy + radius * math.sin(a)
        r = stroke / 2
        ld.ellipse([px(cx_ - r), px(cy_ - r), px(cx_ + r), px(cy_ + r)], fill=colour)
    art = Image.alpha_composite(art, layer)

# Gentle shadow under the artwork
shadow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
shadow.putalpha(art.getchannel("A").point(lambda a: a * 0.35))
shadow = shadow.filter(ImageFilter.GaussianBlur(px(18)))
shadow = ImageChops.offset(shadow, 0, px(14))

icon = Image.alpha_composite(Image.alpha_composite(bg, shadow), art)
icon = icon.resize((OUT, OUT), Image.LANCZOS).convert("RGB")
icon.save(sys.argv[1], optimize=True)
print("saved", sys.argv[1], icon.size)
