import face_recognition
import numpy as np
from fastapi import UploadFile, HTTPException
from app.core.security import hash_descriptor

class FaceService:
    @staticmethod
    async def extract_descriptor(file: UploadFile) -> dict:
        image = face_recognition.load_image_file(file.file)
        encodings = face_recognition.face_encodings(image, num_jitters=2) # More accurate

        if not encodings:
            raise HTTPException(status_code=400, detail="No face detected in image")
        if len(encodings) > 1:
            raise HTTPException(status_code=400, detail="Multiple faces detected")

        descriptor = encodings[0].tolist()
        return {
            "descriptor": descriptor,
            "hash": hash_descriptor(descriptor),
            "quality": "high" if len(encodings[0]) == 128 else "low"
        }

    @staticmethod
    def compare_faces(stored_desc: list, file: UploadFile, tolerance: float = 0.6) -> dict:
        new_img = face_recognition.load_image_file(file.file)
        new_enc = face_recognition.face_encodings(new_img)

        if not new_enc:
            return {"match": False, "reason": "No face in verification image"}

        distance = np.linalg.norm(np.array(stored_desc) - np.array(new_enc[0]))
        return {
            "match": distance <= tolerance,
            "distance": round(float(distance), 4),
            "confidence": round(float(1 - distance), 4)
        }
