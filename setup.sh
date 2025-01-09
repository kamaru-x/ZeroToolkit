#!/bin/bash

SCRIPT_PATH="$PWD/zeroxploit.py"
DESKTOP_FILE="$HOME/.local/share/applications/zeroxploit.desktop"
SYMLINK_PATH="/usr/local/bin/zeroxploit"
ICON_PATH="$PWD/assets/icon.png"

if [ ! -f "$ICON_PATH" ]; then
    mkdir -p "$PWD/assets"
    echo "Creating a placeholder icon at $ICON_PATH"
    convert -size 128x128 xc:blue -fill white -gravity center -pointsize 24 -draw "text 0,0 'ZTK'" "$ICON_PATH" 2>/dev/null || echo "Icon creation failed. Install ImageMagick or use your own icon."
fi

cat << EOF > "$DESKTOP_FILE"
[Desktop Entry]
Version=1.0
Name=Zeroxploit
Comment=Penetration Testing Toolkit
Exec=gnome-terminal -- bash -c "/usr/bin/python3 $SCRIPT_PATH; echo 'Press Enter to exit...'; read"
Icon=$ICON_PATH
Terminal=true
Type=Application
Categories=Utility;
EOF

chmod +x "$DESKTOP_FILE"

sudo ln -sf "$SCRIPT_PATH" "$SYMLINK_PATH"

update-desktop-database ~/.local/share/applications