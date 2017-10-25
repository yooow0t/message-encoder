import sys, string, base64

def alphabet_gen(key=""):
    lowercase = list(string.ascii_lowercase)
    uppercase = list(string.ascii_uppercase)

    if key:
        key = list(key)
        key.reverse()
        for char in key:
            if char in lowercase or char in uppercase:
                lowercase.insert(0, lowercase.pop(lowercase.index(char.lower())))
                uppercase.insert(0, uppercase.pop(uppercase.index(char.upper())))

    return lowercase, uppercase


def ceaser_encode(message, b=13, a=1, key=""):
    lowercase, uppercase = alphabet_gen(key)
    message = list(message)

    for num in range(len(message)):
        if message[num] in lowercase or message[num] in uppercase:
            letter = lowercase.index(message[num].lower())
            cipher = ((a * letter) + b) % 26 if a > 1 else letter + b
            if cipher > 25:
                cipher = cipher - 26
            if message[num] in lowercase:
                message[num] = lowercase[cipher]
            elif message[num] in uppercase:
                message[num] = uppercase[cipher] 
    return message
            
def ceaser_decode():
    pass


def vig_encode(message, cipher_key, alpha_key="", auto=False, grom=False):
    alphabet = alphabet_gen(alpha_key)[0]
    message = list(message)
    cipher_key = list(cipher_key)
    alpha_key = list(alpha_key)
    if auto:
        i = 0
        while len(cipher_key) < len(message):
            if i >= len(message):
                i = 0
            if message[i].lower() in alphabet:
                cipher_key.append(message[i].lower())
            i += 1

    else:
        i = 0
        while len(cipher_key) < len(message):
            cipher_key.append(cipher_key[i])
            i += 1    

    for char in range(len(message)):
        if message[char].lower() not in alphabet:
            cipher_key.insert(char, " ")
            cipher_key.pop()

    if grom:
        grom_dict = {x : string.ascii_lowercase[x] for x in range(10)}
        for i in range(len(cipher_key)):
            if cipher_key[i] != " ":
                cipher_key[i] = grom_dict[int(cipher_key[i])]
    
    tabula = {}
    shifted_alphabet = list(alphabet)
    for char in alphabet:
        tabula[char] = (list(shifted_alphabet))
        shifted_alphabet.append(shifted_alphabet.pop(0))


    for char in range(len(message)):
        upper = False
        if message[char].lower() in alphabet:
            if message[char].isupper():
                message[char] = message[char].lower()
                upper = True

            index = alphabet.index(message[char])
            message[char] = tabula[cipher_key[char]][index]

            if upper == True:
                message[char] = message[char].upper()

    return message

def vig_decode():
    pass

if __name__ == "__main__":
    help_message = """
    python message-encoder.py [file] [flag] [method] [other arguments]
    
    Flags
    -d -- decode message
    -e -- encode message
    -h -- help

    Methods
        NOTE    :  For more detailed information about each cipher
                   visit rumkin.com/tools/cipher
        -CEASAR FAMILY-
        ROT13   --
        c_shift -- (Ceasarian Shift) takes an int (n)
        affine  -- Takes two integers (a, b) 
        c_key   -- (Keyed Ceaser) takes a string (key) and an int (n)
        NOTE    :  This implementation of c_key is different to
                   rumkin.com. It inserts the key then performs the
                   shift
        -VIGENERE FAMILY-
        vig     -- (Vigenere Cipher) takes a string (cipher_key)
        vig_key -- (Keyed Vigenere) takes two strings (cipher_key, 
                   alpha_key)
        v_auto  -- (Autokey Vignere) takes two strings (cipher_key,
                   alpha_key)
        grons   -- (Gronsfeld Cipher) takes an int (cipher_key) and a
                   string (alpha_key)
        -ORPHANS-
        base64  --
    """
    
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            msg = f.read()
            flag = sys.argv[2]
            method = sys.argv[3]

            if flag == "-d":
                ceaser_decode()

            elif flag == "-e":
                if method == "ROT13":
                    print("".join(ceaser_encode(msg, 13)))

                elif method == "c_shift":
                    print("".join(ceaser_encode(msg, int(sys.argv[4]))))

                elif method == "affine":
                    print("".join(ceaser_encode(msg, int(sys.argv[5]), int(sys.argv[4]))))

                elif method == "c_key":
                    print("".join(ceaser_encode(msg, int(sys.argv[4]), 1, sys.argv[5])))

                elif method == "base64":
                    print(base64.b64encode(bytes(msg, "utf-8")).decode("ascii"))

                elif method == "vig":
                    print("".join(vig_encode(msg, sys.argv[4])))

                elif method == "vig_key":
                    print("".join(vig_encode(msg, sys.argv[4], sys.argv[5])))

                elif method == "v_auto":
                    print("".join(vig_encode(msg, sys.argv[4], sys.argv[5], True)))

                elif method == "grons":
                    print("".join(vig_encode(msg, sys.argv[4], sys.argv[5], False, True)))

            else:
                print(help_message)

    else:
        print(help_message)
