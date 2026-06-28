from openai import OpenAI

client = OpenAI()

def summarize_notes(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a study assistant. Turn messy lecture notes into clear, structured bullet-point summaries. Keep it simple and easy to understand for students."
            },
            {
                "role": "user",
                "content": text
            }
        ]
    )

    return response.choices[0].message.content


def main():
    print("\n=== STUDY SUMMARIZER AI ===\n")
    print("Paste your notes below:\n")

    user_input = input()

    result = summarize_notes(user_input)

    print("\n=== SUMMARY ===\n")
    print(result)


main()