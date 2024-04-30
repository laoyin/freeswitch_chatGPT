# Freeswitch-ChatGPT
## 演示识别
[查看freeswitch-chatGPT demo视频](https://www.zhihu.com/pin/1632180684897804288)
## 打赏
开发不易,欢迎打赏  
<p align="center">
  欢迎打赏-咨询
<img src="https://github.com/laoyin/java-sip-mrcp/blob/master/audio/200-zixun.jpg"  height="500" width="450">
</p>

## 项目概述
本项目实现了通过 FreeSWITCH-SIP 电话与 chatGPT 的联合使用，具体包括部署 FreeSWITCH 和 MRCP 服务，并利用 chatGPT 进行交互。

主要第三方服务
- 大语言模型(LLM):  opneai gpt
- 语音识别（ASR）: 项目中使用了科大讯飞的语音识别技术可以实时将用户的语音转换成文本
- 文本到语音（TTS）: 项目中使用了科大讯飞的文本到语音技术，经文字转为语音

## 数据流
FreeSWITCH 通过 Media Resource Control Protocol (MRCP) 向科大讯飞请求服务的过程涉及几个关键步骤。MRCP 是一种网络协议，用于控制音频和视频资源的媒体服务器。在 FreeSWITCH 和科大讯飞的场景中，MRCP 允许 FreeSWITCH 作为客户端（通常称为 MRCP 客户端）与远程语音识别和合成服务（作为 MRCP 服务器）进行通信。下面是整个流程的详细说明：

### 1. MRCP 服务器设置
在使用科大讯飞的服务之前，首先需要设置一个 MRCP 服务器。这个服务器会与科大讯飞的 API 接口进行对接，处理来自 FreeSWITCH 的 MRCP 请求。通常情况下，你会使用一个中间件，如 unimrcp 服务器，这个中间件配置了与科大讯飞服务的连接细节，如 API 密钥、服务器地址等。

### 2. 配置 FreeSWITCH
FreeSWITCH 需要配置以连接到 MRCP 服务器。这包括在 FreeSWITCH 配置文件中设置 MRCP 服务器的 IP 地址、端口、以及其他必要的通信参数。例如，在 FreeSWITCH 的 `mrcp_profiles` 文件夹中，你可能会添加一个 XML 配置文件，指定 MRCP 服务器的详细信息。

### 3. 发送语音请求
当 FreeSWITCH 接收到一个电话呼入时，它将根据预设的应用逻辑（如 IVR 应用）处理呼叫。如果需要进行语音识别或语音合成，FreeSWITCH 会通过 MRCP 将请求发送到配置好的 MRCP 服务器。

#### 示例 MRCP 请求：
- **语音识别（ASR）**: FreeSWITCH 发送一段音频流到 MRCP 服务器，请求将其转换为文本。
- **文本到语音（TTS）**: FreeSWITCH 发送文本到 MRCP 服务器，请求转换为音频流。

### 4. MRCP 服务器处理请求
MRCP 服务器接收到请求后，会将相应的语音识别或文本到语音请求转发到科大讯飞的服务器。科大讯飞处理这些请求并返回结果。

### 5. 返回结果
MRCP 服务器收到科大讯飞的处理结果后，将结果通过 MRCP 协议返回给 FreeSWITCH。对于 ASR，这通常是识别出的文本；对于 TTS，是生成的音频流。

### 6. FreeSWITCH 处理结果
FreeSWITCH 接收到结果后，根据业务逻辑进行相应的处理，如根据用户的语音输入提供相应的服务或信息。

通过以上步骤，FreeSWITCH 能够借助 MRCP 协议和科大讯飞的强大语音技术，实现高效的语音交互系统。这种集成提供了强大的语音识别和生成能力，极大地增强了电话系统的交互性和用户体验。

## 如何使用

### 部署 FreeSWITCH
使用 Docker 来部署 FreeSWITCH：
- [Docker 部署 FreeSWITCH](https://github.com/laoyin/freeswitch_docker_file)

### 部署 MRCP 服务
- MRCP 服务可选择使用第三方服务（如百度、腾讯）或自研。这里提供了基于讯飞的自研 MRCP-server 方式。
- 可以通过 QQ:263733228 联系进行自研 MRCP-server 开发，支持 ASR、实时语音转写质检等功能。


[参考资料](https://github.com/wangkaisine/mrcp-plugin-with-freeswitch)
这是目前github上star最多的中文mrcp对接freeswitch，写的很详细，但是里面有一些坑，如果你不注意，可能就无法得到你想要的。

1：mrcp-server 部署搭建. 注意，mrcp-server里面的坑，代码基本都修复了，你只需要修改 你的appid即可

编译依赖后，及得在编译mrcp-server时候，
```

./configure --with-apr=/opt/mrcp/MRCP-Plugin-Demo-master/unimrcp-deps-1.5.0/libs/apr --with-apr-util=/opt/mrcp/MRCP-Plugin-Demo-master/unimrcp-deps-1.5.0/libs/apr-util

```

其中后面 --with-apr 是我安装的目录和 代码文件对应的目录

这里就有坑，有可能你编译好久都无法成功。



### 配置mrcp-server 和 freeswitch 配置。

freeswitch 你需要配置两个地方，

#### a、你需要新增一个 conf/mrcp_profiles/unimrcpserver-mrcp-v2.xml
```

<include>
 <profile name="unimrcpserver-mrcp-v2" version="2">
   <param name="client-ip" value="127.0.0.1"/>
   <param name="client-port" value="9060"/>
   <param name="server-ip" value="192.168.0.190"/>
   <param name="server-port" value="8060"/>
   <param name="sip-transport" value="udp"/>
   <param name="rtp-ip" value="192.168.0.190"/>
   <param name="rtp-port-min" value="4000"/>
   <param name="rtp-port-max" value="5000"/>
   <param name="codecs" value="PCMU PCMA L16/96/8000"/>
    <param name="speechsynth" value="speechsynthesizer"/>
    <param name="speechrecog" value="speechrecognizer"/>
   <synthparams>
   </synthparams>
   <recogparams>
       <param name="start-input-timers" value="false"/>
   </recogparams>
 </profile>
</include>

```
我上面介绍的，client是freeswitch sip uas，所以你根据你自己的进行配置ip和sip端口

server是你的mrcp-server 配置的sip地址



3：下载训练对应的sdk，

注意要勾选两个，一个是语音听写、一个是tts
```
替换对应的目录，plugins/third-party/xfyun

坑来了，记住了，需要修改代码里面的appkey。！！！！！！！

```

不然tts识别时候就会遇到问题：

MRCP/2.0 83 1 200 IN-PROGRESS
Channel-Identifier: ede2ac36452811ec@speechsynth


2021-11-14 16:57:43:392587 [WARN]   [xfyun] 正在合成 ...
2021-11-14 16:57:43:543463 [WARN]   [xfyun] QTTSAudioGet failed, error code: 10407.
2021-11-14 16:57:43:551022 [INFO]   Process SPEAK-COMPLETE Event <ede2ac36452811ec@speechsynth> [1]
2021-11-14 16:57:43:551051 [NOTICE] State Transition SPEAKING -> IDLE <ede2ac36452811ec@speechsynth>
2021-11-14 16:57:43:551089 [INFO]   Send MRCPv2 Data 192.168.0.190:1544 <-> 192.168.0.190:41578 [122 bytes]
MRCP/2.0 122 SPEAK-COMPLETE 1 COMPLETE
Channel-Identifier: ede2ac36452811ec@speec


10407，就是权限问题，所以记得替换 xfyun_login 方法里面 appid= 后面的星号，其他不用改！！！！，不用改。

坑又来了：

2021-11-14 16:41:52:936062 [NOTICE] Create RTP Termination Factory 192.168.0.190:[5000,6000]
2021-11-14 16:41:52:936073 [INFO]   Register RTP Termination Factory [RTP-Factory-1]
2021-11-14 16:41:52:936086 [INFO]   Load Plugin [XFyun-Recog-1] [/usr/local/unimrcp/plugin/xfyunrecog.so]
2021-11-14 16:41:52:936626 [WARN]   Failed to Load DSO: /lib/libmsc.so: undefined symbol: _ZTVN10__cxxabiv117__class_type_infoE
2021-11-14 16:41:52:936653 [INFO]   Load Plugin [XFyun-Synth-1] [/usr/local/unimrcp/plugin/xfyunsynth.so]
2021-11-14 16:41:52:937044 [WARN]   Failed to Load DSO: /lib/libmsc.so: undefined symbol: _ZTVN10__cxxabiv117__class_type_infoE
2021-11-14 16:41:52:937076 [INFO]   Register RTP Settings [RTP-Settings-1]


项目挺好的，不知道为啥，明明有人反应了问题，但是还是没有人更新代码，难道是半开源【开玩笑】

这个就是需要在Makefile文件加上 -lstdc++

```
./third-party/xfyun/samples/sch_translate_sample/Makefile:18:LDFLAGS += -lmsc -lrt -ldl -lpthread -lstdc++
./third-party/xfyun/samples/iat_online_sample/Makefile:18:LDFLAGS += -lmsc -lrt -ldl -lpthread -lstdc++
./third-party/xfyun/samples/ise_online_sample/Makefile:18:LDFLAGS += -lmsc -lrt -ldl -lpthread -lstdc++
./third-party/xfyun/samples/tts_online_sample/Makefile:18:LDFLAGS += -lmsc -lrt -ldl -lpthread -lstdc++
./xfyun-recog/xfyunrecog.la:20:dependency_libs=' -L../../plugins/third-party/xfyun/libs/x64 -lmsc -ldl -lpthread -lrt -lstdc++'
./xfyun-recog/Makefile.in:359:                              -lmsc -ldl -lpthread -lrt -lstdc++
./xfyun-recog/Makefile:359:                              -lmsc -ldl -lpthread -lrt -lstdc++
./xfyun-recog/.libs/xfyunrecog.lai:20:dependency_libs=' -L../../plugins/third-party/xfyun/libs/x64 -lmsc -ldl -lpthread -lrt -lstdc++'
./xfyun-recog/Makefile.am:8:                              -lmsc -ldl -lpthread -lrt -lstdc++
```

配置完成后，启动看不见报错，说明ok了。

#### c：配置 FreeSWITCH 的拨号计划（dialplan)

配置如下
```
   <extension name="mrcq_demo">
     <condition field="destination_number" expression="^5001$">
                          <action application="set" data="RECORD_TITLE=Recording ${destination_number} ${caller_id_number} ${strftime(%Y-%m-%d %H:%M)}"/>
                          <action application="set" data="RECORD_COPYRIGHT=(c) 2011"/>
                          <action application="set" data="RECORD_SOFTWARE=FreeSWITCH"/>
                          <action application="set" data="RECORD_ARTIST=FreeSWITCH"/>
                          <action application="set" data="RECORD_COMMENT=FreeSWITCH"/>
                          <action application="set" data="RECORD_DATE=${strftime(%Y-%m-%d %H:%M)}"/>
                          <action application="set" data="RECORD_STEREO=true"/>
                          <action application="record_session" data="$${base_dir}/recordings/archive/${strftime(%Y-%m-%d-%H-%M-%S)}_${destination_number}_${caller_id_number}_${call_uuid}.wav"/>
        <action application="answer"/>
        <action application="sleep" data="2000"/>
                <action application="python" data="mrcp"/>
     </condition>
   </extension>
```

这段配置是 FreeSWITCH 的拨号计划（dialplan）配置，它定义了当接收到目的号码为 `5001` 的呼叫时如何处理这个呼叫。拨号计划中的每个 `<action>` 标签代表一个执行的动作，这些动作按顺序执行。下面详细解释这些配置：

##### 配置详解

1. **记录呼叫信息**：
   - `RECORD_TITLE`: 设置录音标题，包括目的号码、来电号码和时间。
   - `RECORD_COPYRIGHT`: 设置录音版权为 "2011"。
   - `RECORD_SOFTWARE`: 指定录音使用的软件是 "FreeSWITCH"。
   - `RECORD_ARTIST`: 设置录音的艺术家名为 "FreeSWITCH"。
   - `RECORD_COMMENT`: 添加关于录音的评论。
   - `RECORD_DATE`: 设置录音日期。
   - `RECORD_STEREO`: 指定录音为立体声。

2. **记录会话**：
   - `record_session`: 这个动作启动录音会话，文件保存在指定路径，包含日期、时间、目的号码、来电号码和呼叫的 UUID。

3. **接听电话**：
   - `answer`: 这个动作指示 FreeSWITCH 接听来电。

4. **延时**：
   - `sleep`: 在执行后续动作前，让 FreeSWITCH 暂停 2000 毫秒（2秒）。这通常用于等待一些初始化操作完成。

5. **执行 Python 脚本**：
   - `python`: 这个动作指示 FreeSWITCH 执行一个名为 `mrcp` 的 Python 脚本。在 FreeSWITCH 配置中，必须有一个与此名字相对应的 Python 脚本配置，通常在 `autoload_configs/python.conf.xml` 中配置。

##### Python 脚本的运行

当你在拨号计划中指定 `action application="python" data="mrcp"` 时，FreeSWITCH 将查找并运行对应的 Python 脚本。在这个示例中，`mrcp` 应该是在 FreeSWITCH 的 Python 配置中注册的一个脚本名。这个脚本会在 FreeSWITCH 接听电话后执行。

**注意**：具体的 Python 脚本需要在 FreeSWITCH 的 Python 配置文件中进行指定和配置。通常，这个脚本会包含处理语音识别、语音合成、或其他电话功能的代码。例如，它可能通过 MRCP 向语音识别服务器发送请求，接收语音识别结果，并基于结果做出相应的处理。

如果你要查看或修改这个 Python 脚本的内容，你需要找到 FreeSWITCH 服务器上相应的 Python 文件，它的具体位置和内容取决于你的具体配置和业务需求。

#### d：实现asr和文字nlp对话

##### 测试脚本1
```
#encoding=utf-8
from freeswitch import *
def handler1(session, args):
    call_addr='user/1018'
    session.execute("bridge", call_addr)

def handler(session, args):
    #uuid = "ggg"
    #console_log("1", "... test from my python program\n")
    #session = PySession(uuid)
    session.answer()
    session.set_tts_params("unimrcp", "xiaofang")
    session.speak("你好啊，我爱你，中国，哎你你，爱你�")
    #session.execute()
    session.execute("play_and_detect_speech", "say:please say yes or no. please say no or yes. please say something! detect:unimrcp {start-input-timers=false,no-input-timeout=5000,recognition-timeout=5000}builtin:grammar/boolean?language=en-US;y=1;n=2")
    session.hangup()

```
这段 Python 脚本是为 FreeSWITCH 写的，并用于处理来电。脚本使用 FreeSWITCH 的 Python 模块 `freeswitch`，执行一系列的电话会话控制操作。以下是详细的解释：

#### 脚本概述

- **导入模块**: `from freeswitch import *` 语句导入 FreeSWITCH 的 Python API，允许脚本控制电话会话。
- **定义函数**: 脚本定义了两个函数：`handler1` 和 `handler`。

##### 函数 `handler1`

- **功能**: 当被调用时，这个函数将当前电话会话桥接到另一个用户（用户号码1018）。
- **参数**:
  - `session`: 当前的电话会话对象。
  - `args`: 传递给函数的任何额外参数。
- **操作**: 使用 `bridge` 方法将当前会话连接到指定的内部用户 `user/1018`。

##### 函数 `handler`

- **功能**: 这是主要的处理函数，负责接听电话，执行文本到语音转换，并通过 MRCP 服务器启动语音识别。
- **参数**:
  - `session`: 当前的电话会话对象。
  - `args`: 传递给函数的任何额外参数。
- **操作**:
  - `session.answer()`: 接听来电。
  - `session.set_tts_params("unimrcp", "xiaofang")`: 设置文本到语音转换的参数。这里使用的是 MRCP 协议（`unimrcp`），并指定使用的语音为 `xiaofang`。
  - `session.speak(...)`: 通过 MRCP 服务播放指定的中文文本（"你好啊，我爱你，中国，哎你你，爱你�"），这句话直接通过 TTS 转换并播放。
  - `session.execute(...)`: 执行 `play_and_detect_speech` 命令，该命令组合了播放和语音识别功能。它提示用户说“是”或“否”，并使用 MRCP 服务来识别用户的响应。
    - `start-input-timers=false`: 表示不自动开始输入计时。
    - `no-input-timeout=5000`: 无输入的超时时间为 5000 毫秒。
    - `recognition-timeout=5000`: 识别的超时时间也是 5000 毫秒。
    - `builtin:grammar/boolean?language=en-US;y=1;n=2`: 使用内建的布尔语法，用于解析是/否响应，适用于英文。
  - `session.hangup()`: 在执行完以上操作后挂断电话。

这段脚本展示了如何在 FreeSWITCH 中使用 Python 来接听电话，进行语音播放和语音识别。此脚本需要正确配置 MRCP 服务器，以确保 TTS 和 ASR 功能正常工作。
##### 交互机器人
优化一下：做一个简单的交互机器人，python代码如下：
```

#encoding=utf-8
import json
import tempfile
import requests
import xml.etree.ElementTree as ET
import freeswitch as fs
from freeswitch import *


# `UNI_ENGINE`: unimrcp engine
# In Python, `+` is optional for quoted string concatenation, ^_^
UNI_ENGINE = 'detect:unimrcp {start-input-timers=false,' \
        'no-input-timeout=5000,recognition-timeout=5000}'
# this will be ignored by baidu ASR, and `chat-empty` is also available
UNI_GRAMMAR = 'builtin:grammar/boolean?language=en-US;y=1;n=2'

def asr2text(result):
    """fetch recognized text from asr result (xml)"""
    root = ET.fromstring(result)
    node = root.find('.//input[@mode="speech"]')
    text = None
    if node is not None and node.text:
        # node.text is unicode
        text = node.text.encode('utf-8')
    return text

def handler1(session, args):
    call_addr='user/1018'
    session.execute("bridge", call_addr)

def handler(session, args):
    fs.consoleLog('info', '>>> start chatbot service')
    #uuid = "ggg"
    #console_log("1", "... test from my python program\n")
    #session = PySession(uuid)
    session.answer()

    # first 请求proxy-第一句应该返回什么内容，
    answer_sound = Synthesizer()('你好啊，baby。')

    while session.ready():
        # here, we play anser sound and detect user input in a loop
        session.execute('play_and_detect_speech',
                answer_sound + UNI_ENGINE + UNI_GRAMMAR)
        asr_result =  session.getVariable('detect_speech_result')
        if asr_result is None:
            # if result is None, it means session closed or timeout
            fs.consoleLog('CRIT', '>>> ASR NONE')
            break
        try:
            text = asr2text(asr_result)
        except Exception as e:
            fs.consoleLog('CRIT', '>>> ASR result parse failed \n%s' % e)
            continue
        fs.consoleLog('CRIT', '>>> ASR result is %s' % text)
        # len will get correct length with unicode
        if text is None or len(unicode(text, encoding='utf-8')) < 2:
            fs.consoleLog('CRIT', '>>> ASR result TOO SHORT')
            # answer_sound = sound_query('inaudible')
            answer_sound = Synthesizer()('不好意思，我没有听清您的话，请再说一次。')
            continue
        # chat with robot
        # text = Robot()(text)
        fs.consoleLog('CRIT', 'Robot result is %s' % text)
        if not text:
            text = '不好意思，我刚才迷失在人生的道路上了。请问您还需要什么帮助？'
        # speech synthesis
        answer_sound = Synthesizer()(text)
    
    # session close
    fs.msleep(800)
    session.hangup(1)
    # session.set_tts_params("unimrcp", "xiaofang")
    # session.speak("你好啊，我爱你，中国，哎你你，爱你�")
    #session.playFile("/path/to/your.mp3", "")
    #session.speak("Please enter telephone number with area code and press pound sign. ")
    #input = session.getDigits("", 11, "*#", "#", 10000)
    # session.hangup(1)



class Synthesizer:

    def __init__(self):
        self.audiofile = tempfile.NamedTemporaryFile(prefix='session_', suffix='.wav')

    def __call__(self, text):
        if isinstance(text, unicode):
            text = text.encode('utf-8')
        audio = requests.post("http://127.0.0.1:8001/tts_text", files=dict(text=(None, text))).content
        import uuid
        name = str(uuid.uuid1())
        filename = "/tmp/" + name
        with open(filename, "wb") as file:
            file.write(audio.decode())
        return filename
    
```

这个 Python 脚本设计用于 FreeSWITCH 平台，实现一个简单的交互机器人，主要通过语音识别（ASR）和文本到语音（TTS）技术与用户进行交互。以下是对脚本各部分的详细解释：

### 导入模块和配置

- **模块导入**：脚本开始部分导入了必要的 Python 模块，包括处理 JSON、临时文件、网络请求、XML 解析以及 FreeSWITCH 的专用模块。
- **UNI_ENGINE 和 UNI_GRAMMAR**：定义了用于 FreeSWITCH 的 MRCP 引擎配置，控制语音识别的参数，如不自动开始计时器、设置识别超时等。同时定义了一个内置的语法规则，用于解析是/否的语音命令。

### 辅助函数 asr2text

- **功能**：从 ASR 返回的 XML 结果中提取识别的文本。
- **参数**：`result` 是 MRCP 服务器返回的 XML 格式的字符串。
- **处理**：使用 XML 解析来找到包含语音输入的节点，并返回其文本内容。

### 主处理函数 handler

- **功能**：处理来电，通过 ASR 与用户交互，并根据用户的回答进行响应。
- **流程**：
  - **接听电话**：使用 `session.answer()` 接听来电。
  - **初始化 TTS**：使用 `Synthesizer` 类的实例来初始化一个 TTS 响应，首先以一句欢迎语开始。
  - **循环交互**：通过一个循环，不断播放 TTS 响应并等待用户的语音输入。
  - **语音识别**：使用 `play_and_detect_speech` 方法来播放当前 TTS 输出并激活语音识别，等待用户回应。
  - **处理 ASR 结果**：解析 ASR 返回的 XML，提取用户的语音输入。
  - **生成响应**：根据用户的语音输入，生成下一步的 TTS 输出。如果识别内容太短或无法理解，生成一条错误消息要求用户重复。
  - **结束会话**：如果会话结束或超时，使用 `hangup()` 方法挂断电话。

### 类 Synthesizer

- **功能**：将文本转换为语音（TTS）。
- **构造函数**：初始化一个临时文件来保存生成的音频。
- **调用方法**：
  - **参数**：接受一个文本字符串。
  - **处理**：使用 POST 请求向 TTS 服务发送文本，获取生成的音频数据。
  - **返回**：保存音频到临时文件，并返回该文件路径，以便 FreeSWITCH 可以播放该音频文件。

这个脚本展示了如何在 FreeSWITCH 平台上利用 Python 实现一个基本的交互机器人，处理来电，进行语音交互，生成语音反馈，并且控制会话流程。这种设置特别适用于需要通过电话进行客服或自动信息查询服务的场景。


以上为freeswitch-mrcp协议的配置和使用


#### f:接入open ai chatGPT

以下是对接open-ai的 流式接口，使用websocket方式。

open ai

<p align="center">
<img src="https://github.com/laoyin/freeswitch_chatGPT/blob/main/src/open_ai/7_1679898071.gif"  height="500" width="220">
</p>

使用open ai python ask等方式。
