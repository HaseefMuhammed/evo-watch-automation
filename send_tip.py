import json
import os
import random
import requests

# 1. Load the tech messages
with open('lessons.json', 'r') as f:
    all_lessons = json.load(f)

# 2. Read execution history (to prevent duplicates)
history_file = 'history.json'
if os.path.exists(history_file):
    with open(history_file, 'r') as f:
        try:
            shown_titles = json.load(f)
        except json.JSONDecodeError:
            shown_titles = []
else:
    shown_titles = []

# 3. Filter out topics that were already displayed
available_lessons = [item for item in all_lessons if item['title'] not in shown_titles]

# 4. If everything has been shown, reset the cycle automatically
if not available_lessons:
    available_lessons = all_lessons
    shown_titles = []

# 5. Pick a random item from what's left
chosen = random.choice(available_lessons)

# 6. Save back to history tracker
shown_titles.append(chosen['title'])
with open(history_file, 'w') as f:
    json.dump(shown_titles, f)

# 7. Package and fire the Telegram alert
bot_token = os.environ['TELEGRAM_BOT_TOKEN']
chat_id = os.environ['TELEGRAM_CHAT_ID']

message_text = f"💡 *Topic: {chosen['topic']}*\n\n🔥 *{chosen['title']}*\n{chosen['message']}\n\n🔗 track the topics from : https://tinyurl.com/evo-tracker-wc\n\n- Evo AI"telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

payload = {
    "chat_id": chat_id,
    "text": message_text,
    "parse_mode": "Markdown"
}

response = requests.post(telegram_url, json=payload)
if response.status_code == 200:
    print(f"Success! Sent: {chosen['title']}")
else:
    print(f"Error sending message: {response.text}")
