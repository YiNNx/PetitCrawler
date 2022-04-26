2021年8月31日

# How to sample a circle uniformly in 2D-CCS?

![How to sample a circle uniformly in 2D-CCS?](https://ksmeow.moe/wp-content/uploads/2021/08/houkai3-kiana-1-opt.jpg)

目录

  * 1 Question Description
  * 2 Naive Solutions
    * 2.1 Sample with Filter
    * 2.2 Polar Coordinates
  * 3 Wise in Probabilities[2]
  * 4 References

## Question Description

Assume that we have a unit circle with R=1 and centered at the origin point.
We need to generate some sample points inside the circle uniformly. The points
should distribute uniformly inside the circle area in 2D-CCS, that is, **the
expectation per area** of the number of sample points is the same inside the
circle.

 _Note: 2D-CCS, 2-dimension Cartesian coordinate system._

##  Naive Solutions

### Sample with Filter

Consider the bounding box of the unit circle, or the 2×2 square centered at
the origin point, like the graph below.

![image - How to sample a circle uniformly in 2D-CCS?](https://ksmeow.moe/wp-content/uploads/2021/08/image.png)A unit circle with a square around it

Assume we have two independent random variables $P, Q$ uniformly distributed
in $[0,1]$. Sampling the 2×2 square just need a simple tranformation as below:

$$ \begin{cases} x = 2P-1, \\\ y=2Q-1. \end{cases} $$

The transformation just scales each variable by 2 times, and moves the value
interval center to 0.

But sampling the square is not sampling the circle, some sample points may be
out of the circle. Given the square area is $2 \times 2 = 4$, and the circle
area is $\pi \times 1^2 = \pi$, there are $\left(1-\dfrac{\pi}{4}\right)$ of
all sample points expected to be out of the circle, or the failure probability
of the sampling is $\left(1-\dfrac{\pi}{4}\right)$.

The idea of the failure probability leads us to a different concept - expected
random count for an output. This is easy to solve as the reciprocal of the
area ratio, or $\dfrac{4}{\pi} \approx 1.27$. That means in average, we need
127 random results for 100 valid sample points, implying **the poor
efficiency** of this method.

### Polar Coordinates

How about mapping a square area to a circle area? This idea leads us to polar
coodinate system, which uses $(\rho, \theta)$ to present a point in a plane.
In PCS, a unit circle can be described as an equation $\rho = 1, \theta \in
[0, 2\pi]$, as the graph below.

![image 1 - How to sample a circle uniformly in
2D-CCS?](https://ksmeow.moe/wp-content/uploads/2021/08/image-1.png)A circle in
PCS

Same as above, we get 2 random variables $P, Q$, then scale $Q$ to $[0,2\pi]$,
finally transform the polar coordinates to Cartesian coordinates.

$$ \begin{cases} x=P \cos(2 \pi Q), \\\ y=P \sin(2 \pi Q). \end{cases} $$

![7154520 619eb36fdd982005 - How to sample a circle uniformly in
2D-CCS?](https://ksmeow.moe/wp-content/uploads/2021/08/7154520-619eb36fdd982005.png)Random points generated
by the method above[1]

Let's have a try on this method, and get the distribution graph above. Points
seem **closer** around the center than far from the center. Why?

In this method, we independently sample $\rho$ and $\theta$, that is, for
every value of $\rho$, we are expected to have the same number of points
distributed uniformly in $\theta$ value. But for smaller $\rho$, the circle
perimeter, $2 \pi \rho$, becomes smaller too. Smaller perimeter, same amount
of points, closer the points seem to be.

## Wise in Probabilities[2]

First, it's OK to sample $\theta$ value uniformly in $[0, 2\pi]$, for the
circle is centrosymmetric. All we need to do is to adjust the point
distribution in sampling $\rho$ value. But how?

Consider this, if we have 2 $\rho$ values $\rho_1, \rho_2$, then the circle
perimeters are $2 \pi \rho_1$ and $2 \pi \rho_2$. Points must be evenly
distributed in this area, so the ratio of amount of points is the ratio of
perimeter, that is $\dfrac{\rho_1}{\rho_2}$. This leads to the idea of
**Probability Density Function** , or PDF. If we let the PDF of points defined
with $\rho$ values is $f(\rho)$, then the fact above indicates $f(\rho)$ is a
**linear function**.

$f(0)=0$ is the next things we know about the PDF, for $\rho=0$ presents a
point. Then we assume $f(\rho)=k\rho$ and try to solve $k$. PDF must be
normalized, or integrated to be 1. So

$$ \int_0^1 f(\xi) \mathrm{d}\xi = \int_0^1 k\xi \mathrm{d}\xi = \dfrac{k}{2}
= 1. $$

Obviously $k = 2$, and $f(\rho)=2\rho$.

Let $X$ be the random variable with a PDF of $f(x)=2x$. The question is, we
have another random variable $Y$ uniformly distributed in $[0,1]$, try to find
a function $G(x)$ making $G(Y)$ has the same distribution as $X$. This is a
question about probability.

We can use **Probability Distribution Function** , another PDF, to solve this.
This PDF is the integral of the PDF above, that is, $\mathrm{P} \\{ X \leq x
\\} = \int_0^x f(x)\mathrm{d}x = x^2$. The same distribution means the same
PDF, so $\mathrm{P} \\{ G(Y) \leq x \\} = \mathrm{P} \\{ X \leq x \\} = x^2$,
or $\mathrm{P} \\{ Y \leq G^{-1}(x) \\} = x^2$. We also know that $\mathrm{P}
\\{ Y \leq y \\} = y$, then $G^{-1}(x)=x^2$ and $G(x)=\sqrt{x}$.

Back to the question, we have 2 variables $P, Q$, then let another variable
$P' = \sqrt{P}$, then do the transformation like

$$ \begin{cases} x=P' \cos(2 \pi Q), \\\ y=P' \sin(2 \pi Q). \end{cases} =
\begin{cases} x=\sqrt{P} \cos(2 \pi Q), \\\ y=\sqrt{P} \sin(2 \pi Q).
\end{cases} $$

Problem solved.

![7154520 29fa81a308d987b1 - How to sample a circle uniformly in
2D-CCS?](https://ksmeow.moe/wp-content/uploads/2021/08/7154520-29fa81a308d987b1.png)Random generated by the
method with a $\sqrt{P}$ in it[1]

Look at the sample points, how beautiful!

## References

  1. 圆内的均匀随机点 - MrYun - 博客园  
<https://www.cnblogs.com/yunlambert/p/10161339.html>

  2. math - Generate a random point within a circle (uniformly) - Stack Overflow  
<https://stackoverflow.com/questions/5837572/generate-a-random-point-within-a-circle-uniformly>

Author: [KSkun](https://ksmeow.moe/author/kskun/ "文章作者 KSkun")

Filed Under: [算法](https://ksmeow.moe/category/algorithm/),
[知识](https://ksmeow.moe/category/algorithm/knowledge/)

Tags: [概率](https://ksmeow.moe/tag/probability/),
[随机化](https://ksmeow.moe/tag/random/)

