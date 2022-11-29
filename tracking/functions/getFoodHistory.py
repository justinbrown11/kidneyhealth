# Import dependencies

def getFoodHistory(userId) -> dict:
    """
    Gets all food ordered by user by user id
    \n
    Params:
    - userId | INTEGER
    \n
    Returns:
    - Response object with data attached
    """
    
    try:
        # Get all foods from users
        foods = ()

        # Return response
        return {
            "result": 0,
            "msg": "Success",
            "data": foods
        }

    except Exception as e:

        # Log error
        print(e)

        # Return error response
        return {
            "result": 1,
            "msg": "Error occured in getFoodHistory"
        }