from openai import OpenAI
import json
import time

print("Script started. Connecting to Ollama...")

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

emails = [
    "I want to check my current savings balance. Account ending 3344.",
    "Why is there a $12.50 monthly fee? This is ridiculous! Account 1122.",
    "I need a loan for a new car, about $25,000. Can you call me back?"
]

system_prompt = """Classify intent as fraud_dispute, loan_inquiry, balance_check, or complaint. 
Extract account_last_four and amount_usd. Output valid JSON only. No extra text."""

print("Sending first request... This may take 30 seconds if the model is cold.")
start_time = time.time()

for i, email in enumerate(emails):
    print(f"Processing email {i+1}...")
    try:
        response = client.chat.completions.create(
            model="deepseek-r1:7b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Email: {email}"}
            ],
            temperature=0.1,
            timeout=120  # Wait up to 2 minutes
        )
        raw = response.choices[0].message.content
        print(f"Raw response: {raw[:100]}...")  # Print first 100 chars
        try:
            clean = raw[raw.find("{"):raw.rfind("}")+1]
            data = json.loads(clean)
            print(f"Email {i+1}: {data}")
        except:
            print(f"Email {i+1}: Failed to parse - {raw}")
    except Exception as e:
        print(f"Error on email {i+1}: {e}")

print(f"Total time: {time.time() - start_time:.2f} seconds")