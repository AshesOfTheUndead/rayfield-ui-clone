#!/usr/bin/env python3
"""Fix tab onTheme/MouseEnter/MouseLeave to use btn directly (no textLbl alias)
and use C.borderAcc (orange) for inactive tab outlines."""
import sys

filepath = "/home/z/my-project/RezurXLib.lua"
with open(filepath, "r") as f:
    src = f.read()

# Replace the onTheme block for tabs
old_ontheme = """                onTheme(function()
                        page.ScrollBarImageColor3 = C.accent
                        if ActiveTab == tab then
                                Tween(iconLbl, T20, { TextColor3 = C.accentHi })
                                Tween(textLbl, T20, { TextColor3 = C.accentHi })
                        else
                                Tween(btn, T20, { BackgroundColor3 = C.tabChip })
                                Tween(chipStroke, T20, { Color = C.border })
                                Tween(iconLbl, T20, { TextColor3 = C.textDim })
                                Tween(textLbl, T20, { TextColor3 = C.textDim })
                        end
                end)"""

new_ontheme = """                onTheme(function()
                        page.ScrollBarImageColor3 = C.accent
                        if ActiveTab == tab then
                                Tween(btn, T20, { TextColor3 = C.accentHi })
                        else
                                Tween(btn, T20, { BackgroundColor3 = C.tabChip })
                                Tween(chipStroke, T20, { Color = C.borderAcc })
                                Tween(btn, T20, { TextColor3 = C.textDim })
                        end
                end)"""

if old_ontheme in src:
    src = src.replace(old_ontheme, new_ontheme, 1)
    print("OK: onTheme fixed")
else:
    print("ERROR: onTheme not found")
    sys.exit(1)

# Replace MouseEnter
old_enter = """                btn.MouseEnter:Connect(function()
                        if ActiveTab ~= tab then
                                Tween(btn, T10, { BackgroundColor3 = C.tabChipHov })  -- hover
                                Tween(chipStroke, T10, { Color = C.accentDim })  -- hover orange
                                Tween(iconLbl, T10, { TextColor3 = C.text })
                                Tween(textLbl, T10, { TextColor3 = C.text })
                                Tween(btn, TPRESS, { Position = UDim2.new(0, btn.Position.X.Offset, 0, 4) })
                        end
                end)"""

new_enter = """                btn.MouseEnter:Connect(function()
                        if ActiveTab ~= tab then
                                Tween(btn, T10, { BackgroundColor3 = C.tabChipHov })
                                Tween(chipStroke, T10, { Color = C.accentDim })
                                Tween(btn, T10, { TextColor3 = C.text })
                        end
                end)"""

if old_enter in src:
    src = src.replace(old_enter, new_enter, 1)
    print("OK: MouseEnter fixed")
else:
    print("ERROR: MouseEnter not found")
    sys.exit(1)

# Replace MouseLeave
old_leave = """                btn.MouseLeave:Connect(function()
                        if ActiveTab ~= tab then
                                Tween(btn, T10, { BackgroundColor3 = C.tabChip })
                                Tween(chipStroke, T10, { Color = C.border })
                                Tween(iconLbl, T10, { TextColor3 = C.textDim })
                                Tween(textLbl, T10, { TextColor3 = C.textDim })
                        end
                        Tween(btn, TPRESS, { Position = UDim2.new(0, btn.Position.X.Offset, 0, 5) })"""

new_leave = """                btn.MouseLeave:Connect(function()
                        if ActiveTab ~= tab then
                                Tween(btn, T10, { BackgroundColor3 = C.tabChip })
                                Tween(chipStroke, T10, { Color = C.borderAcc })
                                Tween(btn, T10, { TextColor3 = C.textDim })
                        end"""

if old_leave in src:
    src = src.replace(old_leave, new_leave, 1)
    print("OK: MouseLeave fixed")
else:
    print("ERROR: MouseLeave not found")
    sys.exit(1)

with open(filepath, "w") as f:
    f.write(src)

print("All tab theme/hover fixes applied.")
