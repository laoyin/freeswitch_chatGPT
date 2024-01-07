

[查看freeswitch-chatGPT demo视频](https://www.zhihu.com/pin/1632180684897804288)
=====


本项目，实现了freeswitch-sip-电话和 chatGPT的连通。

如何实现需要：
a: 部署freeswitch： 可以使用docker方式： [docker 部署 fs](https://github.com/laoyin/freeswitch_docker_file)



b: 部署对应的asr、mrcp服务。
mrcp-server 你可以选择第三方的【百度】【腾讯】或者自研，这里提供的是基于讯飞的自研mrcp-server方式

asr：你可以根据media-bug 自研。

mrcp-server：你可以联系 qq：263733228， 自研mrcp-server，能够实现asr、实时语音转写质检等。


mrcp-server：参考下方

使用mrcp协议，mrcp-server参考前辈的项目，项目已经没有维护了，因此做了所有坑的填补，src/mrcp 需要修改自己的 讯飞appid即可。


【mrcp-server服务编译运行的坑，现在可以替换appid后直接使用】

其实mrcp-server就是实现了，sip协议的，以及rtp协议，将自己作为一个sipserver，freeswitch作为client，进行连接，同时freeswitch将自己的rtp流实时传给mrcp-server。


废话少说，我们直接先根据网上前辈的资料，

https://github.com/wangkaisine/mrcp-plugin-with-freeswitch
​github.com/wangkaisine/mrcp-plugin-with-freeswitch
这是目前github上star最多的中文mrcp对接freeswitch，写的很详细，但是里面有一些坑，如果你不注意，可能就无法得到你想要的。



1：mrcp-server 部署搭建. 注意，mrcp-server里面的坑，代码基本都修复了，你只需要修改 你的appid即可

编译依赖后，及得在编译mrcp-server时候，
```

./configure --with-apr=/opt/mrcp/MRCP-Plugin-Demo-master/unimrcp-deps-1.5.0/libs/apr --with-apr-util=/opt/mrcp/MRCP-Plugin-Demo-master/unimrcp-deps-1.5.0/libs/apr-util

```

其中后面 --with-apr 是我安装的目录和 代码文件对应的目录

这里就有坑，有可能你编译好久都无法成功。



2：配置mrcp-server 和 freeswitch 配置。

freeswitch 你需要配置两个地方，

a、你需要新增一个 conf/mrcp_profiles/unimrcpserver-mrcp-v2.xml
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

c：配置路由，获取asr监听


写上路由: 不用lua，用python

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

d：实现asr和文字nlp对话

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


以上为freeswitch-mrcp协议的配置和使用


f:接入open ai chatGPT

以下是对接open-ai的 流式接口，使用websocket方式。

open ai

<p align="center">
<img src="https://github.com/laoyin/freeswitch_chatGPT/blob/main/src/open_ai/7_1679898071.gif"  height="500" width="220">
</p>

使用open ai python ask等方式。
