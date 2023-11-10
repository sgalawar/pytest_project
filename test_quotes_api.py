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
        
        # Store data from dictionary
        response_data = response_data.get("data")
        
        # Check for sorted by ID
        assert all(response_data[i]['id'] < response_data[i + 1]['id'] for i in range(len(response_data) - 1)), "Quotes are not sorted by ID"
        
        # Check for duplicates
        assert len(response_data) == len(set(quote["id"] for quote in response_data)), "Duplicate IDs found"

        # Display quotes
        print(f"\n\nQuotes in JSON format from GET /quotes:\n\n {response_data}")
        
        return response_data

    # POST /quotes
    def add_quote(self, text):
        
        # Check for STRING INPUT else return error 400
        assert isinstance(text, str), "400 Bad Request - Invalid text format"
        
        # Check for EMPTY FIELD else return error 400
        assert len(text) > 0, "400 Bad Request - Text cannot be empty"
        
        # Make a GET request to retrieve current list of quotes
        previous_get_response = self.session.get(f"{self.base_url}/quotes")
        
        # Store JSON data
        previous_get_response_data = previous_get_response.json()
        
        # Verify OLD quotes were retrieved
        assert previous_get_response_data.get("ok") is True, "Failed to retrieve quote"
        
        # Store OLD quotes' IDs 
        previous_ids_list = [item["id"] for item in previous_get_response_data.get("data")]
        
        # Make a POST request to add a new quote
        post_response = self.session.post(f"{self.base_url}/quotes", json={"text": text})
        
        # Store JSON data
        post_response_data = post_response.json()
        
        # Verify NEW quote addition
        assert post_response_data.get("ok") is True, "Failed to add quote"
        
        # Retrieve UPDATED list of quotes
        new_get_response = self.session.get(f"{self.base_url}/quotes")
        
        # Store JSON data
        new_get_response_data = new_get_response.json()
        
        # Verify NEW UPDATED quotes retrieved
        assert new_get_response_data.get("ok") is True, "Failed request. Possible max capacity reached."
        
        # Store NEW last quote's id
        new_id = max([item["id"] for item in new_get_response_data.get("data")]) # Only works if the new id = new id - 1 (e.g. 9 is the previous ID, and 10 is the new last ID)

        # Store NEW last quote's text
        new_text = next(item["text"] for item in new_get_response_data.get("data") if item["id"] == new_id)
        
        # Verify new quote contains a new ID
        assert new_id not in list(set(previous_ids_list)), "New quote does not have a new ID"
        
        # Verify new quote contains the new input text corresponding to its new assigned ID
        assert new_text == text, f"Text mismatch: {new_text} != {text}"
        
        return new_get_response_data
        
    # GET /quotes/<id>
    def get_quote_by_id(self, quote_id):
        
        # Make a GET request to fetch a specific quote by ID
        quote_response = self.session.get(f"{self.base_url}/quotes/{quote_id}")
        
        # Store JSON data
        quote_response_data = quote_response.json()
        
        # Verify quote retrieval
        assert quote_response_data.get("ok") is True, f"404 Not Found - Quote with ID {quote_id} not found"
        
        # Store text requested by ID
        quote_by_id = quote_response_data.get("data").get("text")
        
        # Make a GET request to fetch all quotes
        all_response = self.session.get(f"{self.base_url}/quotes")
        
        # Store JSON
        all_response_data = all_response.json()
        
        # Store text by ID from dictionary of all quotes (response_data)
        quote_from_all = next(quote["text"] for quote in all_response_data["data"] if quote["id"] == quote_id)
        
        # Verify text of quote by ID matches quote from GET /quotes
        assert quote_by_id == quote_from_all, "Text retrieved by ID does not match text in API list"
        
        # Store quote
        quote_object = quote_response_data.get("data")
        
        # Display object [id, text]
        print(f"\nRequested quote: {quote_object}\n")
        
        return quote_object
    
    # DELETE /quotes/<id>
    def delete_quote_by_id(self, quote_id):
        
        # Make a DELETE request to remove a specific quote
        response = self.session.delete(f"{self.base_url}/quotes/{quote_id}")
        
        # Store JSON
        response_data = response.json()
        
        # Verify quote deletion
        assert response_data.get("ok") is True, f"404 Not Found - Quote with ID {quote_id} not found"
        
        # Store data
        deleted_quote = response_data.get("data")
        
        # Print retrieved data from API (data should be None/Null)
        print(f"\nDeleted quote '{quote_id}' data: {deleted_quote}\n")

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
    print("Beginning of 1st set of tests: Retrieved data should be sorted by id & without duplicates for at least 12 quotes.")
    print("\n\nBEFORE POSTING NEW QUOTES")
    api_client.get_quotes()
    api_client.add_quote("Mambo number 4")
    api_client.add_quote("Mambo number 5")
    api_client.add_quote("Mambo number 6")
    api_client.add_quote("Mambo number 7")
    api_client.add_quote("Mambo number 8")
    api_client.add_quote("Mambo number 9")
    api_client.add_quote("Mambo number 10") # AssertionError
    api_client.add_quote("Mambo number 11") # AssertionError
    api_client.add_quote("Mambo number 12") # AssertionError
    print("\n\nAFTER POSTING NEW QUOTES")
    api_client.get_quotes()
    print("\n\nEnd of 1st set of tests.")


def test_add_quote(api_client):
    print("Beginning of 2nd set of tests: User can add a new code with personalized text. Added quote should be a non-empty string.\n"
          "Response data should contain a new ID with its corresponding text. Verify that API can store at least 20 quotes.")
    api_client.get_quotes()
    print("\n\nBEFORE POSTING NEW QUOTES")
    api_client.add_quote("Mambo number 4")
    api_client.add_quote("Mambo number 5")
    api_client.add_quote("Mambo number 6")
    api_client.add_quote("Mambo number 7")
    api_client.add_quote("Mambo number 8")
    api_client.add_quote("Mambo number 9")
    api_client.add_quote("Mambo number 10")
    api_client.add_quote("Mambo number 11")
    api_client.add_quote("Mambo number 12")
    api_client.add_quote("Mambo number 13")
    api_client.add_quote("Mambo number 14")
    api_client.add_quote("Mambo number 15")
    api_client.add_quote("Mambo number 16")
    api_client.add_quote("Mambo number 17")
    api_client.add_quote("Mambo number 18")
    api_client.add_quote("Mambo number 19") # AssertionError
    api_client.add_quote("Mambo number 20") # AssertionError
    api_client.add_quote(123)               # AssertionError
    api_client.add_quote("")                # AssertionError
    print("\n\nAFTER POSTING NEW QUOTES")
    api_client.get_quotes()
    print("\n\nEnd of 2nd set of tests.")            

def test_get_quote_by_id(api_client):
    print("Beginning of 3rd set of tests: All quotes are retrievable individually based on their ID, and the text matches.")
    print("\n\nBEFORE POSTING NEW QUOTES")
    api_client.get_quotes()
    api_client.add_quote("Mambo number 4")
    api_client.add_quote("Mambo number 5")
    api_client.add_quote("Mambo number 6")
    api_client.add_quote("Mambo number 7")
    api_client.add_quote("Mambo number 8")
    api_client.add_quote("Mambo number 9")
    api_client.add_quote("Mambo number 10")
    api_client.get_quote_by_id(5)
    api_client.get_quote_by_id(10)
    api_client.get_quote_by_id(11) # AssertionError
    print("\nAFTER POSTING NEW QUOTES")
    api_client.get_quotes()
    print("\n\nEnd of 3rd set of tests.")


def test_delete_quote_by_id(api_client):
    print("Beginning of 4th set of tests: Removing quotes should succeed and subsequent attempts reply with code 404. No longer shows up in GET /quotes after deletion.")
    print("\n\nBEFORE POSTING NEW QUOTES")
    api_client.get_quotes()
    api_client.add_quote("Mambo number 4")
    api_client.add_quote("Mambo number 5")
    api_client.delete_quote_by_id(2)
    api_client.delete_quote_by_id(4)
    api_client.delete_quote_by_id(4) # AssertionError
    print("\nAFTER POSTING NEW QUOTES & DELETION")
    api_client.get_quotes()
    print("\n\nEnd of 4th set of tests.")