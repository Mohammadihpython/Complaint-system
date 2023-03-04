import os
import uuid

from constants import TEMP_FILE_FOLDER
from db import database
from models import complaint, RoleType, State
from services.s3 import S3Service
from utils.helpers import decode_photo

s3 = S3Service()


class ComplaintManager:
    @staticmethod
    async def get_complaints(user):
        """get user complaints only"""
        query = complaint.select()
        if user["role"] == RoleType.complainer:
            query = query.where(complaint.c.complainer_id == user["id"])
        elif user["role"] == RoleType.approver:
            query = query.where(complaint.c.state == State.pending)
        return await database.fetch_all(query)

    @staticmethod
    async def create_complaint(complaint_data, user):
        complaint_data["complainer_id"] = user["id"]
        encoded_photo = complaint_data.pop("encoded_photo", None)
        extension = complaint_data.pop("extension", None)
        name = f"{uuid.uuid4()}.{extension}"
        path = os.path.join(TEMP_FILE_FOLDER, name)
        decode_photo(path, encoded_photo)
        complaint_data["photo_url"] = s3.upload(path, key=name, ext=extension)
        os.remove(path)
        id_ = await database.execute(complaint.insert().values(complaint_data))
        return await database.fetch_one(complaint.select().where(complaint.c.id == id_))

    @staticmethod
    async def delete(complaint_id):
        await database.execute(complaint.delete().where(complaint.c.id == complaint_id))

    @staticmethod
    async def approve(id_):
        await database.execute(
            complaint.update()
            .where(complaint.c.id == id_)
            .values(status=State.approved)
        )

    @staticmethod
    async def reject(id_):
        await database.execute(
            complaint.update()
            .where(complaint.c.id == id_)
            .values(status=State.rejected)
        )
