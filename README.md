# Quotes API Test Project

This project tests the functionality of a REST API for managing quotes. The API provides endpoints for resetting the state, retrieving quotes, adding new quotes, retrieving quotes by ID, and deleting quotes.

# Prerequisites

- Python 3.11.4 installed on your system. If not, you can download and install it from python.org.

# Setup

1. Clone the Repository:
   ```
    git clone https://github.com/sgalawar/python_project.git
    cd python_project
   ```

3. Create a Virtual Environment:
   ```
    python -m venv venv
   ```

5. Activate the virtual environment:
- On Windows:
  ```
    venv\Scripts\activate
  ```
- On Unix or MacOS:
  ```
    source venv/bin/activate
  ```
4. Install dependencies:
   ```
    pip install -r requirements.txt
   ```

# Running the tests using pytest:
Ensure your virtual environment is activated, and make sure the API server is running and accessible at http://127.0.0.1:6543 before executing the tests. Then, run the following command to execute the tests:
```
    pytest test_quotes_api.py
```
