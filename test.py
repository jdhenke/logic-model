from apollo import *
a = Claim('a')
s = Pro(a,a)
r = Con(a,a)
k = Con(s,r)

print a.get_weight()