import os
import numpy as np
from PIL import Image
################################################################################
from pytictoc import TicToc
t = TicToc()
################################################################################
################################################################################

def func_default_save(output_dir,filename_img, image_pil):
    os.makedirs(output_dir,exist_ok=True);
    filepath_img = os.path.join(output_dir,filename_img);
    image_pil.save(filepath_img);

################################################################################

def redimensionar_pil(imagen_pil, max_size):
    if max_size!=None and isinstance(max_size, (int, float)):
        # Obtener las dimensiones actuales de la imagen
        ancho, alto = imagen_pil.size

        if ancho>max_size or alto>max_size:
            # Calcular el factor de escala para redimensionar la imagen
            factor_escala = min(max_size*1.0 / ancho, max_size*1.0 / alto)

            # Redimensionar la imagen manteniendo la relación de aspecto original
            nueva_ancho = int(ancho * factor_escala)
            nueva_alto = int(alto * factor_escala)
            imagen_pil.thumbnail((nueva_ancho, nueva_alto), Image.ANTIALIAS)
        
    return imagen_pil;
    
import lib.lib_split_pil as lsp

def func_default_save2(output_dir,filename_img, image_pil,annotation1,resize=None):
    #os.makedirs(output_dir,exist_ok=True);
    
    rois_body, rois_face, coord_skeleton = lsp.get_rois_and_coordinates(image_pil,annotation1);
    output_dir_body = os.path.join(output_dir,'body');
    output_dir_face = os.path.join(output_dir,'face');
    output_dir_skel = os.path.join(output_dir,'skeleton');
    
    if os.path.isdir(output_dir_body)==False:
        os.makedirs(output_dir_body,exist_ok=True);
        os.makedirs(output_dir_face,exist_ok=True);
        os.makedirs(output_dir_skel,exist_ok=True);

    for i in range(len(rois_body)):
        if rois_body[i].size[0]>0 and rois_body[i].size[1]>0 and rois_face[i].size[0]>0 and rois_face[i].size[1]>0:
            filepath_body_img = os.path.join(output_dir_body,filename_img);
            body_dir=os.path.dirname(filepath_body_img);
            if os.path.isdir(body_dir)==False:
                os.makedirs(body_dir,exist_ok=True);
            rois_body[i]=redimensionar_pil(rois_body[i], resize);
            #print('body',filepath_body_img)
            rois_body[i].save(filepath_body_img);
            
            filepath_face_img = os.path.join(output_dir_face,filename_img);
            face_dir=os.path.dirname(filepath_face_img);
            if os.path.isdir(face_dir)==False:
                os.makedirs(face_dir,exist_ok=True);
            rois_face[i]=redimensionar_pil(rois_face[i], resize);
            rois_face[i].save(filepath_face_img);
            
            nombre_archivo, _ = filename_img.rsplit('.', 1)
            filename_skel = nombre_archivo + '.npy' 
            filepath_skel_npy = os.path.join(output_dir_skel,filename_skel);
            skel_dir=os.path.dirname(filepath_skel_npy);
            if os.path.isdir(skel_dir)==False:
                os.makedirs(skel_dir,exist_ok=True);
            np.save(filepath_skel_npy, coord_skeleton[i]);
    if len(rois_body)>0:
        return True;
    else:
        return False;
