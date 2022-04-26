2021年12月4日

# 一次 Git 无法使用公钥的 Debug

![一次 Git 无法使用公钥的 Debug](https://ksmeow.moe/wp-content/uploads/2021/12/genshin-ganyu-2-opt.jpg)

目录

  * 1 问题描述
  * 2 调试步骤
    * 2.1 查看密钥列表
    * 2.2 验证 SSH 连接
    * 2.3 发现要点
  * 3 解决问题
  * 4 参考资料

## 问题描述

打算在命令行里把 Git 的 SSH 密钥配起来，于是按照 Atlanssian 的指引[1]把密钥添加到 `ssh-agent` 里，使用的命令

    
    
    ssh-add ~/.ssh/private.key

使用 `git push` 测试，提示

    
    
    Permission denied (publickey).
    fatal: Could not read from remote repository.
    
    Please make sure you have the correct access rights
    and the repository exists.

看起来 `git.exe` 连 SSH 的时候没用刚才注册的公钥

## 调试步骤

### 查看密钥列表

运行 `ssh-add -l` 提示

    
    
    2048 SHA256:blablablabla C:\Users\kskun\.ssh\private.key (RSA)

看起来密钥有被注册到 `ssh-agent.exe` 里

### 验证 SSH 连接

运行 `ssh -vT [[email protected]](/cdn-cgi/l/email-protection)` 提示

    
    
    Hi KSkun! You've successfully authenticated, but GitHub does not provide shell access.

看起来 `ssh.exe` 能使用注册的密钥认证

### 发现要点

一通乱搞之后在任务管理器里发现了两个 `ssh-agent.exe` 进程，一个用户是 SYSTEM，一个是 kskun，且文件路径一个在
OpenSSH，一个在 Git，发现问题所在。

应该就是因为 Git 使用的 SSH 组件是它自带的，而不是系统默认的，所以需要把 Git 要使用的 SSH 组件指定到 OpenSSH 去。

## 解决问题

在 Git 文档中发现了环境变量 `GIT_SSH`，指定为 `C:\Windows\System32\OpenSSH\ssh.exe`，问题解决。

## 参考资料

  1. Set up an SSH key | Bitbucket Cloud | Atlassian Support  
<https://support.atlassian.com/bitbucket-cloud/docs/set-up-an-ssh-key/>

  2. Git - Environment Variables  
<https://git-scm.com/book/en/v2/Git-Internals-Environment-Variables>

Author: [KSkun](https://ksmeow.moe/author/kskun/ "文章作者 KSkun")

Filed Under: [未分类](https://ksmeow.moe/category/uncategorized/)

