import pytest
from consent_form import create_consent_form, create_data_category, ConsentFormDatabase

def test_create_consent_form():
    ai_service = "AI Service 1"
    data_categories = [create_data_category("Category 1", "Description 1"), create_data_category("Category 2", "Description 2")]
    consent_form = create_consent_form(ai_service, data_categories)
    assert consent_form.ai_service == ai_service
    assert len(consent_form.data_categories) == 2

def test_toggle_data_category():
    ai_service = "AI Service 1"
    data_categories = [create_data_category("Category 1", "Description 1"), create_data_category("Category 2", "Description 2")]
    consent_form = create_consent_form(ai_service, data_categories)
    assert consent_form.data_categories[0].enabled is None  # default is None
    consent_form.toggle_data_category("Category 1", True)
    assert consent_form.data_categories[0].enabled is True

def test_submit_consent_form():
    ai_service = "AI Service 1"
    data_categories = [create_data_category("Category 1", "Description 1"), create_data_category("Category 2", "Description 2")]
    consent_form = create_consent_form(ai_service, data_categories)
    consent_form.toggle_data_category("Category 1", True)
    consent_form.toggle_data_category("Category 2", False)
    consent_record = consent_form.submit()
    assert consent_record["ai_service"] == ai_service
    assert len(consent_record["data_categories"]) == 2
    assert consent_record["data_categories"][0]["enabled"] is True
    assert consent_record["data_categories"][1]["enabled"] is False

def test_store_consent_record():
    consent_database = ConsentFormDatabase()
    ai_service = "AI Service 1"
    data_categories = [create_data_category("Category 1", "Description 1"), create_data_category("Category 2", "Description 2")]
    consent_form = create_consent_form(ai_service, data_categories)
    consent_form.toggle_data_category("Category 1", True)
    consent_form.toggle_data_category("Category 2", False)
    consent_record = consent_form.submit()
    consent_database.store_consent_record(consent_record)
    assert len(consent_database.consent_records) == 1
    assert consent_database.consent_records[0] == consent_record
