import gpt4all
 
gptj = gpt4all.GPT4All("ggml-gpt4all-j-v1.3-groovy")

messages = [{"role": "user", "content": "Give me a list of 10 colors and their RGB code"}]
ret = gptj.chat_completion(messages)
print(ret)