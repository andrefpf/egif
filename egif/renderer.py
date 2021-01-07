import matplotlib.pyplot as plt

def show_image(matrix):
    plt.imshow(matrix, vmin=0, vmax=255, cmap='gray')
    plt.show()

def compare_images(matrix_a, matrix_b):
    fig = plt.figure()

    ax = fig.add_subplot(1, 2, 1)
    imgplot = plt.imshow(matrix_a, vmin=0, vmax=255, cmap='gray')

    ax = fig.add_subplot(1, 2, 2)
    imgplot = plt.imshow(matrix_b, vmin=0, vmax=255, cmap='gray')

    plt.show()
