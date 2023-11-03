import requests
import pytest

class APIClient:
    
    def __init__(self):
        
        self.base_url = "http://127.0.0.1:6543"
        
        self.session = requests.Session()

    # POST /reset
    def reset_api_state(self):
        
        # Make a POST request to the /reset endpoint with an empty JSON object
        response = self.session.post(f"{self.base_url}/reset", json={})
        
        # Store JSON data
        response_data = response.json()
        
        # Verify API status
        assert response_data.get("ok") is True, "Failed to reset API state"

    # GET /quotes
    def get_quotes(self):
        
        # Retrieve list of quote objects
        response = self.session.get(f"{self.base_url}/quotes")
        
        # Store JSON data
        response_data = response.json()
        
        # Verify quotes retrieval
        assert response_data.get("ok") is True, "Failed to retrieve quotes"
        
        # Sort quotes list by ID
        quotes = sorted(response_data.get("data", []), key=lambda x: x.get("id"))
        
        # Check for at least 12 quotes
        assert len(quotes) >= 12, "Less than 12 quotes found"
        
        # Check for duplicate IDs
        assert len(quotes) == len(set(quote["id"] for quote in quotes)), "Duplicate IDs found"

        # Display quotes
        print(quotes)
        
        return quotes

    # POST /quotes
    def add_quote(self, text):
        
        # Check for STRING INPUT else return error 400
        assert isinstance(text, str), "400 Bad Request - Invalid text format"
        
        # Check for EMPTY FIELD else return error 400
        assert len(text) > 0, "400 Bad Request - Text cannot be empty"
        
        # Make a POST request to add a new quote
        response = self.session.post(f"{self.base_url}/quotes", json={"text": text})
        
        # Store JSON data
        response_data = response.json()
        
        # Verify quote addition
        assert response_data.get("ok") is True, "Failed to add quote"
        
        # Retrieve NEW UPDATED list of quotes
        response = self.session.get(f"{self.base_url}/quotes")
        
        # Store JSON data
        response_data = response.json()
        
        # Verify quotes retrieval
        assert response_data.get("ok") is True, "Failed to retrieve quotes"
        
        # Display updated quotes
        print(response_data.get("data"))
        
        return response_data
        
    # GET /quotes/<id>
    def get_quote_by_id(self, quote_id):
        
        # Make a GET request to fetch a specific quote
        response = self.session.get(f"{self.base_url}/quotes/{quote_id}")
        
        # Store JSON data
        response_data = response.json()
        
        # Verify quote retrieval
        assert response_data.get("ok") is True, f"404 Not Found - Quote with ID {quote_id} not found"
        
        # Return the retrieved quote
        print(response_data.get("data"))
        
        return response_data.get("data")
    
    # DELETE /quotes/<id>
    def delete_quote_by_id(self, quote_id):
        
        # Make a DELETE request to remove a specific quote
        response = self.session.delete(f"{self.base_url}/quotes/{quote_id}")
        
        # Store JSON data
        response_data = response.json()
        
        # Verify quote deletion
        assert response_data.get("ok") is True, f"404 Not Found - Quote with ID {quote_id} not found"
        
        # Print retrieved data from API (data should be None/Null)
        print(response_data)

# Decorator allowing pytest to identify a fixture
@pytest.fixture

def api_client():
    
    # Create an instance of APIClient for each test
    client = APIClient()
    
    # Reset the API state before each test
    client.reset_api_state()

    # Return the client object
    return client


# ALL TESTS ARE BELOW

def test_get_quotes(api_client):
    
    api_client.get_quotes()


def test_add_quote(api_client):
    
    api_client.add_quote("I have a dream")
            

def test_get_quote_by_id(api_client):
    
    api_client.get_quote_by_id(5)


def test_delete_quote_by_id(api_client):
    
    api_client.delete_quote_by_id(3)