import string
import math
import random

# Create dictionary
def create_cipher_dict(cipher):
    cipher_dict = {}
    alphabet_list = list(alphabet)
    for i in range(len(cipher)):
        cipher_dict[alphabet_list[i]] = cipher[i]
    return cipher_dict

# Apply encryption key or decryption key on text
def apply_cipher_on_text(text, cipher):
    cipher_dict = create_cipher_dict(cipher)
    text = list(text)
    newtext = ""
    for elem in text:
        if elem.upper() in cipher_dict:
            newtext += cipher_dict[elem.upper()]
        else:
            newtext += " "
    return newtext

# Count the number of bi-gram in the reference text
def create_scoring_params_dict(longtext_path):
    scoring_params = {}
    alphabet_list = list(alphabet)
    with open(longtext_path, 'rb') as fp:
        for line in fp:
            data = list(line.strip().upper())
            for i in range(len(data) - 1):
                alpha_i = data[i]
                alpha_j = data[i + 1]
                if alpha_i not in alphabet_list and alpha_i != " ":
                    alpha_i = " "
                if alpha_j not in alphabet_list and alpha_j != " ":
                    alpha_j = " "
                key = alpha_i + alpha_j
                if key in scoring_params:
                    scoring_params[key] += 1
                else:
                    scoring_params[key] = 1
    return scoring_params

# Count the number of bi-gram in the cipher text
def score_params_on_cipher(text):
    scoring_params = {}
    alphabet_list = list(alphabet)
    data = list(text.strip())
    for i in range(len(data) - 1):
        alpha_i = data[i].upper()
        alpha_j = data[i + 1].upper()
        if alpha_i not in alphabet_list and alpha_i != " ":
            alpha_i = " "
        if alpha_j not in alphabet_list and alpha_j != " ":
            alpha_j = " "
        key = alpha_i + alpha_j
        if key in scoring_params:
            scoring_params[key] += 1
        else:
            scoring_params[key] = 1
    return scoring_params

# Compute the score function
def get_cipher_score(text, cipher, scoring_params):
    decrypted_text = apply_cipher_on_text(text,cipher)
    scored_f = score_params_on_cipher(decrypted_text)
    cipher_score = 0
    for k,v in scored_f.items():
        if k in scoring_params:
            cipher_score += v * math.log(scoring_params[k])
    return cipher_score

# Swap moves
def generate_cipher(cipher):
    pos1 = random.randint(0, len(list(cipher)) - 1)
    pos2 = random.randint(0, len(list(cipher)) - 1)
    if pos1 == pos2:
        return generate_cipher(cipher)
    else:
        cipher = list(cipher)
        pos1_alpha = cipher[pos1]
        pos2_alpha = cipher[pos2]
        cipher[pos1] = pos2_alpha
        cipher[pos2] = pos1_alpha
        return "".join(cipher)

# Random coin
def random_coin(p):
    unif = random.uniform(0, 1)
    if unif >= p:
        return False
    else:
        return True

# MCMC algorithm
def MCMC_decrypt(n_iter, cipher_text, scoring_params):
    p = 0.15
    current_cipher = alphabet
    state_keeper = set()
    best_state = ''
    score = 0
    for i in range(n_iter):
        state_keeper.add(current_cipher)
        proposed_cipher = generate_cipher(current_cipher)
        score_current_cipher = get_cipher_score(cipher_text, current_cipher, scoring_params)
        score_proposed_cipher = get_cipher_score(cipher_text, proposed_cipher, scoring_params)
        acceptance_probability = min(1, math.exp(p * (score_proposed_cipher - score_current_cipher)))
        if score_current_cipher > score:
            best_state = current_cipher
            score = score_current_cipher
        if random_coin(acceptance_probability):
            current_cipher = proposed_cipher
        if i % 500 == 0:
            print("iter", i, ":", apply_cipher_on_text(cipher_text, current_cipher)[0:99])
    return state_keeper, best_state

alphabet = string.ascii_uppercase
# Main algorithm
# Reference Text: War and Peace
scoring_params = create_scoring_params_dict('war_and_peace.txt')
# Test Text
plain_text = "As Oliver gave this first proof of the free and proper action of his lungs, \
the patchwork coverlet which was carelessly flung over the iron bedstead, rustled; \
the pale face of a young woman was raised feebly from the pillow; and a faint voice imperfectly \
articulated the words, Let me see the child, and die. \
The surgeon had been sitting with his face turned towards the fire: giving the palms of his hands a warm \
and a rub alternately. As the young woman spoke, he rose, and advancing to the bed's head, said, with more kindness \
than might have been expected of him: "

encryption_key = "XEBPROHYAUFTIDSJLKZMWVNGQC"
cipher_text = apply_cipher_on_text(plain_text,encryption_key)
decryption_key = "ICZNBKXGMPRQTWFDYEOLJVUAHS"

print("Text To Decode:", cipher_text)
print("\n")
states, best_state = MCMC_decrypt(10000, cipher_text, scoring_params)
print("\n")
print("Decoded Text:", apply_cipher_on_text(cipher_text, best_state))
print("\n")
print("MCMC KEY FOUND:", best_state)
print("DECRYPTION KEY:", decryption_key)