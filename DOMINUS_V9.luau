-- ============================================================
-- 👑 DOMINUS V9 — Self-Contained Edition
-- No external library load. Everything inline. No caching issues.
-- ============================================================

local Players           = game:GetService("Players")
local UserInputService  = game:GetService("UserInputService")
local TweenService      = game:GetService("TweenService")
local RunService        = game:GetService("RunService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local VirtualUser       = game:GetService("VirtualUser")
local HttpService       = game:GetService("HttpService")
local CoreGui           = game:GetService("CoreGui")
local player            = Players.LocalPlayer
local playerGui         = player:WaitForChild("PlayerGui")

-- ═══ HELPERS ═══
local function corner(p, r)
	local c = Instance.new("UICorner")
	c.CornerRadius = UDim.new(0, r or 8)
	c.Parent = p
end

local function stroke(p, col, thick)
	local s = Instance.new("UIStroke")
	s.Color = col or Color3.fromRGB(60, 60, 80)
	s.Thickness = thick or 1
	s.ApplyStrokeMode = Enum.ApplyStrokeMode.Border
	s.Parent = p
	return s
end

local T20 = TweenInfo.new(0.2, Enum.EasingStyle.Quad, Enum.EasingDirection.Out)
local T50 = TweenInfo.new(0.5, Enum.EasingStyle.Back, Enum.EasingDirection.Out)

local function Tween(inst, props)
	local t = TweenService:Create(inst, T20, props)
	t:Play()
	return t
end

-- ═══ THEME ═══
local C = {
	bg       = Color3.fromRGB(12, 12, 18),
	panel    = Color3.fromRGB(22, 22, 32),
	panelHov = Color3.fromRGB(34, 34, 50),
	accent   = Color3.fromRGB(255, 122, 28),
	accentHi = Color3.fromRGB(255, 155, 65),
	accentDim= Color3.fromRGB(185, 88, 20),
	text     = Color3.fromRGB(240, 240, 250),
	textDim  = Color3.fromRGB(170, 170, 190),
	muted    = Color3.fromRGB(100, 100, 130),
	border   = Color3.fromRGB(50, 50, 70),
	track    = Color3.fromRGB(40, 40, 55),
	white    = Color3.fromRGB(255, 255, 255),
	red      = Color3.fromRGB(225, 58, 58),
	green    = Color3.fromRGB(48, 215, 92),
	yellow   = Color3.fromRGB(255, 210, 48),
	tabBg    = Color3.fromRGB(18, 18, 26),
	tabChip  = Color3.fromRGB(32, 32, 46),
	tabHov   = Color3.fromRGB(44, 44, 62),
	headerA  = Color3.fromRGB(28, 24, 38),
	headerB  = Color3.fromRGB(16, 16, 26),
}

-- ═══ DRAG SYSTEM ═══
local activeDrag = nil

UserInputService.InputChanged:Connect(function(inp)
	if inp.UserInputType == Enum.UserInputType.MouseMovement
		or inp.UserInputType == Enum.UserInputType.Touch then
		if activeDrag and activeDrag.move then
			activeDrag.move(inp.Position)
		end
	end
end)

UserInputService.InputEnded:Connect(function(inp)
	if inp.UserInputType == Enum.UserInputType.MouseButton1
		or inp.UserInputType == Enum.UserInputType.Touch then
		if activeDrag and activeDrag.onEnd then
			activeDrag.onEnd()
		end
		activeDrag = nil
	end
end)

local function startDrag(startPos, startAbs, moveFn, onEndFn)
	activeDrag = { move = moveFn, onEnd = onEndFn }
end

-- ═══ CREATE WINDOW ═══
local WIN_W, WIN_H = 420, 480
local HEADER_H = 50
local TAB_H = 38
local SB_H = 22

local screenGui = Instance.new("ScreenGui")
screenGui.Name = "DOMINUS_V9"
screenGui.ResetOnSpawn = false
screenGui.IgnoreGuiInset = true
screenGui.ZIndexBehavior = Enum.ZIndexBehavior.Sibling
pcall(function() screenGui.Parent = CoreGui end)
if not screenGui.Parent then screenGui.Parent = playerGui end

-- Shadow
local shadow = Instance.new("Frame")
shadow.Size = UDim2.new(0, WIN_W + 20, 0, WIN_H + 20)
shadow.Position = UDim2.new(0.5, -(WIN_W + 20) / 2, 0.45, -(WIN_H + 20) / 2)
shadow.BackgroundColor3 = Color3.new(0, 0, 0)
shadow.BackgroundTransparency = 0.5
shadow.BorderSizePixel = 0
shadow.ZIndex = 1
shadow.Parent = screenGui
corner(shadow, 16)

-- Main frame
local frame = Instance.new("Frame")
frame.Size = UDim2.new(0, WIN_W, 0, WIN_H)
frame.Position = UDim2.new(0.5, -WIN_W / 2, 0.45, -WIN_H / 2)
frame.BackgroundColor3 = C.bg
frame.BorderSizePixel = 0
frame.ClipsDescendants = true
frame.ZIndex = 2
frame.Parent = screenGui
corner(frame, 14)
stroke(frame, C.border, 1.5)

-- Header
local header = Instance.new("Frame")
header.Size = UDim2.new(1, 0, 0, HEADER_H)
header.BackgroundColor3 = C.headerA
header.BorderSizePixel = 0
header.ZIndex = 3
header.Parent = frame
corner(header, 14)

-- Title
local title = Instance.new("TextLabel")
title.Size = UDim2.new(0, 200, 0, 24)
title.Position = UDim2.new(0, 16, 0, 6)
title.BackgroundTransparency = 1
title.Font = Enum.Font.GothamBold
title.TextSize = 18
title.TextColor3 = C.text
title.TextXAlignment = Enum.TextXAlignment.Left
title.Text = "DOMINUS V9"
title.ZIndex = 4
title.Parent = header

local subtitle = Instance.new("TextLabel")
subtitle.Size = UDim2.new(0, 200, 0, 14)
subtitle.Position = UDim2.new(0, 17, 0, 30)
subtitle.BackgroundTransparency = 1
subtitle.Font = Enum.Font.Gotham
subtitle.TextSize = 11
subtitle.TextColor3 = C.muted
subtitle.TextXAlignment = Enum.TextXAlignment.Left
subtitle.Text = "Self-Contained Edition"
subtitle.ZIndex = 4
subtitle.Parent = header

-- Close button
local closeBtn = Instance.new("TextButton")
closeBtn.Size = UDim2.new(0, 36, 0, 30)
closeBtn.Position = UDim2.new(1, -42, 0.5, -15)
closeBtn.BackgroundColor3 = C.red
closeBtn.Text = "X"
closeBtn.Font = Enum.Font.GothamBold
closeBtn.TextSize = 14
closeBtn.TextColor3 = C.white
closeBtn.BorderSizePixel = 0
closeBtn.ZIndex = 5
closeBtn.Parent = header
corner(closeBtn, 6)

-- Minimize button
local minBtn = Instance.new("TextButton")
minBtn.Size = UDim2.new(0, 36, 0, 30)
minBtn.Position = UDim2.new(1, -82, 0.5, -15)
minBtn.BackgroundColor3 = C.panel
minBtn.Text = "-"
minBtn.Font = Enum.Font.GothamBold
minBtn.TextSize = 18
minBtn.TextColor3 = C.text
minBtn.BorderSizePixel = 0
minBtn.ZIndex = 5
minBtn.Parent = header
corner(minBtn, 6)

-- Drag bar (covers header except buttons)
local dragBar = Instance.new("TextButton")
dragBar.Size = UDim2.new(1, -100, 1, 0)
dragBar.Position = UDim2.new(0, 0, 0, 0)
dragBar.BackgroundTransparency = 1
dragBar.Text = ""
dragBar.ZIndex = 6
dragBar.Parent = header

dragBar.InputBegan:Connect(function(inp)
	if inp.UserInputType == Enum.UserInputType.MouseButton1
		or inp.UserInputType == Enum.UserInputType.Touch then
		local startPos = inp.Position
		local startAbs = frame.AbsolutePosition
		startDrag(startPos, startAbs, function(pos)
			local d = pos - startPos
			frame.Position = UDim2.new(0, startAbs.X + d.X, 0, startAbs.Y + d.Y)
			shadow.Position = UDim2.new(0, startAbs.X + d.X - 10, 0, startAbs.Y + d.Y - 10)
		end)
	end
end)

-- Minimize logic
local minimized = false
minBtn.Activated:Connect(function()
	minimized = not minimized
	if minimized then
		frame.Size = UDim2.new(0, WIN_W, 0, HEADER_H)
		shadow.Size = UDim2.new(0, WIN_W + 20, 0, HEADER_H + 20)
	else
		frame.Size = UDim2.new(0, WIN_W, 0, WIN_H)
		shadow.Size = UDim2.new(0, WIN_W + 20, 0, WIN_H + 20)
	end
end)

-- Close logic
local floatIcon = nil
closeBtn.Activated:Connect(function()
	frame.Visible = false
	shadow.Visible = false
	if floatIcon then floatIcon.Visible = true end
end)

-- Floating restore icon
floatIcon = Instance.new("TextButton")
floatIcon.Size = UDim2.new(0, 50, 0, 50)
floatIcon.Position = UDim2.new(0, 20, 0, 20)
floatIcon.BackgroundColor3 = C.accent
floatIcon.Text = ""
floatIcon.BorderSizePixel = 0
floatIcon.ZIndex = 100
floatIcon.Visible = false
floatIcon.Parent = screenGui
corner(floatIcon, 25)
stroke(floatIcon, C.white, 2)

local floatLabel = Instance.new("TextLabel")
floatLabel.Size = UDim2.new(1, 0, 1, 0)
floatLabel.BackgroundTransparency = 1
floatLabel.Text = "D"
floatLabel.Font = Enum.Font.GothamBold
floatLabel.TextSize = 24
floatLabel.TextColor3 = C.white
floatLabel.Parent = floatIcon

floatIcon.Activated:Connect(function()
	frame.Visible = true
	shadow.Visible = true
	floatIcon.Visible = false
end)

-- Body
local body = Instance.new("Frame")
body.Size = UDim2.new(1, 0, 1, -HEADER_H)
body.Position = UDim2.new(0, 0, 0, HEADER_H)
body.BackgroundTransparency = 1
body.ZIndex = 2
body.Parent = frame

-- Tab bar
local tabBar = Instance.new("Frame")
tabBar.Size = UDim2.new(1, 0, 0, TAB_H)
tabBar.BackgroundColor3 = C.tabBg
tabBar.BorderSizePixel = 0
tabBar.ZIndex = 3
tabBar.Parent = body

local tabList = Instance.new("UIListLayout")
tabList.FillDirection = Enum.FillDirection.Horizontal
tabList.Padding = UDim.new(0, 4)
tabList.SortOrder = Enum.SortOrder.LayoutOrder
tabList.Parent = tabBar

local tabPad = Instance.new("UIPadding")
tabPad.PaddingLeft = UDim.new(0, 6)
tabPad.PaddingRight = UDim.new(0, 6)
tabPad.Parent = tabBar

-- Content area
local content = Instance.new("ScrollingFrame")
content.Size = UDim2.new(1, 0, 1, -(TAB_H + SB_H))
content.Position = UDim2.new(0, 0, 0, TAB_H)
content.BackgroundTransparency = 1
content.BorderSizePixel = 0
content.ScrollBarThickness = 3
content.ScrollBarImageColor3 = C.accent
content.CanvasSize = UDim2.new(0, 0, 0, 0)
content.ZIndex = 3
content.Parent = body

local contentList = Instance.new("UIListLayout")
contentList.Padding = UDim.new(0, 6)
contentList.SortOrder = Enum.SortOrder.LayoutOrder
contentList.Parent = content

local contentPad = Instance.new("UIPadding")
contentPad.PaddingTop = UDim.new(0, 8)
contentPad.PaddingBottom = UDim.new(0, 8)
contentPad.PaddingLeft = UDim.new(0, 10)
contentPad.PaddingRight = UDim.new(0, 10)
contentPad.Parent = content

contentList:GetPropertyChangedSignal("AbsoluteContentSize"):Connect(function()
	content.CanvasSize = UDim2.new(0, 0, 0, contentList.AbsoluteContentSize.Y + 16)
end)

-- Status bar
local statusBar = Instance.new("Frame")
statusBar.Size = UDim2.new(1, 0, 0, SB_H)
statusBar.Position = UDim2.new(0, 0, 1, -SB_H)
statusBar.BackgroundColor3 = C.panel
statusBar.BorderSizePixel = 0
statusBar.ZIndex = 3
statusBar.Parent = body

local statusText = Instance.new("TextLabel")
statusText.Size = UDim2.new(1, -20, 1, 0)
statusText.Position = UDim2.new(0, 10, 0, 0)
statusText.BackgroundTransparency = 1
statusText.Font = Enum.Font.Gotham
statusText.TextSize = 10
statusText.TextColor3 = C.muted
statusText.TextXAlignment = Enum.TextXAlignment.Left
statusText.Text = "DOMINUS V9 v9.0 | Ready"
statusText.Parent = statusBar

-- ═══ TAB SYSTEM ═══
local tabs = {}
local activeTab = nil

local function makeTab(name, icon)
	local tab = {}

	-- Tab button — uses a TextButton with .Text directly
	-- [FIX] No RichText, no AutomaticSize, no TextService:GetTextSize
	-- Simple fixed width, plain text, visible color
	local btn = Instance.new("TextButton")
	btn.Size = UDim2.new(0, 95, 1, -6)
	btn.Position = UDim2.new(0, 0, 0, 3)
	btn.BackgroundColor3 = C.tabChip
	btn.AutoButtonColor = false
	btn.BorderSizePixel = 0
	btn.Text = (icon or "") .. " " .. name
	btn.Font = Enum.Font.GothamBold
	btn.TextSize = 12
	btn.TextColor3 = C.text
	btn.TextXAlignment = Enum.TextXAlignment.Center
	btn.ZIndex = 4
	btn.Parent = tabBar
	corner(btn, 7)
	local btnStroke = stroke(btn, C.border, 1)

	-- Page (content container for this tab)
	local page = Instance.new("Frame")
	page.Size = UDim2.new(1, 0, 1, 0)
	page.BackgroundTransparency = 1
	page.Visible = false
	page.ZIndex = 3
	page.Parent = content

	local pageList = Instance.new("UIListLayout")
	pageList.Padding = UDim.new(0, 6)
	pageList.SortOrder = Enum.SortOrder.LayoutOrder
	pageList.Parent = page

	local pagePad = Instance.new("UIPadding")
	pagePad.PaddingTop = UDim.new(0, 2)
	pagePad.PaddingBottom = UDim.new(0, 8)
	pagePad.PaddingLeft = UDim.new(0, 0)
	pagePad.PaddingRight = UDim.new(0, 0)
	pagePad.Parent = page

	pageList:GetPropertyChangedSignal("AbsoluteContentSize"):Connect(function()
		content.CanvasSize = UDim2.new(0, 0, 0, pageList.AbsoluteContentSize.Y + 16)
	end)

	tab.btn = btn
	tab.page = page
	tab.pageList = pageList
	tab.name = name

	local function setActive()
		if activeTab and activeTab ~= tab then
			activeTab.page.Visible = false
			Tween(activeTab.btn, { BackgroundColor3 = C.tabChip })
			activeTab.btn.TextColor3 = C.textDim
		end
		activeTab = tab
		page.Visible = true
		Tween(btn, { BackgroundColor3 = C.accentDim })
		btn.TextColor3 = C.accentHi
	end

	btn.MouseEnter:Connect(function()
		if activeTab ~= tab then
			Tween(btn, { BackgroundColor3 = C.tabHov })
		end
	end)
	btn.MouseLeave:Connect(function()
		if activeTab ~= tab then
			Tween(btn, { BackgroundColor3 = C.tabChip })
		end
	end)
	btn.Activated:Connect(function()
		setActive()
	end)

	table.insert(tabs, tab)
	if #tabs == 1 then
		task.defer(function() setActive() end)
	end

	return tab
end

-- ═══ ELEMENT CREATORS ═══

local function makeHolder(tab, h)
	local holder = Instance.new("Frame")
	holder.Size = UDim2.new(1, 0, 0, h)
	holder.BackgroundColor3 = C.panel
	holder.BorderSizePixel = 0
	holder.Parent = tab.page
	corner(holder, 8)
	local s = stroke(holder, C.border, 1)
	return holder, s
end

local function createSection(tab, text)
	local l = Instance.new("TextLabel")
	l.Size = UDim2.new(1, 0, 0, 18)
	l.BackgroundTransparency = 1
	l.Font = Enum.Font.GothamBold
	l.TextSize = 10
	l.TextColor3 = C.accent
	l.TextXAlignment = Enum.TextXAlignment.Left
	l.Text = string.upper(text)
	l.Parent = tab.page
	return l
end

local function createButton(tab, name, callback)
	local holder = makeHolder(tab, 40)
	local lbl = Instance.new("TextLabel")
	lbl.Size = UDim2.new(1, -20, 1, 0)
	lbl.Position = UDim2.new(0, 12, 0, 0)
	lbl.BackgroundTransparency = 1
	lbl.Font = Enum.Font.GothamMedium
	lbl.TextSize = 13
	lbl.TextColor3 = C.text
	lbl.TextXAlignment = Enum.TextXAlignment.Left
	lbl.Text = name
	lbl.Parent = holder

	-- Transparent hit button covering the whole holder
	local hit = Instance.new("TextButton")
	hit.Size = UDim2.new(1, 0, 1, 0)
	hit.BackgroundTransparency = 1
	hit.Text = ""
	hit.AutoButtonColor = false
	hit.ZIndex = 5
	hit.Parent = holder

	hit.MouseEnter:Connect(function() Tween(holder, { BackgroundColor3 = C.panelHov }) end)
	hit.MouseLeave:Connect(function() Tween(holder, { BackgroundColor3 = C.panel }) end)
	hit.Activated:Connect(function()
		Tween(holder, { BackgroundColor3 = C.accentDim })
		task.delay(0.15, function() Tween(holder, { BackgroundColor3 = C.panelHov }) end)
		if callback then task.spawn(function() pcall(callback) end) end
	end)

	return { Set = function(t) lbl.Text = t end }
end

local function createToggle(tab, name, default, callback)
	local holder, hStroke = makeHolder(tab, 40)
	local state = default == true
	if state then hStroke.Color = C.accentDim end

	local lbl = Instance.new("TextLabel")
	lbl.Size = UDim2.new(1, -60, 1, 0)
	lbl.Position = UDim2.new(0, 12, 0, 0)
	lbl.BackgroundTransparency = 1
	lbl.Font = Enum.Font.GothamMedium
	lbl.TextSize = 13
	lbl.TextColor3 = C.text
	lbl.TextXAlignment = Enum.TextXAlignment.Left
	lbl.Text = name
	lbl.Parent = holder

	local sw = Instance.new("Frame")
	sw.Size = UDim2.new(0, 40, 0, 20)
	sw.Position = UDim2.new(1, -48, 0.5, -10)
	sw.BackgroundColor3 = state and C.accent or C.track
	sw.BorderSizePixel = 0
	sw.Parent = holder
	corner(sw, 10)

	local knob = Instance.new("Frame")
	knob.Size = UDim2.new(0, 16, 0, 16)
	knob.Position = state and UDim2.new(1, -18, 0.5, -8) or UDim2.new(0, 2, 0.5, -8)
	knob.BackgroundColor3 = C.white
	knob.BorderSizePixel = 0
	knob.Parent = sw
	corner(knob, 8)

	local hit = Instance.new("TextButton")
	hit.Size = UDim2.new(1, 0, 1, 0)
	hit.BackgroundTransparency = 1
	hit.Text = ""
	hit.AutoButtonColor = false
	hit.ZIndex = 5
	hit.Parent = holder

	local obj = { CurrentValue = state }
	local function apply(v)
		state = v
		obj.CurrentValue = v
		Tween(sw, { BackgroundColor3 = state and C.accent or C.track })
		Tween(hStroke, { Color = state and C.accentDim or C.border })
		Tween(knob, { Position = state and UDim2.new(1, -18, 0.5, -8) or UDim2.new(0, 2, 0.5, -8) })
		if callback then pcall(callback, state) end
	end

	hit.Activated:Connect(function() apply(not state) end)

	obj.Set = function(v) apply(v) end
	obj.SetLabel = function(t) lbl.Text = t end
	obj.Get = function() return state end
	return obj
end

local function createSlider(tab, name, min, max, default, suffix, callback)
	local holder = makeHolder(tab, 50)
	local value = math.clamp(default or min, min, max)

	local lbl = Instance.new("TextLabel")
	lbl.Size = UDim2.new(1, -70, 0, 16)
	lbl.Position = UDim2.new(0, 12, 0, 6)
	lbl.BackgroundTransparency = 1
	lbl.Font = Enum.Font.GothamMedium
	lbl.TextSize = 13
	lbl.TextColor3 = C.text
	lbl.TextXAlignment = Enum.TextXAlignment.Left
	lbl.Text = name
	lbl.Parent = holder

	local valLbl = Instance.new("TextLabel")
	valLbl.Size = UDim2.new(0, 60, 0, 16)
	valLbl.Position = UDim2.new(1, -68, 0, 6)
	valLbl.BackgroundTransparency = 1
	valLbl.Font = Enum.Font.GothamBold
	valLbl.TextSize = 13
	valLbl.TextColor3 = C.accent
	valLbl.TextXAlignment = Enum.TextXAlignment.Right
	valLbl.Text = tostring(value) .. (suffix or "")
	valLbl.Parent = holder

	local track = Instance.new("Frame")
	track.Size = UDim2.new(1, -24, 0, 5)
	track.Position = UDim2.new(0, 12, 0, 34)
	track.BackgroundColor3 = C.track
	track.BorderSizePixel = 0
	track.Parent = holder
	corner(track, 3)

	local fill = Instance.new("Frame")
	fill.Size = UDim2.new(0, 0, 1, 0)
	fill.BackgroundColor3 = C.accent
	fill.BorderSizePixel = 0
	fill.Parent = track
	corner(fill, 3)

	local knob = Instance.new("Frame")
	knob.Size = UDim2.new(0, 14, 0, 14)
	knob.Position = UDim2.new(0, -7, 0.5, -7)
	knob.BackgroundColor3 = C.white
	knob.BorderSizePixel = 0
	knob.Parent = track
	corner(knob, 7)
	stroke(knob, C.accent, 2)

	local function update()
		local pct = (value - min) / (max - min)
		fill.Size = UDim2.new(pct, 0, 1, 0)
		knob.Position = UDim2.new(pct, -7, 0.5, -7)
		valLbl.Text = tostring(value) .. (suffix or "")
	end
	update()

	local hit = Instance.new("TextButton")
	hit.Size = UDim2.new(1, 0, 1, 0)
	hit.BackgroundTransparency = 1
	hit.Text = ""
	hit.AutoButtonColor = false
	hit.ZIndex = 5
	hit.Parent = holder

	local function setFromX(x)
		local pct = math.clamp((x - track.AbsolutePosition.X) / track.AbsoluteSize.X, 0, 1)
		value = math.floor(min + pct * (max - min) + 0.5)
		update()
		if callback then pcall(callback, value) end
	end

	hit.InputBegan:Connect(function(inp)
		if inp.UserInputType == Enum.UserInputType.MouseButton1
			or inp.UserInputType == Enum.UserInputType.Touch then
			setFromX(inp.Position.X)
			startDrag(inp.Position, nil, function(pos) setFromX(pos.X) end)
		end
	end)

	return {
		Set = function(v) value = math.clamp(v, min, max) update() if callback then pcall(callback, value) end end,
		Get = function() return value end,
	}
end

local function createDropdown(tab, name, options, default, callback)
	local holder = makeHolder(tab, 40)
	local selected = default or options[1]

	local lbl = Instance.new("TextLabel")
	lbl.Size = UDim2.new(1, -30, 1, 0)
	lbl.Position = UDim2.new(0, 12, 0, 0)
	lbl.BackgroundTransparency = 1
	lbl.Font = Enum.Font.GothamMedium
	lbl.TextSize = 13
	lbl.TextColor3 = C.text
	lbl.TextXAlignment = Enum.TextXAlignment.Left
	lbl.Text = name .. ": " .. selected
	lbl.Parent = holder

	local arrow = Instance.new("TextLabel")
	arrow.Size = UDim2.new(0, 20, 1, 0)
	arrow.Position = UDim2.new(1, -24, 0, 0)
	arrow.BackgroundTransparency = 1
	arrow.Font = Enum.Font.GothamBold
	arrow.TextSize = 12
	arrow.TextColor3 = C.muted
	arrow.Text = "v"
	arrow.Parent = holder

	-- [FIX] Use a TextButton as the hit target (not Frame.InputBegan)
	-- Frames don't consume touch on mobile, causing the freeze
	local hit = Instance.new("TextButton")
	hit.Size = UDim2.new(1, 0, 1, 0)
	hit.BackgroundTransparency = 1
	hit.Text = ""
	hit.AutoButtonColor = false
	hit.ZIndex = 5
	hit.Parent = holder

	local listOpen = false
	local listFrame = nil
	local catcher = nil

	local function closeList()
		listOpen = false
		arrow.Text = "v"
		if listFrame then listFrame:Destroy() listFrame = nil end
		if catcher then catcher:Destroy() catcher = nil end
	end

	local function openList()
		if listOpen then closeList() return end
		listOpen = true
		arrow.Text = "^"

		-- Position the list below the holder
		local hPos = holder.AbsolutePosition
		local hSize = holder.AbsoluteSize
		local ITEM_H = 32
		local LIST_H = math.min(#options, 6) * ITEM_H + 8

		-- List frame
		listFrame = Instance.new("Frame")
		listFrame.Size = UDim2.new(0, hSize.X, 0, LIST_H)
		listFrame.Position = UDim2.new(0, hPos.X, 0, hPos.Y + hSize.Y + 2)
		listFrame.BackgroundColor3 = C.panel
		listFrame.BorderSizePixel = 0
		listFrame.ClipsDescendants = true
		listFrame.ZIndex = 50
		listFrame.Parent = screenGui
		corner(listFrame, 8)
		stroke(listFrame, C.accent, 1)

		local listLayout = Instance.new("UIListLayout")
		listLayout.Padding = UDim.new(0, 2)
		listLayout.Parent = listFrame

		local listPad = Instance.new("UIPadding")
		listPad.PaddingTop = UDim.new(0, 4)
		listPad.PaddingBottom = UDim.new(0, 4)
		listPad.PaddingLeft = UDim.new(0, 4)
		listPad.PaddingRight = UDim.new(0, 4)
		listPad.Parent = listFrame

		for _, opt in ipairs(options) do
			local item = Instance.new("TextButton")
			item.Size = UDim2.new(1, 0, 0, ITEM_H - 2)
			item.BackgroundColor3 = opt == selected and C.accentDim or C.panelHov
			item.Text = opt
			item.Font = Enum.Font.Gotham
			item.TextSize = 13
			item.TextColor3 = C.text
			item.TextXAlignment = Enum.TextXAlignment.Left
			item.AutoButtonColor = false
			item.ZIndex = 51
			item.Parent = listFrame
			corner(item, 6)
			stroke(item, C.border, 1)

			item.MouseEnter:Connect(function()
				if opt ~= selected then Tween(item, { BackgroundColor3 = C.panelHov }) end
			end)
			item.MouseLeave:Connect(function()
				if opt ~= selected then Tween(item, { BackgroundColor3 = C.panelHov }) end
			end)

			item.Activated:Connect(function()
				selected = opt
				lbl.Text = name .. ": " .. selected
				if callback then pcall(callback, selected) end
				closeList()
			end)
		end

		-- [FIX] Catcher: use 0.01 transparency (not 1.0) so it receives touch
		-- Use task.delay(0.15) so the opening tap doesn't close it
		catcher = Instance.new("TextButton")
		catcher.Size = UDim2.new(1, 0, 1, 0)
		catcher.BackgroundTransparency = 0.01
		catcher.BackgroundColor3 = Color3.new(0, 0, 0)
		catcher.Text = ""
		catcher.AutoButtonColor = false
		catcher.ZIndex = 49
		catcher.Visible = false
		catcher.Parent = screenGui

		catcher.Activated:Connect(function()
			closeList()
		end)

		task.delay(0.15, function()
			if catcher and catcher.Parent then
				catcher.Visible = true
			end
		end)
	end

	hit.Activated:Connect(function()
		openList()
	end)

	return {
		Set = function(v) selected = v lbl.Text = name .. ": " .. selected if callback then pcall(callback, selected) end end,
		Get = function() return selected end,
	}
end

local function createInput(tab, name, placeholder, callback)
	local holder, hStroke = makeHolder(tab, 46)

	local lbl = Instance.new("TextLabel")
	lbl.Size = UDim2.new(1, -20, 0, 14)
	lbl.Position = UDim2.new(0, 12, 0, 5)
	lbl.BackgroundTransparency = 1
	lbl.Font = Enum.Font.GothamMedium
	lbl.TextSize = 10
	lbl.TextColor3 = C.muted
	lbl.TextXAlignment = Enum.TextXAlignment.Left
	lbl.Text = string.upper(name)
	lbl.Parent = holder

	local box = Instance.new("TextBox")
	box.Size = UDim2.new(1, -24, 0, 20)
	box.Position = UDim2.new(0, 12, 0, 22)
	box.BackgroundTransparency = 1
	box.Font = Enum.Font.Gotham
	box.TextSize = 13
	box.TextColor3 = C.text
	box.PlaceholderColor3 = C.muted
	box.PlaceholderText = placeholder or ""
	box.TextXAlignment = Enum.TextXAlignment.Left
	box.ClearTextOnFocus = false
	box.Parent = holder

	box.Focused:Connect(function()
		hStroke.Color = C.accent
	end)
	box.FocusLost:Connect(function()
		hStroke.Color = C.border
		if callback then pcall(callback, box.Text) end
	end)

	return {
		Set = function(t) box.Text = t end,
		Get = function() return box.Text end,
	}
end

local function createLabel(tab, text)
	local lbl = Instance.new("TextLabel")
	lbl.Size = UDim2.new(1, 0, 0, 16)
	lbl.BackgroundTransparency = 1
	lbl.Font = Enum.Font.GothamBold
	lbl.TextSize = 10
	lbl.TextColor3 = C.accent
	lbl.TextXAlignment = Enum.TextXAlignment.Left
	lbl.Text = string.upper(text)
	lbl.Parent = tab.page
	return lbl
end

-- ═══ BUILD UI ═══

local farmTab = makeTab("Farm", "F")
createLabel(farmTab, "Mode & Speed")
local modeDD = createDropdown(farmTab, "Mode", {"Hybrid", "Legacy"}, "Hybrid", function(v) print("Mode:", v) end)
local speedDD = createDropdown(farmTab, "Speed", {"Infinity", "1e9", "1e15"}, "Infinity", function(v) print("Speed:", v) end)
createSlider(farmTab, "Workers", 1, 1000, 50, "", function(v) print("Workers:", v) end)
createLabel(farmTab, "Options")
local antiDetect = createToggle(farmTab, "Anti-Detect", false, function(v) print("AntiDetect:", v) end)
local maxPerf = createToggle(farmTab, "Max Performance", false, function(v) print("MaxPerf:", v) end)
local farmToggle = createToggle(farmTab, "Start Farm", false, function(v)
	if v then farmToggle.SetLabel("Farm: ON") else farmToggle.SetLabel("Farm: OFF") end
end)
createButton(farmTab, "Turbo Boost", function() print("Turbo!") end)

local moveTab = makeTab("Move", "M")
createLabel(moveTab, "Walk & Jump")
local overrideToggle = createToggle(moveTab, "Override Stats", false, function(v)
	if v then overrideToggle.SetLabel("Override: ON") else overrideToggle.SetLabel("Override: OFF") end
end)
createSlider(moveTab, "WalkSpeed", 16, 1000, 16, " sp", function(v) print("WS:", v) end)
createSlider(moveTab, "JumpPower", 50, 1000, 50, " pw", function(v) print("JP:", v) end)
createButton(moveTab, "Reset Movement", function() print("Reset") end)
createLabel(moveTab, "Noclip")
local noclipMode = createDropdown(moveTab, "Noclip Mode", {"V777", "Improved"}, "Improved", function(v) print("Noclip:", v) end)
local noclipToggle = createToggle(moveTab, "Noclip", false, function(v)
	if v then noclipToggle.SetLabel("Noclip: ON") else noclipToggle.SetLabel("Noclip: OFF") end
end)

local chatTab = makeTab("Chat", "C")
createLabel(chatTab, "Ghost Shout")
local msgInput = createInput(chatTab, "Message", "Type message...", function(v) end)
createButton(chatTab, "Send", function()
	local msg = msgInput.Get()
	if msg and msg ~= "" then print("Send:", msg) end
end)
createButton(chatTab, "Clear", function() msgInput.Set("") end)

local sysTab = makeTab("Sys", "S")
createLabel(sysTab, "System")
createButton(sysTab, "Destroy UI", function()
	screenGui:Destroy()
end)

-- Toggle key
UserInputService.InputBegan:Connect(function(inp, gp)
	if gp then return end
	if inp.KeyCode == Enum.KeyCode.K then
		frame.Visible = not frame.Visible
		shadow.Visible = frame.Visible
	end
end)

print("[DOMINUS V9] Loaded successfully. Press K to toggle.")
