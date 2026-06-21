import json
from dataclasses import dataclass
from enum import Enum

class ConsentStatus(Enum):
    ACTIVE = "active"
    REVOKED = "revoked"

@dataclass
class User:
    id: int
    consent_status: ConsentStatus

class ConsentManager:
    def __init__(self):
        self.users = {}

    def add_user(self, user_id):
        self.users[user_id] = User(id=user_id, consent_status=ConsentStatus.ACTIVE)

    def revoke_consent(self, user_id):
        if user_id in self.users:
            self.users[user_id].consent_status = ConsentStatus.REVOKED
            self.emit_webhook(user_id)
            return True
        return False

    def emit_webhook(self, user_id):
        # Simulate emitting a webhook
        print(f"Webhook emitted for user {user_id}")

    def get_consent_status(self, user_id):
        if user_id in self.users:
            return self.users[user_id].consent_status
        return None

    def prevent_ai_access(self, user_id):
        if user_id in self.users and self.users[user_id].consent_status == ConsentStatus.REVOKED:
            return True
        return False
