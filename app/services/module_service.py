from typing import List
from motor.motor_asyncio import AsyncIOMotorCollection
from fastapi import Depends
from bson import ObjectId
from app.db.mongodb import get_collection
from app.models.module import Module
from app.schemas.module import ModuleCreate, ModuleResponse, ModuleUpdate

class ModuleService:
    def __init__(self, collection: AsyncIOMotorCollection = Depends(lambda: get_collection("modules"))):
        if collection is None:
            raise ValueError("Collection dependency is None")
        self.collection = collection

    async def create_module(self, module_data: ModuleCreate) -> Module:
        module_dict = module_data.dict()
        result = await self.collection.insert_one(module_dict)
        module_dict['id'] = str(result.inserted_id)
        module_dict['course_id'] = ObjectId(module_dict['course_id'])
        return Module(**module_dict)

    async def get_modules(self) -> List[Module]:
        modules = []
        async for module in self.collection.find():
            module['id'] = str(module['_id'])
            module['course_id'] = ObjectId(module['course_id'])
            modules.append(Module(**module))
        return modules

    async def get_module(self, module_id: str) -> Module:
        module = await self.collection.find_one({"_id": ObjectId(module_id)})
        module['id'] = str(module['_id'])
        module['course_id'] = ObjectId(module['course_id'])
        if module:
            return Module(**module)
        return None

    async def update_module(self, module_id: str, module_data: ModuleUpdate) -> ModuleResponse:
        update_data = {"$set": {k: v for k, v in module_data.dict(exclude_unset=True).items() if v is not None}}
        await self.collection.update_one({"_id": ObjectId(module_id)}, update_data)
        updated_module = await self.collection.find_one({"_id": ObjectId(module_id)})
        updated_module['id'] = str(updated_module['_id'])
        updated_module['course_id'] = ObjectId(updated_module['course_id'])
        return Module(**updated_module)

    async def delete_module(self, content_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(content_id)})
        return result.deleted_count == 1