# Custom Web Browser

A simple web browser built with PyQt5 that includes basic navigation features and bookmark management.

## Features

- Basic navigation (back, forward, reload, home);
- URL bar with address input;
- Bookmark management:
  - Add/remove bookmarks;
  - Bookmark toolbar with quick access;
  - Bookmark persistence using JSON storage;
- Modern UI with custom styling;
- Icon support for navigation buttons.

## Requirements

- Python 3.x
- PyQt5
- PyQtWebEngine

## Installation

1. Install the required dependencies:
```sh
pip install PyQt5 PyQtWebEngine
```

2. Clone this repository:
```sh
git clone <repository-url>
cd project2
```

3. Run the browser:
```sh
python main.py
```

## Usage:
- Type a URL in the address bar and press Enter to navigate;
- Click the bookmark icon to save the current page;
- Right-click on bookmarks to remove them;
- Use the navigation buttons for back/forward/reload/home functions;
- The browser automatically saves bookmarks between sessions.

## License
This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details. ```