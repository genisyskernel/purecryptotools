from ecc.elliptic_curve_cryptography import EllipticCurveCryptography


class Secp256k1:
    def __init__(self):
        # Params Bitcoin Curve (secp256k1)
        self.p = 115792089237316195423570985008687907853269984665640564039457584007908834671663         # Modulo (número primo pequeno)
        self.n_order = 115792089237316195423570985008687907852837564279074904382605163141518161494337   # Ordem do ponto gerador (por simplicidade, não precisa ser o valor real)
        self.Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240         # Coordenadas X do ponto gerador
        self.Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424         # Coordenadas Y do ponto gerador
        self.A = 0
        self.B = 7

        # Ecc Instance
        self.ecc = EllipticCurveCryptography(self.p, self.n_order, self.Gx, self.Gy, self.A, self.B)
