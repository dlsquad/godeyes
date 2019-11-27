import aiofiles

from .base import Base

class Picture(Base):

    def __init__(self):
        pass

    async def post_picture(self, request):
        pass
        
    async def get_picture(self, request, picture_id):
        pass

    async def put_picture(self, request, picture_id):
        pass

    async def insert(self, ):
        sql = "INSERT INTO picture()"
        pass

