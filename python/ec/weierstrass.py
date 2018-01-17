
class EllipticCurve(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

        self.discriminant = -16 * (4 * a**3 + 27 * b**2)
        if not self.isSmooth():
            raise RuntimeError("The curve %s is not smooth!" % self)

    def isSmooth(self):
        return self.discriminant != 0

    def testPoint(self, x, y):
        return y**2 == x**3 + self.a * x + self.b

    def __str__(self):
        return 'y^2 = x^3 + %Gx + %G' % (self.a, self.b)

    def __eq__(self, other):
        return (self.a, self.b) == (other.a, other.b)

class Point(object):
    def __init__(self, curve, x, y):
        self.curve = curve
        self.x = x
        self.y = y

        if not curve.testPoint(x, y):
            raise RuntimeError("The point %s is not on the given curve %s" % (self, curve))

    def __neg__(self):
        return Point(self.curve, self.x, -self.y)

    def __sub__(self, Q):
        return self + -Q

    def __mul__(self, n):
        if not isinstance(n, int):
            raise RuntimeError("Can't scale a point by something which isn't an int")

        if n < 0:
            return -self * -n

        if n == 0:
            return Ideal(self.curve)

        Q = self
        R = self if n & 1 == 1 else Ideal(self.curve)

        i = 2
        while i <= n:
            Q += Q
            if n & i == i:
                R = Q + R
            i = i << 1
        return R

    def __rmul__(self, n):
        return self * n

    def __add__(self, Q):
        if isinstance(Q, Ideal):
            return self

        x_1, y_1, x_2, y_2 = self.x, self.y, Q.x, Q.y

        if (x_1, y_1) == (x_2, y_2):
            if y_1 == 0:
                return Ideal(self.curve)

            m = (3 * x_1**2 + self.curve.a) / (2 * y_1)
        else:
            if x_1 == x_2:
                return Ideal(self.curve) # vertical line

            # slope of the secant line
            m = (y_2 - y_1) / (x_2 - x_1)

        x_3 = m**2 - x_2 - x_1
        y_3 = m * (x_3 - x_1) + y_1
        return Point(self.curve, x_3, -y_3)

class Ideal(object):
    def __init__(self, curve):
        self.curve = curve

    def __str__(self):
        return "Ideal"

    def __neg__(self):
        return self

    def __add__(self, Q):
        return Q

    def __mul__(self, n):
        if not isinstance(n, int):
            raise RuntimeError("Can't scale a point by something which isn't an int")
        return self

