"""
file_name = file_resource.py
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
import falcon
...

# LOCAL LIBRARY IMPORTS
...

class FileResource:
    def on_post(self, req, resp):
        file = req.get_param('file')
        if file is not None:
            # Handle regular file
            file_data = file.file.read()
            file_name = file.filename
            # Process the file as needed
            # ...
            resp.status = falcon.HTTP_200
            resp.body = 'File processed successfully'
        else:
            resp.status = falcon.HTTP_400
            resp.body = 'No file provided'
