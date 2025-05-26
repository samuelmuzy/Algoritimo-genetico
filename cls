[33mcommit 2ea44550debb33f3b9055f59aaf90cd112a6c453[m[33m ([m[1;36mHEAD[m[33m -> [m[1;32mmain[m[33m)[m
Author: Gabriel Bianquini <gsilvabianquini@gmail.com>
Date:   Mon May 26 02:15:24 2025 -0300

    Aumento de gerações para melhor desempenho do fitness e robo

[33mcommit bba6d6f1fccd38a020109b635442aec1ef4321a4[m
Author: samuel muzy <samuelmuzyfernandes4@gmail.com>
Date:   Sun May 25 12:06:37 2025 -0300

    Melhora avaliação de indivíduos com penalidades balanceadas e critérios mais robustos
    
    Reduz penalidades excessivas por comportamentos como loops de posição, loops de ângulo e tempo sem progresso.
    
    Ajusta detecção de loop espacial e angular para critérios mais realistas (menor distância final e janela de observação reduzida).
    
    Penaliza suavemente comportamentos indesejados como ausência de coleta, estagnação e colisões consecutivas.
    
    Rebalanceia recompensas: coleta de recursos e alcance da meta agora oferecem ganhos proporcionais, evitando overfitting em um único critério.
    
    Adiciona métricas como diversidade de posições visitadas e tempo sem coletar para enriquecer a avaliação do comportamento.
    
    Garante maior robustez e estabilidade durante a evolução, reduzindo falsos negativos e viabilizando soluções funcionais.

[33mcommit ef328a2872132404f08ef49522b7df51b2077bc2[m
Author: GabrielSetta <devsetta@gmail.com>
Date:   Sat May 24 19:44:49 2025 -0300

    Implementação de algoritmo genético para navegação de robô com detecção inteligente de recursos
    
    Implementação de um sistema de navegação autônoma usando programação genética com as seguintes melhorias:
    
    - Sistema de detecção e rastreamento inteligente de recursos
    - Mapeamento contínuo do ambiente com atualização dinâmica
    - Navegação adaptativa com ajuste de velocidade baseado em obstáculos
    - Sistema de evasão eficiente de colisões
    - Processamento paralelo para avaliação da população
    - Mutação adaptativa baseada no fitness do indivíduo
    - Cruzamento inteligente com preservação de características boas
    - Seleção elitista dos melhores indivíduos
    
    Parâmetros otimizados:
    - População: 200 indivíduos
    - Gerações: 40
    - Profundidade das árvores: 4
    - Processamento paralelo: Todos os núcleos disponíveis
    
    O sistema demonstra melhorias significativas na:
    - Taxa de coleta de recursos
    - Navegação suave e precisa
    - Evasão eficiente de obstáculos
    - Comportamento adaptativo ao ambiente

[33mcommit 8ae98b5b5ec24632a9b51ba8b909985b0555a6b6[m
Author: samuel muzy <samuelmuzyfernandes4@gmail.com>
Date:   Tue May 20 22:18:16 2025 -0300

    primeiro commit

[33mcommit ec2baba39ea850f892cac9a9b58ec54a2079e2a5[m
Author: samuel muzy fernandes <135380750+samuelmuzy@users.noreply.github.com>
Date:   Tue May 20 19:17:34 2025 -0300

    Initial commit
