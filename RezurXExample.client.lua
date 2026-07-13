--!strict
-- RezurXLib v3.1 complete component catalogue.
-- Put RezurXUI.lua in a ModuleScript named "RezurXUI" under ReplicatedStorage,
-- then run this LocalScript from StarterPlayerScripts or StarterGui.

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RezurXLib = require(ReplicatedStorage:WaitForChild("RezurXUI"))

-- Asset ids can be remembered by a friendly local key. This is only a small
-- in-memory registry; it does not preload or make a network request.
RezurXLib:RegisterImage("brand", 6031094678)

RezurXLib:RegisterTheme("Violet", {
    accent = Color3.fromRGB(136, 105, 244),
    accentHi = Color3.fromRGB(193, 174, 255),
    accentDim = Color3.fromRGB(88, 66, 170),
    accentDark = Color3.fromRGB(45, 34, 82),
    headerA = Color3.fromRGB(34, 29, 55),
    headerB = Color3.fromRGB(19, 17, 33),
})

local window = RezurXLib:CreateWindow({
    Name = "RezurX Showcase",
    Subtitle = "A complete, local component catalogue",
    Theme = "Quiet",
    Size = Vector2.new(540, 610),
    MinSize = Vector2.new(340, 380),
    Resizable = true,
    LoadingEnabled = true,
    ToggleUIKeybind = Enum.KeyCode.RightControl,
    Accessibility = { ReducedMotion = false },
})

local main = window:CreateTab("Controls", "C")
main:CreateSection("Core controls")
main:CreateLabel("Every callback in this example is isolated by the library.")
main:CreateParagraph({
    Title = "Built for normal Roblox UI",
    Content = "Use RezurXLib for game settings, diagnostics, moderation tools, and player-facing configuration.",
})
main:CreateDivider("Interactive")

main:CreateButton({
    Name = "Notify with actions",
    Tooltip = "Notifications can be tapped outside an action to dismiss.",
    Callback = function()
        window:Notify({
            Title = "Profile saved",
            Content = "The current Flag snapshot is ready.",
            Type = "success",
            Duration = 6,
            Actions = {
                { Text = "Undo", Callback = function() print("Undo requested") end },
                { Text = "Keep", Dismiss = true },
            },
        })
    end,
})

main:CreateMultiButton({
    Buttons = {
        { Name = "Violet theme", Callback = function() window:ModifyTheme("Violet") end },
        { Name = "Quiet theme", Callback = function() window:ModifyTheme("Quiet") end },
    },
})

local effects = main:CreateToggle({
    Name = "Enable effects",
    CurrentValue = true,
    Flag = "effectsEnabled",
    Callback = function(enabled)
        print("Effects enabled:", enabled)
    end,
})

local volume = main:CreateSlider({
    Name = "Music volume",
    Range = { 0, 100 },
    Increment = 1,
    CurrentValue = 65,
    Suffix = "%",
    Flag = "musicVolume",
    Callback = function(value)
        print("Music volume:", value)
    end,
})

main:CreateInput({
    Name = "Status message",
    CurrentValue = "Ready",
    PlaceholderText = "Type a short message...",
    Flag = "statusMessage",
    Callback = function(value)
        window:SetStatus(value, "healthy")
    end,
})

main:CreateDropdown({
    Name = "Quality preset",
    Options = { "Low", "Balanced", "High", "Ultra" },
    CurrentOption = "Balanced",
    Searchable = true,
    Flag = "qualityPreset",
    Callback = function(value)
        print("Quality:", value)
    end,
})

main:CreateDropdown({
    Name = "Enabled channels",
    Options = { "Chat", "Hints", "Trading", "Party", "Notifications" },
    CurrentOption = { "Chat", "Hints" },
    MultipleOptions = true,
    Searchable = true,
    Flag = "channels",
    Callback = function(values)
        print("Channels:", table.concat(values, ", "))
    end,
})

main:CreateKeybind({
    Name = "Quick action",
    CurrentKeybind = Enum.KeyCode.G,
    Flag = "quickAction",
    Callback = function()
        window:Notify({ Title = "Quick action", Content = "G was pressed.", Type = "info" })
    end,
})

main:CreateColorPicker({
    Name = "Accent preview",
    Color = Color3.fromRGB(8, 122, 72),
    Presets = {
        Color3.fromRGB(255, 255, 255),
        Color3.fromRGB(0, 0, 0),
        Color3.fromRGB(236, 82, 90),
        Color3.fromRGB(60, 160, 245),
        Color3.fromRGB(136, 105, 244),
    },
    Flag = "accentPreview",
    Callback = function(color)
        print("Accent RGB:", color.R, color.G, color.B)
    end,
})

main:CreateBindable({
    Name = "Feature shortcut",
    Keybind = Enum.KeyCode.H,
    Enabled = true,
    Callback = function()
        print("H pressed while the feature shortcut is enabled")
    end,
})

local feedback = window:CreateTab("Feedback", "F")
feedback:CreateSection("Visible progress")
feedback:CreateNotice({
    Title = "No hidden work",
    Content = "The spinner below only animates while it is explicitly running.",
    Type = "info",
})

local progress = feedback:CreateProgress({
    Name = "Asset preparation",
    Min = 0,
    Max = 100,
    CurrentValue = 34,
    Suffix = "%",
    Flag = "assetProgress",
})
feedback:CreateButton({
    Name = "Advance progress",
    Callback = function()
        progress:Set(math.min(progress:Get() + 11, 100))
    end,
})

local spinner = feedback:CreateSpinner({
    Name = "Background work",
    Detail = "Waiting for a request",
    Running = false,
})
feedback:CreateToggle({
    Name = "Run spinner",
    CurrentValue = false,
    Callback = function(running)
        if running then
            spinner:Set({ Detail = "Working...", Running = true })
        else
            spinner:Set({ Detail = "Waiting for a request", Running = false })
        end
    end,
})

feedback:CreateStatus({
    Name = "Service health",
    Text = "Connected",
    State = "online",
    Detail = "Updated locally",
})

feedback:CreateCodeBlock({
    Title = "Snapshot preview",
    Code = "local snapshot = RezurXLib:SaveConfiguration()",
    CopyCallback = function(code)
        print("Copy requested:", code)
    end,
})

feedback:CreateButton({
    Name = "Open confirmation modal",
    Callback = function()
        window:ShowModal({
            Title = "Reset controls?",
            Content = "This demonstration restores the toggle and slider to their defaults.",
            ConfirmText = "Reset",
            CancelText = "Keep values",
            Destructive = true,
            ConfirmCallback = function()
                effects:Reset()
                volume:Reset()
                window:Notify({ Title = "Reset", Content = "Defaults restored.", Type = "success" })
            end,
        })
    end,
})

local extras = window:CreateTab("Extras", "E")
extras:CreateSection("Extended components")
extras:CreateImage({
    Image = "brand",
    Height = 92,
    ScaleType = Enum.ScaleType.Fit,
    Tooltip = "A locally registered image identifier.",
})

extras:CreateCarousel({
    Items = {
        { Title = "Keyboard friendly", Description = "Use Tab, Enter, and arrow keys with selectable controls." },
        { Title = "Touch aware", Description = "Sliders, picker fields, menus, and panel dragging share pointer ownership." },
        { Title = "Theme tokens", Description = "Every built-in and custom palette uses the same semantic colour keys." },
    },
    Callback = function(item, index)
        print("Carousel item:", index, item.Title)
    end,
})

extras:CreateContextMenu({
    Name = "More actions",
    ButtonText = "OPEN MENU",
    Tooltip = "A popup that is not clipped by the scroll view.",
    Items = {
        { Text = "Show info", Callback = function() window:Notify({ Title = "Info", Content = "Context action fired.", Type = "info" }) end },
        { Text = "Show warning", Callback = function() window:Notify({ Title = "Warning", Content = "A safe warning example.", Type = "warning" }) end },
        { Text = "Unavailable", Disabled = true },
    },
})

local accordion = extras:CreateAccordion({
    Title = "Collapsible custom content",
    DefaultExpanded = false,
})
local customText = Instance.new("TextLabel")
customText.Size = UDim2.new(1, 0, 0, 36)
customText.BackgroundTransparency = 1
customText.Font = Enum.Font.Gotham
customText.TextSize = 12
customText.TextColor3 = Color3.fromRGB(205, 215, 208)
customText.TextWrapped = true
customText.Text = "Accordions expose a container for project-specific GuiObjects."
customText.Parent = accordion:GetContainer()

extras:CreateTable({
    Title = "Recent tasks",
    Columns = { "Task", "State", "Owner" },
    Rows = {
        { "Theme pass", "Done", "Client" },
        { "Input test", "Ready", "Client" },
        { "Review", "Queued", "Team" },
    },
    OnRowActivated = function(values)
        window:Notify({ Title = "Row selected", Content = tostring(values[1]), Type = "info" })
    end,
})

extras:CreateTextArea({
    Name = "Release notes",
    CurrentValue = "Write notes here.",
    MaxLength = 240,
    Tooltip = "Callbacks run on focus loss by default; set Live = true for live input.",
    Callback = function(value)
        print("Notes committed:", value)
    end,
})

-- The supplied settings tab exposes theme, motion, shortcut, status, and
-- minimize preferences. It returns a normal tab that can be extended further.
local settings = window:CreateSettingsPanel()
settings:CreateButton({
    Name = "Save Flag snapshot in memory",
    Callback = function()
        local snapshot = RezurXLib:SaveConfiguration()
        print("Saved snapshot:", RezurXLib:Serialize(snapshot))
    end,
})

-- GetDocs is useful for building a project-specific help tab.
print("RezurXLib docs:", RezurXLib:GetDocs().Version)
