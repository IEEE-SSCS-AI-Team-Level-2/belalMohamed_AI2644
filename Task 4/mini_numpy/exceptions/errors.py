class InvalidShapeError(Exception):
    def __init__(self, message="Invalid shape for array operation."):
        super().__init__(message)

class DimensionMismatchError(Exception):
    def __init__(self, message="Dimensions of the arrays do not match."):
        super().__init__(message)

class NonNumericDataError(Exception):
    def __init__(self, message="Array elements must be numeric."):
        super().__init__(message)

class InvalidOperationError(Exception):
    def __init__(self, message="This operation is not supported."):
        super().__init__(message)