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

In this way, we can create a funny DAG of Assertions, in which Relations may originate from or point to other Relations.

## Weights
Using Pros and Cons, I here hypothesize one way to establish the validity of each Assertion. 
I make no claims about the validity of these validities, however they seem intuitive at the moment.

### Terminology

* Let how valid an Assertion is be thought of as how much *Weight* it has.
* If assertion A supports assertion B, i.e. `rel = Pro(A,B)`, 
then 
  * A is the **child** of the relation
  * B the **parent** of the relation
  * the relation can be considered one of B's **child relations**.
* each relation has some output as a function of it's input in the range [0,1]
  * A Pro outputs its child's weight
  * A Con outputs the compliment of its child's weight 

### My Intuition

1. The weight of an Assertion is a function of its child relations.
2. Since Relations are themselves Assertions, and thus have weight, a Relation's impact on its parents's weight should scale with its own weight. 
In other words, Relations we are confident in should matter more.

Some increasingly complex examples
* A Claim with many Pros should have a high weight.
* A Claim with equal Pros and Cons should have weight of 50%.
* A Claim with one undisputed Pro and one Con with a Pro and a Con itself, should be over 50% because the Pro is presumed to be more valid than the Con.

### Algorithm
The weight is then computed as sum of each child relation's output scaled (multiplied) by that relation's weight.
This is then normalized to be in the range [0,1], meaning it is divided by the sum of each relation's weight.
Run `logic.py` to see an example of this.

## Big Ideas
Here are some thoughts on how I would flush this paradigm out.

More **emergent properties** could potentially also be derived for every Assertion. 
Weight is already one we've explored.
Contentiousness could be another.

To abstract my design even further, Relations could be transformed to be more like **functions**.
Functions would take Assertions as arguments.
Output is tricky, and I'm torn.
On one hand, the output could simply be represented as the value of the Assertion.
On the other, it could in turn produce an arbitary DAG of its own, 
but this DAG would need to be linked back to the function it created.

**Loops** would be a kind of function. 
I'd like to think more about the desired result from loops.

## Cool Questions
1. How would a recursive argument like induction be modeled in this paradigm?
2. How would a self fulfilling argument be modeled?
3. Could we create a sort of differential equation of Assertions we could step through and see how the lay of the land changes at teach time step?


