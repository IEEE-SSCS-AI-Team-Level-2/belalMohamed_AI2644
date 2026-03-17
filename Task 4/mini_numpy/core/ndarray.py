from exceptions.errors import DimensionMismatchError, InvalidOperationError, NonNumericDataError, InvalidShapeError
class CustomArray:
    def __init__(self, data):
        self.data = data
        self.shape = self._get_shape(data)
        self.ndim = len(self.shape)

    def _get_shape(self, lst):
        if not isinstance(lst, list):
            return ()
        if not lst:
            return (0,)
        inner_shape = self._get_shape(lst[0])
        return (len(lst),) + inner_shape

    def flatten(self):
        def _flatten_recursive(lst):
            flat_list = []
            for item in lst:
                if isinstance(item, list):
                    flat_list.extend(_flatten_recursive(item))
                else:
                    flat_list.append(item)
            return flat_list
        
        flattened_data = _flatten_recursive(self.data)
        return CustomArray(flattened_data)

    def __add__(self, other):
        return self._element_wise_op(other, lambda x, y: x + y)

    def __sub__(self, other):
        return self._element_wise_op(other, lambda x, y: x - y)

    def __mul__(self, other):
        return self._element_wise_op(other, lambda x, y: x * y)

    def __pow__(self, other):
        return self._element_wise_op(other, lambda x, y: x ** y)

    def _element_wise_op(self, other, op_func):
        if isinstance(other, (int, float)):
            def _scalar_op(lst, scalar):
                if not isinstance(lst, list):
                    return op_func(lst, scalar)
                return [_scalar_op(item, scalar) for item in lst]
            return CustomArray(_scalar_op(self.data, other))
        
        elif isinstance(other, CustomArray):
            if self.shape != other.shape:
                raise DimensionMismatchError("Dimension Mismatch Error")
            def _array_op(lst1, lst2):
                if not isinstance(lst1, list):
                    return op_func(lst1, lst2)
                return [_array_op(i1, i2) for i1, i2 in zip(lst1, lst2)]
            return CustomArray(_array_op(self.data, other.data))
        else:
            raise InvalidOperationError("Invalid Operation Error")
            
    def __str__(self):
        return str(self.data)
    
    def __repr__(self):
        return f"CustomArray({self.data})"