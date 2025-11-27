







import pygame
import sys
import random
import csv
import os
from datetime import datetime

# --- CONFIGURAÇÕES GERAIS ---
TOTAL_CLIQUES = 15  # Alterado de 30 para 15
LARGURA_AREA_TEXTO = 300  # Área reservada para o texto na esquerda

# Constantes de tamanho dos quadrados
PEQUENO = 15
MEDIO = 25
GRANDE = 35
TAMANHOS_QUADRADO = [PEQUENO, MEDIO, GRANDE]
NOMES_TAMANHOS = {PEQUENO: "Pequeno", MEDIO: "Médio", GRANDE: "Grande"}

def posicao_aleatoria(tamanho_quadrado):
    """Gera uma posição aleatória que não sobrepõe os botões NEM O TEXTO"""
    while True:
        # Gera X e Y dentro dos limites da tela
        x = random.randint(0, LARGURA - tamanho_quadrado)
        y = random.randint(0, ALTURA - tamanho_quadrado)
        
        # Cria o retangulo do quadrado potencial
        quadrado_rect = pygame.Rect(x, y, tamanho_quadrado, tamanho_quadrado)
        
        # 1. Verifica colisão com botões (Direita Superior)
        botao_liga_rect = pygame.Rect(botao_liga_x, botao_liga_y, LARGURA_BOTAO, ALTURA_BOTAO)
        botao_teste_rect = pygame.Rect(botao_teste_x, botao_teste_y, LARGURA_BOTAO, ALTURA_BOTAO)
        
        # 2. Verifica colisão com área de texto (Esquerda)
        # Define uma área do topo até 400px de altura na esquerda
        area_texto_rect = pygame.Rect(0, 0, LARGURA_AREA_TEXTO, 400)
        
        # Se não bater em nada, retorna a posição
        if not (quadrado_rect.colliderect(botao_liga_rect) or 
                quadrado_rect.colliderect(botao_teste_rect) or
                quadrado_rect.colliderect(area_texto_rect)):
            return x, y

def cor_aleatoria():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def obter_tamanho_aleatorio():
    """Retorna um tamanho aleatório para o quadrado"""
    return random.choice(TAMANHOS_QUADRADO)

def salvar_dados():
    """Salva os dados coletados em um arquivo CSV"""
    if not tempos_cliques:
        return
    
    if not os.path.exists('dados'):
        os.makedirs('dados')
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_arquivo = f'dados/teste_agilidade_{timestamp}.csv'
    
    with open(nome_arquivo, 'w', newline='', encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo)
        writer.writerow(['Numero_Clique', 'Tempo_Reacao(s)', 'Tamanho_Alvo', 'Timestamp'])
        
        for i, (tempo, tamanho) in enumerate(zip(tempos_cliques, tamanhos_cliques), 1):
            writer.writerow([i, tempo, NOMES_TAMANHOS[tamanho], datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    
    print(f"Dados salvos em: {nome_arquivo}")

def iniciar_teste_cliques():
    """Reinicia todas as variáveis para um novo teste"""
    global contador_cliques, tempo_inicio, tempo_ultimo, soma_tempos, tempos_cliques, teste_concluido
    global cliques_errados, tamanhos_cliques, tamanho_atual, programa_ligado
    
    contador_cliques = 0
    tempo_ultimo = 0.0
    soma_tempos = 0.0
    tempos_cliques = []
    tamanhos_cliques = []
    cliques_errados = 0
    teste_concluido = False
    programa_ligado = True # Garante que o programa liga ao iniciar
    
    # Reseta o tempo APENAS AGORA, no início do teste
    tempo_inicio = pygame.time.get_ticks()
    
    tamanho_atual = obter_tamanho_aleatorio()
    quadrado_x, quadrado_y = posicao_aleatoria(tamanho_atual)
    return quadrado_x, quadrado_y

pygame.init()

LARGURA = 800
ALTURA = 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption(f"Teste de Agilidade - {TOTAL_CLIQUES} Cliques")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 100, 255)
CINZA = (200, 200, 200)
VERDE_CLARO = (100, 255, 100)
VERMELHO_CLARO = (255, 100, 100)
AZUL_CLARO = (100, 200, 255)
AMARELO = (255, 255, 0)
LARANJA = (255, 165, 0)

LARGURA_BOTAO = 150
ALTURA_BOTAO = 40
ESPACAMENTO_BOTOES = 10

# Variáveis do programa
contador_cliques = 0
tempo_inicio = 0 # Começa zerado
tempo_decorrido = 0.0
tempo_ultimo = 0.0
soma_tempos = 0.0
programa_ligado = False
teste_concluido = False
cliques_errados = 0
tempos_cliques = []
tamanhos_cliques = []
tamanho_atual = MEDIO

# Posições dos botões
botao_liga_x = LARGURA - LARGURA_BOTAO - 20
botao_liga_y = 20

botao_teste_x = LARGURA - LARGURA_BOTAO - 20
botao_teste_y = botao_liga_y + ALTURA_BOTAO + ESPACAMENTO_BOTOES

quadrado_x = 400 # Posição inicial segura
quadrado_y = 300
cor_quadrado = VERDE

fonte = pygame.font.SysFont(None, 30)
fonte_pequena = pygame.font.SysFont(None, 24)
fonte_grande = pygame.font.SysFont(None, 36)

while True:
    tempo_atual_tick = pygame.time.get_ticks()
    
    # Lógica do cronômetro: Só conta se estiver ligado E teste não acabou
    if programa_ligado and not teste_concluido:
        tempo_decorrido = (tempo_atual_tick - tempo_inicio) / 1000
    elif not programa_ligado:
        tempo_decorrido = 0.0
    # Se teste concluído, mantém o último tempo decorrido congelado na tela

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            if tempos_cliques:
                salvar_dados()
            pygame.quit()
            sys.exit()
        
        if evento.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = evento.pos
            
            # Botão LIGA/DESLIGA
            if (botao_liga_x <= mouse_x <= botao_liga_x + LARGURA_BOTAO) and \
               (botao_liga_y <= mouse_y <= botao_liga_y + ALTURA_BOTAO):
                programa_ligado = not programa_ligado
                if programa_ligado:
                    quadrado_x, quadrado_y = iniciar_teste_cliques()
                else:
                    if tempos_cliques:
                        salvar_dados()
            
            # Botão INICIAR TESTE
            elif (botao_teste_x <= mouse_x <= botao_teste_x + LARGURA_BOTAO) and \
                 (botao_teste_y <= mouse_y <= botao_teste_y + ALTURA_BOTAO):
                quadrado_x, quadrado_y = iniciar_teste_cliques()
            
            # Clique no Quadrado Alvo
            elif programa_ligado and not teste_concluido:
                if (quadrado_x <= mouse_x <= quadrado_x + tamanho_atual) and \
                   (quadrado_y <= mouse_y <= quadrado_y + tamanho_atual):
                    
                    tempo_ultimo = tempo_decorrido # Pega o tempo exato do clique
                    soma_tempos += tempo_ultimo
                    tempos_cliques.append(tempo_ultimo)
                    tamanhos_cliques.append(tamanho_atual)
                    
                    contador_cliques += 1
                    
                    # Reinicia o timer para medir o tempo "entre cliques" ou mantém contínuo?
                    # O código original mantinha contínuo (tempo total).
                    # Se quiser medir reflexo por clique, descomente a linha abaixo:
                    # tempo_inicio = pygame.time.get_ticks() 
                    
                    if contador_cliques >= TOTAL_CLIQUES:
                        teste_concluido = True
                        salvar_dados()
                    else:
                        tamanho_atual = obter_tamanho_aleatorio()
                        quadrado_x, quadrado_y = posicao_aleatoria(tamanho_atual)
                        # Reinicia timer a cada clique para medir tempo de reação individual
                        tempo_inicio = pygame.time.get_ticks() 
                        cor_quadrado = cor_aleatoria()
                
                else:
                    # Clique fora (apenas se não clicou nos botões ou área proibida)
                    # Verifica se o clique não foi na área de texto antes de contar erro
                    if mouse_x > LARGURA_AREA_TEXTO: 
                        cliques_errados += 1

    TELA.fill(BRANCO)

    # Calcula média
    if contador_cliques > 0:
        tempo_medio = soma_tempos / contador_cliques
    else:
        tempo_medio = 0.0

    # --- DESENHO DA INTERFACE ---
    
    # Desenha linha divisória da área de texto (opcional, para visualização)
    pygame.draw.line(TELA, CINZA, (LARGURA_AREA_TEXTO, 0), (LARGURA_AREA_TEXTO, ALTURA), 1)

    texto_contador = fonte.render(f"Cliques: {contador_cliques}/{TOTAL_CLIQUES}", True, PRETO)
    texto_tempo_atual = fonte.render(f"Atual: {tempo_decorrido:.2f}s", True, PRETO)
    texto_ultimo = fonte.render(f"Último: {tempo_ultimo:.2f}s", True, PRETO)
    texto_medio = fonte.render(f"Médio: {tempo_medio:.2f}s", True, PRETO)
    texto_errados = fonte.render(f"Erros: {cliques_errados}", True, VERMELHO)
    
    status_texto = "PROGRAMA: LIGADO" if programa_ligado else "PROGRAMA: DESLIGADO"
    status_cor = VERDE if programa_ligado else VERMELHO
    texto_status = fonte.render(status_texto, True, status_cor)
    
    if teste_concluido:
        status_teste = "TESTE CONCLUÍDO!"
        cor_teste = AMARELO
    else:
        status_teste = "EM ANDAMENTO" if programa_ligado else "AGUARDANDO"
        cor_teste = AZUL
    texto_teste = fonte.render(status_teste, True, cor_teste)
    
    if programa_ligado and not teste_concluido:
        tamanho_texto = f"Tamanho: {NOMES_TAMANHOS[tamanho_atual]}"
        texto_tamanho = fonte.render(tamanho_texto, True, LARANJA)
    else:
        texto_tamanho = fonte.render("Tamanho: -", True, LARANJA)

    # Posicionamento dos textos (Margem Esquerda)
    margem_x = 10
    TELA.blit(texto_contador, (margem_x, 10))
    TELA.blit(texto_tempo_atual, (margem_x, 40))
    TELA.blit(texto_ultimo, (margem_x, 70))
    TELA.blit(texto_medio, (margem_x, 100))
    TELA.blit(texto_errados, (margem_x, 130))
    TELA.blit(texto_status, (margem_x, 160))
    TELA.blit(texto_teste, (margem_x, 190))
    TELA.blit(texto_tamanho, (margem_x, 220))
    
    if tempos_cliques:
        texto_dados = fonte_pequena.render(f"Dados coletados: {len(tempos_cliques)}", True, PRETO)
        TELA.blit(texto_dados, (margem_x, 250))
        
        progresso = f"Progresso: {contador_cliques}/{TOTAL_CLIQUES} ({contador_cliques/TOTAL_CLIQUES*100:.0f}%)"
        texto_progresso = fonte_pequena.render(progresso, True, PRETO)
        TELA.blit(texto_progresso, (margem_x, 280))
        
        if contador_cliques + cliques_errados > 0:
            precisao = (contador_cliques / (contador_cliques + cliques_errados)) * 100
            texto_precisao = fonte_pequena.render(f"Precisão: {precisao:.1f}%", True, PRETO)
            TELA.blit(texto_precisao, (margem_x, 310))

    # --- DESENHO DOS OBJETOS ---

    # Quadrado alvo
    if programa_ligado and not teste_concluido:
        pygame.draw.rect(TELA, cor_quadrado, (quadrado_x, quadrado_y, tamanho_atual, tamanho_atual))
        pygame.draw.rect(TELA, PRETO, (quadrado_x, quadrado_y, tamanho_atual, tamanho_atual), 2)
    elif programa_ligado and teste_concluido:
        pygame.draw.rect(TELA, CINZA, (quadrado_x, quadrado_y, tamanho_atual, tamanho_atual))
    else:
        # Quando desligado, desenha cinza
        pygame.draw.rect(TELA, CINZA, (quadrado_x, quadrado_y, tamanho_atual, tamanho_atual))

    # Botão LIGA/DESLIGA
    cor_botao_liga = VERDE_CLARO if programa_ligado else VERMELHO_CLARO
    pygame.draw.rect(TELA, cor_botao_liga, (botao_liga_x, botao_liga_y, LARGURA_BOTAO, ALTURA_BOTAO))
    pygame.draw.rect(TELA, PRETO, (botao_liga_x, botao_liga_y, LARGURA_BOTAO, ALTURA_BOTAO), 2)
    
    texto_botao_liga = fonte.render("LIGAR/DESLIGAR", True, PRETO)
    texto_botao_liga_rect = texto_botao_liga.get_rect(center=(botao_liga_x + LARGURA_BOTAO//2, botao_liga_y + ALTURA_BOTAO//2))
    TELA.blit(texto_botao_liga, texto_botao_liga_rect)

    # Botão INICIAR TESTE
    cor_botao_teste = AZUL_CLARO if programa_ligado and not teste_concluido else CINZA
    pygame.draw.rect(TELA, cor_botao_teste, (botao_teste_x, botao_teste_y, LARGURA_BOTAO, ALTURA_BOTAO))
    pygame.draw.rect(TELA, PRETO, (botao_teste_x, botao_teste_y, LARGURA_BOTAO, ALTURA_BOTAO), 2)
    
    texto_botao_teste = fonte.render(f"INICIAR {TOTAL_CLIQUES}", True, PRETO)
    texto_botao_teste_rect = texto_botao_teste.get_rect(center=(botao_teste_x + LARGURA_BOTAO//2, botao_teste_y + ALTURA_BOTAO//2))
    TELA.blit(texto_botao_teste, texto_botao_teste_rect)

    pygame.display.update()