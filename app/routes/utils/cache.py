from flask import make_response, request, url_for, redirect

def disable_caching(response=None):
    """ Utility function to disable caching for a response """
    if response is None:
        response = make_response()
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Cache-Control'] += ', post-check=0, pre-check=0'
    response.headers['Pragma'] = 'no-cache'
    return response

def redirect_to(endpoint=None):
    """ Redirect the user to a specified page and disable caching """
    previous_page = url_for(endpoint)
    
    response = make_response(redirect(previous_page))
    
    response = disable_caching(response)
    
    return response
