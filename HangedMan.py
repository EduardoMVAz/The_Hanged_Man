import pandas as pd

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
            

    def guess(self, word:str, wrong_letters:list):
        # --a--b
        df_ = self.df[self.df.index.str.len() == len(word)]
        guessed_letters = [i for i in word if i != "-"]
        df_ = df_.drop(guessed_letters + wrong_letters, axis=1)

        # acha a letra mais frequente e chuta
        lf = self.letter_frequencies(df_)
        letter = lf.idxmax()

        return letter
    

    def letter_frequencies(self, df_:pd.DataFrame):
        df_ = df_.reset_index(drop=True)
        letter_counts = df_.sum()
        total_letters = letter_counts.sum()

        return letter_counts/total_letters



def main():
    df = pd.read_csv("br-sem-acentos.txt", header=None, names=['word'])
    df['word'] = df['word'].str.lower()
    p = HangedMan(df)
    word = "-----"

    print(p.guess(word, []))

if __name__ == "__main__":
    main()