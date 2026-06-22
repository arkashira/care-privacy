from consent_management import ConsentManagement, ConsentRecord
from datetime import datetime
import pytest

def test_add_consent_record():
    management = ConsentManagement()
    record = ConsentRecord("user1", "consent1", datetime(2022, 1, 1), "policy1", "active")
    management.add_consent_record(record)
    assert len(management.get_consent_records()) == 1

def test_get_consent_records():
    management = ConsentManagement()
    record1 = ConsentRecord("user1", "consent1", datetime(2022, 1, 1), "policy1", "active")
    record2 = ConsentRecord("user2", "consent2", datetime(2022, 1, 2), "policy2", "active")
    management.add_consent_record(record1)
    management.add_consent_record(record2)
    records = management.get_consent_records()
    assert len(records) == 2
    assert records[0].user_id == "user1"
    assert records[1].user_id == "user2"

def test_revoke_consent():
    management = ConsentManagement()
    record = ConsentRecord("user1", "consent1", datetime(2022, 1, 1), "policy1", "active")
    management.add_consent_record(record)
    management.revoke_consent("consent1")
    records = management.get_consent_records()
    assert records[0].status == "revoked"

def test_revoke_consent_not_found():
    management = ConsentManagement()
    with pytest.raises(ValueError):
        management.revoke_consent("consent1")

def test_log_event():
    management = ConsentManagement()
    management.log_event("test event")
    # No assertion, just checking that it runs without error
