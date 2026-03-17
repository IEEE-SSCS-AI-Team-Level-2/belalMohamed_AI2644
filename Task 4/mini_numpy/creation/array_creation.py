from core.ndarray import CustomArray
from validation.schemas import ArrayData, ArrayShape
from pydantic import ValidationError
from exceptions.errors import NonNumericDataError, InvalidShapeError

def _build_array(shape, value):
    if not shape:
        return value
    if len(shape) == 1:
        return [value for _ in range(shape[0])]
    return [_build_array(shape[1:], value) for _ in range(shape[0])]

def array(data):
    try:
        validated_model = ArrayData(data=data)
        return CustomArray(validated_model.data)
    except ValidationError as e:
        error_msg = str(e)
        if "numeric" in error_msg.lower():
            raise NonNumericDataError("Array elements must be numeric.") from None
        else:
            raise InvalidShapeError("Nested list structures are inconsistent or invalid.") from None

def zeros(shape):
    try:
        validated_model = ArrayShape(shape=shape)
        actual_shape = (validated_model.shape,) if isinstance(validated_model.shape, int) else validated_model.shape
        return CustomArray(_build_array(actual_shape, 0.0))
    except ValidationError:
        raise InvalidShapeError("Shape dimensions must be non-negative integers.") from None

def ones(shape):
    try:
        validated_model = ArrayShape(shape=shape)
        actual_shape = (validated_model.shape,) if isinstance(validated_model.shape, int) else validated_model.shape
        return CustomArray(_build_array(actual_shape, 1.0))
    except ValidationError:
        raise InvalidShapeError("Shape dimensions must be non-negative integers.") from None

def eye(m, n, k=0):
    matrix = []
    for i in range(m):
        row = []
        for j in range(n):
            if j - i == k:
                row.append(1.0)
            else:
                row.append(0.0)
        matrix.append(row)
    return CustomArray(matrix)