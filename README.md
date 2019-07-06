<h1 align="center">TCP-KP-I101h使用说明文档</h1>

<p align="right">by <a href="http://www.dxksi.top">dexin</a>@youibot 8/7/2018 10:11:07 PM </p>

<h2>目录</h2>

[1. 模块配置](#1.0)

>[1.1 概述](#1.1)

>[1.2 网络参数配置](#1.2)

>[1.3 通讯模式和参数选择及配置](#1.3)

>[1.4 局域网内使用](#1.4)

>[1.5 互联网内使用](#1.5)

>[1.6 调试端口](#1.6)

[2. TODO list](#2.0)

[3. 关于去除嗅探功能的说明](#3.0)


<h2 id="1.0">1. 模块配置</h2>

<h3 id="1.1">1.1 概述</h3>
>该模块可以为自身配置静态的IP地址，因此只需要将其接入任意路由器即可。

>对于仅需在内网访问场景，只需要将配置端和继电器模块置于同一局域网中即可。 
>对于期望在外网访问的场景，一般有两种方式：

>- 将网络继电器映射到外网中，并将其作为server端使用
>- 采用同服务器建立套接字连接的方式，实现远程继电器控制。

>为实现稳定、易布置的设备管理方法，本方案采用了第二种方法。 

<img src="https://www.easyicon.net/download/png/525279/32/" width="20" hegiht="20"> 采用同服务器直接建立socket连接方式并不利于集群模块的应用场景。</img>

<h3 id="1.2">1.2 网络参数配置</h3>
>配置该继电器需要一台路由器；一台具有连接网络能力、且可运行Python脚本的计算机。

>另外需要将路由器的**网关**设置为192.168.1.1，**子网掩码**设置为255.255.255.0。并将运行可运行python脚本的计算机设置为静态IP，IP地址为：**192.168.1.190**。

>为了测试静态IP配置的正确性，应当在配置完成后，使用ipconfig（win）或ifconfig(linux)等指令查看当前的IP地址。

<img src="https://www.easyicon.net/download/png/525279/32/" width="20"> 静态IP地址完成后，**务必**查看配置是否生效！</img>

>最后您需要确定项目中，继电器是否具备持续访问互联网的能力  &rarr; 

>若仅希望在局域网中访问网络继电器，或者网络继电器不具备持续访问互联网的能力，参考[1.4小节](#1.4)配置继电器；如网络继电器具备互联网访问能力，请参考[1.5小节](#1.5)配置。

<img src="https://www.easyicon.net/download/png/511635/64/" width="20">在部署服务端脚本之前，我**建议**您顺序阅读本说明的[1.3小节](#1.3)小节，完成继电器网络通讯模式的选择和参数的配置，因为这直接决定您服务器脚本的**启动参数**</img>。

<h3 id="1.3">1.3 通讯模式和参数选择及配置</h3>
<h4 style="text-indent:1em">1.3.1 模块初始化</h4>

>将继电器模块的初始化方法为：长按电源输入端附近的按钮，达到5s以上。

<h4 style="text-indent:1em">1.3.2 通讯模式选择及配置</h4>

>继电器模块具备多种通讯模式，如果您直接使用我的python脚本，需要将模块的通讯模式设置为TCP 模式。我选择基于TCP通讯模式是因为这是一种相对高度稳定的通讯方法，当然您也可以根据项目的具体需求进行修改，但是我默认您选择了我相同的思路，一种依托协议的可信通讯方法。

<h4 style="text-indent:1em">1.3.3 网络参数选择及配置</h4>

>TCP通信具有两个较为核心的参数

>- 服务器的**IP地址**：取决于系统的布置模式，互联网下的配置，此处填写您的服务的静态IP地址；局域网配置下，此处填写您的作为服务器的计算机的IP地址。
>- 服务器的**端口地址**：这是一个完全取决于您的参数，您可以在确保该端口没有被其他应用占用的前提下，根据个人喜好选择。不过我在这里强烈推荐您选择6000端口，这也是模块初始化后默认选择连接的端口。

>本质上来说，需要在本步骤选择的参数只有上述两个。之后，使用模块的配置软件配置模块的连接目标IP和端口即可：

><code>AT+DIP=<目标IP\>+<回车符\></code>

><code>AT+DPORT=<目标PORT\>+<回车符\></code>

<img src="https://www.easyicon.net/download/png/525279/32/" width="20" hegiht="20"> AT指令末尾必须携带回车结束符，这对于AT系列的指令是通用的。另外，模块不会响应没有结束符的指令。</img>

<h3 id="1.4">1.4 局域网内使用</h3>
>您需要一台具有静态IP地址的服务器。并确保继电器所在局域网具备互联网访问能力。

>选择合适的python脚本，并转移到您的服务器中。

>启动python程序 <code>python <work_dir\>+app.py <relay_port\> <debugger_port\> </code>

>例如：我在服务器上开放端口6000等待网路继电器连接；并向调试者开放9000端口，等待调试者连接并传入控制指令。app.py文件在D:\prototype下，那么我应当在命令行输入：<code>python D:\prototype\app.py 6000 9000 </code>即可启动服务。

>![](https://i.imgur.com/u8aauXw.png)

<img src="https://www.easyicon.net/download/png/525279/32/" width="20"> 脚本具有两个版本，分别适用于python2和python3。您需要按照计算机中安装的**Python解释器版本**选择。否可能导致脚本程序报错及失效</img>

<img src="https://www.easyicon.net/download/png/511635/64/" width="20"> 您大可不必担心忘记两个端口的输入顺序造成调试问题，如果您在输入指令时记不清参数次序，您可直接输入 <code>python <work_dir\>+app.py </code> 我的程序会自动引导您以正确的顺序输入端口参数。<img>

>![](https://i.imgur.com/9MdGGcE.png)

<img src="https://www.easyicon.net/download/png/511635/64/" width="20"> 接下来，您可直接跳过1.5小节，查看[调试端口](#1.6)小节。<img>

<h3 id="1.5">1.5 互联网内使用</h3>
>希望在互联网中访问网络继电器需要一台具有静态IP地址的服务器。并确保继电器所在局域网具备互联网访问能力。

>互联网中服务器脚本的配置及同局域网中服务器的配置相互一致,但是您需要咨询您服务器的供应商，获取您服务器的静态IP地址。

<h3 id="1.6">1.6 调试端口</h3>
>我创建的Python脚本等价于直接将调试者的指令，转译成模块可读的AT指令，并发送到连接到系统中的模块中，并接收模块的回复指令。

>服务器端的python脚本一旦启动会持续运行，而调试者同服务器可以在任意时刻连接或断开。每次连接后，调试者可以向服务器发送任意数量的操作继电器的请求。

<img src="https://www.easyicon.net/download/png/525279/32/" width="20">请不要允许客户端主动终止同服务器的连接，这会造成服务器的阻塞。如您希望结束本次连接，只需要按照约定，向服务器发送'EX'指令即可，服务器端会主动完成同调试者网络端口连接的切断。<img>

<img src="https://www.easyicon.net/download/png/525279/32/" width="20">请注意，python脚本要求同继电器保持持续的连接，这意味着，如果您的继电器在中间同服务器连接中断，您需要**重启**Python脚本的运行。<img>

> 操作网络继电器的操作指令如下：

<table>
<tr>
    <th width=10%, bgcolor=#afafaf >参数</th>
    <th width=80%, bgcolor=#afafaf >详细解释</th>
</tr>
<tr>
    <td bgcolor=#eeff00>SL</td>
    <td>设置继电器状态为 &rarr; 闭合</td>
</tr>
<tr>
    <td bgcolor=#eeff00>SH</td>
    <td>设置继电器状态为 &rarr; 断开</td>
</tr>
<tr>
    <td bgcolor=#99ff99>TG</td>
    <td>读取当前继电器状态，取反并传递至继电器</td>
</tr>
<tr>
    <td bgcolor=#8f8efe>EX</td>
    <td>通知服务器推出调试者</td>
</tr>
</table>

<h2 id="2.0">2. TODO list</h2>

<input type="checkbox" checked="checked">继电器参数配置

<input type="checkbox" checked="checked">基于socket server的服务器python脚本

<input type="checkbox" checked="checked">基于socket server的服务器python脚本基于socket的局域网内服务端驱动

<h2 id="3.0">3. 关于去除嗅探功能的说明</h2>

>模块支持在线的网络模块的搜索。通PC的5000 端口的UDP 模式向IP 255.255.255.255 目的端口5000 发测试指令：AT，在线的网络模块收到测试指令后回复OK即可实现在局域网中完成模块的嗅探。

<img src="https://www.easyicon.net/download/png/525279/32/" width="20" hegiht="20">在win10环境中实测，发现系统进程已经占用了电脑5000端口的UDP服务，因此自动嗅探功能无法在本电脑上实现。也说明了该模块的网络嗅探功能同Windows系统存在着一定的不兼容性。</img>

>![](https://i.imgur.com/ozJ0m2V.png)

>![](https://i.imgur.com/w6O7wl6.png)