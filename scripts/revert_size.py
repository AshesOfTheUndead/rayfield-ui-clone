#!/usr/bin/env python3
"""Revert the bad 2x-smaller changes while keeping the good fixes (tabs, touch, drag).
Use 320x380 default — fits 360px phones at scale 1.0, reasonable on desktop.
Position at 0.55 — slightly below center, thumb-friendly.
"""
import sys

filepath = "/home/z/my-project/RezurXLib.lua"
with open(filepath, "r") as f:
    src = f.read()

T = "\t"
edits = 0

def replace_once(old, new, label):
    global src, edits
    if old not in src:
        print(f"ERROR: {label} — old text not found")
        sys.exit(1)
    if src.count(old) > 1:
        print(f"ERROR: {label} — old text found {src.count(old)} times")
        sys.exit(1)
    src = src.replace(old, new, 1)
    edits += 1
    print(f"OK: {label}")

# 1. Window size: 200x210 → 320x380 (sensible mobile-first default)
replace_once(
    T + "local WIN_W        = (cfg.Size and cfg.Size.X) or 200  -- [FIX] halved for mobile\n"
    + T + "local WIN_H        = (cfg.Size and cfg.Size.Y) or 210  -- [FIX] halved for mobile",

    T + "local WIN_W        = (cfg.Size and cfg.Size.X) or 320  -- mobile-first (fits 360px phones)\n"
    + T + "local WIN_H        = (cfg.Size and cfg.Size.Y) or 380  -- mobile-first",
    "window size 320x380"
)

# 2. Scale ceiling: 0.55 → 1.0 (was making everything microscopic on desktop)
replace_once(
    T*2 + "local scale = math.clamp(math.min(scaleX, scaleY), 0.35, 0.55)\n"
    + T*2 + "-- [FIX] Scale ceiling 0.55 = UI stays small even on desktop (was 1.0)\n",

    T*2 + "local scale = math.clamp(math.min(scaleX, scaleY), 0.4, 1.0)\n",
    "scale ceiling 1.0"
)

# 3. Position: 0.7 → 0.55 (0.7 was too low, 0.5 is center, 0.55 is thumb-friendly)
replace_once(
    T + "shadow.Position = UDim2.new(0.5, -(WIN_W + 36) / 2, 0.7, -(WIN_H + 36) / 2)  -- [FIX] lower on screen",
    T + "shadow.Position = UDim2.new(0.5, -(WIN_W + 36) / 2, 0.55, -(WIN_H + 36) / 2)",
    "shadow position 0.55"
)
replace_once(
    T + "frame.Position = UDim2.new(0.5, -WIN_W / 2, 0.7, -WIN_H / 2)  -- [FIX] lower on screen",
    T + "frame.Position = UDim2.new(0.5, -WIN_W / 2, 0.55, -WIN_H / 2)",
    "frame position 0.55"
)

with open(filepath, "w") as f:
    f.write(src)

print(f"\n{edits} reverts applied.")
