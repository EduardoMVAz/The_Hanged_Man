import pandas as pd
from Hangman import Hangman


class HangedMan:

    def __init__(self, words:pd.DataFrame):

        # inicializa o alfabeto para a contagem das letras
        self.alphabet = 'abcdefghijklmnopqrstuvwxyz'

        letter_counts = {}
        # para cada palavra da base de dados, faz a contagem de letras de cada uma
        for word in words['word']:
            counts = {i:0 for i in self.alphabet}
            # para cada letra da palavra, adiciona 1 na contagem
            for letter in word:
                counts[letter] += 1
            # salva a palavra em um dicionário
            letter_counts[word] = counts
        # dataframe que cada coluna é uma letra, e cada linha é uma palavra

        # transforma no dataframe que é a base de conhecimento do jogador
        self.df = pd.DataFrame.from_dict(letter_counts, orient='index')
            

    def guess(self, word:str):
        '''
        Função que encontra a letra mais frequente dentre as palavras que ainda podem ser a palavra secreta

        Parâmetros:
        word: palavra parcial que está sendo adivinhada

        Retorno:
        letter: letra mais frequente dentre as palavras que ainda podem ser a palavra secreta
        '''

        guessed_letters = [i for i in word if i != "-"]
        
        # retira as letras já chutadas
        df__ = self.df_.drop(guessed_letters, axis=1)
        lf = self.letter_frequencies(df__)

        # retorna a letra mais frequente
        letter = lf.idxmax()

        return letter
    

    def letter_frequencies(self, df_:pd.DataFrame):
        '''
        Função que calcula a frequência de cada letra dentre as palavras que ainda podem ser a palavra secreta

        Parâmetros:
        df_: dataframe que cada coluna é uma letra, e cada linha é uma palavra

        Retorno:
        letter_counts/total_letters: frequência de cada letra dentre as palavras que ainda podem ser a palavra secreta
        '''
        df_ = df_.reset_index(drop=True)
        letter_counts = df_.sum()
        total_letters = letter_counts.sum()

        return letter_counts/total_letters
    

    def count_same_place_letters(self, word1, word2):
        '''
        Função que conta quantas letras estão no mesmo lugar em duas palavras

        Parâmetros:
        word1: primeira palavra
        word2: segunda palavra

        Retorno:
        count: quantidade de letras que estão no mesmo lugar em duas palavras
        '''

        count = 0
        for i in range(len(word1)):
            if word1[i] == word2[i]:
                count += 1
        return count
    

    def find_incomplete_word(self, word):
        '''
        Função que encontra a palavra que mais se parece com a palavra parcial para poder fazer um chute

        Parâmetros:
        word: palavra parcial que está sendo adivinhada

        Retorno:
        final_word: palavra que mais se parece com a palavra parcial para chute
        '''

        # inicializa a contagem máxima e a palavra final
        max_count = 0
        final_word = ""

        # para cada palavra da base de dados, conta quantas letras estão no mesmo lugar
        for palavra in self.df_.index:
            count = self.count_same_place_letters(word, palavra)
            if count > max_count:
                max_count = count
                final_word = palavra

        return final_word


    def play(self, palavra=""):
        '''
        Função que joga o jogo da forca

        Parâmetros:
        palavra: palavra secreta

        Retorno:
        game.tentar_palavra(word): chute final do jogador
        '''

        # inicializa o jogo
        game = Hangman()
        game.novo_jogo(palavra=palavra.lower())
        
        # inicializa a palavra parcial
        word = ""
        for i in range(len(game.palavra)):
            word += "-"
        
        # inicializa o dataframe de palavras que ainda podem ser a palavra secreta, podando inicialmente pelo tamanho da palavra
        self.df_ = self.df[self.df.index.str.len() == len(word)]
        word = list(word)

        # enquanto o jogador ainda tem mais que 1 vida, pode chutar letras
        while game.vidas > 1:
            
            # se a palavra não tem mais traços, é porque o jogador encontrou a palavra
            if word.count("-") == 0:
                return game.tentar_palavra("".join(word))

            # chuta uma letra
            letter = self.guess(word)
            result = game.tentar_letra(letter)

            if result != False:
                # se a letra está na palavra, atualiza a palavra parcial e poda o dataframe de palavras que possuem essa letra
                if len(result) > 0:
                    for i in result:
                        word[i] = letter
                    self.df_ = self.df_[self.df_[letter] == len(result)]
                # se a letra não está na palavra, poda o dataframe de palavras mantendo as que não possuem essa letra
                else:
                    self.df_ = self.df_[self.df_[letter] == 0]

        # caso sobra apenas uma vida, ele chuta a mais provável parecida com a palavra parcial
        word = self.find_incomplete_word(word)
        
        return game.tentar_palavra(word) 




def main():
    '''
    Função principal que testa o jogo
    '''

    # Inicializa o dataframe de palavras
    df = pd.read_csv("br-sem-acentos.txt", header=None, names=['word'])
    df['word'] = df['word'].str.lower()
    hangedman = HangedMan(df)
    print(hangedman.play())

if __name__ == "__main__":
    main()