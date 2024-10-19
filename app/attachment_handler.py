import os

SAVE_PATH = './attachments/'

def save_attachment(part, filename):
    os.makedirs(SAVE_PATH, exist_ok=True)
    filepath = os.path.join(SAVE_PATH, filename)
    with open(filepath, 'wb') as f:
        f.write(part.get_payload(decode=True))
    print(f'Saved: {filepath}')