# 👑 RezurXLab — Rayfield UI Clone + DOMINUS Engine

A RezurXLab UI library (RezurXLib) with the same API surface as Rayfield, plus the DOMINUS V7 engine for Train to Fight.

## 📦 Files

| File | Description |
|------|-------------|
| `RezurXLib.lua` | The UI library (ModuleScript). Janitor, shared drag router, Tween manager, themes, full component set. |
| `DOMINUS_V7.luau` | DOMINUS V7 engine — loads RezurXLib from this repo, wires the full farm/noclip/chat/ESP engine. 1000 workers, math.huge, PVP Off default ON. |
| `ExampleUsage.client.lua` | Example admin panel showing all RezurXLib components. |

## 🚀 Quick Start (DOMINUS V7)

Execute `DOMINUS_V7.luau` in your executor. It auto-loads RezurXLib from this repo's `main` branch.

```lua
loadstring(game:HttpGet("https://raw.githubusercontent.com/AshesOfTheUndead/rayfield-ui-clone/main/DOMINUS_V7.luau"))()
```

## 🎨 RezurXLib Features

- **Janitor** — every connection captured, zero leaks on teardown
- **Shared drag router** — ONE InputChanged/InputEnded pair for the whole script
- **Tween manager** — per-instance-per-property cancel
- **4 themes** — Ember (orange), Ocean (blue), Crimson (red), Slate (green)
- **Components** — Button, Toggle, Slider, Dropdown, ColorPicker, Input, Keybind, Paragraph, Label, Divider, Section
- **Window chrome** — drag (clamped), minimize (animated), close (fade contract), loading overlay
- **Notifications** — slide-in, progress bar, type icons
- **FPS + Ping** display
- **Idempotent re-run** — destroys prior instance first

## ⚡ DOMINUS V7 Engine

- 1000 max workers (100 default)
- `math.huge` train speed
- 0.001s worker loop (no anti-cheat delays)
- PVP Off default ON (0.2s aggressive spam, multiple area paths)
- Adaptive throttle (FPS + gains trend based)
- Overnight mode (5min work / 30s break cycles)
- Turbo boost (2x / 10s, 5s cooldown)
- V777 + Improved noclip (no upward glitch)
- ESP with cached BillboardGuis
- Chat bypass with RichText + color pickers
- Save/Load profiles
- Keyboard shortcuts (K, Ctrl+F, Ctrl+N, Ctrl+T)

## 👑 Credits

**Creator:** RezurXshin  
**Studio:** RezurXLabs  
**All rights reserved.** (c) 2026 RezurXshin.

---

## Next.js Project (v0)

This repository also contains a Next.js project for the RezurXLab website.

```bash
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000).
