2021年10月21日

# MIT 6.837：Local Illumination 局部光照

![MIT 6.837：Local Illumination 局部光照](https://ksmeow.moe/wp-content/uploads/2021/10/mit6.837_local_illumination.jpg)

局部光照是一种较为简单的渲染方式，它仅依赖视线与物体交点的材质、法线与光源到该点的光照计算像素的颜色，而不考虑多次反射的光线对像素颜色的贡献，因此计算开销比较小，渲染速度快。早期的电子游戏与动画普遍采用了这种方式。

目录

  * 1 双向反射分布函数（BRDF）
  * 2 关于光照的基本结论
    * 2.1 线性性
    * 2.2 平方反比
    * 2.3 $\cos \theta$ 法则
  * 3 局部光照模型
    * 3.1 理想漫反射模型
    * 3.2 理想镜面反射模型
    * 3.3 Blinn-Phong 模型
  * 4 参考资料

## 双向反射分布函数（BRDF）

在考虑如何渲染之前，我们首先考虑如何定义一种材质。材质对渲染的影响在于其如何反射光源射进的光线，因此我们可以定义这样一种函数 $R(\theta_i,
\phi_i; \theta_o,
\phi_o)$，输入视线到材质上一点的方向与光源的方向，输出为被材质反射的光照辐射率比例。光照辐射率（radience）表示单位立体角单位面积的辐射功率，或可以简单理解为某处沿某一方向的光照功率，其
SI 单位为 $\mathrm{W \cdot sr^{-1} \cdot m^{-2}}$。

![image 12 - MIT 6.837：Local Illumination 局部光照](https://ksmeow.moe/wp-content/uploads/2021/10/image-12.png)

上图展示了如何求一个点的光照。首先得到光源向此方向发出的辐射率 $L_i$，根据入射和反射方向求出 BRDF 的值 $R$，则反射到相机中的辐射率为
$L_o=RL_i$。

如果材质表现出各向同性，即旋转材质平面后 BRDF 的值不发生变化，则此时 BRDF 只关心入射和出射方向方位角的差值 $|\phi_i -\phi_o|$，函数退化为一个三维函数。

我们可以使用特制的测量工具测量一个现实材质的 BRDF，并采样记入数据库，利用这样得到的 BRDF 与光线追踪技术可以获得近乎逼真的渲染结果。但通常这样的
BRDF 函数数据量过大，不适用于需要即时渲染的场景，在这种场景中我们将使用经验模型来代替基于物理原理的渲染模型。

## 关于光照的基本结论

### 线性性

能量具有线性性质，因此功率也具有，辐射度量学中的这些物理量派生自辐射功率，因此也具有线性性质。这一性质是好用的，因为我们可以分别求出每个光源对场景的作用，将其叠加起来就得到了所有光源作用时的结果。

### 平方反比

辐射率（radience）满足平方反比关系，即假设光源在某方向上的辐射率为 $L_0$，则在同一方向上距离 $r$ 外的某处辐射率变为
$L_0/r^2$。这可以由通量不变、立体角不变、球面面积变大 $r^2$ 来给出推导证明。

### $\cos \theta$ 法则

![image 14 - MIT 6.837：Local Illumination 局部光照](https://ksmeow.moe/wp-content/uploads/2021/10/image-14.png)

当光线与平面法线成 $\theta$ 角度入射平面时，平面实际吸收的辐射率只有原本的 $\cos \theta$
倍。由上图所示，当平行光入射方向与平面不垂直时，入射的能量并非全部被平面吸收，而吸收的部分只是它的垂直分量，即 $\cos \theta$ 的部分。

## 局部光照模型

除了基于真实 BRDF 的渲染，在局部光照中还有各种基于近似与经验的模型，在此部分我们将介绍这些模型。

### 理想漫反射模型

这是一种最简单的模型，如黏土、粉笔等表面非常粗糙的材质会看起来比较像这种模型。

![image 15 - MIT 6.837：Local Illumination 局部光照](https://ksmeow.moe/wp-content/uploads/2021/10/image-15.png)

这种模型会将吸收的能量均匀地反射到所有出射方向上，因此可以简单地写出出射辐射率。

$\cos \theta$ 可以通过单位入射方向向量的反向向量 $\mathbf{l}$ 与单位法向量 $\mathbf{n}$
的点乘求出，因此吸收的辐射率为 $\max(0, \mathbf{n} \cdot \mathbf{l})
\dfrac{L_i}{r^2}$，乘上一个常系数即可得到出射辐射率 $L_o = k_d \cdot \max(0, \mathbf{n} \cdot
\mathbf{l}) \dfrac{L_i}{r^2}$。

由于光源可能在交点所在平面的背面，此时点乘的结果为负数，这样的入射光线会被物体遮挡而无法提供能力，因此我们通过一个 $\max(0, \mathbf{n}
\cdot \mathbf{l})$ 将这种情况也考虑进去了。

系数 $k_d$ 的选择与材质颜色有关。

### 理想镜面反射模型

这是另一种简单的模型，如镜子、光滑的金属表面等看起来像这种模型。

![image 16 - MIT 6.837：Local Illumination 局部光照](https://ksmeow.moe/wp-content/uploads/2021/10/image-16.png)

它只是把入射的能量通过入射方向关于法线对称的方向反射出去，其他方向均没有出射。

### Blinn-Phong 模型

![image 17 - MIT 6.837：Local Illumination 局部光照](https://ksmeow.moe/wp-content/uploads/2021/10/image-17.png)

这是一种经验模型，它不基于物理原理，而是提供了一种效果还不错的近似解。

我们考虑对于粗糙程度一般的物体，其必然存在一定的镜面反射和漫反射，因此在各个方向都会有出射量，但越靠近镜面反射方向出射量越大。假设镜面反射方向为
$\mathbf{r}$，则我们可以通过相机方向 $\mathbf{v}$ 和 $\mathbf{r}$ 的夹角 $\alpha$
的大小来决定出射量，角度越小出射量越大，因此 $\cos \alpha$ 是一个很好的比例值选择。Phong 模型的公式由此得出：

$$ L_o = k_s (\mathbf{v} \cdot \mathbf{r})^q \dfrac{L_i}{r^2} $$

式中的 $q$ 是一个参数，容易发现 $q$ 越大则镜面程度越大，表现出材质越光滑。

这种方法需要计算镜面方向 $\mathbf{r}$，考虑法向量是 $\mathbf{l}$ 和 $\mathbf{r}$ 的角平分线，则成立
$\mathbf{l} + \mathbf{r} = (2 \cos \theta) \mathbf{n}$，而得到 $\mathbf{r} = 2
(\mathbf{n} \cdot \mathbf{l}) \mathbf{n} - \mathbf{l}$。

![advanced lighting over 90 - MIT 6.837：Local Illumination
局部光照](https://learnopengl.com/img/advanced-lighting/advanced_lighting_over_90.png)

![advanced lighting phong limit - MIT 6.837：Local Illumination
局部光照](https://learnopengl.com/img/advanced-lighting/advanced_lighting_phong_limit.png)

Phong 模型中存在一个问题，当视线较远时，可能出现视线方向和反射方向之间夹角大于 90° 的情况，此时 $\cos \theta$
值为负数，此光源的贡献降为 0。这容易导致画面中不自然的亮度骤减，如上图所示。

![image 18 - MIT 6.837：Local Illumination 局部光照](https://ksmeow.moe/wp-content/uploads/2021/10/image-18.png)

Blinn-Phong 模型可以改善这一问题。我们不再研究反射方向与视线方向的关系，而研究半程向量，即 $\mathbf{h} =
\dfrac{\mathbf{l} + \mathbf{v}}{||\mathbf{l} +
\mathbf{v}||}$，与法线的关系。如果视线方向接近反射方向，半程向量将靠近法线，而 $\cos \beta$ 的值越大，可以达到和原始 Phong
模型类似的效果（但不完全相同）。Blinn-Phong 的公式为：

$$ L_o = k_s (\mathbf{n} \cdot \mathbf{h})^q \dfrac{L_i}{r^2} $$

由于半程向量与法线的夹角一定为锐角，Phong 模型中的亮度突变将不会发生，但此角度 $\beta$ 一般比视线与反射方向的夹角 $\alpha$
更小，$\cos \beta$ 比 $\cos \alpha$ 更大，因此在参数 $q$ 相同时 Blinn-Phong 会更亮一些。

上面主要给出了一种有镜面反射特性、又不完全是镜面反射的模型，我们将这一结果作为镜面反射项，同时根据理想漫反射模型引入漫反射项 $k_d \cdot
\max(0, \mathbf{n} \cdot \mathbf{l})
\dfrac{L_i}{r^2}$，再加入环境光照项（表达场景中多次反射的环境光）$k_a L_a$，就得到了 Blinn-Phong 模型的完整公式：

$$ L_o = k_a L_a + [k_d \cdot \max(0, \mathbf{n} \cdot \mathbf{l}) +
(\mathbf{n} \cdot \mathbf{h})^q] \dfrac{L_i}{r^2} $$

通常颜色通过 RGB 三个分量表达，分别对三个分量计算该分量下的辐射率，即可得到最终的像素颜色值。

## 参考资料

  * MIT 6.837 Fall 2004
  * GAMES101
  * <https://learnopengl.com/Advanced-Lighting/Advanced-Lighting>

Author: [KSkun](https://ksmeow.moe/author/kskun/ "文章作者 KSkun")

Filed Under: [计算机图形学](https://ksmeow.moe/category/game_development/computer-graphics/), [游戏开发](https://ksmeow.moe/category/game_development/)

