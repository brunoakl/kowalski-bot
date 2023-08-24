import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import string

# É necessário baixar o lexicon do VADER (Valence Aware Dictionary and sEntiment Reasoner)
nltk.download('vader_lexicon')

def analisar_sentimento(texto):
    # Criar o analisador de sentimentos VADER
    sid = SentimentIntensityAnalyzer()

    # Remover a pontuação e converter para letras minúsculas
    texto_sem_pontuacao = texto.translate(str.maketrans('', '', string.punctuation)).lower()
    
    # Obter a pontuação do sentimento do texto pré-processado
    pontuacao = sid.polarity_scores(texto_sem_pontuacao)
    
    # Interpretar a pontuação em uma resposta
    if pontuacao['compound'] >= 0.05:
        return "positivo"
    elif pontuacao['compound'] <= -0.05:
        return "negativo"
    else:
        return "neutro"

if __name__ == "__main__":
    # Exemplo de utilização
    while True:
        mensagem = input("Digite uma mensagem (ou 'sair' para encerrar): ")
        
        if mensagem.lower() == "sair":
            break

        sentimento = analisar_sentimento(mensagem)
        print(f"Sentimento da mensagem: {sentimento}")
