from app.permissions import is_allowed

def test_hr_allowed():
    assert is_allowed("HR", "HR,Manager") is True

def test_finance_blocked():
    assert is_allowed("Finance", "HR,Manager") is False