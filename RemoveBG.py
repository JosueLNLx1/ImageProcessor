import os
from rembg import remove
from PIL import Image

# =========================================================
# CONFIGURA TUS RUTAS AQUÍ
# =========================================================
CARPETA_ENTRADA = "./imagenes_origen"  # Carpeta donde pones tus fotos
CARPETA_SALIDA = "./resultados_webp"   # Carpeta donde se guardarán
# =========================================================

def procesar_imagen(ruta_en, ruta_sal):
    img_original = Image.open(ruta_en)
    img_sin_fondo = remove(img_original)
    
    caja_objeto = img_sin_fondo.getbbox()
    if not caja_objeto:
        return 
    img_objeto = img_sin_fondo.crop(caja_objeto)
    
    # Redimensionar a 1000x1000 manteniendo proporción
    img_objeto.thumbnail((900, 900), Image.Resampling.LANCZOS)
    
    lienzo_blanco = Image.new("RGBA", (1000, 1000), "WHITE")
    x = (1000 - img_objeto.width) // 2
    y = (1000 - img_objeto.height) // 2
    
    lienzo_blanco.paste(img_objeto, (x, y), img_objeto)
    resultado_final = lienzo_blanco.convert("RGB")
    
    # Guarda en WebP con calidad original
    resultado_final.save(ruta_sal, "WEBP", quality=95)
    print(f"✓ Guardado en: {ruta_sal}")

# Crear las carpetas automáticamente si no existen
os.makedirs(CARPETA_ENTRADA, exist_ok=True)
os.makedirs(CARPETA_SALIDA, exist_ok=True)

# Buscar y procesar imágenes
formatos = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp')
imagenes = [f for f in os.listdir(CARPETA_ENTRADA) if f.lower().endswith(formatos)]

if not imagenes:
    print(f"La carpeta '{CARPETA_ENTRADA}' está vacía. Pon tus imágenes ahí dentro.")
else:
    for archivo in imagenes:
        ruta_in = os.path.join(CARPETA_ENTRADA, archivo)
        nombre_base = os.path.splitext(archivo)[0]
        ruta_out = os.path.join(CARPETA_SALIDA, f"{nombre_base}_1000x1000.webp")
        
        try:
            procesar_imagen(ruta_in, ruta_out)
        except Exception as e:
            print(f"✗ Error con {archivo}: {e}")
