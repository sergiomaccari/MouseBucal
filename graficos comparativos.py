import pandas as pd
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# --- CONFIGURAÇÃO ---
# Defina aqui o caminho da pasta onde o jogo salva os arquivos
PASTA_CSV = "D:\Trabalhos UTFPR\Oficinas" 

class GraficoAgilidade:
    def __init__(self, root):
        self.root = root
        self.root.title("Analisador de Tempos de Reação")
        self.root.geometry("1000x700")
        
        self.arquivos_selecionados = []
        self.dados = {}
        
        # Carregar automaticamente os arquivos da pasta configurada
        self.carregar_pasta_automatica()
        
        self.criar_interface()
    
    def carregar_pasta_automatica(self):
        """Carrega automaticamente os arquivos CSV da pasta configurada"""
        if os.path.exists(PASTA_CSV) and os.path.isdir(PASTA_CSV):
            print(f"Procurando arquivos CSV na pasta: {PASTA_CSV}")
            
            arquivos_encontrados = 0
            for arquivo in os.listdir(PASTA_CSV):
                if arquivo.endswith('.csv') and 'teste_agilidade' in arquivo:
                    caminho_completo = os.path.join(PASTA_CSV, arquivo)
                    self.arquivos_selecionados.append(caminho_completo)
                    arquivos_encontrados += 1
                    print(f"✓ Encontrado: {arquivo}")
            
            if arquivos_encontrados > 0:
                print(f"Total de arquivos encontrados: {arquivos_encontrados}")
            else:
                print("❌ Nenhum arquivo CSV encontrado na pasta especificada.")
                print("   Certifique-se de que os arquivos têm 'teste_agilidade' no nome.")
        else:
            print(f"❌ Pasta não encontrada: {PASTA_CSV}")
            print("   Verifique o caminho configurado na variável PASTA_CSV")
    
    def criar_interface(self):
        # Frame principal
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame de informações da pasta
        info_frame = tk.Frame(main_frame, bg="#e8f4fd", relief=tk.RAISED, bd=1)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        info_text = f"Pasta configurada: {os.path.abspath(PASTA_CSV)} | Arquivos carregados: {len(self.arquivos_selecionados)}"
        tk.Label(info_frame, text=info_text, bg="#e8f4fd", font=("Arial", 9)).pack(pady=5)
        
        # Frame de controles
        control_frame = tk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Botões de seleção de arquivos
        btn_frame = tk.Frame(control_frame)
        btn_frame.pack(fill=tk.X)
        
        tk.Button(btn_frame, text="Selecionar Arquivo CSV", 
                 command=self.selecionar_arquivo, width=20).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(btn_frame, text="Selecionar Outra Pasta", 
                 command=self.selecionar_pasta, width=20).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(btn_frame, text="Recarregar Pasta Configurada", 
                 command=self.recarregar_pasta, width=20, bg="#FFE4B2").pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(btn_frame, text="Limpar Seleção", 
                 command=self.limpar_selecao, width=15).pack(side=tk.LEFT, padx=(0, 10))
        
        # Frame de opções
        options_frame = tk.Frame(control_frame)
        options_frame.pack(fill=tk.X, pady=10)
        
        # Checkboxes para opções de visualização
        self.var_media = tk.BooleanVar(value=True)
        self.var_linhas = tk.BooleanVar(value=True)
        self.var_pontos = tk.BooleanVar(value=True)
        self.var_tendencia = tk.BooleanVar(value=False)
        
        tk.Checkbutton(options_frame, text="Mostrar Média", 
                      variable=self.var_media).pack(side=tk.LEFT, padx=(0, 15))
        tk.Checkbutton(options_frame, text="Mostrar Linhas", 
                      variable=self.var_linhas).pack(side=tk.LEFT, padx=(0, 15))
        tk.Checkbutton(options_frame, text="Mostrar Pontos", 
                      variable=self.var_pontos).pack(side=tk.LEFT, padx=(0, 15))
        tk.Checkbutton(options_frame, text="Linha de Tendência", 
                      variable=self.var_tendencia).pack(side=tk.LEFT, padx=(0, 15))
        
        # Botão para gerar gráfico
        tk.Button(options_frame, text="Gerar Gráfico", 
                 command=self.gerar_grafico, bg="#4CAF50", fg="white", width=15,
                 font=("Arial", 10, "bold")).pack(side=tk.RIGHT)
        
        # Lista de arquivos selecionados
        lista_frame = tk.Frame(main_frame)
        lista_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(lista_frame, text="Arquivos Selecionados:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        
        self.lista_arquivos = tk.Listbox(lista_frame, height=4)
        self.lista_arquivos.pack(fill=tk.X, pady=(5, 0))
        
        # Atualizar lista com arquivos carregados automaticamente
        self.atualizar_lista_arquivos()
        
        # Frame do gráfico
        graph_frame = tk.Frame(main_frame)
        graph_frame.pack(fill=tk.BOTH, expand=True)
        
        # Criar figura do matplotlib
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Frame de estatísticas
        self.stats_frame = tk.Frame(main_frame)
        self.stats_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Gerar gráfico automaticamente se houver arquivos
        if self.arquivos_selecionados:
            self.root.after(1000, self.gerar_grafico)  # Gerar após 1 segundo
    
    def recarregar_pasta(self):
        """Recarrega os arquivos da pasta configurada"""
        self.arquivos_selecionados.clear()
        self.carregar_pasta_automatica()
        self.atualizar_lista_arquivos()
        
        if self.arquivos_selecionados:
            messagebox.showinfo("Recarregado", 
                               f"Carregados {len(self.arquivos_selecionados)} arquivos da pasta configurada.")
            self.gerar_grafico()
        else:
            messagebox.showwarning("Aviso", 
                                  "Nenhum arquivo encontrado na pasta configurada.")
    
    def selecionar_arquivo(self):
        arquivos = filedialog.askopenfilenames(
            title="Selecione os arquivos CSV",
            filetypes=[("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")]
        )
        
        for arquivo in arquivos:
            if arquivo not in self.arquivos_selecionados:
                self.arquivos_selecionados.append(arquivo)
                self.atualizar_lista_arquivos()
    
    def selecionar_pasta(self):
        pasta = filedialog.askdirectory(title="Selecione a pasta com arquivos CSV")
        
        if pasta:
            arquivos_adicionados = 0
            for arquivo in os.listdir(pasta):
                if arquivo.endswith('.csv') and 'teste_agilidade' in arquivo:
                    caminho_completo = os.path.join(pasta, arquivo)
                    if caminho_completo not in self.arquivos_selecionados:
                        self.arquivos_selecionados.append(caminho_completo)
                        arquivos_adicionados += 1
            
            self.atualizar_lista_arquivos()
            
            if arquivos_adicionados > 0:
                messagebox.showinfo("Sucesso", f"Adicionados {arquivos_adicionados} arquivos.")
                self.gerar_grafico()
            else:
                messagebox.showwarning("Aviso", "Nenhum arquivo CSV encontrado na pasta selecionada.")
    
    def limpar_selecao(self):
        self.arquivos_selecionados.clear()
        self.atualizar_lista_arquivos()
        self.ax.clear()
        self.canvas.draw()
        self.limpar_estatisticas()
    
    def atualizar_lista_arquivos(self):
        self.lista_arquivos.delete(0, tk.END)
        for arquivo in self.arquivos_selecionados:
            nome_arquivo = os.path.basename(arquivo)
            self.lista_arquivos.insert(tk.END, nome_arquivo)
    
    def carregar_dados(self):
        """Carrega os dados dos arquivos CSV selecionados de forma flexível"""
        self.dados.clear()
        
        for arquivo in self.arquivos_selecionados:
            try:
                df = pd.read_csv(arquivo)
                nome_arquivo = os.path.basename(arquivo)
                
                # Verificar se as colunas esperadas existem
                if 'Tempo_Reacao(s)' in df.columns and 'Numero_Clique' in df.columns:
                    # Carrega todos os dados, independente se são 15, 30 ou outro número
                    dados_df = df.copy()
                    
                    if len(dados_df) > 0:
                        self.dados[nome_arquivo] = dados_df
                    else:
                        print(f"Aviso: {nome_arquivo} está vazio")
                else:
                    print(f"Erro: {nome_arquivo} não tem as colunas esperadas")
                    
            except Exception as e:
                print(f"Erro ao carregar {arquivo}: {str(e)}")
    
    def gerar_grafico(self):
        """Gera o gráfico ajustando-se automaticamente ao número de cliques"""
        if not self.arquivos_selecionados:
            messagebox.showwarning("Aviso", "Nenhum arquivo CSV selecionado.")
            return
        
        self.carregar_dados()
        
        if not self.dados:
            messagebox.showwarning("Aviso", "Nenhum dado válido foi carregado.")
            return
        
        self.ax.clear()
        
        # Cores para diferentes arquivos
        cores = plt.cm.Set3(np.linspace(0, 1, len(self.dados)))
        
        # Descobre qual é o número máximo de cliques entre todos os arquivos carregados
        max_cliques = 0
        for df in self.dados.values():
            if len(df) > max_cliques:
                max_cliques = len(df)
        
        # Preparar dados para a média geral
        todos_tempos = []
        
        for i, (nome_arquivo, df) in enumerate(self.dados.items()):
            tempos = df['Tempo_Reacao(s)'].values
            num_cliques_arquivo = len(tempos)
            
            # Normaliza o tamanho dos arrays para o cálculo da média
            if num_cliques_arquivo < max_cliques:
                # Preenche com NaN se for menor que o máximo
                tempos_pad = np.pad(tempos, (0, max_cliques - num_cliques_arquivo), 'constant', constant_values=np.nan)
            else:
                tempos_pad = tempos[:max_cliques]
            
            todos_tempos.append(tempos_pad)
            
            # Plotar dados individuais
            x = np.arange(1, num_cliques_arquivo + 1)
            cor = cores[i]
            label = nome_arquivo.replace('teste_agilidade_', '').replace('.csv', '')
            
            if self.var_linhas.get():
                self.ax.plot(x, tempos, color=cor, alpha=0.7, linewidth=1.5, label=label)
            
            if self.var_pontos.get():
                self.ax.scatter(x, tempos, color=cor, alpha=0.8, s=50)
        
        # Calcular e plotar média geral
        if len(todos_tempos) > 0 and self.var_media.get():
            # numpy nanmean ignora os NaNs, permitindo médias entre arquivos de tamanhos diferentes
            media_geral = np.nanmean(todos_tempos, axis=0)
            
            # Remove NaNs do final se a média for mais curta (para visualização limpa)
            mask_validos = ~np.isnan(media_geral)
            x_media = np.arange(1, max_cliques + 1)[mask_validos]
            y_media = media_geral[mask_validos]

            self.ax.plot(x_media, y_media, color='red', linewidth=3, 
                         label='Média Geral', linestyle='--', marker='o', markersize=6)
            
            # Adicionar linha de tendência se solicitado
            if self.var_tendencia.get() and len(x_media) > 1:
                z = np.polyfit(x_media, y_media, 1)
                p = np.poly1d(z)
                self.ax.plot(x_media, p(x_media), "r--", alpha=0.8, linewidth=2, 
                             label='Tendência (média)')
        
        # Configurar o gráfico
        self.ax.set_xlabel('Número do Clique', fontsize=12, fontweight='bold')
        self.ax.set_ylabel('Tempo de Reação (segundos)', fontsize=12, fontweight='bold')
        self.ax.set_title(f'Tempo de Reação ({max_cliques} Cliques)', 
                          fontsize=14, fontweight='bold', pad=20)
        
        # Ajusta o eixo X dinamicamente
        self.ax.set_xticks(range(1, max_cliques + 1))
        self.ax.grid(True, alpha=0.3)
        self.ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # Ajustar layout
        self.fig.tight_layout()
        self.canvas.draw()
        
        # Mostrar estatísticas
        self.mostrar_estatisticas()
    
    def mostrar_estatisticas(self):
        # Limpar frame de estatísticas
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        if len(self.dados) == 0:
            return
        
        # Calcular estatísticas gerais
        todos_tempos = []
        for df in self.dados.values():
            tempos_validos = df['Tempo_Reacao(s)'].dropna()
            todos_tempos.extend(tempos_validos)
        
        if not todos_tempos:
            return
        
        todos_tempos = np.array(todos_tempos)
        
        # Criar frame para estatísticas
        stats_text = f"""
        ESTATÍSTICAS GERAIS ({len(self.dados)} testes):
        • Média geral: {np.mean(todos_tempos):.3f}s
        • Desvio padrão: {np.std(todos_tempos):.3f}s
        • Melhor tempo: {np.min(todos_tempos):.3f}s
        • Pior tempo: {np.max(todos_tempos):.3f}s
        • Mediana: {np.median(todos_tempos):.3f}s
        • Coeficiente de variação: {(np.std(todos_tempos)/np.mean(todos_tempos)*100):.1f}%
        """
        
        tk.Label(self.stats_frame, text=stats_text, justify=tk.LEFT, 
                font=("Courier", 9), bg="#f0f0f0", relief=tk.SUNKEN, bd=1).pack(fill=tk.X, padx=5, pady=5)
    
    def limpar_estatisticas(self):
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

def main():
    root = tk.Tk()
    app = GraficoAgilidade(root)
    root.mainloop()

if __name__ == "__main__":
    main()