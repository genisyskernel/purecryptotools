# PureCryptoTools

**PureCryptoTools** é um conjunto de ferramentas criptográficas desenvolvidas em puro Python, sem bibliotecas externas. Este projeto permite realizar operações relacionadas a chaves privadas, WIF (Wallet Import Format), chaves públicas e endereços de carteira para Bitcoin.

## Funcionalidades

- Converter chave privada para WIF.
- Converter WIF para chave privada.
- Gerar pontos de chave pública a partir de uma chave privada.
- Gerar chave pública comprimida e não comprimida.
- Gerar endereço de Bitcoin a partir de uma chave pública.
- Verificar se uma chave pública está na curva elíptica secp256k1.
- Validar se uma chave privada é válida.

## Pré-requisitos

- Python 3.6 ou superior.
- Pipenv para gerenciamento de dependências e ambiente virtual.

## Como usar

1. Clone este repositório:

```bash
git clone https://github.com/genisyskernel/purecryptotools.git
```

2. Acesse o diretório do projeto:

```bash
cd purecryptotools
```

3. Crie o ambiente virtual usando o `pipenv`:

```bash
pipenv install
```

4. Ative o ambiente virtual criado pelo `pipenv`:

```bash
pipenv shell
```

5. Execute o arquivo principal:

```bash
python src/main/main.py
```

6. Siga as instruções interativas no terminal para realizar operações com chaves privadas, WIF e endereços de Bitcoin.

## Estrutura do Projeto

```plaintext
src/
├── base/
│   └── base58.py
├── bitcoin/
│   ├── address.py
│   ├── secp256k1.py
│   └── wif.py
├── crypto/
│   ├── ripemd160.py
│   └── sha256.py
├── ecc/
│   └── elliptic_curve_cryptography.py
├── main/
│   └── main.py
```

- **base/**: Contém utilitários para codificação Base58.
- **bitcoin/**: Contém módulos para manipulação de endereços, chaves privadas e formato WIF.
- **crypto/**: Implementa funções de hash criptográfico, como RIPEMD-160 e SHA-256.
- **ecc/**: Implementa operações de criptografia de curva elíptica (secp256k1).
- **main/**: Contém o arquivo principal `main.py`.

## Observação para usuários do VS Code

Se estiver usando o projeto com o VS Code, crie um arquivo chamado `.env` na raiz do projeto com o seguinte conteúdo para garantir o funcionamento correto da modularização:

```plaintext
PYTHONPATH=./src:${PYTHONPATH}
```

## Exemplo de Uso

Ao executar `main.py`, você será solicitado a inserir uma chave privada em hexadecimal ou inteiro. O programa irá:

- Exibir a chave privada em vários formatos (hexadecimal e inteiro).
- Gerar a chave pública e seu endereço associado (comprimido e não comprimido).
- Converter a chave privada para WIF (comprimido e não comprimido).
- Validar a chave privada e verificar se a chave pública gerada está na curva.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma _issue_ ou enviar um _pull request_.

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
