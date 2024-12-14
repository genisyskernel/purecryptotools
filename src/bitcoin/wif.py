from crypto.sha256 import SHA256
from base.base58 import Base58


class WIF:

    def __init__(self):
        # Instances
        self.base58 = Base58()
        self.sha256 = SHA256()

    def private_key_to_WIF(self, private_key, compressed=False, testnet=False):
        """
        Converte uma chave privada (inteira ou hexadecimal) para o formato WIF.

        Args:
            private_key (int ou str): A chave privada em formato inteiro ou hexadecimal.
            compressed (bool): Indica se a chave está em formato comprimido.
            testnet (bool): Indica se é para a rede de teste (testnet).

        Returns:
            str: A chave privada em formato WIF.
        """
        # Verifica se a chave privada é um inteiro ou uma string hexadecimal
        if isinstance(private_key, int):
            # Converte inteiro para hexadecimal (mínimo 32 bytes)
            private_key_hex = f"{private_key:064x}"
        elif isinstance(private_key, str):
            # Valida se é um hexadecimal válido
            if all(c in "0123456789abcdefABCDEF" for c in private_key) and len(private_key) <= 64:
                private_key_hex = private_key.zfill(64)  # Garante 64 caracteres preenchendo com zeros à esquerda
            else:
                raise ValueError("A chave privada em formato string não é um hexadecimal válido.")
        else:
            raise TypeError("A chave privada deve ser um inteiro ou uma string hexadecimal.")

        # Passo 1: Prefixo da rede
        prefix = b'\x80' if not testnet else b'\xEF'  # \x80 para mainnet, \xEF para testnet

        # Passo 2: Adicionar o prefixo à chave privada
        private_key_bytes = bytes.fromhex(private_key_hex)
        extended_key = prefix + private_key_bytes

        # Passo 3: Adicionar o sufixo de compressão se necessário
        if compressed:
            extended_key += b'\x01'

        # Passo 4: Calcular o checksum
        first_sha256 = self.sha256.sha256(extended_key)
        second_sha256 = self.sha256.sha256(first_sha256)
        checksum = second_sha256[:4]  # 4 bytes do início do hash

        # Passo 5: Concatenar extended_key e checksum
        final_key = extended_key + checksum

        # Passo 6: Codificar em base58
        wif = self.base58.encode(final_key)
        return wif

    def WIF_to_privatekey(self, wif, integer=False):
        """
        Converte uma chave privada em formato WIF de volta para hexadecimal.

        Args:
            wif (str): A chave privada no formato WIF.
            integer (bool): Indica se o retorno deve ser um inteiro em vez de uma string hexadecimal.

        Returns:
            tuple: Uma tupla contendo a chave privada em hexadecimal (str ou int) e um booleano indicando se está em formato comprimido.
        """
        # Decodificar a chave WIF usando Base58
        decoded = self.base58.decode(wif)

        # Dividir a chave nos componentes: prefixo, chave, e checksum
        network_byte = decoded[0:1]  # Prefixo da rede
        key = decoded[1:-4]          # Chave sem o checksum
        checksum = decoded[-4:]      # Últimos 4 bytes são o checksum

        # Validar o checksum
        first_sha256 = self.sha256.sha256(decoded[:-4])
        second_sha256 = self.sha256.sha256(first_sha256)
        calculated_checksum = second_sha256[:4]  # Primeiros 4 bytes do segundo hash
        if calculated_checksum != checksum:
            raise ValueError("Checksum inválido para a chave WIF fornecida.")

        # Verificar se a chave está em formato comprimido
        if len(key) == 33 and key[-1] == 0x01:  # Verificar se o último byte é 0x01
            key = key[:-1]
            compressed = True
        else:
            compressed = False

        # Converter a chave privada para o formato desejado
        private_key_hex = key.hex()

        if integer:
            private_key = int(private_key_hex, 16)
        else:
            private_key = private_key_hex

        return private_key, compressed


if __name__ == "__main__":
    wif = WIF()

    private_key_int_tests = 1
    private_key_hex_tests = 0x1

    # Compressed
    # Teste com chave privada em formato inteiro
    private_key_wif = wif.private_key_to_WIF(private_key_int_tests, compressed=True)
    print("WIF Compressed (Int):", private_key_wif)

    # Teste com chave privada em formato hexadecimal
    private_key_wif_hex = wif.private_key_to_WIF(private_key_hex_tests, compressed=True)
    print("WIF Compressed (Hex):", private_key_wif_hex)

    # Compressed
    # WIF para chave privada
    wif_private_key_c, private_key_compressed = wif.WIF_to_privatekey(private_key_wif, integer=True)
    wif_private_key_hex_c, private_key_hex_compressed = wif.WIF_to_privatekey(private_key_wif_hex, integer=False)

    if private_key_compressed:
        print("Private Key Compressed (Int):", wif_private_key_c)
    else:
        print("Private Key Uncompressed (Int):", wif_private_key_c)

    if private_key_hex_compressed:
        print("Private Key Hex Compressed (Hex):", wif_private_key_hex_c)
    else:
        print("Private Key Hex Uncompressed (Hex):", wif_private_key_hex_c)

    #######################################################################################################

    print(f"="*120)

    #######################################################################################################

    # Uncompressed
    # Teste com chave privada em formato inteiro
    private_key_int = 1
    private_key_wif = wif.private_key_to_WIF(private_key_int_tests, compressed=False)
    print("WIF Uncompressed (Int):", private_key_wif)

    # Teste com chave privada em formato hexadecimal
    private_key_hex = "1"
    private_key_wif_hex = wif.private_key_to_WIF(private_key_hex_tests, compressed=False)
    print("WIF Uncompressed (Hex):", private_key_wif_hex)

    # Uncompressed
    # WIF para chave privada
    wif_private_key_u, private_key_uncompressed = wif.WIF_to_privatekey(private_key_wif, integer=True)
    wif_private_key_hex_u, private_key_hex_uncompressed = wif.WIF_to_privatekey(private_key_wif_hex, integer=False)

    if private_key_uncompressed:
        print("Private Key Compressed (Int):", wif_private_key_u)
    else:
        print("Private Key Uncompressed (Int):", wif_private_key_u)

    if private_key_hex_uncompressed:
        print("Private Key Hex Compressed (Hex):", wif_private_key_hex_u)
    else:
        print("Private Key Hex Uncompressed (Hex):", wif_private_key_hex_u)