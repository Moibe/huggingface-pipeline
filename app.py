import gradio as gr
from PIL import Image
import time
import os
import pathlib

def greet(input1, input2):

    modo = "video"
    #local o huggingface
    plataforma = "local"
    #face_swapper o face_enhancer o la combinación de ellos.
    procesador = "face_swapper"
    print("Inicio: Estamos en modo ", modo)
    print("Estamos en la plataforma:", plataforma)
    print("El procesador es: ", procesador)

    print("Input1:")
    print(input1)
    print("Input2:")
    print(input2)

    path_video = input2

    if plataforma == "local":
        #Para local.
        path_parts = path_video.split("\\")
    else:
        #Para HuggingFace
        path_parts = path_video.split("/")
    
    
    print("Imprimiendo path_parts: ", path_parts)
    path_particular = "/".join(path_parts[0:len(path_parts) - 1])
    path_general = "/".join(path_parts[0:len(path_parts) - 2])

    
    path_general = path_general.replace("\\", "/")
    path_particular = path_particular.replace("\\", "/")

    print("Path general: ", path_general)
    print("Path general: ", path_particular)

    path = pathlib.Path("result.mp4")
    path_foto = pathlib.Path(path_particular + "/temp/whitebeauty/0015.png")
    print("Éste es el path foto: ", path_foto)
    
    files = os.listdir(path_general)
    print("Estos son los files que hay:")
    print(files)

    time.sleep(5)

    ext_imagen = "png"
    ext_video = "mp4"

    #Selector de modo.
    if modo == "video": 
        print("Se asigno la extensión de video:", ext_video)
        extension = ext_video
    else:
        print("Se asigno la extensión de video:", ext_video)
        extension = ext_imagen

    #El source siempre es una imagen.
    source_path = "source.png"
    target_path = "target." + extension
    result_path = "result." + extension

    #La primera siempre será una imagen, por eso no entra en el modo selector.
    source_image = Image.fromarray(input1)
    print("Esto es source_image: ", source_image)
    source_image.save(source_path)
        
    #Aquí trabajaremos solo el target.
    if modo == "video":
        #Para Video
        target_path = input2
    else:
        #Es decir si es modo imagen
        #Para Imagenes
        target_image = Image.fromarray(input2)
        print("Esto es target_image: ", target_image)
        target_image.save(target_path)

    print("Después de los selectores de modo los paths quedaron así:")
    print("source_path: ", source_path)
    print("target_path: ", target_path)

    command = f"python run.py -s {source_path}  -t {target_path} -o {result_path} --frame-processor {procesador}"
    print(command)
    time.sleep(1)
    proc = os.popen(command)
    output = proc.read()

    print("Output (resultado de la ejecución del código):")
    time.sleep(2)
    print(output)
    print("Terminó la impresión del output...")

    print("Ahora estamos imprimiendo las rutas para ver si apareció una nueva:")
    files = os.listdir(path_general)
    print("Estos son los files que hay:")
    print(files)

    if modo == "video":
        #Para video
        return path, path_foto
    else:
        #Para imagen
        path = pathlib.Path("result.png")
        print("Éste es el path para imagen:", path)
        return path, path
     
#Así para imagenes
# demo = gr.Interface(
# fn=greet, inputs=[gr.Image(), gr.Image()], outputs=[gr.Image(), gr.Image()]
# )

#Así para video
demo = gr.Interface(
fn=greet, inputs=[gr.Image(), gr.Video()], outputs=[gr.Video(), gr.Image()]
)

demo.launch()