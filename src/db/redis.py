from redis import asyncio as aioredis
from src.config import Config

ACCESS_TOKEN_EXPIRY = 3600 #JTI expiry

#create redis client object
REDIS_URL = f"redis://{Config.REDIS_HOST}:{Config.REDIS_PORT}"
token_blocklist = aioredis.from_url(REDIS_URL, db=0)
# token_blocklist = aioredis.StrictRedis(host=Config.REDIS_HOST,port=Config.REDIS_PORT,db=0)

# define - two functions - one is to help us add token to blocklist & other is to check if token is in blocklist
async def add_jti_to_blocklist(jti: str) -> None:
     await token_blocklist.set(
         name=jti, value="", ex=ACCESS_TOKEN_EXPIRY
     )

async def token_in_blocklist(jti: str) -> bool:
    return await token_blocklist.get(jti) is not None