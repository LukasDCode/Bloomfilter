import time
import random
import hashlib
import argparse
from bitarray import bitarray
from tqdm import tqdm

# currently only 5 hash functions implemented for both cryptographic and non-cryptographic hashes
max_num_hash_functions = 5 


class bloom_filter:


    def __init__(self, array_size_exponent=4, num_hash_functions=3, is_cryptographic=False):
        self.filter_array = bitarray([0] * 2**array_size_exponent)
        self.array_size_exponent = array_size_exponent
        self.num_hash_functions = num_hash_functions

        self.hash_func_switch = {
            0: self.get_md5,
            1: self.get_blake2s,
            2: self.get_sha256,
            3: self.get_sha512,
            4: self.get_sha3_256
        }
        self.hash_name_switch = {
            0: "MD5     ",
            1: "BLAKE2s ",
            2: "SHA256  ",
            3: "SHA512  ",
            4: "SHA3-256"
        }    

    def print_filter(self):
        print(self.filter_array, "size:", 2**self.array_size_exponent)

    def insert(self, item):
        for hash_f_index in range(self.num_hash_functions):
            cell_position = self.hash_func_switch[hash_f_index](item)
            self.filter_array[cell_position] = 1

    def check(self, item):
        for hash_f_index in range(self.num_hash_functions):
            cell_position = self.hash_func_switch[hash_f_index](item)
            if not self.filter_array[cell_position]: return False
        return True

    def get_md5(self, input):
        md5_hash = hashlib.md5(input.encode("utf-8")).hexdigest()
        return self.position_from_hex(md5_hash)

    def get_blake2s(self, input):
        blake2s_hash = hashlib.blake2s(input.encode("utf-8")).hexdigest()
        return self.position_from_hex(blake2s_hash)

    def get_sha256(self, input):
        sha256_hash = hashlib.sha256(input.encode("utf-8")).hexdigest()
        return self.position_from_hex(sha256_hash)

    def get_sha512(self, input):
        sha512_hash = hashlib.sha512(input.encode("utf-8")).hexdigest()
        return self.position_from_hex(sha512_hash)

    def get_sha3_256(self, input):
        sha3_256_hash = hashlib.sha3_256(input.encode("utf-8")).hexdigest()
        return self.position_from_hex(sha3_256_hash)
    
    """ return cell positons for the filter """
    def position_from_hex(self, hex):
        return int(hex, 16)%(2**self.array_size_exponent)

    def position_from_int(self, number):
        return number%(2**self.array_size_exponent)


def manual_mode(bf):
    is_insert_mode = True
    print("setup bloom filter of size", str(2**bf.array_size_exponent))
    print("'!q' to quit, '!i' to toggle insertion mode, '!c' to toggle check mode")
    print("!p to print the current filter array, !v to toggle verbose mode")
    print("insertion mode activated")
    while(True):
        user_input = input().lstrip() # lstrip removes leading spaces & tabs
        if user_input == "":
            print("no useful input detected, try again")
            continue
        
        if user_input[0] == "!":
            try:
                if user_input[1].lower() == "i": # insert
                    is_insert_mode = True
                    print("insertion mode activated")
                elif user_input[1].lower() == "c": # check
                    is_insert_mode = False
                    print("check mode activated")
                elif user_input[1].lower() == "p": # print
                    bf.print_filter()
                elif user_input[1].lower() == "q": # quit
                    break
                else:
                    print("unknown symbol after '!' - no action executed")
                    continue
            except IndexError:
                print("letter after '!' expected - no action executed")
                continue

            try: # tries switching modes and applying new item
                item = user_input.split()[1]
            except IndexError:
                continue # only switching modes, without inserting or checking
        else:
            item = user_input.split()[0]
        
        if item:
            if is_insert_mode:
                bf.insert(item)
            else:
                if bf.check(item): print(item, "is probably in the set")
                else: print(item, "is definitely not in the set")
        else: print("no useful input detected")


def get_x_random_elements_from_list(original_list, num_elements):
    num_elements = min(len(original_list), max(1, num_elements))
    to_keep = set(random.sample(range(len(original_list)), num_elements))
    return [x for i,x in enumerate(original_list) if i in to_keep]


def automatic_mode(args):
    """
    Automatic modes creates 100 bloom filter of size 2^16,
    fills each of them with 2500 items and checks each of them for another 2000 items.
    From the 2000 items it checks it will use 1000 of which have been inserted before
    and another 1000 which the filter has not seen before.
    This is done to also check for interdependencies between the hash functions.
    """
    size_bloom_filter = 20 #16 # 2^16= 65536 # 2^20 = 1048576
    num_bloom_filter = 1000 #100
    num_items_to_insert = 50000 #2500 # max of 104k
    num_known_items = 25000 #1000
    num_unknown_items = 25000 #1000
    
    try:
        word_file = "/usr/share/dict/words"
        items_to_insert = get_x_random_elements_from_list(open(word_file).read().splitlines(), num_items_to_insert)
    except: items_to_insert = [str(i) for i in range(num_items_to_insert)] # if not unix system

    start_time = time.time()
    false_positive_counter = 0
    for _ in tqdm(range(num_bloom_filter)):
        bf = bloom_filter(size_bloom_filter, args.num_func, args.crypto)
        
        # fill filter with items
        for item in items_to_insert:
            bf.insert(item)
        
        # check known items
        known_items = get_x_random_elements_from_list(items_to_insert, num_known_items)
        for item in known_items:
            item_included = bf.check(item)
            if not item_included:
                print("This is really suspicious.", item, "should be included in the filter.")

        # check unknown items
        unknown_items = get_x_random_elements_from_list(word_list, num_unknown_items)
        for item in unknown_items:
            # add a salt to make sure none of the items are the same as the known_items list
            #item_included = bf.check(item+"xy")
            item_included = bf.check(item)
            if item_included:
                false_positive_counter += 1
    
    end_time = time.time()
    false_positive_avg = (false_positive_counter / (num_bloom_filter * num_unknown_items))*100

    print("Execution took:          ", end_time - start_time, "seconds")
    print("False Positive average of", false_positive_avg, "% - total amount of", false_positive_counter, "False Positives")
    

def main(args):
    if args.auto: automatic_mode(args)
    else:
        bf = bloom_filter(args.size, args.num_func, args.crypto)
        manual_mode(bf)


def sanitize_arguments(args):
    if args.num_func < 1:
        print("at least one hash function should be used, value set to 1")
        args.num_func = 1
    elif args.num_func > max_num_hash_functions:
        print("not enough hash functions available, value set to the max of", max_num_hash_functions)
        args.num_func = max_num_hash_functions
    
    if args.size < 2: # lower limit is set, because a bloom filter with 2 entries makes very little sense
        print("size restriction, needs to be bigger, now set to 2**2 = 4 Bits")
        args.size = 2
    elif args.size > 30: # upper limit is set because of local machine, everything above is not feasible
        print("size restriction, cant be that big, now set to 2**30 = 1 073 741 824 Bits")
        args.size = 30 # that seems plenty big (~1 billion Bits) and also takes a lot of time to instanciate
        # I had a memory Error with exponent 32 (~4.3 billion Bits)
        # on my local machine the task got killed with exponent 31

    return args


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--size', type=int, default=4, help='exponent size of the bloom filter')
    parser.add_argument('-n', '--num_func', type=int, default=3, help='number of hash functions to be used')
    parser.add_argument('-c', '--crypto', action='store_true', help='cryptographic or non-cryptographic hash functions toggle')
    parser.add_argument('-a', '--auto', action='store_true', help='automatic or manual mode toggle')
    args = sanitize_arguments(parser.parse_args())
    main(args)
    