from flask import session, redirect, url_for, flash

#to make debugging easier
DEBUG_MODE = True  

def check_session(role='admin'):
    if DEBUG_MODE:
        print(f"DEBUG_MODE is set to {DEBUG_MODE}")
        print('DEBUG_MODE is enabled. Skipping session check.')
        return None

    try:
        if role == 'admin':
            if 'admin_id' not in session:
                flash('You must be logged in to access this page.', 'warning')
                print('Admin not logged in!', session)
                return redirect(url_for('main.index'))
        elif role == 'user':
            if 'user_id' not in session:
                flash('You must be logged in to access this page.', 'warning')
                print('User not logged in!', session)
                return redirect(url_for('main.index'))
    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'danger')
        print(f"An error occurred: {str(e)}")
        return redirect(url_for('main.index'))

