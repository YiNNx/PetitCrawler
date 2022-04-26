2021年12月6日

# 游戏开发自底向下：内存分配与管理

![游戏开发自底向下：内存分配与管理](https://ksmeow.moe/wp-content/uploads/2021/12/genshin-ganyu-3-opt.jpg)

By KSkun, 2021/11

实习时接触了许多关于游戏开发相关的内存话题，在这里分享一些基于 Unity 游戏开发视角可能用得上的底层知识。这个系列将分成 4 期来探讨以下 4 个话题：

  * 内存分配与管理
  * 垃圾回收
  * 内存占用、泄露的排查方法
  * PC、Android 和 iOS 的平台差异

这些内容所参考的都是公开的信息，不会涉及需要保密的内容，请放心食用！

（只是挖了个坑，填不填二说，请不要期待下期 doge.webp）

目录

  * 1 从物理内存到 C# 对象
    * 1.1 物理内存
    * 1.2 虚拟内存
    * 1.3 进程内存模型
    * 1.4 C# 的变量与对象
  * 2 C# 内存管理机制
    * 2.1 托管堆
    * 2.2 小对象堆
    * 2.3 大对象堆
    * 2.4 内存碎片
  * 3 在 Unity 中进行内存性能分析
    * 3.1 Memory Profiler
    * 3.2 脚本 API
  * 4 结语
  * 5 参考资料

## 从物理内存到 C# 对象

### 物理内存

![sdram module 1024x259 - 游戏开发自底向下：内存分配与管理](https://ksmeow.moe/wp-content/uploads/2021/12/sdram_module-1024x259.jpg)图 1 一根 4GB PC3-10600U 内存条[1]

上图是一条由三星电子生产的 4GB 容量的 PC3-10600U (DDR3L-1333) 内存条，上面整齐排列着三星电子生产的、型号为
K4B2G0846D 的 SDRAM 存储器芯片。这样的一个芯片的规格是 256M x 8[2]，也即 256×106 个宽度为 8
的存储单元（字节），故用 MB 来表示它的容量就是 256MB。你需要告诉芯片操作第几个数据单元，芯片则会根据操作读写对应单元。

这个存储器只能完成简单的存取功能，它并不关心你想存什么东西进去，数据和地址对它而言只是一些 0 或 1 的比特。CPU
中的内存管理单元会与它交互，来完成程序中的 IO
指令。只有操作系统才能和具体的内存设备打交道，用户程序并不用关心它的数据会保存在哪颗芯片的第几个单元，也即： **物 理内存对用户程序是透明的。**

### 虚拟内存

![virtual memory space 1024x500 - 游戏开发自底向下：内存分配与管理](https://ksmeow.moe/wp-content/uploads/2021/12/virtual_memory_space-1024x500.jpg)图 2 32 位 Linux
进程虚拟内存空间分布[3]

对于一个 32 位 Linux 系统上运行的程序而言，它的每一个进程（process）都具有一段长 4GB 的内存空间，64
位系统甚至更大。即使你的电脑并不具备 4GB
物理内存也能运行这个程序，这是因为这个内存空间是「虚拟的」，不是每个地址对应的内存单元都被分配并存在于物理内存中。虚拟内存（virtual
memory）的概念由此引入。

![page table - 游戏开发自底向下：内存分配与管理](https://ksmeow.moe/wp-content/uploads/2021/12/page_table.jpg)图 3 页表的工作原理[4]

进程的内存以页（page）为单位管理，如果你需要操作某一内存单元，则操作系统先查询页表（page
table）项，如果对应了物理内存中的单元则操作物理内存，否则需要将对应数据换入物理内存中，再操作物理内存。不存在物理内存中的页可能临时保存于外部存储器中，或未被分配。

综上所述，操作系统提供了 4GB 的虚拟内存空间，却并不是都能被用户程序所使用。能够使用的条件是：处于合理的内存区域内、被分配或被映射。 **操
作系统通过虚拟内存、页式管理的机制彻底屏蔽了物理内存的特性，用户程序只关心自己的虚拟内存空间，而不再需要操心物理内存的种类、接口与大小。但用户程序在需要使用内存时必须注意地址是否合法，新分配内存也需与操作系统交互，不能任意使用内存。**

### 进程内存模型

回到上面的图 2，这张图还包含了非常重要的东西：一个进程如何使用它的虚拟内存空间。这里我们以 C/C++
程序的角度来理解。一个进程的虚拟内存空间中包含许多段，其中包括：

  *  **栈 （stack）：**函数调用和返回信息、自动变量，先进后出
  *  **堆 （heap）：**运行时分配的变量
  *  **数 据段（data segment）：**静态变量、常量等编译时分配的变量
  *  **代 码段（text segment）：**程序的指令

程序运行时可能进行多次函数调用，形成一条调用链，链末端的函数先退出，因此适用先进后出（FILO，first-in-last-out）数据结构，也即栈（stack）。而运行时发生的内存分配，如 `new MyClass;` 或
`malloc(100);`，则在堆区域分配内存。编译时即完成解析的内存（代码、静态变量、常量等）则另分配固定的区域存储。

### C# 的变量与对象

Unity 使用的脚本语言是 C#，这种语言的程序需要在运行时通过 JIT（Just-In-Time）编译器编译至本地指令再执行。此外，C#
运行时也提供了更高层的内存管理抽象与垃圾回收机制。因此，我们在 C# 中创建和使用对象并不是直接基于上面提到的机制，而是与 C#
运行时交互，运行时再与操作系统交互。

在了解 C# 如何管理内存之前，需要对 C# 的变量类型所有了解。C# 的变量类型可分为两类：

  * 值类型（value type）：在变量的内存空间存储值，包括 int、bool、char、double、enum 类型、struct 类型等
  * 引用类型（reference type）：在变量的内存空间中保存引用，通过引用访问堆中的对象，包括 class 类型、delegate、string、object、数组等

 **C# 的栈中保存的是值类型变量的值和引用类型变量的引用，堆中保存引用类型对象。**C#
的栈工作原理与上面的进程内存模型类似，是对系统栈的一个封装；而堆则与系统堆的管理方式大相径庭，因为 C#
提供了自动内存管理和垃圾回收机制，并不需要手动分配和回收内存空间。

## C# 内存管理机制

C# 的内存管理机制主要依赖 CLR（Common Language Runtime）中的垃圾回收（GC，Garbage
Collect）组件完成，本章重点将放在堆内存的分配和管理上，有关垃圾回收的话题会在后续文章中介绍。

### 托管堆

为了与系统堆区分，C# 中引入了一个叫「托管堆（managed heap）」的概念，表示受 C# 运行时垃圾回收组件管理的堆空间。C#
的引用类型对象都在托管堆中分配。

![csharp managed heap 1024x430 - 游戏开发自底向下：内存分配与管理](https://ksmeow.moe/wp-content/uploads/2021/12/csharp_managed_heap-1024x430.png)图 4 托管堆的结构[6]

托管堆分为小对象堆（SOH，Small Object Heap）和大对象堆（LOH，Large Object
Heap），每一部分都由许多内存段（segment）组成，每个段是进程内存中的一段连续内存空间。在运行时启动时，托管堆会预先从系统分配一些段作为初始内存空间。如果一个段被分配殆尽，运行时尝试对段运行
GC，如果还无法分配，则运行时向系统请求新的段来完成分配。

小于 85000B 的对象被分配在小对象堆，超过这一阈值的对象被分配在大对象堆。由于对象的大小差异，这两个区域有着不同的管理方式。

![csharp heap compacting 1024x760 - 游戏开发自底向下：内存分配与管理](https://ksmeow.moe/wp-content/uploads/2021/12/csharp_heap_compacting-1024x760.png)图 5 SOH 和 LOH
中的分配与管理[9]

### 小对象堆

小对象堆保存的主要是体积较小的对象，在内存间复制这样的对象开销不大，因此采用了 **分 代与压缩**的管理策略。

小对象堆的分配总在末尾进行，运行时维护一个当前分配的末尾指针，新分配时直接增加此指针的值并将末尾未分配内存分配给对象即可。如果剩余未分配内存不够，则 GC
会尝试对段进行一次压缩。

GC 运行压缩的过程会将一个段分成若干代，从首部到尾部依次为 Gen 2、Gen 1 和 Gen 0。代数越高，表示存活的时间越久，新分配的对象都属于
Gen 0。当压缩进行时，GC 将被释放的对象移走，需要保留的对象搬运到一起，使段的未分配内存集中在末尾的连续一段，留给下一次分配使用。GC
和压缩结束后各对象的代数增加 1，增加到 2 则不再增加。这样一次操作使得 GC 释放出的未分配区域被移到末尾，用来支持只需移动指针的快速分配。

### 大对象堆

压缩的做法在大对象堆一般难以实现，因为这里的对象较大，搬运时需要较大开销，导致 GC
运行时间长。因此，在大对象堆不使用分代和压缩，只是使用最原始的管理方法：分配内存时，首先找前面的未分配内存碎片中有没有满足要求的，如果没有则在末端分配。

### 内存碎片

![memory fragmentation - 游戏开发自底向下：内存分配与管理](https://ksmeow.moe/wp-content/uploads/2021/12/memory_fragmentation.jpg)图 6 大对象堆中的内存碎片[8]

C# 关于 LOH
的管理方式很容易产生内存碎片，如果大对象的分配顺序不当，先分配较小的对象再分配较大的对象，此时可能因小对象回收出的间隙不足以容纳大对象而被浪费，原本小对象分配的内存区域中产生大量内存碎片。由于分代和压缩机制的存在，小对象堆则不需要担心这一问题。

一种解决内存碎片问题的方法是， **预
先统计出有哪些大对象需要分配，在使用前统一地预先分配这些对象。**较大对象被回收后产生的空缺能够被较小对象利用，因此能够降低内存碎片的比例。

## 在 Unity 中进行内存性能分析

### Memory Profiler

Unity 官方提供了一个很方便的内存分析工具----Memory Profiler，可以在 Package Manager 中找到这款插件，但由于是
Preview 版本，需要在 Project Settings 中勾选 Enable Preview Packages 设置项。

![memory profiler - 游戏开发自底向下：内存分配与管理](https://ksmeow.moe/wp-content/uploads/2021/12/memory_profiler.png)图 7 Memory Profiler 的插件页面![project
settings 1024x604 - 游戏开发自底向下：内存分配与管理](https://ksmeow.moe/wp-content/uploads/2021/12/project_settings-1024x604.png)图 8 Project Settings
中的设置项

安装完成后，可以在菜单栏 Window - Analysis - Memory Profiler 打开插件窗口，如下图所示。

![mp main 1024x520 - 游戏开发自底向下：内存分配与管理](https://ksmeow.moe/wp-content/uploads/2021/12/mp_main-1024x520.png)图 9 Memory Profiler 主界面

在编辑器内启动游戏后，点击上面界面菜单栏中的 Capture
抓取内存快照。此处演示已经抓取了一个，在界面左下角列表中可以看到。点击快照后插件展示内存的基本信息。

![mp summary 1024x520 - 游戏开发自底向下：内存分配与管理](https://ksmeow.moe/wp-content/uploads/2021/12/mp_summary-1024x520.png)图 10 内存使用总览![mp summary2
1024x639 - 游戏开发自底向下：内存分配与管理](https://ksmeow.moe/wp-content/uploads/2021/12/mp_summary2-1024x639.jpg)图 11 分类内存占用块图![mp object
1024x505 - 游戏开发自底向下：内存分配与管理](https://ksmeow.moe/wp-content/uploads/2021/12/mp_object-1024x505.png)图 12 内存对象列表![mp fragmentation
1024x505 - 游戏开发自底向下：内存分配与管理](https://ksmeow.moe/wp-content/uploads/2021/12/mp_fragmentation-1024x505.png)图 13 内存段分布情况

上面的截图反应了插件的主要功能，包括

  * 总览：内存总的分类分析
  * 块图：将对象按类型分类呈现内存占用的大小
  * 对象列表：所有在内存中分配的对象
  * 段分布：内存分布和占用的情况

其中我们在游戏内分配了一个超级大的 int 类型数组，在图 13 中可以找到它。根据上文的描述，从 0x000001c0f8831000
开始的一段内存应该是 C# 大对象堆的一个段。

### 脚本 API

有关内存分析的 C# 脚本 API 都在命名空间 `UnityEngine.MemoryProfiler` 中，你可以通过文档找到它们。

例如，你可以通过 `MemorySnapshot.RequestNewSnapshot()` 请求一个内存快照，拿到
`PackedMemorySnapshot` 对象，它包含的成员如下所示。

![packedmemorysnapshot 1024x240 - 游戏开发自底向下：内存分配与管理](https://ksmeow.moe/wp-content/uploads/2021/12/packedmemorysnapshot-1024x240.png)图 14
PackedMemorySnapshot 的成员[10]

利用这些信息，你可以得到快照获取时内存中的所有对象和对象之间的引用关系，进行二次开发以分析内存。例如，一个第三方插件 Heap
Explorer（<https://github.com/pschraut/UnityHeapExplorer>）就是对此 API 的二次开发。

## 结语

这期文章中自底向上地介绍了 C# 中的内存和对象与系统内存、物理内存的关系，并简单介绍了 C# 管理内存的方法，最后分享了一些在 Unity
中进行内存性能分析的方法。有关垃圾回收机制、内存泄露排查等话题将会在后续的文章中介绍。

所谓「工欲善其事，必先利其器」，进行 Unity 游戏开发的时候，对 Unity 本身的底层工作机制有所了解，有助于在进行 gameplay
开发时实现出性能优的方案。这一系列文章也是为 gameplay 开发者介绍 Unity
中内存相关知识而编写的，旨在为新人开发者降低了解底层知识的门槛。由于作者水平有限，文章难免存在错误或纰漏，欢迎读后提出建议和意见。

这里是 KSkun，一个不知道接下来打算研究啥而胡乱研究的新人开发者，不知道能不能下期再见（狗头）。

## 参考资料

  1. Samsung Ram DDR3 PC3 2RX8 4GB 1333 1600 MHz Desktop Memory 240pin sell 4GB/8GB DIMM 4G 8G 10600U 12800U 1333MHZ 1600MHZ. **Yao Yue Store (AliExpress)**  
<https://www.aliexpress.com/item/32873164329.html>

  2. 2Gb D-die DDR3L SDRAM K4B2G0846D Datasheet (pdf). **Samsung Electronics Co., Ltd.**  
<https://datasheet.ciiva.com/26786/k4b2g0846d-hck0-26786806.pdf>

  3. 虚拟内存[01] 用户内存空间的各个段分布. **Gary Chan ( 知乎)**  
<https://durant35.github.io/2017/10/29/VM1_UserSpaceSegments/>

  4. CS142 Lecture 16 OS Virtual Memory. **University of Northern Iowa**  
<http://www.cs.uni.edu/~fienup/cs142f03/lectures/lec16_OS_virtual_memory.htm>

  5. C# Memory Management - Part 1. **Sena K ılıçarslan (Medium)**  
<https://medium.com/c-programming/c-memory-management-part-1-c03741c24e4b>

  6. Deep Dive Into .NET Garbage Collection. **Nazar Kvartalnyi (DZone)**  
<https://dzone.com/articles/deep-dive-into-net-garbage-collection>

  7. Fundamentals of garbage collection. **Microsoft Docs**  
<https://docs.microsoft.com/en-us/dotnet/standard/garbage-collection/fundamentals>

  8. Managed memory. **Unity Documentation**  
<https://docs.unity3d.com/Manual/performance-managed-memory.html>

  9. Memory Management in C#. **Adam Thorn (Rewind)**  
<https://www.rewind.co/technical-articles/memory-management-c-sharp-lzfz3>

  10. Scripting API. **Unity Documentation**  
<https://docs.unity3d.com/ScriptReference/>

Author: [KSkun](https://ksmeow.moe/author/kskun/ "文章作者 KSkun")

Filed Under: [游戏开发](https://ksmeow.moe/category/game_development/),
[Slider](https://ksmeow.moe/category/slider/)

