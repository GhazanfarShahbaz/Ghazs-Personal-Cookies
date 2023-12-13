"""
file_name = machine_handler.py
Created On: 2023/11/18
Lasted Updated: 2023/11/18
Description: _FILL OUT HERE_
Edit Log:
2023/11/18
    - Created file
"""

# STANDARD LIBRARY IMPORTS
from os import environ
from typing import Dict, List, Final, TypeAlias
from json import load, dump

# THIRD PARTY LIBRARY IMPORTS

# LOCAL LIBRARY IMPORTS
from apps.falcon_apps.file_transporter.utils.machine_utils.machine import Machine


MachineId: TypeAlias = str

class MachineHandler:
    def __init__(self, registered_machines_path: None or str = None) -> None:
        if not registered_machines_path:
            registered_machines_path = environ["PATH_TO_REGISTERED_MACHINES"]

        self._registered_machines_path_: str = registered_machines_path   
        self._registered_machines_ = self._get_registered_machines_dict_()    


    # PROPERTIES START HERE

    @property 
    def registered_machines(self) -> Dict[MachineId, Machine]:
        return self._registered_machines_

    # PROPERTIES END HERE

    # PUBLIC METHODS START HERE

    def register_machine(self, machine_id: MachineId) -> bool: 
        if self.is_registered(machine_id):
            return False
        
        self._registered_machines_[machine_id] = {}
        self._update_registered_machins_json_()
        
        # assign a password to the machine
    
    
    def is_registered(self, machine_id: MachineId) -> bool: 
        return machine_id in self._registered_machines_
    
    
    def list_machines(self) -> List[str]:
        return self._registered_machines_.keys()
    
    # TODO: List machines

    # PUBLIC METHODS END HERE

    # PRIVATE METHODS START HERE

    def _get_registered_machines_dict_(self) -> Dict[MachineId, Machine]:
        data = None
        
        with open(self._registered_machines_path_, "r") as registered_machines_json:
            data = load(registered_machines_json)
        
        return data
    
    def _update_registered_machins_json_(self) -> None:
        with open(self._registered_machines_path_, "w") as registered_machines_json:
            dump(self._registered_machines_, registered_machines_json, indent = 4)

    # PRIVATE METHODS END HERE 
        
        

MACHINE_HANDLER: MachineHandler = MachineHandler()