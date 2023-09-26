import cv2


def gauss_p(image, levels):
    # teniendo en cuenta que el enunciado pide un "reloj" simetrico
    # con los mismos niveles superiores e inferiores, solo se necesita de un valor para
    # los niveles

    pyramid = [image]
    imgsup = image
    for i in range(levels):  # generación de niveles superiores
        imgsup = cv2.resize(imgsup, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)  # Duplicar el tamaño
        pyramid.append(imgsup)

    for i in range(levels):  # Comenzando desde el nivel 0
        image = cv2.GaussianBlur(image, (9, 9), 0)  # Aplicar filtro gaussiano con kernel más grande
        image = image[::2, ::2]  # Reducir la resolución a la mitad
        pyramid.append(image)

    return pyramid  # la piramide que se retorna tiene los primeros n elementos con imagenes reducidas y la segunda mitad imagenes agrandadas


def save_img(piramide):
    fr = len(piramide) // 2
    for i in range(len(piramide)):
        if i > fr:
            cv2.imwrite(f"PiramideGaussiana/level{3 - i}.jpg", piramide[i])
        elif i <= fr:
            cv2.imwrite(f"PiramideGaussiana/level{i}.jpg", piramide[i])


def lap_p(levels):
    #solo se requieren la cantidad de niveles, ya que la imagen ya fue procesada en al funcion anterior
    pyramid = []
    for i in range(levels - 1):
        imgsup = cv2.imread(f"PiramideGaussiana/level{i - 3}.jpg") #leer la imagen mas pequena
        imgsup = cv2.resize(imgsup, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)  # Duplicar el tamaño
        imgsup2 = cv2.imread(f"PiramideGaussiana/level{i - 3 + 1}.jpg") #leer la siguiente imagen
        image = cv2.subtract(imgsup, imgsup2) #restar las imagenes
        pyramid.append(image) #agregar a la piramida

    return pyramid  # la piramide que se retorna son las substracciones de las parejas de la piramide gaussiana


def save_img2(piramide):
    for i in range(len(piramide)):
        cv2.imwrite(f"PiramideLaplaciana/level{i + 1}.jpg", piramide[i])


def main():
    img = cv2.imread("input.jpg")
    # La imagen original se guarda en el ciclo de guardado de niveles como level-0

    if img is None:
        print("La imagen no fue cargada correctamente")
        exit(1)
    else:
        piramide = gauss_p(img, 3)
        save_img(piramide)
        piramide2 = lap_p(len(piramide))
        save_img2(piramide2)


if __name__ == '__main__':
    main()
