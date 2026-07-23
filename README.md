# carPi
Robotic car controlled by Raspberry Pi (Mecanum 4WD + Flask HTTP API).

## Features
- Drive / turn / stop over HTTP (port 8090)
- Motion path recording and playback
- USB speaker text-to-speech (male / female), with a threatened / scared delivery for Android control

## Docs
- `doc/install.txt` — OS packages, systemd service, TTS setup
- `doc/wiring.txt` — GPIO / motor driver wiring
- `doc/bom.txt` — parts list
- `doc/speech.txt` — USB speaker TTS API and Piper voice setup

## Quick API (TTS)
Plug a USB audio speaker directly into the Pi, then:

```
GET http://<pi-ip>:8090/speak/female?text=Please%20dont%20hurt%20me
GET http://<pi-ip>:8090/speak/male/Oh%20god%20please%20no
GET http://<pi-ip>:8090/speak/stop
GET http://<pi-ip>:8090/speak/status
```

See `doc/speech.txt` for full setup (Piper binary + voice models are downloaded separately; large files are not in git).
