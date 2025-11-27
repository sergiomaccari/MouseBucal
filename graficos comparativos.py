import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.cm as cm

PASTA_PADRAO = r"D:\Trabalhos UTFPR\Oficinas" 
COR_FUNDO = "#f0f0f0"
COR_DESTAQUE = "#4a7a8c"

class AnalisadorAgilidadeApp:
    def __init__(self, root):
        self.root = root
        self.configurar_janela()

        self.arquivos_selecionados = []
        self.dados_cache = {}
        
        self.var_media = tk.BooleanVar(value=True)
        self.var_linhas = tk.BooleanVar(value=True)
        self.var_pontos = tk.BooleanVar(value=True)
        self.var_tendencia = tk.BooleanVar(value=False)
        
        self.construir_interface()
        
        # Tentativa de carregamento automático
        self.carregar_pasta_inicial()

    def configurar_janela(self):
        self.root.title("Analisador de Performance - Agilidade e Reação")
        self.root.state('zoomed') # Maximizar janela
        self.root.configure(bg=COR_FUNDO)
        
        # Estilo para Treeview (Tabela)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="white", fieldbackground="white", rowheight=25)
        style.configure("Treeview.Heading", font=('Arial', 9, 'bold'), background="#e1e1e1")

    def construir_interface(self):
        # ================= LAYOUT PRINCIPAL (GRID) =================
        self.root.columnconfigure(0, weight=1) # Coluna esquerda (Controles)
        self.root.columnconfigure(1, weight=3) # Coluna direita (Gráfico e Tabela)
        self.root.rowconfigure(0, weight=1)

        # --- PAINEL ESQUERDO (CONTROLES) ---
        frame_esq = tk.Frame(self.root, bg="#e0e0e0", padx=10, pady=10, width=250)
        frame_esq.grid(row=0, column=0, sticky="nsew")
        frame_esq.grid_propagate(False) # Mantém largura fixa

        # Título Lateral
        tk.Label(frame_esq, text="CONTROLES", font=("Arial", 12, "bold"), bg="#e0e0e0", fg="#333").pack(pady=(0, 10))

        # Botões de Arquivo
        self.criar_botao(frame_esq, "📂 Selecionar Arquivos", self.selecionar_arquivos, "#ffffff").pack(fill=tk.X, pady=2)
        self.criar_botao(frame_esq, "📁 Selecionar Pasta", self.selecionar_pasta, "#ffffff").pack(fill=tk.X, pady=2)
        self.criar_botao(frame_esq, "🗑 Limpar Tudo", self.limpar_tudo, "#ffcccc").pack(fill=tk.X, pady=(10, 2))

        # Lista de Arquivos
        tk.Label(frame_esq, text="Arquivos Carregados:", bg="#e0e0e0", font=("Arial", 9)).pack(anchor="w", pady=(15, 0))
        self.lista_box = tk.Listbox(frame_esq, height=10, selectmode=tk.EXTENDED, font=("Consolas", 9))
        self.lista_box.pack(fill=tk.X, pady=2)
        
        # Opções do Gráfico
        tk.Label(frame_esq, text="Visualização:", bg="#e0e0e0", font=("Arial", 9, "bold")).pack(anchor="w", pady=(15, 5))
        tk.Checkbutton(frame_esq, text="Média Geral", variable=self.var_media, bg="#e0e0e0", command=self.atualizar_visualizacao).pack(anchor="w")
        tk.Checkbutton(frame_esq, text="Linhas Individuais", variable=self.var_linhas, bg="#e0e0e0", command=self.atualizar_visualizacao).pack(anchor="w")
        tk.Checkbutton(frame_esq, text="Mostrar Pontos", variable=self.var_pontos, bg="#e0e0e0", command=self.atualizar_visualizacao).pack(anchor="w")
        tk.Checkbutton(frame_esq, text="Linha de Tendência", variable=self.var_tendencia, bg="#e0e0e0", command=self.atualizar_visualizacao).pack(anchor="w")

        self.criar_botao(frame_esq, "🔄 ATUALIZAR", self.atualizar_visualizacao, COR_DESTAQUE, fg="white").pack(fill=tk.X, pady=20)

        self.lbl_status = tk.Label(frame_esq, text="Aguardando...", bg="#e0e0e0", fg="gray", wraplength=230, justify="left")
        self.lbl_status.pack(side=tk.BOTTOM, fill=tk.X)

        frame_dir = tk.Frame(self.root, bg=COR_FUNDO)
        frame_dir.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        frame_dir.rowconfigure(0, weight=2) # Gráfico ganha mais espaço
        frame_dir.rowconfigure(1, weight=1) # Tabela ganha menos espaço
        frame_dir.columnconfigure(0, weight=1)

        # 1. Área do Gráfico
        self.frame_grafico = tk.LabelFrame(frame_dir, text="Análise Gráfica", bg=COR_FUNDO)
        self.frame_grafico.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, self.frame_grafico)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        frame_inferior = tk.Frame(frame_dir, bg=COR_FUNDO)
        frame_inferior.grid(row=1, column=0, sticky="nsew")

        frame_resumo = tk.LabelFrame(frame_inferior, text="Estatísticas Globais", bg=COR_FUNDO, width=250)
        frame_resumo.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        frame_resumo.pack_propagate(False)
        
        self.txt_resumo = tk.Text(frame_resumo, bg="#f9f9f9", wrap=tk.WORD, font=("Consolas", 10), state="disabled", relief=tk.FLAT)
        self.txt_resumo.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        frame_tabela_container = tk.LabelFrame(frame_inferior, text="Dados por Participante", bg=COR_FUNDO)
        frame_tabela_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        colunas = ('arquivo', 'tempo_medio', 'melhor_tempo', 'erros', 'precisao')
        self.tabela = ttk.Treeview(frame_tabela_container, columns=colunas, show='headings')

        self.tabela.heading('arquivo', text='Arquivo / Participante')
        self.tabela.heading('tempo_medio', text='Média (s)')
        self.tabela.heading('melhor_tempo', text='Melhor (s)')
        self.tabela.heading('erros', text='Erros')
        self.tabela.heading('precisao', text='Precisão')

        self.tabela.column('arquivo', width=200, minwidth=100)
        self.tabela.column('tempo_medio', width=80, anchor='center')
        self.tabela.column('melhor_tempo', width=80, anchor='center')
        self.tabela.column('erros', width=60, anchor='center')
        self.tabela.column('precisao', width=80, anchor='center')

        sb_y = ttk.Scrollbar(frame_tabela_container, orient=tk.VERTICAL, command=self.tabela.yview)
        sb_x = ttk.Scrollbar(frame_tabela_container, orient=tk.HORIZONTAL, command=self.tabela.xview)
        self.tabela.configure(yscroll=sb_y.set, xscroll=sb_x.set)

        sb_y.pack(side=tk.RIGHT, fill=tk.Y)
        sb_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tabela.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def criar_botao(self, parent, texto, comando, cor_bg, fg="black"):
        return tk.Button(parent, text=texto, command=comando, bg=cor_bg, fg=fg, relief=tk.RAISED, bd=1, font=("Arial", 9))

    def log(self, mensagem):
        self.lbl_status.config(text=mensagem)
        self.root.update_idletasks()

    def ler_csv_inteligente(self, caminho):
        """
        Tenta ler o arquivo de todas as formas possíveis para evitar erros de encoding e separador.
        """
        tentativas = [
            ('utf-8', ','),
            ('utf-8', ';'),
            ('cp1252', ','),
            ('cp1252', ';'),
            ('latin1', ','),
            ('latin1', ';'),
        ]
        
        for encoding, sep in tentativas:
            try:
                df = pd.read_csv(caminho, sep=sep, encoding=encoding)
                df.columns = df.columns.str.strip()

                if 'Tempo_Reacao(s)' in df.columns:
                    return df
            except:
                continue
        
        return None

    def carregar_arquivos(self, lista_caminhos):
        novos_arquivos = 0
        erros = []
        
        for caminho in lista_caminhos:
            caminho_norm = os.path.normpath(caminho)
            if caminho_norm in self.dados_cache:
                continue
                
            df = self.ler_csv_inteligente(caminho_norm)
            
            if df is not None:
                self.dados_cache[caminho_norm] = df
                self.arquivos_selecionados.append(caminho_norm)
                novos_arquivos += 1

                nome = os.path.basename(caminho_norm)
                self.lista_box.insert(tk.END, f"✔ {nome}")
            else:
                erros.append(os.path.basename(caminho))
                self.lista_box.insert(tk.END, f"❌ ERRO: {os.path.basename(caminho)}")
                self.lista_box.itemconfig(tk.END, {'fg': 'red'})

        if novos_arquivos > 0:
            self.atualizar_visualizacao()
            msg = f"{novos_arquivos} arquivos carregados com sucesso."
        else:
            msg = "Nenhum arquivo novo carregado."
            
        if erros:
            msg += f"\nFalha em {len(erros)} arquivos."
            print("Arquivos com erro:", erros)
            
        self.log(msg)

    def carregar_pasta_inicial(self):
        if os.path.exists(PASTA_PADRAO):
            csvs = [os.path.join(PASTA_PADRAO, f) for f in os.listdir(PASTA_PADRAO) if f.lower().endswith('.csv')]
            if csvs:
                self.carregar_arquivos(csvs)
            else:
                self.log(f"Pasta encontrada, mas sem CSVs.")
        else:
            self.log("Pasta padrão não encontrada. Selecione manualmente.")

    def selecionar_arquivos(self):
        arquivos = filedialog.askopenfilenames(filetypes=[("CSV", "*.csv")])
        if arquivos:
            self.carregar_arquivos(arquivos)

    def selecionar_pasta(self):
        pasta = filedialog.askdirectory()
        if pasta:
            csvs = [os.path.join(pasta, f) for f in os.listdir(pasta) if f.lower().endswith('.csv')]
            self.carregar_arquivos(csvs)

    def limpar_tudo(self):
        self.arquivos_selecionados.clear()
        self.dados_cache.clear()
        self.lista_box.delete(0, tk.END)
        self.tabela.delete(*self.tabela.get_children())
        self.ax.clear()
        self.canvas.draw()
        self.txt_resumo.config(state="normal")
        self.txt_resumo.delete("1.0", tk.END)
        self.txt_resumo.config(state="disabled")
        self.log("Tudo limpo.")

    def atualizar_visualizacao(self):
        if not self.arquivos_selecionados:
            return

        self.ax.clear()

        n_arquivos = len(self.arquivos_selecionados)
        cmap = cm.get_cmap('tab10') if n_arquivos <= 10 else cm.get_cmap('tab20')
        cores = [cmap(i) for i in np.linspace(0, 1, n_arquivos)]

        todos_tempos = []
        todas_precisoes = []
        total_erros = 0

        max_len = 0
        dados_lista = []

        self.tabela.delete(*self.tabela.get_children())
        
        for i, caminho in enumerate(self.arquivos_selecionados):
            df = self.dados_cache[caminho]
            nome_arquivo = os.path.basename(caminho)
            nome_limpo = nome_arquivo.replace('.csv', '').replace('teste_', '')
            
            tempos = df['Tempo_Reacao(s)'].values

            dados_lista.append(tempos)
            max_len = max(max_len, len(tempos))

            media_ind = np.mean(tempos)
            melhor_ind = np.min(tempos)
            todos_tempos.extend(tempos)
            
            erros_ind = 0
            precisao_ind = "-"
            
            if 'Erros_Ate_Agora' in df.columns:
                try: 
                    erros_ind = int(df['Erros_Ate_Agora'].iloc[-1])
                    total_erros += erros_ind
                except: pass
            
            if 'Precisao_Atual(%)' in df.columns:
                try:
                    val = float(df['Precisao_Atual(%)'].iloc[-1])
                    precisao_ind = f"{val:.1f}%"
                    todas_precisoes.append(val)
                except: pass

            self.tabela.insert('', 'end', values=(
                nome_limpo, 
                f"{media_ind:.3f}", 
                f"{melhor_ind:.3f}",
                erros_ind, 
                precisao_ind
            ))

            x = np.arange(1, len(tempos) + 1)
            cor = cores[i % len(cores)]
            
            if self.var_linhas.get():
                self.ax.plot(x, tempos, color=cor, alpha=0.4, linewidth=1, label=nome_limpo if n_arquivos < 10 else "")
            
            if self.var_pontos.get():
                self.ax.scatter(x, tempos, color=cor, s=15, alpha=0.6)

        if self.var_media.get() and dados_lista:
            matriz = np.full((len(dados_lista), max_len), np.nan)
            for i, arr in enumerate(dados_lista):
                matriz[i, :len(arr)] = arr
                
            media_geral = np.nanmean(matriz, axis=0)
            x_media = np.arange(1, len(media_geral) + 1)
            
            self.ax.plot(x_media, media_geral, color='red', linewidth=2.5, label='MÉDIA GERAL', zorder=10)
            
            if self.var_tendencia.get() and len(x_media) > 1:
                idx_validos = ~np.isnan(media_geral)
                xm_valid = x_media[idx_validos]
                ym_valid = media_geral[idx_validos]
                
                if len(xm_valid) > 1:
                    z = np.polyfit(xm_valid, ym_valid, 1)
                    p = np.poly1d(z)
                    self.ax.plot(xm_valid, p(xm_valid), "k--", linewidth=1.5, label='Tendência')

        self.ax.set_title("Evolução do Tempo de Reação")
        self.ax.set_xlabel("Tentativa (Clique)")
        self.ax.set_ylabel("Tempo (s)")
        self.ax.grid(True, linestyle='--', alpha=0.5)
        if n_arquivos <= 10 or self.var_media.get():
            self.ax.legend(loc='upper right', fontsize='8')
        
        self.canvas.draw()

        texto_resumo = f"=== RESUMO GERAL ===\n\n"
        texto_resumo += f"Arquivos: {n_arquivos}\n"
        if todos_tempos:
            texto_resumo += f"Média Geral: {np.mean(todos_tempos):.3f} s\n"
            texto_resumo += f"Melhor Tempo: {np.min(todos_tempos):.3f} s\n"
            texto_resumo += f"Pior Tempo: {np.max(todos_tempos):.3f} s\n\n"
            texto_resumo += f"Total de Erros: {total_erros}\n"
            if todas_precisoes:
                texto_resumo += f"Precisão Média: {np.mean(todas_precisoes):.1f} %\n"
        
        self.txt_resumo.config(state="normal")
        self.txt_resumo.delete("1.0", tk.END)
        self.txt_resumo.insert(tk.END, texto_resumo)
        self.txt_resumo.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = AnalisadorAgilidadeApp(root)
    root.mainloop()