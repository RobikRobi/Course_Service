from enum import Enum



class CoursesCategory(Enum):
    PROGRAMMING = "programming"
    MATH = "math"
    DATA = "data"
    BACKEND = "backend"

class CoursesLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"