#!/usr/bin/env python3
"""Round 6 fixes based on code review:

1. TAB CHIP AutomaticSize.X missing — fixed 90px, names >6 chars overflow
2. DRAG ROUTER cross-talk — multiple handlers fire simultaneously.
   Fix: single active drag instead of a table of handlers.
3. POPUP self-cleanup race — dropdown/color picker call closePopup() then
   set currentPopupCleanup = nil manually. Should call closeCurrentPopup()
   which handles both atomically.
4. SLIDER — verified NOT a bug (callback only fires on tap + drag end,
   not during drag move). No change needed.
"""
import sys

filepath = "/home/z/my-project/RezurXLib.lua"
with open(filepath, "r") as f:
    src = f.read()

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

# ── 1. Tab chip: add AutomaticSize.X + min size ──
replace_once(
    '\t\t\tbtn.Name = "TabChip"\n'
    '\t\t\tbtn.Size = UDim2.new(0, 90, 1, -10)\n'
    '\t\t\tbtn.Position = UDim2.new(0, 0, 0, 5)\n',

    '\t\t\tbtn.Name = "TabChip"\n'
    '\t\t\t-- [FIX] AutomaticSize.X so chip grows to fit text (was fixed 90px,\n'
    '\t\t\t-- names >6 chars overflowed). Min 90px via Size, auto-grows beyond.\n'
    '\t\t\tbtn.Size = UDim2.new(0, 90, 1, -10)\n'
    '\t\t\tbtn.AutomaticSize = Enum.AutomaticSize.X\n'
    '\t\t\tbtn.Position = UDim2.new(0, 0, 0, 5)\n',
    "1. tab chip AutomaticSize.X"
)

# Also need TextScaled off and proper text sizing for AutomaticSize to work
# GothamBold at 12px with the text — AutomaticSize.X needs TextXAlignment = Center
replace_once(
    '\t\t\tbtn.Text = (icon or "") .. "  " .. name\n'
    '\t\t\tbtn.Font = Enum.Font.GothamBold\n'
    '\t\t\tbtn.TextSize = 12\n'
    '\t\t\tbtn.TextColor3 = C.textDim\n',

    '\t\t\tbtn.Text = (icon or "") .. "  " .. name\n'
    '\t\t\tbtn.Font = Enum.Font.GothamBold\n'
    '\t\t\tbtn.TextSize = 12\n'
    '\t\t\tbtn.TextColor3 = C.textDim\n'
    '\t\t\tbtn.TextXAlignment = Enum.TextXAlignment.Center\n',
    "1b. tab chip TextXAlignment Center"
)

# ── 2. Drag router cross-talk fix — single active drag ──
# Replace the DragHandlers table + InputChanged/InputEnded with a single
# currentDrag variable.
old_drag_system = '''\tlocal DragHandlers = {}
\tlocal function registerDrag(key, moveFn, onEndFn, threshold)
\t\tDragHandlers[key] = {
\t\t\tmove      = moveFn,
\t\t\tonEnd     = onEndFn,
\t\t\tthreshold = threshold or 0,
\t\t\tstartPos  = nil,
\t\t\tarmed     = false,
\t\t}
\tend

\tWindowJanitor:Add(UserInputService.InputChanged:Connect(function(inp)
\t\tif inp.UserInputType == Enum.UserInputType.MouseMovement
\t\t\tor inp.UserInputType == Enum.UserInputType.Touch then
\t\t\tfor _, h in pairs(DragHandlers) do
\t\t\t\tif h.move then
\t\t\t\t\tif h.threshold > 0 and not h.armed then
\t\t\t\t\t\tif not h.startPos then
\t\t\t\t\t\t\th.startPos = inp.Position
\t\t\t\t\t\telseif (inp.Position - h.startPos).Magnitude >= h.threshold then
\t\t\t\t\t\t\th.armed = true
\t\t\t\t\t\tend
\t\t\t\t\tend
\t\t\t\t\tif h.threshold == 0 or h.armed then
\t\t\t\t\t\tpcall(h.move, inp.Position)
\t\t\t\t\tend
\t\t\t\tend
\t\t\tend
\t\tend
\tend))

\tWindowJanitor:Add(UserInputService.InputEnded:Connect(function(inp)
\t\tif inp.UserInputType == Enum.UserInputType.MouseButton1
\t\t\tor inp.UserInputType == Enum.UserInputType.Touch then
\t\t\tfor _, h in pairs(DragHandlers) do
\t\t\t\tif h.onEnd then pcall(h.onEnd) end
\t\t\tend
\t\t\ttable.clear(DragHandlers)
\t\tend
\tend))'''

new_drag_system = '''\t-- [FIX] Single active drag — prevents cross-talk where multiple
\t-- handlers fire simultaneously. Only one drag can be active at a time.
\tlocal currentDrag = nil
\tlocal function registerDrag(key, moveFn, onEndFn, threshold)
\t\tcurrentDrag = {
\t\t\tkey       = key,
\t\t\tmove      = moveFn,
\t\t\tonEnd     = onEndFn,
\t\t\tthreshold = threshold or 0,
\t\t\tstartPos  = nil,
\t\t\tarmed     = false,
\t\t}
\tend

\tWindowJanitor:Add(UserInputService.InputChanged:Connect(function(inp)
\t\tif inp.UserInputType == Enum.UserInputType.MouseMovement
\t\t\tor inp.UserInputType == Enum.UserInputType.Touch then
\t\t\tif currentDrag and currentDrag.move then
\t\t\t\tlocal h = currentDrag
\t\t\t\tif h.threshold > 0 and not h.armed then
\t\t\t\t\tif not h.startPos then
\t\t\t\t\t\th.startPos = inp.Position
\t\t\t\t\telseif (inp.Position - h.startPos).Magnitude >= h.threshold then
\t\t\t\t\t\th.armed = true
\t\t\t\t\tend
\t\t\t\tend
\t\t\t\tif h.threshold == 0 or h.armed then
\t\t\t\t\tpcall(h.move, inp.Position)
\t\t\t\tend
\t\t\tend
\t\tend
\tend))

\tWindowJanitor:Add(UserInputService.InputEnded:Connect(function(inp)
\t\tif inp.UserInputType == Enum.UserInputType.MouseButton1
\t\t\tor inp.UserInputType == Enum.UserInputType.Touch then
\t\t\tif currentDrag then
\t\t\t\tif currentDrag.onEnd then pcall(currentDrag.onEnd) end
\t\t\t\tcurrentDrag = nil
\t\t\tend
\t\tend
\tend))'''

replace_once(old_drag_system, new_drag_system, "2. drag router single-active")

# Also fix the Destroy function that references DragHandlers
replace_once(
    '\t\ttable.clear(DragHandlers)',
    '\t\tcurrentDrag = nil',
    "2b. Destroy clears currentDrag"
)

# ── 3. Dropdown popup self-cleanup race ──
# Replace the manual closePopup() + currentPopupCleanup = nil pattern
# with closeCurrentPopup() which is atomic.
replace_once(
    '''\t\t\t\t\t\t\t\trefreshLabel()
\t\t\t\t\t\t\t\tclosePopup()
\t\t\t\t\t\t\t\tcurrentPopupCleanup = nil
\t\t\t\t\t\t\t\tfire()''',

    '''\t\t\t\t\t\t\t\trefreshLabel()
\t\t\t\t\t\t\t\tcloseCurrentPopup()
\t\t\t\t\t\t\t\tfire()''',
    "3a. dropdown single-select uses closeCurrentPopup"
)

replace_once(
    '''\t\t\t\tcatcher.MouseButton1Click:Connect(function()
\t\t\t\t\t\tclosePopup()
\t\t\t\t\t\tcurrentPopupCleanup = nil
\t\t\t\t\tend)''',

    '''\t\t\t\tcatcher.MouseButton1Click:Connect(closeCurrentPopup)''',
    "3b. dropdown catcher uses closeCurrentPopup"
)

# Color picker — same fix
replace_once(
    '''\t\t\t\tdoneBtn.MouseButton1Click:Connect(function()
\t\t\t\t\tclosePopup()
\t\t\t\t\tcurrentPopupCleanup = nil
\t\t\t\tend)
\t\t\t\tcatcher.MouseButton1Click:Connect(function()
\t\t\t\t\tclosePopup()
\t\t\t\t\tcurrentPopupCleanup = nil
\t\t\t\tend)''',

    '''\t\t\t\tdoneBtn.MouseButton1Click:Connect(closeCurrentPopup)
\t\t\t\tcatcher.MouseButton1Click:Connect(closeCurrentPopup)''',
    "3c. color picker uses closeCurrentPopup"
)

with open(filepath, "w") as f:
    f.write(src)

print(f"\n{edits} edits applied.")
