# KvDeveloper Client
[![Android Build](https://github.com/Novfensec/KvDeveloper-Client/actions/workflows/buildozer_android_action.yml/badge.svg)](https://github.com/Novfensec/KvDeveloper-Client/actions/workflows/buildozer_android_action.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/Novfensec/KvDeveloper-Client/blob/main/LICENSE)
[![Made with Python](https://img.shields.io/badge/Made%20with-Python-blue.svg)](https://www.python.org/)
[![KvDeveloper Project](https://img.shields.io/badge/Part%20of-KvDeveloper%20Project-blueviolet.svg)](https://github.com/Novfensec/KvDeveloper)

Instantly load your app on mobile via QR code or Server URL. Experience blazing-fast Kivy app previews on Android with KvDeveloper Client, It’s the Expo Go for Python devs—hot reload without the hassle.

<!-- GitAds-Verify: QCB8LYMU8FNAS8LP4OB1TWLG2R9OR182 -->

## GitAds Sponsored
[![Sponsored by GitAds](https://gitads.dev/v1/ad-serve?source=novfensec/kvdeveloper-client@github)](https://gitads.dev/v1/ad-track?source=novfensec/kvdeveloper-client@github)

## Overview

![KvDeveloper Client](https://raw.githubusercontent.com/Novfensec/KvDeveloper-Client/master/assets/kvdeveloperclient.jpg)

**KvDeveloper Client** is your mobile companion for hot-reloading **Kivy apps**—designed to give developers a lightning-fast preview and live-edit experience, directly on Mobile devices.

Inspired by the **Expo Go** workflow for React Native, this tool lets you:

- Start a dev server from any Kivy app directory.
- Instantly **load your app on mobile** via QR code or Server URL.
- Get **real-time updates** with automatic file watching.
- Skip USB cables, installs, and tedious builds.

Whether you're tweaking UI layouts or debugging logic, this workflow keeps you moving fast and focused.

## Features

- Zero-install app preview on mobile.
- Server-to-client sync via HTTP & QR code.
- Hot-reload on file changes (KV, Python).
- Clean UI with simple connection steps.
- Safe and secure local access with opt-in controls.

## Installation & Usage

### Server (Desktop)
Run below command in the root directory of your app.
```bash
pip install https://github.com/Novfensec/KvDeveloper/archive/master.zip
kvdeveloper serve
```

### `[Important]`
Add below lines at the top of your entrypoint file `normally main.py`:

```python
import os, sys
from kivy.resources import resource_add_path

sys.path.insert(0, os.path.dirname(__file__))
resource_add_path(os.path.dirname(__file__))
```

### Client (Mobile)
Download and extract debuggable package.zip from the [latest workflow run](https://github.com/Novfensec/KvDeveloper-Client/actions/workflows/buildozer_android_action.yml) **OR** old packages from `binaries` folder, and then install the application.

1. Launch KvDeveloper Client on your Android device.
2. Scan the QR code or enter the server URL manually.
3. Your app loads instantly—with live updates as you edit files.

[Live Demo](https://youtu.be/-VTCTNmHB94)


## Part of KvDeveloper Ecosystem
KvDeveloper Client is a subproject under the [KvDeveloper](https://github.com/Novfensec/KvDeveloper) initiative. The ecosystem aims to streamline Python-powered mobile workflows with modern tooling.

🤝 Contributing

We welcome PRs, suggestions, and bug reports!

```bash
git clone https://github.com/Novfensec/KvDeveloper-Client.git
```
Feel free to open issues or jump into our [Discord](https://discord.gg/U9bfkD6A4c) community!

### Financial Contribution
Please Contribute financially to this project. Make small one time contributions!! Thank You 😊!!

Github Sponsors: https://github.com/sponsors/Novfensec

PayPal: https://paypal.me/KARTAVYASHUKLA 

Opencollective: https://opencollective.com/KvDeveloper

## License
This project is licensed under the MIT License.

## Credits
Built with ❤️ by [Kartavya Shukla](https://github.com/Novfensec).
Inspired by the spirit of fast and efficient development.
