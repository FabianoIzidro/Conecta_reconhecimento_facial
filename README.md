# Inteligência da Robô Conecta

Essa aplicação permite que você faça uma pergunta à Conecta após falar a palavra "Conecta". Perguntas como quem é a conecta, sobre o que é o núcleo de robótica, como ela está, que horas são, o que é o submarino rov, entre outras. A aplicação responde a pergunta e apresenta na tela uma animação representando as expressões de seus olhos, de acordo com seu status (ausente, aguardando pergunta e respondendo).

## Tecnologia

Esse projeto foi desenvolvido com [Python 3.10.2](https://www.python.org/downloads/) e faz uso das dependências listadas abaixo. É recomendado instalá-las com o terminal no modo administrador, para que elas possam ser instaladas globalmente e não dar erro quando o script inicializar com a raspberry. <br/>

### `pip install SpeechRecognition`
"SpeechRecognition" para reconhecer a voz e transformá-la em texto

### `pip install pyaudio`
"pyaudio" possibilita a captura de sons através do microfone

### `pip install pyttsx3`
"pyttsx3" para transformar texto em audio

### `pip install pillow`
"pillow" foi utilizado na interface gráfica

### `pip install playsound`
"playsound" para reproduzir arquivos de audio

### `pip install requests`
"requests" para consumir APIs

### `pip install firebase_admin`
"firebase_admin" para poder utilizar o firebase

## Configuração

Para fazer o script rodar automaticamente quando a raspberry inicializa, rode o comando `sudo crontab -e` no terminal da raspberry, vá até a última linha e digite `@reboot sleep 60 && python3 /home/pi/Desktop/Conecta/main.py >> /home/pi/Desktop/Conecta/log-inicializacao.txt 2>&1`. Nesse caso o script estava na pasta RFID que estava no Desktop da Raspberry.

## Scripts disponíveis

No diretório do projeto, você pode rodar:

### `python main.py`

Para iniciar a aplicação.

## Observações

- A implementação da animação dos gifs que foi feita precisa que eles não estejam otimizados (unoptimized) devido ao disposal method, como explicado [aqui](https://stackoverflow.com/questions/50904093/gif-animation-in-tkinter-with-pill-flickering-on-every-other-frame). Pra transformar um gif otimizado em não otimizado você pode usar a ferramenta [Ezgif - Repair corrupted gif](https://ezgif.com/repair), fazer upload do gif e usar o método de reparo "ImageMagick coalesce (unoptimize)". Depois basta salvar o gif não otimizado.

## O que falta?

- Otimizar a interface gráfica (Loading dos GIFs) e permitir que gifs otimizados sejam animados sem falhas; <br/>
- Adicionar mais perguntas

## Links que podem ser úteis

[Playlist: Python Voice Assistant](https://www.youtube.com/watch?v=-AzGZ_CHzJk&list=PLzMcBGfZo4-mBungzp4GO4fswxO8wTEFx) <br/>
[Explicação em português sobre o speech_recognition](https://letscode.com.br/blog/speech-recognition-com-python) <br/>
[Auto run any script on startup for Raspberry Pi 4](https://youtu.be/wVPAHI9on0o) <br/>
[Adicionar sleep 60 antes de executar o script](https://stackoverflow.com/questions/66182730/crontab-doesnt-run-python-script-on-a-raspberry-pi-4) para dar tempo da Raspberry inicializar antes de tentar executá-lo <br/>
[Criar um log na inicialização da raspberry](https://forums.raspberrypi.com/viewtopic.php?t=276808) para saber se o script foi executado. Isso também é útil para saber se houve erros ou não.
