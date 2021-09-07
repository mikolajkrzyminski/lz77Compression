# LZ77 compression algorithm

LZ77 is lossless data compression algorithm. 

inputFilePath const is a relative path to file to compress (input of algorithm).
I created a set of examples to compress in "input" directory.
Algorithm works the best for repeating patterns close to each other (white.bmp, wolf.bmp).
On the other hand it doesn't work with noises (noise.bmp).
For Huffman algorithm I used dahuffman library.

## output of algorithm

.lz77 is a compressed file. File with (lz77) prefix is a file recovered from compressed one.

![img1](https://github.com/mikolajkrzyminski/lz77Compression/blob/master/img/lz77Output.png?raw=true)

## console output 

![img2](https://github.com/mikolajkrzyminski/lz77Compression/blob/master/img/lz77Console.png?raw=true)

First two lines are binary comparison of received files with original one.
Next lines are level of compression for pure huffman, lz77 + huffman and lz77 calculated from formula in brackets.





