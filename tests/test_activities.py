def test_get_activities_returns_initial_data(client):
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert len(data) == 10  # Assuming 10 activities from the initial data


def test_signup_for_activity_success(client):
    response = client.post("/activities/Chess Club/signup?email=newstudent@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "Signed up newstudent@mergington.edu for Chess Club" in data["message"]

    # Verify the student was added
    response = client.get("/activities")
    activities = response.json()
    assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_for_activity_already_signed_up_raises_400(client):
    # First signup
    client.post("/activities/Chess Club/signup?email=test@mergington.edu")
    
    # Try to signup again
    response = client.post("/activities/Chess Club/signup?email=test@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert "Student already signed up for this activity" in data["detail"]


def test_signup_for_activity_not_found_raises_404(client):
    response = client.post("/activities/Nonexistent Activity/signup?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_unregister_from_activity_success(client):
    # First signup
    client.post("/activities/Chess Club/signup?email=test@mergington.edu")
    
    # Then unregister
    response = client.post("/activities/Chess Club/unregister?email=test@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered test@mergington.edu from Chess Club" in data["message"]

    # Verify the student was removed
    response = client.get("/activities")
    activities = response.json()
    assert "test@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_from_activity_not_registered_raises_404(client):
    response = client.post("/activities/Chess Club/unregister?email=notregistered@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "Student not registered for this activity" in data["detail"]


def test_unregister_from_activity_not_found_raises_404(client):
    response = client.post("/activities/Nonexistent Activity/unregister?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]