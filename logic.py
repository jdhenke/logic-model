#!/usr/bin/python

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

def main():
    '''walk through an example'''

    c1 = Claim("Congressman C supports policy P")
    c2 = Claim("Yeah, he voted for bill B")
    c3 = Claim("No way, his hometown is X")
    r1 = Pro(c2, c1) #: c2 correct fact which supports the claim
    r2 = Con(c3, c1) #: c3 correct fact that's maybe not applicable
    print "One pro and one con yields:\n\t%s" % c1

    # Now, c3 is a true statement, however people will have different opinions
    # on how it relates to the argument. They are in essence for or against
    # it's **Relation** to the claim.

    print 'Initial relation weight of con: %s' % r2.get_weight()

    c4 = Claim("I don't like stereotyping")
    r3 = Con(c4, r2)
    c5 = Claim("This city historically produces many P supporters")
    r4 = Pro(c5, r2)

    print "Weakening the weight of the Con's **Relation** yields:\n\t%s" % c1
    print 'Reduced relation weight of con: %s' % r2.get_weight()

    # It is weakened becuase, by default, assertions are accepted as 
    # fully weighted. Once they have children pros or cons, those children
    # dictate their parent's weight.

    # Intuitively, this should all be sensible. Reducing the weight of
    # an argument in conflict with the claim should strengthen the claim.

    # Also, be careful of notation. Con as described above is the Claim,
    # but note that the class itself is a Relation.

class Assertion(object):
    '''fundamental unit of an argument'''
    
    def __init__(self):
        self.relations = set() #: relations to children only
    
    def get_weight(self):
        
        actual_weight = 0
        possible_weight = 0
        for r in self.relations:
            actual_weight += r.get_weight() * r.get_output()
            possible_weight += r.get_weight()
        if possible_weight == 0:
            return 1.0
        return actual_weight / possible_weight
        
    def add_relation(self, relation):
        self.relations.add(relation)

class Claim(Assertion):
    '''primitive assertion containing text'''
    
    def __init__(self, text):
        super(Claim, self).__init__()
        self.text = text

    def __str__(self):
        return '%s has weight %.2f' % (self.text, self.get_weight())

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
    
    def get_output(self):
        return self.child.get_weight()

    def __str__(self):
        return '%s implies %s with weight %.2f' %\
            (self.child.get_text(), self.parent.get_text(), self.get_weight())
    
    def get_text(self):
        return '(%s ==> %s)' % (self.child.get_text(), self.parent.get_text())

class Con(Relation):
    '''child refutes parent'''
    
    def get_output(self):
        return 1.0 - self.child.get_weight()

    def __str__(self):
        return '%s implies NOT %s with weight %.2f' %\
            (self.child.get_text(), self.parent.get_text(), self.get_weight())

    def get_text(self):
        return '(%s ==> NOT(%s))' % (self.child.get_text(), self.parent.get_text())

if __name__ == '__main__':
    main()
