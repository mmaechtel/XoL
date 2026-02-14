"""
MkDocs hook: Custom social card rendering with background image.
Monkey-patches the built-in social plugin to use Sozial_Background.png
instead of a solid color, with the page title centered in the lower third.
"""

import os
import re
import types
from html import unescape

from PIL import Image, ImageDraw


def on_config(config):
    bg_path = os.path.join(config.docs_dir, "assets/images/Sozial_Background.png")
    if not os.path.isfile(bg_path):
        return

    bg = Image.open(bg_path).convert("RGBA").resize((1200, 630), Image.LANCZOS)

    # Find the social plugin instance
    plugin = None
    for name, p in config.plugins.items():
        if "social" in name.lower() or "Social" in type(p).__name__:
            plugin = p
            break

    if not plugin:
        return

    def _render_card(self, site_name, title, description):
        image = bg.copy()

        # Clean title text
        title = re.sub(r"(<[^>]+>)", "", title)
        title = unescape(title)

        # Render title centered in upper part of lower third
        font = self._get_font("Bold", 56)
        txt_layer = Image.new("RGBA", (1200, 180), (0, 0, 0, 0))
        draw = ImageDraw.Draw(txt_layer)

        # Word wrap by measuring actual text width
        max_width = 1080
        words = title.split()
        lines, current = [], ""
        for word in words:
            test = f"{current} {word}".strip()
            bbox = draw.textbbox((0, 0), test, font=font)
            if bbox[2] - bbox[0] <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)

        wrapped = "\n".join(lines[:2])
        bbox = draw.multiline_textbbox(
            (0, 0), wrapped, font=font, align="center", spacing=10
        )
        text_w = bbox[2] - bbox[0]
        x = (1200 - text_w) // 2
        draw.multiline_text(
            (x, 0), wrapped,
            font=font, fill="white",
            align="center", spacing=10
        )
        image.alpha_composite(txt_layer, (0, 372))

        return image

    plugin._render_card = types.MethodType(_render_card, plugin)
