# Simulador de Robô com Programação Genética

Um simulador de robô que utiliza programação genética para aprender a coletar recursos e navegar em um ambiente 2D.

## Funcionalidades

### Sistema de Detecção e Navegação
- Mapeamento contínuo de recursos
- Rastreamento inteligente dos 3 recursos mais próximos
- Navegação adaptativa com ajuste dinâmico de velocidade
- Sistema de evasão eficiente de obstáculos

### Algoritmo Genético
- Mutação adaptativa baseada no fitness
- Cruzamento inteligente com preservação de características boas
- Seleção elitista dos melhores indivíduos
- Processamento paralelo para avaliação da população

## Como Usar

1. Para treinar um novo robô:
```bash
python robo_exercicio.py
```

2. Para simular o melhor robô salvo:
```bash
python simular_melhor_robo.py
```

## Estrutura do Projeto
- `robo_exercicio.py`: Arquivo principal com o algoritmo genético
- `simular_melhor_robo.py`: Simulador do melhor robô salvo
- `melhor_robo.json`: Arquivo com o melhor robô treinado
- `alteracoes_implementadas.txt`: Documentação das mudanças

## Características do Robô
- Coleta recursos de forma eficiente
- Navegação suave e precisa
- Evasão inteligente de obstáculos
- Comportamento adaptativo

## Métricas de Performance
- Taxa de coleta de recursos
- Tempo total de missão
- Número de colisões
- Eficiência energética

## Parâmetros Atuais
- População: 200 indivíduos
- Gerações: 40
- Profundidade das árvores: 4
- Processamento paralelo: Todos os núcleos disponíveis

## 📝 Licença
Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## ✨ Melhorias Futuras

- [ ] Implementação de algoritmos de pathfinding
- [ ] Adição de mais tipos de obstáculos
- [ ] Sistema de comunicação entre robôs
- [ ] Interface gráfica mais elaborada
- [ ] Sistema de aprendizado por reforço

## 📧 Contato

Seu Nome - [@seu_twitter](https://twitter.com/seu_twitter) - email@exemplo.com

Link do Projeto: [https://github.com/seu-usuario/robo-programacao-genetica](https://github.com/seu-usuario/robo-programacao-genetica) 