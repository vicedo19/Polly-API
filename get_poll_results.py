import requests
from typing import Dict, List, Any, Optional


def get_poll_results(base_url: str, poll_id: int) -> Optional[Dict[str, Any]]:
    """
    Retrieve poll results from the API.
    
    Args:
        base_url (str): The base URL of the API (e.g., "http://localhost:8000")
        poll_id (int): The ID of the poll to get results for
    
    Returns:
        Dict containing poll results with structure:
        {
            "poll_id": int,
            "question": str,
            "results": [
                {
                    "option_id": int,
                    "text": str,
                    "vote_count": int
                }
            ]
        }
        Returns None if an error occurs.
    
    Raises:
        requests.RequestException: For network-related errors
    """
    try:
        # Construct the URL
        url = f"{base_url.rstrip('/')}/polls/{poll_id}/results"
        
        # Make the GET request
        response = requests.get(url)
        
        # Handle different response status codes
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print(f"Error: Poll with ID {poll_id} not found")
            return None
        else:
            print(f"Error: Unexpected status code {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to {base_url}")
        return None
    except requests.exceptions.Timeout:
        print("Error: Request timed out")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error: Request failed - {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def display_poll_results(results: Dict[str, Any]) -> None:
    """
    Display poll results in a formatted way.
    
    Args:
        results (Dict): The poll results dictionary from get_poll_results()
    """
    if not results:
        print("No results to display")
        return
    
    print(f"\nPoll Results for Poll ID: {results['poll_id']}")
    print(f"Question: {results['question']}")
    print("\nResults:")
    print("-" * 50)
    
    total_votes = sum(option['vote_count'] for option in results['results'])
    
    for option in results['results']:
        vote_count = option['vote_count']
        percentage = (vote_count / total_votes * 100) if total_votes > 0 else 0
        
        print(f"Option {option['option_id']}: {option['text']}")
        print(f"  Votes: {vote_count} ({percentage:.1f}%)")
        print()
    
    print(f"Total votes: {total_votes}")


# Example usage
if __name__ == "__main__":
    # Configuration
    BASE_URL = "http://localhost:8000"
    POLL_ID = 1  # Change this to the poll ID you want to check
    
    # Get poll results
    print(f"Fetching results for poll {POLL_ID}...")
    results = get_poll_results(BASE_URL, POLL_ID)
    
    if results:
        display_poll_results(results)
    else:
        print("Failed to retrieve poll results")
    
    # Example of checking multiple polls
    print("\n" + "="*60)
    print("Checking multiple polls:")
    
    for poll_id in [1, 2, 3]:
        print(f"\nChecking poll {poll_id}:")
        results = get_poll_results(BASE_URL, poll_id)
        if results:
            total_votes = sum(option['vote_count'] for option in results['results'])
            print(f"  Question: {results['question']}")
            print(f"  Total votes: {total_votes}")
        else:
            print(f"  Poll {poll_id} not found or error occurred")