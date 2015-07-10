import sympy
from sympy import Eq, S

class Assertion(object):
    '''fundamental unit of an argument'''

    # global int that's incremented to uniquely track assertions
    num = 0

    def __init__(self):
        self.relations = set() #: relations to children only
        self.weight = sympy.Symbol(str("v%s" % (Assertion.num, ))) #: sympy truth variable
        Assertion.num += 1

    def get_weight(self):
        '''returns a number in [0,1] indicating this assertion's truth'''

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

        # assemble system of equations defining weights of all assertions
        equations = [a.get_equation() for a in all_assertions]

        # assemble weight variables of all assertions
        weights = [a.weight for a in all_assertions]

        # attempt to solve the system equating weights and formulas
        solutions = sympy.solve(equations, weights, dict=True)

        # interpret solution results
        if not isinstance(solutions, list):
            raise Exception("Unknown solution type: %s solution: %s" % \
                (type(solution), solution))
        if len(solutions) == 0:
            raise Exception("No solutions found. Equations: %s" % \
                (equations, ))
        if len(solutions) > 1:
            raise Exception("Multiple solutions found. \
                Equations: %s Solutions: %s" % (equations, solutions))

        # interpret single solution
        solution = solutions[0]
        if self.weight not in solution:
            raise Exception("Weight variable %s not in solution %s" % (self.weight, solution))
        answer = solution[self.weight]

        #winning
        return answer

    def get_equation(self):
        '''returns the equation defining this assertion's weight'''

        # if no relations point to this assertion, we assume it is true
        if len(self.relations) == 0:
            return Eq(self.weight, S.One)

        # if we have relations pointing to this assertion, we define this
        # assertion's weight as the average of each relation's support scaled by
        # each relation's own weight
        support = sum([r.output for r in self.relations])
        possible_support = sum([r.weight for r in self.relations])
        return Eq(self.weight, support / possible_support)

    def add_relation(self, relation):
        '''makes this assertion aware that this relation is pointing at it'''
        self.relations.add(relation)

class Claim(Assertion):
    '''primitive assertion containing text'''

    def __init__(self, text):
        super(Claim, self).__init__()
        self.text = text

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

class Con(Relation):
    '''child refutes parent'''

    def __init__(self, child, parent):
        super(Con, self).__init__(child, parent)
        self.output = self.weight * (S.One - child.weight)

if __name__ == '__main__':

    print "Creating a simple argument..."

    # create a basic claim
    c = Claim('main claim')
    # add a few supporting claims
    r1 = Pro(Claim('supporting claim 1'), c)
    _ = Pro(Claim('supporting claim 2'), c)
    # add a refuting claim
    _ = Con(Claim('refuting claim 1'), c)
    # print the derived weight of the original claim
    print "Main Claim's Derived Weight: %s" % (c.get_weight(), )
    # ==> 2/3

    print "Modifying the debate..."

    # now debate over how reasonable it is to support c with supporting claim 1
    _ = Con(Claim('refuting claim 2'), r1)
    _ = Con(Claim('refuting claim 3'), r1)
    _ = Pro(Claim('supporting claim 4'), r1)
    # print the new derived weight of the original claim
    print "Main Claim's Derived Weight: %s" % (c.get_weight(), )
    # ==> 4/7
