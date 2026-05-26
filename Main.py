import ImageProcessor as ip
import PIL as Image

def main():
    print("Selecciona una opción:")
    print("1. imágenes y convertir a WebP")
    print("2. Agregar precio a la imagen (en desarrollo)")

    opcion = input("Ingresa el número de la opción deseada: ")
    
    if opcion == "1":
        ImageToWebP()
    elif opcion == "2":
        ImageWithPrice()
    else:
        print("Opción no válida. Por favor, selecciona 1 o 2.")

def ImageToWebP():
    images = ip.ImageProcessor("input", "output")
    images.RemoveBG()
    images.CreateCanvas()
    images.PasteOnCanvas()
    images.CleanTemp()

def ImageWithPrice():
    images = ip.ImageProcessor("input", "output")
    images.SourcePhotos()
    print("Función para agregar precio a la imagen (en desarrollo)" )
    

if __name__ == "__main__":    main()