from typing import Optional
from datetime import datetime
from pydantic import BaseModel,Field
import uuid

class ReviewModel(BaseModel):
    uid: uuid.UUID
    rating: int = Field(lt=5)
    review_text: str
    user_uid: Optional[uuid.UUID] 
    book_uid: Optional[uuid.UUID] 
    updated_at: datetime
    
class ReviewCreateModel(BaseModel):
    rating: int = Field(lt=5)
    review_text: str
    