-- ============================================================
-- ExampleUsage.client.lua — Admin Panel built on RezurXLib
--
-- Put RezurXLib as a ModuleScript (e.g. ReplicatedStorage) and
-- this as a LocalScript. Every callback below is a placeholder —
-- wire each one into YOUR OWN server-validated RemoteEvents.
-- Nothing here touches the game directly.
-- ============================================================

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Lib = require(ReplicatedStorage:WaitForChild("RezurXLib"))

-- Example remote hookups (create these on your server):
-- local Remotes = ReplicatedStorage:WaitForChild("AdminRemotes")
-- local KickRemote = Remotes:WaitForChild("KickPlayer")

local Window = Lib:CreateWindow({
	Name            = "Admin Panel",
	Subtitle        = "Management Console · RezurXlab",
	LoadingTitle    = "RezurX lab",
	LoadingEnabled  = true,
	Theme           = "Ember",            -- "Ember" | "Ocean" | "Crimson" | "Slate"
	ToggleUIKeybind = Enum.KeyCode.K,     -- hide/show the whole UI
})

-- ============================================================
-- OVERVIEW
-- ============================================================
local Overview = Window:CreateTab("Overview", "📊")

Overview:CreateSection("System Status")
local statusPara = Overview:CreateParagraph({
	Title = "Status",
	Content = "System ready.\nBoot sequence: OK\nActive: Yes",
})

Overview:CreateSection("Quick Actions")
Overview:CreateButton({
	Name = "Refresh",
	Callback = function()
		statusPara:Set({ Content = "Refreshed at " .. os.date("%X") })
		Window:Notify({ Title = "Refresh", Content = "Panel data refreshed.", Duration = 2, Type = "success" })
	end,
})
Overview:CreateButton({
	Name = "Help",
	Callback = function()
		Window:Notify({ Title = "Help", Content = "Documentation placeholder.", Duration = 3 })
	end,
})

-- ============================================================
-- PLAYERS — plain moderation UI. Hook the callbacks into your
-- own RemoteEvents; validate everything server-side.
-- ============================================================
local PlayersTab = Window:CreateTab("Players", "👥")

PlayersTab:CreateSection("Player Lookup")
local targetInput = PlayersTab:CreateInput({
	Name = "Player Name",
	PlaceholderText = "Enter username…",
	Flag = "TargetPlayer",
	Callback = function(text)
		print("[Players] Target set:", text)
	end,
})

PlayersTab:CreateDivider("moderation")
PlayersTab:CreateButton({
	Name = "Kick Player",
	Callback = function()
		local target = Lib.Flags.TargetPlayer and Lib.Flags.TargetPlayer:Get() or ""
		-- KickRemote:FireServer(target)
		Window:Notify({ Title = "Players", Content = "Fire your Kick RemoteEvent for: " .. target, Duration = 3 })
	end,
})
PlayersTab:CreateDropdown({
	Name = "Ban Duration",
	Options = { "1 Hour", "1 Day", "1 Week", "Permanent" },
	CurrentOption = "1 Day",
	Flag = "BanDuration",
	Callback = function(opt) print("[Players] Ban duration:", opt) end,
})
PlayersTab:CreateDropdown({
	Name = "Grant Roles",
	Options = { "Helper", "Moderator", "Admin", "Builder" },
	MultipleOptions = true,               -- multi-select: click several, list stays open
	CurrentOption = {},
	Flag = "GrantRoles",
	Callback = function(list) print("[Players] Roles:", table.concat(list, ", ")) end,
})
PlayersTab:CreateToggle({
	Name = "Freeze Target Player",
	CurrentValue = false,
	Flag = "FreezeTarget",
	Callback = function(v) print("[Players] Freeze:", v) end,
})

-- ============================================================
-- SETTINGS — themes, keybinds, sliders
-- ============================================================
local Settings = Window:CreateTab("Settings", "⚙")

Settings:CreateSection("Appearance")
Settings:CreateDropdown({
	Name = "Theme",
	Options = { "Ember", "Ocean", "Crimson", "Slate" },
	CurrentOption = "Ember",
	Callback = function(theme)
		Window:ModifyTheme(theme)  -- live re-theme, gradients included
	end,
})
Settings:CreateColorPicker({
	Name = "Highlight Color",
	Color = Color3.fromRGB(255, 122, 28),
	Flag = "HighlightColor",
	Callback = function(color) print("[Settings] Highlight:", color) end,
})

Settings:CreateDivider("keybinds")
-- Functional keybind: click the pill, press a key to rebind
-- (Escape cancels). Callback fires whenever the key is pressed.
Settings:CreateKeybind({
	Name = "Open Player List",
	CurrentKeybind = Enum.KeyCode.P,
	Flag = "PlayerListKey",
	Callback = function()
		Window:Notify({ Title = "Keybind", Content = "Player list keybind pressed.", Duration = 2 })
	end,
})
Settings:CreateKeybind({
	Name = "Push To Talk (hold)",
	CurrentKeybind = Enum.KeyCode.V,
	HoldToInteract = true,               -- Callback(true) on press, Callback(false) on release
	Callback = function(down) print("[Settings] PTT:", down) end,
})

Settings:CreateDivider("gameplay")
Settings:CreateSlider({
	Name = "Announcement Cooldown",
	Range = { 5, 120 },
	Increment = 5,
	Suffix = "s",
	CurrentValue = 30,
	Flag = "AnnounceCooldown",
	Callback = function(v) print("[Settings] Cooldown:", v) end,
})
Settings:CreateToggle({
	Name = "Notifications",
	CurrentValue = true,
	Flag = "NotifyOn",
	Callback = function(v) print("[Settings] Notifications:", v) end,
})

-- ============================================================
-- ABOUT
-- ============================================================
local About = Window:CreateTab("About", "ℹ")
About:CreateParagraph({
	Title = "Notes",
	Content = "Every control in this panel is UI-only. Wire each callback into your own "
		.. "server-validated RemoteEvents — nothing here touches the game directly.",
})
About:CreateLabel("RezurXLib v" .. Lib.Version)

-- Welcome toast
Window:Notify({
	Title = "Admin Panel",
	Content = "Loaded. Press K to hide/show the interface.",
	Duration = 4,
	Type = "success",
})
