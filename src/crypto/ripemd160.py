import struct


class Ripemd160:
    
    def __init__(self):    
        # The permutation ρ
        rho = [7, 4, 13, 1, 10, 6, 15, 3, 12, 0, 9, 5, 2, 14, 11, 8]

        # The permutation π(i) = 9i + 5  (mod 16)
        pi = [(9*i + 5) % 16 for i in range(16)]

        # Round permutation r (left line)
        self.rl = [list(range(16))]  # id
        self.rl += [[rho[j] for j in self.rl[-1]]]  # ρ
        self.rl += [[rho[j] for j in self.rl[-1]]]  # ρ^2
        self.rl += [[rho[j] for j in self.rl[-1]]]  # ρ^3
        self.rl += [[rho[j] for j in self.rl[-1]]]  # ρ^4

        # r' (right line)
        self.rr = [list(pi)]  # π
        self.rr += [[rho[j] for j in self.rr[-1]]]  # ρπ
        self.rr += [[rho[j] for j in self.rr[-1]]]  # ρ^2 π
        self.rr += [[rho[j] for j in self.rr[-1]]]  # ρ^3 π
        self.rr += [[rho[j] for j in self.rr[-1]]]  # ρ^4 π

        # Boolean functions
        f1 = lambda x, y, z: x ^ y ^ z
        f2 = lambda x, y, z: (x & y) | (~x & z)
        f3 = lambda x, y, z: (x | ~y) ^ z
        f4 = lambda x, y, z: (x & z) | (y & ~z)
        f5 = lambda x, y, z: x ^ (y | ~z)

        # boolean functions (left line)
        self.fl = [f1, f2, f3, f4, f5]

        # boolean functions (right line)
        self.fr = [f5, f4, f3, f2, f1]

        # Shifts
        _shift1 = [11, 14, 15, 12, 5, 8, 7, 9, 11, 13, 14, 15, 6, 7, 9, 8]
        _shift2 = [12, 13, 11, 15, 6, 9, 9, 7, 12, 15, 11, 13, 7, 8, 7, 7]
        _shift3 = [13, 15, 14, 11, 7, 7, 6, 8, 13, 14, 13, 12, 5, 5, 6, 9]
        _shift4 = [14, 11, 12, 14, 8, 6, 5, 5, 15, 12, 15, 14, 9, 9, 8, 6]
        _shift5 = [15, 12, 13, 13, 9, 5, 8, 6, 14, 11, 12, 11, 8, 6, 5, 5]

        # shifts (left line)
        self.sl = [[_shift1[self.rl[0][i]] for i in range(16)]]
        self.sl.append([_shift2[self.rl[1][i]] for i in range(16)])
        self.sl.append([_shift3[self.rl[2][i]] for i in range(16)])
        self.sl.append([_shift4[self.rl[3][i]] for i in range(16)])
        self.sl.append([_shift5[self.rl[4][i]] for i in range(16)])

        # shifts (right line)
        self.sr = [[_shift1[self.rr[0][i]] for i in range(16)]]
        self.sr.append([_shift2[self.rr[1][i]] for i in range(16)])
        self.sr.append([_shift3[self.rr[2][i]] for i in range(16)])
        self.sr.append([_shift4[self.rr[3][i]] for i in range(16)])
        self.sr.append([_shift5[self.rr[4][i]] for i in range(16)])

        # Constants
        self._kg = lambda x, y: int(2**30 * (y ** (1.0 / x)))

        # constants (left line)
        self.KL = [
            0,          # Round 1: 0
            self._kg(2, 2),  # Round 2: 2**30 * sqrt(2)
            self._kg(2, 3),  # Round 3: 2**30 * sqrt(3)
            self._kg(2, 5),  # Round 4: 2**30 * sqrt(5)
            self._kg(2, 7),  # Round 5: 2**30 * sqrt(7)
        ]

        # constants (right line)
        self.KR = [
            self._kg(3, 2),  # Round 1: 2**30 * cubert(2)
            self._kg(3, 3),  # Round 2: 2**30 * cubert(3)
            self._kg(3, 5),  # Round 3: 2**30 * cubert(5)
            self._kg(3, 7),  # Round 4: 2**30 * cubert(7)
            0,          # Round 5: 0
        ]

        # Initial value
        self.initial_h = tuple(struct.unpack("<5L", bytes.fromhex("0123456789ABCDEFFEDCBA9876543210F0E1D2C3")))

    # Rather than writing & 0xffffffff every time (and risking typographical
    # errors each time), we use this function.
    # Thanks to Thomas Dixon for the idea.
    def u32(self, n):
        return n & 0xFFFFFFFF

    # cyclic rotate
    def rol(self, s, n):
        assert 0 <= s <= 31
        assert 0 <= n <= 0xFFFFFFFF
        return self.u32((n << s) | (n >> (32-s)))

    def box(self, h, f, k, x, r, s):
        assert len(s) == 16
        assert len(x) == 16
        assert len(r) == 16
        (a, b, c, d, e) = h
        for word in range(16):
            T = self.u32(a + f(b, c, d) + x[r[word]] + k)
            T = self.u32(self.rol(s[word], T) + e)
            (b, c, d, e, a) = (T, b, self.rol(10, c), d, e)
        return (a, b, c, d, e)

    def _compress(self, h, x):    # x is a list of 16 x 32-bit words
        hl = hr = h

        # Iterate through all 5 rounds of the compression function for each parallel pipeline
        for round in range(5):
            # left line
            hl = self.box(hl, self.fl[round], self.KL[round], x, self.rl[round], self.sl[round])
            # right line
            hr = self.box(hr, self.fr[round], self.KR[round], x, self.rr[round], self.sr[round])

        # Mix the two pipelines together
        h = (self.u32(h[1] + hl[2] + hr[3]),
            self.u32(h[2] + hl[3] + hr[4]),
            self.u32(h[3] + hl[4] + hr[0]),
            self.u32(h[4] + hl[0] + hr[1]),
            self.u32(h[0] + hl[1] + hr[2]))

        return h

    def compress(self, h, s):
        """The RIPEMD-160 compression function"""
        assert len(s) % 64 == 0
        p = 0
        while p < len(s):
            x = s[p:p+64]  # chunk
            x = [struct.unpack("<L", x[i:i+4])[0] for i in range(0, len(x), 4)]
            h = self._compress(h, x)
            p += 64
        return h

    def hsh(self, message):
        # Preprocessing: Add padding and append length of message
        #message = message.encode('utf-8')  # Convert string to bytes
        length = len(message)
        message += b'\x80'  # add padding byte
        while len(message) % 64 != 56:
            message += b'\x00'  # pad with zeros
        message += struct.pack("<Q", 8 * length)  # append length

        h = self.initial_h
        # 2. Compute the hash
        h = self.compress(h, message)  # Use the bytes directly
        return h

    def digest(self, message):
        h = self.hsh(message)
        return bytes(struct.pack("<5L", *h))


if __name__ == "__main__":
    ripemd160 = Ripemd160()
    test_message = b"Test"
    ripemd160_hash = ripemd160.digest(test_message).hex()
    print(f"RIPEMD-160 Hash of '{test_message.decode("utf-8")}': {ripemd160_hash}")
    print(f"Valid? {ripemd160_hash == "76c82682cd7af7e812e513fa0e7914ab40b842e0"}")
