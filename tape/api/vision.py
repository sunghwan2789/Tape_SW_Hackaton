from google.cloud.vision_v1 import ImageAnnotatorClient, enums, types


def detect_faces(face_content: bytes):
    client = ImageAnnotatorClient()

    image = types.Image(content=face_content)
    results = client.face_detection(image=image)
    return results.face_annotations


def detect_mouths(face_content: bytes):
    for face in detect_faces(face_content):
        yield filter(
            lambda x: x.type
            in (
                enums.FaceAnnotation.Landmark.Type.UPPER_LIP,
                enums.FaceAnnotation.Landmark.Type.LOWER_LIP,
                enums.FaceAnnotation.Landmark.Type.MOUTH_LEFT,
                enums.FaceAnnotation.Landmark.Type.MOUTH_RIGHT,
                enums.FaceAnnotation.Landmark.Type.MOUTH_CENTER,
            ),
            face.landmarks,
        )
