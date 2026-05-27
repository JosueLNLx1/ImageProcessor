import ImageProcessor as ip
import PIL as Image

def main():
    print("Selecciona una opción:")
    print("1. imágenes y convertir a WebP")
    print("2. Agregar precio a la imagen (en desarrollo)")
    print("3. Eliminar fondo de las imágenes")

    opcion = input("Ingresa el número de la opción deseada: ")
    
    if opcion == "1":
        ImageToWebP()
    elif opcion == "2":
        ImageWithPrice()
        
    elif opcion == "3":
        RemoveBG()
    else:
        print("Opción no válida. Por favor, selecciona 1, 2 o 3.")

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

if __name__ == "__main__":    main()