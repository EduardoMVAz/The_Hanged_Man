import pandas as pd
from Hangman import Hangman

class HangedMan:

    def __init__(self, words:pd.DataFrame):
        self.alphabet = 'abcdefghijklmnopqrstuvwxyz'

        letter_counts = {}
        for word in words['word']:
            counts = {i:0 for i in self.alphabet}
            for letter in word:
                counts[letter] += 1
            letter_counts[word] = counts
        # dataframe que cada coluna é uma letra, e cada linha é uma palavra

        self.df = pd.DataFrame.from_dict(letter_counts, orient='index')
            

    def guess(self, word:str):
        # acha a letra mais frequente e chuta

        guessed_letters = [i for i in word if i != "-"]
        df_ = self.df.drop(guessed_letters, axis=1)
        lf = self.letter_frequencies(df_)
        letter = lf.idxmax()

        return letter
    

    def letter_frequencies(self, df_:pd.DataFrame):
        df_ = df_.reset_index(drop=True)
        letter_counts = df_.sum()
        total_letters = letter_counts.sum()

        return letter_counts/total_letters
    
    def count_same_place_letters(self, word1, word2):
        count = 0
        for i in range(len(word1)):
            if word1[i] == word2[i]:
                count += 1
        return count
    
    def find_incomplete_word(self, word):
        max_count = 0
        final_word = ""
        for palavra in self.df.index:
            count = self.count_same_place_letters(word, palavra)
            if count > max_count:
                max_count = count
                final_word = palavra
        return final_word


    def play(self):

        game = Hangman()
        game.novo_jogo()
        print(game.palavra)
        

        word = ""
        for i in range(len(game.palavra)):
            word += "-"
        self.df = self.df[self.df.index.str.len() == len(word)]
        word = list(word)

        while game.vidas > 1:
             
            if word.count("-") == 0:
                return game.tentar_palavra("".join(word))

            letter = self.guess(word)
            result = game.tentar_letra(letter)

            if result != False:
                if len(result) > 0:
                    for i in result:
                        word[i] = letter
                    self.df = self.df[self.df[letter] == len(result)]
                else:
                    self.df = self.df[self.df[letter] == 0]

        word = self.find_incomplete_word(word)
        
        return game.tentar_palavra(word) 






def main():
    # Inicializa o dataframe de palavras
    df = pd.read_csv("br-sem-acentos.txt", header=None, names=['word'])
    df['word'] = df['word'].str.lower()
    hangedman = HangedMan(df)
    return hangedman.play()

if __name__ == "__main__":
    main()