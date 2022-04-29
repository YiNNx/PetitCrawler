# Re: 从零开始的 Petit Crawler

- 爬一爬b战up主**崩坏3第一偶像爱酱**的视频评论区！

  获取所有视频信息列表 & 对应视频的高赞评论 并存入db

- 使用[proxy_pool](https://github.com/jhao104/proxy_pool)

- config.json

  - mid - up主主页url内的id
  - likes_min - 设置爬取评论的最小赞数
  - cookie - 自己的cookie

- 一个简单的接口`/video?bv=xxxx`，可返回视频信息以及对应的高赞评论：

  e.g. `GET http://127.0.0.1:5000/video?bv=BV1aW411P7UJ`

  Response:

  ```
  {
      "video_info": {
          "bvid": "BV1aW411P7UJ",
          "aid": 24149246,
          "pic": "http://i0.hdslb.com/bfs/archive/ed881fa267c6e3248573550d551892c99368d120.jpg",
          "title": "《崩坏3》动画短片「女王降临」",
          "pubdate": 1527739201,
          "desc": "简介: 《崩坏3》动画短片「女王降临」正式发布！\n掌控空间、统御崩坏兽的女王终于降临了，在她经过的地方，只留下破坏和死亡……\n\n本片由miHoYo Anime出品，片中印象曲《Befall》由HOYO-MiX制作，电子唱作人尚雯婕演唱。\n视频类型: 原创动画\n相关题材: 崩坏3",
          "owner": 27534330,
          "view": 9624688,
          "danmaku": 74500,
          "reply": 33979,
          "favorite": 239485,
          "coin": 254813,
          "share": 184088,
          "like": 258858
      },
      "comments": [
          {
              "rpid": 838382445,
              "oid": 24149246,
              "mid": 49128862,
              "root": 0,
              "dialog": 0,
              "rcount": 185,
              "ctime": 1528995737,
              "like": 41703,
              "uname": "启世天华",
              "content": "只有看了短片，你才会蓦然醒悟——TM的泰坦和崩坏兽不是一伙的啊！\n你们为什么打我的时候这么齐心协力。"
          },
          ...
      ]
  }
  ```

  

- [optional] 高赞大多都会有表情！统计他们发的表情以及对应的赞数，从而得知使用最频繁的表情，以及用哪些表情可以掌握高赞密码