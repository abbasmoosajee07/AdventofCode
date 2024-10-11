import hashlib

def find_md5_with_leading_zeros(prefix, count):
    results = []
    num = 0

    while len(results) < count:
        # Create a string representation of the number
        input_str = str(num).encode()  # Encode the string to bytes
        # Calculate MD5 hash
        md5_hash = hashlib.md5(input_str).hexdigest()
        # Check if the hash starts with the required number of zeroes
        if md5_hash.startswith(prefix):
            results.append((num, md5_hash))
            print(f"Found: {num} -> {md5_hash}")
        num += 1

    return results

# Find MD5 hashes that start with at least five zeroes
prefix = '00000'
count = 1  # Specify how many hashes you want to find
results = find_md5_with_leading_zeros(prefix, count)
# ckczppom