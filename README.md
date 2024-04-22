# freeswitch_chatGPT
=====
English | [简体中文](./ZH-README.md)   [查看demo视频](https://www.zhihu.com/pin/1632180684897804288)
Using ChatGPT to connect with FreeSWITCH, creating an intelligent phone robot.


freeswitch-chatGPT
freeswitch-chatGPT is an open-source project aimed at integrating FreeSWITCH with OpenAI's Stream API, as well as implementing MRCP-based ASR (Automatic Speech Recognition) and TTS (Text-to-Speech) using FreeSWITCH.


open ai

<p align="center">
<img src="https://github.com/laoyin/freeswitch_chatGPT/blob/main/src/open_ai/7_1679898071.gif"  height="500" width="300">
</p>


Installation
Before installing freeswitch-chatGPT, make sure you have the following prerequisites:

FreeSWITCH 1.10 or later installed and configured
Python 3.6 or later installed
A valid OpenAI API key
To install freeswitch-chatGPT, follow these steps:

Clone the repository:
bash
```   
Copy code
git clone https://github.com/laoyin/freeswitch_chatGPT.git
Install the required Python dependencies:
```
Copy code
```
pip install -r requirements.txt
Set up your OpenAI API authentication credentials:
javascript
Copy code
export OPENAI_API_KEY=your_api_key_here
Run the installation script:
bash
Copy code
./install.sh
This will create a freeswitch-chatGPT directory in your FreeSWITCH scripts directory, and copy the necessary files there.
```
Usage
freeswitch-chatGPT is divided into three stages, each corresponding to one of the project goals stated above. To use each stage, follow these instructions:

Stage 1: OpenAI Stream integration
To use the OpenAI Stream integration, start a FreeSWITCH session and load the openai_stream.lua script. Then, call the openai_stream() function with the appropriate arguments:

lua
Copy code
openai_stream(model, prompt, length)
where model is the name of the OpenAI model to use, prompt is the initial prompt text to send to the model, and length is the length of the generated text.

For example:

lua
Copy code
```
openai_stream("text-davinci-002", "Hello, world!", 50)
This will generate 50 characters of text using the specified OpenAI model, starting with the "Hello, world!" prompt.
```

Stage 2: MRCP integration
To use the MRCP integration, start a FreeSWITCH session and load the mrcp.lua script. Then, call the mrcp_asr() or mrcp_tts() function with the appropriate arguments:

lua
Copy code
```
mrcp_asr(engine, prompt, callback_url)
```

lua
Copy code

```
mrcp_tts(engine, text, callback_url)
```

where engine is the name of the MRCP engine to use, prompt or text are the speech or text input for the ASR or TTS operation respectively, and callback_url is the URL to which the MRCP server will send the recognition or synthesized audio data.

For example:

lua
Copy code
mrcp_asr("google", "Say something...", "http://myserver/callback")
This will perform an ASR operation using the Google MRCP engine, prompting the user to say something, and sending the recognition result to the specified callback URL.

Stage 3: ASR and TTS
To use the ASR and TTS functionality, start a FreeSWITCH session and load the asr.lua or tts.lua script. Then, call the asr() or tts() function with the appropriate arguments:

lua
Copy code
```
asr(engine, path, lang, grammar, callback_url)
```

lua
Copy code
```
tts(engine, text, path, lang, callback_url)
where engine is the name of the ASR or TTS engine to use, path is the path to the audio file to use for ASR, lang is the language code for the input or output text, grammar is the grammar file for the ASR engine, if applicable, and callback_url is the URL to which the recognition or synthesized audio data will be sent.
```

For example:

lua
Copy code
```
asr("google", "/path/to/audio.wav", "en-US", "/path/to/grammar.xml", "http://myserver/callback")
This will perform ASR on the specified audio file using the Google ASR engine, with the specified grammar file and language, and sending the recognition result to the specified callback URL.
```

License
freeswitch-chatGPT is released under the MIT License. See the LICENSE file for details.

Contributing
Contributions are welcome! Please see the CONTRIBUTING file for guidelines.

Contact
For questions or feedback, please contact me at 2637332218@qq.com

<p align="center">
  欢迎打赏-咨询
<img src="https://github.com/laoyin/java-sip-mrcp/blob/master/audio/200-zixun.jpg"  height="500" width="450">
</p>


