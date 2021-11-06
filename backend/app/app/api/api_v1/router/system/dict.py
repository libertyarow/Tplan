from typing import Any, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, schemas
from app.common import deps

router = APIRouter()


@router.get("/type/list", response_model=schemas.Response)
def get_type_list(*, db: Session = Depends(deps.get_db),
                  name: str = None, code: str = None, page: Optional[int] = 0, limit: Optional[int] = 10,
                  ) -> Any:
    """字典管理-查询"""
    query = db.query(models.DictType)
    if name: query = query.filter(models.DictType.name.like("%" + name + "%"))
    if code: query = query.filter(models.DictType.code.like("%" + code + "%"))
    total = query.count()
    items = query.limit(limit).offset((page - 1) * limit).all()
    return {"code": 20000, "data": {"items": items, 'total': total}, }


# 需要写在/type/{id}前面
@router.get("/type/all", response_model=schemas.Response)
def read_types(*, db: Session = Depends(deps.get_db)) -> Any:
    """字典数据明细 select 查询所有字典"""
    types = db.query(models.DictType).all()
    return {"code": 20000, "data": types}


@router.get("/type/{id}", response_model=schemas.Response)
def read_dict_type(*, db: Session = Depends(deps.get_db), id: int, ) -> Any:
    """字典管理-获取一个字典详情"""
    type = db.query(models.DictType).filter(models.DictType.id == id).one()
    return {"code": 20000, "data": type, }


@router.put("/type", response_model=schemas.Response)
def update_dict_type(*, db: Session = Depends(deps.get_db), type: schemas.DictTypeUpdate, ) -> Any:
    """字典管理-更新"""
    db.query(models.DictType).filter(models.DictType.id == type.id).update(type)
    return {"code": 20000, "message": "修改成功", }


@router.delete("/type/{type_id}", response_model=schemas.Response)
def delete_type_id(type_id: str, db: Session = Depends(deps.get_db), ) -> Any:
    """字典管理-删除"""
    type_ids = [int(type_id) for type_id in type_id.split(",")]
    db.query(models.DictType).filter(models.DictType.id.in_(type_ids)).delete(synchronize_session=False)
    return {"code": 20000, "data": "", "message": f"删除成功"}


@router.post("/type", response_model=schemas.Response)
def add_type(*, db: Session = Depends(deps.get_db), type: schemas.DictTypeCreate, ) -> Any:
    """字典管理 新增"""
    db.add(models.DictType(**type.dict()))
    return {"code": 20000, "message": "新增成功", }


@router.get("/data/list", response_model=schemas.Response)
def read_routes(*, db: Session = Depends(deps.get_db),
                type_id: str, page: int = 0, limit: int = 100, label: str = None) -> Any:
    """字典数据明细 查询"""
    query = db.query(models.DictData).join(models.DictType, models.DictType.id == models.DictData.type_id
                                           ).filter(models.DictType.id == type_id)
    if label: query = query.filter(models.DictData.label.like("%" + label + "%"))
    total = query.count()
    dict_data = query.limit(limit).offset((page - 1) * limit).all()
    return {"code": 20000, "data": {"dict_data": dict_data, 'total': total}, }


@router.get("/data/{id}", response_model=schemas.Response)
def read_data(*, db: Session = Depends(deps.get_db), id: int) -> Any:
    """字典数据明细-修改前查询"""
    data = db.query(models.DictData).filter(models.DictData.id == id).one()
    return {"code": 20000, "data": data, }


@router.put("/data", response_model=schemas.Response)
def add_dict_data(*, db: Session = Depends(deps.get_db), data: schemas.DictDataUpdate, ) -> Any:
    """字典数据明细-修改"""
    db.query(models.DictData).filter(models.DictData.id == data.id).update(data)
    return {"code": 20000, "message": "修改成功", }


@router.post("/data", response_model=schemas.Response)
def add_data(*, db: Session = Depends(deps.get_db), data: schemas.DictDataCreate, ) -> Any:
    """字典数据明细-新增"""
    db.add(models.DictData(**data.dict()))
    return {"code": 20000, "message": "新增成功", }


@router.delete("/data/{data_id}", response_model=schemas.Response)
def delete_data_id(data_id: str, db: Session = Depends(deps.get_db)) -> Any:
    """字典数据明细-删除"""
    data_ids = [int(type_id) for type_id in data_id.split(",")]
    db.query(models.DictData).filter(models.DictData.id.in_(data_ids)).delete(synchronize_session=False)
    return {"code": 20000, "data": "", "message": f"删除成功"}


@router.get("/data/type_code/{type_code}", response_model=schemas.Response)
def get_data_type_code(*, db: Session = Depends(deps.get_db), type_code: str) -> Any:
    """根据type.code获取type.data 用于前端user"""
    data = db.query(models.DictType).filter(models.DictType.code == type_code).one().data
    data = [{"id": i.id, "label": i.label} for i in data]
    return {"code": 20000, "data": data}
