import unittest
from matrix import Matrix, Integer, Complex

class TestMatrix(unittest.TestCase):
    def test_make_unit_matrix(self):
        res = Matrix.make_unit_matrix(3)
        self.assertListEqual(res.data, [1, 0, 0, 0, 1, 0, 0, 0 ,1])

        self.assertRaises(ValueError, Matrix.make_unit_matrix, 0)

    def test_get_ith_row(self):
        mat = Matrix(3, 3, [1, 2, 3, 4, 5, 6, 7, 8, 9])
        res = Matrix.get_ith_row(mat, 1)
        self.assertListEqual(res, [4, 5, 6])

    def test_get_ith_col(self):
        mat = Matrix(2, 3, [1, 2, 3, 4, 5, 6])
        res = Matrix.get_ith_col(mat, 1)
        self.assertListEqual(res, [2, 5])
    
    def test_is_zero_matrix(self):
        mat = Matrix(2, 3, [0, 0, 0, 0.0, Complex(0, 0), 0])
        res = Matrix.is_zero_matrix(mat)
        self.assertEqual(res, True)
        mat = Matrix(3, 3, [0, 0, 0, 0, 0, 0, 0, 0, 9])
        res = Matrix.is_zero_matrix(mat)
        self.assertEqual(res, False)

    def test_is_unit_matrix(self):
        mat = Matrix.make_unit_matrix(3)
        res = Matrix.is_unit_matrix(mat)
        self.assertEqual(res, True)

        mat = Matrix(2, 3, [1, 0, 0, 0, 1, 0])
        res = Matrix.is_unit_matrix(mat)
        self.assertEqual(res, False)

        mat = Matrix(3, 3, 
        [1, 0, 0,
         0, 1, 0, 
         -1, 0, 1])
        
        res = Matrix.is_unit_matrix(mat)
        self.assertEqual(res, False)

        mat = Matrix(1, 1, [1])
        res = Matrix.is_unit_matrix(mat)
        self.assertEqual(res, True)

    def test_is_top_triangular_matrix(self):
        mat = Matrix(3, 3, 
        [1, 2, 3,
         0, 4, 5, 
         0, 0, 6])
        res = Matrix.is_top_triangular_matrix(mat)
        self.assertEqual(res, True)

        mat = Matrix(3, 3, 
        [1, 2, 3,
         0, 4, 5, 
         0, 1, 6])

        res = Matrix.is_top_triangular_matrix(mat)
        self.assertEqual(res, False)
        
        mat = Matrix(2, 3, 
        [1, 2, 3,
         0, 4, 5])

        res = Matrix.is_top_triangular_matrix(mat)
        self.assertEqual(res, False)

    def test_is_bottom_triangular_matrix(self):
        mat = Matrix(3, 3, 
        [1, 0, 0,
         3, 4, 0,
         2, 1, 6])
        res = Matrix.is_bottom_triangular_matrix(mat)
        self.assertEqual(res, True)

        mat = Matrix(3, 3, 
        [1, 0, 0,
         0, 4, 5, 
         0, 1, 6])

        res = Matrix.is_bottom_triangular_matrix(mat)
        self.assertEqual(res, False)
        
        mat = Matrix(2, 3, 
        [1, 0, 0,
         0, 4, 5])

        res = Matrix.is_bottom_triangular_matrix(mat)
        self.assertEqual(res, False)

    def test_matrix_from_string(self):
        string = "1 2i+3 0j+2,2 3 0,2j+0 3 2"
        mat = Matrix.make_matrix_from_string(string)
        expectation = [Integer(1), Complex(3, 2), Complex(2, 0), Integer(2), Integer(3), Integer(0), Complex(0, 2), Integer(3), Integer(2)]
        self.assertListEqual(mat.data, expectation)

    def test_addition(self):
        mat = Matrix(3, 3, 
        [1, 2, Complex(imag=3),
        4, 5, 6,
        7, 8, 9])
        com = Complex(1, 2)
        int_ = Integer(2)

        self.assertListEqual((mat + mat).data, [2, 4, Complex(imag=6), 8, 10, 12, 14, 16, 18])
        self.assertListEqual((mat + int_).data, [3, 4, Complex(imag=3, real=2), 6, 7, 8, 9, 10, 11])
        self.assertListEqual((mat + com).data, 
        [Complex(2, 2), Complex(3, 2), Complex(1, 5),
        Complex(5, 2), Complex(6, 2), Complex(7, 2), 
        Complex(8, 2), Complex(9, 2), Complex(10, 2)])

        self.assertListEqual((int_ + mat).data, [3, 4, Complex(imag=3, real=2), 6, 7, 8, 9, 10, 11])
        self.assertListEqual((com + mat).data, 
        [Complex(2, 2), Complex(3, 2), Complex(1, 5),
        Complex(5, 2), Complex(6, 2), Complex(7, 2), 
        Complex(8, 2), Complex(9, 2), Complex(10, 2)])

    def test_matrix_multiply(self):
        mat1 = Matrix(2, 3, data=
        [1, 2, 3,
        4, 5, 6])
        mat2 = Matrix(3, 2, data=
        [1, 2,
        3, 4, 
        5, 6])
        self.assertListEqual(Matrix.matrix_multiply(mat1, mat2).data, [22, 28, 49, 64])

        mat2 = Matrix(2, 3, data=
        [1, 2, 3,
        4, 5, 6])

        self.assertRaises(ValueError, Matrix.matrix_multiply, mat1, mat2)

    def test_multiplication(self):
        mat = Matrix(3, 3, 
        [1, 2, Complex(imag=3),
        4, 5, 6,
        7, 8, 9])
        com = Complex(1, 2)
        int_ = Integer(2)

        self.assertListEqual((mat * int_).data, [2, 4, Complex(imag=6), 8, 10, 12, 14, 16, 18])
        self.assertListEqual((mat * com).data, 
        [Complex(1, 2), Complex(2, 4), Complex(-6, 3),
        Complex(4, 8), Complex(5, 10), Complex(6, 12), 
        Complex(7, 14), Complex(8, 16), Complex(9, 18)])

        self.assertListEqual((int_ * mat).data, [2, 4, Complex(imag=6), 8, 10, 12, 14, 16, 18])
        self.assertListEqual((com * mat).data, 
        [Complex(1, 2), Complex(2, 4), Complex(-6, 3),
        Complex(4, 8), Complex(5, 10), Complex(6, 12), 
        Complex(7, 14), Complex(8, 16), Complex(9, 18)])

    def test_subtraction(self):
        mat = Matrix(3, 3, 
        [1, 2, Complex(imag=3),
        4, 5, 6,
        7, 8, 9])
        com = Complex(1, 2)
        int_ = Integer(2)

        self.assertEqual(Matrix.is_zero_matrix(mat - mat), True)
        self.assertListEqual((mat - int_).data, [-1, 0, Complex(imag=3, real=-2), 2, 3, 4, 5, 6, 7])
        self.assertListEqual((mat - com).data, 
        [Complex(0, -2), Complex(1, -2), Complex(-1, 1),
        Complex(3, -2), Complex(4, -2), Complex(5, -2), 
        Complex(6, -2), Complex(7, -2), Complex(8, -2)])

        self.assertListEqual((int_ - mat).data, [1, 0, Complex(imag=-3, real=2), -2, -3, -4, -5, -6, -7])
        self.assertListEqual((com - mat).data, 
        [Complex(0, 2), Complex(-1, 2), Complex(1, -1),
        Complex(-3, 2), Complex(-4, 2), Complex(-5, 2), 
        Complex(-6, 2), Complex(-7, 2), Complex(-8, 2)])

if __name__ == '__main__':
    unittest.main(verbosity=2)
