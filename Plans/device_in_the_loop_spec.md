# Device-in-the-Loop Simulation in Isaac Sim
## Implementation Specification — v1

**Audience:** Implementer (new-grad SDE / robotics MS). This doc assumes Python fluency, basic React, and familiarity with Linux. It does **not** assume prior Omniverse, USD, or Isaac Sim experience — those are covered inline with pointers to canonical docs.

**Estimated effort:** 3–4 weeks full-time for a v1 demo. Add 1–2 weeks for polish and the recorded video.

**Owner:** [Implementer name]
**Reviewer / Architect:** Nirty
**Target completion:** ~4 weeks from kickoff

---

## 1. Project Summary

Build a working demo where:

1. A web-based HMI (factory dashboard, POS, or similar) runs in a headless browser.
2. Its rendered frames stream in real time onto the screen of a tablet asset inside an Isaac Sim scene.
3. A stylized human hand inside the sim can reach out and touch the tablet's screen.
4. Those touches map to coordinates on the source HMI and dispatch click/tap events.
5. The HMI responds, its updated frame streams back into the sim, and the loop closes.

A user interacting with the sim should feel like the simulated tablet behaves identically to a real tablet running the same HMI in a real browser. End-to-end touch-to-response latency target: **<150ms** (stretch goal: <80ms).

The output is:
- A public GitHub repo with reproducible setup
- A 45–90 second demo video
- A short technical write-up (markdown, in `docs/`)

The repo will be cited in a public LinkedIn / Substack post. Quality, reproducibility, and visual polish all matter.

---

## 2. Background & Why This Matters

Robotic simulators (Isaac Sim, Gazebo, MuJoCo) faithfully simulate physics, lighting, sensors, and materials, but treat displays — tablets, kiosks, HMIs — as static textures. Modern deployments of physical AI (warehouse robots, hospital carts, factory automation) constantly interact with such displays, and there is no public infrastructure for testing those interactions in simulation.

This project closes that gap with the smallest possible useful primitive: a tablet in Isaac Sim that behaves like the real thing because it actually runs the real HMI underneath. Downstream applications (training VLM policies that read screens, validating GUI agents in embodied settings, generating synthetic data for screen-aware perception models) all become possible once this primitive exists.

The technical primitive — pushing live pixel data to a USD material via Omniverse's `DynamicTextureProvider` — already exists (see MomentFactory's NDI extension for reference). The contribution here is the **closed-loop application**: bidirectional integration with a real screen source.

---

## 3. Architecture Overview

```
┌─────────────────┐         ┌──────────────────┐
│  React HMI      │  events │  WebSocket       │
│  (Vite + Chrome)│◄────────│  Server (Node)   │
└────────┬────────┘         └──────────▲───────┘
         │ rendered                    │ tap events (UV→px)
         ▼                             │
┌─────────────────┐                    │
│  Playwright     │                    │
│  Screencast     │                    │
└────────┬────────┘                    │
         │ frames (RGBA, 30 fps)       │
         ▼                             │
┌─────────────────────────────────────┴────────┐
│         Isaac Sim Extension (Python)         │
│  ┌────────────────┐  ┌────────────────────┐  │
│  │ Frame Receiver │  │ Touch Dispatcher   │  │
│  └────────┬───────┘  └────────▲───────────┘  │
│           │ push               │ UV→pixel    │
│           ▼                    │             │
│  ┌────────────────┐  ┌────────┴───────────┐  │
│  │  Dynamic       │  │  Contact Listener  │  │
│  │  Texture       │  │  (fingertip∩plane) │  │
│  │  Provider      │  └────────────────────┘  │
│  └────────┬───────┘                          │
└───────────┼──────────────────────────────────┘
            │ dynamic://tablet_screen
            ▼
   ┌────────────────────┐
   │  Tablet USD asset  │
   │  (emissive shader) │
   └────────────────────┘
```

Three processes:
- **Browser process** (headless Chromium, driven by Playwright): runs the HMI, exposes a CDP endpoint for screencast, and a WebSocket endpoint for incoming taps.
- **Isaac Sim process**: hosts the extension, scene, dynamic texture provider, and contact-detection logic.
- **WebSocket relay** (lightweight Node server, optional): can be merged into the browser process for v1.

For v1, the simplest topology is **two processes**: the Playwright script (which embeds the WS server) and Isaac Sim. They communicate over `localhost` only.

---

## 4. Prerequisites & Environment

### Hardware

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| GPU       | RTX 3060 (8GB) | RTX 4070+ (12GB+) |
| RAM       | 16 GB    | 32 GB |
| CPU       | 6 cores  | 12+ cores |
| Disk      | 50 GB free | 100 GB free (SSD) |
| OS        | Ubuntu 22.04 LTS | Ubuntu 22.04 LTS |

Windows 11 works too, but Linux is the documented Isaac Sim path and the implementer should default to it.

### Software versions (pin these)

- **NVIDIA driver:** ≥ 535 (check Isaac Sim release notes for the exact range matching the chosen Isaac Sim version)
- **Isaac Sim:** 5.0 or later (built on Omniverse Kit 107.x). Install via the official binaries from the Isaac Sim GitHub releases page; do not use the deprecated Omniverse Launcher.
- **Python:** 3.11 (Isaac Sim ships its own; you'll use `python.sh` from the Isaac Sim install)
- **Node.js:** 20.x LTS
- **Playwright (Python):** 1.45+
- **React:** 18+ with Vite 5+
- **Git LFS:** required if you ever commit USD assets

### Required accounts

- GitHub (for the public repo)
- None else — all tools are free and don't require sign-ups for this scope

### Learning path before coding

Spend the first 2–3 days reading and running the following. Do not skip — the project assumes you understand each at a basic level:

1. **Isaac Sim Quick Start:** docs.isaacsim.omniverse.nvidia.com — load a scene, run the simulation, open the Python script editor.
2. **Omniverse Kit Extension tutorial:** kit-app-template repo on GitHub. Build and load a "Hello World" extension. Understand `extension.toml`, the extension lifecycle (`on_startup` / `on_shutdown`), and how to register UI.
3. **USD basics:** Pixar's USD tutorial (`openusd.org/release/tut_usd_tutorials.html`). Read the first 4 sections only — Stage, Layer, Prim, Property. Don't go deep.
4. **USD shader / MDL materials:** read NVIDIA's MDL material guide for Omniverse — focus on how a Mesh prim binds to a Material prim and how a Shader's texture inputs reference asset paths.
5. **`omni.ui.DynamicTextureProvider` API:** read the omni.ui docs for `ByteImageProvider` and `DynamicTextureProvider`. Run the example that creates a 2x2 pixel texture and assigns it to a UI widget — get this working first.
6. **MomentFactory NDI extension:** clone `github.com/MomentFactory/Omniverse-NDI-extension` and read the source. ~300 lines of Python; you'll borrow patterns directly.
7. **Playwright Python:** `playwright.dev/python`. Run the headless screenshot example.

Total: ~3 days. Don't write any project code before completing this list.

---

## 5. Project Structure

Use this layout exactly. Predictable structure helps the reviewer.

```
device-in-the-loop-isaacsim/
├── README.md
├── LICENSE                      # MIT
├── .gitignore
├── docs/
│   ├── ARCHITECTURE.md
│   ├── SETUP.md
│   └── images/
├── hmi/                         # Web HMI (React + Vite)
│   ├── package.json
│   ├── vite.config.ts
│   ├── index.html
│   └── src/
│       ├── App.tsx
│       ├── pages/FactoryDashboard.tsx
│       └── lib/remoteTouch.ts
├── streamer/                    # Playwright-based frame streamer + WS relay
│   ├── requirements.txt
│   ├── streamer.py
│   └── ws_server.py
├── isaac-ext/                   # Omniverse Kit extension
│   └── exts/com.devloop.tablet/
│       ├── config/extension.toml
│       └── com/devloop/tablet/
│           ├── __init__.py
│           ├── extension.py
│           ├── stream_receiver.py
│           ├── texture_provider.py
│           ├── touch_detector.py
│           └── ws_client.py
├── scenes/                      # USD assets
│   ├── tablet.usda
│   ├── factory_demo.usda
│   └── materials/
│       └── screen_mat.mdl
├── scripts/
│   ├── start_hmi.sh
│   ├── start_streamer.sh
│   └── start_sim.sh
└── tests/
    ├── test_uv_mapping.py
    └── test_latency.py
```

---

## 6. Component 1: Web HMI

A simple React + Vite app. Single page, factory-dashboard style. The HMI must:

- Render at exactly **1024 × 768** (matches the tablet screen resolution in sim; if you change one, change both)
- Have at least 6 interactive elements arranged in a grid that are easy to hit (large buttons ≥ 100×100 px)
- Show state visibly (e.g., a counter that increments on click, a status banner that changes color)
- Accept synthetic pointer events sent over WebSocket and dispatch them to the right DOM element

### Suggested screen content for v1

A factory-floor task dashboard:
- Header bar showing current shift and operator ID
- 4 large task tiles ("Inspect Bin 4", "Replenish Line 2", etc.) — each toggles a state when tapped
- A status panel showing the most recently tapped tile
- A counter showing total taps received
- A timestamp of last event

This gives the demo something visually demonstrative without requiring complex UI logic.

### Synthetic touch dispatch (HMI side)

In `src/lib/remoteTouch.ts`, open a WebSocket to `ws://localhost:8765`. On message receipt, parse `{type, x, y}` and dispatch a synthetic PointerEvent at that location:

```typescript
const ws = new WebSocket('ws://localhost:8765/touch');
ws.onmessage = (msg) => {
  const { type, x, y } = JSON.parse(msg.data);
  const el = document.elementFromPoint(x, y);
  if (!el) return;

  if (type === 'down') {
    el.dispatchEvent(new PointerEvent('pointerdown', {
      clientX: x, clientY: y, bubbles: true, pointerType: 'touch'
    }));
  } else if (type === 'up') {
    el.dispatchEvent(new PointerEvent('pointerup', {
      clientX: x, clientY: y, bubbles: true, pointerType: 'touch'
    }));
    el.dispatchEvent(new PointerEvent('click', {
      clientX: x, clientY: y, bubbles: true
    }));
  }
};
```

This deliberately mimics a real touch by firing `pointerdown` → `pointerup` → `click` in sequence. Most React handlers will respond to `click`; some interactive components (drag, hold) need the lower-level events.

### Acceptance for this component

- Runs standalone in a normal browser at `http://localhost:5173`
- All buttons clickable by mouse
- Connecting to `ws://localhost:8765/touch` and sending `{type:'down', x:200, y:300}` followed by `{type:'up', x:200, y:300}` triggers the button at (200, 300) and updates state visibly
- Renders at exactly 1024×768 with no scrollbars

---

## 7. Component 2: Frame Streamer + WS Server

A Python process that:
1. Launches a headless Chromium via Playwright, loads the HMI from `http://localhost:5173`
2. Subscribes to Chrome DevTools Protocol's `Page.startScreencast` for streamed frames
3. Decodes frames (base64 PNG/JPEG from CDP) → raw RGBA → sends over a Unix domain socket or TCP to Isaac Sim
4. Hosts a WebSocket server on port 8765 that accepts inbound touch events from Isaac Sim and forwards them to the HMI WebSocket client

### Frame capture: CDP `startScreencast` vs `page.screenshot()`

- `page.screenshot()` in a tight loop: simple but slow (~10–15 fps achievable, lots of allocation)
- CDP `Page.startScreencast`: callback-based, returns JPEG frames at up to 60 fps, lower CPU

Use CDP for v1. Example skeleton:

```python
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=['--disable-gpu-vsync'])
        context = await browser.new_context(viewport={'width': 1024, 'height': 768})
        page = await context.new_page()
        await page.goto('http://localhost:5173')

        client = await context.new_cdp_session(page)
        await client.send('Page.startScreencast', {
            'format': 'jpeg',
            'quality': 80,
            'everyNthFrame': 1
        })

        client.on('Page.screencastFrame', on_frame)

        # keep alive
        while True:
            await asyncio.sleep(1)

async def on_frame(params):
    jpeg_b64 = params['data']
    session_id = params['sessionId']
    await client.send('Page.screencastFrameAck', {'sessionId': session_id})

    jpeg_bytes = base64.b64decode(jpeg_b64)
    rgba = jpeg_to_rgba(jpeg_bytes)   # use PIL or turbojpeg
    await send_to_sim(rgba)
```

Decode JPEG → RGBA with **PyTurboJPEG** if you can install it (5–10x faster than PIL), otherwise PIL.

### IPC to Isaac Sim

Two options:
- **TCP localhost socket** (simpler, recommended for v1). Length-prefixed binary frames: 4-byte width (little-endian uint32), 4-byte height, 4-byte timestamp_ms, then `width*height*4` bytes of RGBA.
- **Unix domain socket** (slightly faster, Linux-only): same protocol over an AF_UNIX socket.

Stick with TCP for v1. Port `9876`.

### WS server for touch events

In the same process, run a small `websockets` server on port `8765`. Accept connections from both:
- The HMI (browser): receives touch events to dispatch
- Isaac Sim: sends touch events

On receipt from Isaac Sim, broadcast to the HMI connection. Hold a single HMI connection at a time; reject extras.

### Acceptance

- Start Playwright, point at the HMI, see frames arriving on the TCP port at ≥30 fps
- Send a touch JSON via WS from a test script (`websocat ws://localhost:8765/sim` then paste `{"type":"down","x":512,"y":384}`), see HMI respond
- Process runs for 30 minutes without leaking memory above 1 GB

---

## 8. Component 3: Isaac Sim Extension (Display Side)

Build as a standard Omniverse Kit extension. Use the kit-app-template's extension scaffold as a starting point.

### `extension.toml`

```toml
[package]
title = "Device-in-the-Loop Tablet"
version = "0.1.0"
category = "simulation"

[dependencies]
"omni.kit.uiapp" = {}
"omni.ui" = {}
"omni.usd" = {}
"omni.physx" = {}

[[python.module]]
name = "com.devloop.tablet"
```

### `extension.py` (lifecycle)

```python
import omni.ext
from .stream_receiver import StreamReceiver
from .texture_provider import ScreenTextureProvider
from .touch_detector import TouchDetector
from .ws_client import TouchDispatcher

class DeviceInTheLoopExtension(omni.ext.IExt):
    def on_startup(self, ext_id):
        self.provider = ScreenTextureProvider("tablet_screen", width=1024, height=768)
        self.receiver = StreamReceiver(host='127.0.0.1', port=9876, on_frame=self.provider.push)
        self.dispatcher = TouchDispatcher(url='ws://127.0.0.1:8765/sim')
        self.touch_detector = TouchDetector(
            screen_prim_path='/World/Tablet/Screen',
            finger_prim_path='/World/Hand/Fingertip',
            screen_width_px=1024,
            screen_height_px=768,
            on_touch=self.dispatcher.send
        )
        self.receiver.start()
        self.dispatcher.start()
        self.touch_detector.start()

    def on_shutdown(self):
        self.receiver.stop()
        self.dispatcher.stop()
        self.touch_detector.stop()
```

### `texture_provider.py`

```python
import omni.ui as ui

class ScreenTextureProvider:
    def __init__(self, name: str, width: int, height: int):
        self.provider = ui.DynamicTextureProvider(name)
        self.width = width
        self.height = height
        # Hold a reference so it isn't garbage collected.

    def push(self, rgba_bytes: bytes):
        # rgba_bytes must be width * height * 4 bytes, RGBA8 layout.
        self.provider.set_bytes_data(rgba_bytes, [self.width, self.height])
```

### `stream_receiver.py`

A background thread that connects to the streamer's TCP port, reads framed packets, and calls `on_frame(rgba_bytes)` for each.

Use Python's `asyncio` if you want; threading is fine for v1 and easier to reason about. Make sure the `push` call lands on the main Kit thread or is itself safe to call from a worker thread (test it — `DynamicTextureProvider.set_bytes_data` is documented to be safe from worker threads in recent Kit versions, but verify on your installed version with a quick test).

If you hit thread-safety issues, marshal the call into the Kit update loop using `omni.kit.app.get_app().get_update_event_stream()`.

### Performance notes

- For 30 fps at 1024×768 RGBA = ~95 MB/s. Localhost TCP handles this comfortably.
- v1: CPU-side push via `set_bytes_data`. Acceptable.
- v2 (later optimization): GPU-side push via `set_bytes_data_from_gpu` with a CUDA pointer, avoiding the CPU roundtrip. Use Warp or PyTorch tensors. Skip for v1 unless you need >60 fps.

### Acceptance

- Run the streamer, then start Isaac Sim with the extension loaded
- Open the included `factory_demo.usda` scene
- The tablet's screen surface should display the live HMI
- Tap the HMI in a separate browser window manually — the tablet in sim should update within 100 ms
- Stable for 10+ minutes

---

## 9. Component 4: USD Scene & Tablet Asset

Create two USD files.

### `tablet.usda` — the tablet asset itself

A simple ruggedized panel:
- Outer body: rounded box, **260 × 180 × 12 mm**, dark gray PBR material (Albedo: 0.1 / 0.1 / 0.1)
- Screen quad: child mesh, **220 × 140 mm**, positioned 0.1 mm forward of the body's front face, **separate material binding**
- The screen quad is a single rectangular Mesh prim with two triangles. Set UVs so (0,0) is the top-left corner of the visible content and (1,1) is the bottom-right.

If modeling from scratch feels slow, grab a free CC-licensed tablet model from Sketchfab and decompose it:
- Open in Blender
- Separate the screen face into its own object
- Export both as USD with Blender's USD exporter

Either way, the deliverable is a USD with two children:
```
/Tablet
  /Body          (Mesh, material: BodyMat)
  /Screen        (Mesh, material: ScreenMat)
```

### `ScreenMat` — the dynamic material

Author this in USD Composer or directly in USD. Use an OmniPBR or OmniSurface MDL material with:

- `emissive_color_texture` asset path: `dynamic://tablet_screen`
- `emissive_intensity`: 8000 (the screen should be a light emitter, not a reflector — this number is roughly what a tablet at 50% brightness produces in nits, scaled to Omniverse's units)
- `diffuse_color`: black (0, 0, 0) — we want the screen to emit, not reflect ambient
- `enable_emission`: true

**Why emissive, not diffuse:** a real device screen lights itself. If you bind the dynamic texture to diffuse, the screen will look dim/dead in any lighting other than bright direct light. Emissive makes it self-luminous and matches real device behavior, including in low-light scenes.

### `factory_demo.usda` — the demo scene

- Floor plane (concrete material)
- Wall behind the tablet (industrial gray)
- Tablet mounted on a wall bracket (reference `tablet.usda`)
- Stylized hand (Component 7) positioned in front
- A camera positioned to show the tablet and hand together (this becomes the demo video angle)
- A second camera that's roughly where a human user's head would be (first-person view for the demo)
- Lighting: one key area light, one fill, slight environment HDRI for ambient

Keep the scene small — it should load in <5 seconds.

### Acceptance

- Open `factory_demo.usda` in Isaac Sim, the scene loads cleanly
- The tablet appears, the screen surface is visible
- With no extension loaded, the screen shows as black (the dynamic texture isn't yet bound)
- With the extension loaded and streamer running, the screen shows live HMI content

---

## 10. Component 5: Touch Interaction (Sim Side)

The touch system has three jobs:
1. Detect when the fingertip primitive contacts the screen plane.
2. Convert that contact point into screen-space UV coordinates (range [0, 1]² over the visible content area).
3. Convert UV to pixel coordinates and emit a touch event.

### Detection strategy

Two viable approaches:

**Option A — Ray casting (recommended for v1).**
- Each Kit update tick, cast a short ray from the fingertip in the direction of the screen normal
- If the ray hits the screen prim within a small threshold (e.g., 5 mm), emit a touch-down event
- When the ray no longer hits, emit a touch-up
- Pros: simple, predictable, no PhysX needed
- Cons: requires the fingertip to be aimed roughly perpendicular to the screen

**Option B — Physics trigger collider.**
- Attach a `Trigger` collider (PhysX) to the screen prim
- Attach a small sphere collider to the fingertip
- On overlap-begin, emit touch-down; on overlap-end, emit touch-up
- Pros: more natural, handles oblique approaches
- Cons: requires PhysX setup, can be flaky with very thin trigger geometry

Use **Option A for v1**. Migrate to Option B in v2 if accuracy matters.

### UV computation

Given a 3D contact point `P_world`, the screen mesh's world transform `M`, and the screen's local-space dimensions (`Sx`, `Sy`):

```
P_local = M^-1 · P_world
u = (P_local.x / Sx) + 0.5      # assuming screen is centered at local origin
v = 1.0 - ((P_local.y / Sy) + 0.5)   # flip Y if your UVs run top-down
```

Validate this with a calibration step (see Section 13). The Y-flip is the most common bug; expect to debug it.

### Touch event emission

```python
from .ws_client import TouchDispatcher

def on_touch_down(self, uv):
    px = int(uv[0] * self.screen_width_px)
    py = int(uv[1] * self.screen_height_px)
    self.dispatcher.send({'type': 'down', 'x': px, 'y': py})

def on_touch_up(self, uv):
    px = int(uv[0] * self.screen_width_px)
    py = int(uv[1] * self.screen_height_px)
    self.dispatcher.send({'type': 'up', 'x': px, 'y': py})
```

Debounce: don't emit more than one event per 50 ms. If the fingertip jitters, you'll spam clicks.

### Acceptance

- Hand-place the fingertip exactly at the center of the screen surface → UV should be (0.5, 0.5)
- Move to each corner → UVs should be (0,0), (1,0), (0,1), (1,1) (or correctly flipped)
- Verify in HMI logs that pixel coordinates match expected positions
- A test button at HMI position (512, 384) is triggered when the fingertip touches the screen center

---

## 11. Component 6: Touch Routing to HMI

Already covered in Components 2 and 6 — the dispatcher (`ws_client.py`) in the Isaac Sim extension is a thin WebSocket client. Keep it dumb: connect, reconnect on failure, fire-and-forget JSON.

```python
import websocket
import json
import threading

class TouchDispatcher:
    def __init__(self, url):
        self.url = url
        self.ws = None
        self._thread = None
        self._running = False

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self):
        while self._running:
            try:
                self.ws = websocket.create_connection(self.url)
                while self._running:
                    # keep alive; rely on send() to detect disconnects
                    self.ws.recv()  # blocks, server sends pings
            except Exception as e:
                print(f"[TouchDispatcher] reconnecting: {e}")
                time.sleep(1)

    def send(self, event: dict):
        if self.ws:
            try:
                self.ws.send(json.dumps(event))
            except Exception:
                self.ws = None  # next loop reconnects

    def stop(self):
        self._running = False
        if self.ws:
            self.ws.close()
```

Use `websocket-client` (synchronous library); install with `python.sh -m pip install websocket-client`.

---

## 12. Component 7: Stylized Hand

Ship two versions.

### v1 — Mouse-driven fingertip

The minimum viable interaction.

- A simple stylized fingertip mesh — a small elongated capsule or sphere — placed at `/World/Hand/Fingertip`
- A plane in world space, parallel to the tablet screen and 30 cm in front of it, defines the "input plane"
- Mouse cursor position → plane coordinates via the active camera's projection inverse
- Mouse scroll wheel (or W/S keys) → fingertip Z position (depth toward screen)
- Mouse left button down → push fingertip 30 cm forward along its forward axis (toward screen), triggering contact
- Mouse left button up → retract

Bind to Kit's input events via `omni.appwindow.get_default_app_window().get_keyboard()` / `.get_mouse()`. The kit-app-template repo has examples.

### v2 — IK-rigged hand or arm

Visual upgrade for the demo video.

- Import a rigged hand or forearm model. Free options: Mixamo (rig your own static hand), or NVIDIA's Audio2Face hand assets if accessible
- Add a 2-bone IK solver (shoulder-elbow-wrist, or upper-arm-forearm-wrist) targeting the fingertip
- Drive the IK target with the same input as v1 (mouse position in 3D)
- Pose the rest of the hand in a "pointing index finger" pose, static

Isaac Sim has IK support via the `omni.isaac.motion_generation` package or via OmniGraph; either is acceptable. The new grad should expect to spend ~2 days getting IK to look natural.

### v3 (out of scope for v1, plan for follow-up)

VR controller input via OpenXR. Requires a Quest 3 or similar and SteamVR/OpenXR setup. Worth ~1 week of work. Save for a v2 post.

### Acceptance

- v1: User can move the fingertip with the mouse and tap buttons on the HMI with reasonable precision (hits intended button >80% of attempts)
- v2: The hand reaches to the target with visually plausible motion, no obvious snapping or pose explosions

---

## 13. Calibration & Latency

### One-time calibration

The most failure-prone part of the project. Don't skip.

1. With the extension and streamer running, load a calibration HMI page that fills the screen with a 4×4 grid of numbered tiles
2. Manually move the fingertip to tile (0,0) (top-left). Print the computed UV. It should be approximately (0.125, 0.125) (center of the top-left cell). If it's off, debug the UV transform.
3. Repeat for tile (3,3) (bottom-right). Should be approximately (0.875, 0.875).
4. If Y is flipped, fix the flip in the UV transform code.
5. If X is mirrored (left-right swap), check the screen mesh's local-axis orientation — it may be facing -X instead of +X.

Encode the calibration result as constants in code. Do not make the screen prim's transform variable for v1; if you ever move the tablet in the scene, recompute the UV transform from the prim's `xformOp`.

### Latency measurement

Set up a simple test:
- HMI displays a button labeled "PING"
- Clicking the button in the HMI: record the timestamp on the HMI, send it to a logging endpoint
- The HMI's PING handler also updates the screen to display "PONG" with the original ping timestamp
- In Isaac Sim: when the fingertip taps PING, record timestamp `t_sim_tap`
- When the tablet's screen shows "PONG" (visible in the rendered viewport), the streamer can detect the frame change and log `t_pong_visible`
- Latency = `t_pong_visible - t_sim_tap`

You'll need at least a 3-second running average; single-frame measurements are too noisy.

Target: <150 ms round-trip. If you're getting >300 ms, profile the streamer (JPEG decode is the usual culprit) and the touch dispatch (WebSocket reconnect loops).

---

## 14. Milestones & Acceptance Criteria

Track these as GitHub Issues / Project board columns. Each milestone is a demoable artifact.

**Week 1: Display flow**
- [ ] Repo created, README skeleton in place
- [ ] HMI runs at `localhost:5173` with all 6 interactive elements working manually
- [ ] Playwright streamer connects to HMI, captures frames, logs FPS ≥30
- [ ] TCP framing protocol implemented; a Python test client can receive and save a frame as PNG
- [ ] Isaac Sim extension loads, creates a `DynamicTextureProvider`, displays a static test pattern (e.g., red square)
- [ ] Live HMI streams to the tablet in Isaac Sim. Visible, no crashes.

**Week 2: Touch flow**
- [ ] Stylized fingertip prim (v1, mouse-driven) implemented
- [ ] Ray-cast contact detection working; UVs printed to console match expected
- [ ] WebSocket dispatcher sends events from sim
- [ ] HMI receives events and synthesizes pointer events that trigger buttons
- [ ] End-to-end: user moves mouse in sim → fingertip taps screen → HMI button responds
- [ ] Calibration verified at all 4 corners

**Week 3: Polish**
- [ ] IK-rigged hand (v2) implemented and works
- [ ] Factory demo scene composed with good lighting and camera angles
- [ ] HMI content polished: realistic-looking dashboard, not placeholder text
- [ ] Latency measured and documented (<150 ms target)
- [ ] Stable for 30+ minute sessions
- [ ] README documents setup, with screenshots
- [ ] `ARCHITECTURE.md` written

**Week 4: Demo and release**
- [ ] Demo video recorded: 45–90 seconds, split-screen showing HMI in browser + sim viewport
- [ ] All TODOs in code resolved
- [ ] Repo is public, MIT-licensed
- [ ] Tag a v0.1.0 release
- [ ] Short technical write-up in `docs/POST.md` (~800 words) — this is the basis for the public post

---

## 15. Demo Recording Notes

The video is the primary deliverable for visibility. Treat it as a product, not an afterthought.

- Record at 1080p minimum, 60 fps. Use OBS Studio.
- Two source captures: the HMI in a normal browser window (left half), the Isaac Sim viewport (right half). Composite in OBS or in post.
- Add a third small overlay showing the WebSocket message log scrolling — proves it's live, not pre-rendered.
- No voiceover. Use clean text labels for each beat.
- Length: 45–75 seconds. Anything longer loses social media reach.
- Suggested beats:
  1. (0–5s) Title card: "Device-in-the-Loop Simulation in Isaac Sim"
  2. (5–15s) HMI running standalone in browser. "This is a normal web HMI."
  3. (15–25s) Cut to Isaac Sim viewport. Tablet on a factory wall, same HMI rendering on its screen. "Now it's running inside the simulation."
  4. (25–45s) Hand reaches over, taps buttons. HMI responds. Counter increments. "Touch input from the sim drives the real HMI."
  5. (45–60s) Wider shot, robot or environment context. "Foundation for closed-loop testing of embodied agents that interact with displays."
  6. (60s+) End card with repo link.

Shoot multiple takes. The hand motion in v2 will need rehearsing.

---

## 16. References

- Isaac Sim Documentation: `docs.isaacsim.omniverse.nvidia.com`
- Omniverse Kit App Template: `github.com/NVIDIA-Omniverse/kit-app-template`
- `omni.ui.DynamicTextureProvider` API: Omniverse Kit docs, omni.ui module
- MomentFactory NDI Extension (reference implementation pattern): `github.com/MomentFactory/Omniverse-NDI-extension`
- Pixar USD tutorials: `openusd.org/release/tut_usd_tutorials.html`
- Playwright Python: `playwright.dev/python`
- Chrome DevTools Protocol — Page domain: `chromedevtools.github.io/devtools-protocol/tot/Page`
- React + Vite quickstart: `vitejs.dev`

---

## 17. Known Pitfalls

- **Forgetting to hold a Python reference to `DynamicTextureProvider`.** It will be garbage collected and the texture will disappear silently. Always assign to `self.provider` (or a module-level variable) on creation.
- **Y-axis flipped in UV mapping.** Touch lands on the wrong button, mirrored vertically. Easy fix once you suspect it; spend 30 seconds testing each corner before assuming complex bugs.
- **Screen mesh oriented backward.** The screen surface might face -Z instead of +Z in local space depending on how the asset was authored. Test by enabling backface culling and rotating until it's visible from the expected angle.
- **JPEG decode bottleneck.** If FPS is below 20 in the streamer, `from turbojpeg import TurboJPEG` will fix it (3–5x speedup over PIL).
- **Synchronous frame push blocks the Kit update thread.** If the sim viewport stutters, marshal the texture push into an async task or run frame reception on a separate thread that touches `set_bytes_data` from the main thread via a queue.
- **Emissive vs diffuse on the screen material.** Screen looks dead in dim scenes if you bind to diffuse. Always emissive.
- **TCP framing bugs.** Length prefixes must be little-endian uint32 and must match the actual payload size; a mismatch makes the receiver lose sync. Add an explicit magic number (e.g., `0xDEADBEEF`) at the start of each frame for easy resync after errors.
- **WebSocket port collisions.** If something else is on 8765 or 9876, the streamer fails silently. Add health logs.
- **`DynamicTextureProvider` is officially beta.** It works reliably on Kit 107.x but is not a versioned API. If NVIDIA changes it in a major Kit update, the extension will need re-validation. Document the Kit version pinned in the repo's README.
- **Mouse-cursor → 3D plane projection.** Don't try to invert the camera projection by hand. Use Isaac Sim's existing viewport utilities (`omni.kit.viewport.utility`) to get a ray from screen-space, then intersect with the input plane.
- **Isaac Sim shaders compile on first launch.** Takes 5–10 minutes. Don't think the build is broken; let it finish.

---

## Appendix A: Suggested Reading Order if Time-Constrained

If you have less than 3 days to onboard:
1. Isaac Sim quick-start tutorial (run the GUI, load a scene)
2. The kit-app-template README and one tutorial extension
3. The `omni.ui.DynamicTextureProvider` reference page
4. Skim MomentFactory NDI extension source
5. Playwright Python quickstart

Skip USD tutorials initially; learn USD as needed when authoring the tablet asset.

## Appendix B: Definition of Done (v1 release)

- [ ] Public GitHub repo with MIT license
- [ ] README has 1-paragraph summary, prerequisites, 5-step quickstart, and screenshots
- [ ] `./scripts/start_*.sh` scripts launch each component
- [ ] Demo video committed (or hosted, linked from README)
- [ ] Reviewer (Nirty) can clone the repo on a fresh machine, follow the README, and reproduce the demo within 1 hour
- [ ] Round-trip latency documented and <150 ms in measured conditions
- [ ] No known crashes in 30 minutes of continuous use

---

**Open questions to surface to the reviewer early (don't decide alone):**

- Tablet vs. wall-mounted HMI panel asset — which makes the demo more legible? (Default: wall-mounted HMI panel)
- Whether to ship v2 (IK hand) for v1.0 or push to v1.1 (Default: ship v2)
- Whether to record the demo with a robot arm visible in the scene, even though it's not functional in v1 (Default: no — keep the scope tight, add robot in part-2 post)

Surface these in the first weekly sync.
