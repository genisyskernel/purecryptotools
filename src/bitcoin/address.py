from bitcoin.secp256k1 import Secp256k1
from crypto.ripemd160 import Ripemd160
from crypto.sha256 import SHA256
from base.base58 import Base58


class Address:
    def __init__(self):
        # Instanciar secp256k1
        self.secp256k1 = Secp256k1()

        # Instanciar Base58
        self.base58 = Base58()

        # Instanciar SHA256
        self.sha256 = SHA256()
        
        # Instanciar Ripemd160
        self.ripemd160 = Ripemd160()

    def private_key_to_public_key_points(self, private_key):
        # Calculate public key point
        public_key_x, public_key_y = self.secp256k1.ecc.eccnP(private_key)

        return public_key_x, public_key_y

    def private_to_public(self, private_key, compressed=True):
        """
        Converte uma chave privada para chave pública usando a curva secp256k1.
        """
        public_key_x, public_key_y = self.private_key_to_public_key_points(private_key)
        
        if not self.secp256k1.ecc.in_curve(public_key_x, public_key_y):
            raise ValueError("A chave pública gerada não está na curva.")
        
        if compressed:
            # Formato comprimido: 0x02 se y é par, 0x03 se y é ímpar
            prefix = b'\x02' if public_key_y % 2 == 0 else b'\x03'
            public_key = prefix + public_key_x.to_bytes(32, byteorder='big')
        else:
            # Formato não comprimido: 0x04 + x + y
            public_key = (
                b'\x04'
                + public_key_x.to_bytes(32, byteorder='big')
                + public_key_y.to_bytes(32, byteorder='big')
            )
        
        return public_key.hex()
    
    def public_to_address(self, public_key):
        """
        Converte a chave pública em um endereço compatível com BitAiir.
        """
        public_key_bytes = bytes.fromhex(public_key)
        sha256_bpk = self.sha256.sha256(public_key_bytes)
        ripemd160_bpk = self.ripemd160.digest(sha256_bpk)
        prefixed_bpk = b'\x00' + ripemd160_bpk  # Prefixo 0x00 para endereço padrão
        
        checksum = self.sha256.sha256(self.sha256.sha256(prefixed_bpk))[:4]
        address = self.base58.encode(prefixed_bpk + checksum)
        return address

    def private_key_to_WIF(self, private_key, compressed=False):
        """
        Converte uma chave privada para o formato WIF, com suporte para formato comprimido.
        """
        private_key_hex = f"{private_key:064x}"  
        extended_key = b'\x80' + bytes.fromhex(private_key_hex)  # Prefixo 'fe' para BitAiir
        if compressed:
            extended_key += b'\x01'  # Byte adicional para WIF comprimido

        first_sha256 = self.sha256.sha256(extended_key)
        second_sha256 = self.sha256.sha256(first_sha256)
        checksum = second_sha256[:4]
        final_key = extended_key + checksum
        return self.base58.encode(final_key)


if __name__ == "__main__":
    # Instanciar
    address = Address()

    # Definir uma chave privada (k)
    # Hex
    # private_key = 0xabc

    # Int
    private_key = 1

    # Calculate public key point
    public_key_x, public_key_y = address.private_key_to_public_key_points(private_key)

    # Exibir a chave pública
    print(f"Chave pública (x):          {public_key_x}")
    print(f"Chave pública (y):          {public_key_y}")
    #
    print(f"Chave pública Hex (x):      {hex(public_key_x)}")
    print(f"Chave pública Hex (y):      {hex(public_key_y)}")
    #
    print(f"in_curve? =>                {address.secp256k1.ecc.in_curve(public_key_x, public_key_y)}")
    print(f"is_valid_private_key? =>    {address.secp256k1.ecc.is_valid_private_key(private_key)}")

    #############################################################################################################

    print(f"="*120)

    #############################################################################################################

    # Chave pública e endereço não comprimidos
    public_key_uncompressed = address.private_to_public(private_key, compressed=False)
    address_uncompressed = address.public_to_address(public_key_uncompressed)
    wif_uncompressed = address.private_key_to_WIF(private_key, compressed=False)
    
    # Chave pública e endereço comprimidos
    public_key_compressed = address.private_to_public(private_key, compressed=True)
    address_compressed = address.public_to_address(public_key_compressed)
    wif_compressed = address.private_key_to_WIF(private_key, compressed=True)

    print(f"Private Key:                {private_key}")
    print(f"Public Key (Uncompressed):  {public_key_uncompressed}")
    print(f"Public Key (Compressed):    {public_key_compressed}")
    print(f"Address (Uncompressed):     {address_uncompressed}")
    print(f"Address (Compressed):       {address_compressed}")
    print(f"WIF (Uncompressed):         {wif_uncompressed}")
    print(f"WIF (Compressed):           {wif_compressed}")
