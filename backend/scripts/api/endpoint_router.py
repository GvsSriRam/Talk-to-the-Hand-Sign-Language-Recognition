from fastapi import APIRouter, File, UploadFile

from log import logger
from api.model_connector import ModelConnector

# Contains End_Points that are exposed externally

router = APIRouter()

model_connector_obj = ModelConnector()

@router.get("/train", tags=["split"])
def train_model():
    result = {"success": False, "error": ""}
    try:
        model_connector_obj.train()
        result["success"] = True
    except Exception as e:
        logger.error(str(e))
        result["error"] = str(e)
    return result

@router.post("/pred", tags=["split"])
def prediction(params: dict):
    # print(params)
    # print("\n\n")
    result = {
                "success": False, 
                "pred": None, 
                "error": ""
            }
    try:
        landmarks = params["landmarks"]
        # print(landmarks)
        # print("\n\n")

        # Convert array of landmarks of {x: val, y: val, z: val} to numpy array
        landmarks_np = [[landmark["x"], landmark["y"], landmark["z"]] for landmark in landmarks[0]]
        # print(landmarks_np)
        # print("\n\n")

        res = model_connector_obj.predict(landmarks_np)
        result["pred"] = res
        result["success"] = True
    except Exception as e:
        logger.error(str(e))
        result["error"] = str(e)
    return result
