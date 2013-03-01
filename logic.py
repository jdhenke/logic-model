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

    # Start with basic structure:
    # A supports C
    # B refutes C
    a = Claim("A")
    b = Claim("B")
    c = Claim("C")
    i1 = Implies(a, c)
    i2 = ImpliesNot(b, c)
    print 'Basic Structure...'
    print '\t%s' % (c, )
    
    # Now, we assert the ImpliesNot from b to c is false
    # In other words, we feel that while b may be true,
    # it has no bearing on C
    r1 = Claim("R1")
    i3 = ImpliesNot(r1, i2)
    print "After Refuting B's Implication on C..."
    print '\t%s' % (i2, )
    print '\t%s' % (c, )

    # Now, we pose the opposite argument
    # Namely, we feel that b does in fact refute c
    r2 = Claim("R2")
    i4 = Implies(r2, i2)
    print 'Countering this with an argument that B does refute C...'
    print '\t%s' % (i2, )
    print '\t%s' % (c, )

    i5 = ImpliesNot(r2, b)
    i6 = Implies(r2, b)

    # Display the entire network
    print 'For clarity, he is the final resulting set of assertions...'
    print
    print a
    print b
    print c
    print r1
    print r2
    print i1
    print i2
    print i3
    print i4

class Assertion(object):
    
    def __init__(self):
        self.conditions = set() #: relations
    
    def get_prob(self):
        
        achieved_probability = 0
        possible_probability = 0
        for cond in self.conditions:
            achieved_probability += cond.get_prob() * cond.get_output()
            possible_probability += cond.get_prob()
        if possible_probability == 0:
            return 1.0
        return achieved_probability / possible_probability

    def add_condition(self, relation):
        self.conditions.add(relation)



class Claim(Assertion):
    
    def __init__(self, text):
        super(Claim, self).__init__()
        self.text = text

    def __str__(self):
        return '%s is true with probability %.2f' % (self.text, self.get_prob())

    def get_text(self):
        return self.text

class Relation(Assertion):
    
    def __init__(self, input, output):
        super(Relation, self).__init__()
        self.input = input
        self.output = output
        self.output.add_condition(self)

class Implies(Relation):
    
    def get_output(self):
        return self.input.get_prob()

    def __str__(self):
        return '%s implies %s with probability %.2f' %\
            (self.input.get_text(), self.output.get_text(), self.get_prob())
    def get_text(self):
        return '(%s ==> %s)' % (self.input.get_text(), self.output.get_text())

class ImpliesNot(Relation):
    
    def get_output(self):
        return 1.0 - self.input.get_prob()

    def __str__(self):
        return '%s implies NOT %s with probability %.2f' %\
            (self.input.get_text(), self.output.get_text(), self.get_prob())

    def get_text(self):
        return '(%s ==> NOT(%s))' % (self.input.get_text(), self.output.get_text())

if __name__ == '__main__':
    main()
