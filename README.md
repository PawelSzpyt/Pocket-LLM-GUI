# Pocket-LLM-GUI
Small, unofficial companion app for OpenWebUI

Inspired by OpenAI ChatGPT app for MacOS, I decided it would be useful to have something similar for my local LLM. It is a handy idea to get a small input box with a keyboard shortcut - no matter what window is focused - and to send the request to your local LLM.
Integrating it to OpenWebUI is not straightforward and I was not sure if it would be accepted and how useful other people would find it, so I just hacked my way through it.

## HOW TO USE
1. Download pocket_llm_gui.py from this repo
2. Open "Shortcuts" app, click "+", click "Apps", click "Terminal", double click "Run shell script"
3. Write the command with correct paths to python and pocket_llm_gui.py, for example:
```/opt/homebrew/anaconda3/envs/ai/bin/python '/Users/ai/pocket_llm_gui.py'```
4. Click on "i" icon, and in "Run with:" choose desired shortcut, alt+space is great if you don't use ChatGPT's app.
5. You can exit "Shortcuts" app
6. Now you can invoke this script with your desired keyboard shortcut
7. Small GUI shows up. You can adjust port (of your running OpenWebUI) and delay (too small delay will prevent the page from fully loading and you'll loose your prompt)
8. For new lines press shift + enter
9. You can send the request by pressing "enter" or by clicking "Send" button
10. After sending, browser will pop up with localhost:port, and after the delay your text will be pasted (hopefully into the focused input box). Then app closes and you can continue your chat in OpenWebUI.
