from model.model import Model

model = Model()

model.creaGrafo(7.4, 7.8)
print('Grafo correttamente creato')

nodi, archi = model.getInfo() #Questa formattazione può variare in base all'esempio
print(f'Numero di nodi: {nodi}')
print(f'Numero di archi: {archi}')

print()
best = model.getBestArchi()
print(f'Top 5 archi:')
for b in best:
    print(f'{b[0]} -> {b[1]} : {b[2]['weight']}')
print()
num, conn = model.getCompConn()
print(f'Il grafo ha {num} componenti connesse')
print(f'La più grande componente connessa è lunga {len(conn)}')
for b in conn:
    print(f'{b}')

print()
cammino, lunghezza = model.getCamminoOttimo()

print(f'Ho trovato un cammino lungo {lunghezza}')
for b in cammino:
    print(f'{b}')