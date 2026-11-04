from fastapi import APIRouter, HTTPException
from app.services.ollama_service import OllamaService
from app.schemas.ollama import GenerateRequest

router = APIRouter()

ollama_service = OllamaService()


@router.get("/ollama/status")
def ollama_status():

    result = ollama_service.check_connection()

    if result["status"] == "disconnected":
        raise HTTPException(
            status_code=503,
            detail=result["message"]
        )

    return result


@router.get("/ollama/models")
def get_ollama_models():

    try:
        models = ollama_service.get_models()

        return {
            "count": len(models),
            "models": models
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

## ollama generate endpoint
@router.post("/ollama/generate")
def generate_response(request: GenerateRequest):

    try:
        result = ollama_service.generate_response(
            prompt=request.prompt,
            model=request.model
        )

        return {
            "status": "success",
            "data": result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )