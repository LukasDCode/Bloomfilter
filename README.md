# Bloom Filter
Personal implementation of a bloom filter.


## Install
The python packages for the hash functions have to be installed manually.  


## How to Use
Simple call to run the bloom filter:  
```$ python bloom.py```  
Then filter is created with a default size of 16 and set to manual & insertion mode, meaning that everything that is typed in the command line will be added to the filter.  

### Manual Mode
```$ !c <some_item>``` activates checking mode and it checks whether ```<some_item>``` is in the filter. Everything entered in the command line from now on is checked against the content of the filter and not added to it. In order to add more items to the filter insertion mode has to be switched back on again with the following command: ```$ !i```  


This is an exhaustive list of all possible commands:  

- ```$ !q``` quit the running execution  
- ```$ !i``` toggles insertion mode  
- ```$ !c``` toggles checking mode  
- ```$ !p``` prints the current bloom filter  
- ```$ !v``` activates verbose mode  

The commands can be used with an additional item (like seen above) separated by space. For example switching back to insertion mode and directly insert some new item: ```$ !i <some_item>```  


### More Advanced Usages
The code gives options for 4 additional arguments while initiating the bloom filter.  
```$ python bloom.py --size <int> --num_func <int> --crypto --auto```  
  
- ```--size <int>``` allows to specify the exponent to the base of 2 to create the bloom filter. (Example: size = 6 --> total size 2^6 = 64). This is a design choice, because the exponent is also used internally.  
- ```--num_func <int>``` allows to specify the number of hash functions that should be used for insertion & checking of items (max of 5 and min of 1).  
- ```--crypto``` activates a toggle to use cryptographic hash functions instead of non-cryptographic ones.  
- ```--auto``` runs the script in an automatic mode. it inserts and checks for values automatically to compare different hash functions against each other.  



## Hash Functions
5 hash functions were used for both the cryptographic and the non-crpytographic mode. More hash functions can be used, they just have to be inserted into the ```switch``` and the ```verbose_switch``` of the bloom filter class, as well as their respective functions added at the bottom of the class.

### Cryptographic Hash Functions
- MD5
- BLAKE2S
- SHA256
- SHA512
- SHA3-256

Information about them can be found [here](https://cryptobook.nakov.com/cryptographic-hash-functions/secure-hash-algorithms).

### Non-Cryptographic Hash Functions
- Murmur
- FNV
- Jenkins
- Pearson
- Hex-value

Information about them can be found [here](https://en.wikipedia.org/wiki/Category:Hash_function_(non-cryptographic))