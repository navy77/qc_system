from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, models, schemas, database

router = APIRouter()

@router.post("/", response_model=schemas.Calibration)
def create_calibration(calibration: schemas.CalibrationCreate, db: Session = Depends(database.get_db)):
    return crud.create_calibration(db=db, calibration=calibration)

@router.get("/{instrument_no}", response_model=schemas.Calibration)
def read_machine(instrument_no: str, db: Session = Depends(database.get_db)):
    db_calibration = crud.get_calibration(db, instrument_no=instrument_no)
    if db_calibration is None:
        raise HTTPException(status_code=404, detail="Calibration not found")
    return db_calibration

@router.get("/", response_model=list[schemas.Calibration])
def read_calibration(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    calibrations = crud.get_all_calibration(db, skip=skip, limit=limit)
    return calibrations


@router.put("/{instrument_no}", response_model=schemas.Calibration)
def update_carlibration(instrument_no: str, calibration: schemas.CalibrationCreate, db: Session = Depends(database.get_db)):
    db_calibration = crud.update_machine(db, instrument_no=instrument_no, calibration=calibration)
    if db_calibration is None:
        raise HTTPException(status_code=404, detail="Calibration not found")
    return db_calibration

@router.delete("/{instrument_no}", response_model=schemas.Calibration)
def delete_calibration(instrument_no: str, db: Session = Depends(database.get_db)):
    db_calibration = crud.delete_calibration(db, instrument_no=instrument_no)
    if db_calibration is None:
        raise HTTPException(status_code=404, detail="Calibration not found")
    return db_calibration