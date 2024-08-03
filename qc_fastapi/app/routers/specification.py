from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from .. import  models, schemas, database

router = APIRouter()

@router.post("/", response_model=schemas.Specification)
def create_specification(specification: schemas.Specification, db: Session = Depends(database.get_db)):
    existing_spec_id= db.query(models.Specification).filter(models.Specification.spec_id == specification.spec_id).first()
    if existing_spec_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="spec_id already exists")
    db_specification = models.Specification(**specification.dict())
    db.add(db_specification)
    db.commit()
    db.refresh(db_specification)
    return db_specification

@router.get("/", response_model=list[schemas.Specification])
def read_specification(limit: int = 100, db: Session = Depends(database.get_db)):
    specifications_all = db.query(models.Specification).limit(limit).all()
    if specifications_all is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not found any spec")
    return specifications_all

@router.get("/{spec_id}", response_model=schemas.Specification)
def read_specification(spec_id: str, db: Session = Depends(database.get_db)):
    specifications_spec_id = db.query(models.Specification).filter(models.Specification.spec_id == spec_id).first()
    if specifications_spec_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not found spec")
    return specifications_spec_id

@router.get("/part_no/{part_no}", response_model=list[schemas.Specification])
def read_specification_by_part_no(part_no: str, db: Session = Depends(database.get_db)):
    specifications_part_no = db.query(models.Specification).filter(models.Specification.part_no == part_no).all()
    if specifications_part_no is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not found spec")
    return specifications_part_no

@router.get("/process/{process}", response_model=list[schemas.Specification])
def read_specification_by_process(process: str, db: Session = Depends(database.get_db)):
    specifications_process = db.query(models.Specification).filter(models.Specification.process == process).all()
    if specifications_process is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not found spec")
    return specifications_process

@router.put("/{spec_id}", response_model=schemas.Specification)
def update_specification(spec_id: str, specification: schemas.Specification, db: Session = Depends(database.get_db)):
    specification_update = db.query(models.Specification).filter(models.Specification.spec_id == spec_id).first()
    if specification_update:
        specification_update.process = specification.process
        specification_update.part_no = specification.part_no
        specification_update.item_no = specification.item_no
        specification_update.item_check = specification.item_check
        specification_update.spec_nominal = specification.spec_nominal
        specification_update.tolerance_max = specification.tolerance_max
        specification_update.tolerance_min = specification.tolerance_min
        specification_update.point = specification.point
        specification_update.method = specification.method

        db.commit()
        db.refresh(specification_update)

    if specification_update is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can not update spec")
    return specification_update

@router.delete("/{spec_id}", response_model=schemas.Specification)
def delete_specification(spec_id: str, db: Session = Depends(database.get_db)):
    specification_delete = db.query(models.Specification).filter(models.Specification.spec_id == spec_id).first()
    if specification_delete:
        db.delete(specification_delete)
        db.commit()

    if specification_delete is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can not delete spec")
    return specification_delete

