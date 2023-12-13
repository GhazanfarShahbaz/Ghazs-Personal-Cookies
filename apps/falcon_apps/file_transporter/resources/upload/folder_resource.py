"""
file_name = folder_resource.py
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

class FolderZipResource:
    def on_post(self, req, resp):
        file = req.get_param('file')
        
        if file is not None:
            if file.filename.endswith('.zip'):
                # Handle zip file
                with zipfile.ZipFile(file.file, 'r') as zip_ref:
                    zip_ref.extractall('extracted_files/')
                # Process the extracted files
                
                for root, dirs, files in os.walk('extracted_files/'):
                    for file_name in files:
                        file_path = os.path.join(root, file_name)
                        
                        # Process the file as needed
                        # ...

                resp.status = falcon.HTTP_200
                resp.body = 'Zip file extracted and processed successfully'

            elif os.path.isdir(file.filename):
                # Handle folder
                for root, dirs, files in os.walk(file.filename):
                    for file_name in files:
                        file_path = os.path.join(root, file_name)
                        # Process the file as needed
                        # ...
                resp.status = falcon.HTTP_200
                resp.body = 'Folder processed successfully'

            else:
                resp.status = falcon.HTTP_400
                resp.body = 'Invalid file format'

        else:
            resp.status = falcon.HTTP_400
            resp.body = 'No file provided'