Logic
=====

If I had to create Justify in a weekend, here's how I'd do it.

## Assertions
Everything is an **Assertion**, the fundamental unit of an argument.

One type of Assertion is a **Claim**, which simply contains text.
```python
c1 = Claim("Congressman C supports policy P")
```

Individual Assertions mean little, so we allow **Relations** between Assertions.
Relations are abstract. 
Two concrete Relations are **Pros** and **Cons**.
```python
c2 = Claim("Agreed, he voted for bill B")
c3 = Claim("No way, he's from state S")

r1 = Pro(c2, c1)  # read: c2 supports c1
r2 = Con(c3, c1)  # read: c3 refutes c1
```

NOTE: Pros and Cons are not Claims, they are Relations. 

But here's the kicker: **Relations are Assertions!**

And because Relations operate on Assertions, they can operate on other Relations!

```python
c4 = Claim("I don't like to stereotype people")
c5 = Claim("A person's hometown often shapes their views")

r3 = Con(c4, r2)  # refute a **Relation**
r4 = Pro(c5, r2)  # support a **Relation**
```

Intuition: No one can dispute that Congressman C was born in state S.
To dispute that fact would be to sidestep the true issue.
You don't like this Assertion's *use* in this argument.
Put differently, you don't like it's *Relation* to another Assertion.

In this way, we can create a funny DAG of Assertions, in which Relations may originate from or point to other Assertions.

## Weights
Using Pros and Cons, I also hypothesize one way to establish the validity of each Assertion. 
I make no claims about the validity of these validities, however they seem intuitive at the moment.
Also, let how valid an Assertion is be thought of as how much *Weight* it has.

Here's my intuition:

1. The weight of an Assertion is a function of the Relations pointing to it.
2. Since Relations are themselves Assertions, and thus have weight, a Relation's impact on its target's weight should scale with its own weight. 
In other words, Relations we are confident in should matter more.

Some increasingly complex examples
* A Claim with many Pros should have a high weight.
* A Claim with equal Pros and Cons should have weight of 50%.
* A Claim with one undisputed Pro and one Con with a Pro and a Con itself, should be over 50% because the Pro is presumed to be more valid than the Con.

Algorithm
A Relation is a child relation of an Assertion if it points to that Assertion.
A Relation's output scales with its support for its parent.

Considering those thoughts, the weight is then computed as sum of each child relation's output scaled by that relation's weight.
This is then normalized to be in the range [0,1], meaning it is divided by the sum of each relation.
