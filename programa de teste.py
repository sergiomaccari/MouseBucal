import pygame
import sys
import random
import csv
import os
from datetime import datetime

TOTAL_CLIQUES = 15
LARGURA_AREA_TEXTO = 300
DELAY_CLIQUE = 150

PEQUENO = 15
MEDIO = 25
GRANDE = 35
TAMANHOS_QUADRADO = [PEQUENO, MEDIO, GRANDE]
NOMES_TAMANHOS = {PEQUENO: "Pequeno", MEDIO: "Médio", GRANDE: "Grande"}

def posicao_aleatoria(tamanho_quadrado):
    while True:
        x = random.randint(LARGURA_AREA_TEXTO + 10, LARGURA - tamanho_quadrado)
        y = random.randint(0, ALTURA - tamanho_quadrado)
        
        quadrado_rect = pygame.Rect(x, y, tamanho_quadrado, tamanho_quadrado)
        
        botao_liga_rect = pygame.Rect(botao_liga_x, botao_liga_y, LARGURA_BOTAO, ALTURA_BOTAO)
        botao_teste_rect = pygame.Rect(botao_teste_x, botao_teste_y, LARGURA_BOTAO, ALTURA_BOTAO)
        
        if not (quadrado_rect.colliderect(botao_liga_rect) or 
                quadrado_rect.colliderect(botao_teste_rect)):
            return x, y

def cor_aleatoria():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def obter_tamanho_aleatorio():
    return random.choice(TAMANHOS_QUADRADO)

def salvar_dados():
    global dados_ja_salvos
    
    if not tempos_cliques or dados_ja_salvos:
        return
    
    if not os.path.exists('dados'):
        os.makedirs('dados')
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_arquivo = f'dados/teste_agilidade_{timestamp}.csv'
    
    try:
        with open(nome_arquivo, 'w', newline='', encoding='utf-8') as arquivo:
            writer = csv.writer(arquivo)
            writer.writerow(['Numero_Clique', 'Tempo_Reacao(s)', 'Tamanho_Alvo', 'Erros_Ate_Agora', 'Precisao_Atual(%)', 'Timestamp'])
            
            total_tentativas = len(tempos_cliques) + cliques_errados
            precisao_final = (len(tempos_cliques) / total_tentativas * 100) if total_tentativas > 0 else 0
            
            for i, (tempo, tamanho) in enumerate(zip(tempos_cliques, tamanhos_cliques), 1):
                writer.writerow([
                    i, 
                    tempo, 
                    NOMES_TAMANHOS[tamanho], 
                    cliques_errados, 
                    f"{precisao_final:.2f}", 
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ])
        
        print(f"Dados salvos em: {nome_arquivo}")
        dados_ja_salvos = True
        
    except Exception as e:
        print(f"Erro ao salvar arquivo: {e}")

def iniciar_teste_cliques():
    global contador_cliques, tempo_inicio, soma_tempos, tempos_cliques, teste_concluido
    global cliques_errados, tamanhos_cliques, tamanho_atual, programa_ligado, dados_ja_salvos
    global retangulo_alvo
    
    contador_cliques = 0
    soma_tempos = 0.0
    tempos_cliques = []
    tamanhos_cliques = []
    cliques_errados = 0
    teste_concluido = False
    programa_ligado = True 
    dados_ja_salvos = False
    
    tempo_inicio = pygame.time.get_ticks()
    
    tamanho_atual = obter_tamanho_aleatorio()
    x, y = posicao_aleatoria(tamanho_atual)
    retangulo_alvo = pygame.Rect(x, y, tamanho_atual, tamanho_atual)

pygame.init()

LARGURA = 800
ALTURA = 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption(f"Teste de Agilidade - {TOTAL_CLIQUES} Cliques")

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

contador_cliques = 0
tempo_inicio = 0 
tempo_decorrido = 0.0
tempo_ultimo = 0.0
soma_tempos = 0.0
programa_ligado = False
teste_concluido = False
dados_ja_salvos = False
cliques_errados = 0
tempos_cliques = [] 
tamanhos_cliques = [] 
tamanho_atual = MEDIO 
ultimo_clique_tick = 0

botao_liga_x = LARGURA - LARGURA_BOTAO - 20
botao_liga_y = 20
botao_teste_x = LARGURA - LARGURA_BOTAO - 20
botao_teste_y = botao_liga_y + ALTURA_BOTAO + ESPACAMENTO_BOTOES

retangulo_alvo = pygame.Rect(400, 300, MEDIO, MEDIO)
cor_quadrado = VERDE

fonte = pygame.font.SysFont(None, 30)
fonte_pequena = pygame.font.SysFont(None, 24)

while True:
    tempo_atual_tick = pygame.time.get_ticks()
    
    if programa_ligado and not teste_concluido:
        tempo_decorrido = (tempo_atual_tick - tempo_inicio) / 1000
    elif not programa_ligado:
        tempo_decorrido = 0.0

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            salvar_dados()
            pygame.quit()
            sys.exit()
        
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if tempo_atual_tick - ultimo_clique_tick < DELAY_CLIQUE:
                continue
            
            ultimo_clique_tick = tempo_atual_tick
            
            mouse_pos = evento.pos
            mouse_x, mouse_y = mouse_pos
            
            rect_botao_liga = pygame.Rect(botao_liga_x, botao_liga_y, LARGURA_BOTAO, ALTURA_BOTAO)
            rect_botao_teste = pygame.Rect(botao_teste_x, botao_teste_y, LARGURA_BOTAO, ALTURA_BOTAO)
            
            if rect_botao_liga.collidepoint(mouse_pos):
                programa_ligado = not programa_ligado
                if programa_ligado:
                    iniciar_teste_cliques()
                else:
                    salvar_dados()
                continue

            elif rect_botao_teste.collidepoint(mouse_pos):
                iniciar_teste_cliques()
                continue

            if programa_ligado and not teste_concluido:
                if retangulo_alvo.collidepoint(mouse_pos):
                    tempo_ultimo = tempo_decorrido
                    soma_tempos += tempo_ultimo
                    tempos_cliques.append(tempo_ultimo)
                    tamanhos_cliques.append(tamanho_atual)
                    
                    contador_cliques += 1
                    
                    if contador_cliques >= TOTAL_CLIQUES:
                        teste_concluido = True
                        salvar_dados()
                    else:
                        tamanho_atual = obter_tamanho_aleatorio()
                        x, y = posicao_aleatoria(tamanho_atual)
                        retangulo_alvo = pygame.Rect(x, y, tamanho_atual, tamanho_atual)
                        tempo_inicio = pygame.time.get_ticks() 
                        cor_quadrado = cor_aleatoria()
                
                else:
                    if mouse_x > LARGURA_AREA_TEXTO:
                        cliques_errados += 1

    TELA.fill(BRANCO)

    if contador_cliques > 0:
        tempo_medio = soma_tempos / contador_cliques
    else:
        tempo_medio = 0.0
        
    total_tentativas = contador_cliques + cliques_errados
    precisao = (contador_cliques / total_tentativas * 100) if total_tentativas > 0 else 0

    pygame.draw.line(TELA, CINZA, (LARGURA_AREA_TEXTO, 0), (LARGURA_AREA_TEXTO, ALTURA), 1)

    texto_contador = fonte.render(f"Cliques: {contador_cliques}/{TOTAL_CLIQUES}", True, PRETO)
    texto_tempo_atual = fonte.render(f"Atual: {tempo_decorrido:.2f}s", True, PRETO)
    texto_ultimo = fonte.render(f"Último: {tempo_ultimo:.2f}s", True, PRETO)
    texto_medio = fonte.render(f"Médio: {tempo_medio:.2f}s", True, PRETO)
    texto_errados = fonte.render(f"Erros: {cliques_errados}", True, VERMELHO)
    texto_precisao_tela = fonte.render(f"Precisão: {precisao:.1f}%", True, AZUL)
    
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

    margem_x = 10
    TELA.blit(texto_contador, (margem_x, 10))
    TELA.blit(texto_tempo_atual, (margem_x, 40))
    TELA.blit(texto_ultimo, (margem_x, 70))
    TELA.blit(texto_medio, (margem_x, 100))
    TELA.blit(texto_errados, (margem_x, 130))
    TELA.blit(texto_precisao_tela, (margem_x, 160))
    TELA.blit(texto_status, (margem_x, 200))
    TELA.blit(texto_teste, (margem_x, 230))
    TELA.blit(texto_tamanho, (margem_x, 260))
    
    if tempos_cliques:
        texto_dados = fonte_pequena.render(f"Dados coletados: {len(tempos_cliques)}", True, PRETO)
        TELA.blit(texto_dados, (margem_x, 290))
            
    if dados_ja_salvos and teste_concluido:
        texto_salvo = fonte_pequena.render("ARQUIVO SALVO!", True, VERDE)
        TELA.blit(texto_salvo, (margem_x, 320))

    if programa_ligado and not teste_concluido:
        pygame.draw.rect(TELA, cor_quadrado, retangulo_alvo)
        pygame.draw.rect(TELA, PRETO, retangulo_alvo, 2)
    elif programa_ligado and teste_concluido:
        pygame.draw.rect(TELA, CINZA, retangulo_alvo)
    else:
        pygame.draw.rect(TELA, CINZA, retangulo_alvo)

    cor_botao_liga = VERDE_CLARO if programa_ligado else VERMELHO_CLARO
    pygame.draw.rect(TELA, cor_botao_liga, (botao_liga_x, botao_liga_y, LARGURA_BOTAO, ALTURA_BOTAO))
    pygame.draw.rect(TELA, PRETO, (botao_liga_x, botao_liga_y, LARGURA_BOTAO, ALTURA_BOTAO), 2)
    
    texto_botao_liga = fonte.render("LIGAR/DESLIGAR", True, PRETO)
    texto_botao_liga_rect = texto_botao_liga.get_rect(center=(botao_liga_x + LARGURA_BOTAO//2, botao_liga_y + ALTURA_BOTAO//2))
    TELA.blit(texto_botao_liga, texto_botao_liga_rect)

    cor_botao_teste = AZUL_CLARO if programa_ligado and not teste_concluido else CINZA
    pygame.draw.rect(TELA, cor_botao_teste, (botao_teste_x, botao_teste_y, LARGURA_BOTAO, ALTURA_BOTAO))
    pygame.draw.rect(TELA, PRETO, (botao_teste_x, botao_teste_y, LARGURA_BOTAO, ALTURA_BOTAO), 2)
    
    texto_botao_teste = fonte.render(f"INICIAR {TOTAL_CLIQUES}", True, PRETO)
    texto_botao_teste_rect = texto_botao_teste.get_rect(center=(botao_teste_x + LARGURA_BOTAO//2, botao_teste_y + ALTURA_BOTAO//2))
    TELA.blit(texto_botao_teste, texto_botao_teste_rect)

    pygame.display.update()