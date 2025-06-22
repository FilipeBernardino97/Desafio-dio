class bicicleta:
    def __init__(self, cor, modelo, ano, valor):
        self.cor = cor
        self. modelo = modelo
        self. ano = ano
        self.valor = valor

    def buzinar(self):
        print( "bibi")
    
    def parar(self):
        print("parando bicicleta...")
        print("bicicleta parada!")

    def correr(self):
        print("VRUMMMMM..")    

b1 = bicicleta("vermelha", "caloi", 2022, 1000)
b1. buzinar()
b1. correr()
b1. parar()
print(b1.cor, b1.modelo, b1.ano, b1.valor)
