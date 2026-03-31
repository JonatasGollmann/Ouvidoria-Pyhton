import tkinter as tk
from tkinter import ttk, scrolledtext
from database import Database


class InterfaceOuvidoria:

    TAGS_POR_TIPO = {
        "Elogio": "elogio",
        "Crítica": "critica",
        "Comentário": "comentario",
    }
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Ouvidoria")
        self.root.geometry("900x650")
        self.root.resizable(False, False)
        
        self.db = Database()
        
        self.cor_fundo = "#1e1e1e"
        self.cor_fundo_sec = "#2d2d2d"
        self.cor_fundo_ter = "#3a3a3a"
        self.cor_texto = "#e0e0e0"
        self.cor_texto_sec = "#a0a0a0"
        self.cor_botao = "#00a8e8"
        self.cor_botao_hover = "#00d4ff"
        self.cor_remover = "#ff4757"
        self.cor_remover_hover = "#ff6b7f"
        self.cor_sucesso = "#2ed573"
        
        self.root.config(bg=self.cor_fundo)
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TCombobox', 
                       background=self.cor_fundo_ter,
                       fieldbackground=self.cor_fundo_ter,
                       foreground=self.cor_texto)
        
        self._criar_interface()
        self._atualizar_lista()
    
    def _criar_interface(self):
        frame_titulo = tk.Frame(self.root, bg=self.cor_fundo_sec, height=70)
        frame_titulo.pack(fill=tk.X, padx=0, pady=0)
        frame_titulo.pack_propagate(False)
        
        titulo = tk.Label(
            frame_titulo,
            text="OUVIDORIA",
            font=("Segoe UI", 24, "bold"),
            bg=self.cor_fundo_sec,
            fg=self.cor_botao
        )
        titulo.pack(pady=15)
        
        frame_principal = tk.Frame(self.root, bg=self.cor_fundo)
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        frame_left = tk.Frame(frame_principal, bg=self.cor_fundo)
        frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        label_form = tk.Label(
            frame_left,
            text="NOVA MANIFESTAÇÃO",
            font=("Segoe UI", 11, "bold"),
            bg=self.cor_fundo,
            fg=self.cor_botao
        )
        label_form.pack(anchor=tk.W, pady=(0, 15))
        
        tk.Label(
            frame_left,
            text="Tipo",
            font=("Segoe UI", 9),
            bg=self.cor_fundo,
            fg=self.cor_texto
        ).pack(pady=(0, 6), anchor=tk.W)
        
        self.combo_tipo = ttk.Combobox(
            frame_left,
            values=["Elogio", "Crítica", "Comentário"],
            state="readonly",
            width=35,
            font=("Segoe UI", 10)
        )
        self.combo_tipo.pack(pady=(0, 15), fill=tk.X)
        self.combo_tipo.current(0)
        
        tk.Label(
            frame_left,
            text="Descrição",
            font=("Segoe UI", 9),
            bg=self.cor_fundo,
            fg=self.cor_texto
        ).pack(pady=(0, 6), anchor=tk.W)
        
        self.text_descricao = scrolledtext.ScrolledText(
            frame_left,
            width=40,
            height=6,
            wrap=tk.WORD,
            font=("Segoe UI", 9),
            bg=self.cor_fundo_ter,
            fg=self.cor_texto,
            insertbackground=self.cor_botao,
            relief=tk.FLAT,
            bd=0
        )
        self.text_descricao.pack(pady=(0, 15), fill=tk.BOTH, expand=False)
        
        botao_criar = tk.Button(
            frame_left,
            text="Criar Manifestação",
            font=("Segoe UI", 10, "bold"),
            bg=self.cor_botao,
            fg="#000000",
            command=self._criar_manifestacao,
            cursor="hand2",
            relief=tk.FLAT,
            bd=0,
            pady=10
        )
        botao_criar.pack(fill=tk.X, pady=(0, 0))
        botao_criar.bind("<Enter>", lambda e: botao_criar.config(bg=self.cor_botao_hover))
        botao_criar.bind("<Leave>", lambda e: botao_criar.config(bg=self.cor_botao))
        
        frame_right = tk.Frame(frame_principal, bg=self.cor_fundo)
        frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        label_busca = tk.Label(
            frame_right,
            text="BUSCAR",
            font=("Segoe UI", 11, "bold"),
            bg=self.cor_fundo,
            fg=self.cor_botao
        )
        label_busca.pack(anchor=tk.W, pady=(0, 12))
        
        tk.Label(
            frame_right,
            text="Palavra-chave",
            font=("Segoe UI", 9),
            bg=self.cor_fundo,
            fg=self.cor_texto
        ).pack(pady=(0, 6), anchor=tk.W)
        
        self.entry_busca = tk.Entry(
            frame_right,
            font=("Segoe UI", 10),
            bg=self.cor_fundo_ter,
            fg=self.cor_texto,
            insertbackground=self.cor_botao,
            relief=tk.FLAT,
            bd=0
        )
        self.entry_busca.pack(pady=(0, 12), fill=tk.X, ipady=8)
        self.entry_busca.bind("<Return>", lambda e: self._buscar())
        
        frame_btn_busca = tk.Frame(frame_right, bg=self.cor_fundo)
        frame_btn_busca.pack(fill=tk.X, pady=(0, 15))
        
        botao_buscar = tk.Button(
            frame_btn_busca,
            text="Buscar",
            font=("Segoe UI", 9, "bold"),
            bg=self.cor_botao,
            fg="#000000",
            command=self._buscar,
            cursor="hand2",
            relief=tk.FLAT,
            bd=0,
            padx=15,
            pady=7
        )
        botao_buscar.pack(side=tk.LEFT, padx=(0, 8))
        botao_buscar.bind("<Enter>", lambda e: botao_buscar.config(bg=self.cor_botao_hover))
        botao_buscar.bind("<Leave>", lambda e: botao_buscar.config(bg=self.cor_botao))
        
        botao_limpar_busca = tk.Button(
            frame_btn_busca,
            text="Limpar",
            font=("Segoe UI", 9, "bold"),
            bg=self.cor_fundo_ter,
            fg=self.cor_texto,
            command=self._limpar_busca,
            cursor="hand2",
            relief=tk.FLAT,
            bd=0,
            padx=15,
            pady=7
        )
        botao_limpar_busca.pack(side=tk.LEFT)
        botao_limpar_busca.bind("<Enter>", lambda e: botao_limpar_busca.config(bg="#4a4a4a"))
        botao_limpar_busca.bind("<Leave>", lambda e: botao_limpar_busca.config(bg=self.cor_fundo_ter))
        
        label_manifest = tk.Label(
            frame_right,
            text="MANIFESTAÇÕES",
            font=("Segoe UI", 11, "bold"),
            bg=self.cor_fundo,
            fg=self.cor_botao
        )
        label_manifest.pack(anchor=tk.W, pady=(0, 12))
        
        frame_listbox = tk.Frame(frame_right, bg=self.cor_fundo_ter, relief=tk.FLAT, bd=0)
        frame_listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 12))
        
        scrollbar = tk.Scrollbar(frame_listbox, bg=self.cor_fundo_sec, troughcolor=self.cor_fundo_ter)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox_manifestacoes = tk.Text(
            frame_listbox,
            font=("Segoe UI", 10),
            yscrollcommand=scrollbar.set,
            bg=self.cor_fundo_ter,
            fg=self.cor_texto,
            relief=tk.FLAT,
            bd=0,
            state=tk.DISABLED,
            wrap=tk.WORD
        )
        self.listbox_manifestacoes.pack(fill=tk.BOTH, expand=True, padx=0)
        scrollbar.config(command=self.listbox_manifestacoes.yview)
        
        self.listbox_manifestacoes.tag_config("elogio", foreground="#2ed573", font=("Segoe UI", 10, "bold"))
        self.listbox_manifestacoes.tag_config("critica", foreground="#ff4757", font=("Segoe UI", 10, "bold"))
        self.listbox_manifestacoes.tag_config("comentario", foreground="#00a8e8", font=("Segoe UI", 10, "bold"))
        self.listbox_manifestacoes.tag_config("normal", foreground=self.cor_texto)
        
        botao_remover = tk.Button(
            frame_right,
            text="Remover Selecionada",
            font=("Segoe UI", 10, "bold"),
            bg=self.cor_remover,
            fg="#ffffff",
            command=self._remover_manifestacao,
            cursor="hand2",
            relief=tk.FLAT,
            bd=0,
            pady=10
        )
        botao_remover.pack(fill=tk.X)
        botao_remover.bind("<Enter>", lambda e: botao_remover.config(bg=self.cor_remover_hover))
        botao_remover.bind("<Leave>", lambda e: botao_remover.config(bg=self.cor_remover))
        
        frame_stats = tk.Frame(self.root, bg=self.cor_fundo_sec, height=60)
        frame_stats.pack(fill=tk.X, padx=0, pady=0)
        frame_stats.pack_propagate(False)
        
        self.label_stats = tk.Label(
            frame_stats,
            text="",
            font=("Segoe UI", 9),
            bg=self.cor_fundo_sec,
            fg=self.cor_texto,
            justify=tk.CENTER
        )
        self.label_stats.pack(pady=15)
    
    def _criar_manifestacao(self):
        tipo = self.combo_tipo.get()
        descricao = self.text_descricao.get("1.0", tk.END).strip()
        
        if not descricao:
            return
        
        try:
            self.db.criar(tipo, descricao)
            self.text_descricao.delete("1.0", tk.END)
            self.combo_tipo.current(0)
            self._atualizar_lista()
            
        except ValueError:
            return
    
    def _buscar(self):
        palavra_chave = self.entry_busca.get().strip()
        
        if not palavra_chave:
            return
        
        resultados = self.db.buscar_por_descricao(palavra_chave)
        self._renderizar_manifestacoes(resultados, "Nenhum resultado encontrado")
    
    def _limpar_busca(self):
        self.entry_busca.delete(0, tk.END)
        self._atualizar_lista()
    
    def _atualizar_lista(self):
        manifestacoes = self.db.listar_todas()
        self._renderizar_manifestacoes(manifestacoes, "Nenhuma manifestação registrada")

    def _renderizar_manifestacoes(self, manifestacoes, mensagem_vazia):
        self.listbox_manifestacoes.config(state=tk.NORMAL)
        self.listbox_manifestacoes.delete("1.0", tk.END)

        if not manifestacoes:
            self.listbox_manifestacoes.insert(tk.END, mensagem_vazia)
        else:
            for manifestacao in manifestacoes:
                texto = self._formatar_manifestacao(manifestacao)
                tag = self._get_tag_por_tipo(manifestacao.tipo)
                self.listbox_manifestacoes.insert(tk.END, texto, tag)

        self.listbox_manifestacoes.config(state=tk.DISABLED)
        self._atualizar_stats()

    def _formatar_manifestacao(self, manifestacao):
        descricao = manifestacao.descricao[:50]
        sufixo = "...\n" if len(manifestacao.descricao) > 50 else "\n"
        return f"[{manifestacao.codigo}] {manifestacao.tipo}: {descricao}{sufixo}"
    
    def _get_tag_por_tipo(self, tipo):
        return self.TAGS_POR_TIPO.get(tipo, "comentario")
    
    def _atualizar_stats(self):
        total = self.db.total_manifestacoes()
        contagem = self.db.contar_por_tipo()
        
        texto_stats = (
            f"Total: {total}  •  "
            f"Elogios: {contagem['Elogio']}  •  "
            f"Críticas: {contagem['Crítica']}  •  "
            f"Comentários: {contagem['Comentário']}"
        )
        
        self.label_stats.config(text=texto_stats)
    
    def _on_select_manifestacao(self, event):
        pass
    
    def _remover_manifestacao(self):
        try:
            sel_inicio = self.listbox_manifestacoes.index(tk.SEL_FIRST)
            sel_fim = self.listbox_manifestacoes.index(tk.SEL_LAST)
        except tk.TclError:
            return
        
        linha_selecionada = self.listbox_manifestacoes.get(sel_inicio, sel_fim)
        
        if "Nenhuma" in linha_selecionada or "Nenhum" in linha_selecionada:
            return
        
        try:
            codigo = int(linha_selecionada.split("[")[1].split("]")[0])
        except (IndexError, ValueError):
            return

        if self.db.remover(codigo):
            self._atualizar_lista()
            self._limpar_busca()


def iniciar_interface():
    root = tk.Tk()
    app = InterfaceOuvidoria(root)
    root.mainloop()


if __name__ == "__main__":
    iniciar_interface()
