#!/usr/bin/env bash

SOURCE="/Users/joe/Library/Caches/com.apple.findmy.fmipcore/Items.data"
DEST_DIR="/Users/joe/Desktop/logs"

while true; do
    timestamp=$(date +"%Y-%m-%d_%H-%M-%S")
    cp "$SOURCE" "$DEST_DIR/file_$timestamp.txt"
    Sleep 900
done 