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

To me, this is logical.
No one can dispute that Congressman C was born in state S.
To dispute that fact would be to sidestep the true issue.
You don't like this Assertions *use* in this argument.
Put differently, you don't like it's *Relation* to another Assertion.
