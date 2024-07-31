from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, models, schemas, database

router = APIRouter()

@router.post("/", response_model=schemas.Specification)
def create_specification(specification: schemas.SpecificationCreate, db: Session = Depends(database.get_db)):
    return crud.create_spec(db=db, specification=specification)

@router.get("/{spec_id}", response_model=schemas.Specification)
def read_specification(spec_id: str, db: Session = Depends(database.get_db)):
    db_specification = crud.get_spec(db, spec_id=spec_id)
    if db_specification is None:
        raise HTTPException(status_code=404, detail="Spec not found")
    return db_specification

@router.get("/part_no/{part_no}", response_model=list[schemas.Specification])
def read_specification_by_part_no(part_no: str, db: Session = Depends(database.get_db)):
    db_specification = crud.get_spec_by_part_no(db, part_no=part_no)
    if db_specification is None:
        raise HTTPException(status_code=404, detail="Spec not found")
    return db_specification

@router.get("/process/{process}", response_model=list[schemas.Specification])
def read_specification_by_process(process: str, db: Session = Depends(database.get_db)):
    db_specification = crud.get_spec_by_process(db, process=process)
    if db_specification is None:
        raise HTTPException(status_code=404, detail="Spec not found")
    return db_specification

@router.get("/", response_model=list[schemas.Specification])
def read_specification(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    specifications = crud.get_all_spec(db, skip=skip, limit=limit)
    return specifications

@router.put("/{spec_id}", response_model=schemas.Specification)
def update_specification(spec_id: str, specification: schemas.SpecificationCreate, db: Session = Depends(database.get_db)):
    db_specification = crud.update_spec(db, spec_id=spec_id, specification=specification)
    if db_specification is None:
        raise HTTPException(status_code=404, detail="Spec not found")
    return db_specification

@router.delete("/{spec_id}", response_model=schemas.Specification)
def delete_specification(spec_id: str, db: Session = Depends(database.get_db)):
    db_specification = crud.delete_spec(db, spec_id=spec_id)
    if db_specification is None:
        raise HTTPException(status_code=404, detail="Spec not found")
    return db_specification