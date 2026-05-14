user_input = input("You: ").lower()

if "sad" in user_input:
    print("Bot: I'm here for you. You're not alone.")
elif "happy" in user_input:
    print("Bot: That's great to hear!")
else:
    print("Bot: Tell me more.")
import google.generativeai as genai

genai.configure(api_key="YOUR_KEY")

model = genai.GenerativeModel("gemini-1.5-flash")

response = model.generate_content("I feel stressed")
print(response.text)    