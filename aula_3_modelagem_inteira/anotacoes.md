# Aula 3 - Modelagem Inteira

## Índice

1. Introdução
2. Solução analítica / Método Gráfico
3. Funcionamento do Simplex
4. Solução no Solver do Excel


## 1. Introdução

Nesta aula, teremos um problema de programação linear que será resolvido de 3 formas:

* Forma analítica
* Simplex, de forma manual
* Solver do Excel

Vale ressaltar que, nessa aula, ignoraremos a restrição de que as variáveis devem ser inteiras. Por isso, vamos obter soluções com casas decimais.


## 2. Solução analítica / Método Gráfico

Seja o seguinte problema de programação linear:

$$
\begin{align*}

& Max Z = 3 \cdot x_1 + 3 \cdot x_2 \\
& s.a. \\
& x_1 + 4 \cdot x_2 <= 12 \\
& 6 \cdot x_1 + 4 \cdot x_2 <= 24 \\
& x_1, x_2 \text{ inteiros} 

\end{align*}
$$

Para resolvê-lo, primeiro precisamos traçar as duas retas das restrições.
Faremos isso encontrando 2 pontos pelos quais cada reta passa.
A forma mais simples de fazer isso é substituir $x_1 = 0$ para obter $x_2$ e vice-versa, em cada uma das equações envolvidas.

Com isso, obtemos que a primeira reta passa por $(0,3)$ e $(12,0)$, enquanto a segunda reta passa por $(0,6)$ e $(4,0)$.

Em segundo lugar, identificamos qual é o semiplano que satisfaz a restrição, em cada reta. Isto é, a reta divide o plano em $2$ partes, queremos achar qual parte satisfaz a desigualdade envolvida.

Para fazer isso, basta tomar qualquer ponto de um dos lados da reta. Se esse ponto satisfizer a restrição, então esse lado é o lado correto, se não, é o outro lado. Identificamos isso com uma seta em cada reta.

Fazendo isso, obtemos a região viável, que atende a todas as restrições, conforme a imagem abaixo:

![Alt text](solucao_analitica_1.png)

Igualando as equações das retas, conseguimos obter todos os pontos que são os vértices da região viável, como na imagem:

![Alt text](solucao_analitica_2.png)

Os vértices são:

* $A (0,0)$
* $B (0,3)$
* $C (2,4; 2,4)$
* $D (4,0)$

Já foi provado que a solução ótima é um dos vértices da região viável. Sendo assim, podemos seguir duas abordagens para encontrar a solução ótima:

1. Testar todos os pontos na função objetivo e ver qual deles a maximiza
2. Calcular o gradiente de $Z$: $Grad(Z) = (3,3)$; e ver qual vértice está em uma curva de nível maior, segundo o gradiente

De qualquer das duas formas, concluímos que o ponto $C (2,4; 2,4)$ é a solução ótima, que resulta em $Z = 14$.


## 3. Funcionamento do Simplex

Agora, vamos resolver exatamente o mesmo problema. Porém, seguindo o algoritmo do Simplex, para entender o seu funcionamento.

Para resolver um problema com o Simplex, precisamos colocar o problema na **Forma Padrão**:

* FO de Max
* $b \geq 0$ (RHS)
* $x \geq 0$
* Restrições de igualdade (variáveis de folga)

Voltemos ao problema:

$$
\begin{align*}

& Max Z = 3 \cdot x_1 + 3 \cdot x_2 \\
& s.a. \\
& x_1 + 4 \cdot x_2 <= 12 \\
& 6 \cdot x_1 + 4 \cdot x_2 <= 24 \\
& x_1, x_2 \text{ inteiros} 

\end{align*}
$$

A nossa FO já é de Maximizar. Se não fosse, teríamos que multiplicar a função por -1 para trocar.

As variáveis $x_1, x_2$ e os RHS's $12$ e $24$ já são maiores ou iguais a zero, então não precisaremos mexer nisso.

Porém, as nossas restrições não são de igualdade (são de desigualdade). Para corrigir isso, usaremos as **variáveis de folga** $x_3$ e $x_4$:

$$
\begin{align*}

& Max Z = 3 \cdot x_1 + 3 \cdot x_2 \\
& s.a. \\
& x_1 + 4 \cdot x_2 + x_3 = 12 \\
& 6 \cdot x_1 + 4 \cdot x_2 + x_4 = 24 \\
& x_1, x_2 >= 0

\end{align*}
$$

Uma vez que o problema já está na **Forma Padrão**, faremos o **Quadro Simplex Inicial**, onde inserimos os coeficienes e o valor da função objetivo. Vale ressaltar que os coeficientes da função objetivo devem ficar com **sinal invertido**:


| $x_1$ | $x_2$ | $x_3$ | $x_4$ | $Z$ |
|-------|-------|-------|-------|-----|
| -3    | -3    | 0     | 0     | 0   |
| 1     | 4     | 1     | 0     | 12  |
| 6     | 4     | 0     | 1     | 24  |

Quando temos uma solução para o problema, chamamos de **Solução Básica Factível (SBF)**.

Note que como temos 2 restrições, aparece uma matriz identidade 2x2 e, na linha da função objetivo, temos 2 zeros acima dessa identidade. Por isso, dizemos que temos uma **SBF**.

Começamos definindo $A = |B : N|$, onde:

$$
\begin{align*}

& B = (x_3, x_4) = (12, 24) \\
& N = (x_1, x_2) = (0, 0)

\end{align*}
$$

Onde $B$ é composto pelos vetores que **estão na base** e $N$ pelos vetores que **não estão na base**.

* **Pergunta:** estamos no valor ótimo? Como ainda temos valores negativos na linha da função objetivo, então **ainda não estamos no valor ótimo**

* **2 - Próximo passo:** escolhemos o valor **mais negativo** e dizemos que ele quer **entrar na base**. Como os dois valores negativos $x_1 = -3$ e $x_2 = -3$ são iguais, então vamos escolher qualquer um: vamos escolher $x_1$. Mas se o $x_1$ quer entrar na base, temos que tirar alguém, pois queremos uma base do $R^2$ porque temos $2$ restrições.

* **3 - Cálculo do Bloqueio:** dividimos o RHS pelo valor da coluna que quer entrar ($x_1$):

| $x_1$ | $x_2$ | $x_3$ | $x_4$ | $Z$ | Bloqueio |
|-------|-------|-------|-------|-----|----------|
| -3    | -3    | 0     | 0     | 0   |          |
| 1     | 4     | 1     | 0     | 12  | 12       |
| 6     | 4     | 0     | 1     | 24  | 4        |

$$Bloqueio = Min(b_i / a_{ij*}, a_{ij*} > 0)$$

Então $Bloqueio = 4$. O bloqueio serve para não sairmos da região viável. Na imagem abaixo, fica evidente que o vértice onde $x_1 = 4$ bloqueia para não sairmos da região viável.

![Alt text](solucao_analitica_2.png)

**Quem sai:** na linha do bloqueio, quem estiver com valor 1 dentre as colunas da base, sai. Ou seja, o $x_4$ sai.

* **4 - Pivoteamento:** queremos fazer operações com as linhas para incluir o $x_1$ na base.

Queremos deixar $L_2$ com 1 na coluna $x_1$. Para isso, fazemos a operação:

$$
L_2 = L_2 / 6
$$

Ficamos com a tabela:

| $x_1$ | $x_2$  | $x_3$ | $x_4$  | $Z$ |
|-------|--------|-------|--------|-----|
| -3    | -3     | 0     | 0      | 0   |
| 1     | 4      | 1     | 0      | 12  |
| 1     | 0,66667| 0     | 0,16667| 4   |

Em seguida, queremos zerar $L_1$ na coluna $x_1$, então fazemos a operação:

$$
L_1 = L_1 - 1 \cdot L_2
$$

| $x_1$ | $x_2$  | $x_3$ | $x_4$  | $Z$ |
|-------|--------|-------|--------|-----|
| -3    | -3     | 0     | 0      | 0   |
| 0     | 3,33333| 1     | 0,16667| 8   |
| 1     | 0,66667| 0     | 0,16667| 4   |

Queremos zerar $L_0$ na coluna $x_1$ também:

$$
L_0 = L_0 - (-3) \cdot L_2
$$

| $x_1$ | $x_2$  | $x_3$ | $x_4$   | $Z$ |
|-------|--------|-------|---------|-----|
| 0     | -1     | 0     | 0,5     | 12  |
| 0     | 3,33333| 1     | -0,16667| 8   |
| 1     | 0,66667| 0     | 0,16667 | 4   |

Ou seja, de forma geral, as operações entre linhas realizadas são, nessa ordem:

$$
\begin{align}

& L_2 = L_2 \cdot \dfrac{1}{Pivô(L_2)} \\
& L_1 = L_1 - Pivô(L_1) \cdot L_2 \\
& L_0 = L_0 - Pivô(L_0) \cdot L_2

\end{align}
$$

Agora, temos:

$$
\begin{align*}

& B = (x_3, x_1) = (8, 4) \\
& N = (x_4, x_2) = (0, 0)

\end{align*}
$$

Agora, finalizamos uma iteração do Simplex e conseguimos substituir todos os valores acima na forma padrão para verificar se está tudo certo.

Vamos para a próxima iteração.

1. O mais negativo na linha da FO entra na base: $x_2$ entrará na base.
2. Calcula-se os bloqueios usando o RHS e os valores da coluna $x_2$:

| $x_1$ | $x_2$  | $x_3$ | $x_4$   | $Z$ | Bloqueio |
|-------|--------|-------|---------|-----|----------|
| 0     | -1     | 0     | 0,5     | 12  |          |
| 0     | 3,33333| 1     | -0,16667| 8   | 2,4      |
| 1     | 0,66667| 0     | 0,16667 | 4   | 6        |

A linha $L_1$ tem o menor bloqueio, então procuramos - na $L_1$ - qual elemento da base tem entrada igual a 1: é o $x_3$. Então o $x_3$ sairá da base.

3. Agora, resta fazer o pivoteamento:

$$L_1 = L1 \cdot \dfrac{1}{3,33333}$$

| $x_1$ | $x_2$  | $x_3$ | $x_4$   | $Z$ |
|-------|--------|-------|---------|-----|
| 0     | -1     | 0     | 0,5     | 12  |
| 0     | 1      | 0,3   | -0,005  | 2,4 |
| 1     | 0,66667| 0     | 0,16667 | 4   |

$$L_0 = L0 - (-1) \cdot L_1$$

| $x_1$ | $x_2$  | $x_3$ | $x_4$   | $Z$ |
|-------|--------|-------|---------|-----|
| 0     | 0      | 0,3   | 0,495   | 14,4|
| 0     | 1      | 0,3   | -0,005  | 2,4 |
| 1     | 0,66667| 0     | 0,16667 | 4   |

$$L_2 = L2 - (0,66667) \cdot L_1$$

| $x_1$ | $x_2$  | $x_3$ | $x_4$   | $Z$ |
|-------|--------|-------|---------|-----|
| 0     | 0      | 0,3   | 0,495   | 14,4|
| 0     | 1      | 0,3   | -0,005  | 2,4 |
| 1     | 0      | -0,2  | 0,2     | 2,4 |

Ficamos com:

$$
\begin{align*}

& B = (x_2, x_1) = (2,4; 2,4) \\
& N = (x_4, x_3) = (0, 0)

\end{align*}
$$

Verificando a forma padrão, os valores estão corretos.

Agora, note que não temos mais valores negativos na linha da FO, isso quer dizer que - a partir de agora - outras soluções não trarão valores maiores do que o já obtido. Isto é, encontramos a solução ótima: $(2,4;2,4)$.


## 4. Solver do Excel

Ver aula.