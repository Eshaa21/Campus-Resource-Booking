
#This ensures all four models are imported together. Alembic needs to know about these model classes to detect their tables.
from app.models.category import Category
from app.models.user import User
from app.models.resource import Resource
from app.models.booking import Booking
