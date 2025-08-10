import json
import dataclasses

class Person:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.amount = 0

    def process_message(self, text):
        if isinstance(text, list):
            for a in text:
                self.process_message(a)
            return
        if isinstance(text, dict):
            return
        if 'xd' in text.lower():
            print(text)
            self.amount += 1

    def __eq__(self, other):
        if self.id == other.id and self.name != other.name:
            print(f"Warning, names dont match: {self.name} =/= {other.name}")
        return self.id == other.id

    def __lt__(self, other):
        return self.amount < other.amount
    def __gt__(self, other):
        return self.amount > other.amount

chatfile = "rawData/result.json"
ALLOWED_CHAT_TYPES = ['private_group', 'personal_chat', 'private_supergroup']
if __name__ == "__main__":
    f = open(chatfile, 'r')
    data = f.readlines()
    j = json.loads("".join(data))
    del j["about"]
    del j["stories"]

    people = []
    chats = j["chats"]["list"]
    for chat in chats:
        # Skip saved messages
        if chat['type'] not in ALLOWED_CHAT_TYPES:
            print(f"SKIPPING {chat} because it is {chat['type']}")
            continue
        print(f"Processing chat with {chat['name']}, type: {chat['type']}, id: {chat['id']}")
        for m in chat['messages']:
            # phone call skip
            if m['type'] != 'message':
                continue
            sender = Person(m['from'], m['from_id'])
            if sender not in people:
                people.append(sender)

            people[people.index(sender)].process_message(m['text'])
    people.sort(reverse=True)
    for p in people:
        if p.amount < 100: continue
        print(f"{p.name}: \t {p.amount}")