import ImageProcessor as ip
import PIL as Image

def main():
    print("Selecciona una opción:")
    print("1. imágenes y convertir a WebP")
    print("2. Agregar precio a la imagen (en desarrollo)")
    print("3. Eliminar fondo de las imágenes")
    print("4. Limpiar carpeta de entrada")

    opcion = input("Ingresa el número de la opción deseada: ")
    
    if opcion == "1":
        ImageToWebP()
    elif opcion == "2":
        ImageWithPrice()
        
    elif opcion == "3":
        RemoveBG()
    elif opcion == "4":
        cleanInput()
    else:
        print("Opción no válida. Por favor, selecciona 1, 2, 3 o 4.")

def ImageToWebP():
    images = ip.ImageProcessor("input", "output")
    images.RemoveBG()
    images.CreateCanvas()
    images.PasteOnCanvas()
    images.__CleanTemp()

def ImageWithPrice():
    images = ip.ImageProcessor("input", "output")
    images.ImagesWithPrice()
    print("Función para agregar precio a la imagen (en desarrollo)" )
    

def RemoveBG():
    images = ip.ImageProcessor("input", "output")
    images.RemoveBG()

def cleanInput():
    try:
        for item in ip.Path("input").iterdir():
            if item == ip.Path(".gitignore"):
                continue  # No eliminar el archivo .gitignore
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                for subitem in item.iterdir():
                    subitem.unlink()
        print("✓ Carpeta de entrada limpiada.")
    except Exception as e:
        print(f"✗ Error al limpiar la carpeta de entrada: {e}")

if __name__ == "__main__":    main()