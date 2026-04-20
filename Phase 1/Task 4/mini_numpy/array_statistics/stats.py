from core.ndarray import CustomArray

def mean(array: CustomArray):
    flat_array = array.flatten().data
    if not flat_array:
        return 0.0
    return sum(flat_array) / len(flat_array)

def var(array: CustomArray):
    flat_array = array.flatten().data
    if not flat_array:
        return 0.0
    m = mean(array)
    variance = sum((x - m) ** 2 for x in flat_array) / len(flat_array)
    return variance

def std(array: CustomArray):
    return var(array) ** 0.5