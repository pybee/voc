from ..utils import TranspileTestCase

from unittest import expectedFailure


class ComparisonTests(TranspileTestCase):
    def test_is(self):
        self.assertCodeExecution("""
            x = 1234
            if x is 1234:
                print('True')
            else:
                print('False')
            """)

        self.assertCodeExecution("""
            x = 1234
            if x is 2345:
                print('True')
            else:
                print('False')
            """)

        self.assertCodeExecution("""
            x = None
            if x is None:
                print('True')
            else:
                print('False')
            """)

        self.assertCodeExecution("""
            x = 1234
            if x is None:
                print('True')
            else:
                print('False')
            """)

    def test_is_not(self):
        self.assertCodeExecution("""
            x = 1234
            if x is not 2345:
                print('True')
            else:
                print('False')
            """)

        self.assertCodeExecution("""
            x = 1234
            if x is not 1234:
                print('True')
            else:
                print('False')
            """)

        self.assertCodeExecution("""
            x = 1234
            if x is not None:
                print('True')
            else:
                print('False')
            """)

        self.assertCodeExecution("""
            x = None
            if x is not None:
                print('True')
            else:
                print('False')
            """)

    def test_lt(self):
        self.assertCodeExecution("""
            x = 1
            if x < 5:
                print('True')
            else:
                print('False')
            """)

        self.assertCodeExecution("""
            x = 5
            if x < 5:
                print('True')
            else:
                print('False')
            """)

        self.assertCodeExecution("""
            x = 10
            if x < 5:
                print('True')
            else:
                print('False')
            """)

    def test_le(self):
        self.assertCodeExecution("""
            x = 1
            if x <= 5:
                print('True')
            else:
                print('False')
            """)

        self.assertCodeExecution("""
            x = 5
            if x <= 5:
                print('True')
            else:
                print('False')
            """)

        self.assertCodeExecution("""
            x = 10
            if x <= 5:
                print('True')
            else:
                print('False')
            """)

    def test_gt(self):
        self.assertCodeExecution("""
            x = 10
            if x > 5:
                print('True')
            else:
                print('False')
            """)

        self.assertCodeExecution("""
            x = 5
            if x > 5:
                print('True')
            else:
                print('False')
            """)

        self.assertCodeExecution("""
            x = 1
            if x > 5:
                print('True')
            else:
                print('False')
            """)

    def test_ge(self):
        self.assertCodeExecution("""
            x = 10
            if x >= 5:
                print('True')
            else:
                print('False')
            """)

        self.assertCodeExecution("""
            x = 5
            if x >= 5:
                print('True')
            else:
                print('False')
            """)

        self.assertCodeExecution("""
            x = 1
            if x >= 5:
                print('True')
            else:
                print('False')
            """)

    def test_eq(self):
        self.assertCodeExecution("""
            x = 10
            if x == 5:
                print('True')
            else:
                print('False')
            """)

        self.assertCodeExecution("""
            x = 5
            if x == 5:
                print('True')
            else:
                print('False')
            """)

    def test_ne(self):
        self.assertCodeExecution("""
            x = 5
            if x != 5:
                print('True')
            else:
                print('False')
            """)

        self.assertCodeExecution("""
            x = 10
            if x != 5:
                print('True')
            else:
                print('False')
            """)

    # next few tests from cpython's Lib/test/test_compare.py @ v3.6.0
    def test_comparisons(self):
        self.assertCodeExecution("""
            class Cmp:
                def __init__(self,arg):
                    self.arg = arg
                def __repr__(self):
                    return '<Cmp %s>' % self.arg
                def __eq__(self, other):
                    return self.arg == other
            class Empty:
                def __repr__(self):
                    return '<Empty>'

            set1 = [2, 2.0, 2, 2+0j, Cmp(2.0)]
            set2 = [[1], (3,), None, Empty()]
            candidates = set1 + set2
            for a in candidates:
                for b in candidates:
                    print(a == b)
            """)

    # list object does not have insert() implemented yet
    @expectedFailure
    def test_id_comparisons(self):
        self.assertCodeExecution("""
            class Empty:
                def __repr__(self):
                    return '<Empty>'

            # Ensure default comparison compares id() of args
            L = []
            for i in range(10):
                L.insert(len(L)//2, Empty())
            for a in L:
                for b in L:
                    print(a == b, id(a) == id(b), 'a=%r, b=%r' % (a, b))
            """)

    def test_ne_defaults_to_not_eq(self):
        self.assertCodeExecution("""
            class Cmp:
                def __init__(self,arg):
                    self.arg = arg

                def __repr__(self):
                    return '<Cmp %s>' % self.arg

                def __eq__(self, other):
                    return self.arg == other

            a = Cmp(1)
            b = Cmp(1)
            c = Cmp(2)
            print(a == b) # True
            print(a != b) # False
            print(a != c) # True
            """)

    def test_ne_high_priority(self):
        self.assertCodeExecution("""
            # object.__ne__() should allow reflected __ne__() to be tried
            calls = []
            class Left:
                # Inherits object.__ne__()
                def __eq__(*args):
                    calls.append('Left.__eq__')
                    return NotImplemented
            class Right:
                def __eq__(*args):
                    calls.append('Right.__eq__')
                    return NotImplemented
                def __ne__(*args):
                    calls.append('Right.__ne__')
                    return NotImplemented
            Left() != Right()
            print(calls) # ['Left.__eq__', 'Right.__ne__']
            """)

    def test_ne_low_priority(self):
        self.assertCodeExecution("""
            # object.__ne__() should not invoke reflected __eq__()
            calls = []
            class Base:
                # Inherits object.__ne__()
                def __eq__(*args):
                    calls.append('Base.__eq__')
                    return NotImplemented
            class Derived(Base):  # Subclassing forces higher priority
                def __eq__(*args):
                    calls.append('Derived.__eq__')
                    return NotImplemented
                def __ne__(*args):
                    calls.append('Derived.__ne__')
                    return NotImplemented
            print(Base() != Derived())
            print(calls) # ['Derived.__ne__', 'Base.__eq__']
            """)

    # lambda not implemented yet
    @expectedFailure
    def test_other_delegation(self):
        self.assertCodeExecution("""
            # No default delegation between operations except __ne__()
            ops = (
                ('__eq__', lambda a, b: a == b),
                ('__lt__', lambda a, b: a < b),
                ('__le__', lambda a, b: a <= b),
                ('__gt__', lambda a, b: a > b),
                ('__ge__', lambda a, b: a >= b),
            )
            for name, func in ops:
                def unexpected(*args):
                    print('Unexpected operator method called')
                class C:
                    __ne__ = unexpected
                for other, _ in ops:
                    if other != name:
                        setattr(C, other, unexpected)
                if name == '__eq__':
                    print(func(C(), object())) # False
                else:
                    try:
                        print(func(C(), object()))
                    except TypeError as err:
                        print(err)
            """)

    # lambda not implemented yet
    @expectedFailure
    def test_issue_1393(self):
        self.assertCodeExecution("""
            class Anything:
                def __eq__(self, other):
                    return True

                def __ne__(self, other):
                    return False

            x = lambda: None
            print(x == Anything())
            print(Anything() == x)
            y = object()
            print(y == Anything())
            print(Anything() == y)
            """)
