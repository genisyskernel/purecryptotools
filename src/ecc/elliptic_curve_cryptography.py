class EllipticCurveCryptography:
    def __init__(self, p, n_order, Gx, Gy, A, B):
        self.p = p
        self.n_order = n_order
        self.Gx = Gx
        self.Gy = Gy
        self.A = A
        self.B = B
        self.pointNULL = (0, 0)

    def modp(self, n, p1):
        return n % p1

    def inverse(self, r, p):
        t, newt = 1, 0
        r, newr = r, p
        while newr != 0:
            quotient = r // newr
            t, newt = newt, t - quotient * newt
            r, newr = newr, r - quotient * newr
        return t % p

    def doublep(self, x, y):
        m = self.modp((3 * x**2 + self.A) * self.inverse(2 * y, self.p), self.p)
        x_r = self.modp(m**2 - 2 * x, self.p)
        y_r = self.modp(m * (x - x_r) - y, self.p)
        return x_r, y_r

    def addp(self, x1, y1, x2, y2):
        if x1 == x2 and y1 == y2:
            return self.doublep(x1, y1)
        m = self.modp((y2 - y1) * self.inverse(x2 - x1, self.p), self.p)
        x_r = self.modp(m**2 - x1 - x2, self.p)
        y_r = self.modp(m * (x1 - x_r) - y1, self.p)
        return x_r, y_r

    def eccnP(self, n):
        qx, qy = self.Gx, self.Gy
        resx, resy = self.pointNULL
        while n:
            if n & 1:
                resx, resy = self.addp(resx, resy, qx, qy) if resx != 0 else (qx, qy)
            qx, qy = self.doublep(qx, qy)
            n >>= 1
        return resx, resy

    def in_curve(self, x, y):
        return (y * y) % self.p == (x**3 + self.A * x + self.B) % self.p
    
    def is_valid_private_key(self, k):
        return 1 <= k < self.n_order


if __name__ == "__main__":
    # Parâmetros da Curva do Bitcoin (secp256k1)
    p = 115792089237316195423570985008687907853269984665640564039457584007908834671663         # Modulo (número primo pequeno)
    n_order = 115792089237316195423570985008687907852837564279074904382605163141518161494337   # Ordem do ponto gerador (por simplicidade, não precisa ser o valor real)
    Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240         # Coordenadas X do ponto gerador
    Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424         # Coordenadas Y do ponto gerador
    A, B = 0, 7                                                                                # Coeficientes da curva

    # Instanciar ECC com parâmetros menores
    ecc = EllipticCurveCryptography(p, n_order, Gx, Gy, A, B)

    # Definir uma chave privada (k)
    private_key = 1  # Exemplo de chave privada

    # Calculate public key point
    public_key_x, public_key_y = ecc.eccnP(private_key)

    # Exibir a chave pública
    print(f"Chave pública (x):       {public_key_x}")
    print(f"Chave pública (y):       {public_key_y}")
    #
    print(f"Chave pública Hex (x):   {hex(public_key_x)}")
    print(f"Chave pública Hex (y):   {hex(public_key_y)}")
    #
    print(f"in_curve?             => {ecc.in_curve(public_key_x, public_key_y)}")
    print(f"is_valid_private_key? => {ecc.is_valid_private_key(private_key)}")
