# 👑 RezurXLib

**A universal, premium UI library for Roblox** — built by RezurXLab for developers, trusted by players.

---

## 📦 What Is RezurXLib?

RezurXLib is a **complete, self-contained UI framework** for Roblox. It provides everything you need to build beautiful, functional, and reliable interfaces — whether you're creating an admin panel, a settings menu, a game hub, or any other in-game UI.

**It works everywhere:** CoreGui, PlayerGui, executors, and any environment that supports standard Roblox APIs.

---

## ✨ Features

### 🎨 Visual Excellence
- **7 built-in themes** — Ember, Ocean, Crimson, Slate, Midnight, Forest, Coral
- **Smooth animations** — 60fps tweens with Back/Exponential/Quad easings
- **Modern design** — depth, shadows, gradients, and micro-interactions
- **Responsive** — auto-scales to any screen size (desktop, mobile, tablet)

### 🧩 Complete Component Library
| Component | Description |
|-----------|-------------|
| **Window** | Draggable, minimizable, closeable, resizable |
| **Tabs** | Auto-sizing, scrollable, with sliding indicator |
| **Buttons** | Ripple feedback, hover states, callback error handling |
| **Toggles** | Smooth slide animation, reset method |
| **Sliders** | Throttled callbacks, live value display |
| **Dropdowns** | Searchable, multi-select, fuzzy matching |
| **Inputs** | Text boxes with focus states |
| **Keybinds** | Click to rebind, collision protection |
| **Color Pickers** | HSV, RGB, Hex, live preview, preset palettes |
| **Notifications** | Action buttons, type icons, progress bars |
| **Tooltips** | Hover + touch support |
| **Context Menus** | Nested options with icons |
| **Progress Bars** | Indeterminate and value display |
| **Spinners** | Loop animations, no heartbeat required |
| **Accordions** | Collapsible content sections |
| **Bindable Controls** | Toggle + keybind combined |
| **Carousels** | Image sliders with dots |
| **Search Bars** | Live filtering |

### 🛡️ Reliability & Trust
- **No telemetry** — zero analytics, zero data collection
- **No external requests** — never calls HttpGet/HttpPost
- **Error-handled** — every callback wrapped in `pcall`
- **Memory-safe** — Janitor pattern prevents leaks
- **Executor-compatible** — works in Synapse, Krnl, Script-Ware, Xeno, Delta, and more
- **Optional file I/O** — persistence is opt-in, never forced

### 👨‍💻 Developer Experience
- **Fluent API** — `:CreateWindow()`, `:CreateTab()`, `:CreateButton()`, `:Set()`, `:Get()`
- **Self-documenting** — comments on every public function
- **Built-in docs** — `Library:GetDocs()` for auto-reference
- **Global access** — `_G.RezurXLib = Library`
- **MIT licensed** — open, free, and transparent

---

## 🚀 Quick Start

### In a ModuleScript
```lua
local RezurXLib = require(path.to.RezurXLib)

local Window = RezurXLib:CreateWindow({
    Name = "My Panel",
    Subtitle = "Built with RezurXLib",
    Theme = "Ember",
})

local Tab = Window:CreateTab("Main", "📊")
Tab:CreateButton({
    Name = "Click Me",
    Callback = function()
        print("Button clicked!")
    end
})
```

### In an Executor (Synapse, Krnl, Xeno, etc.)
```lua
local RezurXLib = loadstring(game:HttpGet("https://raw.githubusercontent.com/AshesOfTheUndead/rayfield-ui-clone/main/RezurXLib.lua"))()
```

### Using the Global Reference
```lua
_G.RezurXLib:CreateWindow({
    Name = "Admin Panel",
})
```

---

## 🎨 Themes

| Theme | Description |
|-------|-------------|
| **Ember** | Warm orange accents — RezurXLab signature |
| **Ocean** | Cool blue accents — calm and professional |
| **Crimson** | Bold red accents — powerful and dramatic |
| **Slate** | Green accents — clean and modern |
| **Midnight** | Purple accents — deep and mysterious |
| **Forest** | Natural green accents — earthy and grounded |
| **Coral** | Soft pink accents — warm and inviting |

**Custom themes are easy to create** — just pass a token table to `Window:ModifyTheme()`.

---

## 📚 Documentation

### `Library:CreateWindow(config)`
Creates a new window.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Name` | `string` | Window title |
| `Subtitle` | `string` | Subtitle text |
| `Theme` | `string` | One of the built-in themes |
| `ToggleUIKeybind` | `Enum.KeyCode` | Keybind to toggle visibility |
| `LoadingEnabled` | `boolean` | Show loading animation |
| `Size` | `{X, Y}` | Window size (default: 460x500) |

**Returns:** `Window` object

---

### `Window:CreateTab(name, icon)`
Creates a new tab.

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | `string` | Tab label |
| `icon` | `string` | Emoji or icon text |

**Returns:** `Tab` object

---

### `Tab:CreateButton(config)`
Creates a button.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Name` | `string` | Button label |
| `Callback` | `function` | Called when clicked |
| `Tooltip` | `string` | Optional tooltip text |

**Returns:** `Button` object with `:Set()` method

---

### `Tab:CreateToggle(config)`
Creates a toggle switch.

| Parameter | Type | Description |
|-----------|------|-------------|
| `Name` | `string` | Toggle label |
| `CurrentValue` | `boolean` | Initial state |
| `Callback` | `function` | Called on state change |
| `Flag` | `string` | Optional flag for config |

**Returns:** `Toggle` object with `:Set()`, `:Get()`, `:Reset()` methods

---

*[Full API documentation available in `Library:GetDocs()`]*

---

## 📦 Files in This Repository

| File | Description |
|------|-------------|
| `RezurXLib.lua` | The complete UI library (ModuleScript) |
| `ExampleUsage.client.lua` | Example showing all components in action |

---

## 🏢 Powered By

| Project | Description |
|---------|-------------|
| **DOMINUS Engine** | Full-featured automation engine using RezurXLib |
| **RezurXLab Tools** | Various tools and utilities built with RezurXLib |

---

## 👑 Credits

**Creator:** RezurXshin  
**Studio:** RezurXLabs  
**License:** MIT — open, free, and transparent.

---

## 🙏 Acknowledgments

- Inspired by the **Rayfield UI Library** and its contributions to the Roblox community.
- Built with ❤️ for developers and players everywhere.

---

## 📜 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

**RezurXLib — The UI library you can trust.** 🚀
