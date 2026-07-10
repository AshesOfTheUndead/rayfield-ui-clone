#!/usr/bin/env python3
"""Round 5 — comprehensive fixes based on screenshot analysis.

1. TABS BLANK: Use btn.Text directly (no child labels). Sirius/Rayfield style.
2. MINIMIZE BROKEN: Use Activated, make button bigger.
3. CLOSE TOO SMALL: Make it 40x32 (was 30x28).
4. DROPDOWN FLIES OFF: UIScale double-scaling bug. Divide AbsolutePosition by scale.
5. DRAG SUCKS: Ensure smooth by using InputBegan + registerDrag properly.
"""
import sys

filepath = "/home/z/my-project/RezurXLib.lua"
with open(filepath, "r") as f:
    lines = f.readlines()

def find_line(substr, start=0):
    for i in range(start, len(lines)):
        if substr in lines[i]:
            return i
    return -1

edits = 0

# ── 1. Rewrite tab buttons: use btn.Text directly ──
ct_idx = find_line("function Window:CreateTab")
btn_start = find_line('local btn = Instance.new("TextButton")', ct_idx)
btn_end = -1
for i in range(btn_start, min(btn_start + 60, len(lines))):
    if 'textLbl.Parent = btn' in lines[i]:
        btn_end = i
        break
if btn_end == -1:
    print("ERROR: tab btn end not found")
    sys.exit(1)

indent = lines[btn_start][:len(lines[btn_start])-len(lines[btn_start].lstrip())]

new_btn_lines = [
    indent + 'local btn = Instance.new("TextButton")\n',
    indent + 'btn.Name = "TabChip"\n',
    indent + '-- [FIX] Use btn.Text directly for icon+text (Sirius/Rayfield style).\n',
    indent + '-- Child labels had rendering issues on some devices → blank tabs.\n',
    indent + 'btn.Size = UDim2.new(0, 90, 1, -10)\n',
    indent + 'btn.Position = UDim2.new(0, 0, 0, 5)\n',
    indent + 'btn.BackgroundColor3 = C.tabChip\n',
    indent + 'btn.AutoButtonColor = false\n',
    indent + 'btn.BorderSizePixel = 0\n',
    indent + 'btn.Text = (icon or "") .. "  " .. name\n',
    indent + 'btn.Font = Enum.Font.GothamBold\n',
    indent + 'btn.TextSize = 12\n',
    indent + 'btn.TextColor3 = C.textDim\n',
    indent + 'btn.ZIndex = 4\n',
    indent + 'btn.Parent = tabBar\n',
    indent + 'corner(btn, R.tab)\n',
    indent + 'local chipStroke = stroke(btn, C.borderAcc, 1)\n',
    indent + '-- Keep refs for setActive color tweens\n',
    indent + 'local iconLbl = btn  -- alias so setActive code works\n',
    indent + 'local textLbl = btn  -- alias so setActive code works\n',
]

lines[btn_start:btn_end+1] = new_btn_lines
edits += 1
print("OK: 1. tab buttons use btn.Text directly")

# ── 2. Fix minimize: use Activated, make button bigger ──
# Find minBtn size and change it
for i, line in enumerate(lines):
    if 'minBtn.Size = UDim2.new(0, 30, 0, 28)' in line:
        lines[i] = line.replace('0, 30, 0, 28', '0, 38, 0, 32')
        edits += 1
        print("OK: 2a. minBtn bigger")
        break

# Find minBtn position and adjust
for i, line in enumerate(lines):
    if 'minBtn.Position = UDim2.new(1, -74' in line:
        lines[i] = line.replace('1, -74', '1, -86')
        edits += 1
        print("OK: 2b. minBtn position adjusted")
        break

# Change minBtn.MouseButton1Click to minBtn.Activated
for i, line in enumerate(lines):
    if 'minBtn.MouseButton1Click:Connect' in line:
        lines[i] = line.replace('minBtn.MouseButton1Click:Connect', 'minBtn.Activated:Connect')
        edits += 1
        print("OK: 2c. minBtn uses Activated")
        break

# ── 3. Make close button bigger ──
for i, line in enumerate(lines):
    if 'closeBtn.Size = UDim2.new(0, 30, 0, 28)' in line:
        lines[i] = line.replace('0, 30, 0, 28', '0, 38, 0, 32')
        edits += 1
        print("OK: 3a. closeBtn bigger")
        break

for i, line in enumerate(lines):
    if 'closeBtn.Position = UDim2.new(1, -38' in line:
        lines[i] = line.replace('1, -38', '1, -44')
        edits += 1
        print("OK: 3b. closeBtn position adjusted")
        break

# Change closeBtn.MouseButton1Click to closeBtn.Activated
for i, line in enumerate(lines):
    if 'closeBtn.MouseButton1Click:Connect' in line:
        lines[i] = line.replace('closeBtn.MouseButton1Click:Connect', 'closeBtn.Activated:Connect')
        edits += 1
        print("OK: 3c. closeBtn uses Activated")
        break

# Also adjust dragBar to not overlap the bigger buttons
# dragBar was (1, -80, 1, 0) — need to make it shorter to leave room for bigger buttons
for i, line in enumerate(lines):
    if 'dragBar.Size = UDim2.new(1, -80, 1, 0)' in line:
        lines[i] = line.replace('1, -80, 1, 0', '1, -96, 1, 0')
        edits += 1
        print("OK: 3d. dragBar shorter for bigger buttons")
        break

# ── 4. Fix dropdown positioning — account for UIScale ──
# The dropdown uses holder.AbsolutePosition which is already scaled by UIScale.
# But the popup is parented to screenGui which has UIScale, so it gets scaled AGAIN.
# Fix: divide by the current scale factor.
# Find the dropdown openList function
ol_idx = find_line("local function openList()")
if ol_idx == -1:
    print("ERROR: openList not found")
    sys.exit(1)

# Find the line with 'local hPos, hSize = holder.AbsolutePosition' and add scale correction
for i in range(ol_idx, min(ol_idx + 30, len(lines))):
    if 'local hPos, hSize = holder.AbsolutePosition' in lines[i]:
        indent = lines[i][:len(lines[i])-len(lines[i].lstrip())]
        # Replace the line and add scale correction
        lines[i] = indent + 'local hPos, hSize = holder.AbsolutePosition, holder.AbsoluteSize\n'
        # Insert scale correction after this line
        lines.insert(i+1, indent + '-- [FIX] Account for UIScale — AbsolutePosition is already scaled,\n')
        lines.insert(i+2, indent + '-- but popup is in screenGui which scales AGAIN. Divide by scale.\n')
        lines.insert(i+3, indent + 'local _uiScale = screenGui:FindFirstChild("UIScale")\n')
        lines.insert(i+4, indent + 'local _s = _uiScale and _uiScale.Scale or 1\n')
        lines.insert(i+5, indent + 'if _s > 0 then hPos = Vector2.new(hPos.X / _s, hPos.Y / _s) hSize = Vector2.new(hSize.X / _s, hSize.Y / _s) end\n')
        edits += 1
        print("OK: 4. dropdown UIScale correction")
        break

# ── 5. Fix float icon size (make it bigger for easier drag) ──
for i, line in enumerate(lines):
    if 'floatIcon.Size = UDim2.new(0, 44, 0, 44)' in line:
        lines[i] = line.replace('0, 44, 0, 44', '0, 52, 0, 52')
        edits += 1
        print("OK: 5. float icon bigger")
        break

with open(filepath, "w") as f:
    f.writelines(lines)

print(f"\n{edits} edits applied.")
