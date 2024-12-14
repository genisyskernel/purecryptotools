from bitcoin.address import Address
from bitcoin.wif import WIF


class Main:
    def __init__(self):
        # Instanciar WIF
        self.wif = WIF()

        # Instanciar Address
        self.address = Address()

    def private_key_to_wif(self, private_key, compressed=False, testnet=False):
        return self.wif.private_key_to_WIF(private_key, compressed, testnet)

    def wif_to_private_key(self, wif, integer):
        return self.wif.WIF_to_privatekey(wif, integer)

    def private_key_to_public_key_points(self, private_key):
        return self.address.private_key_to_public_key_points(private_key)
    
    def private_key_to_public_key(self, private_key, compressed):
        return self.address.private_to_public(private_key, compressed)

    def public_key_to_address(self, public_key):
        return self.address.public_to_address(public_key)

    def is_in_curve(self, public_key_x, public_key_y):
        return self.address.secp256k1.ecc.in_curve(public_key_x, public_key_y)

    def is_valid_private_key(self, private_key):
        return self.address.secp256k1.ecc.is_valid_private_key(private_key)


if __name__ == "__main__":
    main = Main()

    # Input private key
    hex_or_int = int(input("Informe qual o formato da chave privada [Hex=1/Int=2]: "))

    if (hex_or_int == 1):
        private_key = str(input("Informe a chave privada em hexadecimal:  "))
        private_key = int(private_key, 16)
    
    elif (hex_or_int == 2):
        private_key = int(input("Informe a chave privada em inteiro:      "))

    private_key_hex = hex(private_key)

    print(f"Private Key:                             {private_key}")
    print(f"Private Key Hex:                         {private_key_hex}")

    public_key_x, public_key_y = main.private_key_to_public_key_points(private_key)

    print(f"Chave pública (x):                       {public_key_x}")
    print(f"Chave pública (y):                       {public_key_y}")
    
    print(f"Chave pública Hex (x):                   {hex(public_key_x)}")
    print(f"Chave pública Hex (y):                   {hex(public_key_y)}")

    public_key_uncompressed = main.private_key_to_public_key(private_key, False)
    public_key_compressed = main.private_key_to_public_key(private_key, True)

    print(f"Public Key (Uncompressed):               {public_key_uncompressed}")
    print(f"Public Key (Compressed):                 {public_key_compressed}")

    wallet_address_uncompressed = main.public_key_to_address(public_key_uncompressed)
    wallet_address_compressed = main.public_key_to_address(public_key_compressed)

    print(f"Wallet Address (Uncompressed):           {wallet_address_uncompressed}")
    print(f"Wallet Address (Compressed):             {wallet_address_compressed}")

    is_valid_private_key = main.is_valid_private_key(private_key)

    in_curve = main.is_in_curve(public_key_x, public_key_y)

    wif_compressed = main.private_key_to_wif(private_key, compressed=True, testnet=False)
    wif_uncompressed = main.private_key_to_wif(private_key, compressed=False, testnet=False)

    print(f"WIF (Compressed):                        {wif_compressed}")
    print(f"WIF (Uncompressed):                      {wif_uncompressed}")

    wif_compressed_private_key = main.wif_to_private_key(wif_compressed, False)
    wif_compressed_private_key_hex = main.wif_to_private_key(wif_compressed, True)

    print(f"WIF To Private Key (Compressed):         {wif_compressed_private_key}")
    print(f"WIF To Private Key Hex (Compressed):     {wif_compressed_private_key_hex}")

    wif_uncompressed_private_key = main.wif_to_private_key(wif_uncompressed, False)
    wif_uncompressed_private_key_hex = main.wif_to_private_key(wif_uncompressed, True)

    print(f"WIF To Private Key (Uncompressed):       {wif_uncompressed_private_key}")
    print(f"WIF To Private Key Hex (Uncompressed):   {wif_uncompressed_private_key_hex}")

    print(f"in_curve? =>                             {in_curve}")
    print(f"is_valid_private_key? =>                 {is_valid_private_key}")

