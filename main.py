import mediapipe as mp 
import cv2

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces = 1,
    refine_landmarks = True,
    min_detection_confidence = 0.5,
    min_tracking_confidence = 0.5
)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Kamera Yok !")
        continue

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    result = face_mesh.process(image)

    if result.multi_face_landmarks:
        for face_landmark in result.multi_face_landmarks:
            mp_drawing.draw_landmarks(
                image = image,
                landmark_list = face_landmark,
                connections = mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec = None,
                connection_drawing_spec = mp_drawing_styles.get_default_face_mesh_tesselation_style()
            )
            mp_drawing.draw_landmarks(
                image = image,
                landmark_list = face_landmark,
                connections = mp_face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec = None,
                connection_drawing_spec = mp_drawing_styles.get_default_face_mesh_contours_style()
            )
            mp_drawing.draw_landmarks(
                image = image,
                landmark_list = face_landmark,
                connections = mp_face_mesh.FACEMESH_IRISES,
                landmark_drawing_spec = None,
                connection_drawing_spec = mp_drawing_styles.get_default_face_mesh_iris_connections_style()
            )

    cv2.imshow("TEST", image)
    if cv2.waitKey(5) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()