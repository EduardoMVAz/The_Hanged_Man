# The Hanged Man
## The hanged man is a computer program that plays the hangman game. It utilizes an adaptation of the linear algebra concepts of entropy and decision trees to try to maximize its winning rate.

Developers:

* João Lucas de Moraes Barros Cadorniga [JoaoLucasMBC](https://github.com/JoaoLucasMBC)  
* Eduardo Mendes Vaz [EduardoMVaz](https://github.com/EduardoMVAz)

This repository is an implementation of a Hangman player, a program that utilizes linear algebra concepts such as the huffman tree to play Hangman. 

---
<br/>

## Como Instalar & Utilizar

Para utilizar o projeto <em>"The Hanged Man"</em>, você deve ter o Python instalado em seu computador e seguir os passos:

1. Clone o repositório na sua máquina na pasta de sua escolha. Utilize o comando:

`git clone https://github.com/EduardoMVAz/The_Hanged_Man.git`

2. Utilizando o terminal / a IDE de sua escolha, crie uma *Virtual Env* de Python e a ative:

`python -m venv env`

`env/Scripts/Activate.ps1` (Windows)

3. Mude para a pasta do <em>"The Hanged Man"</em> e instale as bibliotecas requeridas:

`cd ./The_Hanged_Man`

`pip install -r requirements.txt`

4. Após a instalação, visualize as informações e demonstrações no arquivo `demo.ipynb`, célula a célula, para ver o jogador e ver os testes feitos por nós.

---
<br/>

## 1. **Funcionamento do Jogo**
O jogo é uma simples implementação de forca, no qual é escolhida uma palavra aleatória (existe a opção na nossa implementação de escolher a palavra para o jogador automático tentar advinhar, mas somente se a palavra está no banco de dados fornecido¹) e o jogador, sabendo somente o tamanho da palavra, deve chutar letras que vão sendo preenchidas nas suas posições na palavra, caso a palavra contenha a letra chutada. Toda vez que o jogador chuta uma letra que não está na palavra, ele perde uma vida. O jogador tem um número padrão de 5 vidas (que também pode ser alterado), e deve ou descobrir a palavra nessas 5 vidas, ou chutar uma palavra para tentar acertar e ganhar sem saber com certeza a palavra.

¹[Banco de Dados de Palavras](https://www.ime.usp.br/~pf/dicios/br-sem-acentos.txt)

---
<br/>

## 2. **Implementação e Problemas Encontrados**  
### 2.1. *Implementação*

Inicialmente, temos um banco de dados com 243 mil palavras. O programa então cria um dataframe para servir como "base de conhecimento" do jogador, onde se encontram como índices todas as palavras, enquanto cada coluna é uma letra. Portanto, cada célula representa a contagem das letras que aparecem em cada palavra. 

Então, o jogo é iniciado e a única informação que o jogador recebe é o tamanho da palavra (como em um jogo usual de forca). A partir disso, ele poda inicialmente o *dataframe* retirando todas as palavras que não tenham o mesmo tamanho, já que elas não podem ser a palavra correta. Depois desse *setup*, ele entra no seguinte loop de passos para reduzir ainda mais o seu rol de possibilidades, até ou acertar a palavra, ou suas vidas chegarem a 1:

1. Chuta a **letra mais frequente** de todo o dataframe;
2. Verifica se a letra aparece na palavra, e quantas vezes a letra aparece na palavra;
3. Se a letra aparece na palavra, **todas as palavras que não tenham a mesma quantidade dessa letra são removidas**;
4. Se a letra não aparece na palavra, **todas as palavras que possuem essa letra são removidas**;
5. Se ele acertou a palavra, ou seja, todas as letras estão preenchidas, ele chuta a própria palavra;
6. Se as suas vidas chegaram a 1, ele sai do loop;
7. Recomeça o loop.

Caso o jogador tenha já encontrado a palavra completa, o programa acaba aqui mesmo. Do contrário, **sua última vida é usada em um *all-in***: o programa percorre as palavras restantes no dataframe, procurando a palavra mais parecida com o que ele tem atualmente, ou seja, **a palavra que tem mais letras no mesmo lugar do que a palavra correta semi-preenchida**, e então a utiliza como chute final.

O conceito fundamental da implementação é reduzir ao máximo as possibilidades, da mesma forma que a **árvore de possibilidades funcionava**, quando em um jogo de adivinhação com baralho. Todo chute realizado pelo jogador diminui o dataframe, e como essa diminuição é feita a partir de similaridades entre as palavras (número específico da letra chutada, presença ou não da letra), os cortes no dataframe sempre aprocimam as palavras restantes da palavra correta, e, portanto, a próxima letra a ser chutada tem uma chance maior de estar na palavra correta, pela semelhança das palavras restantes.

Assim, a estratégia utilizada pelo jogador se assemelha ao conceito de ***entropia***. Cada chute busca recuperar *o máximo de informação do sistema*, ou seja, diminuir a entropia total, se aproximando cada vez mais da palavra correta. Ao invés de implementar diretamente uma árvore de decisão, ele utiliza do dataframa e as *frequências* de cada letra para escolher a **pergunta mais útil**, isto é, a letra mais provável de estar na palavra, ou, pela lógica inversa, que também mais eliminará possibilidades caso não se encontre na resposta correta.

Essa implementação teve uma acurácia de aproximadamente 90%, como se pode ver após a realização de 1000 jogos (código no arquivo `demo.ipynb`).

### 2.2. *Problemas e Erros do Jogador*

Para entender como o jogador pode errar e quais são os casos onde ele erra com mais frequência, precisamos ter em mente os fatores que **aumentam** a chance do jogador acertar uma palavra, e, por consequência, os fatores que **diminuem** essa chance.

Os dois fatores mais importantes são: 

A. O tamanho da palavra;  
B. E as vogais que ela possuí. 

Durante os testes, realizamos a contagem do número de palavras com cada tamanho, de 1 letra até 20, e **entre 6 e 14 letras são os tamanhos mais frequentes de palavras**. 

Sabendo que existem *somente 5 mil palavras com 5 letras, e 35 mil com 11 letras* na base de dados, e entendendo como funciona o algoritmo, é natural propor que seria mais fácil acertar uma palavra de 5 letras. No entanto, ness momento o outro fator deve ser levado em consideração: **as vogais e a construção das palavras em português**. Como uma palavra menor tem menos letras, ela não pode ter muitas letras que a diferenciem das outras, e, portanto, acaba que *palavras menores tendem a possuir muitas letras em comum*, o que dificulta a remoção de palavras do banco de dados. 

Uma palavra grande, porém com muitas letras diferentes, ou uma contagem incomum de letras, como `salvaguardar`, que possuí 4 "a"s, é muito mais fácil para o algoritmo de advinhar. Após chutar a vogal "a" e então as consoantes mais comuns, "r" e "s", quase nenhuma palavra tem essa mesma combinação atual no banco, facilitando o chute.

O principal fator de erro é esse: O jogador acaba caíndo muitas vezes na situação em que falta uma ou duas letras para acertar, mas como as palavras são muito parecidas, ele chuta uma errada. Um exemplo prático seria entre as palavras `PEDRO` e `PEDRA`. Caso o algoritmo chegue na palavra parcial **PEDR-** e não tenha mais chutes, é impossível diferenciar entre as duas, portanto, sua chance de erro é maior com um "chute cego".

Outro fator observado nos testes é que existem letras extremamente incomuns em relação as outras. Ao realizar a contagem da frequência de cada letra, o "a", letra mais comum, aparece 359 mil vezes, enquanto o "k", "w" e "y" aparecem 22, 18 e 8 vezes, respectivamente, dentre as centenas de milhares de palavras, o que torna palavras com essas letras mais dificeis de serem acertadas, pois o jogador dificilmente irá chutá-las com um método voltado à frequência.

Mais um problema são palavras que possuem vogais, mas apenas as mais "incomuns", como "u". Acompanhando o processo do programa, é possível ver que ele sempre aposta primeiro nas vogais mais frequentes ("a", "e", "i" e "o"), até que palavras o suficiente tenham sido removidas da base de dados e ele possa começar a escolher consoantes. Quando a palavra tem somente "u", porém, ele demora um pouco para começar a acertar as letras dessa palavra, o que pode levar a suas vidas a acabarem cedo demais e ele ter pouco conhecimento, ou seja, pouca entropia foi removida do sistema, para então chutar uma palavra final.
