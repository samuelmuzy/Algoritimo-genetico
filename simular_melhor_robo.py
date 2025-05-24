from robo_exercicio import IndividuoPG, Ambiente, Robo, Simulador

def simular_melhor_robo():
    print("Carregando o melhor robô salvo...")
    try:
        melhor_individuo = IndividuoPG.carregar('melhor_robo.json')
        print("Robô carregado com sucesso!")
        
        # Criar ambiente e robô
        ambiente = Ambiente()
        robo = Robo(ambiente.largura // 2, ambiente.altura // 2)
        
        # Criar simulador
        simulador = Simulador(ambiente, robo, melhor_individuo)
        
        print("\nExecutando simulação do melhor robô...")
        print("A simulação será exibida em uma janela separada.")
        print("Pressione Ctrl+C para fechar a janela quando desejar.")
        
        simulador.simular()
    except FileNotFoundError:
        print("Erro: Arquivo 'melhor_robo.json' não encontrado!")
        print("Execute primeiro o treinamento do algoritmo genético.")
    except Exception as e:
        print(f"Erro ao carregar o robô: {str(e)}")

if __name__ == "__main__":
    simular_melhor_robo() 