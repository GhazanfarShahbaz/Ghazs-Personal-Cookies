"""
file_name = middleware.py
Created On: 2023/12/03
Lasted Updated: 2023/12/03
Description: _FILL OUT HERE_
Edit Log:
2023/12/03
    - Created file
"""

# STANDARD LIBRARY IMPORTS
...

# THIRD PARTY LIBRARY IMPORTS
...

# LOCAL LIBRARY IMPORTS
...

class Middleware:
    def process_request(self, req, resp):
        # Logic to execute before the request is processed
        print("Before request logic")

    # def process_response(self, req, resp, resource, req_succeeded):
    #     # Logic to execute after the response is processed
    #     print("After response logic")
    #     return resp