import sys
import os
import traceback

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app/models')))

from database import get_db_connection, get_cursor, close_db_connection  # type: ignore

# def test_connection():
#     try:
#         conn = get_db_connection()
#         if conn:
#             print("Connection successful")
#             conn.close()
#         else:
#             print("Connection failed")
#     except Exception as e:
#         print(f"Error: {e}")

# def test_get_cursor():
#     try:
#         cursor, conn = get_cursor()
#         print("Cursor and connection obtained successfully")
#         cursor.close()  
#         close_db_connection(conn)  
#     except Exception as e:
#         print(f"Error: {e}")
#         traceback.print_exc()

# if __name__ == "__main__":
#     print("Testing database connection...")
#     test_connection()
#     print("\nTesting cursor retrieval...")
#     test_get_cursor()
