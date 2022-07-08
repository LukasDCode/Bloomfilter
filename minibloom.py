import time, random, argparse, hashlib
from bitarray import bitarray
from tqdm import tqdm

class bloom_filter:
    def __init__(self):
        self.filter_array = bitarray([0] * 2**20) # size=1048576
        self.hash_func_switch = {
            0: self.get_md5,
            1: self.get_blake2s,
            2: self.get_sha256,
            3: self.get_sha512,
            4: self.get_sha3_256
        }

    def insert(self, item):
        for hash_f_index in range(len(self.hash_func_switch)):
            self.filter_array[self.hash_func_switch[hash_f_index](item)] = 1

    def check(self, item):
        for hash_f_index in range(len(self.hash_func_switch)):
            if not self.filter_array[self.hash_func_switch[hash_f_index](item)]: return False
        return True

    def get_md5(self, input):
        return self.position_from_hex(hashlib.md5(input.encode("utf-8")).hexdigest())

    def get_blake2s(self, input):
        return self.position_from_hex(hashlib.blake2s(input.encode("utf-8")).hexdigest())

    def get_sha256(self, input):
        return self.position_from_hex(hashlib.sha256(input.encode("utf-8")).hexdigest())

    def get_sha512(self, input):
        return self.position_from_hex(hashlib.sha512(input.encode("utf-8")).hexdigest())

    def get_sha3_256(self, input):
        return self.position_from_hex(hashlib.sha3_256(input.encode("utf-8")).hexdigest())
    
    def position_from_hex(self, hex):
        return int(hex, 16)%len(self.filter_array)

def manual_mode():
    bf = bloom_filter()
    is_insert_mode = True
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
                elif user_input[1].lower() == "q": break # quit
                else:
                    print("unknown symbol after '!' - no action executed")
                    continue
            except IndexError:
                print("symbol after '!' expected - no action executed")
                continue
            try: item = user_input.split()[1] # tries switching modes and applying new item  
            except IndexError: continue # only switching modes, without inserting or checking
        else: item = user_input.split()[0] #normally checking or inserting item
        if item:
            if is_insert_mode: bf.insert(item)
            else:
                if bf.check(item): print(item, "is probably in the set")
                else: print(item, "is definitely not in the set")
        else: print("no useful input detected")

def get_x_random_elements_from_list(original_list, num_elements):
    to_keep = set(random.sample(range(len(original_list)), min(len(original_list), max(1, num_elements))))
    return [x for i,x in enumerate(original_list) if i in to_keep]

def automatic_mode():
    num_bloom_filter, num_items_to_insert, num_known_items, num_unknown_items  = 1000, 50000, 25000, 25000  
    try:
        word_file = "/usr/share/dict/words" # eventhough this is not minimal, it is more parameterized like this
        word_list = open(word_file).read().splitlines()
        items_to_insert = get_x_random_elements_from_list(word_list, num_items_to_insert)
    except: items_to_insert = [str(i) for i in range(num_items_to_insert)] # if not unix system
    start_time, false_positive_counter = time.time(), 0
    for _ in tqdm(range(num_bloom_filter)):
        bf = bloom_filter()
        # fill filter with items
        for item in items_to_insert: bf.insert(item)
        # check known items
        known_items = get_x_random_elements_from_list(items_to_insert, num_known_items)
        for item in known_items:
            if not bf.check(item):
                print("This is really suspicious.", item, "should be included in the filter.")
        # check unknown items
        unknown_items = get_x_random_elements_from_list(word_list, num_unknown_items)
        for item in unknown_items:
            item_included = bf.check(item)
            if item_included:
                false_positive_counter += 1
    print("Execution took:          ", time.time() - start_time, "seconds")
    print("False Positive average of", (false_positive_counter / (num_bloom_filter * num_unknown_items))*100, "% - total amount of", false_positive_counter, "False Positives")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--auto', action='store_true', help='automatic or manual mode toggle')
    if parser.parse_args().auto: automatic_mode()
    else: manual_mode()
    