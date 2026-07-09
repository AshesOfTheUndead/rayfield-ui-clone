#!/usr/bin/env python3
"""Apply round 2 of fixes:
1. Make UI 2x smaller — halve base window defaults, lower scale ceiling
2. Drag window lower — position at 0.7 vertical (was 0.5 center)
3. Fix tab text/emoji — use AutomaticSize on btn/textLbl so they grow to fit content
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

# ── Fix 1: Make UI 2x smaller ──
# Halve the default window size and the scale ceiling.
replace_once(
    T + "local WIN_W        = (cfg.Size and cfg.Size.X) or 400  -- smaller default for mobile\n"
    + T + "local WIN_H        = (cfg.Size and cfg.Size.Y) or 420  -- smaller default for mobile",

    T + "local WIN_W        = (cfg.Size and cfg.Size.X) or 200  -- [FIX] halved for mobile\n"
    + T + "local WIN_H        = (cfg.Size and cfg.Size.Y) or 210  -- [FIX] halved for mobile",
    "Fix 1a: halve default window size"
)

# Lower the scale ceiling from 1.0 to 0.5 so even on desktop it stays small
replace_once(
    T*2 + "local scale = math.clamp(math.min(scaleX, scaleY), 0.35, 1.0)\n",

    T*2 + "local scale = math.clamp(math.min(scaleX, scaleY), 0.35, 0.55)\n"
    + T*2 + "-- [FIX] Scale ceiling 0.55 = UI stays small even on desktop (was 1.0)\n",
    "Fix 1b: lower scale ceiling to 0.55"
)

# ── Fix 2: Drag window lower ──
# Change vertical position from 0.5 (center) to 0.7 (lower on screen)
replace_once(
    T + "shadow.Position = UDim2.new(0.5, -(WIN_W + 36) / 2, 0.5, -(WIN_H + 36) / 2)",
    T + "shadow.Position = UDim2.new(0.5, -(WIN_W + 36) / 2, 0.7, -(WIN_H + 36) / 2)  -- [FIX] lower on screen",
    "Fix 2a: shadow lower"
)
replace_once(
    T + "frame.Position = UDim2.new(0.5, -WIN_W / 2, 0.5, -WIN_H / 2)",
    T + "frame.Position = UDim2.new(0.5, -WIN_W / 2, 0.7, -WIN_H / 2)  -- [FIX] lower on screen",
    "Fix 2b: frame lower"
)

# ── Fix 3: Tab text/emoji blank ──
# The btn starts at 0 width and updateBtnSize() uses TextBounds which is 0
# before render. Replace with AutomaticSize so btn and textLbl grow to fit.
# Replace the btn.Size line to use AutomaticSize
replace_once(
    T*2 + "local btn = Instance.new(\"TextButton\")\n"
    + T*2 + "btn.Name = \"TabChip\"\n"
    + T*2 + "btn.Size = UDim2.new(0, 0, 1, -10)\n"
    + T*2 + "btn.Position = UDim2.new(0, 0, 0, 5)\n"
    + T*2 + "btn.BackgroundColor3 = C.tabChip\n"
    + T*2 + "btn.AutoButtonColor = false\n"
    + T*2 + "btn.BorderSizePixel = 0\n"
    + T*2 + "btn.Text = \"\"\n"
    + T*2 + "btn.ZIndex = 4\n"
    + T*2 + "btn.Parent = tabBar\n"
    + T*2 + "corner(btn, R.tab)\n"
    + T*2 + "local chipStroke = stroke(btn, C.borderAcc, 1)\n",

    T*2 + "local btn = Instance.new(\"TextButton\")\n"
    + T*2 + "btn.Name = \"TabChip\"\n"
    + T*2 + "-- [FIX] AutomaticSize X so btn grows to fit icon+text (was 0 width → blank)\n"
    + T*2 + "btn.Size = UDim2.new(0, 70, 1, -10)\n"
    + T*2 + "btn.AutomaticSize = Enum.AutomaticSize.X\n"
    + T*2 + "btn.Position = UDim2.new(0, 0, 0, 5)\n"
    + T*2 + "btn.BackgroundColor3 = C.tabChip\n"
    + T*2 + "btn.AutoButtonColor = false\n"
    + T*2 + "btn.BorderSizePixel = 0\n"
    + T*2 + "btn.Text = \"\"\n"
    + T*2 + "btn.ZIndex = 4\n"
    + T*2 + "btn.Parent = tabBar\n"
    + T*2 + "corner(btn, R.tab)\n"
    + T*2 + "local chipStroke = stroke(btn, C.borderAcc, 1)\n",
    "Fix 3a: btn AutomaticSize"
)

# Replace textLbl to use AutomaticSize X (grows to fit text)
replace_once(
    T*2 + "local textLbl = Instance.new(\"TextLabel\")\n"
    + T*2 + "textLbl.Size = UDim2.new(0, 60, 1, 0)  -- fixed width so text is visible\n"
    + T*3 + "textLbl.AutomaticSize = Enum.AutomaticSize.None  -- disabled\n"
    + T*2 + "textLbl.BackgroundTransparency = 1\n"
    + T*2 + "textLbl.Font = Enum.Font.GothamBold\n"
    + T*2 + "textLbl.TextSize = 12\n"
    + T*2 + "textLbl.TextColor3 = C.textDim\n"
    + T*2 + "textLbl.Text = name\n"
    + T*2 + "textLbl.LayoutOrder = 2\n"
    + T*2 + "textLbl.Parent = btn\n",

    T*2 + "local textLbl = Instance.new(\"TextLabel\")\n"
    + T*2 + "-- [FIX] AutomaticSize X so label grows to fit text (was fixed 60px → text clipped)\n"
    + T*2 + "textLbl.Size = UDim2.new(0, 50, 1, 0)\n"
    + T*2 + "textLbl.AutomaticSize = Enum.AutomaticSize.X\n"
    + T*2 + "textLbl.BackgroundTransparency = 1\n"
    + T*2 + "textLbl.Font = Enum.Font.GothamBold\n"
    + T*2 + "textLbl.TextSize = 12\n"
    + T*2 + "textLbl.TextColor3 = C.textDim\n"
    + T*2 + "textLbl.Text = name\n"
    + T*2 + "textLbl.LayoutOrder = 2\n"
    + T*2 + "textLbl.Parent = btn\n",
    "Fix 3b: textLbl AutomaticSize"
)

# Remove the broken updateBtnSize() — it's no longer needed since btn auto-sizes
replace_once(
    T*3 + "local function updateBtnSize()\n"
    + T*4 + "local textW = textLbl.TextBounds.X > 0 and textLbl.TextBounds.X or 50\n"
    + T*4 + "local iconW = icon and 16 or 0\n"
    + T*4 + "local w = math.max(textW + iconW + (icon and 5 or 0) + 24, 60)\n"
    + T*4 + "btn.Size = UDim2.new(0, w, 1, -10)\n"
    + T*4 + "if ActiveTab == tab then\n"
    + T*5 + "moveIndicatorTo(btn, false)\n"
    + T*4 + "end\n"
    + T*2 + "end\n"
    + T*2 + "textLbl:GetPropertyChangedSignal(\"TextBounds\"):Connect(updateBtnSize)\n"
    + T*2 + "updateBtnSize()\n",

    T*3 + "-- [FIX] updateBtnSize removed — btn uses AutomaticSize.X now\n"
    + T*3 + "-- Just move the indicator to the btn's current position on load\n"
    + T*3 + "task.defer(function()\n"
    + T*4 + "if ActiveTab == tab then\n"
    + T*5 + "moveIndicatorTo(btn, false)\n"
    + T*4 + "end\n"
    + T*2 + "end)\n",
    "Fix 3c: remove updateBtnSize"
)

# ── Also update the tab indicator initial size to match new btn min width ──
replace_once(
    T + "tabIndicator.Size = UDim2.new(0, 0, 0, TABBAR_H - 10)\n"
    + T + "tabIndicator.Position = UDim2.new(0, 4, 0, 5)\n",

    T + "tabIndicator.Size = UDim2.new(0, 70, 0, TABBAR_H - 10)\n"
    + T + "tabIndicator.Position = UDim2.new(0, 4, 0, 5)\n",
    "Fix 3d: tab indicator min size"
)

with open(filepath, "w") as f:
    f.write(src)

print(f"\nAll {edits} edits applied.")
