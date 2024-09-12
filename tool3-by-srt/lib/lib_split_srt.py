#!/usr/bin/python
import os
import pysrt
import subprocess
import datetime

def calcular_duracion(start_time, end_time):
    start_seconds = start_time.hours * 3600 + start_time.minutes * 60 + start_time.seconds + start_time.milliseconds / 1000
    end_seconds = end_time.hours * 3600 + end_time.minutes * 60 + end_time.seconds + end_time.milliseconds / 1000
    
    duration_seconds = end_seconds - start_seconds

    return duration_seconds

def split_video(input_dir,reldir,filename,output_dir,format_outname,min_time_dec=3):
    str_path = os.path.join(input_dir,reldir,filename);
    
    filename_mp4 = os.path.splitext(filename)[0]+'.mp4';
    mp4_path = os.path.join(input_dir,reldir,filename_mp4);
    
    
    
    # Carrega o arquivo SRT
    subtitles = pysrt.open(str_path)

    # Itera sobre as legendas
    for subtitle in subtitles:
        #print(f"Index: {subtitle.index}")
        #print(f"Start: {subtitle.start}")
        #print(f"End: {subtitle.end}")
        #print(f"Text: {subtitle.text}")

        start_time_str = f"{subtitle.start.hours:02}:{subtitle.start.minutes:02}:{subtitle.start.seconds:02}.{subtitle.start.milliseconds:03}"
        end_time_str = f"{subtitle.end.hours:02}:{subtitle.end.minutes:02}:{subtitle.end.seconds:02}.{subtitle.end.milliseconds:03}"

        duration = calcular_duracion(subtitle.start,subtitle.end)
        duration_str = f"{int(duration // 3600):02}:{int((duration % 3600) // 60):02}:{int(duration % 60):02}.{int((duration % 1) * 1000):03}"
        
        
        print("\n\n---")
        print('duration:',duration,duration_str)

        mp4_out_dir = os.path.join(output_dir,reldir,subtitle.text); 
        os.makedirs(mp4_out_dir,exist_ok=True);
        
        new_filename = str(format_outname);
        new_filename = new_filename.replace("{INDEX}", str(subtitle.index))
        new_filename = new_filename.replace("{VNAME}", os.path.splitext(filename)[0])
        mp4_out_path = os.path.join(mp4_out_dir,new_filename);

        # Comando FFmpeg para dividir el video
        if duration>min_time_dec:
            command = [
                'ffmpeg',
                '-i', mp4_path,         # Archivo de entrada
                '-ss',start_time_str,     # Tiempo de inicio
                '-to',end_time_str,       # Tiempo de inicio
                #'-t', duration_str,      # Duración calculada
                '-c','copy',             # Copiar el video y audio sin reencodear
                mp4_out_path              # Archivo de salida
            ]
        else:
            command = [
                'ffmpeg',
                '-i', mp4_path,         # Archivo de entrada
                '-ss',start_time_str,     # Tiempo de inicio
                '-to',end_time_str,       # Tiempo de inicio
                '-c:v','libx264',       # Copiar el video 
                '-c:a','aac',       # Copiar el video 
                mp4_out_path              # Archivo de salida
            ]
        
        for ttt in command:
            print(ttt);
        print('')
        
        # Ejecutar el comando
        try:
            subprocess.run(command, check=True)
            print(f"El video ha sido dividido y guardado en {mp4_out_path}")
        except subprocess.CalledProcessError as e:
            print(f"Ocurrió un error al dividir el video: {e}")
        
