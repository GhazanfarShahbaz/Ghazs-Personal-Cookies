import falcon

from falcon import before as falcon_before_request

from apps.falcon_apps.file_transporter.hooks.authenticate import authenticate
from apps.falcon_apps.file_transporter.utils.machine_utils.machine_handler import MACHINE_HANDLER

@falcon_before_request(authenticate)
class RegisterMachineResource:
    def on_post(self, req, resp, **kwargs):
        request = req.get_media()
        
        machine_id = request.get("MachineID")
        
        if not MACHINE_HANDLER.register_machine(machine_id):
            resp.status = falcon.HTTP_400
            return 
        
        resp.status = falcon.HTTP_201