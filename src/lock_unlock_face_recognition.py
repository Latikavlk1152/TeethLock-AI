import cv2
import sys
import numpy as np
import pyautogui
import ctypes
import os
import datetime
import dlib
from keras.models import load_model

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_ROOT = os.path.dirname(BASE_DIR)

MODELS_DIR = os.path.join(PROJECT_ROOT, "models")
TRAINER_DIR = os.path.join(PROJECT_ROOT, "trainer")

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

def crop_teeth(image, detector, predictor):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    dets = detector(img, 1)
    teeth_regions = []

    for k, d in enumerate(dets):
        shape = predictor(img, d)

        # Define the region for teeth
        xteethpoints = [shape.part(x).x for x in range(48, 67)]
        yteethpoints = [shape.part(x).y for x in range(48, 67)]
        maxx = max(xteethpoints)
        minx = min(xteethpoints)
        maxy = max(yteethpoints)
        miny = min(yteethpoints)

        pad = 10
        crop_image = image[miny - pad:maxy + pad, minx - pad:maxx + pad]
        teeth_regions.append(crop_image)

    return teeth_regions

counter_correct = 0
counter_wrong = 0

# now = datetime.datetime.now().second
now = datetime.datetime.now()

# Load the teeth recognition model using Keras (replace 'your_model.h5' with the correct path)
model_path = os.path.join(TRAINER_DIR, "trained_model.h5")

teeth_recognizer = load_model(model_path)

cascade_path = os.path.join(MODELS_DIR, "haarcascade_frontalface_default.xml")
face_cascade = cv2.CascadeClassifier(cascade_path)
font = cv2.FONT_HERSHEY_COMPLEX_SMALL

cam = cv2.VideoCapture(0)  # Start video capturing
detector = dlib.get_frontal_face_detector()
landmark_path = os.path.join(MODELS_DIR, "shape_predictor_68_face_landmarks.dat")

predictor = dlib.shape_predictor(landmark_path)

print('before the loop')
while True:
    # now1 = datetime.datetime.now().second
    # if now1 > now + 8:
        # cam.release()
        # cv2.destroyAllWindows()
        # ctypes.windll.user32.LockWorkStation()
        # sys.exit()

    ret, im = cam.read()
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    print(f"Detected: {len(faces)}")

    if len(faces) != 1:
        elapsed_time = (datetime.datetime.now() - now).total_seconds()
        if elapsed_time > 3:
            cam.release()
            cv2.destroyAllWindows()
            ctypes.windll.user32.LockWorkStation()
            sys.exit()
    else:
        # Reset the timer whenever a face is detected
        now = datetime.datetime.now()

    for (x, y, w, h) in faces:
        # print("for every face")

        # Define the region for teeth using facial landmarks
        shape = predictor(gray, dlib.rectangle(x, y, x + w, y + h))

        xteethpoints = [shape.part(x).x for x in range(48, 67)]
        yteethpoints = [shape.part(x).y for x in range(48, 67)]
        maxx_teeth = max(xteethpoints)
        minx_teeth = min(xteethpoints)
        maxy_teeth = max(yteethpoints)
        miny_teeth = min(yteethpoints)

        # Coordinates for the teeth region
        x_teeth = minx_teeth - 20
        y_teeth = miny_teeth - 20
        w_teeth = maxx_teeth - minx_teeth + 40
        h_teeth = maxy_teeth - miny_teeth + 40

        # Draw the rectangle around the teeth region
        cv2.rectangle(im, (x_teeth, y_teeth), (x_teeth+w_teeth, y_teeth+h_teeth), (0, 255, 0), 4)

        # Crop the teeth region
        teeth_regions = crop_teeth(im[y:y+h, x:x+w], detector, predictor)

        for teeth_region in teeth_regions:
            if teeth_region is not None:
                # print("teeth region found - processing")
                # Resize the teeth region to match the input size of the teeth recognition model
                teeth_region_resized = cv2.resize(teeth_region, (128, 128))

                # Normalize the pixel values to be in the range [0, 1]
                teeth_region_normalized = teeth_region_resized / 255.0

                # Reshape to match the input shape of the model
                teeth_region_input = np.reshape(teeth_region_normalized, (1, 128, 128, 3))  # Adjust the number of channels if needed

                # Recognize the user based on teeth features
                prediction_teeth = teeth_recognizer.predict(teeth_region_input)

                # Modify this part based on your model output
                label_teeth = np.argmax(prediction_teeth)
                confidence_teeth = prediction_teeth[0, label_teeth]

                if confidence_teeth < 0.5:
                    counter_wrong += 1
                    print("Wrong")
                    label_teeth = "Unknown"
                    print(f"Label (Teeth): {label_teeth}")
                    print(f"Confidence (Teeth): {confidence_teeth * 100}")
                    print("counter_wrong - " + str(counter_wrong))
                    cv2.rectangle(im, (x-22, y-90), (x+w+22, y-22), (0, 0, 255), -1)
                    cv2.putText(im, str(label_teeth), (x, y-40), font, 1, (0, 0, 0), 2)
                else:
                    label_teeth = "Verified"
                    print("Verified (Teeth)")
                    print(f"Label (Teeth): {label_teeth}")
                    print(f"Confidence (Teeth): {confidence_teeth * 100}")
                    counter_correct += 1
                    print("counter_correct - " + str(counter_correct))
                    cv2.rectangle(im, (x-22, y-90), (x+w+22, y-22), (255, 255, 255), -1)
                    cv2.putText(im, str(label_teeth), (x, y-40), font, 1, (0, 0, 0), 2)

        if counter_wrong == 5:
            pyautogui.moveTo(48, 748)
            pyautogui.click(48, 748)
            pyautogui.typewrite("Hello Stranger!!! What's Up.")
            cam.release()
            cv2.destroyAllWindows()
            ctypes.windll.user32.LockWorkStation()
            sys.exit()

        if counter_correct == 20:
            cam.release()
            cv2.destroyAllWindows()
            sys.exit()

    cv2.imshow('Webcam', im)

    if cv2.waitKey(10) & 0xFF == ord('*'):
        break

cam.release()
cv2.destroyAllWindows()
