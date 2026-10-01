# My Habit Tracker — Android

A simple Python/Kivy habit tracker.

## Features
- Add unlimited habits
- Mark today's habit complete
- Daily percentage
- Streak counter
- Delete habits
- Data saved locally in `habits.json`
- Works offline

## Build APK

Use Ubuntu/WSL/Linux:

```bash
sudo apt update
sudo apt install -y python3-pip git zip unzip openjdk-17-jdk
pip install --upgrade buildozer cython
buildozer android debug
```

The APK will be created in the `bin/` folder.

For a release APK:

```bash
buildozer android release
```

This project is ready to open in Android Studio/VS Code or build with Buildozer.
