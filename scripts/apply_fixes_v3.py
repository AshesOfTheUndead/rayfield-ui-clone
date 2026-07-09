#!/usr/bin/env python3
"""Round 3 fixes:
1. Bigger window: 320x380 → 420x480 (text was cramped)
2. Scale floor: 0.4 → 0.5 (don't shrink below half)
3. More breathing room: item padding 6→8px, page padding 10→12px
4. Resize handle at bottom-right corner (drag to resize)
5. Status bar draggable (move window from bottom too)
6. Minimize recomputes body height from current WIN_H (supports resize)
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

# 1. Bigger window + min/max size constants
replace_once(
    T + "local WIN_W        = (cfg.Size and cfg.Size.X) or 320  -- mobile-first (fits 360px phones)\n"
    + T + "local WIN_H        = (cfg.Size and cfg.Size.Y) or 380  -- mobile-first\n",

    T + "local WIN_W        = (cfg.Size and cfg.Size.X) or 420  -- bigger (was 320, text was cramped)\n"
    + T + "local WIN_H        = (cfg.Size and cfg.Size.Y) or 480  -- bigger (was 380)\n"
    + T + "local MIN_W, MIN_H = 300, 360  -- minimum resizable size\n"
    + T + "local MAX_W, MAX_H = 900, 900  -- maximum resizable size\n",
    "1. bigger window + min/max"
)

# 2. Scale floor 0.4 → 0.5
replace_once(
    T*2 + "local scale = math.clamp(math.min(scaleX, scaleY), 0.4, 1.0)\n",
    T*2 + "local scale = math.clamp(math.min(scaleX, scaleY), 0.5, 1.0)  -- [FIX] floor 0.5 (was 0.4)\n",
    "2. scale floor 0.5"
)

# 3. Content padding
replace_once(
    T*2 + "local pLayout = Instance.new(\"UIListLayout\")\n"
    + T*2 + "pLayout.Padding = UDim.new(0, 6)\n"
    + T*2 + "pLayout.SortOrder = Enum.SortOrder.LayoutOrder\n"
    + T*2 + "pLayout.Parent = page\n"
    + T*2 + "pad(page, 10, 10, 9, 10)\n",

    T*2 + "local pLayout = Instance.new(\"UIListLayout\")\n"
    + T*2 + "pLayout.Padding = UDim.new(0, 8)  -- [FIX] 8px between items (was 6, cramped)\n"
    + T*2 + "pLayout.SortOrder = Enum.SortOrder.LayoutOrder\n"
    + T*2 + "pLayout.Parent = page\n"
    + T*2 + "pad(page, 12, 12, 11, 12)  -- [FIX] 12px page padding (was 10)\n",
    "3. content padding"
)

# 4. Minimize: remove BODY_H_FULL capture, recompute on restore
replace_once(
    T + "local minimized = false\n"
    + T + "local BODY_H_FULL = WIN_H - HEADER_H\n"
    + T + "minBtn.MouseButton1Click:Connect(function()\n"
    + T*2 + "minimized = not minimized\n"
    + T*2 + "if minimized then\n"
    + T*3 + "tabBar.Visible = false\n"
    + T*3 + "content.Visible = false\n"
    + T*3 + "statusBar.Visible = false\n"
    + T*3 + "Tween(frame, TMIN, { Size = UDim2.new(0, WIN_W, 0, HEADER_H) })\n"
    + T*3 + "Tween(body, TMIN, { Size = UDim2.new(1, 0, 0, 0) })\n"
    + T*3 + "Tween(shadow, TMIN, { Size = UDim2.new(0, WIN_W + 36, 0, HEADER_H + 36) })\n"
    + T*3 + "Tween(minGlyph, T20, { Rotation = 180 })\n"
    + T*2 + "else\n"
    + T*3 + "tabBar.Visible = true\n"
    + T*3 + "content.Visible = true\n"
    + T*3 + "statusBar.Visible = true\n"
    + T*3 + "Tween(frame, TMIN, { Size = UDim2.new(0, WIN_W, 0, WIN_H) })\n"
    + T*3 + "Tween(body, TMIN, { Size = UDim2.new(1, 0, 0, BODY_H_FULL) })\n"
    + T*3 + "Tween(shadow, TMIN, { Size = UDim2.new(0, WIN_W + 36, 0, WIN_H + 36) })\n"
    + T*3 + "Tween(minGlyph, T20, { Rotation = 0 })\n"
    + T*2 + "end\n"
    + T + "end)",

    T + "local minimized = false\n"
    + T + "minBtn.MouseButton1Click:Connect(function()\n"
    + T*2 + "minimized = not minimized\n"
    + T*2 + "if minimized then\n"
    + T*3 + "tabBar.Visible = false\n"
    + T*3 + "content.Visible = false\n"
    + T*3 + "statusBar.Visible = false\n"
    + T*3 + "Tween(frame, TMIN, { Size = UDim2.new(0, WIN_W, 0, HEADER_H) })\n"
    + T*3 + "Tween(body, TMIN, { Size = UDim2.new(1, 0, 0, 0) })\n"
    + T*3 + "Tween(shadow, TMIN, { Size = UDim2.new(0, WIN_W + 36, 0, HEADER_H + 36) })\n"
    + T*3 + "Tween(minGlyph, T20, { Rotation = 180 })\n"
    + T*2 + "else\n"
    + T*3 + "tabBar.Visible = true\n"
    + T*3 + "content.Visible = true\n"
    + T*3 + "statusBar.Visible = true\n"
    + T*3 + "-- [FIX] recompute body height from current WIN_H (supports resize)\n"
    + T*3 + "Tween(frame, TMIN, { Size = UDim2.new(0, WIN_W, 0, WIN_H) })\n"
    + T*3 + "Tween(body, TMIN, { Size = UDim2.new(1, 0, 0, WIN_H - HEADER_H) })\n"
    + T*3 + "Tween(shadow, TMIN, { Size = UDim2.new(0, WIN_W + 36, 0, WIN_H + 36) })\n"
    + T*3 + "Tween(minGlyph, T20, { Rotation = 0 })\n"
    + T*2 + "end\n"
    + T + "end)",
    "4. minimize recomputes body height"
)

# 5. Add status bar drag + resize handle, inserted after the status bar onTheme block
replace_once(
    T + "onTheme(function()\n"
    + T*2 + "Tween(sTxt, T20, { TextColor3 = C.muted })\n"
    + T*2 + "Tween(sVer, T20, { TextColor3 = C.muted })\n"
    + T + "end)\n",

    T + "onTheme(function()\n"
    + T*2 + "Tween(sTxt, T20, { TextColor3 = C.muted })\n"
    + T*2 + "Tween(sVer, T20, { TextColor3 = C.muted })\n"
    + T + "end)\n"
    + "\n"
    + T + "-- [FIX] Make status bar draggable (move window from bottom too)\n"
    + T + "WindowJanitor:Add(statusBar.InputBegan:Connect(function(inp)\n"
    + T*2 + "if inp.UserInputType == Enum.UserInputType.MouseButton1\n"
    + T*3 + "or inp.UserInputType == Enum.UserInputType.Touch then\n"
    + T*2 + "local dragStart = inp.Position\n"
    + T*2 + "local startPos = frame.Position\n"
    + T*2 + "Tween(shadow, T15, { BackgroundTransparency = 0.65 })\n"
    + T*2 + "local vp = workspace.CurrentCamera and workspace.CurrentCamera.ViewportSize or Vector2.new(1920, 1080)\n"
    + T*2 + "registerDrag(\"statusbar\", function(pos)\n"
    + T*3 + "local d = pos - dragStart\n"
    + T*3 + "local nx = math.clamp(startPos.X.Offset + d.X, -WIN_W + 100, vp.X - 100)\n"
    + T*3 + "local ny = math.clamp(startPos.Y.Offset + d.Y, 0, vp.Y - 30)\n"
    + T*3 + "frame.Position = UDim2.new(0, nx, 0, ny)\n"
    + T*3 + "shadow.Position = UDim2.new(0, nx - 18, 0, ny - 18)\n"
    + T*2 + "end, function()\n"
    + T*3 + "Tween(shadow, T15, { BackgroundTransparency = 0.52 })\n"
    + T*2 + "end)\n"
    + T*2 + "end\n"
    + T + "end))\n"
    + "\n"
    + T + "-- [FIX] Resize handle (bottom-right corner) — drag to resize window\n"
    + T + "local resizeHandle = Instance.new(\"TextButton\")\n"
    + T + "resizeHandle.Name = \"ResizeHandle\"\n"
    + T + "resizeHandle.Size = UDim2.new(0, 22, 0, 22)\n"
    + T + "resizeHandle.Position = UDim2.new(1, -22, 1, -22)\n"
    + T + "resizeHandle.BackgroundColor3 = C.panelAlt\n"
    + T + "resizeHandle.BackgroundTransparency = 0.3\n"
    + T + "resizeHandle.Text = \"⇲\"\n"
    + T + "resizeHandle.TextColor3 = C.muted\n"
    + T + "resizeHandle.Font = Enum.Font.GothamBold\n"
    + T + "resizeHandle.TextSize = 12\n"
    + T + "resizeHandle.AutoButtonColor = false\n"
    + T + "resizeHandle.BorderSizePixel = 0\n"
    + T + "resizeHandle.ZIndex = 8\n"
    + T + "resizeHandle.Parent = frame\n"
    + T + "corner(resizeHandle, R.small)\n"
    + T + "local resizeStroke = stroke(resizeHandle, C.border, 1)\n"
    + T + "resizeHandle.MouseEnter:Connect(function()\n"
    + T*2 + "Tween(resizeHandle, T10, { BackgroundColor3 = C.panelHov, BackgroundTransparency = 0.1 })\n"
    + T*2 + "Tween(resizeHandle, T10, { TextColor3 = C.accent })\n"
    + T + "end)\n"
    + T + "resizeHandle.MouseLeave:Connect(function()\n"
    + T*2 + "Tween(resizeHandle, T10, { BackgroundColor3 = C.panelAlt, BackgroundTransparency = 0.3 })\n"
    + T*2 + "Tween(resizeHandle, T10, { TextColor3 = C.muted })\n"
    + T + "end)\n"
    + T + "WindowJanitor:Add(resizeHandle.InputBegan:Connect(function(inp)\n"
    + T*2 + "if inp.UserInputType == Enum.UserInputType.MouseButton1\n"
    + T*3 + "or inp.UserInputType == Enum.UserInputType.Touch then\n"
    + T*2 + "-- Lock top-left corner: record it in absolute pixels, resize from there\n"
    + T*2 + "local topLeft = frame.AbsolutePosition\n"
    + T*2 + "local dragStart = inp.Position\n"
    + T*2 + "local startW, startH = WIN_W, WIN_H\n"
    + T*2 + "Tween(shadow, T15, { BackgroundTransparency = 0.65 })\n"
    + T*2 + "registerDrag(\"resize\", function(pos)\n"
    + T*3 + "local d = pos - dragStart\n"
    + T*3 + "local newW = math.clamp(startW + d.X, MIN_W, MAX_W)\n"
    + T*3 + "local newH = math.clamp(startH + d.Y, MIN_H, MAX_H)\n"
    + T*3 + "WIN_W = newW\n"
    + T*3 + "WIN_H = newH\n"
    + T*3 + "frame.Position = UDim2.new(0, topLeft.X, 0, topLeft.Y)\n"
    + T*3 + "frame.Size = UDim2.new(0, newW, 0, newH)\n"
    + T*3 + "shadow.Position = UDim2.new(0, topLeft.X - 18, 0, topLeft.Y - 18)\n"
    + T*3 + "shadow.Size = UDim2.new(0, newW + 36, 0, newH + 36)\n"
    + T*3 + "if not minimized then\n"
    + T*4 + "body.Size = UDim2.new(1, 0, 0, newH - HEADER_H)\n"
    + T*3 + "end\n"
    + T*3 + "updateScale()\n"
    + T*2 + "end, function()\n"
    + T*3 + "Tween(shadow, T15, { BackgroundTransparency = 0.52 })\n"
    + T*2 + "end)\n"
    + T*2 + "end\n"
    + T + "end))\n"
    + T + "onTheme(function()\n"
    + T*2 + "Tween(resizeHandle, T20, { BackgroundColor3 = C.panelAlt })\n"
    + T*2 + "Tween(resizeStroke, T20, { Color = C.border })\n"
    + T + "end)\n",
    "5. resize handle + status bar drag"
)

with open(filepath, "w") as f:
    f.write(src)

print(f"\n{edits} edits applied.")
