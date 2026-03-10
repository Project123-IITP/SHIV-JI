import cv2
import os
from datetime import datetime


def AuthenticateFace():

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("engine/auth/trainer/trainer.yml")

    faceCascade = cv2.CascadeClassifier(
        "engine/auth/haarcascade_frontalface_default.xml"
    )

    font = cv2.FONT_HERSHEY_SIMPLEX

    names = ["", "Ravikant"]

    cam = cv2.VideoCapture(0)

    unknown_count = 0

    while True:

        ret, img = cam.read()

        if not ret:
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(100, 100),
        )

        for (x, y, w, h) in faces:

            id, distance = recognizer.predict(gray[y:y+h, x:x+w])

            accuracy = 100 - distance

            print("Accuracy:", accuracy)

            # draw face box
            cv2.rectangle(img, (x, y), (x+w, y+h), (0,255,0), 2)

            # progress bar width
            bar_width = int(accuracy * 2)

            cv2.rectangle(img, (50, 400), (50 + bar_width, 430), (0,255,0), -1)
            cv2.rectangle(img, (50, 400), (450, 430), (255,255,255), 2)

            cv2.putText(
                img,
                f"Scanning Face: {accuracy:.1f}%",
                (50, 390),
                font,
                0.8,
                (0,255,0),
                2
            )

            if accuracy > 50:

                name = names[id]

                cv2.putText(
                    img,
                    f"{name} {accuracy:.1f}%",
                    (x, y-10),
                    font,
                    0.8,
                    (0,255,0),
                    2
                )

                cv2.imshow("Face Authentication", img)

                cv2.waitKey(1500)

                cam.release()
                cv2.destroyAllWindows()

                return 1

            else:

                unknown_count += 1

                cv2.putText(
                    img,
                    f"Unknown {accuracy:.1f}%",
                    (x, y-10),
                    font,
                    0.8,
                    (0,0,255),
                    2
                )

                if unknown_count >= 5:

                    if not os.path.exists("intruders"):
                        os.makedirs("intruders")

                    filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"

                    cv2.imwrite(f"intruders/{filename}", img)

                    print("Intruder detected. Photo saved.")

                    cam.release()
                    cv2.destroyAllWindows()

                    return 0

        cv2.imshow("Face Authentication", img)

        if cv2.waitKey(10) & 0xff == 27:
            break

    cam.release()
    cv2.destroyAllWindows()

    return 0