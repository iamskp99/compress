# compress

A file compression tool based on run-length encoding and Huffman encoding.

## Usage
```
Run the main.py file.

The program will prompt you to give an input.
Enter 0 if you want to compress or 1 if you want to de-compress.

If you want to compress :

Enter the input.txt file and output.bin file.
input.txt which you will input, contains the data which
you want to compress and output.bin file will contain
the data in compressed form.

If you want to de-compress :

Enter the decode.txt file and output.bin file.
decode.txt is the de-compressed file.
```

## How it works ?
```
Encoding :

The program reads the input.txt file and then it performs
RLE on it.

Now, how we will determine if some character in the RLE encoded string
should be treated as an integer or the frequency of a character. 

We will add 152 to the ASCII values to deal with the integers.
This means that frequency will be treated as normal int character and
the integer will have different characters which have higher ASCII
value.This will help us to deal with confusion with integer as a character and
integer as frequency.

After this,the program performs huffman coding. Now,a hash map is made having 
key as huffman code and character as its value.After,that we encode the code we 
got after performing RLE to huffman encoded string. Now, it adds extra zeroes
to make the length of the string a multiple of 8. The program now converts the
hash map into an encoded string which has a length,multiple of 8 and appends
it to the huffman encoded string.

So,now the data is encoded in the following format :

[zeroes added to the last to make the huffman code multiple of 8][length of the table]
Now, the data is stored in this format.

This is the table (This is our hash map):

[zeroes before the code][Length of the bytes to read][Actual huffman code][Actual ASCII code]
"Zeroes before the code" is the amount of zeroes added before actual huffman code.

Now,we add this binary string to our huffman encoded string.
After that, we write it to the output.bin file.

Decoding :

First of all the program decodes the hash map.
It reads the amount of zeroes added before huffman code to convert it into a code of length
which is a multiple of 8.It now reads the number of bytes the huffman code has.After that it reads
the actual huffman code.It removes the zero added before from it and then it reads the actual ascii code.
It converts it into the character and saves it in the hash map.

Now after getting the hashmap,it reads the actual huffman coded text,removes the extra zeroes and 
convert it into the actual decoded text.

It now writes it to the decoded.txt.

```
# Sources

What is Huffman coding ? : [https://www.youtube.com/watch?v=co4_ahEDCho](https://www.youtube.com/watch?v=co4_ahEDCho)

A good video on file compression : [https://www.youtube.com/watch?v=IuFKDrdmgIQ&list=LL&index=8&t=254s](https://www.youtube.com/watch?v=IuFKDrdmgIQ&list=LL&index=8&t=254s) 

You can also read this pdf : [https://www.researchgate.net/publication/309616501_Role_of_Run_Length_Encoding_on_Increasing_Huffman_Effect_in_Text_Compression](https://www.researchgate.net/publication/309616501_Role_of_Run_Length_Encoding_on_Increasing_Huffman_Effect_in_Text_Compression)
