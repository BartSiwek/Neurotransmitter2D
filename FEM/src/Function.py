class FunctionMultiplication:
    def __init__(self, f1, f2):
        self.f1 = f1
        self.f2 = f2    
    def __str__(self):
        return "(" + str(self.f1) + ") * (" + str(self.f2) + ")"
    def __call__(self, x, y):
        return self.f1(x,y) * self.f2(x,y)
    def __add__(self, other):
        return FunctionSum(self, other)
    def __sub__(self, other):
        return FunctionSubstitution(self, other)
    def __mul__(self, other):
        return FunctionMultiplication(self, other)

class FunctionSubstitution:
    def __init__(self, f1, f2):
        self.f1 = f1
        self.f2 = f2    
    def __str__(self):
        return "(" + str(self.f1) + ") - (" + str(self.f2) + ")"
    def __call__(self, x, y):
        return self.f1(x,y) - self.f2(x,y)
    def __add__(self, other):
        return FunctionSum(self, other)
    def __sub__(self, other):
        return FunctionSubstitution(self, other)
    def __mul__(self, other):
        return FunctionMultiplication(self, other)

class FunctionSum:
    def __init__(self, f1, f2):
        self.f1 = f1
        self.f2 = f2
    def __str__(self):
        return str(self.f1) + " + " + str(self.f2)
    def __call__(self, x, y):
        return self.f1(x,y) + self.f2(x,y)
    def __add__(self, other):
        return FunctionSum(self, other)
    def __sub__(self, other):
        return FunctionSubstitution(self, other)
    def __mul__(self, other):
        return FunctionMultiplication(self, other)
    
class ConstantFunction:
    def __init__(self, c):
        self.c = float(c)
    def __str__(self):
        return str(self.c)
    def __call__(self, x, y):
        return self.c
    def __add__(self, other):
        return FunctionSum(self, other)
    def __sub__(self, other):
        return FunctionSubstitution(self, other)
    def __mul__(self, other):
        return FunctionMultiplication(self, other)
    
class PositivePartFunction:
    def __init__(self, f):
        self.f = f
    def __str__(self):
        return "(" + str(self.f) + ")^+"
    def __call__(self, x, y):
        return max(0, self.f(x,y))
    def __add__(self, other):
        return FunctionSum(self, other)
    def __sub__(self, other):
        return FunctionSubstitution(self, other)
    def __mul__(self, other):
        return FunctionMultiplication(self, other)
    
class FunctionWrapper:
    def __init__(self, f, desc):
        self.f = f
        self.desc = desc
    def __str__(self):
        if self.desc is None:
            return str(self.f)
        return self.desc
    def __call__(self, x, y):
        return self.f(x,y)
    def __add__(self, other):
        return FunctionSum(self, other)
    def __sub__(self, other):
        return FunctionSubstitution(self, other)
    def __mul__(self, other):
        return FunctionMultiplication(self, other)