from bitarray import bitarray
import argparse

# non-cryptographic hash functions
import mmh3 #https://pypi.org/project/mmh3/
from fnvhash import fnv1a_32 #https://pypi.org/project/fnvhash/
import jenkins_cffi as jenkins #https://github.com/what-studio/jenkins-cffi/
from pearhash import PearsonHasher #https://github.com/ze-phyr-us/pearhash


crypto_hash_list = [] #md5, sha
non_crpyto_hash_list = ["murmur", "fnv", "jenkins", "pearson", "hex"] # fnv = fowler-noll-vo


class bloom_filter:
    """
    k = # of hash functions used for each item
    m = size of the bloom filter
    n = # of items inserted into the filter
    """
    verbose = False

    def __init__(self, array_size_exponent=4, num_hash_functions=3, is_cryptographic=False):
        self.filter_array = bitarray([0] * 2**array_size_exponent)
        self.array_size_exponent = array_size_exponent
        self.num_hash_functions = num_hash_functions
        #print(self.filter_array, "size:", 2**array_size_exponent)
    

    def print_filter(self):
        print(self.filter_array, "size:", 2**self.array_size_exponent)

    def toggle_verbose(self):
        bloom_filter.verbose = not bloom_filter.verbose
        print("verbose toggled to", bloom_filter.verbose)

    def insert(self, item):
        murmur_position = self.get_murmur(item)
        fnv_position = self.get_fnv(item)
        jenkins_position = self.get_jenkins(item)
        pearson_position = self.get_pearson(item)
        hex_position = self.get_hex(item)

        if bloom_filter.verbose:
            print("insert", item)
            print("murmur ", murmur_position)
            print("fnv    ", fnv_position)
            print("jenkins", jenkins_position)
            print("pearson", pearson_position)
            print("hex    ", hex_position)
        

        self.filter_array[murmur_position] = 1
        self.filter_array[fnv_position] = 1
        self.filter_array[jenkins_position] = 1
        self.filter_array[pearson_position] = 1
        self.filter_array[hex_position] = 1


        #TODO only use specific hash functions
        #TODO also for cryptographic hash functions


    def check(self, item):
        murmur_position = self.get_murmur(item)
        fnv_position = self.get_fnv(item)
        jenkins_position = self.get_jenkins(item)
        pearson_position = self.get_pearson(item)
        hex_position = self.get_hex(item)

        if bloom_filter.verbose: print("check", item)
        
        return (self.filter_array[murmur_position] and
                self.filter_array[fnv_position] and
                self.filter_array[jenkins_position] and
                self.filter_array[pearson_position] and
                self.filter_array[hex_position])


    def get_murmur(self, input):
        murmur_hash = mmh3.hash(input, signed=False)
        #print("murmur", murmur_hash)
        return self.position_from_int(murmur_hash)

    def get_fnv(self, input):
        fnv_hash = hex(fnv1a_32(input.encode()))
        #print("fnv", fnv_hash, "fnv int", int(fnv_hash, 16))
        return self.position_from_hex(fnv_hash)

    def get_jenkins(self, input):
        jenkins_hash = jenkins.hashlittle(input.encode())
        #print("jenkins", jenkins_hash)
        return self.position_from_int(jenkins_hash)

    def get_pearson(self, input):
        pearson_hasher = PearsonHasher(self.array_size_exponent) # Set desired hash length in bytes.
        pearson_hash = pearson_hasher.hash(input.encode()).hexdigest()
        #print("pearson", pearson_hash, "pearson int", int(pearson_hash, 16))
        return self.position_from_hex(pearson_hash)
        
    def get_hex(self, input):
        hex_value = input.encode('utf-8').hex() #hex(item)
        #print("hex_value", hex_value, "hex to int", int(hex_value, 16)
        return self.position_from_hex(hex_value)

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
            if user_input[1].lower() == "i": # insert
                is_insert_mode = True
                print("insertion mode activated")
            elif user_input[1].lower() == "c": # check
                is_insert_mode = False
                print("check mode activated")
            elif user_input[1].lower() == "p":
                bf.print_filter()
            elif user_input[1].lower() == "v":
                bf.toggle_verbose()
            elif user_input[1].lower() == "q":
                break
            else:
                print("unknown symbol after '!' - no action executed")
                continue

            try:
                item = user_input.split()[1]
            except:
                continue # only switching modes, without inserting or checking
        else:
            item = user_input.split()[0]
        
        if item:
            #print("item:", item)
            if is_insert_mode:
                bf.insert(item)
            else:
                in_set = bf.check(item)
                if in_set:
                    print(item, "is probably in the set")
                else:
                    print(item, "is definitely not in the set")
        else:
            print("no useful input detected")


def automatic_mode(bf):
    print("automatic mode is currently not implemented, try again without the '--auto' tag")


def main(filter_size_exponent, num_hash_functions, cryptographic_hash_functions=False, is_automatic_mode=False): # 2**4=16, 2**8=256
    bf = bloom_filter(filter_size_exponent, num_hash_functions, cryptographic_hash_functions)

    if is_automatic_mode:
        automatic_mode(bf)
    else:
        manual_mode(bf)


def sanitize_arguments(args):
    if args.crypto:
        if args.num_func < 1:
            print("at least one hash function should be used, value set to 1")
            args.num_func = 1
        elif args.num_func > len(crypto_hash_list):
            print("not enough hash functions available, value set to the max of", len(crypto_hash_list))
            args.num_func = len(crypto_hash_list)
    else:
        if args.num_func < 1:
            print("at least one hash function should be used, value set to 1")
            args.num_func = 1
        elif args.num_func > len(non_crpyto_hash_list):
            print("not enough hash functions available, value set to the max of", len(non_crpyto_hash_list))
            args.num_func = len(non_crpyto_hash_list)

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
    parser.add_argument('--size', type=int, default=4, help='exponent size of the bloom filter')
    parser.add_argument('--num_func', type=int, default=3, help='number of hash functions to be used')
    parser.add_argument('--crypto', action='store_true', help='cryptographic or non-cryptographic hash functions toggle')
    parser.add_argument('--auto', action='store_true', help='automatic or manual mode toggle')
    args = sanitize_arguments(parser.parse_args())
    main(filter_size_exponent=args.size, num_hash_functions=args.num_func, cryptographic_hash_functions=args.crypto, is_automatic_mode=args.auto)