import os
import subprocess

def flip_videos(input_directory, output_directory):
    # Verificar se o diretório de saída existe, caso contrário, criar
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # Iterar sobre todos os arquivos no diretório de entrada
    for filename in os.listdir(input_directory):
        if filename.endswith(".mp4"):
            # Caminho completo do arquivo de vídeo de entrada
            input_filepath = os.path.join(input_directory, filename)
            
            # Caminho completo do arquivo de vídeo de saída
            output_filepath = os.path.join(output_directory, filename)
            
            # Comando ffmpeg para aplicar flip horizontal
            comando = [
                'ffmpeg',
                '-i', input_filepath,
                '-vf', 'vflip',
                '-c:a', 'copy',  # Copia a trilha de áudio sem recodificar
                output_filepath
            ]
            
            # Executar o comando ffmpeg
            subprocess.run(comando)

# Diretório de entrada contendo os vídeos originais
input_directory = '/media/fernando/Expansion/DATASET/TESE/PATIENT-MIBOCAM/patients-videos/patient0/2024-05-21-9578'

# Diretório de saída onde os vídeos flipados serão salvos
output_directory = '2024-05-21-9578-vflip'

# Aplicar flip horizontal a todos os vídeos no diretório de entrada e salvar no diretório de saída
flip_videos(input_directory, output_directory)
