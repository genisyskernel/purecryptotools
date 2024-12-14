class Base58:

    def __init__(self):
        # O alfabeto Base58 utilizado em Bitcoin (exclui 0, O, I, l)
        self.ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

    def encode(self, input_bytes):
        """Codifica uma sequência de bytes em Base58."""
        # Conta o número de bytes zero no início
        leading_zeros = len(input_bytes) - len(input_bytes.lstrip(b'\x00'))
        
        # Converte os bytes restantes para um número inteiro
        n = int.from_bytes(input_bytes, 'big')
        encoded = []

        # Realiza a codificação para Base58
        while n > 0:
            n, rem = divmod(n, 58)
            encoded.append(self.ALPHABET[rem])

        # Adiciona os zeros à esquerda na forma de '1'
        return '1' * leading_zeros + ''.join(reversed(encoded)) or '1'

    def decode(self, base58_str):
        """Decodifica uma string Base58 de volta para bytes."""
        base58_map = {char: index for index, char in enumerate(self.ALPHABET)}

        n = 0
        for char in base58_str:
            n *= 58
            n += base58_map[char]

        # Calcula o número de bytes necessário para armazenar o valor
        byte_length = (n.bit_length() + 7) // 8

        # Converte o número de volta para bytes
        decoded_bytes = n.to_bytes(byte_length, 'big')

        # Conta o número de 1s à esquerda no endereço Base58
        leading_zeros = len(base58_str) - len(base58_str.lstrip('1'))

        # Adiciona os zeros à esquerda para refletir a quantidade de '1' no início do endereço Base58
        return b'\x00' * leading_zeros + decoded_bytes


if __name__ == "__main__":
    base58 = Base58()

    wallet = "1Mg4MNgCZ2LFH8GBfjYNpKyGWwVxA43eUR"

    wallet_decode = base58.decode(wallet)

    wallet_encode = base58.encode(wallet_decode)

    print(f"Wallet:         {wallet}")
    print(f"Wallet Encoded: {wallet_encode}")
