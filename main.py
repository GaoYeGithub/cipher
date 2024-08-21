characters = "abcdefghijklmnopqrstuvwxyz"
characters += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
characters += "1234567890"
characters += " !@#$%^&*()-_+=`~;:'[]{}|<>,./?"
characters += "\"\\"

character_count = len(characters)

print("Supported Characters:\n" + characters + "\n")

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

    cipher_character = encrypt_character(key_character, plain_character)

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



while True:
  plaintext = input("Message: ")
  keytext = input("Password: ")

  encrypted = plaintext.startswith("!")

  if encrypted:
    plaintext = plaintext[1:]
    keytext = invert(keytext)

  ciphertext = encrypt(plaintext, keytext)

  if not encrypted:
    ciphertext = "!" + ciphertext

  print("Output: " + ciphertext)
  print()

  ciphertext = input("Encrypted Message")
  keytext = input("Password")

  if ciphertext.startswith("!"):
    ciphertext = ciphertext[1:]
    keytext = invert(keytext)

  plaintext = decrypt(ciphertext, keytext)
  print("Decrypted Message: " + plaintext)