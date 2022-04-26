2021年10月19日

# MIT 6.837：Transformations 变换

![MIT 6.837：Transformations 变换](https://ksmeow.moe/wp-content/uploads/2021/10/mit6.837_transformation.jpg)

在设置 3D 场景时，变换是至关重要的一种操作。通过变换，我们可以实现 3D
物体从模型坐标系到世界坐标系的转换，也可以实现场景从世界坐标系到相机坐标系的转换，还可以通过变换表达物体的运动，从而实现动画效果。在这篇文章中，我们主要介绍一些基本的变换及其计算。

目录

  * 1 变换的分类
    * 1.1 刚体变换/欧几里得变换
    * 1.2 相似变换
    * 1.3 线性变换
    * 1.4 仿射变换
    * 1.5 投影变换
  * 2 变换的表示
    * 2.1 齐次坐标
    * 2.2 平移
    * 2.3 缩放
    * 2.4 旋转
    * 2.5 复合变换
  * 3 变换后的光线投射
    * 3.1 射线的变换
    * 3.2 交点的变换

## 变换的分类

### 刚体变换/欧几里得变换

![rigid transformation - MIT 6.837：Transformations 变换](https://ksmeow.moe/wp-content/uploads/2021/10/rigid_transformation.png)

这一类变换可以保证原来的线段长度与角度在变换后不变，包括

  * 什么都不做
  * 平移
  * 旋转

### 相似变换

![similitudes transform - MIT 6.837：Transformations 变换](https://ksmeow.moe/wp-content/uploads/2021/10/similitudes_transform.png)

这一类变换只保证了角度不变，长度可能发生变化，包括：

  * 刚体变换
  * 各向同性的缩放（各维度缩放倍率相同的缩放）

### 线性变换

![image 8 1024x176 - MIT 6.837：Transformations 变换](https://ksmeow.moe/wp-content/uploads/2021/10/image-8-1024x176.png)

![image 9 - MIT 6.837：Transformations 变换](https://ksmeow.moe/wp-content/uploads/2021/10/image-9.png)

这一类变换可以通过线性的坐标变换（即可以写成变换矩阵的形式）表达，包括：

  * 一部分的相似变换
    * 一部分的刚体变换
      * 什么都不做
      * 旋转
    * 各向同性的缩放
  * 各向异性的缩放（不同维度的缩放倍率有所不同）
  * 镜像
  * 错切（如图中上右的例子）

### 仿射变换

![image 10 - MIT 6.837：Transformations 变换](https://ksmeow.moe/wp-content/uploads/2021/10/image-10.png)

这一类变换可以分解成一个线性变换与一个平移的变换，可以保证平行线在变换后依然平行，包括上面提到过的所有变换。

### 投影变换

![image 11 - MIT 6.837：Transformations 变换](https://ksmeow.moe/wp-content/uploads/2021/10/image-11.png)

这一类变换只保证共线性，而不保证他们之间的平行性。上面提到的所有变换都属于投影变换。透视投影是一种投影变换，但它不是仿射变换。

## 变换的表示

### 齐次坐标

上面我们不仅提到了可以用矩阵表示的线性变换，还提到了仿射变换、投影变换等，这些变换不能简单地用和坐标同维度的矩阵来表示。为了用矩阵表示它们，我们需要引入齐次坐标。

考虑一个仿射变换，它的矩阵表示如下

$$  
\begin{bmatrix} x' \\\ y' \end{bmatrix}  
=  
\begin{bmatrix} a & b \\\ d & e \end{bmatrix}  
\begin{bmatrix} x \\\ y \end{bmatrix}  
+  
\begin{bmatrix} c \\\ f \end{bmatrix}  
$$

对于代表平移的常数向量，考虑将其合并进变换矩阵中，这需要给矩阵和向量都加一个维度，即

$$  
\begin{bmatrix} x' \\\ y' \\\ 1 \end{bmatrix}  
=  
\begin{bmatrix} a & b & c \\\ d & e & f \\\ 0 & 0 & 1 \end{bmatrix}  
\begin{bmatrix} x \\\ y \\\ 1 \end{bmatrix}  
$$

如 $(x,y,1)$ 这样，比其描述的坐标高一维、且最后一维为常数的坐标被叫做 **齐
次坐标**。对于齐次坐标来说，不仅仿射变换可以用一个变换矩阵表达，投影变换也可以。

齐次坐标的最后一维代表前面坐标值的缩放比例，即 $(x,y,w)$ 对应 $(x/w,y/w)$。由于向量的平移没有意义，我们将代表向量的齐次坐标设置为
$w=0$。

### 平移

三维空间中，沿 $x,y,z$ 轴分别平移 $t_x, t_y, t_z$ 的变换可表示为

$$ \begin{bmatrix} 0 & 0 & 0 & t_x \\\ 0 & 0 & 0 & t_y \\\ 0 & 0 & 0 & t_z \\\
0 & 0 & 0 & 1 \end{bmatrix} $$

### 缩放

三维空间中，$x,y,z$ 坐标缩放比例分别为 $s_x,s_y,s_z$ 的变换可表示为

$$ \begin{bmatrix} s_x & 0 & 0 & 0 \\\ 0 & s_y & 0 & 0 \\\ 0 & 0 & s_z & 0 \\\
0 & 0 & 0 & 1 \end{bmatrix} $$

### 旋转

沿坐标轴的旋转比较简单，可以相当于在与坐标轴垂直的平面内完成旋转，以沿 $z$ 轴的旋转为例

$$ \begin{bmatrix} \cos \theta & -\sin \theta & 0 & 0 \\\ \sin \theta & \cos
\theta & 0 & 0 \\\ 0 & 0 & 1 & 0 \\\ 0 & 0 & 0 & 1 \end{bmatrix} $$

如果需要沿任意过原点的轴旋转，则可以使用[罗德里格旋转公式](https://en.wikipedia.org/wiki/Rodrigues%27_rotation_formula
"https://en.wikipedia.org/wiki/Rodrigues%27_rotation_formula")。

### 复合变换

既然都写成矩阵形式了，那么简单变换之间的复合就可以用矩乘表示。需要注意的是， **矩 乘不满足交换律**，不能随便换运算顺序。

## 变换后的光线投射

3D 物体通过变换被放置进世界坐标系中，而射线在世界坐标系中被发出，和 3D
物体求交时不能直接计算，而需要经过变换后在物体自身的坐标系中求交。我们需要研究如何变换射线到物体坐标系，求交的结果如何变换回世界坐标系。

记物体到世界坐标系的变换矩阵为 $\mathbf{M}$，其逆矩阵为 $\mathbf{M}^{-1}$。

### 射线的变换

射线可以表达为 $\boldsymbol{P} = \boldsymbol{R_o} + t \boldsymbol{R_d}$，只需要研究
$\boldsymbol{R_o}, \boldsymbol{R_d}$ 两个向量如何变换即可。

$\boldsymbol{R_o}$
是一个在世界坐标系中的点，在物体坐标系中直接应用逆变换即可：$\boldsymbol{R_o}'=\mathbf{M}^{-1}
\boldsymbol{R_o}$。

$\boldsymbol{R_d}$ 是射线的方向向量，我们可以取 $t=1$ 的一个点 $\boldsymbol{R_o} +
\boldsymbol{R_d}$ 做变换，再拿它与射线起点作差即可：$\boldsymbol{R_d}' = \mathbf{M}^{-1}
(\boldsymbol{R_o}+\boldsymbol{R_d}) - \boldsymbol{R_o}' = \mathbf{M}^{-1}
\boldsymbol{R_d}$。

需要注意，射线的方向向量默认是单位向量，因此变换后需要对 $\boldsymbol{R_d}'$ 做规范化。

### 交点的变换

交点包含的信息通常包含 $t$ 值和交点处物体的法向量 $\boldsymbol{n}$，分别研究它们到世界坐标系的变换。

$t$ 值出现问题的地方在射线变换时，$\boldsymbol{R_d}$ 变换后可能不是单位向量，规范化后求出的 $t'$
是在物体坐标系中的值。假设未规范化时的方向向量长度为 $||\boldsymbol{R_d}'||$，则需要通过换算得到世界坐标系中的 $t$ 值：$t =
t' / ||\boldsymbol{R_d}'||$。

法向量出现问题的地方在于缩放、错切等变换导致正交坐标轴不再正交，需要重新计算法向量。用直接的思路求变换是复杂度，我们考虑使用切向量曲线救国，因为切向量直接做变换是正确的。任取一切向量，物体坐标系中法向量、切向量分别记为
$\boldsymbol{n}_{OS}, \boldsymbol{v}_{OS}$，世界坐标系中记为 $\boldsymbol{n}_{WS},
\boldsymbol{v}_{WS}$。

在物体坐标系中，法向量与切向量有垂直关系，即 $\boldsymbol{n}_{OS} \cdot \boldsymbol{v}_{OS} =
\boldsymbol{n}_{OS}^\mathbf{T} \boldsymbol{v}_{OS} = 0$，在两向量中乘一个
$\mathbf{M}^{-1} \mathbf{M} = \mathbf{I}$，得到 $(\boldsymbol{n}_{OS}^\mathbf{T}
\mathbf{M}^{-1}) (\mathbf{M} \boldsymbol{v}_{OS}) =
(\boldsymbol{n}_{OS}^\mathbf{T} \mathbf{M}^{-1}) \boldsymbol{v}_{WS} =
0$。这说明，$\boldsymbol{n}_{WS}^\mathbf{T} = \boldsymbol{n}_{OS}^\mathbf{T}
\mathbf{M}^{-1}$，或 $\boldsymbol{n}_{WS} = (\mathbf{M}^{-1})^\mathbf{T}
\boldsymbol{n}_{OS}$。

Author: [KSkun](https://ksmeow.moe/author/kskun/ "文章作者 KSkun")

Filed Under: [计算机图形学](https://ksmeow.moe/category/game_development/computer-graphics/), [游戏开发](https://ksmeow.moe/category/game_development/)

