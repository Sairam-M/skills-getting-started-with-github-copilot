"""Tests for FastAPI routes."""


def test_root_redirect(client):
    """Test root endpoint redirects to static index."""
    response = client.get("/")
    assert response.status_code == 307  # RedirectResponse default
    assert response.headers["location"] == "/static/index.html"


def test_get_activities(client):
    """Test getting all activities returns correct structure."""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "description" in data["Chess Club"]
    assert "schedule" in data["Chess Club"]
    assert "max_participants" in data["Chess Club"]
    assert "participants" in data["Chess Club"]
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_success(client):
    """Test successful signup for an activity."""
    email = "test@student.edu"
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity}"}

    # Verify added to participants
    response2 = client.get("/activities")
    data = response2.json()
    assert email in data[activity]["participants"]


def test_signup_activity_not_found(client):
    """Test signup fails if activity does not exist."""
    response = client.post("/activities/Nonexistent Activity/signup?email=test@test.com")
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_already_signed_up(client):
    """Test signup fails if student already signed up."""
    email = "duplicate@test.com"
    activity = "Programming Class"
    # First signup
    client.post(f"/activities/{activity}/signup?email={email}")
    # Second attempt
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}


def test_unregister_success(client):
    """Test successful unregister from an activity."""
    email = "unregister@test.com"
    activity = "Gym Class"
    # First signup
    client.post(f"/activities/{activity}/signup?email={email}")
    # Then unregister
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity}"}

    # Verify removed
    response2 = client.get("/activities")
    data = response2.json()
    assert email not in data[activity]["participants"]


def test_unregister_activity_not_found(client):
    """Test unregister fails if activity does not exist."""
    response = client.post("/activities/Nonexistent Activity/unregister?email=test@test.com")
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_not_signed_up(client):
    """Test unregister fails if student not signed up."""
    email = "notsigned@test.com"
    activity = "Basketball Team"
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 400
    assert response.json() == {"detail": "Student not signed up for this activity"}