# The Hanged Man
## The hanged man is a computer program that plays the hangman game. It utilizes linear algebra concepts to try to win the game.

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

4. Após a instalação, visualize as informações e demonstrações no arquivo `demo.ipynb` para ver jogar e ver os testes feitos por nós.

---
<br/>

## Funcionamento do Jogo
O jogo é um jogo simples de forca, onde é escolhida uma palavra aleatória (existe a opção na nossa implementação de escolher a palavra para o jogador automático tentar advinhar, mas somente se a palavra está no banco de dados fornecido) e o jogador, sabendo somente o tamanho da palavra, deve chutar letras que vão sendo preenchidas nas suas posições na palavra, caso a palavra contenha a letra chutada. Toda vez que o jogador chuta uma letra que não está na palavra, ele perde uma vida. O jogador tem um número padrão de 5 vidas (que também pode ser alterado), e deve ou descobrir a palavra nessas 5 vidas, ou chutar uma palavra para tentar acertar e ganhar sem saber com certeza a palavra.

---
<br/>

## Implementação e Problemas Encontrados
### Implementação

Inicialmente, temos um banco de dados com 243 mil palavras. O programa então cria um dataframe, onde temos todas as palavras, e também a contagem das letras que aparecem em cada palavra. O jogo é iniciado, e a única informação que o jogador recebe é o tamanho da palavra. A partir disso, ele corta do dataframe todas as palavras que não tenham o mesmo tamanho. Depois desse setup, ele entra no seguinte loop, até acertar a palavra, ou suas vidas chegarem a 1:

* Chuta a letra mais frequente de todo o dataframe
* Verifica se a letra aparece na palavra, e quantas vezes a letra aparece na palavra
* Se a letra aparece na palavra, todas as palavras que não tenham a mesma quantidade dessa letra são removidas
* Se a letra não aparece na palavra, todas as palavras que possuem essa letra são removidas
* Se ele acertou a palavra, ou seja, todas as letras estão preenchidas, ele chuta a palavra
* Se as suas vidas chegaram a 1, ele sai do loop
* Recomeça o loop

Caso o jogador tenha acertado a palavra, o programa acaba aqui mesmo. Do contrário, sua última vida é usada no tudo ou nada, onde o programa percorre as palavras restantes no dataframe, procurando a palavra mais parecida com o que ele tem atualmente, ou seja, a palavra que tem mais letras no mesmo lugar do que a palavra correta semi-preenchida, e então chuta essa palavra.

O conceito fundamental da implementação é reduzir ao máximo as possibilidades, da mesma forma que a árvore de possibilidades funcionava, quando em sala praticamos com o baralho. Todo chute realizado pelo jogador diminui o dataframe, e como essa diminuição é feita a partir de similaridades entre as palavras (número específico da letra chutada, presença ou não da letra), os cortes no dataframe sempre aprocimam as palavras restantes da palavra correta, portanto a próxima letra a ser chutada tem uma chance maior de estar na palavra correta, pela semelhança das palavras restantes.

Essa implementação teve uma acurácia de aproximadamente 90%, como se pode ver após a realização de 1000 jogos (código no arquivo demo.ipynb).

### Problemas e Erro do Jogador

Para entender como o jogador pode errar e quais são os casos onde ele erra com mais frequência, precisamos ter em mente os fatores que **aumentam** a chance do jogador acertar uma palavra, e por consequência, os fatores que **diminuem** essa chance.

Os dois fatores mais importantes são o tamanho da palavra, e as vogais que ela possuí. Durante os testes, realizamos a contagem do número de palavras com cada tamanho, de 1 letra até 20, e entre 6 e 14 letras são os tamanhos mais frequentes de palavras. 

Sabendo que existem somente 5 mil palavras com 5 letras, e 35 mil com 11 letras e entendendo como funciona o algoritmo, é natural propor que seria mais fácil acertar uma palavra de 5 letras, mas é ai que o outro fator deve ser levado em consideração: As vogais e a construção das palavras em português. Como uma palavra menor tem menos letras, ela não pode ter muitas letras que a diferenciem das outras, e portanto, acaba que palavras menores possuem muitas letras em comum, o que dificulta a remoção de palavras do banco de dados. Uma palavra grande, porém com muitas letras diferentes, ou uma contagem incomum de letras, como salvaguardar por exemplo, que possuí 4 "a"s, é muito mais fácil para o algoritmo de advinhar. O principal fator de erro é esse: O jogador acaba caíndo muitas vezes na situação em que falta uma ou duas letras para acertar, mas como as palavras são muito parecidas, ele chuta uma errada. 

Outro fator observado nos teste é que existem letras extremamente incomuns em relação as outras. Fizemos a contagem da quantidade de vezes que cada letra aparece, e o "a", letra mais comum, aparece 359 mil vezes, enquanto o "k", "w" e "y" aparecem 22, 18 e 8 vezes, respectivamente, oq que torna palavras com essas letras mais dificeis de serem acertadas, pois o jogador dificilmente irá chutá-las.

Outro problema são palavras que tem somente a vogal "u", devido a ela ser a vogal menos comum, pois acompanhando o processo do programa jogando, é possível ver que ele sempre aposta primeiro nas vogais, até que palavras o suficiente tenham sido removidas da base de dados. Quando a palavra tem somente "u", porém, ele demora um pouco para começar a acertar as letras dessa palavra, o que pode levar a suas vidas a acabarem cedo demais, e ele ter pouca base para então chutar uma palavra no final.
