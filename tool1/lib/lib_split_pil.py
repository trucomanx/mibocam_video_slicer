
import openpifpaf
import OpenPifPafTools.OpenPifPafGetData as oppgd

def get_rois_and_coordinates(image_pil,annotations):
    if annotations==None:
        # Cargar el modelo de OpenPifPaf pre-entrenado
        predictor = openpifpaf.Predictor(checkpoint='shufflenetv2k16');

        # Detectar personas en la imagen
        annotations, gt_anns, image_meta = predictor.pil_image(image_pil);

    # Inicializar listas para almacenar las ROI y las coordenadas del esqueleto
    rois_cuerpo = []
    rois_cabeza = []
    coordenadas_esqueleto = []

    # Procesar cada persona detectada (si hay alguna)
    for annotation in annotations:
        # Extraer la ROI del cuerpo de la imagen original
        (xi,yi,xo,yo) = oppgd.get_body_bounding_rectangle(annotation.data, factor=1.0);
        xi=int(xi);        yi=int(yi);
        xo=int(xo);        yo=int(yo);
        body_bbox=(xi,yi,xo,yo);
        roi_cuerpo = image_pil.crop(body_bbox);
        rois_cuerpo.append(roi_cuerpo);

        # Extraer la ROI de la cabeza de la imagen original
        (xi,yi,xo,yo) = oppgd.get_face_bounding_rectangle(annotation.data, factor=1.0);
        xi=int(xi);        yi=int(yi);
        xo=int(xo);        yo=int(yo);
        head_bbox=(xi,yi,xo,yo);
        roi_cabeza = image_pil.crop(head_bbox);
        rois_cabeza.append(roi_cabeza);

        # Obtener las coordenadas del esqueleto
        coordenadas_esqueleto.append(annotation.data.flatten());

    return rois_cuerpo, rois_cabeza, coordenadas_esqueleto;



