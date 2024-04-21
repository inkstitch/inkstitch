---
title: Multicolor Satin
permalink: /tutorials/multicolor_satin/
last_modified_at: 2024-04-17
language: fr
excerpt: "Simuler des colonnes satin multicolore"
image: "assets/images/tutorials/multicolor_satin/snake.jpg"
tutorial-type:
stitch-type: 
  - Satin Stitch
techniques:
field-of-use:
user-level:
toc : true
---

# Simulate a multi-colored satin column.

We are talking about simulation here, because it is not a single multicolored satin column, but a similar effect obtained by
using several overlapping copies of the same satin column, simply using different random parameters.

## Let's start with the bicolor satin
Let's come back to the "random" parameters of the satin columns.

### Random percentage of satin width  increase
The "Random percentage of satin width  increase" parameter is a so-called asymmetric parameter because it is possible to apply it differently on the two rails. 
This  parameter accepts either a sigle value, in which case it is applied to each of the two rails; but also  two space separeted values, in which case the first is applied to the first rail, the second to the second rail.

![random increase_different_seeds](/assets/images/tutorials/multicolor_satin/random_increase_different_seeds.png)

* When this parameter is set to 0, the column (in black) is made up of zig-zags traveling  between the two rails
* When this parameter is set to 50,  each zig (or zag) of the column (in red)is extended to the left and right by a value between 0 and 50% of the length of the zig. The new column is therefore widened irregularly, at most it can be twice as wide as the black one (50% on the left and 50% on the right), it is never narrower.
* When this parameter is set to 0 50, the left side of the column (in green) is unchanged, but on the right it is extended up to 50% additional length.
* When this parameter is set to 50.0, the column (in blue) is similar by swapping the roles of left and right.
* If we superimpose the three columns having a non-zero value for the parameter, the enlargement seems very random, the borders of the columns are very different, even if they are similar.

What values ​​can be entered in this parameter? Ink/Stitch accepts any pair of numeric values ​​here. 
They can be positive or null, and they can exceed the value 100. 
However, if we can increase the zigs without limit, 
the reduction is de facto limited, at worst the zig would be a simple point on the center line.

![negative augmentation](/assets/images/tutorials/multicolor_satin/negative_augmentation.png)



### Random percentage of satin width decrease 
Satin columns also have the opposite parameter, the "Random percentage of satin width decrease ". 
Rather than increasing by -50%, we can decide to decrease by 50%, it's the same thing.

### Simple, but imperfect method

Thanks to any of these two parameters, we already have a first imperfect but very simple method for simulating two-tone satin columns:

![first_bicolore_satin](/assets/images/tutorials/multicolor_satin/first_bicolor_satin.png)

both examples use a random percentage of width decrease

* On the left example  the left side of the red column is reduced while  the right side of the green column is reduced. But be careful, the second color superimposes the first and here the green hides part of the red.
* On the right, we left the red intact, the green is superimposed, its right side reduced by up to  two thirds rather than one half.

But this method is imperfect: it ensures that the entire column is colored, there is no lack, but there is some overlay.

It is possible to obtain two perfectly joining  columns, but this also requires using other random parameters

### The random seed
Each time we use one or more random parameters, if we are not happy with the result, we can click on “reroll the dice” and obtain a different result. 
Technically, rerolling the dice means giving a new value to the “random seed” parameter.
It is also possible to manually give a value to this parameter. 
This is particularly useful when one want several copies of an object that uses random parameters to be in fact perfectly identical. 
Give them the same random seed value and they will be identical.

If we repeat the first example but this time give all three columns random seeds the same value, here is what we obtain:
![random increase_same_seeds](/assets/images/tutorials/multicolor_satin/random_increase_same_seed.png)

Now when we superimpose the three columns, we see that there is a perfect superposition of the borders. 
The red column has expanded to the left like the blue column and to the right like the green column. 
On the other hand, for the same zig, the widening to the left is different from the widening to the right.

### Method almost as simple, with perfect fit but unfortunately not general

![first_success](/assets/images/tutorials/multicolor_satin/first_good.png)

This time, instead of superimposing two columns, they are placed next to each other. The right edge of one being superimposed on the left edge of the other

* Both columns have the same random seed
* The orange column "Random percentage of satin width decrease " is set to 50 0
* The blue column "Random percentage of satin width decrease " is set  -50 0 (so it is an increase).
* In addition, we have checked the Swap rails box for the blue column

As both have the same random seed and the modifications in both cases concern the same rail, at each zig the calculation gives values ​​which ensure a perfect fit.

Unfortunately, this simple solution does not generalize to columns of any shape.

For a general solution, we'll use yet another additional parameter:

## Pull compensation percentage
To obtain multi-colored satin columns, we will use the “pull compensation percentage” parameter.

It is also an asymmetric parameter.

It is common to give positive values ​​to the compensations, but it is also possible to give them negative values, 
instead of increasing the width of the satin column, we reduce it.

Here are three example values ​​for the pull compensation percentage parameter, and the result
![compensation](/assets/images/tutorials/multicolor_satin/compensation.png)

Here the first rail is the left side of the satin.

When the parameter is set to  "0 -75" (in green)  the left side is unchanged, but everything happens as if the right side had been brought together regularly to reduce the distance between the two rails to a quarter of the initial value. We have in fact gone from a width of 100% to a width of 100-75=25%

When the parameter is set to "-25 -25" (in red) the two edges move closer to the center and the width of the column is uniformly reduced by half.

When the parameter is set to "-75 0" (in blue) we do not touch the right side, but everything happens as if the left side had been brought together regularly to reduce the distance between the two rails to a quarter of the initial value.

If we superimpose these three columns, we obtain a tricolor snake.

![tricolor](/assets/images/tutorials/multicolor_satin/tricolor_snake.png)


**Note** It is possible to use pull compensation in mm and compensation in percentage on the same satin column. Both parameters are asymmetrical. Both parameters accept negative values.
{: .notice--info }

### General method for bicolor satin column

We will use all these parameters together.

If you want to distribute the 100% width of the column into
* G% on the left exclusively for blue
* D% on the right exclusively for green
* and therefore 100-(G+D) percent in the middle for a green-blue mixture,

we will use this setting

|Parameter | Blue satin | Green satin |
| --- | --- |--- |
| Pull Compensation Percentage | 0 100-G| 0 100-D|
| Swap Rails| no | yes |
| Random  satin width increase| 0 100-(L+R)| 0 |
| Random satin width drecrease| 0 | 0 L+R-100|
| Random Seed| identical | identical |

So for example if we want to keep a 25% single color on each side, we will use this setting

Blue satin:
* Pull compensation percentage: 0 -75
* Random satin width increase: 0 50
* Random  satin width decrease: 0
* Random seed: 7 (or "hello" or anything else but enter a value)

Green satin:
* Pull compensation percentage: 0 -75
* Check swap rails
* Random satin width increase: 0
* Random satin width decreas: 0 -50 (so it will be an increase)
* Random seed: 7 (or whatever you entered for the other column)



**Important** If it doesn't seem to be working, check that the satin column rails are both in the same direction, and not automatically corrected. Also check that the short stitches are not triggered.
{: .notice--info }

![solution](/assets/images/tutorials/multicolor_satin/solution.png)

Download [the snake file](/assets/images/tutorials/multicolor_satin/serpent.svg){: download="serpent.svg" }


