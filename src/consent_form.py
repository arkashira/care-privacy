import json
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class DataCategory:
    name: str
    description: str
    enabled: bool = None  # default is None

@dataclass
class ConsentForm:
    ai_service: str
    data_categories: List[DataCategory]

    def to_dict(self):
        return {
            "ai_service": self.ai_service,
            "data_categories": [{"name": dc.name, "description": dc.description} for dc in self.data_categories]
        }

    def toggle_data_category(self, category_name: str, enabled: bool):
        for dc in self.data_categories:
            if dc.name == category_name:
                dc.enabled = enabled
                break

    def submit(self) -> Dict:
        signed_consent_record = {
            "ai_service": self.ai_service,
            "data_categories": [{"name": dc.name, "description": dc.description, "enabled": dc.enabled} for dc in self.data_categories]
        }
        return signed_consent_record

class ConsentFormDatabase:
    def __init__(self):
        self.consent_records = []

    def store_consent_record(self, consent_record: Dict):
        self.consent_records.append(consent_record)

def create_consent_form(ai_service: str, data_categories: List[DataCategory]) -> ConsentForm:
    return ConsentForm(ai_service, data_categories)

def create_data_category(name: str, description: str) -> DataCategory:
    return DataCategory(name, description)
