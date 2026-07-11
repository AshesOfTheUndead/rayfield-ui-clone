#!/usr/bin/env python3
"""Merge v2.0 features into v1.0 base — corrected indentation."""
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
        print(f"ERROR: {label} — found {src.count(old)} times")
        sys.exit(1)
    src = src.replace(old, new, 1)
    edits += 1
    print(f"OK: {label}")

# 1. HttpService
replace_once(
    'local CoreGui          = game:GetService("CoreGui")\n'
    'local TextService      = game:GetService("TextService")',
    'local CoreGui          = game:GetService("CoreGui")\n'
    'local TextService      = game:GetService("TextService")\n'
    'local HttpService      = game:GetService("HttpService")',
    "1. HttpService"
)

# 2. Extra themes
replace_once(
    '\t\tindGradA  = Color3.fromRGB(40, 70, 34),\n'
    '\t\tindGradB  = Color3.fromRGB(26, 48, 22),\n'
    '\t},\n'
    '}',
    '\t\tindGradA  = Color3.fromRGB(40, 70, 34),\n'
    '\t\tindGradB  = Color3.fromRGB(26, 48, 22),\n'
    '\t},\n'
    '\tMidnight = {\n'
    '\t\tbg=Color3.fromRGB(6,6,12),panel=Color3.fromRGB(16,16,28),panelAlt=Color3.fromRGB(24,24,40),panelHov=Color3.fromRGB(34,34,54),\n'
    '\t\taccent=Color3.fromRGB(140,110,255),accentHi=Color3.fromRGB(175,150,255),accentDim=Color3.fromRGB(90,70,180),accentDark=Color3.fromRGB(40,30,80),\n'
    '\t\ttext=Color3.fromRGB(228,228,248),textDim=Color3.fromRGB(165,165,200),muted=Color3.fromRGB(100,100,140),\n'
    '\t\tgreen=Color3.fromRGB(48,215,92),greenDim=Color3.fromRGB(22,75,38),yellow=Color3.fromRGB(255,210,48),red=Color3.fromRGB(225,58,58),\n'
    '\t\tborder=Color3.fromRGB(40,40,64),track=Color3.fromRGB(32,32,52),white=Color3.fromRGB(255,255,255),black=Color3.fromRGB(0,0,0),\n'
    '\t\ttabBarBg=Color3.fromRGB(10,10,18),tabChip=Color3.fromRGB(28,28,46),tabChipHov=Color3.fromRGB(40,40,62),\n'
    '\t\theaderA=Color3.fromRGB(22,22,38),headerB=Color3.fromRGB(14,14,24),indGradA=Color3.fromRGB(50,36,100),indGradB=Color3.fromRGB(32,22,66),\n'
    '\t},\n'
    '\tForest = {\n'
    '\t\tbg=Color3.fromRGB(8,14,10),panel=Color3.fromRGB(18,28,20),panelAlt=Color3.fromRGB(26,38,28),panelHov=Color3.fromRGB(34,50,36),\n'
    '\t\taccent=Color3.fromRGB(80,200,100),accentHi=Color3.fromRGB(120,230,140),accentDim=Color3.fromRGB(50,140,65),accentDark=Color3.fromRGB(22,60,30),\n'
    '\t\ttext=Color3.fromRGB(228,240,230),textDim=Color3.fromRGB(165,185,170),muted=Color3.fromRGB(100,120,105),\n'
    '\t\tgreen=Color3.fromRGB(48,215,92),greenDim=Color3.fromRGB(22,75,38),yellow=Color3.fromRGB(255,210,48),red=Color3.fromRGB(225,58,58),\n'
    '\t\tborder=Color3.fromRGB(36,50,40),track=Color3.fromRGB(28,40,32),white=Color3.fromRGB(255,255,255),black=Color3.fromRGB(0,0,0),\n'
    '\t\ttabBarBg=Color3.fromRGB(12,18,13),tabChip=Color3.fromRGB(26,38,28),tabChipHov=Color3.fromRGB(36,52,38),\n'
    '\t\theaderA=Color3.fromRGB(22,34,24),headerB=Color3.fromRGB(14,22,16),indGradA=Color3.fromRGB(30,80,38),indGradB=Color3.fromRGB(20,54,26),\n'
    '\t},\n'
    '\tCoral = {\n'
    '\t\tbg=Color3.fromRGB(14,8,10),panel=Color3.fromRGB(28,18,22),panelAlt=Color3.fromRGB(40,26,32),panelHov=Color3.fromRGB(54,34,42),\n'
    '\t\taccent=Color3.fromRGB(255,130,140),accentHi=Color3.fromRGB(255,165,175),accentDim=Color3.fromRGB(195,80,90),accentDark=Color3.fromRGB(80,30,36),\n'
    '\t\ttext=Color3.fromRGB(248,232,234),textDim=Color3.fromRGB(200,168,174),muted=Color3.fromRGB(145,104,112),\n'
    '\t\tgreen=Color3.fromRGB(48,215,92),greenDim=Color3.fromRGB(22,75,38),yellow=Color3.fromRGB(255,210,48),red=Color3.fromRGB(225,58,58),\n'
    '\t\tborder=Color3.fromRGB(66,42,48),track=Color3.fromRGB(54,34,40),white=Color3.fromRGB(255,255,255),black=Color3.fromRGB(0,0,0),\n'
    '\t\ttabBarBg=Color3.fromRGB(18,11,13),tabChip=Color3.fromRGB(46,30,34),tabChipHov=Color3.fromRGB(60,40,46),\n'
    '\t\theaderA=Color3.fromRGB(38,22,28),headerB=Color3.fromRGB(22,13,16),indGradA=Color3.fromRGB(100,30,40),indGradB=Color3.fromRGB(66,18,26),\n'
    '\t},\n'
    '}',
    "2. extra themes"
)

# 3. Tooltip system
tooltip_block = '''-- ============================================================
-- TOOLTIP SYSTEM — hover-activated info labels
-- ============================================================
local tooltipFrame = nil
local tooltipText = nil
local tooltipStroke = nil

local function initTooltip()
\tif tooltipFrame then return end
\ttooltipFrame = Instance.new("Frame")
\ttooltipFrame.Name = "Tooltip"
\ttooltipFrame.Size = UDim2.new(0, 0, 0, 24)
\ttooltipFrame.BackgroundColor3 = C.panelAlt
\ttooltipFrame.BackgroundTransparency = 0.05
\ttooltipFrame.BorderSizePixel = 0
\ttooltipFrame.ZIndex = 200
\ttooltipFrame.Visible = false
\tpcall(function() tooltipFrame.Parent = CoreGui end)
\tif not tooltipFrame.Parent then tooltipFrame.Parent = playerGui end
\tcorner(tooltipFrame, R.small)
\ttooltipStroke = stroke(tooltipFrame, C.border, 1)
\ttooltipText = Instance.new("TextLabel")
\ttooltipText.Name = "Text"
\ttooltipText.Size = UDim2.new(1, -12, 1, 0)
\ttooltipText.Position = UDim2.new(0, 6, 0, 0)
\ttooltipText.BackgroundTransparency = 1
\ttooltipText.Font = Enum.Font.GothamMedium
\ttooltipText.TextSize = 11
\ttooltipText.TextColor3 = C.textDim
\ttooltipText.ZIndex = 201
\ttooltipText.Parent = tooltipFrame
end

local function showTooltip(text, anchorGui)
\tif not text or text == "" then return end
\tinitTooltip()
\ttooltipText.Text = text
\ttooltipFrame.Visible = true
\ttooltipFrame.BackgroundColor3 = C.panelAlt
\ttooltipStroke.Color = C.border
\ttooltipText.TextColor3 = C.textDim
\tlocal txtSize = TextService:GetTextSize(text, 11, Enum.Font.GothamMedium, Vector2.new(400, 24))
\ttooltipFrame.Size = UDim2.new(0, txtSize.X + 14, 0, 26)
\tif anchorGui and anchorGui.AbsolutePosition then
\t\tlocal pos = anchorGui.AbsolutePosition
\t\tlocal size = anchorGui.AbsoluteSize
\t\ttooltipFrame.Position = UDim2.new(0, pos.X, 0, pos.Y + size.Y + 4)
\tend
end

local function hideTooltip()
\tif tooltipFrame then tooltipFrame.Visible = false end
end

'''
replace_once('local Library = {}\nLibrary.Flags = {}', tooltip_block + 'local Library = {}\nLibrary.Flags = {}', "3. tooltip system")

# 4. applyTooltip helper
replace_once(
    '\t\tlocal function registerFlag(flag, obj)\n'
    '\t\t\tif flag then Library.Flags[flag] = obj end\n'
    '\t\tend',
    '\t\tlocal function registerFlag(flag, obj)\n'
    '\t\t\tif flag then Library.Flags[flag] = obj end\n'
    '\t\tend\n'
    '\n'
    '\t\tlocal function applyTooltip(instance, text)\n'
    '\t\t\tif not text or text == "" then return end\n'
    '\t\t\tinstance.MouseEnter:Connect(function()\n'
    '\t\t\t\tshowTooltip(text, instance)\n'
    '\t\t\tend)\n'
    '\t\t\tinstance.MouseLeave:Connect(function()\n'
    '\t\t\t\thideTooltip()\n'
    '\t\t\tend)\n'
    '\t\tend',
    "4. applyTooltip helper"
)

# 5. CreateSpacer — insert before CreateLabel
replace_once(
    '\t\tfunction tab:CreateLabel(text)',
    '\t\tfunction tab:CreateSpacer(px)\n'
    '\t\t\tlocal f = Instance.new("Frame")\n'
    '\t\t\tf.Name = "Spacer"\n'
    '\t\t\tf.Size = UDim2.new(1, 0, 0, px or 6)\n'
    '\t\t\tf.BackgroundTransparency = 1\n'
    '\t\t\tf.Parent = page\n'
    '\t\t\treturn f\n'
    '\t\tend\n'
    '\n'
    '\t\tfunction tab:CreateLabel(text)',
    "5. CreateSpacer"
)

# 6. CreateImage — insert before CreateButton
replace_once(
    '\t\tfunction tab:CreateButton(bcfg)',
    '\t\tfunction tab:CreateImage(icfg)\n'
    '\t\t\ticfg = icfg or {}\n'
    '\t\t\tlocal holder, strk = makeHolder(icfg.Height or 120)\n'
    '\t\t\tlocal img = Instance.new("ImageLabel")\n'
    '\t\t\timg.Name = "Image"\n'
    '\t\t\timg.Size = UDim2.new(1, 0, 1, 0)\n'
    '\t\t\timg.BackgroundTransparency = 1\n'
    '\t\t\timg.Image = icfg.Image or ""\n'
    '\t\t\timg.ScaleType = icfg.ScaleType or Enum.ScaleType.Stretch\n'
    '\t\t\timg.Parent = holder\n'
    '\t\t\tcorner(img, R.panel)\n'
    '\t\t\tif icfg.CornerRadius then corner(img, icfg.CornerRadius) end\n'
    '\t\t\tonTheme(function()\n'
    '\t\t\t\tTween(holder, T20, { BackgroundColor3 = C.panel })\n'
    '\t\t\t\tTween(strk, T20, { Color = C.border })\n'
    '\t\t\tend)\n'
    '\t\t\tapplyTooltip(holder, icfg.Tooltip)\n'
    '\t\t\tlocal obj = {}\n'
    '\t\t\tfunction obj:Set(imageId) img.Image = imageId end\n'
    '\t\t\treturn obj\n'
    '\t\tend\n'
    '\n'
    '\t\tfunction tab:CreateButton(bcfg)',
    "6. CreateImage"
)

# 7. CreateMultiButton — insert before CreateToggle
replace_once(
    '\t\tfunction tab:CreateToggle(tcfg)',
    '\t\tfunction tab:CreateMultiButton(mcfg)\n'
    '\t\t\tmcfg = mcfg or {}\n'
    '\t\t\tlocal buttons = mcfg.Buttons or {}\n'
    '\t\t\tlocal holder = Instance.new("Frame")\n'
    '\t\t\tholder.Name = "MultiButton"\n'
    '\t\t\tholder.Size = UDim2.new(1, 0, 0, 36)\n'
    '\t\t\tholder.BackgroundTransparency = 1\n'
    '\t\t\tholder.Parent = page\n'
    '\t\t\tlocal hLayout = Instance.new("UIListLayout")\n'
    '\t\t\thLayout.FillDirection = Enum.FillDirection.Horizontal\n'
    '\t\t\thLayout.Padding = UDim.new(0, 6)\n'
    '\t\t\thLayout.Parent = holder\n'
    '\t\t\tlocal objs = {}\n'
    '\t\t\tfor i, btnCfg in ipairs(buttons) do\n'
    '\t\t\t\tlocal b = Instance.new("TextButton")\n'
    '\t\t\t\tb.Name = btnCfg.Name or ("Btn" .. i)\n'
    '\t\t\t\tb.Size = UDim2.new(1 / #buttons, -(6 * (#buttons - 1)) / #buttons, 1, 0)\n'
    '\t\t\t\tb.BackgroundColor3 = C.panel\n'
    '\t\t\t\tb.Text = ""\n'
    '\t\t\t\tb.AutoButtonColor = false\n'
    '\t\t\t\tb.BorderSizePixel = 0\n'
    '\t\t\t\tb.Parent = holder\n'
    '\t\t\t\tcorner(b, R.control)\n'
    '\t\t\t\tlocal bStrk = stroke(b, C.border, 1)\n'
    '\t\t\t\tlocal bLbl = Instance.new("TextLabel")\n'
    '\t\t\t\tbLbl.Size = UDim2.new(1, 0, 1, 0)\n'
    '\t\t\t\tbLbl.BackgroundTransparency = 1\n'
    '\t\t\t\tbLbl.Font = Enum.Font.GothamMedium\n'
    '\t\t\t\tbLbl.TextSize = 12\n'
    '\t\t\t\tbLbl.TextColor3 = C.text\n'
    '\t\t\t\tbLbl.Text = btnCfg.Name or ""\n'
    '\t\t\t\tbLbl.Parent = b\n'
    '\t\t\t\tb.MouseEnter:Connect(function() Tween(b, T10, { BackgroundColor3 = C.panelHov }) end)\n'
    '\t\t\t\tb.MouseLeave:Connect(function() Tween(b, T10, { BackgroundColor3 = C.panel }) end)\n'
    '\t\t\t\tb.MouseButton1Click:Connect(function()\n'
    '\t\t\t\t\tripple(b, b.AbsoluteSize.X / 2, b.AbsoluteSize.Y / 2, C.accent)\n'
    '\t\t\t\t\tif btnCfg.Callback then task.spawn(function() pcall(btnCfg.Callback) end) end\n'
    '\t\t\t\tend)\n'
    '\t\t\t\tonTheme(function()\n'
    '\t\t\t\t\tTween(b, T20, { BackgroundColor3 = C.panel })\n'
    '\t\t\t\t\tTween(bStrk, T20, { Color = C.border })\n'
    '\t\t\t\t\tTween(bLbl, T20, { TextColor3 = C.text })\n'
    '\t\t\t\tend)\n'
    '\t\t\t\ttable.insert(objs, { Set = function(t) bLbl.Text = t end, Fire = function() if btnCfg.Callback then pcall(btnCfg.Callback) end end })\n'
    '\t\t\tend\n'
    '\t\t\tapplyTooltip(holder, mcfg.Tooltip)\n'
    '\t\t\treturn objs\n'
    '\t\tend\n'
    '\n'
    '\t\tfunction tab:CreateToggle(tcfg)',
    "7. CreateMultiButton"
)

# 8. Searchable dropdown
replace_once(
    '\t\t\tlocal multi    = dcfg.MultipleOptions == true\n'
    '\t\t\tlocal callback = dcfg.Callback',
    '\t\t\tlocal multi    = dcfg.MultipleOptions == true\n'
    '\t\t\tlocal callback = dcfg.Callback\n'
    '\t\t\tlocal searchable = dcfg.Searchable == true',
    "8a. searchable flag"
)

# 9. Add CreateAccordion + CreateBindable before aliases
replace_once(
    '\t\ttab.Label = function(_, text) return tab:CreateSection(text) end',
    '\t\tfunction tab:CreateAccordion(acfg)\n'
    '\t\t\tacfg = acfg or {}\n'
    '\t\t\tlocal titleText = acfg.Title or "Accordion"\n'
    '\t\t\tlocal expanded = acfg.DefaultExpanded == true\n'
    '\t\t\tlocal headerBtn = Instance.new("TextButton")\n'
    '\t\t\theaderBtn.Name = "AccordionHeader"\n'
    '\t\t\theaderBtn.Size = UDim2.new(1, 0, 0, 36)\n'
    '\t\t\theaderBtn.BackgroundColor3 = C.panelAlt\n'
    '\t\t\theaderBtn.Text = ""\n'
    '\t\t\theaderBtn.AutoButtonColor = false\n'
    '\t\t\theaderBtn.BorderSizePixel = 0\n'
    '\t\t\theaderBtn.Parent = page\n'
    '\t\t\tcorner(headerBtn, R.panel)\n'
    '\t\t\tlocal accStroke = stroke(headerBtn, C.border, 1)\n'
    '\t\t\tlocal arrow = Instance.new("TextLabel")\n'
    '\t\t\tarrow.Size = UDim2.new(0, 20, 1, 0)\n'
    '\t\t\tarrow.Position = UDim2.new(0, 8, 0, 0)\n'
    '\t\t\tarrow.BackgroundTransparency = 1\n'
    '\t\t\tarrow.Font = Enum.Font.GothamBold\n'
    '\t\t\tarrow.TextSize = 12\n'
    '\t\t\tarrow.TextColor3 = C.accent\n'
    '\t\t\tarrow.Text = expanded and "▼" or "▶"\n'
    '\t\t\tarrow.Parent = headerBtn\n'
    '\t\t\tlocal ttl = Instance.new("TextLabel")\n'
    '\t\t\tttl.Size = UDim2.new(1, -36, 1, 0)\n'
    '\t\t\tttl.Position = UDim2.new(0, 28, 0, 0)\n'
    '\t\t\tttl.BackgroundTransparency = 1\n'
    '\t\t\tttl.Font = Enum.Font.GothamBold\n'
    '\t\t\tttl.TextSize = 12\n'
    '\t\t\tttl.TextColor3 = C.text\n'
    '\t\t\tttl.TextXAlignment = Enum.TextXAlignment.Left\n'
    '\t\t\tttl.Text = titleText\n'
    '\t\t\tttl.Parent = headerBtn\n'
    '\t\t\tlocal container = Instance.new("Frame")\n'
    '\t\t\tcontainer.Name = "AccordionContent"\n'
    '\t\t\tcontainer.Size = UDim2.new(1, 0, 0, 0)\n'
    '\t\t\tcontainer.BackgroundColor3 = C.panel\n'
    '\t\t\tcontainer.BorderSizePixel = 0\n'
    '\t\t\tcontainer.ClipsDescendants = true\n'
    '\t\t\tcontainer.Visible = expanded\n'
    '\t\t\tcontainer.Parent = page\n'
    '\t\t\tcorner(container, R.panel)\n'
    '\t\t\tstroke(container, C.border, 1)\n'
    '\t\t\tpad(container, 8, 8, 10, 10)\n'
    '\t\t\tlocal cLayout = Instance.new("UIListLayout")\n'
    '\t\t\tcLayout.Padding = UDim.new(0, 6)\n'
    '\t\t\tcLayout.SortOrder = Enum.SortOrder.LayoutOrder\n'
    '\t\t\tcLayout.Parent = container\n'
    '\t\t\tlocal function refreshSize()\n'
    '\t\t\t\tcontainer.Size = UDim2.new(1, 0, 0, cLayout.AbsoluteContentSize.Y + 16)\n'
    '\t\t\tend\n'
    '\t\t\tcLayout:GetPropertyChangedSignal("AbsoluteContentSize"):Connect(refreshSize)\n'
    '\t\t\ttask.defer(refreshSize)\n'
    '\t\t\tlocal obj = {}\n'
    '\t\t\tfunction obj:SetExpanded(e)\n'
    '\t\t\t\texpanded = e\n'
    '\t\t\t\tarrow.Text = expanded and "▼" or "▶"\n'
    '\t\t\t\tif expanded then\n'
    '\t\t\t\t\tcontainer.Visible = true\n'
    '\t\t\t\t\trefreshSize()\n'
    '\t\t\t\t\tTween(container, T20, { BackgroundTransparency = 0 })\n'
    '\t\t\t\telse\n'
    '\t\t\t\t\tTween(container, T20, { BackgroundTransparency = 1 })\n'
    '\t\t\t\t\ttask.delay(0.2, function() if not expanded then container.Visible = false end end)\n'
    '\t\t\t\tend\n'
    '\t\t\tend\n'
    '\t\t\tfunction obj:Toggle() obj:SetExpanded(not expanded) end\n'
    '\t\t\tfunction obj:GetContainer() return container end\n'
    '\t\t\theaderBtn.MouseButton1Click:Connect(function() obj:Toggle() end)\n'
    '\t\t\theaderBtn.MouseEnter:Connect(function() Tween(headerBtn, T10, { BackgroundColor3 = C.panelHov }) end)\n'
    '\t\t\theaderBtn.MouseLeave:Connect(function() Tween(headerBtn, T10, { BackgroundColor3 = C.panelAlt }) end)\n'
    '\t\t\tonTheme(function()\n'
    '\t\t\t\tTween(headerBtn, T20, { BackgroundColor3 = C.panelAlt })\n'
    '\t\t\t\tTween(accStroke, T20, { Color = C.border })\n'
    '\t\t\t\tTween(arrow, T20, { TextColor3 = C.accent })\n'
    '\t\t\t\tTween(ttl, T20, { TextColor3 = C.text })\n'
    '\t\t\t\tTween(container, T20, { BackgroundColor3 = C.panel })\n'
    '\t\t\tend)\n'
    '\t\t\tapplyTooltip(headerBtn, acfg.Tooltip)\n'
    '\t\t\treturn obj\n'
    '\t\tend\n'
    '\n'
    '\t\tfunction tab:CreateBindable(bcfg)\n'
    '\t\t\tbcfg = bcfg or {}\n'
    '\t\t\tlocal nameText = bcfg.Name or "Bindable"\n'
    '\t\t\tlocal callback = bcfg.Callback\n'
    '\t\t\tlocal enabled = bcfg.Enabled ~= false\n'
    '\t\t\tlocal bound = bcfg.Keybind\n'
    '\t\t\tif type(bound) == "string" then\n'
    '\t\t\t\tlocal ok, kc = pcall(function() return Enum.KeyCode[bound] end)\n'
    '\t\t\t\tbound = ok and kc or Enum.KeyCode.E\n'
    '\t\t\telseif bound == nil then\n'
    '\t\t\t\tbound = Enum.KeyCode.E\n'
    '\t\t\tend\n'
    '\t\t\tlocal holder, hStroke = makeHolder(42)\n'
    '\t\t\tlocal lbl = Instance.new("TextLabel")\n'
    '\t\t\tlbl.Size = UDim2.new(1, -100, 1, 0)\n'
    '\t\t\tlbl.Position = UDim2.new(0, 14, 0, 0)\n'
    '\t\t\tlbl.BackgroundTransparency = 1\n'
    '\t\t\tlbl.Font = Enum.Font.GothamMedium\n'
    '\t\t\tlbl.TextSize = 13\n'
    '\t\t\tlbl.TextColor3 = C.text\n'
    '\t\t\tlbl.TextXAlignment = Enum.TextXAlignment.Left\n'
    '\t\t\tlbl.Text = nameText\n'
    '\t\t\tlbl.Parent = holder\n'
    '\t\t\tlocal enSw = Instance.new("Frame")\n'
    '\t\t\tenSw.Size = UDim2.new(0, 32, 0, 18)\n'
    '\t\t\tenSw.Position = UDim2.new(1, -84, 0.5, -9)\n'
    '\t\t\tenSw.BackgroundColor3 = enabled and C.accent or C.track\n'
    '\t\t\tenSw.BorderSizePixel = 0\n'
    '\t\t\tenSw.Parent = holder\n'
    '\t\t\tcorner(enSw, UDim.new(1, 0))\n'
    '\t\t\tlocal enKnob = Instance.new("Frame")\n'
    '\t\t\tenKnob.Size = UDim2.new(0, 14, 0, 14)\n'
    '\t\t\tenKnob.Position = enabled and UDim2.new(1, -16, 0.5, -7) or UDim2.new(0, 2, 0.5, -7)\n'
    '\t\t\tenKnob.BackgroundColor3 = C.white\n'
    '\t\t\tenKnob.BorderSizePixel = 0\n'
    '\t\t\tenKnob.Parent = enSw\n'
    '\t\t\tcorner(enKnob, UDim.new(1, 0))\n'
    '\t\t\tlocal pill = Instance.new("TextLabel")\n'
    '\t\t\tpill.Size = UDim2.new(0, 44, 0, 20)\n'
    '\t\t\tpill.Position = UDim2.new(1, -48, 0.5, -10)\n'
    '\t\t\tpill.BackgroundColor3 = C.accentDark\n'
    '\t\t\tpill.Font = Enum.Font.GothamBold\n'
    '\t\t\tpill.TextSize = 10\n'
    '\t\t\tpill.TextColor3 = C.accent\n'
    '\t\t\tpill.Text = keyName(bound)\n'
    '\t\t\tpill.Parent = holder\n'
    '\t\t\tcorner(pill, R.pill)\n'
    '\t\t\tstroke(pill, C.accentDim, 1)\n'
    '\t\t\tlocal obj = { Enabled = enabled, Keybind = bound }\n'
    '\t\t\tlocal function updateState()\n'
    '\t\t\t\tTween(enSw, T20, { BackgroundColor3 = enabled and C.accent or C.track })\n'
    '\t\t\t\tTween(enKnob, T50, { Position = enabled and UDim2.new(1, -16, 0.5, -7) or UDim2.new(0, 2, 0.5, -7) })\n'
    '\t\t\tend\n'
    '\t\t\tlocal enHit = Instance.new("TextButton")\n'
    '\t\t\tenHit.Size = UDim2.new(0, 36, 1, 0)\n'
    '\t\t\tenHit.Position = UDim2.new(1, -86, 0, 0)\n'
    '\t\t\tenHit.BackgroundTransparency = 1\n'
    '\t\t\tenHit.Text = ""\n'
    '\t\t\tenHit.AutoButtonColor = false\n'
    '\t\t\tenHit.ZIndex = 10\n'
    '\t\t\tenHit.Parent = holder\n'
    '\t\t\tenHit.MouseButton1Click:Connect(function()\n'
    '\t\t\t\tenabled = not enabled\n'
    '\t\t\t\tobj.Enabled = enabled\n'
    '\t\t\t\tupdateState()\n'
    '\t\t\tend)\n'
    '\t\t\tWindowJanitor:Add(UserInputService.InputBegan:Connect(function(inp, gp)\n'
    '\t\t\t\tif gp then return end\n'
    '\t\t\t\tif not enabled then return end\n'
    '\t\t\t\tif UserInputService:GetFocusedTextBox() then return end\n'
    '\t\t\t\tif inp.KeyCode == bound and callback then pcall(callback, enabled) end\n'
    '\t\t\tend))\n'
    '\t\t\tfunction obj:SetEnabled(v) enabled = v obj.Enabled = v updateState() end\n'
    '\t\t\tfunction obj:SetKeybind(kc) bound = kc obj.Keybind = kc pill.Text = keyName(kc) end\n'
    '\t\t\tonTheme(function()\n'
    '\t\t\t\tTween(holder, T20, { BackgroundColor3 = C.panel })\n'
    '\t\t\t\tTween(hStroke, T20, { Color = C.border })\n'
    '\t\t\t\tTween(lbl, T20, { TextColor3 = C.text })\n'
    '\t\t\t\tTween(enSw, T20, { BackgroundColor3 = enabled and C.accent or C.track })\n'
    '\t\t\t\tTween(pill, T20, { BackgroundColor3 = C.accentDark })\n'
    '\t\t\tend)\n'
    '\t\t\tapplyTooltip(holder, bcfg.Tooltip)\n'
    '\t\t\tregisterFlag(bcfg.Flag, obj)\n'
    '\t\t\treturn obj\n'
    '\t\tend\n'
    '\n'
    '\t\ttab.Label = function(_, text) return tab:CreateSection(text) end',
    "9. CreateAccordion + CreateBindable"
)

# 10. Library-level utilities
replace_once('\nreturn Library\n', '''-- ============================================================
-- LIBRARY-LEVEL UTILITIES
-- ============================================================
function Library:DeepCopy(orig)
\tlocal copy
\tif type(orig) == "table" then
\t\tcopy = {}
\t\tfor k, v in next, orig, nil do copy[self:DeepCopy(k)] = self:DeepCopy(v) end
\t\tsetmetatable(copy, self:DeepCopy(getmetatable(orig)))
\telse copy = orig end
\treturn copy
end

function Library:Serialize(data)
\tlocal ok, result = pcall(function() return HttpService:JSONEncode(data) end)
\tif ok then return result else warn("[RezurXLib] Serialize: " .. tostring(result)) return nil end
end

function Library:Deserialize(jsonStr)
\tif type(jsonStr) ~= "string" then return nil end
\tlocal ok, result = pcall(function() return HttpService:JSONDecode(jsonStr) end)
\tif ok then return result else warn("[RezurXLib] Deserialize: " .. tostring(result)) return nil end
end

function Library:SaveConfiguration()
\tlocal config = {}
\tfor flag, obj in pairs(self.Flags) do
\t\tif obj.CurrentValue ~= nil then config[flag] = obj.CurrentValue
\t\telseif obj.CurrentKeybind ~= nil then config[flag] = keyName(obj.CurrentKeybind)
\t\telseif obj.Color ~= nil then local c = obj.Color config[flag] = { R=c.R, G=c.G, B=c.B }
\t\telseif obj.CurrentOption ~= nil then config[flag] = obj.CurrentOption end
\tend
\treturn config
end

function Library:LoadConfiguration(config)
\tif type(config) ~= "table" then warn("[RezurXLib] LoadConfiguration expects table") return end
\tfor flag, value in pairs(config) do
\t\tlocal obj = self.Flags[flag]
\t\tif obj and obj.Set then
\t\t\tpcall(function()
\t\t\t\tif type(value) == "table" and value.R then obj:Set(Color3.new(value.R, value.G, value.B))
\t\t\t\telseif type(value) == "string" and value:match("^%u[%u%d]+$") then
\t\t\t\t\tlocal ok, kc = pcall(function() return Enum.KeyCode[value] end)
\t\t\t\t\tif ok and kc then obj:Set(kc) end
\t\t\t\telse obj:Set(value) end
\t\t\tend)
\t\tend
\tend
end

function Library:HasFlag(flag) return self.Flags[flag] ~= nil end

function Library:GetFlag(flag)
\tlocal obj = self.Flags[flag]
\tif obj then
\t\tif obj.CurrentValue ~= nil then return obj.CurrentValue
\t\telseif obj.Color ~= nil then return obj.Color
\t\telseif obj.CurrentKeybind ~= nil then return obj.CurrentKeybind
\t\telseif obj.CurrentOption ~= nil then return obj.CurrentOption end
\tend
\treturn nil
end

function Library:ColorLighten(color, amount)
\tamount = amount or 0.2
\tlocal h, s, v = color:ToHSV()
\treturn Color3.fromHSV(h, s, math.min(v + amount, 1))
end

function Library:ColorDarken(color, amount)
\tamount = amount or 0.2
\tlocal h, s, v = color:ToHSV()
\treturn Color3.fromHSV(h, s, math.max(v - amount, 0))
end

function Library:GetStats()
\tlocal flagCount = 0
\tfor _ in pairs(self.Flags) do flagCount = flagCount + 1 end
\treturn { Version = self.Version, WindowCount = #self._windows, FlagCount = flagCount,
\t\tThemes = { "Ember", "Ocean", "Crimson", "Slate", "Midnight", "Forest", "Coral" } }
end

return Library''', "10. library utilities")

# 11. Aliases for new elements
replace_once(
    '\t\ttab.Keybind = function(_, n, k, cb) return tab:CreateKeybind({ Name = n, CurrentKeybind = k, Callback = cb }) end',
    '\t\ttab.Keybind = function(_, n, k, cb) return tab:CreateKeybind({ Name = n, CurrentKeybind = k, Callback = cb }) end\n'
    '\t\ttab.Spacer = function(_, px) return tab:CreateSpacer(px) end\n'
    '\t\ttab.Image = function(_, img, h) return tab:CreateImage({ Image = img, Height = h }) end\n'
    '\t\ttab.Accordion = function(_, t, exp) return tab:CreateAccordion({ Title = t, DefaultExpanded = exp }) end\n'
    '\t\ttab.Bindable = function(_, n, k, cb) return tab:CreateBindable({ Name = n, Keybind = k, Callback = cb }) end',
    "11. aliases"
)

with open(filepath, "w") as f:
    f.write(src)

print(f"\n{edits} edits applied.")
