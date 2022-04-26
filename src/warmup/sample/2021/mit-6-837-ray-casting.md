2021年10月10日

# MIT 6.837：Ray Casting 光线投射

![MIT 6.837：Ray Casting 光线投射](https://ksmeow.moe/wp-content/uploads/2021/10/mit6.837_ray_casting.jpg)

光线投射是光线追踪的第一部分内容，在 MIT 6.837 课程（Fall 04）中，我们首先了解光线投射有关的内容。

目录

  * 1 光线投射的基本过程
  * 2 成像
    * 2.1 透视
    * 2.2 投影
  * 3 几何
    * 3.1 光线（射线）
    * 3.2 平面
    * 3.3 球面
    * 3.4 AABB（轴对齐的包围盒）
    * 3.5 多边形
    * 3.6 三角形

## 光线投射的基本过程

    
    
    For every pixel
    	Construct a ray from the eye
    	For every object in the scene
    		Find intersection with the ray 
    		Keep if closest

![ray casting 1 - MIT 6.837：Ray Casting 光线投射](https://ksmeow.moe/wp-content/uploads/2021/10/ray_casting_1.png)

上面这段伪代码即是光线投射的基本过程，即从眼睛发出一个穿过像素的射线，与场景求交取最近的交点，利用交点信息计算像素颜色。

在这里，我们会涉及几个需要解决的问题，在下面将一一介绍。

## 成像

在这个部分，我们研究两种成像方式：透视和投影。

### 透视

这是相机和人眼的成像方式，也即一般情况下我们想要得到的效果。它认为相机可以近似为一个点，视野范围为一个角度（视角，FoV）；远处的物体上的点成像时，做一条与相机的连线，其与成像平面的交点即为对应的成像。这样的成像不能保证原来平行的线依然平行，且会带来长度、角度的变化，比较复杂。

描述一个透视成像的相机需要以下要素：

  * 相机所在位置
  * 相机的摆放（水平向量、向上向量、观察方向）
  * 视角
  * 成像平面的大小（宽、高）

![perspective camera - MIT 6.837：Ray Casting 光线投射](https://ksmeow.moe/wp-content/uploads/2021/10/perspective_camera.png)

使用这样的相机进行光线投射时，光线为一从相机位置出发，方向指向成像平面像素中心的射线。

### 投影

与透视方法不同，投影方式简单了很多。投影方法不再需要关心视角等问题，光线为一系列从无限远处向观察方向发出的平行射线，它们穿过对应像素的中心。由于投影的性质，可以保证原本平行的线在投影后依然平行，其光线射线也更好求出。

描述一个投影相机需要以下要素：

  * 相机所在位置
  * 相机的摆放（水平向量、向上向量、观察方向）
  * 成像平面的大小（宽、高）

![orthographic ray - MIT 6.837：Ray Casting 光线投射](https://ksmeow.moe/wp-content/uploads/2021/10/orthographic_ray.jpg)

在生成投影光线时，其方向即为观察方向，而原点为成像平面上的像素中心点。

## 几何

在几何部分，我们主要研究如何表示光线投射过程中需要用到的几何体，以及光线如何与几何题求交。

### 光线（射线）

根据光线的要素，我们很自然可以得到射线的描述方法：从原点出发，指向某一方向。即，描述一个射线需要两个向量，一个代表原点的 $\mathbf{R_o}$
和一个代表方向的 $\mathbf{R_d}$，通常 $\mathbf{R_d}$ 会规范化成长度为 1 的单位向量。

想表达光线从摄像机出发，经过 $t$ 距离后到达的线，可以表达成 $\mathbf{P}(t) = \mathbf{R_o} + t
\mathbf{R_d}$。因此，射线上任意一点可以通过参数 $t$ 描述，光线求交的结果也不需要保存具体的坐标向量了。

### 平面

描述平面的方法有很多，如用平面上三点描述。最常用的一种描述方法包括一个在平面上的点 $\mathbf{P_o}$ 和平面的法向量
$\mathbf{n}$。平面上任意一个点与已知点 $\mathbf{P_o}$ 的连线一定在平面上，因此此向量与法向量垂直，即点积为
$0$。因此平面可以通过一个方程 $(\mathbf{P} - \mathbf{P_o}) \cdot \mathbf{n} = 0$
描述。根据点积的分配率，又由于 $\mathbf{P_o} \cdot \mathbf{n}$ 是已知数，可以将方程简化为 $\mathbf{P}
\cdot \mathbf{n} + D = 0$。这个方程还可以进一步展开，会得到一个形如 $Ax + By + Cz + D = 0$ 的关于
$\mathbf{P}$ 的坐标的方程，这个方程使用四个实数 $A,B,C,D$ 描述平面。

要解出光线与平面交点的参数，实际上就是在求解这个方程组

$$ \begin{cases}  
\mathbf{P} = \mathbf{R_o} + t \mathbf{R_d} & (1), \\\  
\mathbf{n} \cdot \mathbf{P} + D = 0 & (2),  
\end{cases} $$

而将 (1) 式代入 (2) 式，得到 $\mathbf{n} \cdot (\mathbf{R_o} + t \mathbf{R_d}) + D =
0$，做恰当变形后即可求出 $t$ 的表达式 $t = -\dfrac{D + \mathbf{n} \cdot
\mathbf{R_o}}{\mathbf{n} \cdot \mathbf{R_d}}$。

平面的法向量在平面上任一点都相同，且通常已给出，不需要单独求。

### 球面

描述球面需要一个原点 $\mathbf{O}$ 和半径 $r$，球面上任一点满足到原点的记录等于半径，即 $|| \mathbf{P} -\mathbf{O} || = r$，或 $(\mathbf{P} - \mathbf{O}) \cdot (\mathbf{P} -\mathbf{O}) = r^2$。

可以使用类似平面的考虑方法，求解球面的交点参数。依然代入，得到表达式

$$ (\mathbf{R_o} + t \mathbf{R_d} - \mathbf{O}) \cdot (\mathbf{R_o} + t
\mathbf{R_d} - \mathbf{O}) = r^2, $$

展开并整理得

$$ (\mathbf{R_d} \cdot \mathbf{R_d}) t^2 + 2 \mathbf{R_d} \cdot (\mathbf{R_o}
- \mathbf{O}) t + (\mathbf{R_o} - \mathbf{O}) \cdot (\mathbf{R_o} -\mathbf{O}) - r^2 = 0, $$

这是一个关于 $t$ 的一元二次方程，其判别式与求根公式是简单的，可以直接求解 $t$。由于可能出现多个解，需要选择最近且合理的解。

![image - MIT 6.837：Ray Casting 光线投射](https://ksmeow.moe/wp-content/uploads/2021/10/image.png)

我们也可以从几何考虑这个问题。首先求出向量 $\mathbf{v_RO} = \mathbf{O} - \mathbf{R_o}$，根据 $||
\mathbf{v_RO} ||$ 与 $r^2$ 的大小关系可以得到光线起点在球面内部或外部。

接下来找出光线上距离球心最近的点（垂线段与光线的交点） $t_P = \mathbf{v_RO} \cdot \mathbf{R_d}$，如果 $t_P <
0$ 说明交点在相机背后。

接下来求出垂线段长度，根据勾股定理 $d = \sqrt{\mathbf{v_RO} \cdot \mathbf{v_RO} - t_P^2}$，如果
$d^2 > r^2$ 说明光线与球面没有交点。

要求出交点的参数 $t$，就是交点到光线起点的距离。如上图所示，只需要从 $t_P$ 中减去 $t'$ 就可以了。而根据勾股定理，$t' =
\sqrt{r^2 - d^2}$。需要注意，当相机在球面内部时，应该加上这个 $t'$ 而非减去。

### AABB（轴对齐的包围盒）

![image 1 - MIT 6.837：Ray Casting 光线投射](https://ksmeow.moe/wp-content/uploads/2021/10/image-1.png)

一个 AABB 可以由一对点 $(X_1, Y_1, Z_1), (X_2, Y_2, Z_2)$ 描述，AABB 区域为这一对点之间围成的轴对齐立方体。

对于任意的立方体，可以分别对三对平面求交，求所有交点最近的一个作为结果即可。对于 AABB 来说，可以继续简化。由于 AABB 任一平面的法向量只有一维为非
0 值，求解交点时只需要考虑一维的情况。以上图所示的 $x$ 坐标为例，可以得到以下方程组

$$ \begin{cases}  
t_{\text{near}} & = \dfrac{X_1 - R_{ox}}{R_{dx}}, \\\  
t_{\text{far}} & = \dfrac{X_2 - R_{ox}}{R_{dx}},  
\end{cases} $$

而取三对平面求出来的 $t_{\text{near}}$ 的最大值与 $t_{\text{far}}$ 的最小值，就可以得到光线进入和离开 AABB
的点的参数 $t$ 了，而如果 $t_{\text{near}} > t_{\text{far}}$ 则说明光线与 AABB
无交点。容易发现，在求解过程中经常用到方向向量坐标的倒数，可以提前算出，在计算中使用预处理值，以获得更好的性能。

### 多边形

这里考虑的多边形是平面多边形，因此多边形的所有顶点与边都在同一个平面上。我们可以先求出光线与所在平面的交点，再验证这个交点是否在多边形内。

![image 2 - MIT 6.837：Ray Casting 光线投射](https://ksmeow.moe/wp-content/uploads/2021/10/image-2.png)

测试平面上一个点是否在多边形内可以使用射线法。从该点出发向任意方向射出一条射线，计算射线与多边形边的交点数量，如果为偶数（包括
0）表示在多边形外部，否则在多边形外部。

![image 3 - MIT 6.837：Ray Casting 光线投射](https://ksmeow.moe/wp-content/uploads/2021/10/image-3.png)

对于这样一个星型的多边形，如果按照射线法，则中间的这个区域会被认为是凹多边形的外部，而不认为红点在多边形内；而如果计算多边形包围的部分则射线法不可用，这时可以使用带符号的交点计数。沿顶点顺序将边变为有向向量，认为边方向从左到右跨越认为
+1，反之则 -1，如果求和为 0 则在多边形外。以上图为例，这条射线与多边形边的两个交点都是 +1，因此点被正确标记为多边形内。

![image 4 - MIT 6.837：Ray Casting 光线投射](https://ksmeow.moe/wp-content/uploads/2021/10/image-4.png)

另一种方法是计算以红点为顶点、相邻两多边形顶点构成的角的有向角度。如果有向角度之和为 0 则点在多边形外，否则在多边形内，且求和为 $2 \pi$
的整数倍。

一个技巧是求出点与平面的交点后，把平面投影到与轴平行的平面上再运行上面的算法，这样只是删除其中一个坐标维度，计算开销更小。

### 三角形

三角形作为模型网格中很常见的体素，我们有特化且高效的方法求解光线与三角形的交点。在这种方法里，我们需要引入重心坐标的概念。

![image 5 - MIT 6.837：Ray Casting 光线投射](https://ksmeow.moe/wp-content/uploads/2021/10/image-5.png)

如图所示，设三角形三顶点坐标分别为 $\mathbf{A}, \mathbf{B}, \mathbf{C}$，而点 P 的重心坐标为 $(\alpha,
\beta, \gamma)$，则点 P 的坐标为 $\mathbf{P} = \alpha \mathbf{A} + \beta \mathbf{B} +
\gamma \mathbf{C}$。同时，重心坐标满足 $\alpha+\beta+\gamma=1$。如果点 P 在三角形内部，则它的重心坐标满足
$\alpha, \beta, \gamma \in (0,1)$。

由于重心坐标满足 $\alpha+\beta+\gamma=1$，实际上我们可以简化为 $(1-\beta-\gamma, \beta, \gamma)$
或 $(\beta, \gamma)$。我们可以得到重心坐标的另外一种理解，将 $\alpha$ 的展开代入 P 坐标的表达式中，可以得到如下的推导

$$ \begin{aligned}  
\mathbf{P} & = \alpha \mathbf{A} + \beta \mathbf{B} + \gamma \mathbf{C} \\\  
& = (1-\beta-\gamma) \mathbf{A} + \beta \mathbf{B} + \gamma \mathbf{C} \\\  
& = \mathbf{A} + \beta (\mathbf{B} - \mathbf{A}) + \gamma (\mathbf{C} -\mathbf{A})  
\end{aligned} $$

在得到最后的这个形式后，我们可以把 $(\beta, \gamma)$ 这个坐标看做以 A 为原点，由 BA、CA
张成的非规范二维坐标系中的坐标，如下图所示。

![image 6 - MIT 6.837：Ray Casting 光线投射](https://ksmeow.moe/wp-content/uploads/2021/10/image-6.png)

![image 7 - MIT 6.837：Ray Casting 光线投射](https://ksmeow.moe/wp-content/uploads/2021/10/image-7.png)

接下来介绍一种计算某一点重心坐标的几何方法。考虑求对顶点 A 坐标对应权重的重心坐标值，如上图所示，先将 P
点与三个顶点作连线，会将三角形分割成三个小三角形，而重心坐标值为 A 点对面的小三角形面积与总面积之比。

还有一种代数计算的方法，类似之前的几何体，将射线方程代入重心坐标的表达式中，得到

$$ \mathbf{R_o} + t \mathbf{R_d} = \mathbf{A} + \beta (\mathbf{B} -\mathbf{A}) + \gamma (\mathbf{C} - \mathbf{A}) $$

将三个维度分开，则实际上得到了三个关于未知数 $t, \beta, \gamma$ 的线性方程，整理得

$$ \begin{cases}  
(a_x - b_x) \beta + (a_x - c_x) \gamma + R_{dx} t & = a_x - R_{ox} \\\  
(a_y - b_y) \beta + (a_y - c_y) \gamma + R_{dy} t & = a_y - R_{oy} \\\  
(a_z - b_z) \beta + (a_z - c_z) \gamma + R_{dz} t & = a_z - R_{oz}  
\end{cases} $$

而这样的线性方程容易表达成矩阵与列向量的形式

$$  
\begin{bmatrix}  
a_x - b_x & a_x - c_x & R_{dx} \\\  
a_y - b_y & a_y - c_y & R_{dy} \\\  
a_z - b_z & a_z - c_z & R_{dz}  
\end{bmatrix}  
  
\begin{bmatrix}  
\beta \\\  
\gamma \\\  
t  
\end{bmatrix}  
  
=  
  
\begin{bmatrix}  
a_x - R_{ox} \\\  
a_y - R_{oy} \\\  
a_z - R_{oz}  
\end{bmatrix}  
$$

对这个矩阵方程应用 Cramer 法则，可以得到未知数的解，Cramer 法则的求解这里略过。求解出重心坐标后，验证是否满足 $\alpha, \beta,
\gamma \in (0,1)$ 即可知道交点是否位于三角形内。

这种代数方法求交点的方法具有很多优点：矩阵运算是 GPU 擅长的、能顺便算出重心坐标、不需要和平面扯上关系等。

Author: [KSkun](https://ksmeow.moe/author/kskun/ "文章作者 KSkun")

Filed Under: [计算机图形学](https://ksmeow.moe/category/game_development/computer-graphics/), [游戏开发](https://ksmeow.moe/category/game_development/)

