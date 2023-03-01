import unittest
import math
import geometry as gt


class TestGeometry(unittest.TestCase):
    def test_create_shape(self):
        # triangle
        self.assertRaises(ValueError, gt.Triangle, 1, 1, 2)
        self.assertRaises(ValueError, gt.Triangle, 2, 1, 1)
        self.assertRaises(ValueError, gt.Triangle, -1, 2, 2)

        # circle
        self.assertRaises(ValueError, gt.Circle, 0)
        self.assertRaises(ValueError, gt.Circle, -1)

        # rectangle
        self.assertRaises(ValueError, gt.Rectangle, 0, 10)
        self.assertRaises(ValueError, gt.Rectangle, 10, -1)

        # Square
        self.assertRaises(ValueError, gt.Square, 0)
        self.assertTrue(isinstance(gt.Square(1), gt.Rectangle))

        # Equilateral_Triangle
        self.assertRaises(ValueError, gt.Equilateral_Triangle, -1)
        self.assertTrue(isinstance(gt.Equilateral_Triangle(3), gt.Triangle))
        
        # Regular_Pantagon
        self.assertRaises(ValueError, gt.Regular_Pantagon, 0)

    def test_str_mode(self):
        
        # It's is important because i'll use this to in eval function. so it should be exactly like this.
        # <Name>(param1, param2, param3, ...)
        
        # triangle
        tri = gt.Triangle(3, 3, 2)
        self.assertEqual(str(tri), "Triangle(3, 3, 2)")

        # Equilateral_Triangle
        e_tri = gt.Equilateral_Triangle(3)
        self.assertEqual(str(e_tri), "Equilateral_Triangle(3)")

        # Circle
        cir = gt.Circle(4)
        self.assertEqual(str(cir), "Circle(4)")

        # Rectangle
        rec = gt.Rectangle(4, 5)
        self.assertEqual(str(rec), "Rectangle(4, 5)")

        # Square
        sq = gt.Square(4)
        self.assertEqual(str(sq), "Square(4)")

        # Regular_Pantagon
        rp = gt.Regular_Pantagon(3)
        self.assertEqual(str(rp), "Regular_Pantagon(3)")

    def test_get_perimeter(self):
        # circle
        cir = gt.Circle(3)
        self.assertAlmostEqual(cir.get_perimeter(), 2 * math.pi * 3, 5)

        # triangle
        tri = gt.Triangle(2, 3, 3)
        self.assertEqual(tri.get_perimeter(), 8)

        # Equilateral_Triangle
        e_tri = gt.Equilateral_Triangle(4)
        self.assertEqual(e_tri.get_perimeter(), 12)

        # Rectangle
        rec = gt.Rectangle(3, 4)
        self.assertEqual(rec.get_perimeter(), 14)

        # Square
        sq = gt.Square(3)
        self.assertEqual(sq.get_perimeter(), 12)

        # Regular_Pantagon
        rp = gt.Regular_Pantagon(4)
        self.assertEqual(rp.get_perimeter(), 20)


    def test_get_area(self):
        # circle
        cir = gt.Circle(3)
        self.assertAlmostEqual(cir.get_area(), math.pi * 3 ** 2, 5)

        # triangle
        tri = gt.Triangle(2, 3, 3)
        self.assertAlmostEqual(tri.get_area(), 2.8284271247462, 5)

        # Equilateral_Triangle
        e_tri = gt.Equilateral_Triangle(4)
        self.assertAlmostEqual(e_tri.get_area(), 6.9282032302755, 5)

        # Rectangle
        rec = gt.Rectangle(3, 4)
        self.assertEqual(rec.get_area(), 12)

        # Square
        sq = gt.Square(3)
        self.assertEqual(sq.get_area(), 9)

        # Regular_Pantagon
        rp = gt.Regular_Pantagon(4)
        self.assertAlmostEqual(rp.get_area(), 27.52764, 5)

    def test_get_largest_shape_by_area(self):
        cir = gt.Circle(2)
        sq = gt.Square(4) # largest
        rec = gt.Rectangle(3, 4)
        sh_lst = gt.ShapeList(cir, sq, rec)
        self.assertEqual(sh_lst.get_largest_shape_by_area(), sq)

    def test_get_largest_shape_by_perimeter(self):
        tri = gt.Triangle(2, 3, 3)
        cir = gt.Circle(2)
        rp = gt.Regular_Pantagon(3) # largest
        sh_lst = gt.ShapeList(tri, cir, rp)
        self.assertEqual(sh_lst.get_largest_shape_by_perimeter(), rp)

    def test_add_shape(self):
        new_shape = gt.Circle(3)
        sh_lst = gt.ShapeList(new_shape)
        sh_lst.add_shape(new_shape)
        self.assertEqual(sh_lst.shapes, [new_shape, new_shape])



if __name__ == '__main__':
    unittest.main(verbosity=2)
