import openai


def openai_engine(prompt):
    openai.api_key = "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"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=1,
        max_tokens=2000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0)
    answer = response["choices"][0].text
    print(answer)


prompt = input("Enter a question: ")

openai_engine(prompt)
