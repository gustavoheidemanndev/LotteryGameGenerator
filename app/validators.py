from exceptions import ValidationError

def validate_color_quantities(color_quantities: list[int]) -> None:
    if len(color_quantities) != 10:
        raise ValidationError("Array must have exactly 10 positions")
    if sum(color_quantities) != 15:
        raise ValidationError("Sum of quantities must be 15")
    for i in range(5):
        if not 0 <= color_quantities[i] <= 3:
            raise ValidationError(f"Position {i} must be between 0 and 3")
    for i in range(5, 10):
        if not 0 <= color_quantities[i] <= 2:
            raise ValidationError(f"Position {i} must be between 0 and 2")
        

