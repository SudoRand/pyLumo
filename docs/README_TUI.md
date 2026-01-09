# pyLumo TUI

A beautiful terminal user interface for interacting with the Lumo Proton API. Built with Python, Textual, and Rich libraries featuring a purple and yellow color scheme with animated loading indicators and ASCII cat companions.

![Version](https://img.shields.io/badge/version-0.0.1-purple)
![Python](https://img.shields.io/badge/python-3.12+-blue)

## Table of Contents

- [Features](#features)
  - [Security](#security)
  - [Chat Interface](#chat-interface)
  - [File Management](#file-management)
  - [Session & Tools](#session--tools)
  - [User Interface](#user-interface)
- [Requirements](#requirements)
- [Installation](#installation)
  - [Quick Install](#quick-install)
- [Usage](#usage)
  - [Starting the TUI](#starting-the-tui)
  - [Keyboard Shortcuts](#keyboard-shortcuts)
  - [Sending Messages](#sending-messages)
  - [Attaching Files](#attaching-files)
  - [Saving Chat History](#saving-chat-history)
  - [Saving Debug Output](#saving-debug-output)
- [Troubleshooting](#troubleshooting)
- [Architecture](#architecture)
  - [Components](#components)
  - [Client Integration](#client-integration)
- [Contributing](#contributing)
- [License](#license)
- [Links](#links)
- [Acknowledgments](#acknowledgments)

## Features

### Security
- **Hybrid Encryption**: AES-256-GCM + PGP encryption
- **Secure Communication**: End-to-end encrypted messages with Lumo API
- **PGPy Integration**: Compatible with OpenPGP.js v6.2.2 format

### Chat Interface
- **Real-time Streaming**: Live response streaming from Lumo
- **Markdown Support**: Automatic markdown rendering for formatted responses
- **Message History**: Full conversation tracking within session
- **ASCII Cat Companions**: Random cat faces with each Lumo response 🙀

### File Management
- **File Attachments**: Upload multiple files with preview
- **Directory Navigation**: Browse and navigate directories in file browser
- **Image Preview**: View uploaded images directly in TUI
- **Easy Removal**: Click the ✕ to remove files

### Session & Tools
- **Save Chats**: Export conversation history to text files (Ctrl+S)
- **Auto-timestamped Filenames**: Suggested filenames with timestamps
- **Clear Chat**: Start fresh conversations (Ctrl+X)
- **Tool Selection**: Choose which tools to enable (Tools button)
- **Proton Authentication**: Login for higher rate limits (Ctrl+L)
- **Session Persistence**: Saved sessions across app restarts

### User Interface
- **Clean Design**: Purple and yellow color scheme
- **Responsive Layout**: Adapts to terminal size
- **Loading Animations**: Walking paw prints while waiting
- **Status Bar**: Real-time status updates
- **Debug Panel**: Optional stderr output viewer (F2)
- **Clickable Footer**: Mouse-friendly keyboard shortcuts

## Requirements

- Python 3.12 or higher
- Terminal with Unicode support
- Internet connection for Lumo API access
- **uv** package manager (recommended)

## Installation

### Quick Install

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and install
git clone https://github.com/Mindgard/pylumo.git
cd pylumo
make install-tui
```

**Alternative:**
```bash
python3 scripts/install.py --tui
```

See main [README.md](README.md) for detailed installation options.

## Usage

### Starting the TUI

```bash
# Using uv (recommended)
uv run pylumo-tui

# Or run from the project venv created by `make install-tui`
./.venv/bin/pylumo-tui

# Or activate the venv and run normally
source .venv/bin/activate
pylumo-tui
```

The application launches with a welcome message and is ready to chat.

### Keyboard Shortcuts

| Shortcut | Action | Description |
|----------|--------|-------------|
| `Ctrl+Q` | Quit | Exit the application (with confirmation) |
| `Ctrl+S` | Save Chat | Save conversation history to file |
| `Ctrl+X` | Clear Chat | Clear conversation history |
| `Ctrl+U` | Upload | Browse and attach files |
| `Ctrl+L` | Login | Authenticate with Proton account |
| `Ctrl+K` | Logout | Sign out from Proton |
| `F1` | About | Show application information |
| `F2` | Debug | Toggle debug panel (request/response logs) |
| `F10` | Save Debug | Save debug output to file |
| `Ctrl+\` | Command Palette | Open command palette |
| `Enter` | Send | Send your message |
| `ESC` | Cancel | Close modals/dialogs |

### Sending Messages

1. Type your message in the input field at the bottom
2. Press `Enter` or click the **Send** button
3. Watch the animated loading indicator while Lumo thinks
4. See the response appear with a random ASCII cat face

### Attaching Files

**Method 1: Keyboard**
1. Press `Ctrl+U`
2. Navigate with arrow keys or type directory path
3. Press `Enter` on path input to navigate to directory
4. Select file and press `Enter` or click **Select**

**Method 2: Mouse**
1. Click **Upload** button
2. Type directory path in input field and click **Go**
3. Click on a file in the tree
4. Click **Select** button

**Features:**
- Directory navigation with path input
- Image preview for supported formats
- Multiple file attachments
- Click ✕ to remove files

### Saving Chat History

**Method 1: Keyboard**
1. Press `Ctrl+S`
2. Edit the suggested filename if desired
3. Press `Enter`

**Method 2: Mouse**
1. Click `^S Save` in the footer
2. Edit the filename
3. Click **Save** button

**Output Format:**
```
================================================================================
pyLumo Chat Session
Saved: 2025-10-14 14:53:17
================================================================================

Lumo 14:53:10
  /\_/\
 ( ⊙.⊙ )
  > ▼ <

Welcome to the pyLumo TUI! I'm ready to help you.
--------------------------------------------------------------------------------

You 14:53:12
hi
--------------------------------------------------------------------------------
```

### Saving Debug Output

The debug panel (F2) captures comprehensive debug information including:
- HTTP requests with full payload structure
- API responses with streaming data
- Request details (encrypted keys, turn count, targets)
- Encryption/decryption operations
- Authentication flow
- Error messages

**Method 1: Keyboard**
1. Press `F10`
2. Edit the suggested filename if desired (default: `lumo_debug_YYYYMMDD_HHMMSS.log`)
3. Press `Enter`

**Method 2: Mouse**
1. Click `F10 Save Debug` in the footer
2. Edit the filename
3. Click **Save** button

**Output Format:**
```
================================================================================
pyLumo Debug Output
Saved: 2025-10-14 14:53:17
================================================================================

[Debug messages, API calls, errors, and stderr output...]
```

**Use Cases:**
- Debugging connection issues
- Analyzing API request/response cycles
- Capturing error messages for support
- Monitoring encryption/decryption process

## Troubleshooting

### TUI doesn't start
- Verify Python version: `python --version` (must be 3.12+)
- Install dependencies: `make install-tui` (recommended) or `python3 scripts/install.py --tui`
- Ensure all required files are present

### Characters appear broken
- Use a terminal with Unicode support (e.g., iTerm2, Windows Terminal, GNOME Terminal)
- Ensure your terminal font supports emojis

### Connection errors
- Check internet connection
- Verify Lumo API is accessible
- Check debug panel (F2) for detailed error messages

### File upload not working
- Ensure you have read permissions for the file
- Check file path is correct
- Files must exist and be readable

## Architecture

### Components

- **ChatContainer**: Scrollable message display with markdown rendering
- **StatusBar**: Real-time status and authentication state
- **CustomFooter**: Clickable keyboard shortcuts
- **DebugPanel**: Comprehensive debug output viewer
- **LoadingIndicator**: Animated paw prints
- **Modals**:
  - `FileBrowserModal`: File selection with directory navigation
  - `ImageViewModal`: Image preview for uploaded files
  - `FilePreviewModal`: File content preview
  - `ToolsModal`: Tool selection interface
  - `SaveChatModal`: Save chat dialog
  - `SaveDebugModal`: Save debug output dialog
  - `LoginModal`: Proton authentication
  - `TwoFactorModal`: 2FA code entry
  - `QuitConfirmModal`: Quit confirmation
  - `ClearChatConfirmModal`: Clear chat confirmation
  - `LogoutConfirmModal`: Logout confirmation
  - `AboutModal`: Application information
  - `SplashScreenModal`: Startup splash screen

### Client Integration

The TUI uses `pyLumoDebug` from `_pylumo_debug.py`:
- Hybrid encryption (AES-256-GCM + PGP)
- Real-time streaming responses
- Proton authentication with session persistence
- Comprehensive debug logging
- File upload with base64 encoding

## Contributing

See [docs/TESTING.md](docs/TESTING.md) for the current test and coverage workflow.

Contributions are welcome! Areas for improvement:
- Additional export formats (JSON, Markdown, HTML)
- Search functionality in chat history
- Message editing/deletion
- Theme customization
- Plugin system for custom tools

## License

GNU General Public License v3.0 or later (GPL-3.0-or-later)

Copyright (C) 2025 Mindgard

See [LICENSE](LICENSE) file for full license text.

## Links

- **GitHub**: https://github.com/Mindgard/pylumo
- **Lumo Web App**: https://lumo.proton.me
- **Mindgard**: https://mindgard.ai

## Acknowledgments

Built with:
- [Textual](https://textual.textualize.io/) - Modern TUI framework
- [Rich](https://rich.readthedocs.io/) - Beautiful terminal formatting
- [PGPy](https://pgpy.readthedocs.io/) - PGP encryption
- [Cryptography](https://cryptography.io/) - AES encryption

---

**Brought to you by the cool cats at Mindgard** 🐱✨
