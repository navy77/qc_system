from pydantic import BaseModel
from datetime import datetime

###### Specification #######
class Specification(BaseModel):
    spec_id: str
    process: str
    part_no: str
    item_no : int
    item_check : str
    spec_nominal :float
    tolerance_max : float
    tolerance_min : float
    point : int
    method : int
    class Config:
        from_attributes = True

###### Process #######
class Process(BaseModel):
    process_id: str
    process_name: str
    class Config:
        from_attributes = True
        
###### Calibration #######
class Calibration(BaseModel):
    instrument_no: str
    instrument_name: str
    exp_date:datetime
    calibration_no:str
    class Config:
        from_attributes = True