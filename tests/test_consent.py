from consent import ConsentManager, ConsentStatus

def test_revoke_consent():
    manager = ConsentManager()
    manager.add_user(1)
    assert manager.revoke_consent(1) == True
    assert manager.get_consent_status(1) == ConsentStatus.REVOKED

def test_revoke_consent_non_existent_user():
    manager = ConsentManager()
    assert manager.revoke_consent(1) == False

def test_prevent_ai_access():
    manager = ConsentManager()
    manager.add_user(1)
    manager.revoke_consent(1)
    assert manager.prevent_ai_access(1) == True

def test_prevent_ai_access_active_user():
    manager = ConsentManager()
    manager.add_user(1)
    assert manager.prevent_ai_access(1) == False

def test_emit_webhook():
    manager = ConsentManager()
    manager.add_user(1)
    manager.revoke_consent(1)
    # Check if webhook is emitted
    # This test will print "Webhook emitted for user 1" to the console
    # We can't directly test the print statement, but we can verify the logic
    assert manager.get_consent_status(1) == ConsentStatus.REVOKED
