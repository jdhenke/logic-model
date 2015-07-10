# Logic Model

> Toy modeling of arguments with symbolically derived weights.

## Setup

**Install** [python](https://www.python.org/) and
[virtualenv](https://pypi.python.org/pypi/virtualenv), then **run** the setup
script:

```bash
sh setup.sh
```

## Running

```bash
# always use virtualenv to access required modules installed at setup
source env/bin/activate
# run example script below, leaving REPL open to play with
python -i model.py
```

## Modeling Explanation

Everything is an *Assertion*.

A *Claim* is an atomic Assertion that is just text.

A *Relation* indicates that one Assertion either supports or refutes another
Assertion.

Every Assertion has a *weight*, which is a derived measure of how true that
Assertion is between 0 and 1, where 0 is false and 1 is true. An Assertion that
has no Relations pointing to it is assumed to be true. Otherwise, the weight of
an Assertion is the average of each of its Relation's support scaled by each
Relation's own weight.

```python
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
```

Now, the weird bit is that **Relations are Assertions**. That means
**Relations** can support, refute, be supported by and be refuted by other
Assertions.

```python
# continuing from above...
#
# now debate over how reasonable it is to support c with "supporting claim 1"
_ = Con(Claim('refuting claim 2'), r1)
_ = Con(Claim('refuting claim 3'), r1)
_ = Pro(Claim('supporting claim 4'), r1)
# print the new derived weight of the original claim
print "Main Claim's Derived Weight: %s" % (c.get_weight(), )
# ==> 4/7
```

Note that the new derived weight for the main claim is lower (4/7 < 2/3)
because one of the relations that supports it came under fire.
