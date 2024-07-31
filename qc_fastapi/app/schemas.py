from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class SpecificationBase(BaseModel):
    process: str
    part_no: str
    item : int
    spec_name : str
    spec :float
    spec_max : float
    spec_min : float
    point : int
    method : int

class SpecificationCreate(SpecificationBase):
    spec_id: str

class Specification(SpecificationBase):
    spec_id: str

    class Config:
        from_attributes = True

# class MeasureBase(BaseModel):
#     measure_time: datetime
#     model: str
#     lot_no: str
#     machine_no: str
#     instrument_no: str
#     value: float
#     spec: float
#     spec_max: float
#     spec_min: float
#     judgment: str
#     employee: str
    

# class MeasureCreate(MeasureBase):
#     spec_id: str

# class Measure(MeasureBase):
#     id: int
#     spec_id: str

#     class Config:
#         from_attributes = True

# class CalibrationBase(BaseModel):
#     instrument_name: str
#     exp_date: datetime
#     calibration_no: str

# class CalibrationCreate(CalibrationBase):
#     instrument_no: str

# class Calibration(CalibrationBase):
#     instrument_no: Optional[str] = None

#     class Config:
#         from_attributes = True
