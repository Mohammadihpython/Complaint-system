from db import database
from models import complaint, RoleType, State


class ComplaintManager:
    @staticmethod
    async def get_complaints(user):
        """ get user complaints only"""
        query = complaint.select()
        if user["role"] == RoleType.complainer:
            query = query.where(complaint.c.complainer_id == user["id"])
        elif user["role"] == RoleType.approver:
            query = query.where(complaint.c.state == State.pending)
        return await database.fetch_all(query)

    @staticmethod
    async def create_complaint(complaint_data):
        id_ = await  database.execute(complaint.insert().values(complaint_data))
        return await database.fetch_one(complaint.select().where(complaint.c.id == id_))
