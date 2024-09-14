from flask import make_response

def disable_caching(response=None):
    """ Utility function to disable caching for a response """
    if response is None:
        response = make_response()
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Cache-Control'] += ', post-check=0, pre-check=0'
    response.headers['Pragma'] = 'no-cache'
    return response
