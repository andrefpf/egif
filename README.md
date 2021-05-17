# EGIF - Esperto Graphics Interchange Format

EGIF is a compressed image format meant to be better than GIF. To be honest I just want to learn about image compression, 
but that is a good introduction.

Everybody knows that GIF is a very old and dumb format despite it's widespread use. 
The main problem is that GIF don't use intraframe compression, that should imply in huge files, 
but to solve this problems they only store 8 bits per pixel, resulting in very ugly images.

EGIF try to overcome this issue compressing the images with a Discrete Cossine Transform (DCT) in 3 dimentions.

## How it works
- First the images are loaded using the default Python Imaging Library (PIL) and a numpy 3D matrix is created. 
- The 3d matrix is divided in 3d chunks of 8x8x8 matrix (or any other size if needed).
- For every chunk we apply a DCT in every array in every dimention and quantize it.
- The remaining matrix should be full of zeros, so we go through it and apply a Run Lenght Encoding to compress these repetitions.
- When it's done you can write it into a file.

## Problems
- The process is very slow, i intend to rewrite it in c++.
- I also need to test how to go though the image to optimize the compression (maybe zig-zag? wtf is a zig-zag in 3 dimentions? No idea).
- Some parts are a little bit messy yet.
- I should create a CODEC(?) to make it compatible with players in general, but i really don't know how it works.

## How to run it
- In the project folder run `python egif path/to/file.egif` and wait... because it is very slow.
- There are some egif files in the `examples/converted folder`.
