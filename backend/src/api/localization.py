from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.src.database.database import get_db
from backend.src.models import orm, localization
from backend.src.services import auth_service, localization_service

router = APIRouter(prefix="/translate", tags=["localization"])

@router.post("/", response_model=localization.TranslateResponse)
async def translate_content(
    request: localization.TranslateRequest, 
    current_user: orm.Student = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    """
    Translates a specific block of text for the currently logged-in user.
    """
    translated_text = localization_service.translate_text(request.text, request.target_language)
    
    return localization.TranslateResponse(
        translated_text=translated_text,
        original_text=request.text,
        language=request.target_language
    )
