#!/bin/bash
cd /home/armando/Imágenes/wallpapers

# Procesar todas las imágenes
find . -maxdepth 1 \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.gif" -o -iname "*.webp" \) | sort | while read img; do
    filename=$(basename "$img")
    magick "$img" -resize 300x300 -background white -gravity center -extent 300x300 "thumbnails/thumb_$filename" 2>/dev/null
done

echo "Miniaturas generadas"
