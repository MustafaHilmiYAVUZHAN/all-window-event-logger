## All Window Event Logger

### Overview

This Python application monitors open windows and logs events for windows that are closed or become inactive within a short duration. Events are logged to `log.txt`.

### Libraries Used

- `time`: Standard Python library for time operations.
- `win32gui`: Library for Windows GUI operations.
- `win32process`: Library for managing Windows processes.
- `psutil`: Library for retrieving process information.
- `datetime`: Standard Python library for date and time operations.

### Functions

- `get_process_filename(hwnd)`: Returns the process filename for a given window.
- `log_window_events()`: Main function that monitors open windows and logs events based on conditions.

### Features

- Detects newly opened windows and logs them to the log file.
- Identifies windows closed within a short duration and logs them with timestamp and duration.
- Currently identifies actively open windows; the section for prompting message boxes for short-lived active windows is commented out.

### Usage

- Install necessary libraries and dependencies.
- Run the script using `python script.py`.

### Considerations

- Designed for Windows operating systems; compatibility with other platforms not guaranteed.
- Exercise caution when modifying code for user interactions or additional features.
