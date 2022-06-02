import os
import time
from random import randint
from datetime import datetime
import threading

import speech_recognition
import pyttsx3
from tkinter import *
from PIL import Image
from playsound import playsound
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import numpy as np
import face_recognition as fr
import cv2
from engine import get_rostos

# Palavra que é necessário falar antes de dar inicio a uma pergunta
wake_word = "conect"

"""
Reproduz em audio o texto passado por parâmetro
"""
def falar(textos):
    if(len(textos) > 0):
        texto = textos[randint(0,len(textos)-1)]   # Escolhe um texto dentre vários

        pytts = pyttsx3.init("sapi5")
        pytts.setProperty("voice", "brazil")
        pytts.say(texto)
        pytts.runAndWait()
        print("Eu falei: "+texto)


"""
Fica escutando o microfone e chama a função de entender o que foi falado quando é reconhecido algum som
"""
def escutarMicrofone():
    print("Escutando microfone...")
    textoFalado = ""
    recognizer = speech_recognition.Recognizer()
    recognizer.dynamic_energy_threshold = False
    recognizer.energy_threshold = 400   # Para evitar que um ruído ambiente faça pensar que o usuário ainda está falando: https://stackoverflow.com/questions/32753415/python-speechrecognition-ignores-timeout-when-listening-and-hangs

    while textoFalado == "":
        with speech_recognition.Microphone() as origemAudio:
            audioEscutado = recognizer.listen(origemAudio, phrase_time_limit=5.0)   # phrase_time_limit: máximo de segundos que isso permitirá que uma frase continue antes de parar e retornar a parte da frase processada

        try:
            # Transforma o audio escutado em texto
            textoFalado = recognizer.recognize_google(audioEscutado, language="pt-BR")
        except speech_recognition.UnknownValueError as erro:
            if(str(erro) != ""):
                print("Erro: "+str(erro))

    print("Eu escutei: "+textoFalado)
    return textoFalado.lower()

"""
Checa o texto por meio das condições para tentar entender o que foi falado. Se enteder algo, dá uma resposta em audio
"""
def main():
    while True:
        setarExpressao("ausente")
        textoFalado = escutarMicrofone()
        respostas = []

        # Se a palavra definida na variável wake_word tiver aparecido no texto audioEscutado, então aguarda que o usuário faça uma pergunta
        if (textoFalado.count(wake_word) > 0):
            inicioDelay = time.time()
            parar = False
            numeroRespostas = 0
            falar(["Ao seu dispor"])

            while((time.time() - inicioDelay < 120 and parar == False)): # Enquanto não tiver passado 2 minutos dentro do while ele continua aguardando uma pergunta
                setarExpressao("aguardando")
                textoFalado = escutarMicrofone()

                frasesBoasVindas = ["olá", "bom dia", "boa tarde", "boa noite"]
                for frase in frasesBoasVindas:
                    if frase in textoFalado:
                        setarExpressao("respondendo")
                        falar(["Oi! Tudo bem?"])
                        setarExpressao("aguardando")
                        respostaBoasVindas = escutarMicrofone()
                        if "não" in respostaBoasVindas:
                            respostas = ["Que pena. Desejo que esteja melhor o mais breve possível"]
                        else:
                            respostas = ["Que ótimo! Também estou bem. Melhor agora."]

                if "quem é" in textoFalado:
                    respostas = ["Eu sou a conecta, fui desenvolvida pelo núcleo de robótica do cesmac e esse chapéu de guerreiro na minha cabeça é uma homenagem ao folclore alagoano"]

                if "horas" in textoFalado:
                    respostas = ["Agora são "+str(datetime.today().hour)+" horas e "+str(datetime.today().minute)+" minutos"]

                if "robótica" in textoFalado:
                    respostas = ["Eu fui desenvolvida no núcleo de robótica. Ele é um núcleo de pesquisa onde por meio da tecnologia são desenvolvidos projetos solicitados por alunos e professores. Como aplicativos, equipamentos e até mesmo próteses. O núcleo de robótica é multidisciplinar."]

                if "piada" in textoFalado:
                    respostas = ["Porquê os robôs nunca sentem medo? A resposta é: Porque nós temos nervos de aço. Rárárárá"]
                    

                if "fechar" in textoFalado:
                    db.reference("Portas").child("Porta 1").set(True)
                    respostas = ["Ok, porta fechada", "Tudo bem, fechei a porta", "Pronto"]

                if "abrir" in textoFalado:
                    db.reference("Portas").child("Porta 1").set(False)
                    respostas = ["Ok, porta aberta", "Tudo bem, abri a porta", "Pronto"]

                if "inteligente" in textoFalado:
                    respostas = ["Obrigada", "Muito obrigada"]
                elif "conversa" in textoFalado:
                    respostas = ["Converso sim. Você pode me perguntar o que é o núcleo de robótica, quem eu sou e até mesmo me pedir para contar uma piada."]
                elif "obrigad" in textoFalado:
                    respostas = ["Foi um prazer te responder", "Tamo junto", "Não há de quê", "De nada"]
                elif "desculpa" in textoFalado:
                    respostas = ["Tá tudo bem", "Sem problemas"]
                elif "tchau" in textoFalado:
                    respostas = ["Tchau, adorei ter falado com você", "Até mais", "Tchauzinho"]
                    parar = True

                # Se não tiver entendido o que foi falado (isso roda apenas se a conecta ainda não tiver dado nenhuma resposta)
                if(len(respostas) == 0 and numeroRespostas == 0):
                    setarExpressao("ausente")
                    respostas = ["Desculpa, não entendi o que você falou"]
                else:
                    setarExpressao("respondendo")
                    numeroRespostas = numeroRespostas + 1

                falar(respostas)
                respostas = []


'''
Função recebe por parâmetro o caminho de uma imagem animada GIF e retorna um array com cada frame da animação
que pode ser usado para animá-lo na janela da interface gráfica
'''
def carregarFramesGIF(caminhoImagem):
    imagem = Image.open(caminhoImagem)
    quantidadeFrames = imagem.n_frames
    return [PhotoImage(file=caminhoImagem, format = f'gif -index {i}') for i in range(quantidadeFrames)]

'''
Função que recebe um array com os frames da imagem animada GIF e fica responsável por mantê-la animada
no label presente na janela da interface gráfica
'''
def animarGIFExpressao(nomeGIF, framesGIF, contadorFrame = 0):
    global animacaoGIF

    frame = framesGIF[contadorFrame]
    labelExpressao.configure(image=frame)   # Edita o frame apresentado no label

    contadorFrame += 1
    if contadorFrame == len(framesGIF):
        contadorFrame = 0

    # Para manter o GIF animado por meio de um loop (50 Milissegundos por repetição)
    if(nomeGIF == nomeGIFEmReproducao):
        animacaoGIF = janela.after(50, lambda :animarGIFExpressao(nomeGIF, framesGIF, contadorFrame))

'''
Função que para qualquer animação que esteja em andamento para poder inicializar a animação da expressão
passada por parâmetro
'''
def setarExpressao(nomeExpressao):
    global nomeGIFEmReproducao
    nomeGIFEmReproducao = nomeExpressao # Para caso uma função do animarGIF já esteja em execução, ele evite criar outro loop do GIF antigo e acabar animando 2 gifs ao mesmo tempo.

    if(animacaoGIF != None):
        janela.after_cancel(animacaoGIF) # Parar gif que já está sendo reproduzido
        print("Animação antiga parada")

    if nomeExpressao == "aguardando":
        animarGIFExpressao(nomeExpressao, expressaoAguardando)
    elif nomeExpressao == "respondendo":
        animarGIFExpressao(nomeExpressao, expressaoRespondendo)
    else:
        animarGIFExpressao(nomeExpressao, expressaoAusente)

    print("Expressão "+nomeExpressao+" definida")



"""
# # # # Inicialização da Conecta # # # #
"""
falar(["Inicializando expressões. Isso pode levar alguns minutos."])

janela = Tk()
janela.title("Conecta")
janela.configure(bg="black")
janela.attributes("-fullscreen", True)

# Inicialização do firebase
credencial = credentials.Certificate("serviceAccountKey.json")
firebase = firebase_admin.initialize_app(credencial, {
    'databaseURL': 'https://autcitec-default-rtdb.firebaseio.com/'
})

# Loading das expressões
expressaoAusente = carregarFramesGIF("expressoes/expressao-ausente.gif")
expressaoAguardando = carregarFramesGIF("expressoes/expressao-aguardando.gif")
expressaoRespondendo = carregarFramesGIF("expressoes/expressao-respondendo.gif")

labelExpressao = Label(janela)
labelExpressao.config(bg="black")
labelExpressao.pack()
labelExpressao.place(x=janela.winfo_screenwidth()/2, y=janela.winfo_screenheight()/2, anchor="center") # Posiciona o centro do label na posição x e y equivalentes a metade da janela

animacaoGIF = None  # Pra poder parar a animação do GIF posteriormente
nomeGIFEmReproducao = ""

falar(["Estou pronta"])

# Inicia a função main em uma Thread, para que fique rodando ao  mesmo tempo que as funções responsáveis pelas expressões.
threadMain = threading.Thread(target=main, args=())
threadMain.daemon = True    # https://stackoverflow.com/questions/11815947/cannot-kill-python-script-with-ctrl-c
threadMain.start()

janela.mainloop()

rostos_conhecidos, nomes_dos_rostos = get_rostos()

video_capture = cv2.VideoCapture(0)
while True: 
    ret, frame = video_capture.read()

    rgb_frame = frame[:, :, ::-1]

    localizacao_dos_rostos = fr.face_locations(rgb_frame)
    rosto_desconhecidos = fr.face_encodings(rgb_frame, localizacao_dos_rostos)

    for (top, right, bottom, left), rosto_desconhecido in zip(localizacao_dos_rostos, rosto_desconhecidos):
        resultados = fr.compare_faces(rostos_conhecidos, rosto_desconhecido)
        print(resultados)

        face_distances = fr.face_distance(rostos_conhecidos, rosto_desconhecido)
        g
        melhor_id = np.argmin(face_distances)
        if resultados[melhor_id]:
            nome = nomes_dos_rostos[melhor_id]
        else:
            nome = "Desconhecido"
        
        # Ao redor do rosto
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Embaixo
        cv2.rectangle(frame, (left, bottom -35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_SIMPLEX

        #Texto
        cv2.putText(frame, nome, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv2.imshow('Webcam_facerecognition', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()