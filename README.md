# Bloomfilter
personal implementation of a bloomfilter


## How to use
Simple call to use the bloom filter:  
```$ python bloom.py```
Then filter is created with a default size of 16 and set to manual & insertion mode, meaning that everything that is typed in the command line will be added to the filter.
By typing ```$ !c <some_item>``` checking mode is activated and it checks whether <some_item> is in the filter.


```$ !q``` is used to quit
```$ !i``` toggles insertion mode
```$ !c``` toggles checking mode
```$ !p``` prints the current bloom filter
```$ !v``` activates verbose mode
