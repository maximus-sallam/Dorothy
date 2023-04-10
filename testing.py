import openai


def openai_engine(prompt):
    openai.api_key = "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"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt)
    answer = response["choices"][0].text
    return answer

prompt = ""

while True:
    print(openai_engine(prompt))
