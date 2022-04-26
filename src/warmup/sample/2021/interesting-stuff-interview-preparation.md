2021年8月31日

# 面经里的一些有趣的事情

![面经里的一些有趣的事情](https://ksmeow.moe/wp-content/uploads/2021/08/houkai3-kiana-2-opt.jpg)

 _注 ：2021 秋招结束啦！这篇文章可能不会再更新，或者在下一次招聘季再更新，祝大家好运！_

目录

  * 1 语言
    * 1.1 C++
      * 1.1.1 volatile
      * 1.1.2 C++ 如何处理函数返回值（不带编译器优化）
  * 2 操作系统
    * 2.1 进程、线程、协程
      * 2.1.1 C++ std::thread 子线程的栈空间会分布在哪里？
  * 3 数学、几何与图形学
    * 3.1 概率论与随机
      * 3.1.1 如何生成一系列在圆内的随机点？
  * 4 参考资料

## 语言

### C++

#### volatile

volatile 修饰的变量将在编译器不被优化，且保证其指令执行顺序不被乱序，常用于在开启编译器优化开关时保护某一变量与相关指令不被优化。

这一特性在读写外部内存时非常有用[3]，例如如下例子：

    
    
    volatile char *memPtr = 0x40001000;
    while (*memPtr == 1);

如果不标记 memPtr 为 volatile 变量，则编译器会认为底下的循环是无意义的，因为我们没有对 memPtr 写过东西。如果 0x40001000
是外部内存（如 mmap 内存），它由另一程序管理和写入，则这里的循环是有意义的。

常在多线程或底层相关程序中使用 volatile 关键字。 _有 时合理使用也可以让打开编译开关后，不同平台上的浮点数处理行为一致。*个人经历_

#### C++ 如何处理函数返回值（不带编译器优化）

如果在函数体内初始化自动对象变量，那么变量会被分配在栈上。而返回值所在的内存空间被放置在函数栈的顶端，如果以函数内初始化的自动变量返回，则需要将此对象复制到返回值处。在调用处，返回值对象将被复制到别处。

## 操作系统

### 进程、线程、协程

#### C++ std::thread 子线程的栈空间会分布在哪里？

我们都知道有一个经典的 Linux 进程内存分布图[1]（32 位平台下）：

![program in memory2 -面经里的一些有趣的事情](https://gabrieletolomei.files.wordpress.com/2013/10/program_in_memory2.png)

在多线程模型中，多个线程的栈空间与寄存器都是独立管理的，因此需要给子线程单独分配栈空间。这个栈空间显然不能和主线程的放在一起，不然切换线程的时候会冲突，而且本身栈空间不一定够用。
**在 Linux 下，这个空间是通过 mmap 分配的，因此存在于 mmap 区。**[2] _事 实上，通过 malloc
分配在堆中也许是可行的，但这种做法显然没有 mmap 性能优秀。*仅代表个人观点_

关于 mmap 的 flag MAP_STACK，可以参考 Linux manual：<https://man7.org/linux/man-pages/man2/mmap.2.html>

## 数学、几何与图形学

### 概率论与随机

#### 如何生成一系列在圆内的随机点？

参见：<https://ksmeow.moe/how-to-sample-a-circle-uniformly-in-2d-ccs/>

## 参考资料

  1. In-Memory Layout of a Program (Process) « Gabriele Tolomei  
<https://gabrieletolomei.wordpress.com/miscellanea/operating-systems/in-memory-layout/>

  2. linux - Where are the stacks for the other threads located in a process virtual address space? - Stack Overflow  
<https://stackoverflow.com/questions/44858528/where-are-the-stacks-for-the-other-threads-located-in-a-process-virtual-address>

  3. c++ - Why does volatile exist? - Stack Overflow  
<https://stackoverflow.com/questions/72552/why-does-volatile-exist>

Author: [KSkun](https://ksmeow.moe/author/kskun/ "文章作者 KSkun")

Filed Under: [游戏开发](https://ksmeow.moe/category/game_development/)

