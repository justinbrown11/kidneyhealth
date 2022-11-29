# Import dependencies
import requests
import environ

# Set env
env = environ.Env()

async def searchFood(query:str) -> dict:
    """
    Searches for food items by keyword and returns list
    \n
    Params:
    - query | query string to search by | STRING
    \n
    Returns:
    - Response object with data attached
    """
    
    try:
        # Set body for request
        payload = { 
            "query": query,
            "api_key": env('FOOD_API_KEY')
        }

        # Send request
        outcome = (requests.get(f"{env('FOOD_API_URL')}/foods/search", params=payload)).json()

        # Return response
        return {
            "result": 0,
            "msg": "Success",
            "data": outcome
        }

    except Exception as e:

        # Log error
        print(e)

        # Return error response
        return {
            "result": 1,
            "msg": "Error occured in searchFood"
        }