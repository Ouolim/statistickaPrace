import csv
import json
import re
from dataclasses import dataclass

class Person:
    def __init__(self, name, id):
        self.name = name
        self.id = id

    def __eq__(self, other):
        if self.id == other.id and self.name != other.name:
            print(f"Warning, names dont match: {self.name} =/= {other.name}")
        return self.id == other.id

    def __str__(self):
        return self.name


def preprocess_message_to_str(message):
    if isinstance(message, str):
        return message
    if isinstance(message, list):
        return "".join(map(preprocess_message_to_str, message))
    if isinstance(message, dict):
        return message["text"]
def extract_longest_xd(message):
    matches = re.findall(r'xd+', message, re.IGNORECASE)
    if not matches:
        return None
    # return the longest match
    return max(matches, key=len)


@dataclass
class Message:
    message_id: str
    user_id: str
    timestamp: str
    chat_type: int
    Damount: int

def message_from_chat(message: dict , chat_type: int) -> Message:
    amount = extract_longest_xd(message["text"])
    return Message(message["id"], message["from_id"], message["date"],chat_type ,len(amount)-1 if amount is not None else 0)


chatfile = "data/data.json"
ALLOWED_CHAT_TYPES = {'private_group':0, 'personal_chat':1, 'private_supergroup':0}
if __name__ == "__main__":
    f = open(chatfile, 'r')
    data = f.readlines()
    j = json.loads("".join(data))
    messages = []


    del j["about"]
    del j["stories"]

    people = []
    chats = j["chats"]["list"]
    chat_mode = None
    for chat in chats:
        # Skip saved messages
        if chat['type'] not in ALLOWED_CHAT_TYPES.keys(): continue
        chat_mode = ALLOWED_CHAT_TYPES[chat['type']]
        print(f"Processing chat with {chat['name']}, type: {chat['type']}, id: {chat['id']}")
        for m in chat['messages']:
            # phone call skip
            if m['type'] != 'message':
                continue
            sender = Person(m['from'], m['from_id'])
            if sender not in people:
                people.append(sender)
            m["text"] = preprocess_message_to_str(m["text"])
            message_obj = message_from_chat(m, chat_mode)

            if message_obj.Damount == 0: continue
            messages.append(message_obj)

    # Write messages to CSV
    with open("data/messages.csv", "w", newline="") as f:
        writer = csv.writer(f)
        # header
        writer.writerow(["message_id", "user_id", "timestamp","chat type 0=group, 1=DM", "Damount"])
        # rows
        for msg in messages:
            writer.writerow([msg.message_id, msg.user_id, msg.timestamp,msg.chat_type, msg.Damount])

    # Write users to CSV
    with open("data/users.csv", "w", newline="") as f:
        writer = csv.writer(f)
        # header
        writer.writerow(["user_id", "name"])
        # rows
        for person in people:
            writer.writerow([person.id, person.name])