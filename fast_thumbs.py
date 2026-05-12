#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

def generate_thumbnail(image_path):
    """Genera una miniatura para una imagen."""
    try:
        filename = os.path.basename(image_path)
        thumbnail_path = f"thumbnails/thumb_{filename}"
        
        # Saltar si ya existe
        if os.path.exists(thumbnail_path):
            return f"S"
        
        subprocess.run([
            'magick', image_path,
            '-resize', '300x300',
            '-background', 'white',
            '-gravity', 'center',
            '-extent', '300x300',
            thumbnail_path
        ], capture_output=True, timeout=30)
        return "."
    except Exception as e:
        return "E"

if __name__ == '__main__':
    os.chdir('/home/armando/Imágenes/wallpapers')
    
    # Obtener lista de imágenes
    images = [f for f in os.listdir('.') 
              if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))
              and os.path.isfile(f)]
    
    images.sort()
    
    print(f"Procesando {len(images)} imágenes...")
    
    # Procesar con 4 threads en paralelo
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(generate_thumbnail, images))
    
    dots = results.count(".")
    skipped = results.count("S")
    errors = results.count("E")
    
    print(f"\n✓ Generadas: {dots}, Saltadas (ya existen): {skipped}, Errores: {errors}")
    print(f"✓ Total miniaturas: {len(os.listdir('thumbnails'))}")
