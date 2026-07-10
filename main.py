import os
from dotenv import load_dotenv
from openai import OpenAI

#procurar a chave da API no arquivo .env
load_dotenv()

#atribuição de valor da chave da api para a variável MINHA_CHAVE
MINHA_CHAVE = os.getenv("GROQ_API_KEY")

#setup da IA
client = OpenAI(
    api_key=MINHA_CHAVE,
    base_url="https://api.groq.com/openai/v1"
)

MODELO = "llama-3.1-8b-instant"

#Pedimos para a IA escolher um animal aleatório
resposta_animal = client.chat.completions.create(
    model=MODELO,
    messages=[{"role": "user", "content": "Diga apenas o nome de um animal aleatório em português, apenas"
    " uma palavra e nada mais."}]
)
animal_secreto = resposta_animal.choices[0].message.content.strip()

print("===========================================")
print("Bem vindo ao jogo de adivinhação!")
print("===========================================")

print("Escolha o seu modo de jogo:")
print("1) Fácil - 20 chances")
print("2) Médio- 10 chances")
print("3) Difícil - 5 chances")

x = int(input("digite seu número aqui: "))
y = 20

if(x == 3):
    y = 5
elif(x == 2):
    y = 10
else:
    y = 20

print("O chatbot pensou em um animal, tente adivinhar fazendo perguntas pra ele!")

for i in range(y):
    perguntas_restantes = y - i
    print(f"\n[Você tem {perguntas_restantes} perguntas restantes]")
    
    # Pega a pergunta que você vai digitar no terminal
    pergunta_usuario = input("Sua pergunta: ")
    
    # 4. Criando as instruções secretas para a IA
    prompt_instrucoes = f"""
    Você é o mestre do jogo {y} Perguntas. 
    O animal secreto é: {animal_secreto}.
    O usuário perguntou: '{pergunta_usuario}'.
    Responda à pergunta do usuário de forma curta e útil (ex: Sim, Não, Geralmente, Às vezes).
    REGRA 1: NÃO diga o nome do animal em nenhuma hipótese.
    REGRA 2: Se o usuário adivinhou corretamente o animal, responda EXATAMENTE com a frase 'VOCÊ ACERTOU!'.
    REGRA 3: Responda apenas com sim o não, sempre se referindo ao animal secreto
    """
    
    # Enviamos a sua pergunta e as instruções para a IA avaliar
    resposta_ia = client.chat.completions.create(
        model=MODELO,
        messages=[{"role": "user", "content": prompt_instrucoes}]
    )
    
    # Extraímos a resposta
    texto_resposta = resposta_ia.choices[0].message.content
    print(f"🤖 IA: {texto_resposta}")
    
    # 5. Verifica se o usuário ganhou
    if "VOCÊ ACERTOU" in texto_resposta.upper():
        print(f"\n🎉 Parabéns, você venceu o jogo! O animal era mesmo: {animal_secreto}")
        break

# Se o loop terminar sem o 'break', significa que as tentativas acabaram
else:
    print(f"\n💀 Que pena, suas 20 perguntas acabaram! O animal secreto era: {animal_secreto}")