from flask import Flask, render_template, request
import random

app = Flask(__name__)

characters = "abcdefghijklmnopqrstuvwxyz"
characters += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
characters += "1234567890"
characters += " !@#$%^&*()-_+=`~;:'[]{}|<>,./?"
characters += "\"\\"

character_count = len(characters)

def adjust_key_length(key, message):
    return (key * (len(message) // len(key)) + key[:len(message) % len(key)]) if key else ""

def encrypt_character(plain, key):
    key_code = characters.index(key)
    plain_code = characters.index(plain)
    cipher_code = (key_code + plain_code) % character_count
    cipher = characters[cipher_code]
    return cipher

def encrypt(plain, key):
    cipher = ""
    for (plain_index, plain_character) in enumerate(plain):
        key_index = plain_index % len(key)
        key_character = key[key_index]
        cipher_character = encrypt_character(plain_character, key_character)
        cipher += cipher_character
    return cipher

def invert_character(character):
    character_code = characters.index(character)
    inverted_code = (character_count - character_code) % character_count
    inverted_character = characters[inverted_code]
    return inverted_character

def invert(text):
    inverted_text = ""
    for character in text:
        inverted_text += invert_character(character)
    return inverted_text

def decrypt_character(cipher, key):
    key_code = characters.index(key)
    cipher_code = characters.index(cipher)
    plain_code = (cipher_code - key_code) % character_count
    plain = characters[plain_code]
    return plain

def decrypt(cipher, key):
    plain = ""
    for (cipher_index, cipher_character) in enumerate(cipher):
        key_index = cipher_index % len(key)
        key_character = key[key_index]
        plain_character = decrypt_character(cipher_character, key_character)
        plain += plain_character
    return plain

def random_key(length):
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    history = []
    key = ''  # Initialize key variable

    if request.method == 'POST':
        message = request.form['message']
        key = request.form['key']
        operation = request.form['operation']
        is_case_sensitive = 'case_sensitive' in request.form
        generate_random_key = request.form.get('generate_random_key') == 'true'

        if not is_case_sensitive:
            message = message.lower()
            key = key.lower()

        if generate_random_key:
            key_length = len(message)
            key = random_key(key_length)
        else:
            key = request.form['key']

        if operation == 'Encrypt':
            result = '!' + encrypt(message, key)
        else:
            if message.startswith('!'):
                message = message[1:]
            result = decrypt(message, key)

        history.append({'operation': operation, 'message': message, 'key': key, 'result': result})

    return render_template('index.html', result=result, key=key, history=history)

if __name__ == '__main__':
    app.run(debug=True)
