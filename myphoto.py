import dlib
from PIL import Image
import os, sys
import threading as TH
import glob
import cv2.cv2 as cv2
import shutil

dnnFaceDetector = dlib.cnn_face_detection_model_v1("mmod_human_face_detector.dat")


def __photo_send(user_id:int, file_path:str, func_msg, message, st:str):
    pathdir = 'photos/'
    files = glob.glob(pathdir+'%d-photo_*.jpg'%user_id)
    out_path = pathdir +'%d-photo_%d.jpg'%(user_id, len(files))
    try:
        img = cv2.imread(file_path)
    except:
        print('Img error')
        return 1
    rects = dnnFaceDetector(img, 1)
    print('Rects:', len(rects))
    if len(rects)>0:
        shutil.move(file_path, out_path)
        print('Face detected!!!', out_path)
        func_msg(message.chat.id, st+'Face DETECTED!!! c:\nSaved to "%s"'%out_path)
    else:
        print('Face not detected!', file_path)
        os.remove(file_path)
        func_msg(message.chat.id, st + 'Face not detected! :c')


def photo_send(user_id:int, file_path:str, func_msg, message, st:str):
    thread = TH.Thread(target=__photo_send, args=(user_id, file_path, func_msg, message, st))
    thread.start()
