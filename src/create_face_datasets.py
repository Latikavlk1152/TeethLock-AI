import cv2
import os
import dlib
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

DATASET_DIR = os.path.join(PROJECT_ROOT, "dataset")
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")

def check_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

def crop_teeth(image, detector, predictor):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    dets = detector(img, 1)

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
        return crop_image

def capture_teeth_dataset(user_id, num_images):
    dataset_folder = DATASET_DIR
    user_folder = os.path.join(dataset_folder, f"user_{user_id}")

    check_path(dataset_folder)
    check_path(user_folder)

    vid_cam = cv2.VideoCapture(0)  # Start video capturing

    cascade_path = os.path.join(MODELS_DIR, "haarcascade_frontalface_default.xml")
    face_cascade = cv2.CascadeClassifier(cascade_path)
    detector = dlib.get_frontal_face_detector()
    landmark_path = os.path.join(MODELS_DIR, "shape_predictor_68_face_landmarks.dat")
    predictor = dlib.shape_predictor(landmark_path)

    count = 0

    while count < num_images:
        ret, image_frame = vid_cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            # Define the region for teeth using facial landmarks
            shape = predictor(gray, dlib.rectangle(x, y, x + w, y + h))

            xteethpoints = [shape.part(xi).x for xi in range(48, 67)]
            yteethpoints = [shape.part(xi).y for xi in range(48, 67)]
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
            cv2.rectangle(image_frame, (x_teeth, y_teeth), (x_teeth + w_teeth, y_teeth + h_teeth), (0, 255, 0), 4)

            teeth_cropped = crop_teeth(image_frame[y:y + h, x:x + w], detector, predictor)

            if teeth_cropped is not None and teeth_cropped.size > 0:
                count += 1
                filename = os.path.join(user_folder, f"User_{user_id}_{count}.jpg")
                cv2.imwrite(filename, teeth_cropped)
                print(f"Captured image {count} for user {user_id}")

                # Display count on camera screen window
                cv2.putText(image_frame, f"Captured: {count}/{num_images}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow('Teeth Capture', image_frame)

        if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to stop
            break
        elif count >= num_images:  # Stop when quota is reached
            break

    vid_cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python create_face_datasets.py <user_name> <user_id>")
        sys.exit(1)

    user_name = sys.argv[1]
    user_id = int(sys.argv[2])
    num_images = 100
    capture_teeth_dataset(user_id, num_images)