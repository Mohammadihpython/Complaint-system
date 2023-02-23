from typing import List

from fastapi import APIRouter, Depends, Request
from managers.complaint import ComplaintManager
from schemas.request.complaint import ComplaintIn
from schemas.response.complaint import ComplaintOut
from managers.auth import oauth2_scheme, is_complainer

router = APIRouter(tags=["complaints"])


@router.get("/complaints/",
            dependencies=[Depends(oauth2_scheme)],
            response_model=List[ComplaintOut])
async def get_complaints(request: Request):
    user = request.state.user
    return await ComplaintManager.get_complaints(user)


@router.post("/complaints", dependencies=[Depends(oauth2_scheme), Depends(is_complainer)])
async def create_complaint(request: Request, complaint: ComplaintIn):
    user = request.state.user
    return await ComplaintManager.create_complaint(complaint.dict(),user)
