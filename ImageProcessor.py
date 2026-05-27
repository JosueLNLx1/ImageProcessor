from pathlib import Path
from rembg import remove
from PIL import Image, ImageDraw, ImageFont, ImageText
from requests import get
from dotenv import load_dotenv
import os
from io import BytesIO

load_dotenv()

class ImageProcessor:
    def __init__(self, input_folder: str, output_folder: str):
        self.input_folder = Path(input_folder)
        self.output_folder = Path(output_folder)
        self.temp_folder = Path("temp")
        self.URL_PAGE = os.getenv("URL_PAGE")
        print(f"URL_PAGE cargada: {self.URL_PAGE}")
        
        # Crear carpetas si no existed
        self.output_folder.mkdir(parents=True, exist_ok=True)
        self.temp_folder.mkdir(parents=True, exist_ok=True)
        
        
        self.images_processed_count = 0
        
        # Se verifica si se cargaron imagenes
        self.is_processed = False
        
        # Dimensiones del Lienzo
        self.canvas_size = (1000, 1000)
        self.canvas = None
        
        self.logo_path = "images/HerGozLogo.png"  # Ruta del logo a agregar (si se desea)
        
        if self.output_folder.exists():
            self.__CleanOutput()
        if self.temp_folder.exists():
            self.__CleanTemp()
        
        
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
    
    def ImagesWithPrice(self):
        try:
            photos = self.__SourcePhotosURL()
            print(f"✓ Fotos obtenidas desde la URL: {len(photos)} fotos encontradas.")
            print("Fotos obtenidas:")
            for photo in photos:
                print(f"✓ Foto obtenida: {photo['image_url']}")
                response = get(photo['image_url'])
                imagen = Image.open(BytesIO(response.content))
                imagen.thumbnail((1000, 1000), Image.Resampling.LANCZOS)  # Redimensionar manteniendo proporción
                new_image = self.addPriceToImage(imagen, photo['price'], photo['sku'])
                new_image = self.addLogoToImage(new_image)
                new_image.save(self.output_folder / f"{photo['sku']}.webp", "WEBP", quality=95)
                
                
        except Exception as e:
            print(f"✗ Error al obtener las fotos: {e}")
    
    def __SourcePhotosURL(self):
        return get(self.URL_PAGE).json()
    
    def __CleanTemp(self):
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
    
    def __CleanOutput(self):
        try:
            for item in self.output_folder.iterdir():
                if item.is_file():
                    item.unlink()
            print("✓ Carpeta de salida limpiada.")
        except Exception as e:
            print(f"✗ Error al limpiar la carpeta de salida: {e}")
    
    def addPriceToImage(self, image, price, sku):
        try:
            font = ImageFont.truetype("Inter.ttf", 80)  # Texto más grande
            image = image.convert("RGBA")
            overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)

            padding = 20
            radius = 15
            margin = 50  # separación del borde de la imagen

            # SKU - esquina superior izquierda
            sku_bbox = draw.textbbox((0, 0), str(sku), font=font)
            sku_text_w = sku_bbox[2] - sku_bbox[0]
            sku_text_h = sku_bbox[3] - sku_bbox[1]
            sku_rect_w = sku_text_w + padding * 2
            sku_rect_h = sku_text_h + padding * 2
            draw.rounded_rectangle([(margin, margin), (margin + sku_rect_w, margin + sku_rect_h)], radius=radius, fill=(128, 128, 128, 150))
            sku_x = margin + (sku_rect_w - sku_text_w) // 2 - sku_bbox[0]
            sku_y = margin + (sku_rect_h - sku_text_h) // 2 - sku_bbox[1]
            draw.text((sku_x, sku_y), str(sku), font=font, fill="white")

            # Precio - esquina inferior derecha
            price_text = f"${price}"
            price_bbox = draw.textbbox((0, 0), price_text, font=font)
            price_text_w = price_bbox[2] - price_bbox[0]
            price_text_h = price_bbox[3] - price_bbox[1]
            price_rect_w = price_text_w + padding * 2
            price_rect_h = price_text_h + padding * 2
            img_w, img_h = image.size
            rect_x0 = img_w - price_rect_w - margin
            rect_y0 = img_h - price_rect_h - margin
            draw.rounded_rectangle([(rect_x0, rect_y0), (rect_x0 + price_rect_w, rect_y0 + price_rect_h)], radius=radius, fill=(128, 128, 128, 150))
            price_x = rect_x0 + (price_rect_w - price_text_w) // 2 - price_bbox[0]
            price_y = rect_y0 + (price_rect_h - price_text_h) // 2 - price_bbox[1]
            draw.text((price_x, price_y), price_text, font=font, fill="white")

            # "Mayoreo" - esquina inferior izquierda
            mayoreo_text = "Mayoreo"
            mayoreo_bbox = draw.textbbox((0, 0), mayoreo_text, font=font)
            mayoreo_text_w = mayoreo_bbox[2] - mayoreo_bbox[0]
            mayoreo_text_h = mayoreo_bbox[3] - mayoreo_bbox[1]
            mayoreo_rect_w = mayoreo_text_w + padding * 2
            mayoreo_rect_h = mayoreo_text_h + padding * 2
            img_w, img_h = image.size
            mayoreo_x0 = margin
            mayoreo_y0 = img_h - mayoreo_rect_h - margin
            draw.rounded_rectangle([(mayoreo_x0, mayoreo_y0), (mayoreo_x0 + mayoreo_rect_w, mayoreo_y0 + mayoreo_rect_h)], radius=radius, fill=(128, 128, 128, 150))
            mayoreo_x = mayoreo_x0 + (mayoreo_rect_w - mayoreo_text_w) // 2 - mayoreo_bbox[0]
            mayoreo_y = mayoreo_y0 + (mayoreo_rect_h - mayoreo_text_h) // 2 - mayoreo_bbox[1]
            draw.text((mayoreo_x, mayoreo_y), mayoreo_text, font=font, fill="white")

            return Image.alpha_composite(image, overlay)
        except Exception as e:
            print(f"✗ Error al agregar precio a la imagen: {e}")
            return image
        
    def addLogoToImage(self, image):
        
        try:
            logo = self.logo_path
            image = image.convert("RGBA")
            logo = Image.open(logo).convert("RGBA")

            # Redimensionar el logo al 15% del ancho de la imagen
            img_w, img_h = image.size
            logo_w = int(img_w * 0.30)
            ratio = logo_w / logo.width
            logo_h = int(logo.height * ratio)
            logo = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)

            # Reducir opacidad del logo (80 de 255 = ~30% de visibilidad)
            r, g, b, a = logo.split()
            a = a.point(lambda x: int(x * 1))
            logo = Image.merge("RGBA", (r, g, b, a))

            # Posición: esquina superior derecha con margen
            margin = 30
            x = img_w - logo_w - margin
            y = margin

            overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
            overlay.paste(logo, (x, y), logo)

            return Image.alpha_composite(image, overlay)
        except Exception as e:
            print(f"✗ Error al agregar el logo a la imagen: {e}")
            return image