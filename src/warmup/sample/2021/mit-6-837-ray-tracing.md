2021年12月11日

# MIT 6.837：Ray Tracing 光线追踪

![MIT 6.837：Ray Tracing 光线追踪](https://ksmeow.moe/wp-content/uploads/2021/12/mit_6.837_ray_tracing.jpg)

为了解决局部光照无法计算的阴影、反射、透射等光线经多次改变方向后产生的光照问题，光线追踪方法被引入。这里的光线追踪主要指的是计算多次改变传播方向的光线光照的方法，本文将分别介绍如何用光线追踪实现阴影、反射和透射。

目录

  * 1 阴影
  * 2 反射
  * 3 折射
  * 4 真实性

## 阴影

产生阴影的地方一定是因为光源发出的光线在打到该位置前被遮挡了，因此只需要判断光源在该位置是否被遮挡即可。考虑局部光照计算时，先追踪一条从交点到光源的射线（即阴影光线），如果此光线有交点且在光源之前，说明光源的光线被遮挡，此光源不应对像素产生贡献。

由于阴影光线太靠近物体本身，可能会因精度问题和自己求出交点来，产生噪声。故实现时可以将判断交点的 epsilon
值设置的比较小，再将光线起点移出物体一小段距离，这样可以避免自我遮挡带来的噪声。

此外，在追踪阴影光线时还可以进行优化。在局部光照渲染时，我们需要求出离相机最近的交点，以保证物体先后遮挡关系的正确；但对于阴影光线，只需要知道光源和待渲染点之间有无遮挡即可，故不需要求出最近的交点，只要有交点落在光源和待渲染点之间就可以终止追踪。

修改局部光照的逻辑可以得到带阴影光线追踪的渲染逻辑，伪代码如下：

    
    
    color = ambient*hit->getMaterial()->getDiffuseColor()
    for every light 
        Ray ray2(hitPoint, directionToLight)
        Hit hit2(distanceToLight, NULL, NULL)
        For every object
            object->intersect(ray2, hit2, 0)
        if (hit2->getT() = distanceToLight)
            color += hit->getMaterial()->Shade
                    (ray, hit, directionToLight, lightColor)
    return color

## 反射

回忆一下 ~~小
学二年级~~大学物理/电磁波里面学过的反射，反射光线的传播方向应该与入射光线关于法线对称，强度与入射光存在反射系数的关系。这个反射系数在真实物理规律中的具体计算涉及到一些高深的电磁波理论，在渲染时一般根据效果来为材质指定，也有
PBR 使用更真实的菲涅尔项来计算反射系数。

![.png - MIT 6.837：Ray Tracing 光线追踪](https://ksmeow.moe/wp-content/uploads/2021/12/%E5%9B%BE%E7%89%87.png)

首先解决反射光的方向问题，即如何计算和入射方向关于法线对称的方向。如上图所示，将入射方向向量起点平移至交点处，此时入射方向、反射方向构成了一个等腰三角形，另外一边的方向与法向平行，且长度为
$\cos \theta_v = -\boldsymbol{V} \cdot \boldsymbol{N}$，故容易计算 $\boldsymbol{R} =
\boldsymbol{V} - 2(\boldsymbol{V} \cdot \boldsymbol{N}) \boldsymbol{N}$。

得到了反射方向后，沿此方向追踪一条反射光线，将其颜色向量与反射系数向量相乘即可。此追踪和上面的阴影光线类似，也需要引入一点偏移以免和自己求出交点。

## 折射

折射与反射类似，由折射方向和折射系数来确定折射的效果。折射方向应遵循斯涅尔定律（折射定律），折射系数通过与反射系数类似的推导也可得到。因此，接下来的重点还是如何得到折射方向。

![1 - MIT 6.837：Ray Tracing 光线追踪](https://ksmeow.moe/wp-content/uploads/2021/12/%E5%9B%BE%E7%89%87-1.png)

首先，根据斯涅尔定律有 $n_i \sin \theta_i = n_T \sin \theta_T$。我们引入单位法向量 $\boldsymbol{N}$
和沿切向传播方向的单位切向量 $\boldsymbol{M}$，如上图所示。

可以将入射方向表示为

$$ \boldsymbol{I} = - \boldsymbol{M} \sin \theta_i + \boldsymbol{N} \cos
\theta_i $$

折射方向表示为

$$ \boldsymbol{T} = \boldsymbol{M} \sin \theta_T - \boldsymbol{N} \cos
\theta_T $$

首先得到 $\boldsymbol{M} = \dfrac{\boldsymbol{N} \cos \theta_i -\boldsymbol{I}}{\sin \theta_i}$，代入折射方向的表达式

$$ \boldsymbol{T} = \frac{\sin \theta_T}{\sin \theta_i} ( \boldsymbol{N} \cos
\theta_i - \boldsymbol{I} ) - \boldsymbol{N} \cos \theta_T $$

定义 $n_r = \dfrac{\sin \theta_T}{\sin \theta_i} = \dfrac{n_i}{n_r}$，则 $\sin
\theta_T = n_r \sin \theta_i$，代入上式并整理得

$$ \boldsymbol{T} = (n_r \cos \theta_i - \cos \theta_T) \boldsymbol{N} - n_r
\boldsymbol{I} $$

由于方向向量都是单位向量，有 $\cos \theta_i = \boldsymbol{N} \cdot \boldsymbol{I}$，而根据三角关系得
$\cos \theta_T = \sqrt{1 - \sin^2 \theta_T} = \sqrt{1 - n_r^2 \sin^2 \theta_i}
= \sqrt{1 - n_r^2 [1 - (\boldsymbol{N} \cdot \boldsymbol{I})^2]}$，代入上式得

$$ \boldsymbol{T} = \left\\{ n_r (\boldsymbol{N} \cdot \boldsymbol{I}) -\sqrt{1 - n_r^2 [1 - (\boldsymbol{N} \cdot \boldsymbol{I})^2]} \right\\}
\boldsymbol{N} - n_r \boldsymbol{I} $$

这样就可以根据入射方向的反向与法向量得到折射方向了。

注意到此处存在一个根号，当根号内的表达式为负值时，折射光线没有解，发生全反射。全反射发生的条件 $\sin^2 \theta_T =
\left(\dfrac{n_i}{n_T}\right)^2 \sin^2 \theta_1 > 1$，这只在从光密介质中射向光疏介质时发生。

在真实的物理世界中，一束白光经过三棱镜会得到一系列不同颜色的光，被称为色散，这说明折射率 $n$ 也与波长有关，但一般在渲染时忽略色散现象。

## 真实性

上面提到的光线追踪符合真实的物理结果吗？答案是不。

我们所使用的光线追踪的规律，只是物理规律的一个简化。例如，不是所有渲染器都以菲涅尔项处理光线的反射系数，色散也经常被忽略，且我们总是从相机出发追踪光线，而现实中光线从光源射入相机。这种从相机开始追踪的方法被称为反向光线追踪，它是由一些看起来效果不错，但并不完全符合物理实际的技巧完成的；在后面，我们会有办法更接近物理实际一些。

Author: [KSkun](https://ksmeow.moe/author/kskun/ "文章作者 KSkun")

Filed Under: [计算机图形学](https://ksmeow.moe/category/game_development/computer-graphics/), [游戏开发](https://ksmeow.moe/category/game_development/)

