import pandas as pd
import numpy as np
import math
import time
import gurobipy as gp
from gurobipy import GRB


def calcula_distancias_rota_para_nao_visitados_ex2(rota, lista_nao_visitados, df_copy):
    distancias_rota_para_nao_visitados = {}
    for i in rota:
        for j in lista_nao_visitados:
            distancias_rota_para_nao_visitados[(i, j)] = df_copy.loc[i, str(j)]
    return distancias_rota_para_nao_visitados


def calcular_distancia_total_ex2(df, rota):
    # Calcula a distância total de uma rota dada
    distancia_total = 0
    for i in range(len(rota) - 1):
        ponto_a = rota[i]
        ponto_b = rota[i+1]
        distancia_total += df.loc[ponto_a, str(ponto_b)]
    return distancia_total


def procura_melhor_posicao_ex2(rota, proximo_ponto, df):
    # Inserção exaustiva para encontrar a melhor posição, começando após o ponto zero
    melhor_distancia = float('inf')
    melhor_posicao = None
    # Mantemos o 0 no início e no final
    for i in range(1, len(rota)):
        nova_rota = rota.copy()
        nova_rota.insert(i, proximo_ponto)
        nova_distancia = calcular_distancia_total_ex2(df, nova_rota)
        if nova_distancia < melhor_distancia:
            melhor_distancia = nova_distancia
            melhor_posicao = i
    return melhor_posicao


def busca_rota_mais_economica_ex2(rota, df, lista_nao_visitados):
    melhor_distancia = float('inf')
    for ponto in lista_nao_visitados:
        for i in range(1, len(rota)):
            nova_rota = rota.copy()
            nova_rota.insert(i, ponto)
            nova_distancia = calcular_distancia_total_ex2(df, nova_rota)
            if nova_distancia < melhor_distancia:
                melhor_distancia = nova_distancia
                melhor_rota = nova_rota.copy()
                proximo_ponto = ponto
                print(f'Rota {melhor_rota} - FO {round(melhor_distancia,2)} (nova melhor rota!)')
            else:
                print(f'Rota {nova_rota} - FO {round(nova_distancia,2)}')
    return melhor_rota, proximo_ponto


def atualiza_rota_ex2(rota, tipo, df, lista_nao_visitados, distancias_rota_para_nao_visitados):
    if tipo in [0,1]:
        proximo_ponto = encontrar_proximo_ponto(distancias_rota_para_nao_visitados, tipo)
        melhor_posicao = procura_melhor_posicao_ex2(rota, proximo_ponto, df)
        # Inserir o ponto na melhor posição
        rota.insert(melhor_posicao, proximo_ponto)
    if tipo == 2:
        rota, proximo_ponto = busca_rota_mais_economica_ex2(rota, df, lista_nao_visitados)
    return rota, proximo_ponto


def heuristica_insercao_ex2(df, tipo=0):
    """Implementa a heurística do vizinho mais próximo para um DataFrame de pontos.

    Args:
        df (pd.DataFrame): DataFrame com as colunas 'ponto', 'x' e 'y'.

    Returns:
        list: Lista com a ordem dos pontos na rota encontrada.
    """
    inicio = time.time()
    # Criar uma cópia do DataFrame para não modificar o original
    df_copy = df.copy()

    # Obter o número de pontos
    num_pontos = len(df_copy)

    # Iniciar a rota com um ponto aleatório
    ponto_atual = 0
    rota = [ponto_atual]

    # Marcar o ponto atual como visitado
    df_copy['visitado'] = [False]*len(df_copy)
    df_copy.loc[ponto_atual, 'visitado'] = True

    iter = 1
    # Construir a rota
    while len(rota) <= num_pontos:
        print(f'---------- ITERAÇÃO {iter} ----------')

        # Calcular todas as distâncias entre pontos na rota e pontos não visitados
        lista_nao_visitados = list(df_copy[df_copy['visitado'] == False]['ponto'])
        distancias_rota_para_nao_visitados = calcula_distancias_rota_para_nao_visitados_ex2(rota, lista_nao_visitados, df_copy)

        # Primeira iteração: sempre escolher o mais próximo
        if iter == 1:
            proximo_ponto = encontrar_proximo_ponto(distancias_rota_para_nao_visitados, tipo=0)
            print(f'Escolhido: {proximo_ponto}')
            rota = [0, proximo_ponto, 0]
        # Demais iterações: seguir a regra do tipo
        else:
            rota, proximo_ponto = atualiza_rota_ex2(rota, tipo, df, lista_nao_visitados, distancias_rota_para_nao_visitados=distancias_rota_para_nao_visitados)
            print(f'Escolhido: {proximo_ponto}')

        
        df_copy.loc[proximo_ponto, 'visitado'] = True
        ponto_atual = proximo_ponto
        iter = iter + 1
        fo_parcial = calcular_distancia_total_ex2(df, rota)
        print(f'Rota: {rota}')
        print(f'FO: {round(fo_parcial,2)}\n')

    fo_final = round(calcular_distancia_total_ex2(df, rota),2)
    print('---------- SOLUÇÃO ÓTIMA ----------')
    print(f'Rota final: {rota}')
    print(f'FO final: {fo_final}')
    fim = time.time()
    tempo_execucao = round(fim - inicio, 2)

    return rota, fo_final, tempo_execucao


def distancia_euclidiana_mtz(coord1, coord2):
    # Calcula a distância euclidiana entre dois pontos
    x1, y1 = coord1['x'], coord1['y']
    x2, y2 = coord2['x'], coord2['y']
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5


def rota_dict_para_lista(qtd_pontos, grafo, no_inicial):
    """
    Constrói a rota do caixeiro viajante a partir do grafo representado por um dicionário.

    Args:
        grafo: Dicionário representando o grafo, onde as chaves são as arestas e os valores são 0 ou 1.
        no_inicial: Nó inicial da rota.

    Returns:
        Lista representando a rota do caixeiro viajante.
    """

    rota = [no_inicial]
    visitados = set()
    visitados.add(no_inicial)

    while len(visitados) < qtd_pontos:
        for vizinho in grafo:
            u, v = vizinho
            if u == rota[-1] and v not in visitados and grafo[vizinho] == 1:
                rota.append(v)
                visitados.add(v)
                break
    rota.append(no_inicial)

    return rota


def caixeiro_viajante_mtz(df=pd.DataFrame(), silent=True, dist_matrix = {}):
    inicio = time.time()

    if dist_matrix == {}:
        qtd_pontos = len(df)
        V = set(list(range(int(qtd_pontos))))
        E = gp.tuplelist([(i, j) for i in V for j in V if i != j])
        # Criar um dicionário de coordenadas
        coords = df.set_index('ponto')[['x', 'y']].to_dict('index')
        # Calcular a matriz de distâncias
        for i, j in E:
            dist_matrix[i, j] = distancia_euclidiana_mtz(coords[i], coords[j])
        
    else:
        qtd_pontos = (len(dist_matrix))**0.5
        V = set(list(range(int(qtd_pontos))))
        E = gp.tuplelist([(i, j) for i in V for j in V if i != j])

    m = gp.Model("Caixeiro_Viajante_MTZ")
    if silent:
        m.setParam(GRB.Param.OutputFlag, 0)
    ######### BEGIN: Write here your model for Task 1
    ## Vars
    x = m.addVars(E, vtype=GRB.BINARY)  # 1 if we drive from city i to city j, else 0
    u = m.addVars(V, vtype=GRB.CONTINUOUS, lb=0) # Number of cities visited at city i
    
    ## Objective
    m.setObjective(gp.quicksum(dist_matrix[i, j] * x[i, j] for i, j in E), GRB.MINIMIZE)
    
    ## Restrições padrões do Caixeiro Viajante
    for j in V:
        m.addConstr(gp.quicksum([x[i, j] for i, _ in E.select("*", j)]) == 1)

    for i in V:
        m.addConstr(gp.quicksum([x[i, j] for _, j in E.select(i, "*")]) == 1)
    
    
    # Restrições de subrotas
    n = len(V)
    for i, j in E.select("*", "*"):
        if (i != 0 and j != 0):
            m.addConstr(u[i] - u[j] + n * x[i, j] <= n - 1)
            #m.addConstr(u[j] >= u[i] + 1 - (n) * (1 - x[i, j]))
    m.addConstr(u[0] == 1)

    # Salva e resolve
    #m.display()
    m.write("caixeiro_viajante_mtz.lp")
    m.optimize()
    
    if m.status == GRB.status.OPTIMAL:
        fo_final = m.objVal
        # Criar lista vazia para armazenar a rota
        rota_dict = {e: x[e].X for e in E}
        rota = rota_dict_para_lista(qtd_pontos=qtd_pontos, grafo=rota_dict, no_inicial=0)
        print(f'Rota: {rota}')
        print(f'FO: {round(fo_final,2)}')
        fim = time.time()
        tempo_execucao = round(fim - inicio, 2)
        print(f'Tempo de execução: {tempo_execucao}')
        return rota, fo_final, tempo_execucao
    else:
        print("Não foi possível resolver o problema")
        raise SystemExit


def distancia_euclidiana(x1, y1, x2, y2):

  distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
  return distancia


def calcular_distancia_total(df, rota):
    # Calcula a distância total de uma rota dada
    distancia_total = 0
    for i in range(len(rota) - 1):
        ponto_a = rota[i]
        ponto_b = rota[i+1]
        distancia_total += np.sqrt((df.loc[ponto_a, 'x'] - df.loc[ponto_b, 'x'])**2 +
                                  (df.loc[ponto_a, 'y'] - df.loc[ponto_b, 'y'])**2)
    return distancia_total


def encontrar_proximo_ponto(distancias_rota_para_nao_visitados, tipo):
    """Encontra o próximo ponto a ser adicionado à rota.

    Args:
        distancias_rota_para_nao_visitados (dict): Dicionário contendo as distâncias entre os pontos na rota e os pontos não visitados.
        tipo (int): 0 para encontrar a menor distância, 1 para encontrar a maior.

    Returns:
        int: Índice do próximo ponto a ser adicionado à rota.
    """

    if tipo == 0:
        # Encontrar a menor distância
        return min(distancias_rota_para_nao_visitados, key=distancias_rota_para_nao_visitados.get)[1]
    if tipo == 1:
        # Encontrar a maior distância
        return max(distancias_rota_para_nao_visitados, key=distancias_rota_para_nao_visitados.get)[1]
    

def procura_melhor_posicao(rota, proximo_ponto, df):
    # Inserção exaustiva para encontrar a melhor posição, começando após o ponto zero
    melhor_distancia = float('inf')
    melhor_posicao = None
    # Mantemos o 0 no início e no final
    for i in range(1, len(rota)):
        nova_rota = rota.copy()
        nova_rota.insert(i, proximo_ponto)
        nova_distancia = calcular_distancia_total(df, nova_rota)
        if nova_distancia < melhor_distancia:
            melhor_distancia = nova_distancia
            melhor_posicao = i
    return melhor_posicao


def busca_rota_mais_economica(rota, df, lista_nao_visitados):
    melhor_distancia = float('inf')
    for ponto in lista_nao_visitados:
        for i in range(1, len(rota)):
            nova_rota = rota.copy()
            nova_rota.insert(i, ponto)
            nova_distancia = calcular_distancia_total(df, nova_rota)
            if nova_distancia < melhor_distancia:
                melhor_distancia = nova_distancia
                melhor_rota = nova_rota.copy()
                proximo_ponto = ponto
                print(f'Rota {melhor_rota} - FO {round(melhor_distancia,2)} (nova melhor rota!)')
            else:
                print(f'Rota {nova_rota} - FO {round(nova_distancia,2)}')
    return melhor_rota, proximo_ponto


def calcula_distancias_rota_para_nao_visitados(rota, lista_nao_visitados, df_copy):
    distancias_rota_para_nao_visitados = {}
    for i in rota:
        for j in lista_nao_visitados:
            distancias_rota_para_nao_visitados[(i, j)] = np.sqrt((df_copy.loc[i, 'x'] - df_copy.loc[j, 'x'])**2 +
                                                            (df_copy.loc[i, 'y'] - df_copy.loc[j, 'y'])**2)
    return distancias_rota_para_nao_visitados


def atualiza_rota(rota, tipo, df, lista_nao_visitados, distancias_rota_para_nao_visitados):
    if tipo in [0,1]:
        proximo_ponto = encontrar_proximo_ponto(distancias_rota_para_nao_visitados, tipo)
        melhor_posicao = procura_melhor_posicao(rota, proximo_ponto, df)
        # Inserir o ponto na melhor posição
        rota.insert(melhor_posicao, proximo_ponto)
    if tipo == 2:
        rota, proximo_ponto = busca_rota_mais_economica(rota, df, lista_nao_visitados)
    return rota, proximo_ponto


def heuristica_insercao(df, tipo=0):
    """Implementa a heurística do vizinho mais próximo para um DataFrame de pontos.

    Args:
        df (pd.DataFrame): DataFrame com as colunas 'ponto', 'x' e 'y'.

    Returns:
        list: Lista com a ordem dos pontos na rota encontrada.
    """
    inicio = time.time()
    # Criar uma cópia do DataFrame para não modificar o original
    df_copy = df.copy()

    # Obter o número de pontos
    num_pontos = len(df_copy)

    # Iniciar a rota com um ponto aleatório
    ponto_atual = 0
    rota = [ponto_atual]

    # Marcar o ponto atual como visitado
    df_copy['visitado'] = [False]*len(df_copy)
    df_copy.loc[ponto_atual, 'visitado'] = True

    iter = 1
    # Construir a rota
    while len(rota) <= num_pontos:
        print(f'---------- ITERAÇÃO {iter} ----------')

        # Calcular todas as distâncias entre pontos na rota e pontos não visitados
        lista_nao_visitados = list(df_copy[df_copy['visitado'] == False]['ponto'])
        distancias_rota_para_nao_visitados = calcula_distancias_rota_para_nao_visitados(rota, lista_nao_visitados, df_copy)

        # Primeira iteração: sempre escolher o mais próximo
        if iter == 1:
            proximo_ponto = encontrar_proximo_ponto(distancias_rota_para_nao_visitados, tipo=0)
            print(f'Escolhido: {proximo_ponto}')
            rota = [0, proximo_ponto, 0]
        # Demais iterações: seguir a regra do tipo
        else:
            rota, proximo_ponto = atualiza_rota(rota, tipo, df, lista_nao_visitados, distancias_rota_para_nao_visitados=distancias_rota_para_nao_visitados)
            print(f'Escolhido: {proximo_ponto}')

        
        df_copy.loc[proximo_ponto, 'visitado'] = True
        ponto_atual = proximo_ponto
        iter = iter + 1
        fo_parcial = calcular_distancia_total(df, rota)
        print(f'Rota: {rota}')
        print(f'FO: {round(fo_parcial,2)}\n')

    fo_final = round(calcular_distancia_total(df, rota),2)
    print('---------- SOLUÇÃO ÓTIMA ----------')
    print(f'Rota final: {rota}')
    print(f'FO final: {fo_final}')
    fim = time.time()
    tempo_execucao = round(fim - inicio, 2)

    return rota, fo_final, tempo_execucao


def pega_subrotas(grafo, qtd_pontos):
    inicial = 0
    atual = inicial
    subrotas = []
    subrota = [inicial]
    visitados = set()


    while len(visitados) < qtd_pontos:
        for origem, destino in grafo:
            #print(f'(origem, destino) = ({origem}, {destino})')
            if origem == atual:
                if grafo[origem, destino] == 1:
                    visitados.add(destino)
                    atual = destino
                    subrota.append(atual)
                    #print(subrota)
                    if atual == inicial:
                        subrotas.append(subrota)
                        nao_visitados = set(range(int(qtd_pontos))) - visitados
                        if len(nao_visitados) > 0:
                            inicial = min(nao_visitados)
                            subrota = [inicial]
                            atual = inicial
                        #print(subrotas)
    return subrotas


def calcula_variaveis_caixeiro(df=pd.DataFrame(), dist_matrix = {}):

    if dist_matrix == {}:
        qtd_pontos = len(df)
        
        V = set(list(range(int(qtd_pontos))))
        E = gp.tuplelist([(i, j) for i in V for j in V if i != j])
        # Criar um dicionário de coordenadas
        coords = df.set_index('ponto')[['x', 'y']].to_dict('index')
        # Calcular a matriz de distâncias
        for i, j in E:
            dist_matrix[i, j] = distancia_euclidiana_mtz(coords[i], coords[j])
        
    else:
        qtd_pontos = (len(dist_matrix))**0.5
        V = set(list(range(int(qtd_pontos))))
        E = gp.tuplelist([(i, j) for i in V for j in V if i != j])

    return qtd_pontos, V, E, dist_matrix


def caixeiro_viajante_bb(df=pd.DataFrame(), silent=True, dist_matrix = {}):
    inicio = time.time()
    qtd_pontos, V, E, dist_matrix_inicial = calcula_variaveis_caixeiro(df=df, dist_matrix=dist_matrix)
    big_m = 99999
    iter = 0
    numero_ultimo_problema = 0
    melhor_bound = np.inf
    dict_bb_anteriores = {}
    custos = []
    dict_bb_proximos = {
        iter: {'subrota_alvo': []
            ,'custos': custos}
    }


    while len(dict_bb_proximos) > 0 and iter < 200:

        
        custos_atuais = dict_bb_proximos[iter]['custos']

        print(f'\n---------- ITERAÇÃO {iter} ----------')
        print(f'Melhor bound anterior: {melhor_bound}')
        print(f"Subrota alvo: {dict_bb_proximos[iter]['subrota_alvo']}")
        print(f"Custos alterados: {custos_atuais}")
        print(f'Faltantes: {len(dict_bb_proximos) - 1}')
        print(dict_bb_proximos)
        #print(f'Próximos no início da iter: {dict_bb_proximos}')

        # Atualiza os custos
        dist_matrix_atual = dist_matrix_inicial
        for i,j in dict_bb_proximos[iter]['custos']:
            dist_matrix_atual[i,j] = big_m
        #print(f'{iter} - Custos atualizados')
        
        # Cria o modelo da iteração
        nome = f"caixeiro_viajante_bb_{iter}"
        m = gp.Model(nome)
        if silent:
            m.setParam(GRB.Param.OutputFlag, 0)
        x = m.addVars(E, vtype=GRB.BINARY)  # 1 se o caixeiro vai de i para j, 0 caso contrário
        u = m.addVars(V, vtype=GRB.CONTINUOUS, lb=0) # Number of cities visited at city i (?????????)
        m.setObjective(gp.quicksum(dist_matrix_atual[i, j] * x[i, j] for i, j in E), GRB.MINIMIZE)
        for j in V:
            m.addConstr(gp.quicksum([x[i, j] for i, _ in E.select("*", j)]) == 1)
        for i in V:
            m.addConstr(gp.quicksum([x[i, j] for _, j in E.select(i, "*")]) == 1)
        m.write(f"caixeiro_viajante_bb/{nome}.lp")
        m.optimize()
        #print(f'{iter} - Modelo criado')
        
        # Se o problema for viável, armazena a fo e a rota e atualiza o dict_bb_anteriores
        if m.status == GRB.status.OPTIMAL:
            #print(f'{iter} - Solução encontrada')
            fo_atual = m.objVal
            print(f'FO: {round(fo_atual,0)}')
            dict_subrotas_atual = {e: x[e].X for e in E}
            #print(f'{iter} - rota_dict_atual: {dict_subrotas_atual}')
            subrotas_atual = pega_subrotas(grafo=dict_subrotas_atual, qtd_pontos=qtd_pontos)
            print(f'Subrotas: {subrotas_atual}')
            #print(f'Rota: {rota_atual}')
            #print(f'FO: {round(fo_atual,2)}')
            dict_bb_anteriores[iter] = {
                'fo_atual': fo_atual
                ,'melhor_bound_anterior': melhor_bound
                ,'custos': dict_bb_proximos[iter]['custos']
                ,'rota': subrotas_atual
            }

        # Se o problema não for viável, atualiza o dict_bb_anteriores
        else:
            print(f"Problema inviável")
            dict_bb_anteriores[iter] = {
                'fo_atual': None
                ,'melhor_bound_anterior': melhor_bound
                ,'custos': None
                ,'rota': None
            }
            #raise SystemExit

        # Remove o problema resolvido do dict_bb_proximos
        dict_bb_proximos.pop(iter)
        
        # Se a rota atual tiver subrotas, devem ser adicionados novos nós no dict_bb_proximos
        if len(subrotas_atual) > 1:

            # Seleciona qual é a menor subrota
            tamanho_menor_subrota = np.inf
            for subrota in subrotas_atual:
                tamanho_subrota = len(subrota)
                if tamanho_subrota < tamanho_menor_subrota:
                    tamanho_menor_subrota = tamanho_subrota
                    menor_subrota = subrota

            # Seleciona quais custos devem ser alterados para restringir a menor subrota e adiciona os próximos problemas no dict_bb_proximos
            menor_subrota_sem_dups = list(set(menor_subrota))
            for ponto1 in menor_subrota_sem_dups:
                custos_novos = []
                for ponto2 in menor_subrota_sem_dups:
                    if ponto1 != ponto2:
                        custos_novos.append((ponto1, ponto2))
                numero_ultimo_problema = numero_ultimo_problema + 1
                custos_empilhados = custos_atuais + custos_novos
                dict_bb_proximos[numero_ultimo_problema] = {
                    'subrota_alvo': menor_subrota
                    ,'custos': custos_empilhados}
                        
        # Se a rota atual não tiver subrotas e a FO for melhor que o melhor_bound, o melhor_bound deve ser atualizado
        elif fo_atual < melhor_bound:
            melhor_bound = fo_atual

        #print(f'Próximos no final da iter: {dict_bb_proximos}')
        
        # Incrementamos a iteração
        iter = iter + 1

    fim = time.time()
    tempo_execucao = round(fim - inicio, 2)
    print(f'Tempo de execução: {tempo_execucao}')
    return dict_bb_anteriores, tempo_execucao