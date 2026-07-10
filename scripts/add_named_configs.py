#!/usr/bin/env python3
"""Replace the profile section in DOMINUS_V8.luau with a named config system:
- Save with a name (type in input box, click save)
- Duplicate name detection
- Load by selecting from saved configs
- Delete configs
- Rename configs
"""
import sys

filepath = "/home/z/my-project/DOMINUS_V8.luau"
with open(filepath, "r") as f:
    src = f.read()

# Find the start of the profile section
profile_start = src.find('SysTab:CreateSection("💾 PROFILE")')
if profile_start == -1:
    print("ERROR: PROFILE section not found")
    sys.exit(1)

# Find the end — the DANGER section
danger_start = src.find('SysTab:CreateSection("❌ DANGER")', profile_start)
if danger_start == -1:
    print("ERROR: DANGER section not found")
    sys.exit(1)

old_block = src[profile_start:danger_start]

new_block = '''SysTab:CreateSection("💾 CONFIGS")
-- [FIX] Named config system: save with name, load by name, delete, rename
local CONFIGS_FILE = "DOMINUS_Configs.json"
local function buildProfile()
    return {
        CustomTag=Config.CustomTag, UserName=Config.UserName,
        TagColor={Config.TagColor.R,Config.TagColor.G,Config.TagColor.B},
        UserColor={Config.UserColor.R,Config.UserColor.G,Config.UserColor.B},
        MessageColor={Config.MessageColor.R,Config.MessageColor.G,Config.MessageColor.B},
        FarmMode=Config.FarmMode, FarmSpeedMul=Config.FarmSpeedMul,
        WorkerCount=Config.WorkerCount, MaxPerformance=Config.MaxPerformance,
        TrainSpeedValue=Config.TrainSpeedValue, AntiDetect=Config.AntiDetect,
        WalkSpeed=Config.WalkSpeed, JumpPower=Config.JumpPower,
        OverrideStats=Config.OverrideStats, NoclipMode=Config.NoclipMode,
        NoclipEnabled=Config.NoclipEnabled, AntiAfk=Config.AntiAfk,
        PvpOff=Config.PvpOff,
    }
end

local function applyProfile(p)
    local function safeSet(obj, val)
        if obj and val ~= nil then pcall(function() obj:Set(val) end) end
    end
    safeSet(UI.FarmMode, p.FarmMode)
    safeSet(UI.TrainSpeed, p.TrainSpeedValue)
    safeSet(UI.FarmSpeedMul, mulToStr(p.FarmSpeedMul or 1))
    safeSet(UI.NoclipMode, p.NoclipMode)
    safeSet(UI.Workers, p.WorkerCount)
    safeSet(UI.WalkSpeed, p.WalkSpeed)
    safeSet(UI.JumpPower, p.JumpPower)
    safeSet(UI.AntiDetect, p.AntiDetect)
    safeSet(UI.MaxPerf, p.MaxPerformance)
    safeSet(UI.OverrideStats, p.OverrideStats)
    safeSet(UI.Noclip, p.NoclipEnabled)
    safeSet(UI.AntiAfk, p.AntiAfk)
    safeSet(UI.PvpOff, p.PvpOff)
    safeSet(UI.CustomTitle, p.CustomTag or "")
    safeSet(UI.CustomName, p.UserName or "")
    safeSet(UI.TitlePreset, "None")
    safeSet(UI.NamePreset, "None")
    if p.TagColor then safeSet(UI.TagColor, Color3.new(p.TagColor[1],p.TagColor[2],p.TagColor[3])) end
    if p.UserColor then safeSet(UI.UserColor, Color3.new(p.UserColor[1],p.UserColor[2],p.UserColor[3])) end
    if p.MessageColor then safeSet(UI.MsgColor, Color3.new(p.MessageColor[1],p.MessageColor[2],p.MessageColor[3])) end
end

-- Load all saved configs from file
local function loadConfigsList()
    if not readfile then return {} end
    local ok, c = pcall(readfile, CONFIGS_FILE)
    if not ok or not c or c == "" then return {} end
    local ok2, data = pcall(function() return HttpService:JSONDecode(c) end)
    if not ok2 or type(data) ~= "table" then return {} end
    return data
end

-- Save configs map to file
local function saveConfigsList(data)
    if not writefile then return false end
    local ok = pcall(function() writefile(CONFIGS_FILE, HttpService:JSONEncode(data)) end)
    return ok
end

-- Refresh the config dropdown with current saved configs
local configDropdown = nil
local function refreshConfigs()
    if not configDropdown then return end
    local data = loadConfigsList()
    local names = {}
    for name, _ in pairs(data) do table.insert(names, name) end
    table.sort(names)
    if #names == 0 then names = {"(none)"} end
    configDropdown:Refresh(names, false)
end

-- Config name input
local nameInput = SysTab:CreateInput({
    Name = "✏️ Config Name",
    PlaceholderText = "Enter a name for this config...",
    Callback = function(v) end,
})

-- Saved configs dropdown
configDropdown = SysTab:CreateDropdown({
    Name = "📋 Saved Configs",
    Options = {"(none)"},
    CurrentOption = "(none)",
    Callback = function(v) end,
})
refreshConfigs()

SysTab:CreateButton({Name = "💾 Save Config (use name above)", Callback = function()
    if not writefile then notify("❌ Error", "writefile not available", 4, "error") return end
    local name = nameInput:Get()
    if not name or name == "" or name == "(none)" then
        notify("⚠️ Name Required", "Enter a config name in the input above first.", 4, "warning")
        return
    end
    local data = loadConfigsList()
    if data[name] then
        notify("❌ Already Exists", "Config '"..name.."' already exists. Use a different name or delete it first.", 5, "error")
        return
    end
    data[name] = buildProfile()
    local ok = saveConfigsList(data)
    if ok then
        notify("💾 Saved", "Config '"..name.."' saved successfully.", 4, "success")
        refreshConfigs()
        nameInput:Set("")
    else
        notify("❌ Save Failed", "Could not write to file.", 4, "error")
    end
end})

SysTab:CreateButton({Name = "📂 Load Selected Config", Callback = function()
    local sel = configDropdown:Get()
    if not sel or sel == "(none)" then
        notify("⚠️ None Selected", "Select a config from the dropdown first.", 4, "warning")
        return
    end
    local data = loadConfigsList()
    if not data[sel] then
        notify("❌ Not Found", "Config '"..sel.."' not found.", 4, "error")
        return
    end
    local ok, err = pcall(applyProfile, data[sel])
    if ok then
        notify("📂 Loaded", "Config '"..sel.."' applied to all settings.", 4, "info")
    else
        notify("❌ Load Error", tostring(err):sub(1,60), 5, "error")
    end
end})

SysTab:CreateButton({Name = "🗑️ Delete Selected Config", Callback = function()
    local sel = configDropdown:Get()
    if not sel or sel == "(none)" then
        notify("⚠️ None Selected", "Select a config from the dropdown first.", 4, "warning")
        return
    end
    local data = loadConfigsList()
    if not data[sel] then
        notify("❌ Not Found", "Config '"..sel.."' not found.", 4, "error")
        return
    end
    data[sel] = nil
    local ok = saveConfigsList(data)
    if ok then
        notify("🗑️ Deleted", "Config '"..sel.."' deleted.", 4, "info")
        refreshConfigs()
    else
        notify("❌ Delete Failed", "Could not write to file.", 4, "error")
    end
end})

SysTab:CreateButton({Name = "✏️ Rename Selected Config", Callback = function()
    local sel = configDropdown:Get()
    if not sel or sel == "(none)" then
        notify("⚠️ None Selected", "Select a config from the dropdown first.", 4, "warning")
        return
    end
    local newName = nameInput:Get()
    if not newName or newName == "" or newName == "(none)" then
        notify("⚠️ Name Required", "Enter a new name in the input above first.", 4, "warning")
        return
    end
    local data = loadConfigsList()
    if not data[sel] then
        notify("❌ Not Found", "Config '"..sel.."' not found.", 4, "error")
        return
    end
    if data[newName] then
        notify("❌ Name Exists", "Config '"..newName.."' already exists. Choose a different name.", 5, "error")
        return
    end
    data[newName] = data[sel]
    data[sel] = nil
    local ok = saveConfigsList(data)
    if ok then
        notify("✏️ Renamed", "'"..sel.."' → '"..newName.."'", 4, "success")
        refreshConfigs()
        nameInput:Set("")
    else
        notify("❌ Rename Failed", "Could not write to file.", 4, "error")
    end
end})

SysTab:CreateButton({Name = "🔄 Reset to Defaults", Callback = function()
    local ok, err = pcall(applyProfile, {
        CustomTag="", UserName="", TagColor={128,0,0}, UserColor={255,255,255}, MessageColor={255,255,255},
        FarmMode="Hybrid", FarmSpeedMul=1, WorkerCount=50, MaxPerformance=false,
        TrainSpeedValue="Infinity", AntiDetect=false, WalkSpeed=16, JumpPower=50,
        OverrideStats=false, NoclipMode="Improved", NoclipEnabled=false,
        AntiAfk=true, PvpOff=true,
    })
    if ok then
        notify("🔄 Reset", "All settings reset to defaults.", 3, "info")
    else
        notify("❌ Reset Error", tostring(err):sub(1,60), 5, "error")
    end
end})

'''

src = src[:profile_start] + new_block + src[danger_start:]

with open(filepath, "w") as f:
    f.write(src)

print("OK: Named config system added to DOMINUS_V8.luau")
