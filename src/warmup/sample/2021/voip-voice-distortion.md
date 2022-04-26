2021年2月16日

# VoIP 中的话音失真问题分析

![VoIP 中的话音失真问题分析](https://ksmeow.moe/wp-content/uploads/2021/02/genshin-keqing-1-opt.jpg)

By KSkun, 2021/2

目录

  * 1 前言
  * 2 VoIP 是什么？
  * 3 话音失真现象
    * 3.1 语音卡顿
    * 3.2 「电音」
    * 3.3 ITU-T G.711 附录 I
  * 4 结语
  * 5 参考资料

## 前言

2020
年的疫情使得我经历了一整个学期的网课。课程资源的电子化有方便保存和分享的有点，但是网络状况等问题依然使线上教学成为一件非常折磨人的事情。我依然记得，在这半年里我经历了无数次的自己掉线、老师掉线、声音卡顿、视频变静止或者变糊等一系列问题。有时声音还会变的
**不 自然**，有一种 **电 音**的感觉 ~~（ 导致了某同学被称为电音女王）~~。

为什么网络状况不佳会导致声音的 **卡 顿、不自然**和出现电音一样的 **失 真**呢？这便是本文将要探讨的问题。

## VoIP 是什么？

既然需要研究在线语音通话，就必须先了解其工作原理。

面对面说话时，声音作为机械波通过空气等传播；打电话时，声音被转换为电信号，并通过电话网络传播到对方电话，再将电信号转换回声音；线上语音通话时，声音通过麦克风被设备采集为数字信号，再通过
IP 网络传输到对方设备上，这便基于 VoIP 技术。

![voip struct - VoIP 中的话音失真问题分析](https://ksmeow.moe/wp-content/uploads/2021/02/voip_struct.png)图 1 VoIP 的系统结构[1]

 **VoIP （Voice over IP，基于 IP 的语音传输）**是指利用 IP
网络与相关编码、协议、算法，对语音进行采集、处理、传输与还原的一种语音通话技术。[2]根据描述，我们可以把 VoIP 的工作流程整理如下：

  1. 输入：声音从麦克风输入设备，设备将其转换为数字信号；
  2. 编码：将一定时长的声音信号按指定规则编码；
  3. 传输：使用 RTP（Realtime Transport Protocol，实时传输协议）协议在 IP 网络上传输声音数据；
  4. 处理：利用一些规则与算法减少网络抖动的影响、提高声音质量与抑制回声等；
  5. 输出：通过音频设备输出处理后的声音。

网络不佳主要影响第 3 步的传输过程。为了提供更好的实时性，RTP 协议工作在 UDP 协议之上，而 UDP
协议提供无保证的传输，因此容易发生丢包、乱序等问题。RTP
协议中，一个数据包包含一些必要的信息与一小段声音数据，因此丢包造成的影响直接体现为缺失某一段声音。[3]

## 话音失真现象

我们已经知道使用在线语音通话时，声音失真的问题应该是由丢包导致的，但丢包如何导致我们观察到的这些现象呢？接下来我们就将研究这一问题。

 ~~请 注意：以下内容使用的示例可能会让您血压升高。~~

### 语音卡顿

由于 VoIP 基于 UDP 协议传输数据，而 UDP
是不可靠的，导致丢包时有发生。且因为通话的实时性，我们也无法重传丢失的数据，因此如何填充音频流中的空缺部分成为一个问题。

一个选择是直接填充空白，这可能导致说话时，音节中出现不自然的空白。这种情况听起来一卡一卡的，即卡顿现象。下面是一段在 10%
丢包率下，以空白填充缺失部分的语音示例：[4]

10pct_rand_silence.wav *请在参考资料中获取音频

通过这个示例，我们发现，如果空缺部分覆盖了语音的辅音，很容易造成语音难以辨认。且空白段的存在造成了部分爆破音与不自然的听感，听起来非常难受。

### 「电音」

在空缺部分填充空白的效果不佳，因此需要采用其他方法填充，这便是 **PLC （Packet Loss
Concealment，丢包隐藏）算法**。一种常用的方法是重复输出最后收到的一小段，这在丢包率较低的时候效果良好，但当丢包率升高时，则容易出现类似合成声音的机械音（robotic）效果，也就是所谓的电音。下面是一段在
40% 丢包率下，以重复播放最后一段填充的语音示例：[5]

40pct_rand_plc.wav *请在参考资料中获取音频

接下来的问题是，为什么这种方法会使声音听起来像合成声音。不妨换个角度，先来看看如何制造听起来很机械的合成声音。Valve 公司开发的 Portal
系列游戏中有一个人工智能角色 GLaDOS，其语音就具有这样的特点，以下是 Portal 2 游戏中的一个片段：[6]

GLaDOS_voice.mp4 *请在参考资料中获取音频

Valve Developer Community
中给出了一种将正常语音处理出此效果的方法：固定声调、抑制声调变化[7]，这可以通过某些声音处理软件实现。接下来，我们通过 Melodyne
软件来对一段正常的语音进行以上处理，以制造类似电音的效果。

【Melodyne 使用】 *请自行搜索相关示例

通过这个例子，我们知道，如果声调变化较小，声音听起来就像合成声音。而如果我们连续重复播放最后一段，由于传输时音频切分的较短，会使填充的部分声调单一化，出现类似以上处理的效果。这也说明，通过重复最后一段进行
PLC 处理的做法不总是能得到好的效果，我们需要改进。

### ITU-T G.711 附录 I

国际电信联盟在文档 ITU-T G.711 附录 I 中提供了一种比较好的 PLC 算法。该算法工作在 PCM（Pulse Code
Modulation，脉冲编码调制）编码下，采样频率为 8kHz，且一帧为 10ms（80 个样本），流程如下：[8]

  1. 在正常接收数据时，保存最后的 48.75ms 数据且延迟 3.75ms 输出；
  2. 遇到第一个丢帧时，进行如下工作：
    * 估计声音的周期：用最后的 20ms 声音向前计算相关性数值，取相关性最强的位置计算周期；
    * 填充第一个丢帧：使用计算出的最后一个周期重复来填充第一个丢帧，且前后各取 1/4 周期做平滑过渡的处理；
    * 将生成的一帧保存下来；
  3. 如果第一个丢帧之后还有丢帧，此时继续重复周期将可能生成不自然的声音，因此要引入变化与衰减来调整声音；
  4. 与之后正常数据的衔接处也需要平滑过渡处理。

这种处理方式引入了周期的估计、过渡平滑与引入衰减等处理，相比机械地重复最后一帧效果有极大提升。下面是一段 40% 丢帧率下，使用此方法填充丢帧的示例[9]：

male1_3_itut_20ms_40.wav *请在参考资料中获取音频

可以观察到，此方法填充后效果良好。但与机械重复相比，此方法必须进行大量数学运算且必须引入延迟，可能影响通话效果。

## 结语

本文中，我们简单介绍了 VoIP，并研究了 VoIP
中影响通话质量的问题表现、原因，也讨论了几种对于此问题的解决方法。语音通话是一项要求强实时性的业务，用户可以忍受一定程度上的丢帧，我们必须在延迟和丢帧影响上做平衡。因此，也许我们可以使用更好的方法处理丢帧问题，但由于会引入延迟、消耗算力，实际应用中有时不会采用这些方法。

本文并未深入介绍 VoIP
的相关原理，也只提到了几种解决丢帧问题的方法。在这些方法之外，还有其他从信号处理或人工智能角度解决问题的方法，有兴趣的读者可以自行了解。

## 参考资料

  * [1] Seminar On VoIP（Ankita Kankani） <https://www.slideshare.net/ankitakankani/voip-17170086>
  * [2] VoIP - 维基百科，自由的百科全书（维基百科） <https://zh.wikipedia.org/wiki/VoIP>
  * [3] 实时传输协议 - 维基百科，自由的百科全书（维基百科） <https://zh.wikipedia.org/wiki/%E5%AE%9E%E6%97%B6%E4%BC%A0%E8%BE%93%E5%8D%8F%E8%AE%AE>
  * [4] VoIP Troubleshooter | Problems | Gaps in Speech（VoIP Troubleshooter LLC） <https://www.voiptroubleshooter.com/problems/gaps.html>
  * [5] VoIP Troubleshooter | Problems | Robotic Speech（VoIP Troubleshooter LLC） <https://www.voiptroubleshooter.com/problems/robotic.html>
  * [6] Portal 2 - Boss GLaDOS - YouTube（Christoffer Norberg） <https://www.youtube.com/watch?v=tJJf8yUMKEU>
  * [7] Creating a Portal AI Voice - Valve Developer Community（Thelonesoldier） <https://developer.valvesoftware.com/wiki/Creating_a_Portal_AI_Voice>
  * [8] ITU-T G.711 Appendix I: A high quality low-complexity algorithm for packet loss concealment with G.711（ITU） <https://www.itu.int/rec/T-REC-G.711-199909-I!AppI/en>
  * [9] VoIP Troubleshooter | Packet Loss Concealment（VoIP Troubleshooter LLC） <http://www.voiptroubleshooter.com/problems/plc.html>

Author: [KSkun](https://ksmeow.moe/author/kskun/ "文章作者 KSkun")

Filed Under: [Web开发](https://ksmeow.moe/category/web-dev/),
[Slider](https://ksmeow.moe/category/slider/)

