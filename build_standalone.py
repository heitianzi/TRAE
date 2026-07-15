#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build a standalone single HTML file for the pygbag web game.

Embeds game.tar.gz as base64 inside the HTML and patches the Python loader
to read from the embedded data instead of fetching game.tar.gz.
Result: one self-contained .html file that runs in any browser (runtime
still loaded from CDN on first open, then cached).
"""

import base64
import os
import sys

BUILD_DIR = os.path.join(os.path.dirname(__file__), "build", "web")
INDEX_HTML = os.path.join(BUILD_DIR, "index.html")
TARGZ = os.path.join(BUILD_DIR, "game.tar.gz")
OUTPUT = os.path.join(os.path.dirname(__file__), "index.html")


def main():
    if not os.path.exists(INDEX_HTML):
        print(f"ERROR: {INDEX_HTML} not found. Run 'pygbag --build .' first.")
        sys.exit(1)
    if not os.path.exists(TARGZ):
        print(f"ERROR: {TARGZ} not found.")
        sys.exit(1)

    with open(TARGZ, "rb") as f:
        targz_bytes = f.read()
    b64 = base64.b64encode(targz_bytes).decode("ascii")
    print(f"game.tar.gz: {len(targz_bytes)} bytes, base64: {len(b64)} bytes")

    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    # --- Patch 1: inject embedded data right after <html ...> tag ---
    # Define window.GAME_TARGZ_BASE64 so the Python loader can read it.
    embed_script = (
        '<script>window.GAME_TARGZ_BASE64="'
        + b64
        + '";window.GAME_EMBEDDED=1;</script>'
    )
    # Insert immediately after the opening <html ...> tag
    html = html.replace("<html lang=\"en-us\">", "<html lang=\"en-us\">" + embed_script, 1)

    # --- Patch 2: replace the tarfile loading branch to use embedded data ---
    # Original:
    #   else:
    #       import tarfile
    #       async with platform.fopen("game.tar.gz", "rb") as archive:
    #           tar = tarfile.open(fileobj=archive, mode="r:gz")
    #           tar.extractall(path=appdir.as_posix(), filter='tar')
    #           tar.close()
    # Replacement reads from window.GAME_TARGZ_BASE64 via BytesIO.
    old_block = (
        "    else:\n"
        "        import tarfile\n"
        "        async with platform.fopen(\"game.tar.gz\", \"rb\") as archive:\n"
        "            tar = tarfile.open(fileobj=archive, mode=\"r:gz\")\n"
        "            tar.extractall(path=appdir.as_posix(), filter='tar')\n"
        "            tar.close()"
    )
    new_block = (
        "    else:\n"
        "        import tarfile, io, base64 as _b64\n"
        "        if getattr(platform.window, \"GAME_EMBEDDED\", 0):\n"
        "            _raw = _b64.b64decode(platform.window.GAME_TARGZ_BASE64)\n"
        "            tar = tarfile.open(fileobj=io.BytesIO(_raw), mode=\"r:gz\")\n"
        "            tar.extractall(path=appdir.as_posix(), filter='tar')\n"
        "            tar.close()\n"
        "        else:\n"
        "            async with platform.fopen(\"game.tar.gz\", \"rb\") as archive:\n"
        "                tar = tarfile.open(fileobj=archive, mode=\"r:gz\")\n"
        "                tar.extractall(path=appdir.as_posix(), filter='tar')\n"
        "                tar.close()"
    )

    if old_block in html:
        html = html.replace(old_block, new_block, 1)
        print("Patched tarfile loader to use embedded data (with fallback).")
    else:
        print("WARNING: could not find the tarfile loading block to patch.")
        print("The standalone file may still fetch game.tar.gz (won't work standalone).")

    # --- Patch 3: update title ---
    html = html.replace("<title>game</title>", "<title>She Ji Gui Xu Zhuan - Ming Dynasty RPG</title>", 1)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)

    out_size = os.path.getsize(OUTPUT)
    print(f"\nStandalone HTML written to: {OUTPUT}")
    print(f"Size: {out_size:,} bytes ({out_size/1024:.1f} KB)")


if __name__ == "__main__":
    main()
