#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path

def generate_thumbnails():
    """Generar miniaturas de todas las imágenes."""
    images = sorted([f for f in os.listdir('.') 
                    if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))
                    and os.path.isfile(f)])
    
    thumbnails_dir = Path('thumbnails')
    thumbnails_dir.mkdir(exist_ok=True)
    
    print(f"Procesando {len(images)} imágenes...")
    for i, img in enumerate(images, 1):
        try:
            subprocess.run([
                'magick', img,
                '-resize', '300x300',
                '-background', 'white',
                '-gravity', 'center',
                '-extent', '300x300',
                f'thumbnails/thumb_{img}'
            ], check=True, capture_output=True, timeout=30)
            
            if i % 30 == 0:
                print(f"  {i}/{len(images)}")
        except Exception as e:
            print(f"  Error procesando {img}: {e}")
    
    print(f"✓ {len(images)} miniaturas generadas")
    return images

def create_readme(images):
    """Crear README con galería de miniaturas."""
    readme = """# Wallpapers Collection

Una colección de fondos de pantalla de alta calidad.

## Galería de Fondos

"""
    
    # Agregar imágenes en grid de 3 columnas
    for i, image in enumerate(images):
        if i % 3 == 0:
            readme += "\n"
        
        # Crear enlace con miniatura que apunta a la imagen full-size
        readme += f"""| [![{image}](thumbnails/thumb_{image})]({image}) """
    
    readme += f"""

---

## Información

- **Total de fondos**: {len(images)}
- **Miniaturas**: Generadas automáticamente en 300x300px
- **Última actualización**: {__import__('datetime').datetime.now().strftime('%d de %B de %Y')}

## Cómo usar

1. Elige un fondo que te guste de la galería de arriba
2. Descarga la imagen en tamaño completo haciendo clic en la miniatura
3. Establécela como fondo de pantalla en tu sistema

## Categorías

- Naturaleza
- Tecnología
- Abstracto
- Arte
"""
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme)
    
    print(f"✓ README.md creado")

if __name__ == '__main__':
    images = generate_thumbnails()
    create_readme(images)
    print("\n✓ Proceso completado exitosamente")
