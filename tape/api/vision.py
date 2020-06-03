from google.cloud.vision_v1 import ImageAnnotatorClient, enums, types


def detect_faces(face_content: bytes):
    client = ImageAnnotatorClient()

    image = types.Image(content=face_content)
    results = client.face_detection(image=image)
    return results.face_annotations
