#!/bin/bash

if which nautilus &>/dev/null; then
    FILEMANAGER="nautilus"
elif which caja &>/dev/null; then
    FILEMANAGER="caja"
else
    echo "can't found nautilus or caja..."
    exit 1
fi

mkdir -p "$HOME/.local/share/$FILEMANAGER-python/extensions"

# Download and install the extension
echo "Downloading newest version..."
wget -q -O "$HOME/.local/share/$FILEMANAGER-python/extensions/nautilus_exiftool.py" https://raw.githubusercontent.com/remigermain/nautilus-exiftool/refs/heads/main/nautilus_exiftool/nautilus_exiftool.py

# Restart nautilus
echo "Restarting $FILEMANAGER..."
$FILEMANAGER -q 2>/dev/null

echo "Installation Complete"
