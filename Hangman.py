import random
import pandas as pd


class Hangman:

    def __init__(self):

        # inicializa a base de palavras para o jogo
        self.content = pd.read_csv("br-sem-acentos.txt", header=None, names=['word'])
    

    def novo_jogo(self, palavra="", vidas=5):
        '''
        Função que inicia um novo jogo
        '''

        self.vidas = vidas 

        # Adição da possibilidade de escolher a palavra
        if self.content["word"].str.contains(palavra).any() and palavra != '':
            self.palavra = palavra
            return len(self.palavra)
        elif palavra != "": # checa se a palavra passada é válida
            print("A palavra passada foi inválida! Outra palavra foi escolhida")
        
        # Escolhe uma palavra aleatória caso nenhuma seja bassada
        self.palavra = random.choice(self.content["word"])

        return len(self.palavra)


    def tentar_letra(self, letra):
        '''
        Função que tenta uma letra
        '''

        if self.vidas > 0:
            if letra in self.palavra:
                # retorna os índices onde a letra aparece na palavra
                return [idx for idx in range(len(self.palavra)) if self.palavra[idx]==letra]
            else:
                # perde uma vida
                self.vidas -= 1
                if self.vidas == 0:
                    return [False, self.palavra]
                else:
                    return []
        

    def tentar_palavra(self, palavra):
        '''
        Função que tenta uma palavra
        '''

        # se possui vida
        if self.vidas > 0:
            if self.palavra == palavra: # acertou
                return [True, self.palavra, palavra]
            else: # errou
                self.vidas = 0
                return [False, self.palavra, palavra]