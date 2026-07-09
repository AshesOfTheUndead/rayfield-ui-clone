#!/usr/bin/env python3
"""Fix save/load and destroy button in DOMINUS_V8.luau."""
import sys

filepath = "/home/z/my-project/DOMINUS_V8.luau"
with open(filepath, "r") as f:
    src = f.read()

# Find the save button start and destroy button end
save_start = src.find('SysTab:CreateButton({Name = "💾 Save Profile"')
if save_start == -1:
    print("ERROR: Save button not found")
    sys.exit(1)

# Find the end of the destroy button (the closing '})' after 'end})')
destroy_marker = 'if dc then Lib:Destroy()'
destroy_idx = src.find(destroy_marker, save_start)
if destroy_idx == -1:
    print("ERROR: Destroy button not found")
    sys.exit(1)

# Find the 'end})' that closes the destroy button
end_idx = src.find('end})', destroy_idx)
if end_idx == -1:
    print("ERROR: Destroy button end not found")
    sys.exit(1)
end_idx += len('end})')

old_block = src[save_start:end_idx]

new_block = '''SysTab:CreateButton({Name = "💾 Save Profile", Callback = function()
    if not writefile then notify("❌ Error","writefile N/A",4,"error") return end
    local profile = buildProfile()
    local json = HttpService:JSONEncode(profile)
    local ok, err = pcall(function() writefile(PROFILE_FILE, json) end)
    if ok then
        notify("💾 Saved", "Wrote "..tostring(#json).." bytes to "..PROFILE_FILE, 4, "success")
    else
        notify("❌ Save Failed", tostring(err):sub(1,60), 4, "error")
    end
end})
SysTab:CreateButton({Name = "📂 Load Profile", Callback = function()
    if not readfile then notify("❌ Error","readfile N/A",4,"error") return end
    local ok, c = pcall(readfile, PROFILE_FILE)
    if not ok or not c or c == "" then
        notify("⚠️ No Profile", "Save a profile first (file empty or missing)", 4, "warning")
        return
    end
    local ok2, p = pcall(function() return HttpService:JSONDecode(c) end)
    if not ok2 or type(p) ~= "table" then
        notify("❌ Error", "Profile corrupted: "..tostring(p):sub(1,50), 4, "error")
        return
    end
    -- [FIX] Wrap applyProfile in pcall so one error doesn't silently abort everything
    local ok3, err3 = pcall(applyProfile, p)
    if ok3 then
        notify("📂 Loaded", "Profile applied ("..tostring(#c).." bytes)", 4, "info")
    else
        notify("❌ Load Error", tostring(err3):sub(1,60), 5, "error")
    end
end})
SysTab:CreateButton({Name = "🗑️ Reset to Defaults", Callback = function()
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
SysTab:CreateSection("❌ DANGER")
local dc = false
SysTab:CreateButton({Name = "❌ Destroy UI (confirm)", Callback = function()
    if dc then
        notify("❌ Destroying...", "UI will be removed.", 3, "warning")
        task.delay(0.3, function()
            local ok, err = pcall(function() Lib:Destroy() end)
            if not ok then warn("[DOMINUS] Destroy error:", err) end
        end)
    else
        dc = true
        notify("⚠️ Confirm", "Click again within 5s to destroy UI", 5, "warning")
        task.delay(5, function() dc = false end)
    end
end})'''

src = src[:save_start] + new_block + src[end_idx:]

with open(filepath, "w") as f:
    f.write(src)

print("OK: save/load/destroy fixed in DOMINUS_V8.luau")
