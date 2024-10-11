# Using the extended Euclidean algorithm to find the multiplicative inverse of 101 modulo 23341065
import math


def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


# Inputs
a = 101
mod = 23341065

# Find the gcd and the multiplicative inverse if gcd is 1
gcd, x, _ = extended_gcd(a, mod)

# Ensure the result is positive
if gcd == 1:
    inverse = x % mod
else:
    inverse = None


# Using binary exponentiation technique to find the multiplicative inverse of a number modulo another number.
# We use Fermat's Little Theorem, which states a^(m-1) ≡ 1 (mod m), for prime m.
# Since 23341065 is not necessarily prime, we will use Extended Euclidean Algorithm for mod-inverse.
# However, with binary exponentiation, we can still compute (a^(m-2) mod m).

def binary_exponentiation(base, exponent, mod):
    result = 1
    base = base % mod
    while exponent > 0:
        if (exponent % 2) == 1:  # If exponent is odd, multiply base with result
            result = (result * base) % mod
        exponent = exponent >> 1  # Divide exponent by 2
        base = (base * base) % mod  # Square the base
    return result


# Inverse of 101 mod 23341065
mod = 23341065
num = 101
# We need to find num^(mod-2) % mod
phi = 11316800
a = binary_exponentiation(num, phi - 1, mod)
b = binary_exponentiation(3, phi - 1, mod)

print(inverse, a, b, (a * 3) % mod)
print((num * a) % mod)
print((num * a) % mod)

# for i in range(2, 23341065):
#     if (101 * i) % 23341065 == 3:
#         print(i)

# print(2121, math.gcd(101, 23341065))
# 18025773
print((101 * 7189767) % mod)

print(rec(0, id))
print((3 ** 5 ** 6) % id)
