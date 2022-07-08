import hashlib
from bitarray import bitarray

class bloom_filter:
    def __init__(self):
        self.filter_array = bitarray([0] * 2**20) # size=1048576
        self.hash_func_switch = {0: self.get_md5, 1: self.get_blake2s, 2: self.get_sha256, 3: self.get_sha512, 4: self.get_sha3_256}

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

def manual_mode(bf):
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
        if is_insert_mode: bf.insert(item)
        else:
            if bf.check(item): print(item, "is probably in the set")
            else: print(item, "is definitely not in the set")
   
if __name__ == "__main__":
    manual_mode(bloom_filter())
    