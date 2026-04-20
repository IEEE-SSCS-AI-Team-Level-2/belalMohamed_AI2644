from core.ndarray import CustomArray
from array_statistics.stats import mean, var, std
from creation.array_creation import array, zeros, ones, eye
from exceptions.errors import DimensionMismatchError, NonNumericDataError, InvalidShapeError, InvalidOperationError

def main():
    print("Testing Core & Operators:")
    A = CustomArray([[1, 2], [3, 4]])
    B = CustomArray([[5, 6], [7, 8]])

    print(f"Array A:\n{A}")
    print(f"\nArray B:\n{B}")
    
    C = A + B
    print(f"\nC = A + B:\n{C}")

    D = A + 5
    print(f"\nD = A + 5:\n{D}")

    E = A ** 2
    print(f"\nE = A ** 2:\n{E}")

    F = A * B
    print(f"\nF = A * B:\n{F}")

    G = A - B
    print(f"\nG = A - B:\n{G}")

    print("\nTesting Statistics:")
    print(f"Mean of A: {mean(A)}")
    print(f"Variance of A: {var(A)}")
    print(f"Standard Deviation of A: {std(A)}")

    print(f"\nFlattened Array A:\n{A.flatten()}")
        
    print("\nTesting Array Creation: ")
    list_data = [[10, 20, 30], [40, 50, 60]]
    custom_created = array(list_data)
    print(f"Custom Created Array:\n{custom_created}")
    print(f"Shape: {custom_created.shape}")

    z = zeros((2, 3))
    print(f"\nZeros Array:\n{z}")

    o = ones((3, 2))
    print(f"\nOnes Array:\n{o}")

    e1 = eye(3, 3)
    print(f"\nIdentity Array:\n{e1}")

    e2 = eye(3, 4, k=1)
    print(f"\nOffset Identity Array:\n{e2}")

    print("\nTesting Error Handling & Validation: ")
    
    try:
        print("Attempting to add arrays of different shapes...")
        bad_array = CustomArray([[1, 2, 3]])
        result = A + bad_array
    except DimensionMismatchError as e:
        print(f"Successfully caught: {type(e).__name__} -> {e}")

    try:
        print("\nAttempting to create an array with strings...")
        bad_data = array([["a", "b"], ["c", "d"]])
    except NonNumericDataError as e:
        print(f"Successfully caught: {type(e).__name__} -> {e}")

    try:
        print("\nAttempting to create a ragged array...")
        ragged_data = array([[1, 2], [3, 4, 5]])
    except InvalidShapeError as e:
        print(f"Successfully caught: {type(e).__name__} -> {e}")

    try:
        print("\nAttempting an invalid operation (Array + String)...")
        result = A + "this is a string"
    except InvalidOperationError as e:
        print(f"Successfully caught: {type(e).__name__} -> {e}")


if __name__ == "__main__":
    main()