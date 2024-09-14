from flask import session, redirect, url_for, flash, request

# To make debugging easier
DEBUG_MODE = False

def check_session(role='admin'):
    if DEBUG_MODE:
        print(f"DEBUG_MODE is set to {DEBUG_MODE}")
        print('DEBUG_MODE is enabled. Skipping session check.')
        return None

    try:
        user_logged_in = None
        if 'admin_id' in session:
            user_logged_in = 'admin'
        elif 'user_id' in session:
            user_logged_in = 'user'

        if not user_logged_in:
            flash('You must be logged in to access this page.', 'warning')
            print(f'Not logged in! Session: {session}')
            redirect_url = request.referrer or url_for('main.index')
            print(f"Redirecting to: {redirect_url}")
            return redirect(redirect_url)

        # Check for role conflict only if user is logged in
        return check_role_conflict(role, user_logged_in)
    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'danger')
        print(f"An error occurred: {str(e)}")
        redirect_url = request.referrer or url_for('main.index')
        print(f"Redirecting to: {redirect_url}")
        return redirect(redirect_url)

def check_role_conflict(required_role, logged_in_role):
    if DEBUG_MODE:
        print(f"DEBUG_MODE is set to {DEBUG_MODE}")
        print('DEBUG_MODE is enabled. Skipping role conflict check.')
        return None

    try:
        if required_role == 'admin' and logged_in_role == 'user':
            print('User logged in but trying to access an admin route!', session)
            redirect_url = request.referrer or url_for('user_dashboard.user_dashboard')
            print(f"Redirecting to: {redirect_url}")
            return redirect(redirect_url)
        
        if required_role == 'user' and logged_in_role == 'admin':
            print('Admin logged in but trying to access a user route!', session)
            redirect_url = request.referrer or url_for('admin_dashboard.admin_dashboard')
            print(f"Redirecting to: {redirect_url}")
            return redirect(redirect_url)
    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'danger')
        print(f"An error occurred: {str(e)}")
        redirect_url = request.referrer or url_for('main.index')
        print(f"Redirecting to: {redirect_url}")
        return redirect(redirect_url)

def check_access(role='admin'):
    response = check_session(role)
    if response:
        return response

    return None
