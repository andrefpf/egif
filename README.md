# EGIF - Esperto Graphics Interchange Format

EGIF is an image compression algorithm meant to be better than GIF. To be honest I just want to learn about image compression, 
but that is a good introduction.

Everybody knows that GIF is a very old and dumb format despite it's widespread use. 
The main problem is that GIF don't use intraframe compression, that should imply in huge files, 
but to solve this problems they only store 8 bits per pixel, resulting in very ugly images.

EGIF try to overcome this issue compressing the images with a Discrete Wavelet Transform (DWT) in 3 dimentions. And yes, I know that 
other format exists like WEBP, JPEG 2000, and maybe i could just implement another library making this work, but COMMON that is too boring,
I want to do it from scratch.

## How it works
- I will start assuming that you can load a matrix representing the frames. 
- The first step is to correct dimentions and break the animation into chunks.
- Then we change the colorspace to YCbCr, to separate luminance from croeminescence.
- After this we apply Discrete Wavelet Transform in 3 dimentions, and then remove all the small details.
- The resulting matrix should be full of zeros, so we can apply Run Length Encoding to compress these repetitions
- With the compressed values we can use a Huffman Code to compress it again. 
- After all the data is ready to receive a Header and be dumped into a file. 

## Problems
- The process is very slow, I intend to rewrite it in C.
- Depending on the data used it consumes all my computer RAM.
- Maybe it is possible to increase the compression ratio, but not sure exactly how.
- I should create a CODEC(?) to make it compatible with players in general, but i really don't know how it works.

## How to run it
- No idea, good luck.