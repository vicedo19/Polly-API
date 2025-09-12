import requests
from typing import List, Dict, Optional

def fetch_polls(base_url: str, skip: int = 0, limit: int = 10) -> List[Dict]:
    """
    Fetch paginated poll data from the /polls endpoint.
    
    Args:
        base_url (str): The base URL of the API (e.g., 'http://localhost:8000')
        skip (int): Number of items to skip (default: 0)
        limit (int): Maximum number of items to return (default: 10)
    
    Returns:
        List[Dict]: List of poll objects, each containing:
            - id (int): Poll ID
            - question (str): Poll question
            - created_at (str): Creation timestamp in ISO format
            - owner_id (int): ID of the poll owner
            - options (List[Dict]): List of poll options with id, text, and poll_id
    
    Raises:
        requests.exceptions.RequestException: If the request fails
        ValueError: If the server returns an error response
    """
    # Prepare the endpoint URL with query parameters
    url = f"{base_url.rstrip('/')}/polls"
    
    # Prepare query parameters
    params = {
        "skip": skip,
        "limit": limit
    }
    
    try:
        # Make the GET request
        response = requests.get(url, params=params)
        
        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
            
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"Failed to fetch polls: {e}")

def fetch_all_polls(base_url: str, page_size: int = 10) -> List[Dict]:
    """
    Fetch all polls by automatically handling pagination.
    
    Args:
        base_url (str): The base URL of the API
        page_size (int): Number of items per page (default: 10)
    
    Returns:
        List[Dict]: Complete list of all polls
    
    Raises:
        requests.exceptions.RequestException: If any request fails
    """
    all_polls = []
    skip = 0
    
    while True:
        # Fetch a page of polls
        polls_page = fetch_polls(base_url, skip=skip, limit=page_size)
        
        # If no polls returned, we've reached the end
        if not polls_page:
            break
            
        # Add polls to our collection
        all_polls.extend(polls_page)
        
        # If we got fewer polls than requested, we've reached the end
        if len(polls_page) < page_size:
            break
            
        # Move to next page
        skip += page_size
    
    return all_polls

# Example usage
if __name__ == "__main__":
    try:
        # Fetch first 10 polls
        polls = fetch_polls(
            base_url="http://localhost:8000",
            skip=0,
            limit=10
        )
        print(f"Fetched {len(polls)} polls:")
        for poll in polls:
            print(f"- Poll {poll['id']}: {poll['question']} ({len(poll['options'])} options)")
        
        # Fetch all polls with automatic pagination
        print("\nFetching all polls...")
        all_polls = fetch_all_polls("http://localhost:8000")
        print(f"Total polls found: {len(all_polls)}")
        
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")