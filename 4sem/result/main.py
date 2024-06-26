# -*- coding: utf-8 -*-
"""PAVI - Laba4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18KoyI5d-92yr5bskUqTSnah0_QM-oUqG
"""



import numpy as np
from PIL import Image


def convert_to_gray(image):
    img_array = np.array(image)
    height, width, channels = img_array.shape
    gray_array = np.zeros((height, width), dtype=np.uint8)

    for i in range(height):
        for j in range(width):
            if channels == 4:
                r, g, b, _ = img_array[i, j]
            else:
                r, g, b = img_array[i, j]

            brightness = int(0.2989 * r + 0.5870 * g + 0.1140 * b)

            gray_array[i, j] = brightness

    gray_image = Image.fromarray(gray_array)

    return gray_image


def convolution(image, kernel):
    kernel_height, kernel_width = kernel.shape
    image_height, image_width = image.shape

    result = np.zeros_like(image)

    # свертка
    for i in range(image_height):
        for j in range(image_width):

            window = image[i:i+kernel_height, j:j+kernel_width]

            row_result = np.convolve(window.flatten(), kernel.flatten(), mode='same')

            result[i, j] = row_result[kernel_height * kernel_width // 2]

    return result


def pruitt_operator(image):
    # полутон
    gray_image = convert_to_gray(image)

    gray_array = np.array(gray_image)

    # Прюитт
    kernel_x = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
    kernel_y = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])

    # Gx и Gy
    gradient_x = convolution(gray_array, kernel_x)
    gradient_y = convolution(gray_array, kernel_y)

    gradient = np.abs(gradient_x) + np.abs(gradient_y)

    # Нормализация
    normalized_gradient_x = (gradient_x / np.max(gradient_x)) * 255
    normalized_gradient_y = (gradient_y / np.max(gradient_y)) * 255
    normalized_gradient = (gradient / np.max(gradient)) * 255


    threshold = 128
    binary_gradient = (normalized_gradient > threshold) * 255

    return gray_image, normalized_gradient_x, normalized_gradient_y, normalized_gradient, binary_gradient


def binarize(gradient, threshold):
    binary_gradient = (gradient > threshold) * 255
    return binary_gradient


def main(smth=None):
    image = Image.open('japan.png')

    gray_image, gradient_x, gradient_y, gradient, binary_gradient = pruitt_operator(image)

    gray_image.save('japan_gray_image.png')
    Image.fromarray(gradient_x.astype(np.uint8)).save('japan_gradient_x.png')
    Image.fromarray(gradient_y.astype(np.uint8)).save('japan_gradient_y.png')
    Image.fromarray(gradient.astype(np.uint8)).save('japan_gradient.png')
    Image.fromarray(binary_gradient.astype(np.uint8)).save('japan_binary_gradient.png')

    binary_gradient_100 = binarize(gradient, 100)
    Image.fromarray(binary_gradient_100.astype(np.uint8)).save('japan_binary_gradient_100.png')

    binary_gradient_80 = binarize(gradient, 80)
    Image.fromarray(binary_gradient_80.astype(np.uint8)).save('japan_binary_gradient_80.png')


    image = Image.open('kvant.png')

    gray_image, gradient_x, gradient_y, gradient, binary_gradient = pruitt_operator(image)

    gray_image.save('kvant_gray_image.png')
    Image.fromarray(gradient_x.astype(np.uint8)).save('kvant_gradient_x.png')
    Image.fromarray(gradient_y.astype(np.uint8)).save('kvant_gradient_y.png')
    Image.fromarray(gradient.astype(np.uint8)).save('kvant_gradient.png')
    Image.fromarray(binary_gradient.astype(np.uint8)).save('kvant_binary_gradient.png')


if __name__ == "__main__":
    main()

