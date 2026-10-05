from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import Resource
from app.schemas.resource import ResourceCreate

router = APIRouter(prefix="/resources", tags=["Resources"])


@router.post("/")
def create_resource(
    resource: ResourceCreate,
    db: Session = Depends(get_db),
):
    new_resource = Resource(
        name=resource.name,
        description=resource.description,
        location=resource.location,
        capacity=resource.capacity,
        category_id=resource.category_id,
    )

    db.add(new_resource)
    db.commit()
    db.refresh(new_resource)

    return new_resource


@router.get("/")
def get_resources(db: Session = Depends(get_db)):
    return db.query(Resource).all()
