from math import sqrt
from numbers import Real

class Integer:
    """Integer class"""

    def __init__(self, value:int):
        if type(value) != int:
            raise TypeError("value must be an int.")
        self._value = value

    @property
    def value(self):
        """The value of the integer."""
        return self._value

    def __repr__(self):
        return "Integer(%d)" % self.value

    def __eq__(self, other):
        if isinstance(other, Integer):
            return self.value == other.value
        elif isinstance(other, Real):
            return self.value == other
        else:
            raise TypeError(f"{other} must be Integer.")
    
    def __add__(self, other):
        if isinstance(other, Integer):
            return Integer(other.value + self.value)
        elif isinstance(other, Real):
            return Integer(other + self.value)
        elif isinstance(other, Complex) or isinstance(other, Matrix):
            return other + self
        else:
            raise TypeError(f"can't add matrix to object {other.__class__.__name__}.")

    def __mul__(self, other):
        if isinstance(other, Complex) or isinstance(other, Matrix):
            return other * self
        elif isinstance(other, Integer):
            return Integer(self.value * other.value)
        elif isinstance(other, Real):
            return Integer(self.value * other)          
        else:
            raise TypeError(f"can't add matrix to object {other.__class__.__name__}.")

    def __neg__(self):
        return Integer(-self.value)

    def __sub__(self, other):
        return self + (-other)

    @classmethod
    def make_integer_from_string(cls, string:str) -> "Integer":
        """Creates an Integer number from the given string."""
        assert type(string) == str

        if string.isdigit():
            return cls(int(string))
        else:
            raise ValueError(f"can't convert the {string} to integer.")


class Complex:
    """Complex class"""

    def __init__(self, real:float|int=0, imag:float|int=0) -> None:
        assert isinstance(real, Real) and isinstance(imag, Real)
        self._real = real
        self._imag = imag

    @property
    def real(self):
        """The real part of the complex number."""
        return self._real

    @property
    def imag(self):
        """The real part of the complex number."""
        return self._imag

    def __repr__(self):
        return "Complex(real=%d, imag=%d)" %(self.real, self.imag)

    def __eq__(self, other):
        if isinstance(other, Complex) or isinstance(other, complex):
            return self.real == other.real and self.imag == other.imag
        if isinstance(other, Real):
            return self.real == other and self.imag == 0
        else:
            raise TypeError(f"{other} must be a Complex object.")

    def __add__(self, other):
        if isinstance(other, Complex):
            return Complex(self.real + other.real, self.imag + other.imag)
        elif isinstance(other, Integer):
            return Complex(self.real + other.value, self.imag)
        elif isinstance(other, Real):
            return Complex(self.real + other, self.imag)
        elif isinstance(other, Matrix):
            return other + self
        else:
            raise TypeError(f"can't add Complex to object {other.__class__.__name__}.")

    def __mul__(self, other):
        if isinstance(other, Complex):
            return Complex(self.real * other.real - self.imag * other.imag, self.real * other.imag + self.imag * other.real)
        elif isinstance(other, Integer):
            return Complex(self.real * other.value, self.imag * other.value)
        elif isinstance(other, Real):
            return Complex(self.real * other, self.imag * other)
        elif isinstance(other, Matrix):
            return other * self
        else:
            raise TypeError(f"can't multiply Complex to object {other.__class__.__name__}.")

    def __abs__(self):
        return sqrt(self.real ** 2 + self.imag ** 2)

    def __neg__(self):
        return Complex(-self.real, -self.imag)

    def __sub__(self, other):
        return self + (-other)

    @classmethod
    def make_complex_from_string(cls, string:str) -> "Complex":
        """
        Creates a Complex number from the given string.
        string format: <imag>i + <real> or <imag>j + <real>.
        """
        assert type(string) == str

        parts = string.split('+')
        if 'i' in parts[0] or 'j' in parts[0]:
            imag = int(parts[0].strip()[:-1].strip())
            real = int(parts[1].strip())
        else:
            imag = int(parts[1].strip()[:-1].strip())
            real = int(parts[0].strip())

        return cls(real, imag)


class Matrix:
    """Matrix class"""

    def __init__(self, rows:int, cols:int, data:list[Integer | Complex]):
        assert type(rows) == type(cols) == int
        if rows <= 0 or cols <= 0:
            raise ValueError(f"rows and cols must be positive integers. you entered {rows} {cols}.")
        if not isinstance(data, list) or not len(data):
            raise ValueError(f"data must be a nonempty list.")
        self._rows = rows
        self._cols = cols
        self._data = data

    @property
    def rows(self):
        """The row of the matrix"""
        return self._rows

    @property
    def cols(self):
        """The row of the matrix"""
        return self._cols

    @property
    def data(self):
        """The row of the matrix"""
        return self._data

    @data.setter
    def data(self, new_data:list[Integer | Complex]):
        if len(new_data) != len(self.data):
            raise ValueError(f"data must be in the dimension of {self.rows}x{self.cols}.")
        else:
            self._data = new_data

    def __repr__(self):
        res = ""
        for i in range(self.rows):
            res += '\n'
            for j in range(self.cols):
                res += str(self.data[i*self.cols+j]) + " "
        return res

    def __getitem__(self, items):
        # it's enough for our purpose.
        # returns a row
        if type(items) == int:
            i = items
            if not 0 <= i < self.rows:
                raise IndexError(f"Index out of range. the limitation is {(0, self.rows)}.")
            row = i * self.cols
            return self.data[row:row+self.cols]

    @property
    def shape(self) -> tuple[int]:
        """describe the dimesion of the matrix."""
        return self.rows, self.cols

    @classmethod
    def make_matrix_from_string(cls, string:str) -> "Matrix":
        """
        Creates a Matrix object from the given string.
        - columns must be separated by spaces. 
        - rows must be separated by commas(,).
        - complex numbers must be in this format: <imag>i+<real> or <imag>j+<real> without any space.
        """
        assert type(string) == str
        rows = string.split(',')
        data = []
        for row in rows:
            cols = row.split()
            c = len(cols) # number of columns
            for num in cols:
                if 'i' in num or 'j' in num:
                    data.append(Complex.make_complex_from_string(num))
                else:
                    data.append(Integer.make_integer_from_string(num))
        
        return cls(len(rows), c, data)

    @staticmethod
    def make_unit_matrix(n:int):
        """Returns a unit matrix of dimesion n*n."""
        assert type(n) == int
        data = []

        for i in range(n**2):
            row, col = divmod(i, n) # returns (i//n, i%n)
            if row == col:
                data.append(1)
            else:
                data.append(0)

        return Matrix(n, n, data)

    @staticmethod
    def get_ith_row(matrix:"Matrix", i:int) -> list[Integer|Complex]:
        """returns the ith row of the given matrix."""
        assert type(i) == int
        if not isinstance(matrix, Matrix):
            raise TypeError("matrix must be an object of Matrix class.")
        cols = matrix.cols

        return matrix.data[i*cols:(i+1)*cols]

    @staticmethod
    def get_ith_col(matrix:"Matrix", i:int) -> list[Integer|Complex]:
        """returns the ith column of the given matrix."""
        assert type(i) == int
        if not isinstance(matrix, Matrix):
            raise TypeError("matrix must be an object of Matrix class.")

        data:list[Integer|Complex] = []
        cols = matrix.cols 
        for j, num in enumerate(matrix.data):
            if j % cols == i:
                data.append(num)

        return data

    @staticmethod
    def is_square_matrix(matrix:"Matrix") -> bool:
        """checks if the matrix is a square matrix."""
        if not isinstance(matrix, Matrix):
            raise TypeError("matrix must be an object of Matrix class.")
        
        return matrix.cols == matrix.rows

    @staticmethod
    def is_zero_matrix(matrix:"Matrix") -> bool:
        """returns true if the matrix is a zero matrix otherwise returns False."""
        if not isinstance(matrix, Matrix):
            raise TypeError("matrix must be an object of Matrix class.")

        for d in matrix.data:
            if d != 0:
                return False
        else:
            return True

    @staticmethod
    def is_unit_matrix(matrix:"Matrix") -> bool:
        """returns true if the matrix is a unit matrix otherwise returns False."""
        if not isinstance(matrix, Matrix):
            raise TypeError("matrix must be an object of Matrix class.")

        # make sure the matrix is a square matrix.
        if not Matrix.is_square_matrix(matrix):
            return False

        data = matrix.data
        n = matrix.rows # n = rows = cols.
        for i in range(n**2):
            r, c = divmod(i, n) # (i//rows, i%rows)
            if r == c and data[i] != 1:
                return False
            elif r != c and data[i] != 0:
                return False
        else:
            return True
    
    @staticmethod
    def is_top_triangular_matrix(matrix:"Matrix") -> bool:
        """returns true if the matrix is a top triangular matrix otherwise returns False."""
        if not isinstance(matrix, Matrix):
            raise TypeError("matrix must be an object of Matrix class.")

        # make sure the matrix is a square matrix.
        if not Matrix.is_square_matrix(matrix):
            return False

        data = matrix.data
        n = matrix.rows # n = cols = rows
        for i in range(n**2):
            r, c = divmod(i, n)
            if r > c and data[i] != 0:
                return False
        else:
            return True

    @staticmethod
    def is_bottom_triangular_matrix(matrix:"Matrix") -> bool:
        """returns true if the matrix is a bottom triangular matrix otherwise returns False."""
        if not isinstance(matrix, Matrix):
            raise TypeError("matrix must be an object of Matrix class.")

        # make sure the matrix is a square matrix.
        if not Matrix.is_square_matrix(matrix):
            return False

        data = matrix.data
        n = matrix.rows # n = cols = rows
        for i in range(n**2):
            r, c = divmod(i, n)
            if r < c and data[i] != 0:
                return False
        else:
            return True

    @staticmethod
    def matrix_multiply(mat1:"Matrix", mat2:"Matrix"):
        """
        Multiplies mat1 to mat2.
        columns of mat1 must be equal to rows of mat2.
        """
        if mat1.cols != mat2.rows:
            raise ValueError(f"can't multiply matrix of shape {mat1.shape} and matrix of shape {mat2.shape}.")

        new_data = []

        for i in range(mat1.rows):
            for j in range(mat2.cols):
                new_member = 0
                for k in range(mat2.rows):
                    new_member += mat1[i][k] * mat2[k][j]
                new_data.append(new_member)
                
        return Matrix(mat1.rows, mat2.cols, new_data) 

    def __add__(self, other):
        if isinstance(other, Matrix):
            if other.shape == self.shape:
                new_data = []
                for i in range(self.rows):
                    for j in range(self.cols):
                        k = i * self.cols + j # index for new_data
                        new_data.append(self.data[k] + other.data[k])
                return Matrix(self.rows, self.cols, new_data)
            else:
                raise ValueError(f"can't add matrix of shape {other.shape} to a matrix of shape {self.shape}.")
        
        elif isinstance(other, Integer) or isinstance(other, Complex):
            new_data = []
            for i in range(self.rows):
                for j in range(self.cols):
                    k = i * self.cols + j
                    new_data.append(other + self.data[k])
            return Matrix(self.rows, self.cols, new_data)
        
        else:
            raise TypeError(f"can't add matrix to object {other.__class__.__name__}.")

    def __mul__(self, other):
        if isinstance(other, Matrix):
            return Matrix.matrix_multiply(self, other)
        elif isinstance(other, Complex) or isinstance(other, Integer):
            new_data = []
            for i in range(self.rows):
                for j in range(self.cols):
                    k = i * self.cols + j
                    new_data.append(other * self.data[k])
            return Matrix(self.rows, self.cols, new_data)
        else:
            raise TypeError(f"can't multiply matrix to object {other.__class__.__name__}.")

    def __neg__(self):
        data = [-d for d in self.data]
        return Matrix(self.rows, self.cols, data)

    def __sub__(self, other):
        return self + (-other)

def multiply(obj1, ojb2):
    """Multiplies two given objects."""
    return obj1 * ojb2
