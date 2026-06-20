import json
from consent_form import ConsentForm, DataCategory

def test_consent_form_submission():
    data_categories = [DataCategory("category1", True), DataCategory("category2", False)]
    consent_form = ConsentForm("ai_service_name", data_categories)
    consent_record = consent_form.submit()
    assert json.loads(consent_record) == {
        "ai_service_name": "ai_service_name",
        "data_categories": [
            {"name": "category1", "enabled": True},
            {"name": "category2", "enabled": False},
        ],
    }

def test_toggle_data_category():
    data_categories = [DataCategory("category1", True), DataCategory("category2", False)]
    consent_form = ConsentForm("ai_service_name", data_categories)
    consent_form.toggle_data_category("category1")
    assert consent_form.get_data_categories() == [
        DataCategory("category1", False),
        DataCategory("category2", False),
    ]

def test_get_data_categories():
    data_categories = [DataCategory("category1", True), DataCategory("category2", False)]
    consent_form = ConsentForm("ai_service_name", data_categories)
    assert consent_form.get_data_categories() == data_categories

def test_empty_data_categories():
    consent_form = ConsentForm("ai_service_name", [])
    assert consent_form.get_data_categories() == []
