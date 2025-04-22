from openai import OpenAI

client = OpenAI(
    base_url="https://ai.gitee.com/v1",
    api_key="XWKOBFEFOYJYDXAIONEQBBHLX5TTEEUIN70JTZA6", )


def get_llm(s):
    messages = [
        {'role': 'system', 'content': s},

    ]

    response = client.chat.completions.create(
        model="DeepSeek-R1",
        # model="Qwen/QwQ-32B",
        # model="Qwen2.5-Coder-32B-Instruct",
        # model="deepseek-chat",
        messages=messages,
        # tools=tools,
        # tool_choice="auto",
        # response_format={"type": "json_object"}
    )
    try:
        content = response.choices[0].message.content
    except Exception as e:
        print(e)
        content = ""
    return content
