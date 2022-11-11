import face_recognition as fr

def reconhece_face(url_foto):
    foto = fr.load_image_file(url_foto)
    rostos = fr.face_encodings(foto)
    if(len(rostos) > 0):
        return True, rostos
    
    return False, []

def get_rostos():
    rostos_conhecidos = []
    nomes_dos_rostos = []

    Marlon1 = reconhece_face("./img/Marlon1.jpg")
    if(Marlon1[0]):
        rostos_conhecidos.append(Marlon1[1][0])
        nomes_dos_rostos.append("Marlon")
    
    return rostos_conhecidos, nomes_dos_rostos