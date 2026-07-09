#!/usr/bin/env python3
"""Round 4 — comprehensive fixes. Uses line-by-line replacement to avoid
indentation matching issues."""
import sys
import re

filepath = "/home/z/my-project/RezurXLib.lua"
with open(filepath, "r") as f:
    lines = f.readlines()

# Helper: find a line by substring, return 0-based index
def find_line(substr, start=0):
    for i in range(start, len(lines)):
        if substr in lines[i]:
            return i
    return -1

# Helper: replace a range of lines (inclusive) with new content
def replace_lines(start_idx, end_idx, new_lines, label):
    global lines
    lines[start_idx:end_idx+1] = new_lines
    print(f"OK: {label} (lines {start_idx+1}-{end_idx+1})")

edits = 0

# ── 1. Bigger window: 420x480 → 460x500 ──
for i, line in enumerate(lines):
    if "or 420  -- bigger (was 320, text was cramped)" in line:
        lines[i] = line.replace("420", "460").replace("was 320, text was cramped", "was 420")
        edits += 1
        print(f"OK: 1. WIN_W 420→460")
        break
for i, line in enumerate(lines):
    if "or 480  -- bigger (was 380)" in line:
        lines[i] = line.replace("480", "500").replace("was 380", "was 480")
        edits += 1
        print(f"OK: 1. WIN_H 480→500")
        break

# ── 2a. Fix window drag: replace 'local startPos = frame.Position' with AbsolutePosition ──
# And replace startPos.X.Offset with startAbs.X in the window drag handler
# Find the dragBar drag handler
dragbar_idx = find_line("WindowJanitor:Add(dragBar.InputBegan:Connect")
if dragbar_idx == -1:
    print("ERROR: dragBar handler not found")
    sys.exit(1)

# Replace 'local startPos = frame.Position' with 'local startAbs = frame.AbsolutePosition'
# within the next 20 lines after dragbar_idx
for i in range(dragbar_idx, min(dragbar_idx + 20, len(lines))):
    if "local startPos = frame.Position" in lines[i]:
        lines[i] = lines[i].replace("local startPos = frame.Position",
                                     "-- [FIX] Use AbsolutePosition (screen pixels) not Position.Offset\n"
                                     + (lines[i][:len(lines[i])-len(lines[i].lstrip())])
                                     + "-- Position has scale 0.5/0.55, .Offset gives -WIN_W/2 → flinging\n"
                                     + (lines[i][:len(lines[i])-len(lines[i].lstrip())])
                                     + "local startAbs = frame.AbsolutePosition")
        edits += 1
        print(f"OK: 2a. window drag: startPos→startAbs")
        break

# Replace startPos.X.Offset with startAbs.X and startPos.Y.Offset with startAbs.Y
# in the window drag handler (next 15 lines)
for i in range(dragbar_idx, min(dragbar_idx + 25, len(lines))):
    if "startPos.X.Offset" in lines[i] and "registerDrag" not in lines[i]:
        lines[i] = lines[i].replace("startPos.X.Offset", "startAbs.X")
    if "startPos.Y.Offset" in lines[i] and "registerDrag" not in lines[i]:
        lines[i] = lines[i].replace("startPos.Y.Offset", "startAbs.Y")

# ── 2b. Fix status bar drag: same fix ──
sb_idx = find_line("WindowJanitor:Add(statusBar.InputBegan:Connect")
if sb_idx == -1:
    print("ERROR: statusBar handler not found")
    sys.exit(1)

for i in range(sb_idx, min(sb_idx + 20, len(lines))):
    if "local startPos = frame.Position" in lines[i]:
        indent = lines[i][:len(lines[i])-len(lines[i].lstrip())]
        lines[i] = (indent + "local startAbs = frame.AbsolutePosition  -- [FIX] screen pixels\n")
        edits += 1
        print(f"OK: 2b. status bar drag: startPos→startAbs")
        break

for i in range(sb_idx, min(sb_idx + 25, len(lines))):
    if "startPos.X.Offset" in lines[i]:
        lines[i] = lines[i].replace("startPos.X.Offset", "startAbs.X")
    if "startPos.Y.Offset" in lines[i]:
        lines[i] = lines[i].replace("startPos.Y.Offset", "startAbs.Y")

# ── 3. Float icon: add drag threshold + AbsolutePosition ──
fi_idx = find_line("floatIcon.InputBegan:Connect")
if fi_idx == -1:
    print("ERROR: floatIcon.InputBegan not found")
    sys.exit(1)

# Add floatDragMoved variable before the InputBegan
indent = lines[fi_idx][:len(lines[fi_idx])-len(lines[fi_idx].lstrip())]
lines.insert(fi_idx, indent + "-- [FIX] Track movement so tap (restore) vs drag (move) is distinguished\n")
lines.insert(fi_idx+1, indent + "local floatDragMoved = false\n")
fi_idx += 2  # adjust for inserts

# In the floatIcon InputBegan, replace startPos with startAbs, add floatDragMoved=false
for i in range(fi_idx, min(fi_idx + 15, len(lines))):
    if "local startPos = floatIcon.Position" in lines[i]:
        indent = lines[i][:len(lines[i])-len(lines[i].lstrip())]
        lines[i] = indent + "local startAbs = floatIcon.AbsolutePosition  -- [FIX] screen pixels\n"
        # Insert floatDragMoved = false after this line
        lines.insert(i+1, indent + "floatDragMoved = false\n")
        break

# In the registerDrag callback, add movement threshold check
for i in range(fi_idx, min(fi_idx + 20, len(lines))):
    if "local d = pos - startDrag" in lines[i] and i < len(lines) - 1:
        indent = lines[i+1][:len(lines[i+1])-len(lines[i+1].lstrip())]
        # Check if threshold line already exists
        if "floatDragMoved = true" not in lines[i+1]:
            lines.insert(i+1, indent + "if d.Magnitude > 6 then floatDragMoved = true end  -- threshold\n")
        break

# Replace startPos.X.Offset / startPos.Y.Offset in floatIcon handler
for i in range(fi_idx, min(fi_idx + 20, len(lines))):
    if "startPos.X.Offset" in lines[i]:
        lines[i] = lines[i].replace("startPos.X.Offset", "startAbs.X")
    if "startPos.Y.Offset" in lines[i]:
        lines[i] = lines[i].replace("startPos.Y.Offset", "startAbs.Y")

# Add 'if floatDragMoved then return end' at the start of Activated handler
fa_idx = find_line("floatIcon.Activated:Connect")
if fa_idx >= 0:
    for i in range(fa_idx, min(fa_idx + 5, len(lines))):
        if "floatIcon.Visible = false" in lines[i]:
            indent = lines[i][:len(lines[i])-len(lines[i].lstrip())]
            lines.insert(i, indent + "if floatDragMoved then return end  -- [FIX] was a drag, not a tap\n")
            edits += 1
            print(f"OK: 3. float icon drag threshold + tap guard")
            break

edits += 2  # for the float icon changes

# ── 4. Tab buttons: replace entire creation block ──
# Find 'local btn = Instance.new("TextButton")' inside CreateTab
ct_idx = find_line("function Window:CreateTab")
if ct_idx == -1:
    print("ERROR: CreateTab not found")
    sys.exit(1)

btn_start = find_line('local btn = Instance.new("TextButton")', ct_idx)
if btn_start == -1:
    print("ERROR: tab btn not found")
    sys.exit(1)

# Find the end: 'textLbl.Parent = btn' after btn_start
btn_end = -1
for i in range(btn_start, min(btn_start + 50, len(lines))):
    if 'textLbl.Parent = btn' in lines[i]:
        btn_end = i
        break
if btn_end == -1:
    print("ERROR: textLbl.Parent not found")
    sys.exit(1)

# Get the indentation of the btn line
indent = lines[btn_start][:len(lines[btn_start])-len(lines[btn_start].lstrip())]

new_btn_lines = [
    indent + 'local btn = Instance.new("TextButton")\n',
    indent + 'btn.Name = "TabChip"\n',
    indent + '-- [FIX] Fixed width, no AutomaticSize, no UIListLayout.\n',
    indent + '-- AutomaticSize + UIListLayout caused circular layout → 0-size → blank tabs.\n',
    indent + 'btn.Size = UDim2.new(0, 88, 1, -10)\n',
    indent + 'btn.Position = UDim2.new(0, 0, 0, 5)\n',
    indent + 'btn.BackgroundColor3 = C.tabChip\n',
    indent + 'btn.AutoButtonColor = false\n',
    indent + 'btn.BorderSizePixel = 0\n',
    indent + 'btn.Text = ""\n',
    indent + 'btn.ZIndex = 4\n',
    indent + 'btn.Parent = tabBar\n',
    indent + 'corner(btn, R.tab)\n',
    indent + 'local chipStroke = stroke(btn, C.borderAcc, 1)\n',
    indent + '\n',
    indent + '-- [FIX] Icon at fixed position (left, 8px margin)\n',
    indent + 'local iconLbl = Instance.new("TextLabel")\n',
    indent + 'iconLbl.Size = UDim2.new(0, 20, 1, 0)\n',
    indent + 'iconLbl.Position = UDim2.new(0, 8, 0, 0)\n',
    indent + 'iconLbl.BackgroundTransparency = 1\n',
    indent + 'iconLbl.Font = Enum.Font.GothamBold\n',
    indent + 'iconLbl.TextSize = 13\n',
    indent + 'iconLbl.TextColor3 = C.textDim\n',
    indent + 'iconLbl.Text = icon or ""\n',
    indent + 'iconLbl.ZIndex = 5\n',
    indent + 'iconLbl.Parent = btn\n',
    indent + '\n',
    indent + '-- [FIX] Text fills remaining width, left-aligned after icon\n',
    indent + 'local textLbl = Instance.new("TextLabel")\n',
    indent + 'textLbl.Size = UDim2.new(1, -34, 1, 0)\n',
    indent + 'textLbl.Position = UDim2.new(0, 30, 0, 0)\n',
    indent + 'textLbl.BackgroundTransparency = 1\n',
    indent + 'textLbl.Font = Enum.Font.GothamBold\n',
    indent + 'textLbl.TextSize = 12\n',
    indent + 'textLbl.TextColor3 = C.textDim\n',
    indent + 'textLbl.TextXAlignment = Enum.TextXAlignment.Left\n',
    indent + 'textLbl.Text = name\n',
    indent + 'textLbl.ZIndex = 5\n',
    indent + 'textLbl.Parent = btn\n',
]

lines[btn_start:btn_end+1] = new_btn_lines
edits += 1
print(f"OK: 4. tab buttons fixed positions")

# ── 5. Toggle ON state: set initial stroke color ──
# Find 'local holder, hStroke = makeHolder(42)' in CreateToggle
ct_idx = find_line("function tab:CreateToggle")
if ct_idx == -1:
    print("ERROR: CreateToggle not found")
    sys.exit(1)

for i in range(ct_idx, min(ct_idx + 20, len(lines))):
    if 'local holder, hStroke = makeHolder(42)' in lines[i]:
        indent = lines[i][:len(lines[i])-len(lines[i].lstrip())]
        lines.insert(i+1, indent + '-- [FIX] If toggle starts ON, outline the holder immediately\n')
        lines.insert(i+2, indent + 'if state then hStroke.Color = C.accentDim end\n')
        edits += 1
        print(f"OK: 5. toggle ON initial stroke")
        break

# ── 6. moveIndicatorTo: use absolute position ──
for i, line in enumerate(lines):
    if 'local relX = btn.Position.X.Offset' in line:
        lines[i] = line.replace('local relX = btn.Position.X.Offset',
                                '-- [FIX] Use absolute position relative to tabBar\n'
                                + line[:len(line)-len(line.lstrip())]
                                + 'local relX = btn.AbsolutePosition.X - tabBar.AbsolutePosition.X')
        edits += 1
        print(f"OK: 6. moveIndicatorTo absolute position")
        break

with open(filepath, "w") as f:
    f.writelines(lines)

print(f"\n{edits} edits applied.")
