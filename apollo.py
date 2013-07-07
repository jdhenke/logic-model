import sympy
from sympy.core.numbers import *

'''
Copyright (c) 2013 Joseph Henke

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
copies of the Software, and to permit persons to whom the Software is furnished
to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
SOFTWARE.

'''

class Assertion(object):
    '''fundamental unit of an argument'''

    num = 0
    
    def __init__(self):
        self.relations = set() #: relations to children only
        self.weight = sympy.Symbol(str(Assertion.num))
        Assertion.num += 1
    
    def get_weight(self):

        # get all assertions involved
        all_assertions = {self}
        queue = [self]
        while len(queue) > 0:
            assertion = queue.pop()
            for relation in assertion.relations:
                if relation not in all_assertions:
                    queue.append(relation)
                    all_assertions.add(relation)
                if relation.child not in all_assertions:
                    queue.append(relation.child)
                    all_assertions.add(relation.child)

        # assemble all equations
        equations = set([a.get_equation() for a in all_assertions])
        # print equations

        # solve them
        solutions = sympy.solve(equations, dict=True)
        # print solutions
        # print solutions
        if solutions == False:
            raise Exception("Contradiction found! Here are the equations\n\t%s" % (equations, ))
        if len(solutions) == 0:
            print 'No contradiction found'
            return None
            raise Exception("No solutions found! Here are the equations\n\t%s" % (equations, ))
        if len(solutions) > 1:
            print 'MULTIPLE SOLUTIONS FOUND'
            return None
            raise Exception("Multiple solutions found! Here are the equations\n\t%s\nHere are the solutions\n\t%s" % (equations, solutions))
        solution = solutions[0]
        if self.weight not in solution:
            return None
        else:
            answer = solution[self.weight]
            if isinstance(answer, Float) or\
                isinstance(answer, Zero):
                return answer
            else:
                print type(answer)
                print "WARNING: [%s]" % (answer, )
                return None

    def get_equation(self):
        if len(self.relations) == 0:
            return sympy.Eq(1.0, self.weight)
        weights = 0
        potential = 0
        for relation in self.relations:
            weights += relation.output
            potential += relation.weight
        return sympy.Eq(self.weight, weights / potential)

        
    def add_relation(self, relation):
        self.relations.add(relation)

class Claim(Assertion):
    '''primitive assertion containing text'''
    
    def __init__(self, text):
        super(Claim, self).__init__()
        self.text = text

    def __str__(self):
        return '%s has weight %.2f' % (self.text, self.get_weight())

    def get_weight_variable(self):
        return sympy.Symbol(self.text)

    def get_text(self):
        return self.text

class Relation(Assertion):
    '''relates child to parent in some way'''
    
    def __init__(self, child, parent):
        super(Relation, self).__init__()
        self.child = child
        self.parent = parent
        self.parent.add_relation(self)

class Pro(Relation):
    '''child supports parent'''

    def __init__(self, child, parent):
        super(Pro, self).__init__(child, parent)
        self.output = self.weight * child.weight
    
    def get_output(self):
        return self.child.get_weight()

    def get_text(self):
        return "(%s ==> %s)" % (self.child.get_text(), self.parent.get_text(), )

class Con(Relation):
    '''child refutes parent'''

    def __init__(self, child, parent):
        super(Con, self).__init__(child, parent)
        self.output = self.weight * (1.0-child.weight)
    
    def get_output(self):
        return 1.0 - self.child.get_weight()

    def get_text(self):
        return "(%s ==> !%s)" % (self.child.get_text(), self.parent.get_text(), )

if __name__ == '__main__':
    main()
