from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from .. import models, schemas, database

router = APIRouter()

@router.post("/", response_model=schemas.Calibration)
def create_cal(calibration: schemas.Calibration, db: Session = Depends(database.get_db)):
    existing_instrument_no = db.query(models.Calibration).filter(models.Calibration.instrument_no == calibration.instrument_no).first()
    if existing_instrument_no:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="instrument_no already exists")
    db_cal = models.Calibration(**calibration.dict())
    db.add(db_cal)
    db.commit()
    db.refresh(db_cal)
    return db_cal

@router.get("/", response_model=list[schemas.Calibration])
def read_cal(limit: int = 10, db: Session = Depends(database.get_db)):
    cal_all = db.query(models.Calibration).limit(limit).all()
    if cal_all is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not found any calibration item")
    return cal_all

@router.put("/{instrument_no}", response_model=schemas.Calibration)
def update_cal(instrument_no: str, calibration: schemas.Calibration, db: Session = Depends(database.get_db)):
    cal_update = db.query(models.Calibration).filter(models.Calibration.instrument_no == instrument_no).first()
    if cal_update:
        cal_update.instrument_name = calibration.instrument_name
        cal_update.calibration_no = calibration.calibration_no
        cal_update.exp_date = cal_update.exp_date
        db.commit()
        db.refresh(cal_update)
    if cal_update is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can not update calibration item")
    return cal_update

@router.delete("/{instrument_no}", response_model=schemas.Calibration)
def delete_cal(instrument_no: str, db: Session = Depends(database.get_db)):
    cal_delete = db.query(models.Calibration).filter(models.Calibration.instrument_no == instrument_no).first()
    if cal_delete:
        db.delete(cal_delete)
        db.commit()
    if cal_delete is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can not delete calibration item")
    return cal_delete