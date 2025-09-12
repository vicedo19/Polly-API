import requests
from typing import Dict, Optional

def vote_on_poll(base_url: str, poll_id: int, option_id: int, access_token: str) -> Dict:
    """
    Cast a vote on an existing poll.
    
    Args:
        base_url (str): The base URL of the API (e.g., 'http://localhost:8000')
        poll_id (int): The ID of the poll to vote on
        option_id (int): The ID of the option to vote for
        access_token (str): JWT access token for authentication
    
    Returns:
        Dict: The vote response containing:
            - id (int): Vote ID
            - user_id (int): ID of the user who voted
            - option_id (int): ID of the selected option
            - created_at (str): Vote timestamp in ISO format
    
    Raises:
        requests.exceptions.RequestException: If the request fails
        ValueError: If the server returns an error response
    """
    # Prepare the endpoint URL
    url = f"{base_url.rstrip('/')}/polls/{poll_id}/vote"
    
    # Prepare the request payload
    payload = {
        "option_id": option_id
    }
    
    # Set headers for JSON content and authentication
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        # Make the POST request
        response = requests.post(url, json=payload, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            raise ValueError("Unauthorized: Invalid or expired access token")
        elif response.status_code == 404:
            raise ValueError(f"Poll with ID {poll_id} not found or option with ID {option_id} not found")
        else:
            response.raise_for_status()
            
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"Failed to cast vote: {e}")

def login_and_vote(base_url: str, username: str, password: str, poll_id: int, option_id: int) -> Dict:
    """
    Convenience function that logs in a user and casts a vote in one operation.
    
    Args:
        base_url (str): The base URL of the API
        username (str): Username for authentication
        password (str): Password for authentication
        poll_id (int): The ID of the poll to vote on
        option_id (int): The ID of the option to vote for
    
    Returns:
        Dict: The vote response
    
    Raises:
        requests.exceptions.RequestException: If any request fails
        ValueError: If login fails or voting fails
    """
    # First, log in to get the access token
    login_url = f"{base_url.rstrip('/')}/login"
    login_data = {
        "username": username,
        "password": password
    }
    login_headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    try:
        # Make login request
        login_response = requests.post(login_url, data=login_data, headers=login_headers)
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            access_token = token_data["access_token"]
        elif login_response.status_code == 400:
            raise ValueError("Login failed: Incorrect username or password")
        else:
            login_response.raise_for_status()
        
        # Now cast the vote using the obtained token
        return vote_on_poll(base_url, poll_id, option_id, access_token)
        
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"Failed to login and vote: {e}")

# Example usage
if __name__ == "__main__":
    try:
        # Method 1: Vote with existing access token
        # (Assuming you already have a token from a previous login)
        # vote_result = vote_on_poll(
        #     base_url="http://localhost:8000",
        #     poll_id=1,
        #     option_id=2,
        #     access_token="your_jwt_token_here"
        # )
        # print(f"Vote cast successfully: {vote_result}")
        
        # Method 2: Login and vote in one operation
        vote_result = login_and_vote(
            base_url="http://localhost:8000",
            username="testuser",
            password="testpassword123",
            poll_id=1,
            option_id=2
        )
        print(f"Logged in and voted successfully: {vote_result}")
        
    except ValueError as e:
        print(f"Voting error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")