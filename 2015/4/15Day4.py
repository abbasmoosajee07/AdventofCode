import hashlib

def find_advent_coin(secret_key,zero_start):
    number = 1  # Start from the first positive integer

    while True:
        # Combine the secret key with the current number
        input_str = f"{secret_key}{number}".encode()  # Encode to bytes
        # Calculate the MD5 hash
        md5_hash = hashlib.md5(input_str).hexdigest()
        
        # Check if the hash starts with five zeroes
        if md5_hash.startswith(zero_start):
            return number, md5_hash  # Return the number and corresponding hash
        
        number += 1  # Increment the number

# Your puzzle input
secret_key = "ckczppom"

result_number_5, result_hash_5 = find_advent_coin(secret_key,"00000")

print(f"The lowest positive number that produces an MD5 hash starting with five zeroes is: {result_number_5}")
print(f"The corresponding MD5 hash is: {result_hash_5}")

result_number_6, result_hash_6 = find_advent_coin(secret_key,"000000")
print(f"The lowest positive number that produces an MD5 hash starting with six zeroes is: {result_number_6}")
print(f"The corresponding MD5 hash is: {result_hash_6}")
