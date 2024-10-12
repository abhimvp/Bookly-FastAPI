from src.db.models import User
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from .schemas import UserCreateModel
from .utils import generate_password_hash, verify_password


class UserService:

    async def get_user_by_email(self, email: str, session: AsyncSession):
        """check user by email"""
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        user = result.first()
        return user

    async def user_exits(self, email: str, session: AsyncSession):
        """Check whether a user exist or not in our database"""
        user = await self.get_user_by_email(email=email, session=session)
        return True if user is not None else False

    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        """Create a new user"""
        user_data_dictionary = user_data.model_dump()
        new_user = User(**user_data_dictionary)
        new_user.password_hash = generate_password_hash(
            user_data_dictionary["password"]
        )
        new_user.role = "user"  # add this within token that we provide to each user
        session.add(new_user)
        await session.commit()
        return new_user
