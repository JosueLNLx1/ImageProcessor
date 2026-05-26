from pathlib import Path
from rembg import remove
from PIL import Image, ImageDraw

class ImageProcessor:
    def __init__(self, input_folder: str, output_folder: str):
        self.input_folder = Path(input_folder)
        self.output_folder = Path(output_folder)
        self.temp_folder = Path("temp")
        
        # Crear carpetas si no existed
        self.output_folder.mkdir(parents=True, exist_ok=True)
        self.temp_folder.mkdir(parents=True, exist_ok=True)
        
        
        self.images_processed_count = 0
        
        # Se verifica si se cargaron imagenes
        self.is_processed = False
        
        # Dimensiones del Lienzo
        self.canvas_size = (1000, 1000)
        self.canvas = None
        
        if self.output_folder.exists():
            self.CleanOutput()
        
    def RemoveBG(self):
        Path(self.temp_folder / 'images').mkdir(parents=True, exist_ok=True)
        # Si no se han procesado imágenes, se procesan desde la carpeta de entrada
        datos = self.temp_folder if self.is_processed else self.input_folder
        # Iteramos directamente sobre los archivos válidos
        for image_path in datos.iterdir():
            if image_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp']:
                try:
                    img_original = Image.open(image_path)
                    img_sin_fondo = remove(img_original)
                    
                    # Guardar correctamente en temp (siempre como PNG para soportar RGBA)
                    ruta_temp = self.temp_folder / 'images' / (image_path.stem + '.png')
                    img_sin_fondo.thumbnail((1000, 1000), Image.Resampling.LANCZOS)  # Redimensionar manteniendo proporción
                    img_sin_fondo.save(ruta_temp, "PNG")
                    
                    self.images_processed_count += 1
                    print(f"✓ Procesado: {image_path.name}")
                    #existiran archivos en temp, pero no se moveran a output, solo se guardaran ahi, para evitar errores de permisos
                    self.is_processed = True
                    
                except Exception as e:
                    print(f"✗ Error con {image_path.name}: {e}")
                    
        print(f"✓ Se procesaron {self.images_processed_count} imágenes sin fondo.")
    
    def CreateCanvas(self ):
        try:
            self.canvas = Image.new("RGBA", self.canvas_size, "WHITE")
            Path(self.temp_folder / 'canvas').mkdir(parents=True, exist_ok=True) 
            self.canvas.save(self.temp_folder / "canvas" / "canvas.png")
            print("✓ Lienzo creado correctamente.")
                
        except Exception as e:
            print(f"✗ Error al crear el lienzo: {e}")
            
            
    def PasteOnCanvas(self):
        if not self.is_processed:
            print("No hay imágenes procesadas para pegar en el lienzo.")
            return
        
        if self.canvas is None:
            self.CreateCanvas()
        
        for image_path in (self.temp_folder / 'images').iterdir():
            canvas = self.canvas.copy()  # Crear una copia del lienzo para cada imagen
            if image_path.suffix.lower() == '.png':
                try:
                    img_objeto = Image.open(image_path)
                    x = (self.canvas_size[0] - img_objeto.width) // 2
                    y = (self.canvas_size[1] - img_objeto.height) // 2
                    
                    canvas.paste(img_objeto, (x, y), img_objeto)
                    
                    # Guardar el resultado final en la carpeta de salida
                    output_path = self.output_folder / (image_path.stem + "_final.webp")
                    canvas.convert("RGB").save(output_path, "WEBP", quality=95)
                    
                    print(f"✓ Imagen pegada y guardada: {output_path.name}")
                    
                except Exception as e:
                    print(f"✗ Error al pegar {image_path.name}: {e}")
    
    def SourcePhotos(self):
        return print("Función para agregar precio a la imagen (en desarrollo)")
    
    def CleanTemp(self):
        try:
            for item in self.temp_folder.iterdir():
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    for subitem in item.iterdir():
                        subitem.unlink()
                    item.rmdir()
            print("✓ Carpeta temporal limpiada.")
        except Exception as e:
            print(f"✗ Error al limpiar la carpeta temporal: {e}")
    
    def CleanOutput(self):
        try:
            for item in self.output_folder.iterdir():
                if item.is_file():
                    item.unlink()
            print("✓ Carpeta de salida limpiada.")
        except Exception as e:
            print(f"✗ Error al limpiar la carpeta de salida: {e}")