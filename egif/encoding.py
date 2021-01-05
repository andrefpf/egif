def encode(array):
    counter = 0
    encoded = []

    for n in array:
        if not 0 <= n <= 255:
            print(n)
            raise ValueError('Values should be between 0 and 255')

        if n == 0:
            counter += 1
        elif counter:
            while counter > 0:
                encoded.append(0)
                cu = 255 if counter >= 255 else counter
                encoded.append(cu)
                counter -= cu
            encoded.append(n)
        else:
            encoded.append(n)
    
    while counter > 0:
        encoded.append(0)
        cu = 255 if counter >= 255 else counter
        encoded.append(cu)
        counter -= cu

    return bytes(encoded)

def decode(array):
    marker = False
    decoded = []

    cu = []

    for n in array:
        if n == 0:
            marker = True
        elif marker:
            decoded.extend([0] * n)
            cu.append(n)
            marker = False
        else:
            decoded.append(n)

    print('Decode')
    print(len(cu))
    print(min(cu))
    print(max(cu))
    print(sum(cu) / len(cu))

    return decoded


# import numpy as np 

# for i in range(1, 100):
#     array = np.random.randint(0,255, size=i) * np.random.randint(0,2,size=i)
#     a = encode(array)
#     b = decode(a)
#     assert np.alltrue(array == b)
#     print('all right')
