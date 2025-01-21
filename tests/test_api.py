import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_generate_sql(client):
    # Test data
    test_data = {
        "question": "What are the distinct ages of the heads who are acting?",
        "schema": """
        Table department has columns: Department_ID (number), Name (text), Creation (text), Ranking (number), Budget_in_Billions (number), Num_Employees (number)
        Table head has columns: head_ID (number), name (text), born_state (text), age (number)
        Table management has columns: department_ID (number), head_ID (number), temporary_acting (text)
        Column head_ID references column head_ID
        Column department_ID references column Department_ID
        Column Department_ID is a primary key
        Column head_ID is a primary key
        Column department_ID is a primary key
        """
    }

    # Make a POST request to the API
    response = client.post("/generate-sql", json=test_data)

    # Assert the response status code
    assert response.status_code == 200, "API failed to return a valid response."

    # Assert the response contains a SQL query
    assert "sql_query" in response.json(), "Response does not contain a SQL query."
    assert response.json()["sql_query"].strip() != "", "Generated SQL query is empty."