import requests
from typing import Dict, Optional

def register_user(base_url: str, username: str, password: str) -> Dict:
    """
    Register a new user via the /register endpoint.
    
    Args:
        base_url (str): The base URL of the API (e.g., 'http://localhost:8000')
        username (str): The username for the new user
        password (str): The password for the new user
    
    Returns:
        Dict: The response from the server containing user information
    
    Raises:
        requests.exceptions.RequestException: If the request fails
        ValueError: If the server returns an error response
    """
    # Prepare the endpoint URL
    url = f"{base_url.rstrip('/')}/register"
    
    # Prepare the request payload
    payload = {
        "username": username,
        "password": password
    }
    
    # Set headers for JSON content
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        # Make the POST request
        response = requests.post(url, json=payload, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            raise ValueError(f"Registration failed: Username '{username}' already registered")
        else:
            response.raise_for_status()
            
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"Failed to register user: {e}")

# Example usage
if __name__ == "__main__":
    try:
        # Register a new user
        result = register_user(
            base_url="http://localhost:8000",
            username="testuser",
            password="testpassword123"
        )
        print(f"User registered successfully: {result}")
        
    except ValueError as e:
        print(f"Registration error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")