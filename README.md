# MacWindowCleaner

This simple script automatically closes macOS applications that have not been
used for a while. It checks the currently focused app and tracks when each
visible app was last active. If an app has not been active for more than the
configured timeout, it will be politely asked to quit.

## Usage

1. Make sure Python 3 is installed on your Mac.
2. Run the script in the background:

   ```bash
   python3 main.py
   ```

   By default, apps idle for more than 60 minutes are closed. Adjust
   `IDLE_THRESHOLD_MINUTES` and `CHECK_INTERVAL_SECONDS` in `main.py` if needed.

3. Add apps you never want to close automatically to the `EXEMPT_APPS` set.

The script relies on `osascript` to talk to macOS, so it only works on macOS.
