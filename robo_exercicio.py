import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
import json
import time
import multiprocessing as mp
from functools import partial

# =====================================================================
# PARTE 1: ESTRUTURA DA SIMULAÇÃO (NÃO MODIFICAR)
# Esta parte contém a estrutura básica da simulação, incluindo o ambiente,
# o robô e a visualização. Não é recomendado modificar esta parte.
# =====================================================================

class Ambiente:
    def __init__(self, largura=800, altura=600, num_obstaculos=5, num_recursos=5):
        self.largura = largura
        self.altura = altura
        self.obstaculos = self.gerar_obstaculos(num_obstaculos)
        self.recursos = self.gerar_recursos(num_recursos)
        self.tempo = 0
        self.max_tempo = 1000  # Tempo máximo de simulação
        self.meta = self.gerar_meta()  # Adicionando a meta
        self.meta_atingida = False  # Flag para controlar se a meta foi atingida
        self.todos_recursos_coletados = False  # Flag para controlar se todos recursos foram coletados
    
    def gerar_obstaculos(self, num_obstaculos):
        obstaculos = []
        for _ in range(num_obstaculos):
            x = random.randint(50, self.largura - 50)
            y = random.randint(50, self.altura - 50)
            largura = random.randint(20, 100)
            altura = random.randint(20, 100)
            obstaculos.append({
                'x': x,
                'y': y,
                'largura': largura,
                'altura': altura
            })
        return obstaculos
    
    def gerar_recursos(self, num_recursos):
        recursos = []
        for _ in range(num_recursos):
            x = random.randint(20, self.largura - 20)
            y = random.randint(20, self.altura - 20)
            recursos.append({
                'x': x,
                'y': y,
                'coletado': False
            })
        return recursos
    
    def gerar_meta(self):
        # Gerar a meta em uma posição segura, longe dos obstáculos
        max_tentativas = 100
        margem = 50  # Margem das bordas
        
        for _ in range(max_tentativas):
            x = random.randint(margem, self.largura - margem)
            y = random.randint(margem, self.altura - margem)
            
            # Verificar se a posição está longe o suficiente dos obstáculos
            posicao_segura = True
            for obstaculo in self.obstaculos:
                # Calcular a distância até o obstáculo mais próximo
                dist_x = max(obstaculo['x'] - x, 0, x - (obstaculo['x'] + obstaculo['largura']))
                dist_y = max(obstaculo['y'] - y, 0, y - (obstaculo['y'] + obstaculo['altura']))
                dist = np.sqrt(dist_x**2 + dist_y**2)
                
                if dist < 50:  # 50 pixels de margem extra
                    posicao_segura = False
                    break
            
            if posicao_segura:
                return {
                    'x': x,
                    'y': y,
                    'raio': 30  # Raio da meta
                }
        
        # Se não encontrar uma posição segura, retorna o centro
        return {
            'x': self.largura // 2,
            'y': self.altura // 2,
            'raio': 30
        }
    
    def verificar_colisao(self, x, y, raio):
        # Verificar colisão com as bordas
        if x - raio < 0 or x + raio > self.largura or y - raio < 0 or y + raio > self.altura:
            return True
        
        # Verificar colisão com obstáculos
        for obstaculo in self.obstaculos:
            if (x + raio > obstaculo['x'] and 
                x - raio < obstaculo['x'] + obstaculo['largura'] and
                y + raio > obstaculo['y'] and 
                y - raio < obstaculo['y'] + obstaculo['altura']):
                return True
        
        return False
    
    def verificar_coleta_recursos(self, x, y, raio):
        recursos_coletados = 0
        for recurso in self.recursos:
            if not recurso['coletado']:
                distancia = np.sqrt((x - recurso['x'])**2 + (y - recurso['y'])**2)
                if distancia < raio + 10:  # 10 é o raio do recurso
                    recurso['coletado'] = True
                    recursos_coletados += 1
        
        # Verificar se todos os recursos foram coletados
        if recursos_coletados > 0:
            self.todos_recursos_coletados = all(recurso['coletado'] for recurso in self.recursos)
        
        return recursos_coletados
    
    def verificar_atingir_meta(self, x, y, raio):
        if not self.meta_atingida:
            # Só pode atingir a meta se todos os recursos foram coletados
            if not self.todos_recursos_coletados:
                return False
                
            distancia = np.sqrt((x - self.meta['x'])**2 + (y - self.meta['y'])**2)
            if distancia < raio + self.meta['raio']:
                self.meta_atingida = True
                return True
        return False
    
    def reset(self):
        self.tempo = 0
        for recurso in self.recursos:
            recurso['coletado'] = False
        self.meta_atingida = False
        self.todos_recursos_coletados = False
        return self.get_estado()
    
    def get_estado(self):
        return {
            'tempo': self.tempo,
            'recursos_coletados': sum(1 for r in self.recursos if r['coletado']),
            'recursos_restantes': sum(1 for r in self.recursos if not r['coletado']),
            'meta_atingida': self.meta_atingida
        }
    
    def passo(self):
        self.tempo += 1
        return self.tempo >= self.max_tempo
    
    def posicao_segura(self, raio_robo=15):
        """Encontra uma posição segura para o robô, longe dos obstáculos"""
        max_tentativas = 100
        margem = 50  # Margem das bordas
        
        for _ in range(max_tentativas):
            x = random.randint(margem, self.largura - margem)
            y = random.randint(margem, self.altura - margem)
            
            # Verificar se a posição está longe o suficiente dos obstáculos
            posicao_segura = True
            for obstaculo in self.obstaculos:
                # Calcular a distância até o obstáculo mais próximo
                dist_x = max(obstaculo['x'] - x, 0, x - (obstaculo['x'] + obstaculo['largura']))
                dist_y = max(obstaculo['y'] - y, 0, y - (obstaculo['y'] + obstaculo['altura']))
                dist = np.sqrt(dist_x**2 + dist_y**2)
                
                if dist < raio_robo + 20:  # 20 pixels de margem extra
                    posicao_segura = False
                    break
            
            if posicao_segura:
                return x, y
        
        # Se não encontrar uma posição segura, retorna o centro
        return self.largura // 2, self.altura // 2

class Robo:
    def __init__(self, x, y, raio=15):
        self.x = x
        self.y = y
        self.raio = raio
        self.angulo = 0  # em radianos
        self.velocidade = 0
        self.energia = 100
        self.recursos_coletados = 0
        self.colisoes = 0
        self.distancia_percorrida = 0
        self.tempo_parado = 0  # Novo: contador de tempo parado
        self.ultima_posicao = (x, y)  # Novo: última posição conhecida
        self.meta_atingida = False  # Novo: flag para controlar se a meta foi atingida
    
    def reset(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.energia = 100
        self.recursos_coletados = 0
        self.colisoes = 0
        self.distancia_percorrida = 0
        self.tempo_parado = 0
        self.ultima_posicao = (x, y)
        self.meta_atingida = False
    
    def mover(self, aceleracao, rotacao, ambiente):
        # Atualizar ângulo
        self.angulo += rotacao
        
        # Verificar se o robô está parado
        distancia_movimento = np.sqrt((self.x - self.ultima_posicao[0])**2 + (self.y - self.ultima_posicao[1])**2)
        if distancia_movimento < 0.1:  # Se moveu menos de 0.1 unidades
            self.tempo_parado += 1
            # Forçar movimento após ficar parado por muito tempo
            if self.tempo_parado > 10:  # Aumentado para 10 passos parado
                #print("Robô parado, forçando movimento...") # Debug
                aceleracao = max(0.3, aceleracao)  # Força aceleração mínima um pouco maior
                rotacao = random.uniform(-np.pi/2, np.pi/2)  # Rotação aleatória mais ampla
                self.angulo += rotacao # Aplica a rotação imediatamente
                # Normalizar ângulo para [-pi, pi]
                while self.angulo > np.pi:
                    self.angulo -= 2 * np.pi
                while self.angulo < -np.pi:
                    self.angulo += 2 * np.pi
                self.tempo_parado = 0 # Resetar contador após forçar movimento
        else:
            self.tempo_parado = 0
        
        # Atualizar velocidade
        self.velocidade += aceleracao
        self.velocidade = max(0.1, min(5, self.velocidade))  # --- REVERTIDO: Restaurado clamp mínimo de 0.1 ---
        
        # Calcular nova posição
        novo_x = self.x + self.velocidade * np.cos(self.angulo)
        novo_y = self.y + self.velocidade * np.sin(self.angulo)
        
        # Verificar colisão
        if ambiente.verificar_colisao(novo_x, novo_y, self.raio):
            self.colisoes += 1
            # --- NOVO: Resposta à colisão mais robusta ---
            # 1. Recuo pequeno para evitar ficar preso na parede/obstáculo
            recoil_dist = -3 # Recuar 3 unidades (ajustável)
            self.x += recoil_dist * np.cos(self.angulo)
            self.y += recoil_dist * np.sin(self.angulo)
            # Garantir que o recuo não coloque o robô fora dos limites (simplificado)
            self.x = max(self.raio, min(self.x, ambiente.largura - self.raio))
            self.y = max(self.raio, min(self.y, ambiente.altura - self.raio))

            # 2. Rotação aleatória significativa (entre 90 e 180 graus em qualquer direção)
            rotacao_escape = random.uniform(np.pi/2, np.pi) * random.choice([-1, 1])
            self.angulo += rotacao_escape
            # Normalizar ângulo para [-pi, pi]
            while self.angulo > np.pi:
                self.angulo -= 2 * np.pi
            while self.angulo < -np.pi:
                self.angulo += 2 * np.pi

            # 3. Resetar velocidade para forçar reavaliação da ação
            self.velocidade = 0
            #print(f"Colisão! Recuando e girando {rotacao_escape:.2f} rad.") # Debug
            # --- FIM NOVO ---
        else:
            # Atualizar posição
            self.distancia_percorrida += np.sqrt((novo_x - self.x)**2 + (novo_y - self.y)**2)
            self.x = novo_x
            self.y = novo_y
        
        # Atualizar última posição conhecida
        self.ultima_posicao = (self.x, self.y)
        
        # Verificar coleta de recursos
        recursos_coletados = ambiente.verificar_coleta_recursos(self.x, self.y, self.raio)
        self.recursos_coletados += recursos_coletados
        
        # Verificar se atingiu a meta
        if not self.meta_atingida and ambiente.verificar_atingir_meta(self.x, self.y, self.raio):
            self.meta_atingida = True
            # Recuperar energia ao atingir a meta
            self.energia = min(100, self.energia + 50)
        
        # Consumir energia
        self.energia -= 0.1 + 0.05 * self.velocidade + 0.1 * abs(rotacao)
        self.energia = max(0, self.energia)
        
        # Recuperar energia ao coletar recursos
        if recursos_coletados > 0:
            self.energia = min(100, self.energia + 20 * recursos_coletados)
        
        return self.energia <= 0
    
    def get_sensores(self, ambiente):
        # Distância até o recurso mais próximo
        dist_recurso = float('inf')
        x_recurso = 0
        y_recurso = 0
        for recurso in ambiente.recursos:
            if not recurso['coletado']:
                dist = np.sqrt((self.x - recurso['x'])**2 + (self.y - recurso['y'])**2)
                if dist < dist_recurso:
                    dist_recurso = dist
                    x_recurso = recurso['x']
                    y_recurso = recurso['y']
        
        # Distância até o obstáculo mais próximo
        dist_obstaculo = float('inf')
        for obstaculo in ambiente.obstaculos:
            # Simplificação: considerar apenas a distância até o centro do obstáculo
            centro_x = obstaculo['x'] + obstaculo['largura'] / 2
            centro_y = obstaculo['y'] + obstaculo['altura'] / 2
            dist = np.sqrt((self.x - centro_x)**2 + (self.y - centro_y)**2)
            dist_obstaculo = min(dist_obstaculo, dist)
        
        # Distância até a meta
        dist_meta = np.sqrt((self.x - ambiente.meta['x'])**2 + (self.y - ambiente.meta['y'])**2)
        
        # Ângulo até o recurso mais próximo
        angulo_recurso = 0
        if dist_recurso < float('inf'):
            dx = x_recurso - self.x
            dy = y_recurso - self.y
            angulo = np.arctan2(dy, dx)
            angulo_recurso = angulo - self.angulo
            # Normalizar para [-pi, pi]
            while angulo_recurso > np.pi:
                angulo_recurso -= 2 * np.pi
            while angulo_recurso < -np.pi:
                angulo_recurso += 2 * np.pi
        
        # Ângulo até a meta
        dx_meta = ambiente.meta['x'] - self.x
        dy_meta = ambiente.meta['y'] - self.y
        angulo_meta = np.arctan2(dy_meta, dx_meta) - self.angulo
        # Normalizar para [-pi, pi]
        while angulo_meta > np.pi:
            angulo_meta -= 2 * np.pi
        while angulo_meta < -np.pi:
            angulo_meta += 2 * np.pi
        
        return {
            'dist_recurso': dist_recurso,
            'dist_obstaculo': dist_obstaculo,
            'dist_meta': dist_meta,
            'angulo_recurso': angulo_recurso,
            'angulo_meta': angulo_meta,
            'energia': self.energia,
            'velocidade': self.velocidade,
            'meta_atingida': self.meta_atingida,
            'x': self.x,
            'y': self.y,
            'x_recurso': x_recurso,
            'y_recurso': y_recurso,
            'x_meta': ambiente.meta['x'],
            'y_meta': ambiente.meta['y'],
            'angulo_atual': self.angulo,
            'recursos_coletados': self.recursos_coletados,
            'total_recursos': len(ambiente.recursos)
        }

class Simulador:
    def __init__(self, ambiente, robo, individuo):
        self.ambiente = ambiente
        self.robo = robo
        self.individuo = individuo
        self.frames = []
        
        # Configurar matplotlib para melhor visualização
        plt.style.use('default')  # Usar estilo padrão
        plt.ion()  # Modo interativo
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.ax.set_xlim(0, ambiente.largura)
        self.ax.set_ylim(0, ambiente.altura)
        self.ax.set_title("Simulador de Robô com Programação Genética", fontsize=14)
        self.ax.set_xlabel("X", fontsize=12)
        self.ax.set_ylabel("Y", fontsize=12)
        self.ax.grid(True, linestyle='--', alpha=0.7)
    
    def simular(self):
        self.ambiente.reset()
        # Encontrar uma posição segura para o robô
        x_inicial, y_inicial = self.ambiente.posicao_segura(self.robo.raio)
        self.robo.reset(x_inicial, y_inicial)
        self.frames = []
        
        # Limpar a figura atual
        self.ax.clear()
        self.ax.set_xlim(0, self.ambiente.largura)
        self.ax.set_ylim(0, self.ambiente.altura)
        self.ax.set_title("Simulador de Robô com Programação Genética", fontsize=14)
        self.ax.set_xlabel("X", fontsize=12)
        self.ax.set_ylabel("Y", fontsize=12)
        self.ax.grid(True, linestyle='--', alpha=0.7)
        
        # Desenhar obstáculos (estáticos)
        for obstaculo in self.ambiente.obstaculos:
            rect = patches.Rectangle(
                (obstaculo['x'], obstaculo['y']),
                obstaculo['largura'],
                obstaculo['altura'],
                linewidth=1,
                edgecolor='black',
                facecolor='#FF9999',  # Vermelho claro
                alpha=0.7
            )
            self.ax.add_patch(rect)
        
        # Desenhar recursos (estáticos)
        for recurso in self.ambiente.recursos:
            if not recurso['coletado']:
                circ = patches.Circle(
                    (recurso['x'], recurso['y']),
                    10,
                    linewidth=1,
                    edgecolor='black',
                    facecolor='#99FF99',  # Verde claro
                    alpha=0.8
                )
                self.ax.add_patch(circ)
        
        # Desenhar a meta
        meta_circ = patches.Circle(
            (self.ambiente.meta['x'], self.ambiente.meta['y']),
            self.ambiente.meta['raio'],
            linewidth=2,
            edgecolor='black',
            facecolor='#FFFF00',  # Amarelo
            alpha=0.8
        )
        self.ax.add_patch(meta_circ)
        
        # Criar objetos para o robô e direção (serão atualizados)
        robo_circ = patches.Circle(
            (self.robo.x, self.robo.y),
            self.robo.raio,
            linewidth=1,
            edgecolor='black',
            facecolor='#9999FF',  # Azul claro
            alpha=0.8
        )
        self.ax.add_patch(robo_circ)
        
        # Criar texto para informações
        info_text = self.ax.text(
            10, self.ambiente.altura - 50,  # Alterado de 10 para 50 para descer a legenda
            "",
            fontsize=12,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray', boxstyle='round,pad=0.5')
        )
        
        # Atualizar a figura
        plt.draw()
        plt.pause(0.01)
        
        try:
            while True:
                # Obter sensores
                sensores = self.robo.get_sensores(self.ambiente)
                
                # Avaliar árvores de decisão
                aceleracao = self.individuo.avaliar(sensores, 'aceleracao')
                rotacao = self.individuo.avaliar(sensores, 'rotacao')
                
                # Limitar valores
                aceleracao = max(-1, min(1, aceleracao))
                rotacao = max(-0.5, min(0.5, rotacao))
                
                # Mover robô
                sem_energia = self.robo.mover(aceleracao, rotacao, self.ambiente)
                
                # Atualizar visualização em tempo real
                self.ax.clear()
                self.ax.set_xlim(0, self.ambiente.largura)
                self.ax.set_ylim(0, self.ambiente.altura)
                self.ax.set_title("Simulador de Robô com Programação Genética", fontsize=14)
                self.ax.set_xlabel("X", fontsize=12)
                self.ax.set_ylabel("Y", fontsize=12)
                self.ax.grid(True, linestyle='--', alpha=0.7)
                
                # Desenhar obstáculos
                for obstaculo in self.ambiente.obstaculos:
                    rect = patches.Rectangle(
                        (obstaculo['x'], obstaculo['y']),
                        obstaculo['largura'],
                        obstaculo['altura'],
                        linewidth=1,
                        edgecolor='black',
                        facecolor='#FF9999',
                        alpha=0.7
                    )
                    self.ax.add_patch(rect)
                
                # Desenhar recursos
                for recurso in self.ambiente.recursos:
                    if not recurso['coletado']:
                        circ = patches.Circle(
                            (recurso['x'], recurso['y']),
                            10,
                            linewidth=1,
                            edgecolor='black',
                            facecolor='#99FF99',
                            alpha=0.8
                        )
                        self.ax.add_patch(circ)
                
                # Desenhar a meta
                meta_circ = patches.Circle(
                    (self.ambiente.meta['x'], self.ambiente.meta['y']),
                    self.ambiente.meta['raio'],
                    linewidth=2,
                    edgecolor='black',
                    facecolor='#FFFF00',  # Amarelo
                    alpha=0.8
                )
                self.ax.add_patch(meta_circ)
                
                # Desenhar robô
                robo_circ = patches.Circle(
                    (self.robo.x, self.robo.y),
                    self.robo.raio,
                    linewidth=1,
                    edgecolor='black',
                    facecolor='#9999FF',
                    alpha=0.8
                )
                self.ax.add_patch(robo_circ)
                
                # Desenhar direção do robô
                direcao_x = self.robo.x + self.robo.raio * np.cos(self.robo.angulo)
                direcao_y = self.robo.y + self.robo.raio * np.sin(self.robo.angulo)
                self.ax.plot([self.robo.x, direcao_x], [self.robo.y, direcao_y], 'r-', linewidth=2)
                
                # Adicionar informações
                info_text = self.ax.text(
                    10, self.ambiente.altura - 50,  # Alterado de 10 para 50 para descer a legenda
                    f"Tempo: {self.ambiente.tempo}\n"
                    f"Recursos: {self.robo.recursos_coletados}\n"
                    f"Energia: {self.robo.energia:.1f}\n"
                    f"Colisões: {self.robo.colisoes}\n"
                    f"Distância: {self.robo.distancia_percorrida:.1f}\n"
                    f"Meta atingida: {'Sim' if self.robo.meta_atingida else 'Não'}",
                    fontsize=12,
                    bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray', boxstyle='round,pad=0.5')
                )
                
                # Atualizar a figura
                plt.draw()
                plt.pause(0.05)
                
                # Verificar fim da simulação
                if sem_energia or self.ambiente.passo():
                    break
            
            # Manter a figura aberta até que o usuário a feche
            plt.ioff()
            plt.show()
            
        except KeyboardInterrupt:
            plt.close('all')
        
        return self.frames
    
    def animar(self):
        # Desativar o modo interativo antes de criar a animação
        plt.ioff()
        
        # Criar a animação
        anim = animation.FuncAnimation(
            self.fig, self.atualizar_frame,
            frames=len(self.frames),
            interval=50,
            blit=True,
            repeat=True  # Permitir que a animação repita
        )
        
        # Mostrar a animação e manter a janela aberta
        plt.show(block=True)
    
    def atualizar_frame(self, frame_idx):
        return self.frames[frame_idx]

# =====================================================================
# PARTE 2: ALGORITMO GENÉTICO (PARA O VOCÊ MODIFICAR)
# Esta parte contém a implementação do algoritmo genético.
# Deve modificar os parâmetros e a lógica para melhorar o desempenho.
# =====================================================================

class IndividuoPG:
    def __init__(self, profundidade=3):
        self.profundidade = profundidade
        self.arvore_aceleracao = self.criar_arvore_aleatoria()
        self.arvore_rotacao = self.criar_arvore_aleatoria()
        self.fitness = 0
        self.recurso_atual = None
        self.tempo_perseguindo = 0
        self.estado = 'BUSCANDO_RECURSO'
        self.ultima_posicao = None
        self.tempo_sem_progresso = 0
        self.ultima_rotacao = 0
        self.distancia_anterior = float('inf')
        self.angulo_anterior = 0
        self.ultima_distancia_recurso = float('inf')
        self.velocidade_alvo = 0.5
        self.ultimos_recursos = []  # Lista para rastrear recursos recentes
        self.mapa_recursos = {}  # Mapa para armazenar informações dos recursos
        self.ultima_atualizacao_recursos = 0  # Contador para atualização periódica
        self.ambiente = None  # Novo atributo para armazenar o ambiente
    
    def criar_arvore_aleatoria(self):
        if self.profundidade == 0:
            return self.criar_folha()
        
        # Operadores otimizados com maior chance para os básicos
        operadores = ['+', '-', '*', '/', 'max', 'min', 'abs', 'if_positivo', 'if_negativo', 'cos', 'sin']
        pesos = [0.3, 0.3, 0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.05, 0.05]  # Maior peso para operadores básicos
        operador = random.choices(operadores, weights=pesos)[0]
        
        if operador in ['+', '-', '*', '/']:
            return {
                'tipo': 'operador',
                'operador': operador,
                'esquerda': IndividuoPG(self.profundidade - 1).arvore_aceleracao,
                'direita': IndividuoPG(self.profundidade - 1).arvore_aceleracao
            }
        elif operador in ['max', 'min']:
            return {
                'tipo': 'operador',
                'operador': operador,
                'esquerda': IndividuoPG(self.profundidade - 1).arvore_aceleracao,
                'direita': IndividuoPG(self.profundidade - 1).arvore_aceleracao
            }
        elif operador in ['abs', 'cos', 'sin']:
            return {
                'tipo': 'operador',
                'operador': operador,
                'esquerda': IndividuoPG(self.profundidade - 1).arvore_aceleracao,
                'direita': None
            }
        else:  # if_positivo ou if_negativo
            return {
                'tipo': 'operador',
                'operador': operador,
                'esquerda': IndividuoPG(self.profundidade - 1).arvore_aceleracao,
                'direita': IndividuoPG(self.profundidade - 1).arvore_aceleracao
            }
    
    def criar_folha(self):
        # Variáveis com maior chance para sensores importantes
        variaveis = ['constante', 'dist_recurso', 'dist_obstaculo', 'dist_meta', 'angulo_recurso', 'angulo_meta', 'energia', 'velocidade', 'meta_atingida']
        pesos = [0.2, 0.2, 0.2, 0.1, 0.1, 0.1, 0.05, 0.05, 0.05]  # Maior peso para sensores importantes
        tipo = random.choices(variaveis, weights=pesos)[0]
        
        if tipo == 'constante':
            return {
                'tipo': 'folha',
                'valor': random.gauss(0, 2)  # Distribuição gaussiana para constantes
            }
        else:
            return {
                'tipo': 'folha',
                'variavel': tipo
            }
    
    def atualizar_mapa_recursos(self, sensores, ambiente):
        # Atualizar a cada 5 passos para não sobrecarregar
        if self.ultima_atualizacao_recursos % 5 != 0:
            self.ultima_atualizacao_recursos += 1
            return

        self.ultima_atualizacao_recursos += 1
        posicao_robo = (sensores['x'], sensores['y'])
        
        # Atualizar informações de todos os recursos
        for i, recurso in enumerate(ambiente.recursos):
            if not recurso['coletado']:
                # Calcular distância real considerando obstáculos
                distancia = self.calcular_distancia_segura(
                    posicao_robo,
                    (recurso['x'], recurso['y']),
                    ambiente
                )
                
                # Calcular ângulo em relação ao robô
                dx = recurso['x'] - sensores['x']
                dy = recurso['y'] - sensores['y']
                angulo = np.arctan2(dy, dx)
                
                # Normalizar ângulo em relação à orientação do robô
                angulo_relativo = angulo - sensores['angulo_atual']
                while angulo_relativo > np.pi:
                    angulo_relativo -= 2 * np.pi
                while angulo_relativo < -np.pi:
                    angulo_relativo += 2 * np.pi
                
                # Atualizar mapa de recursos
                self.mapa_recursos[i] = {
                    'posicao': (recurso['x'], recurso['y']),
                    'distancia': distancia,
                    'angulo': angulo_relativo,
                    'ultima_atualizacao': self.ultima_atualizacao_recursos
                }
        
        # Ordenar recursos por distância
        recursos_ordenados = sorted(
            self.mapa_recursos.items(),
            key=lambda x: x[1]['distancia']
        )
        
        # Atualizar lista de recursos recentes
        self.ultimos_recursos = [r[0] for r in recursos_ordenados[:3]]  # Manter os 3 mais próximos

    def encontrar_recurso_mais_proximo(self, sensores, ambiente):
        # Simplificado: Encontra o recurso não coletado geometricamente mais próximo
        self.atualizar_mapa_recursos(sensores, ambiente) # Mantém a atualização do mapa
        
        recurso_mais_proximo = None
        dist_min = float("inf")
        idx_mais_proximo = -1

        # Itera sobre todos os recursos não coletados no ambiente
        for i, recurso in enumerate(ambiente.recursos):
            if not recurso["coletado"]:
                # Usa a distância calculada pelo mapa (que pode considerar obstáculos)
                if i in self.mapa_recursos:
                    dist = self.mapa_recursos[i]["distancia"]
                    if dist < dist_min:
                        dist_min = dist
                        recurso_mais_proximo = recurso
                        idx_mais_proximo = i
                else:
                    # Fallback para distância Euclidiana se não estiver no mapa ainda
                    dist_euclidiana = np.sqrt((sensores["x"] - recurso["x"])**2 + (sensores["y"] - recurso["y"])**2)
                    if dist_euclidiana < dist_min:
                         dist_min = dist_euclidiana
                         recurso_mais_proximo = recurso
                         idx_mais_proximo = i

        # Retorna o recurso encontrado e sua distância
        return recurso_mais_proximo, dist_min

    def avaliar(self, sensores, tipo="aceleracao"):
        # --- NOVO: Se a tarefa está completa, parar o robô ---
        if self.estado == "TAREFA_COMPLETA":
            return 0.0 # Retorna 0 para aceleração e rotação
        # --- FIM NOVO ---

        # Normalização de valores
        sensores_normalizados = sensores.copy()
        sensores_normalizados["dist_recurso"] = min(1.0, sensores["dist_recurso"] / 800)
        sensores_normalizados["dist_obstaculo"] = min(1.0, sensores["dist_obstaculo"] / 800)
        sensores_normalizados["dist_meta"] = min(1.0, sensores["dist_meta"] / 800)
        sensores_normalizados["energia"] = sensores["energia"] / 100
        sensores_normalizados["velocidade"] = sensores["velocidade"] / 5
        
        # Atualizar mapa de recursos se o ambiente estiver disponível
        if self.ambiente is not None:
            self.atualizar_mapa_recursos(sensores, self.ambiente)
        
        # Detecção de paredes e obstáculos
        margem_parede = 50
        proximo_parede = False
        if (sensores['x'] < margem_parede or 
            sensores['x'] > 800 - margem_parede or 
            sensores['y'] < margem_parede or 
            sensores['y'] > 600 - margem_parede):
            proximo_parede = True
            sensores_normalizados['proximo_parede'] = 1.0
        else:
            sensores_normalizados['proximo_parede'] = 0.0
        
        # Sempre calcular o recurso mais próximo
        if self.estado == 'BUSCANDO_RECURSO' and self.ambiente is not None:
            recurso_mais_proximo, dist = self.encontrar_recurso_mais_proximo(sensores, self.ambiente)
            
            if recurso_mais_proximo:
                # Calcular ângulo ideal para o recurso
                dx = recurso_mais_proximo['x'] - sensores['x']
                dy = recurso_mais_proximo['y'] - sensores['y']
                angulo_ideal = np.arctan2(dy, dx)
                
                # Normalizar diferença de ângulo
                diff_angulo = angulo_ideal - sensores['angulo_atual']
                while diff_angulo > np.pi:
                    diff_angulo -= 2 * np.pi
                while diff_angulo < -np.pi:
                    diff_angulo += 2 * np.pi
                
                # Ajustar velocidade baseado na distância e alinhamento
                if abs(diff_angulo) > np.pi/4:  # Se não estiver bem alinhado
                    self.velocidade_alvo = 0.2  # Velocidade reduzida para girar
                else:
                    # Velocidade progressiva baseada na distância
                    self.velocidade_alvo = 0.3 + (1 - dist/800) * 0.7
                
                # Reduzir velocidade próximo a obstáculos
                if sensores['dist_obstaculo'] < 100 or proximo_parede:
                    self.velocidade_alvo *= 0.3
                
                # Verificar progresso
                if dist < self.ultima_distancia_recurso:
                    self.tempo_sem_progresso = 0
                else:
                    self.tempo_sem_progresso += 1
                
                self.ultima_distancia_recurso = dist
                
                # Se ficar preso, tentar uma nova direção
                if self.tempo_sem_progresso > 10:
                    # Calcular novo ângulo evitando obstáculos
                    angulo_escape = sensores['angulo_atual'] + np.pi/2
                    if sensores['dist_obstaculo'] < 100:
                        angulo_escape += np.pi/4
                    sensores_normalizados['angulo_recurso'] = angulo_escape
                    self.tempo_sem_progresso = 0
                    self.velocidade_alvo = 0.3
                
                sensores_normalizados['velocidade_alvo'] = self.velocidade_alvo
                sensores_normalizados['angulo_recurso'] = diff_angulo
                sensores_normalizados['dist_recurso'] = dist/800  # Normalizar distância
        
        else:  # RETORNANDO_META
            # Lógica similar para retornar à meta
            dx = sensores['x_meta'] - sensores['x']
            dy = sensores['y_meta'] - sensores['y']
            angulo_ideal = np.arctan2(dy, dx)
            
            diff_angulo = angulo_ideal - sensores['angulo_atual']
            while diff_angulo > np.pi:
                diff_angulo -= 2 * np.pi
            while diff_angulo < -np.pi:
                diff_angulo += 2 * np.pi
            
            if abs(diff_angulo) > np.pi/4:
                self.velocidade_alvo = 0.2
            else:
                self.velocidade_alvo = 0.3 + (1 - sensores_normalizados['dist_meta']) * 0.7
            
            if sensores['dist_obstaculo'] < 100 or proximo_parede:
                self.velocidade_alvo *= 0.3
            
            sensores_normalizados['velocidade_alvo'] = self.velocidade_alvo
            sensores_normalizados['angulo_meta'] = diff_angulo
        
        # Atualizar última posição
        self.ultima_posicao = (sensores['x'], sensores['y'])
        
        arvore = self.arvore_aceleracao if tipo == 'aceleracao' else self.arvore_rotacao
        return self.avaliar_no(arvore, sensores_normalizados)
    
    def avaliar_no(self, no, sensores):
        if no is None:
            return 0
            
        if no['tipo'] == 'folha':
            if 'valor' in no:
                return no['valor']
            elif 'variavel' in no:
                return sensores[no['variavel']]
        
        if no['operador'] == 'abs':
            return abs(self.avaliar_no(no['esquerda'], sensores))
        elif no['operador'] == 'cos':
            return np.cos(self.avaliar_no(no['esquerda'], sensores))
        elif no['operador'] == 'sin':
            return np.sin(self.avaliar_no(no['esquerda'], sensores))
        elif no['operador'] == 'if_positivo':
            valor = self.avaliar_no(no['esquerda'], sensores)
            if valor > 0:
                return self.avaliar_no(no['direita'], sensores)
            else:
                return 0
        elif no['operador'] == 'if_negativo':
            valor = self.avaliar_no(no['esquerda'], sensores)
            if valor < 0:
                return self.avaliar_no(no['direita'], sensores)
            else:
                return 0
        
        esquerda = self.avaliar_no(no['esquerda'], sensores)
        direita = self.avaliar_no(no['direita'], sensores) if no['direita'] is not None else 0
        
        if no['operador'] == '+':
            return esquerda + direita
        elif no['operador'] == '-':
            return esquerda - direita
        elif no['operador'] == '*':
            return esquerda * direita
        elif no['operador'] == '/':
            return esquerda / direita if direita != 0 else 0
        elif no['operador'] == 'max':
            return max(esquerda, direita)
        else:  # min
            return min(esquerda, direita)
    
    def mutacao_no(self, no, probabilidade):
        if random.random() < probabilidade:
            if no['tipo'] == 'folha':
                if 'valor' in no:
                    no['valor'] = self.mutacao_constante(no['valor'])
                elif 'variavel' in no:
                    no['variavel'] = self.mutacao_variavel(no['variavel'])
            else:
                no['operador'] = self.mutacao_operador(no['operador'])
        
        if no['tipo'] == 'operador':
            self.mutacao_no(no['esquerda'], probabilidade)
            if no['direita'] is not None:
                self.mutacao_no(no['direita'], probabilidade)

    def mutacao_constante(self, valor):
        # Mutação suave usando distribuição gaussiana
        # Reduz a magnitude da mutação para valores maiores
        if abs(valor) > 5:
            return valor + random.gauss(0, 0.2)  # Mutação menor para valores grandes
        else:
            return valor + random.gauss(0, 0.5)  # Mutação normal para valores pequenos
    
    def mutacao_variavel(self, variavel_atual):
        # Variáveis com maior chance para sensores importantes
        variaveis = ['dist_recurso', 'dist_obstaculo', 'dist_meta', 'angulo_recurso', 'angulo_meta', 'energia', 'velocidade', 'meta_atingida']
        pesos = [0.3, 0.2, 0.1, 0.2, 0.1, 0.05, 0.05, 0.05]  # Ajustado para priorizar sensores de recursos
        
        # Maior chance de manter a variável atual se for importante
        if variavel_atual in ['dist_recurso', 'angulo_recurso']:
            if random.random() < 0.7:  # 70% de chance de manter
                return variavel_atual
        
        return random.choices(variaveis, weights=pesos)[0]
    
    def mutacao_operador(self, operador_atual):
        # Operadores com maior chance para os básicos
        operadores = ['+', '-', '*', '/', 'max', 'min', 'abs', 'if_positivo', 'if_negativo', 'cos', 'sin']
        pesos = [0.3, 0.3, 0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.05, 0.05]
        
        # Maior chance de manter operadores básicos que funcionam bem
        if operador_atual in ['+', '-', '*']:
            if random.random() < 0.8:  # 80% de chance de manter
                return operador_atual
        
        return random.choices(operadores, weights=pesos)[0]

    def mutacao(self, probabilidade=0.1):
        # Mutação adaptativa baseada no fitness
        if self.fitness < 5000:  # Ajustado para novos valores
            probabilidade *= 2.0  # 100% mais chance de mutação
        elif self.fitness < 10000:  # Ajustado para novos valores
            probabilidade *= 1.5  # 50% mais chance de mutação
        elif self.fitness > 20000:  # Ajustado para novos valores
            probabilidade *= 0.5  # 50% menos chance de mutação
        elif self.fitness > 30000:  # Ajustado para novos valores
            probabilidade *= 0.3  # 70% menos chance de mutação
        
        self.mutacao_no(self.arvore_aceleracao, probabilidade)
        self.mutacao_no(self.arvore_rotacao, probabilidade)
    
    def crossover(self, outro):
        novo = IndividuoPG(self.profundidade)
        novo.arvore_aceleracao = self.crossover_no(self.arvore_aceleracao, outro.arvore_aceleracao)
        novo.arvore_rotacao = self.crossover_no(self.arvore_rotacao, outro.arvore_rotacao)
        return novo
    
    def crossover_no(self, no1, no2):
        # Probabilidade de crossover adaptativa
        if random.random() < 0.7:  # 70% de chance de crossover
            return no1.copy()
        else:
            return no2.copy()
    
    def salvar(self, arquivo):
        with open(arquivo, 'w') as f:
            json.dump({
                'arvore_aceleracao': self.arvore_aceleracao,
                'arvore_rotacao': self.arvore_rotacao
            }, f)
    
    @classmethod
    def carregar(cls, arquivo):
        with open(arquivo, 'r') as f:
            dados = json.load(f)
            individuo = cls()
            individuo.arvore_aceleracao = dados['arvore_aceleracao']
            individuo.arvore_rotacao = dados['arvore_rotacao']
            return individuo
    
    def atualizar_estado(self, sensores):
        # Verificar se coletou todos os recursos
        recursos_coletados = sensores.get("recursos_coletados", 0)
        total_recursos = sensores.get("total_recursos", 5)
        meta_atingida_agora = sensores.get("meta_atingida", False)

        # Se já completou, não faz nada
        if self.estado == "TAREFA_COMPLETA":
            return

        # Se estava buscando recursos e coletou todos
        if self.estado == "BUSCANDO_RECURSO" and recursos_coletados == total_recursos:
            #print("Todos recursos coletados! Mudando para RETORNANDO_META.") # Debug
            self.estado = "RETORNANDO_META"
            self.velocidade_alvo = 0.5  # Resetar velocidade ao mudar de estado
            self.tempo_sem_progresso = 0 # Resetar contador de progresso
            self.ultima_distancia_recurso = float("inf") # Resetar distância

        # Se estava retornando para a meta e a atingiu
        elif self.estado == "RETORNANDO_META" and meta_atingida_agora:
            #print("Meta atingida após coletar recursos! Mudando para TAREFA_COMPLETA.") # Debug
            self.estado = "TAREFA_COMPLETA"
            self.velocidade_alvo = 0 # Parar
    
    def calcular_distancia_segura(self, ponto1, ponto2, ambiente):
        # Distância euclidiana básica
        dist = np.sqrt((ponto1[0] - ponto2[0])**2 + (ponto1[1] - ponto2[1])**2)
        
        # Penalidade por obstáculos no caminho
        for obstaculo in ambiente.obstaculos:
            if self.obstaculo_no_caminho(ponto1, ponto2, obstaculo):
                dist *= 1.5  # Aumentar distância se houver obstáculo
        
        return dist
    
    def obstaculo_no_caminho(self, ponto1, ponto2, obstaculo):
        # Verificar se o obstáculo está entre os dois pontos
        x1, y1 = ponto1
        x2, y2 = ponto2
        
        # Calcular retângulo do obstáculo
        obs_x1 = obstaculo['x']
        obs_y1 = obstaculo['y']
        obs_x2 = obs_x1 + obstaculo['largura']
        obs_y2 = obs_y1 + obstaculo['altura']
        
        # Verificar interseção da linha com o retângulo
        return self.linha_intersecta_retangulo(x1, y1, x2, y2, obs_x1, obs_y1, obs_x2, obs_y2)
    
    def linha_intersecta_retangulo(self, x1, y1, x2, y2, rx1, ry1, rx2, ry2):
        # Verificar se a linha intersecta o retângulo
        def ccw(A, B, C):
            return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])
        
        def intersecta(A, B, C, D):
            return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)
        
        # Pontos da linha
        A = (x1, y1)
        B = (x2, y2)
        
        # Pontos do retângulo
        C = (rx1, ry1)
        D = (rx2, ry1)
        E = (rx2, ry2)
        F = (rx1, ry2)
        
        # Verificar interseção com cada lado do retângulo
        return (intersecta(A, B, C, D) or
                intersecta(A, B, D, E) or
                intersecta(A, B, E, F) or
                intersecta(A, B, F, C))

class ProgramacaoGenetica:
    def __init__(self, tamanho_populacao=50, profundidade=3):
        self.tamanho_populacao = tamanho_populacao
        self.profundidade = profundidade
        self.populacao = [IndividuoPG(profundidade) for _ in range(tamanho_populacao)]
        self.melhor_individuo = None
        self.melhor_fitness = float('-inf')
        self.historico_fitness = []
        self.historico_media = []
        self.ultima_colisao = False
        self.cache_avaliacao = {}
        self.num_processos = mp.cpu_count()
    
    def avaliar_individuo(self, individuo, num_tentativas=3):
        ambiente = Ambiente()
        robo = Robo(ambiente.largura // 2, ambiente.altura // 2)
        individuo.ambiente = ambiente
        fitness = 0

        for _ in range(num_tentativas):
            ambiente.reset()
            robo.reset(ambiente.largura // 2, ambiente.altura // 2)
            individuo.recurso_atual = None
            individuo.tempo_perseguindo = 0
            individuo.estado = 'BUSCANDO_RECURSO'
            individuo.ultima_posicao = None
            individuo.tempo_sem_progresso = 0
            individuo.ambiente = ambiente

            ultima_colisao = False
            tempo_sem_movimento = 0
            ultima_posicao = (robo.x, robo.y)
            ultima_distancia_recurso = float('inf')
            tempo_sem_progresso_recurso = 0
            angulos_visitados = set()
            ultimos_angulos = []
            tempo_sem_coletar = 0
            ultimo_recurso_coletado = 0
            posicoes_visitadas = set()
            ultimas_posicoes = []
            colisoes_consecutivas = 0

            max_passos = 500
            passos = 0

            while passos < max_passos and individuo.estado != "TAREFA_COMPLETA": # --- NOVO: Parar se tarefa completa
                sensores = robo.get_sensores(ambiente)
                sensores['x'] = robo.x
                sensores['y'] = robo.y
                sensores['recursos_coletados'] = robo.recursos_coletados
                sensores['total_recursos'] = len(ambiente.recursos)

                if robo.recursos_coletados == ultimo_recurso_coletado:
                    tempo_sem_coletar += 1
                else:
                    tempo_sem_coletar = 0
                    ultimo_recurso_coletado = robo.recursos_coletados

                if tempo_sem_coletar > 150:
                    fitness -= 1000  # Penalidade moderada
                    break

                posicao_atual = (round(robo.x, 1), round(robo.y, 1))
                posicoes_visitadas.add(posicao_atual)
                ultimas_posicoes.append(posicao_atual)
                if len(ultimas_posicoes) > 20:
                    ultimas_posicoes.pop(0)

                angulo_atual = sensores['angulo_atual'] # Precisa pegar o angulo atual antes
                angulos_visitados.add(round(angulo_atual, 2)) # Mantem o registro
                ultimos_angulos.append(angulo_atual)
                if len(ultimos_angulos) > 20: # Aumentar janela de ângulos para 20 passos também
                    ultimos_angulos.pop(0)

                # --- PENALIDADE REVISADA PARA GIRO/OSCILAÇÃO ---
                if len(ultimas_posicoes) >= 20 and len(ultimos_angulos) >= 20:
                    # Deslocamento líquido nos últimos 20 passos
                    deslocamento_liquido = np.hypot(ultimas_posicoes[-1][0] - ultimas_posicoes[0][0],
                                                  ultimas_posicoes[-1][1] - ultimas_posicoes[0][1])

                    # Variação angular total nos últimos 20 passos (soma das diferenças absolutas)
                    variacao_angular_total = 0
                    for i in range(len(ultimos_angulos) - 1):
                        diff = ultimos_angulos[i+1] - ultimos_angulos[i]
                        # Normalizar diferença para lidar com a volta de -pi para pi
                        while diff <= -np.pi: diff += 2 * np.pi
                        while diff > np.pi: diff -= 2 * np.pi
                        variacao_angular_total += abs(diff)

                    # Se girou muito (ex: > 2 voltas) E andou pouco (ex: < raio do robô * 5)
                    raio_robo = 10 # Valor padrão do raio do robô
                    if variacao_angular_total > (4 * np.pi) and deslocamento_liquido < (raio_robo * 5):
                        fitness -= 5000  # Penalidade MUITO FORTE por girar em círculos
                        # print(f"[DIAGNÓSTICO] Penalidade Giro Forte: var_ang={variacao_angular_total:.2f}, desloc={deslocamento_liquido:.2f}") # Debug
                        break # Interrompe a avaliação deste indivíduo

                    # Penalidade menor se apenas girou muito (sem verificar deslocamento)
                    elif variacao_angular_total > (6 * np.pi): # Girou mais de 3 voltas nos últimos 20 passos
                         fitness -= 2500 # Penalidade moderada
                         # print(f"[DIAGNÓSTICO] Penalidade Giro Moderada: var_ang={variacao_angular_total:.2f}") # Debug
                         break # Interrompe

                # --- FIM PENALIDADE REVISADA ---

                individuo.atualizar_estado(sensores)

                aceleracao = max(-1, min(1, individuo.avaliar(sensores, "aceleracao")))
                rotacao = max(-0.5, min(0.5, individuo.avaliar(sensores, "rotacao")))
                # Removido print de diagnóstico

                if individuo.recurso_atual:
                    distancia_atual = np.hypot(robo.x - individuo.recurso_atual["x"],
                                            robo.y - individuo.recurso_atual["y"])
                    if distancia_atual >= ultima_distancia_recurso:
                        tempo_sem_progresso_recurso += 1
                    else:
                        tempo_sem_progresso_recurso = 0
                    ultima_distancia_recurso = distancia_atual

                distancia_movimento = np.hypot(robo.x - ultima_posicao[0],
                                            robo.y - ultima_posicao[1])
                if distancia_movimento < 0.1:
                    tempo_sem_movimento += 1
                else:
                    tempo_sem_movimento = 0
                ultima_posicao = (robo.x, robo.y)

                sem_energia = robo.mover(aceleracao, rotacao, ambiente)

                if robo.colisoes > 0 and ultima_colisao:
                    colisoes_consecutivas += 1
                ultima_colisao = robo.colisoes > 0

                if tempo_sem_progresso_recurso > 30 or tempo_sem_movimento > 15:
                    fitness -= 2000
                    break

                if sem_energia or ambiente.passo():
                    break

                        # --- NOVO CÁLCULO DE FITNESS ---
            fitness_tentativa = 0
            todos_recursos_coletados = (robo.recursos_coletados == len(ambiente.recursos))
            tarefa_completa = (individuo.estado == "TAREFA_COMPLETA")

            # Recompensa por cada recurso coletado
            fitness_tentativa += robo.recursos_coletados * 3000

            # Bônus por coletar TODOS os recursos
            if todos_recursos_coletados:
                fitness_tentativa += 10000

                # Bônus por atingir a meta APÓS coletar todos os recursos (TAREFA_COMPLETA)
                if tarefa_completa:
                    fitness_tentativa += 20000 # Bônus MÁXIMO por completar tudo e parar
                else:
                    # Penalidade pela distância até a meta se não foi atingida (após coletar tudo)
                    dist_meta_final = np.sqrt((robo.x - ambiente.meta["x"])**2 + (robo.y - ambiente.meta["y"])**2)
                    fitness_tentativa -= dist_meta_final * 15 # Aumentei a penalidade

            # Penalidade FORTE por colisões (AUMENTADA)
            fitness_tentativa -= robo.colisoes * 1500 # Aumentei ainda mais

            # Penalidade por colisões consecutivas (AUMENTADA)
            fitness_tentativa -= colisoes_consecutivas * 300 # Aumentei também

            # --- PENALIDADE POR FALTA DE PROGRESSO (REVISADA) ---
            # Penalidade por ficar parado (tempo_sem_movimento)
            fitness_tentativa -= tempo_sem_movimento * 150 # Aumentei a penalidade
            # Penalidade se o robô percorreu pouca distância total (sugere oscilação ou travamento)
            if robo.distancia_percorrida < 50 and not tarefa_completa:
                 fitness_tentativa -= 5000 # Penalidade se quase não saiu do lugar
            # Penalidade se ficou muito tempo sem coletar recurso
            fitness_tentativa -= tempo_sem_coletar * 10 # Aumentei a penalidade
            # --- FIM PENALIDADE REVISADA ---

            # Penalidade por energia gasta
            fitness_tentativa -= (100 - robo.energia) * 5

            # Penalidade por não coletar nenhum recurso
            if robo.recursos_coletados == 0:
                fitness_tentativa -= 5000

            # Penalidade por esgotar energia ou tempo sem completar
            if sem_energia and not tarefa_completa:
                 fitness_tentativa -= 7000 # Aumentei
            if passos >= max_passos and not tarefa_completa:
                 fitness_tentativa -= 7000 # Aumentei

            # Pequena penalidade pela distância percorrida para incentivar eficiência (mantida)
            fitness_tentativa -= robo.distancia_percorrida * 0.5

            fitness += max(-100000, fitness_tentativa) # Adiciona um piso

        # Média das tentativas
        return fitness / num_tentativas if num_tentativas > 0 else 0

    def avaliar_populacao(self):
        # Criar pool de processos
        with mp.Pool(processes=self.num_processos) as pool:
            # Avaliar população em paralelo
            fitness_values = pool.map(self.avaliar_individuo, self.populacao)
            
            # Atualizar fitness dos indivíduos
            for individuo, fitness in zip(self.populacao, fitness_values):
                individuo.fitness = fitness
                if fitness > self.melhor_fitness:
                    self.melhor_fitness = fitness
                    self.melhor_individuo = individuo
    
    def calcular_media_fitness(self):
        return sum(ind.fitness for ind in self.populacao) / len(self.populacao)
    
    def selecionar(self):
        # Seleção por torneio com elitismo
        tamanho_torneio = 5  # Aumentado para maior pressão seletiva
        selecionados = []
        
        # Manter os 10% melhores indivíduos
        n_elite = max(1, int(self.tamanho_populacao * 0.1))
        elite = sorted(self.populacao, key=lambda x: x.fitness, reverse=True)[:n_elite]
        selecionados.extend(elite)
        
        # Selecionar o resto da população por torneio
        while len(selecionados) < self.tamanho_populacao:
            torneio = random.sample(self.populacao, tamanho_torneio)
            vencedor = max(torneio, key=lambda x: x.fitness)
            selecionados.append(vencedor)
        
        return selecionados
    
    def evoluir(self, n_geracoes=35):
        print(f"Iniciando evolução com {self.num_processos} processos...")
        
        for geracao in range(n_geracoes):
            print(f"\nGeração {geracao + 1}/{n_geracoes}")
            
            # Avaliar população em paralelo
            self.avaliar_populacao()
            
            # Calcular média do fitness
            media_fitness = self.calcular_media_fitness()
            
            # Registrar histórico
            self.historico_fitness.append(self.melhor_fitness)
            self.historico_media.append(media_fitness)
            
            # Mostrar informações da geração
            print(f"Melhor fitness: {self.melhor_fitness:.2f}")
            print(f"Média do fitness: {media_fitness:.2f}")
            
            # Selecionar indivíduos
            selecionados = self.selecionar()
            
            # Criar nova população
            nova_populacao = []
            nova_populacao.append(self.melhor_individuo)
            
            while len(nova_populacao) < self.tamanho_populacao:
                pai1, pai2 = random.sample(selecionados, 2)
                filho = pai1.crossover(pai2)
                filho.mutacao(probabilidade=0.15) # Mutação aumentada para 0.15
                nova_populacao.append(filho)
            
            self.populacao = nova_populacao
        
        return self.melhor_individuo, self.historico_fitness, self.historico_media

# =====================================================================
# PARTE 3: EXECUÇÃO DO PROGRAMA (PARA O ALUNO MODIFICAR)
# =====================================================================

if __name__ == "__main__":
    try:
        print("Iniciando simulação de robô com programação genética...")
        
        # Criar e treinar o algoritmo genético
        print("Treinando o algoritmo genético...")
        pg = ProgramacaoGenetica(tamanho_populacao=200, profundidade=5) # Profundidade aumentada para 5
        
        # Verificar se o número de processos está correto
        if pg.num_processos < 1:
            pg.num_processos = 1
            print("Aviso: Número de processos ajustado para 1")
        
        print(f"Usando {pg.num_processos} processos para avaliação")
        melhor_individuo, historico, historico_media = pg.evoluir(n_geracoes=20) # Gerações ajustadas para 20
        
        if melhor_individuo is None:
            raise Exception("Nenhum indivíduo válido foi encontrado durante a evolução")
        
        # Salvar o melhor indivíduo
        print("Salvando o melhor indivíduo...")
        try:
            melhor_individuo.salvar('melhor_robo.json')
        except Exception as e:
            print(f"Erro ao salvar o melhor indivíduo: {str(e)}")
        
        # Plotar evolução do fitness
        print("Plotando evolução do fitness...")
        try:
            plt.figure(figsize=(12, 6))
            plt.plot(historico, label='Melhor Fitness', color='blue')
            plt.plot(historico_media, label='Média do Fitness', color='red', linestyle='--')
            plt.title('Evolução do Fitness')
            plt.xlabel('Geração')
            plt.ylabel('Fitness')
            plt.legend()
            plt.grid(True)
            plt.savefig('evolucao_fitness_robo.png')
            plt.close()
        except Exception as e:
            print(f"Erro ao plotar gráfico: {str(e)}")
        
        # Simular o melhor indivíduo
        print("Simulando o melhor indivíduo...")
        ambiente = Ambiente()
        robo = Robo(ambiente.largura // 2, ambiente.altura // 2)
        simulador = Simulador(ambiente, robo, melhor_individuo)
        
        print("Executando simulação em tempo real...")
        print("A simulação será exibida em uma janela separada.")
        print("Pressione Ctrl+C para fechar a janela quando desejar.")
        simulador.simular()
        
    except KeyboardInterrupt:
        print("\nSimulação interrompida pelo usuário")
    except Exception as e:
        print(f"\nErro durante a execução: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # Garantir que todos os processos sejam fechados
        try:
            import multiprocessing as mp
            mp.get_context('spawn').Pool().close()
        except:
            pass 