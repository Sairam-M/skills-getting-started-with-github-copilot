"""Tests for activity data models and business rules."""


def test_activities_initial_structure():
    """Test that initial activities have correct structure."""
    from src.app import activities

    assert isinstance(activities, dict)
    assert len(activities) > 0  # Has some activities

    for name, activity in activities.items():
        assert isinstance(name, str)
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
        assert isinstance(activity["description"], str)
        assert isinstance(activity["schedule"], str)
        assert isinstance(activity["max_participants"], int)
        assert isinstance(activity["participants"], list)
        assert activity["max_participants"] > 0
        # Participants should be list of strings (emails)
        for email in activity["participants"]:
            assert isinstance(email, str)
            assert "@" in email  # Basic email check


def test_activity_participants_uniqueness():
    """Test that participants lists don't have duplicates initially."""
    from src.app import activities

    for name, activity in activities.items():
        participants = activity["participants"]
        assert len(participants) == len(set(participants))  # No duplicates