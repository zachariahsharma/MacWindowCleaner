#!/usr/bin/env python3
"""Automatically close unused macOS apps after a period of inactivity."""

import subprocess
import time
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, Optional

# Duration after which an inactive app should be closed (in minutes)
IDLE_THRESHOLD_MINUTES = 60
# How often to check the active application (in seconds)
CHECK_INTERVAL_SECONDS = 30
# Apps that should never be automatically closed
EXEMPT_APPS = {
    "Finder",
    "SystemUIServer",
    "WindowServer",
}


def run_osascript(script: str) -> str:
    """Run the given AppleScript and return its stdout."""
    return subprocess.check_output(["osascript", "-e", script], text=True).strip()


def get_frontmost_app() -> Optional[str]:
    """Return the name of the currently focused application."""
    script = 'tell application "System Events" to get name of first application process whose frontmost is true'
    try:
        return run_osascript(script)
    except subprocess.CalledProcessError:
        return None


def get_visible_apps() -> Dict[str, None]:
    """Return a set-like dict of visible running applications."""
    script = 'tell application "System Events" to get name of (every process whose visible is true)'
    try:
        output = run_osascript(script)
        names = [name.strip() for name in output.split(",") if name.strip()]
        return {name: None for name in names}
    except subprocess.CalledProcessError:
        return {}


def quit_app(app_name: str) -> None:
    """Ask an application to quit politely."""
    script = f'tell application "{app_name}" to quit'
    # Use call so failure doesn't raise
    subprocess.call(["osascript", "-e", script])


def main() -> None:
    last_active: Dict[str, datetime] = defaultdict(datetime.now)
    while True:
        active = get_frontmost_app()
        if active:
            last_active[active] = datetime.now()

        visible_apps = get_visible_apps()
        now = datetime.now()
        idle_threshold = timedelta(minutes=IDLE_THRESHOLD_MINUTES)

        for app in list(last_active.keys()):
            if app in EXEMPT_APPS:
                continue
            if app not in visible_apps:
                # Remove apps that have exited
                last_active.pop(app, None)
                continue
            if now - last_active[app] > idle_threshold:
                print(f"[INFO] Quitting {app} due to inactivity")
                quit_app(app)
                last_active.pop(app, None)

        time.sleep(CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
