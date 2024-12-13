#!/bin/bash

ICON_PATH="$PWD/assets/icon.png"
DESKTOP_FILE="$HOME/.local/share/applications/zerotoolkit.desktop"
EXEC_PATH="$PWD/zerotoolkit.py"
SYMLINK_PATH="/usr/local/bin/zerotoolkit"

cat << EOF > "$DESKTOP_FILE"
[Desktop Entry]
Version=1.0
Name=ZeroToolkit
Comment=Penetration Testing Tool
Exec=/usr/bin/python $EXEC_PATH
Icon=$ICON_PATH
Terminal=False
Type=Application
Categories=Utility;
EOF

chmod +x "$DESKTOP_FILE"

sudo ln -sf "$EXEC_PATH" "$SYMLINK_PATH"

update-desktop-database ~/.local/share/applications