from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.src.database.database import get_db
from backend.src.models import orm, personalization
from backend.src.services import auth_service, personalization_service

router = APIRouter(prefix="/personalize", tags=["personalization"])

@router.post("/", response_model=personalization.PersonalizeResponse)
async def get_personalized_content(
    request: personalization.PersonalizeRequest, 
    current_user: orm.Student = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    """
    Personalizes a specific block of text for the currently logged-in user.
    """
    personalized_text = personalization_service.personalize_text(request.text, current_user)
    
    return personalization.PersonalizeResponse(
        personalized_text=personalized_text,
        original_text=request.text
    )
