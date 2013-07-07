import unittest
from apollo import *

''' Unit testing of Apollo '''

class TestIntegrities(unittest.TestCase):
    ''' Test every combination '''
    def setUp(self):
        self.a = Claim("a")
        self.b = Claim("b")
    def testDefaultWeight(self):
        self.assertEqual(self.a.get_weight(), 1)
    def testSimpleImplies(self):
        r = Pro(self.a, self.b)
        for x in (self.a, self.b, r,):
            self.assertEqual(x.get_weight(), 1)
    def testSimpleRefutation(self):
        r = Con(self.a, self.b)
        self.assertEqual(self.a.get_weight(), 1)
        self.assertEqual(self.b.get_weight(), 0)
        self.assertEqual(r.get_weight(), 1)

def gen_scenario(claims, relation_indices, relation_bits):
    pass

def gen(max_claims, max_relations):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    output = {} # output[num_claims][num_relations]
    for num_claims in xrange(1, max_claims):
        print 'Creating %i' % (num_claims, )
        output[num_claims] = {}
        output[num_claims][0] = [[letters[i] for i in xrange(num_claims)]]
        for num_relations in xrange(1, max_relations):
            output[num_claims][num_relations] = []
            for previous_answer in output[num_claims][num_relations-1]:
                for new_answer in add_all_possible_new_relations(previous_answer):
                    output[num_claims][num_relations].append(new_answer)
    return output

def add_all_possible_new_relations(assertions):
    for child, parent in combos(list(range(len(assertions))), 2):
        for x in (0,1,):
            yield assertions + [(child, parent, x,), ]

def get_bit(num, bit):
    (num & (1<<bit)) >> bit

def combos(L, n):
    if n == 0:
        yield tuple()
    else:
        for x in L:
            for sub_combo in combos(L, n-1):
                yield (x,) + sub_combo

max_claims = 4
max_relations = 4

max_claims += 1
max_relations += 1

answer = gen(max_claims,max_relations)

def create_scenario(params):
    answer = []
    for param in params:
        if type(param) is str:
            answer.append(Claim(param))
        else:
            child, parent, t = param
            if t == 0:
                answer.append(Pro(answer[child], answer[parent]))
            elif t == 1:
                answer.append(Con(answer[child], answer[parent]))
    return answer

total = 0
for num_claims in xrange(1,max_claims):
    for num_relations in xrange(max_relations):
        # print '== %s x %s == ' % (num_claims, num_relations)
        for x in answer[num_claims][num_relations]:
            # print x
            scene = create_scenario(x)
            for a in scene:
                # print a.get_weight()
                # print x
                try:
                    assert a.get_weight() is None or (a.get_weight() >= 0 and a.get_weight() <= 1)
                except ZeroDivisionError:
                    print 'WARNING: ZERO DIVISION ERROR'

            total += 1



print "TOTAL: %i" % (total,)