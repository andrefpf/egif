def run_length_encode(array):
    # code to remove repetitions of the number 0
    repeted = 0
    encoded = []

    for i in array:
        if i == 0:
            repeted += 1
        elif repeted:
            encoded.append(0)
            encoded.append(repeted)
            encoded.append(i)
            repeted = 0
        else:
            encoded.append(i)

    if repeted:
        encoded.append(0)
        encoded.append(repeted)
    return encoded

def run_length_decode(array):
    last_was_zero = False
    decoded = []

    for i in array:
        if i == 0:
            last_was_zero = True
        elif last_was_zero:
            decoded.extend([0] * i)
            last_was_zero = False
        else:
            decoded.append(i)
    return decoded
