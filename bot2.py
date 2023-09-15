import torch
from transformers import BertTokenizer, BertForSequenceClassification
from torch.nn.functional import softmax

# Carregando o modelo e o tokenizador pré-treinados
MODEL_NAME = "nlptown/bert-base-multilingual-uncased-sentiment"
model = BertForSequenceClassification.from_pretrained(MODEL_NAME)
tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
model.eval()  # Definir o modelo em modo de avaliação

def analisar_sentimento(texto):
    # Tokenizar o texto e obter a saída do modelo
    inputs = tokenizer(texto, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Obter a classe prevista
    predicted_class = torch.argmax(outputs.logits, dim=1).item() + 1  # +1 para ajustar a classificação de 0-4 para 1-5
    
    # Simplificar: 1-2 = triste, 4-5 = feliz, 3 = neutro
    if predicted_class in [1, 2]:
        return "triste"
    elif predicted_class in [4, 5]:
        return "feliz"
    else:
        return "neutro"

def chatbot():
    print("Olá! Como posso ajudar você hoje?")
    
    while True:
        entrada_usuario = input("Você: ")
        
        if entrada_usuario.lower() in ['sair', 'exit', 'tchau']:
            print("Chatbot: Até logo!")
            break
        
        sentimento = analisar_sentimento(entrada_usuario)
        
        if sentimento == "feliz":
            print("Chatbot: Parece que você está feliz! Isso é ótimo!")
        elif sentimento == "triste":
            print("Chatbot: Parece que você está triste. Sinto muito ouvir isso.")
        else:
            print("Chatbot: Como posso ajudar mais?")

if __name__ == "__main__":
    chatbot()
