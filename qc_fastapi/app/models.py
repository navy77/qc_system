from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from .database import Base

class Specification(Base):
    __tablename__ = "specification"
    spec_id = Column(String(50),primary_key=True, index=True)  
    process = Column(String(50))  
    part_no = Column(String(50))
    item = Column(Integer)
    spec_name = Column(String(50))
    spec = Column(Float)
    spec_max = Column(Float)
    spec_min = Column(Float)
    point = Column(Integer)
    method = Column(Integer)
    
# class Measure(Base):
#     __tablename__ = "measure"
#     id = Column(Integer, primary_key=True, index=True)
#     spec_id = Column(String(50), ForeignKey("specification.spec_id"), index=True)  
#     measure_time = Column(DateTime)
#     model = Column(String(100)) 
#     lot_no = Column(String(100))  
#     machine_no = Column(String(100))
#     instrument_no = Column(String(100))
#     spec = Column(Float)
#     spec_max = Column(Float)
#     spec_min = Column(Float)
#     value = Column(Float)
#     judgment = Column(String(100))  
#     employee = Column(String(100))  

# class Calibration(Base):
#     __tablename__ = "calibration"
#     instrument_no = Column(String(50))  
#     instrument_name = Column(String(100)) 
#     exp_date = Column(DateTime)
    # calibration_no = Column(String(100)) 