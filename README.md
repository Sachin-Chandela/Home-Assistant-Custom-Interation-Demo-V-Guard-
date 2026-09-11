# Home-Assistant-Custom-Interation-Demo-V-Guard-
Home Assistant custom integration for VGUARD smart devices (fans, lights) — bridges them to Apple Home, Google Home, and more without needing native Matter/HomeKit firmware.



## Installation
 
### Option A: HACS (recommended, once published)
1. Go to **HACS → Integrations → ⋮ → Custom repositories**.
2. Add this repository URL and select category **Integration**.
3. Search for **VGUARD Devices** and install.
4. Restart Home Assistant.
### Option B: Manual
1. Copy the `vguard_devices` folder into your Home Assistant `custom_components` directory:
```
   config/custom_components/vguard_devices/
```
2. Restart Home Assistant.
## Configuration
 
All configuration is done through the UI — no YAML needed.
 
1. Go to **Settings → Devices & Services → Add Integration**.
2. Search for **VGUARD Devices**.
3. Enter your VGUARD account **username** and **password**.
4. Home Assistant will validate the login and automatically create entities for every device on your account.
To expose these devices to Apple Home, also set up the built-in **HomeKit Bridge** integration and select your VGUARD entities (or the whole `vguard_devices` domain) to expose.
 
## Supported Devices
 
| Device type | Product key | Entity | Capabilities |
|---|---|---|---|
| Smart Fan | `smartfan` | `fan.*` | On/Off, Speed (1–4) |
| Smart Light | `light` | `light.*` | On/Off |
 
More device types can be added by extending `coordinator.py` and adding a matching platform file (see `fan.py` / `light.py` as a template).


## Known Issues - TODO
 
- [ ] `const.py` — `DEFAULT_HOST`, `DEFAULT_PORT`, and `TOKEN` are placeholders and need real values wired in (`TOKEN` in particular should come from the login/redirect flow, not be hardcoded).
- [ ] `devices_api.py` — the device list URL is a placeholder and needs to point to the real VGUARD API endpoint.
- [ ] All fans currently share one control endpoint (`/api/fan/control`) rather than being addressed individually by device UUID — same for lights. Per-device control needs backend support for `uuid`-scoped requests.
- [ ] No re-authentication / token refresh handling yet if the session token expires.
- [ ] `manifest.json` has no `codeowners`, `documentation`, or `issue_tracker` fields — add these before publishing to HACS.
- [ ] No tests yet.


