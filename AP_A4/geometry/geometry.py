"""Explain why the classmethods of the shape class are implemented as classmethods?"""
from numbers import Real
import math

class Shape:
    """this class is an interface class for other shapes."""
    @classmethod
    def check_if_args_not_below_zero(cls, *args) -> bool:
        """Returns True if all of the args are non-negative otherwise returns False."""
        for arg in args:
            if not isinstance(arg, Real):
                raise TypeError("arguments must all be numeric.")
            if arg <= 0:
                return False
        else:
            return True

    @classmethod
    def get_area_formula(cls) -> str:
        f"""Returns the formula of calculating the area of the {type(cls).__name__}."""
        raise NotImplementedError

    @classmethod
    def get_perimeter_formula(cls) -> str:
        f"""Returns the formula of calculating the perimeter of the {type(cls).__name__}."""
        raise NotImplementedError

    def get_area(self) -> float:
        """Returns the area of the shape."""
        raise NotImplementedError

    def get_perimeter(self) -> float:
        """Returns the perimeter of the shape."""
        raise NotImplementedError

    def __str__(self):
        """
        Returns the general info about the shape.
        it sould be accurate. it will be used in eval function later.
        <ShapeName>(param1, param2, ...)
        """
        raise NotImplementedError

    def __eq__(self, other):
        raise NotImplementedError

    def __lt__(self, other):
        if not isinstance(other, Shape):
            return NotImplemented
        else:
            return self.get_area() < other.get_area()

    def __le__(self, other):
        if not isinstance(other, Shape):
            return NotImplemented
        else:
            return self.get_area() <= other.get_area()


class Circle(Shape):
    """Circle class"""
    PI = 3.14159265359 
    
    def __init__(self, r:float):
        if Circle.check_if_args_not_below_zero(r):
            self.r = r
        else:
            raise ValueError("radius must be a non-negative number.")
    
    @classmethod
    def get_area_formula(cls) -> str:
        return "PI * (radius ^ 2)"

    @classmethod
    def get_perimeter_formula(cls) -> str:
        return "2 * PI * radius"

    def get_area(self):
        return Circle.PI * self.r ** 2

    def get_perimeter(self):
        return 2 * Circle.PI * self.r

    def __str__(self):
        return f"Circle({self.r})"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        else:
            return self.r == other.r


class Triangle(Shape):
    """Triangle class"""

    def __init__(self, a:float, b:float, c:float):
        if Triangle.check_creates_triangle([a, b, c]):
            self.a = a
            self.b = b
            self.c = c
        else:
            raise ValueError("sides must be non-negative and create a triangle.")

    @staticmethod
    def check_creates_triangle(sides:list[float]) -> bool:
        """Checks if the given sides can create a triangle considering Triangular inequality."""
        assert len(sides) == 3
        a, b, c = sides

        if b + c <= a or a + b <= c or a + c <= b:
            return False
        else:
            return a > 0 and b > 0 and c > 0

    @classmethod
    def get_area_formula(cls) -> str:
        return "sqrt(s(s-a)(s-b)(s-c))"

    @classmethod
    def get_perimeter_formula(cls) -> str:
        return "a + b + c"

    def get_area(self):
        s = self.get_perimeter() / 2
        return math.sqrt(s*(s-self.a)*(s-self.b)*(s-self.c))

    def get_perimeter(self):
        return self.a + self.b + self.c

    def __str__(self):
        return f"Triangle({self.a}, {self.b}, {self.c})"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        else:
            return {self.a, self.b, self.c} == {other.a, other.b, other.c}


class Equilateral_Triangle(Triangle):
    """Equilateral triangle"""

    def __init__(self, a:float):
        if Equilateral_Triangle.check_if_args_not_below_zero(a):
            self.a = a
            super().__init__(a, a, a)
        else:
            raise ValueError("The edge must be a non-negative number.")
    
    @classmethod
    def get_area_formula(cls) -> str:
        return "sqrt(3 * a) / 4"

    @classmethod
    def get_perimeter_formula(cls) -> str:
        return "3 * a"

    def __str__(self):
        return f"Equilateral_Triangle({self.a})"


class Rectangle(Shape):
    """Rectangle class"""

    def __init__(self, a:float, b:float):
        """
        a: length
        b: width
        """
        if Rectangle.check_if_args_not_below_zero(a, b):
            self.a = a
            self.b = b
        else:
            raise ValueError("length and width must be non-negative numbers.")
    
    @classmethod
    def get_perimeter_formula(cls):
        return "2 * (a + b)"

    @classmethod
    def get_area_formula(cls):
        return "a * b"

    def get_perimeter(self):
        return 2 * (self.a + self.b)

    def get_area(self):
        return self.a * self.b

    def __str__(self):
        return f"Rectangle({self.a}, {self.b})"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        else:
            return {self.a, self.b} == {other.a, other.b}


class Square(Rectangle):
    """Square class"""

    def __init__(self, a:float):
        if Square.check_if_args_not_below_zero(a):
            self.a = a
            super().__init__(a, a)
        else:
            raise ValueError("a must be a non-negative number.")
    
    @classmethod
    def get_perimeter_formula(cls):
        return "4 * a"

    @classmethod
    def get_area_formula(cls):
        return "a ^ 2"

    def __str__(self):
        return f"Square({self.a})"


class Regular_Pantagon(Shape):
    """Regular pantagon"""

    def __init__(self, a:float):
        if Rectangle.check_if_args_not_below_zero(a):
            self.a = a
        else:
            raise ValueError("edges must be non-negative numbers.")

    @classmethod
    def get_area_formula(cls):
        return "5 * area(triangle)"

    @classmethod
    def get_perimeter_formula(cls):
        return "5 * a"

    def get_area(self):
        # the pantagon is made from 5 isosceles triangles.
        leg = self.a / (2 * math.cos( 54 * math.pi / 180 ) )
        triangle = Triangle(self.a, leg, leg)
        return 5 * triangle.get_area()

    def get_perimeter(self):
        return 5 * self.a

    def __str__(self):
        return f"Regular_Pantagon({self.a})"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        else:
            return self.a == other.a


class ShapeList:
    AVAILABLE_SHAPES = ['Circle', 'Triangle', 'Equilateral_Triangle', 'Rectangle', 'Square', 'Regular_Pantagon']

    def __init__(self, *shapes):
        self.shapes:list[Shape] = []
        for shape in shapes:
            self.add_shape(shape)

    def add_shape(self, shape:Shape):
        if issubclass(type(shape), Shape):
            self.shapes.append(shape)
        else:
            raise TypeError(f"{shape} is not an object of Shape class.")
    
    @staticmethod
    def get_table(records:list[tuple], headers:list[str], max_length:int=27):
        """Returns the shapes table in a appropriate format to be saved in the MD file."""

        res = "| "
        # add headers
        for header in headers:
            res += f"{header:^{max_length}} | "
        res += "\n| "

        # add "-----"s
        for _ in range(len(headers)):
            res += f"{':-------------:':^{max_length}} | "
        res += "\n| "

        # add records
        for record in records:
            for field in record:
                res += f"{field:^{max_length}} | "
            res += "\n| "

        # four last characters are '\n| ' and should be eliminated.
        return res[:-4]

    def get_shapes_table(self) -> str:
        """Extract data from shapes and return the corresponding table using get_table staticmethod."""

        # headers: idx, Class, __str__, Perimeter, Formula, Area, Formula
        headers = ['idx', 'Class', '`__str__`', 'Perimeter', 'Formula', 'Area', 'Formula']
        records = []
        # extraction of record information
        for i, shape in enumerate(self.shapes):
            records.append(
                (i,
                shape.__class__.__name__, 
                str(shape), 
                round(shape.get_perimeter(), 2), 
                shape.get_perimeter_formula(), 
                round(shape.get_area(), 2),
                shape.get_area_formula())
                )
        
        return ShapeList.get_table(records, headers)

    def get_largest_shape_by_perimeter(self) -> Shape:
        """Returns the largest shape considering its perimeter."""
        max_perimeter = 0
        res_shape = None
        for shape in self.shapes:
            if (pr:=shape.get_perimeter()) > max_perimeter:
                max_perimeter = pr
                res_shape = shape
        return res_shape

    def get_largest_shape_by_area(self) -> Shape:
        """Returns the largest shape considering its area."""
        return max(self.shapes) if len(self.shapes) else None
