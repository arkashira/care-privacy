from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class ConsentRecord:
    user_id: str
    consent_id: str
    timestamp: datetime
    policy: str
    status: str

class ConsentManagement:
    def __init__(self):
        self.consent_records = []

    def add_consent_record(self, record: ConsentRecord):
        self.consent_records.append(record)

    def get_consent_records(self) -> List[ConsentRecord]:
        return self.consent_records

    def revoke_consent(self, consent_id: str):
        for record in self.consent_records:
            if record.consent_id == consent_id:
                record.status = "revoked"
                return
        raise ValueError("Consent ID not found")

    def log_event(self, event: str):
        print(f"Logged event: {event}")
