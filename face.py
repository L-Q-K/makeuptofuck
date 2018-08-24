from __future__ import division
import dlib
import cv2
import numpy as np
import math
from detect_face_white import *
import menu
import pygame

from threading import Thread

import os

def kc_2_diem(diem1, diem2):
    kc = math.sqrt((diem1[0] / ratio - diem2[0] / ratio) ** 2 + (diem1[1] / ratio - diem2[1] / ratio) ** 2)
    return kc


def resize(img, width=None, height=None, interpolation = cv2.INTER_AREA):
    global ratio
    w, h = img.shape
    if width is None and height is None:
        return img
    elif width is None:
        ratio = height/h
        width = int(w*ratio)
        resized = cv2.resize(img, (height, width), interpolation)
        return resized
    else:
        ratio=width/w
        height=int(h*ratio)
        resized=cv2.resize(img,(height,width),interpolation)
        return resized


def shape_to_np(shape, dtype="int"):
    coords = np.zeros((68,2), dtype=dtype)
    for i in range(0,68):
        coords[i] = (shape.part(i).x, shape.part(i).y)
    return coords

camera = cv2.VideoCapture(0)
predictor_path = 'shape_predictor_68_face_landmarks.dat'
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)

thread_menu = Thread(target=menu.main)
thread_menu.start()

mask_name = menu.btn_clicked

def start():
    while True:
        cv2.moveWindow("BoyHelpsMakeUp", 500, 100)

        ret, frame = camera.read()
        if not ret:
            print('Failed to capture frame from camera. Check camera index in cv2.VideoCapture(0) \n')
            break

        frame_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_resized = resize(frame_grey, width=120)
        dets = detector(frame_resized, 1)

        if len(dets) > 0:
            for k, d in enumerate(dets):
                shape = predictor(frame_resized, d)
                shape = shape_to_np(shape)
                # face=[]
                # for (x,y) in shape:
                #     cv2.circle(frame,(int(x/ratio),int(y/ratio)),3,(255,255,255),-1)
                # face.append(shape[0])
                # face.append(shape[16])
                # for i in range(2):
                #     cv2.circle(frame,(int(face[i][0]/ratio),int(face[i][1]/ratio)),3,(0,0,255),-1)

                # EYEBROW:

                w_lmt = int(kc_2_diem(shape[17], shape[21]))
                h_lmt = int(kc_2_diem(shape[19], shape[37])/2)
                w_lmp = int(kc_2_diem(shape[22], shape[26]))
                h_lmp = int(kc_2_diem(shape[24], shape[44])/2)

                if len(mask_name["EYEBROW"]) == 1:
                    if w_lmt > 0 and h_lmt > 0:
                        lmt = cv2.imread('picture\\eyebrow\\' + mask_name["EYEBROW"][0] + '.png')
                        apply_white_mask(frame, int(shape[17][0]/ratio), int(shape[19][1]/ratio), w_lmt, h_lmt, lmt)
                    if w_lmp > 0 and h_lmp > 0:
                        lmp = cv2.imread('picture\\eyebrow\\' + mask_name["EYEBROW"][0] + '_1.png')
                        apply_white_mask(frame,int(shape[22][0]/ratio),int(shape[24][1]/ratio),w_lmp,h_lmp,lmp)

                # EYE
                w_leye = int(kc_2_diem(shape[37], shape[38]))+8
                h_leye = w_leye
                w_reye = int(kc_2_diem(shape[43], shape[44]))+8
                h_reye = w_reye

                if len(mask_name["EYE"]) == 1:
                    leye = cv2.imread('picture\\eye\\' + mask_name["EYE"][0] + '.png')
                    print('picture\\eye\\' + mask_name["EYE"][0] + '.png')
                    print(type(leye))

                    if w_leye > 0 and h_leye > 0:
                        apply_white_mask(frame, int(shape[43][0]/ratio - 3), int(shape[43][1]/ratio-3), w_leye, h_leye, leye)
                    if w_reye > 0 and h_reye > 0:
                        apply_white_mask(frame, int(shape[37][0]/ratio), int(shape[37][1]/ratio-3), w_reye, h_reye, leye)

                # BEARD
                w_ria = int(kc_2_diem(shape[48], shape[54]))+50
                h_ria = int(kc_2_diem(shape[31], shape[60]))+10

                if len(mask_name["BEARD"]) == 1:
                    ria = cv2.imread('picture\\beard\\' + mask_name["BEARD"][0] + '.png')

                    if w_ria and h_ria > 0:
                        apply_white_mask(frame, int(shape[48][0]/ratio-25), int(shape[31][1]/ratio-10), w_ria, h_ria, ria)

        cv2.imshow("BoyHelpsMakeUp", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            camera.release()
            break


if __name__ == '__main__':
    start()