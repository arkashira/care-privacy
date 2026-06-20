import json
from dataclasses import dataclass
from typing import List

@dataclass
class DataCategory:
    name: str
    enabled: bool

class ConsentForm:
    def __init__(self, ai_service_name: str, data_categories: List[DataCategory]):
        self.ai_service_name = ai_service_name
        self.data_categories = data_categories

    def toggle_data_category(self, category_name: str):
        for category in self.data_categories:
            if category.name == category_name:
                category.enabled = not category.enabled
                break

    def submit(self) -> str:
        consent_record = {
            "ai_service_name": self.ai_service_name,
            "data_categories": [
                {"name": category.name, "enabled": category.enabled} 
                for category in self.data_categories
            ],
        }
        return json.dumps(consent_record)

    def get_data_categories(self) -> List[DataCategory]:
        return self.data_categories
