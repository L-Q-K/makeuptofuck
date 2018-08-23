import cv2
import numpy as np

def apply_white_mask(frame, x, y, w, h, face_mask):
    if face_mask is not None:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Extract the region of interest from the image
        frame_roi = frame[y:y+h, x:x+w]
        face_mask_small = cv2.resize(face_mask, (w, h), interpolation=cv2.INTER_AREA)

        # Convert color image to grayscale and threshold it
        gray_mask = cv2.cvtColor(face_mask_small, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(gray_mask, 180, 255, cv2.THRESH_BINARY_INV)

        # Create an inverse mask
        mask_inv = cv2.bitwise_not(mask)

        # Use the mask to extract the face mask region of interest
        masked_face = cv2.bitwise_and(face_mask_small, face_mask_small, mask=mask)

        # Use the inverse mask to get the remaining part of the image
        masked_frame = cv2.bitwise_and(frame_roi, frame_roi, mask=mask_inv)

        # add the two images to get the final output
        frame[y:y+h, x:x+w] = cv2.add(masked_face, masked_frame)

        return frame[y:y+h, x:x+w]