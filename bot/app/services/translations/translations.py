import json
import os
from typing import Dict
from database.redis import get_redis


async def set_user_language(user_id:int, lang_code:str)->None:
        redis = await get_redis()
        await redis.set(f"user:{user_id}:language", lang_code)

def load_translations() -> Dict[str, Dict[str, str]]:
        """
        Load translations from a JSON file.
        """
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, 'translations.json')
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)