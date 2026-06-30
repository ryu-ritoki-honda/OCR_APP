from openai import AzureOpenAI


class AnswerService:

    def __init__(
        self,
        endpoint,
        api_key,
        api_version,
        deployment
    ):

        self.client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version=api_version
        )

        self.deployment = deployment

    def answer(
        self,
        question,
        chunks
    ):

        context = "\n\n".join(
            chunk.text
            for chunk in chunks
        )

        prompt = f"""
You are a helpful assistant.

Answer ONLY using the provided context.

If the answer is not contained in the context,
say you cannot find the answer.

Context
-------
{context}

Question
--------
{question}

Answer:
"""

        response = self.client.chat.completions.create(

            model=self.deployment,

            messages=[

                {
                    "role": "system",
                    "content":
                    "You answer questions about uploaded documents."
                },

                {
                    "role": "user",
                    "content": prompt
                }

            ],

            temperature=0

        )

        return response.choices[0].message.content