from sqlalchemy.orm import Session
from . import schemas,models
from fastapi import HTTPException, status
######  Specification  ########

def create_spec(db: Session, specification: schemas.SpecificationCreate):
    existing_spec_id= db.query(models.Specification).filter(models.Specification.spec_id == specification.spec_id).first()
    if existing_spec_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="spec_id already exists")
    db_specification = models.Specification(**specification.dict())
    db.add(db_specification)
    db.commit()
    db.refresh(db_specification)
    return db_specification

def get_all_spec(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Specification).order_by(models.Specification.spec_id).offset(skip).limit(limit).all()

def get_spec(db: Session, spec_id: str):
    return db.query(models.Specification).filter(models.Specification.spec_id == spec_id).first()

def get_spec_by_part_no(db: Session, part_no: str):
    return db.query(models.Specification).filter(models.Specification.part_no == part_no).all()

def get_spec_by_process(db: Session, process: str):
    return db.query(models.Specification).filter(models.Specification.process == process).all()

def update_spec(db: Session, spec_id: str, specification: schemas.SpecificationCreate):
    db_specification = db.query(models.Specification).filter(models.Specification.spec_id == spec_id).first()
    if db_specification:
        db_specification.model = specification.model
        db_specification.spec = specification.spec
        db_specification.spec_max = specification.spec_max
        db_specification.spec_min = specification.spec_min
        
        db.commit()
        db.refresh(db_specification)
        return db_specification
    return None

def delete_spec(db: Session, spec_id: str):
    db_specification = db.query(models.Specification).filter(models.Specification.spec_id == spec_id).first()

    if db_specification:
        db.delete(db_specification)
        db.commit()
        return db_specification
    return None

# ######  measure  ########
# def create_measure(db: Session, measure: schemas.MeasureCreate):
#     db_measure = models.Measure(**measure.dict())
#     db.add(db_measure)
#     db.commit()
#     db.refresh(db_measure)
#     return db_measure

# def get_all_measure(db: Session, skip: int = 0, limit: int = 10):
#     # return db.query(models.Measure).offset(skip).limit(limit).all()
#     return db.query(models.Measure).order_by(models.Measure.spec_id).offset(skip).limit(limit).all()

# def get_measure_by_spec_id(db: Session, spec_id: int):
#     # return db.query(models.Measure).filter(models.Measure.spec_id == spec_id).all()
#     return db.query(models.Measure).filter(models.Measure.spec_id == spec_id).first()

# def update_measure(db: Session, id: int, measure: schemas.MeasureCreate):
#     db_measure = db.query(models.Measure).filter(models.Measure.id == id).first()
#     if db_measure:
#         db_measure.model = measure.model
#         db_measure.lot_no = measure.lot_no
#         db_measure.machine_no = measure.machine_no
#         db_measure.instrument_no = measure.instrument_no
#         # db_measure.value = measure.value
#         db_measure.spec_max = measure.spec_max
#         db_measure.spec_min = measure.spec_min
#         db_measure.spec = measure.spec
#         db_measure.judgment = measure.judgment
#         db_measure.judgment = measure.employee

#         db.commit()
#         db.refresh(db_measure)
#         return db_measure
#     return None

# def delete_measure(db: Session, id: int):
#     db_measure = db.query(models.Measure).filter(models.Measure.id == id).first()
#     if db_measure:
#         db.delete(db_measure)
#         db.commit()
#         return db_measure
#     return None

# ######  calibratation  ########

# def create_calibration(db: Session, calibration: schemas.CalibrationCreate):
#     db_calibration = models.Calibration(**calibration.dict())
#     db.add(db_calibration)
#     db.commit()
#     db.refresh(db_calibration)
#     return db_calibration

# def get_calibration(db: Session, instrument_no: str):
#     # return db.query(models.Calibration).filter(models.Calibration.instrument_no == instrument_no).first()
#     return db.query(models.Calibration).filter(models.Calibration.instrument_no == instrument_no).first()

# def get_all_calibration(db: Session, skip: int = 0, limit: int = 10):
#     # return db.query(models.Calibration).offset(skip).limit(limit).all()
#     return db.query(models.Calibration).order_by(models.Calibration.instrument_no).offset(skip).limit(limit).all()

# def update_calibration(db: Session, instrument_no: str, calibration: schemas.CalibrationCreate):
#     db_calibration = db.query(models.Calibration).filter(models.Calibration.instrument_no == instrument_no).first()
#     if db_calibration:
#         db_calibration.instrument_name = calibration.instrument_name
#         db_calibration.exp_date = calibration.exp_date
#         db_calibration.calibration_no = calibration.calibration_no

#         db.commit()
#         db.refresh(db_calibration)
#         return db_calibration
#     return None

# def delete_calibration(db: Session, instrument_no: str):
#     db_calibration = db.query(models.Calibration).filter(models.Calibration.instrument_no == instrument_no).first()
#     if db_calibration:
#         db.delete(db_calibration)
#         db.commit()
#         return db_calibration
#     return None