# ROOTer Home Assistant Integration

A custom component for Home Assistant to monitor ROOTer / GoldenOrb modems by scraping the splash page.

## Features
- Monitors Signal Strength, CSQ, RSSI, RSRP, RSRQ, SINR.
- Monitors Network details (Band, Mode, Cell ID, Provider).
- Monitors Device details (Temperature, Model, IP).
- Updates every 30 seconds (default).

## Installation
1. Copy the `custom_components/rooter` directory to your Home Assistant `custom_components` directory.
2. Restart Home Assistant.
3. Go to **Settings > Devices & Services**.
4. Click **Add Integration** and search for **ROOTer**.
5. Enter your router's IP address (default `192.168.10.1`).

## Configuration
- **Host**: The IP address of your ROOTer device.
- **Verify SSL**: Uncheck if using self-signed certificates (default).

## Troubleshooting
If data is not updating, ensure `https://<router_ip>/splash.html` is accessible from your Home Assistant instance.
