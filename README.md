# Bloom Filter
Personal implementation of a bloom filter. The normal script is the ```bloom.py``` file.  
  
I would like to direct some attention to the ```nanobloom.py``` file, which provides the basic bloom filter functionality, but in a highly compressed version.
[Read more about Nanobloom at the bottom of this page.](##Nanobloom.py) 


## Install
The following python packages for the non-cryptographic hash functions have to be installed manually:  
```
pip install mmh3 fnvhash jenkins-cffi pearhash tqdm
```
The ```tqdm``` package is used to display a nice loading bar while doing the automatic runs.

## How to Use
Simple call to run the bloom filter:  
```
python bloom.py
```  
Then filter is created with all default parameters.  
Size of 16 (= 2^4), set to manual & insertion mode, meaning that everything that is typed in the command line will be added to the filter, and with the use of non-cryptographic hash functions.

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
  
- ```--size <int>``` or ```-s <int>``` allows to specify the exponent to the base of 2 to create the bloom filter. (Example: size = 6 --> total size 2^6 = 64). This is a design choice, because the exponent is also used internally.  
- ```--num_func <int>``` or ```-n <int>``` allows to specify the number of hash functions that should be used for insertion & checking of items (max of 5 and min of 1).  
- ```--crypto``` or ```-c``` activates a toggle to use cryptographic hash functions instead of non-cryptographic ones.  
- ```--auto``` or ```-a``` runs the script in an automatic mode. it inserts and checks for values automatically to compare different hash functions against each other.  



## Hash Functions
5 hash functions were used for both the cryptographic and the non-crpytographic mode. More hash functions can be used, they just have to be inserted into the ```switch``` and the ```verbose_switch``` of the bloom filter class, as well as their respective functions added at the bottom of the class.  

When the amount of hash functions is specified with the ```--num_func``` argument, the hash functions get chosen from the top down. 

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

Information about them can be found [here](https://en.wikipedia.org/wiki/Category:Hash_function_(non-cryptographic)).


## Minibloom.py
The ```minibloom.py``` file is a personal implementation to try out a middle ground of compressing the file, but still keeping the majority of the functionality. Arguments, verbose-mode and printing are completely disregarded. The file consists of 83 lines of code including 3 lines of imports.

## Nanobloom.py
The ```nanobloom.py``` file is a personal implementation to try out the maximal way of compressing the file and only keeping the manual mode. The automatic mode is completely removed, like the argument parser and printing options. Prints are kept to a minimum. The entire file consists of 45 lines of code, where 2 lines are used for imports, 11 lines are for the bloom filter class, 2 lines for the main method and the remaining 30 lines are solely for the manual mode, where user input is validated and prints generated.  
All the magic happens in the ```bloom_filter``` class:

https://github.com/LukasDCode/Bloomfilter/blob/30fd0c7e13009c36b808e875ae619701ce29485e/nanobloom.py#L4-L16

