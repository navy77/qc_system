from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from .. import crud, models, schemas, database

router = APIRouter()

@router.post("/", response_model=schemas.Process)
def create_process(process: schemas.Process, db: Session = Depends(database.get_db)):
    existing_process_id = db.query(models.Process).filter(models.Process.process_id == process.process_id).first()
    if existing_process_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="process_id already exists")
    db_process = models.Process(**process.dict())
    db.add(db_process)
    db.commit()
    db.refresh(db_process)
    return db_process


@router.get("/", response_model=list[schemas.Process])
def read_process(limit: int = 10, db: Session = Depends(database.get_db)):
    process_all = db.query(models.Process).limit(limit).all()
    if process_all is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not found any process")
    return process_all

@router.put("/{process_id}", response_model=schemas.Process)
def update_process(process_id: str, process: schemas.Process, db: Session = Depends(database.get_db)):
    process_update = db.query(models.Process).filter(models.Process.process_id == process_id).first()
    if process_update:
        process_update.process_name = process.process_name
        db.commit()
        db.refresh(process_update)
    if process_update is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can not update spec")
    return process_update

@router.delete("/{process_id}", response_model=schemas.Process)
def delete_process(process_id: str, db: Session = Depends(database.get_db)):
    process_delete = db.query(models.Process).filter(models.Process.process_id == process_id).first()
    if process_delete:
        db.delete(process_delete)
        db.commit()
    
    if process_delete is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can not delete process")
    return process_delete
