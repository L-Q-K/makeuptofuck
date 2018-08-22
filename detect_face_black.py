import cv2
import numpy as np

cap = cv2.VideoCapture(0)
# tao mot doi tuong nhan dang
classhar = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
maskImg = cv2.imread('images.png')

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = classhar.detectMultiScale(gray, 1.25, 6)
    copy_image = np.copy(frame)

    face_crop = []

    x_face_max = 0
    y_face_max = 0
    w_face_max = 0
    h_face_max = 0
    for x, y, w, h in faces:
        if w * h > w_face_max * h_face_max:
            x_face_max = x
            y_face_max = y
            w_face_max = w
            h_face_max = h

        face_crop = frame[y_face_max:y_face_max + h_face_max, x_face_max:x_face_max + w_face_max, 0:3]

    # for f in faces:
    #     x, y, w, h = [v for v in f]
    #     cv2.rectangle(copy_image, (x, y), (x + w, y + h), (255, 0, 0), 3)
    #     # Define the region of interest in the image
    #     face_crop.append(frame[y:y + h, x:x + w, 0:3])

    if len(face_crop) != 0:
        rows, cols, channels = face_crop.shape
        kitty = cv2.resize(maskImg, (cols, rows))
        roi = kitty[0:rows, 0:cols]

        # Now create a mask of logo and create its inverse mask also
        img2gray = cv2.cvtColor(face_crop, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(img2gray, 255, 0, cv2.THRESH_BINARY_INV)
        cv2.imshow("mask", mask)
        mask_inv = cv2.bitwise_not(mask)

        # Now black-out the area of logo in ROI
        img1_bg = cv2.bitwise_and(roi, roi, mask_inv)
        cv2.imshow("img1", img1_bg)

        # Take only region of logo from logo image.
        img2_fg = cv2.bitwise_and(face_crop, face_crop, mask)
        cv2.imshow("img2", img2_fg)
        rows, cols, _ = img2_fg.shape

        # Put logo in ROI and modify the main image
        dst = cv2.add(img2_fg, img1_bg)
        frame[y_face_max:y_face_max+cols, x_face_max:x_face_max+rows] = dst
    cv2.imshow('video', frame)

    cv2.waitKey(30)
