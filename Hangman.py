import random
import pandas as pd
class Hangman:
    def __init__(self):
        self.content = pd.read_csv("br-sem-acentos.txt", header=None, names=['word'])
    
    def novo_jogo(self, palavra="", vidas=5):
        self.vidas = vidas

        # Adição da possibilidade de escolher a palavra
        if palavra in self.content["word"]:
            self.palavra = palavra
        else:
            self.palavra = random.choice(self.content["word"])

        return len(self.palavra)

    def tentar_letra(self, letra):
        if self.vidas > 0:
            if letra in self.palavra:
                return [idx for idx in range(len(self.palavra)) if self.palavra[idx]==letra]
            else:
                self.vidas -= 1
                if self.vidas == 0:
                    return [False, self.palavra]
                else:
                    return []
        
    def tentar_palavra(self, palavra):
        if self.vidas > 0:
            if self.palavra == palavra:
                return [True, self.palavra, palavra]
            else:
                self.vidas = 0
                return [False, self.palavra, palavra]