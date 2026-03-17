from pydantic import BaseModel, field_validator
from typing import Any, Union, Tuple
from exceptions.errors import NonNumericDataError, InvalidShapeError

def _validate_structure_and_types(lst):
    if not isinstance(lst, list):
        if not isinstance(lst, (int, float)):
            raise NonNumericDataError("Array elements must be numeric (int or float).")
        return ()
    
    if not lst:
        return (0,)
    
    inner_shape = _validate_structure_and_types(lst[0])
    
    for item in lst[1:]:
        if _validate_structure_and_types(item) != inner_shape:
            raise InvalidShapeError("Nested list structures are inconsistent.")
            
    return (len(lst),) + inner_shape

class ArrayData(BaseModel):
    data: Any

    @field_validator('data')
    @classmethod
    def validate_data(cls, v):
        _validate_structure_and_types(v)
        return v

class ArrayShape(BaseModel):
    shape: Union[int, Tuple[int, ...]]

    @field_validator('shape')
    @classmethod
    def validate_shape(cls, v):
        if isinstance(v, int):
            if v < 0:
                raise InvalidShapeError("Shape dimensions cannot be negative.")
        else:
            for dim in v:
                if not isinstance(dim, int) or dim < 0:
                    raise InvalidShapeError("Shape dimensions must be non-negative integers.")
        return v