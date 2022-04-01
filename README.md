# Bloomfilter
personal implementation of a bloomfilter


## How to use
Simple call to use the bloom filter:  
```$ python bloom.py```  
Then filter is created with a default size of 16 and set to manual & insertion mode, meaning that everything that is typed in the command line will be added to the filter.  
```$ !c <some_item>``` activates checking mode and it checks whether ```<some_item>``` is in the filter. Everything entered in the command line from now on is checked against the content of the filter and not added to it. In order to add more items to the filter insertion mode has to be switched back on again with the following command: ```!i```  


- ```$ !q``` is used to quit  
- ```$ !i``` toggles insertion mode  
- ```$ !c``` toggles checking mode  
- ```$ !p``` prints the current bloom filter  
- ```$ !v``` activates verbose mode  



