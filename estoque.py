import pandas as pd
import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import os


arquivo_csv = "estoque.csv"
lista_estoque = []

def carregar_estoque():
    if os.path.isfile(arquivo_csv):
        df = pd.read_csv(arquivo_csv)
        lista_estoque.extend(df.values.tolist())
    lista_estoque.sort(key=lambda item: item[0].lower())
    atualizar_tabela()

def adicionar_produto():
    produto = nome_produto.get()
    quantidade = int(quantidade_produto.get())
    valor_str = valor_produto.get().replace(',', '.')
    valor = float(valor_str)
    valor_estoque = quantidade * valor
    lista_estoque.append([produto, quantidade, valor, valor_estoque])
    lista_estoque.sort(key=lambda item: item[0].lower())
    limpar_campos()
    atualizar_tabela()

def atualizar_tabela():
    tabela.delete(*tabela.get_children())
    for item in lista_estoque:
        produto, quantidade, valor, valor_estoque = item
        tabela.insert('', 'end', values=(produto, quantidade, valor, valor_estoque))

def limpar_campos():
    nome_produto.set('')
    quantidade_produto.set('')
    valor_produto.set('')

def excluir_produto():
    item_selecionado = tabela.selection()
    if item_selecionado:
        item_index = tabela.index(item_selecionado)
        del lista_estoque[item_index]
        lista_estoque.sort(key=lambda item: item[0].lower())
        atualizar_tabela()
    else:
        messagebox.showerror("Erro", "Selecione um item para excluir.")

def editar_produto():
    item_selecionado = tabela.selection()
    if item_selecionado:
        item_index = tabela.index(item_selecionado)
        produto_atual, quantidade_atual, valor_atual, valor_estoque_atual = lista_estoque[item_index]
        resultado = editar_detalhes_produto(produto_atual, quantidade_atual, valor_atual)
        if resultado:
            nome_editado, quantidade_editada, valor_editado = resultado
            lista_estoque[item_index] = [nome_editado, quantidade_editada, valor_editado, quantidade_editada * valor_editado]
            lista_estoque.sort(key=lambda item: item[0].lower())
            atualizar_tabela()

def editar_detalhes_produto(nome_atual, quantidade_atual, valor_atual):
    novo_nome = simpledialog.askstring("Editar Produto", "Novo nome do produto:", initialvalue=nome_atual)
    if novo_nome is not None:
        nova_quantidade = simpledialog.askinteger("Editar Produto", "Nova quantidade:", initialvalue=quantidade_atual, minvalue=0)
        if nova_quantidade is not None:
            novo_valor = simpledialog.askfloat("Editar Produto", "Novo valor:", initialvalue=valor_atual, minvalue=0.0)
            if novo_valor is not None:
                return novo_nome, nova_quantidade, novo_valor
    return None

def calcular_valor_total_estoque():
    total_estoque = sum(item[3] for item in lista_estoque)
    return total_estoque

def exibir_valor_total_estoque():
    total_estoque = calcular_valor_total_estoque()
    messagebox.showinfo("Valor Total de Estoque", f"O valor total do estoque é: R$ {total_estoque:.2f}")

def salvar_e_sair():
    df = pd.DataFrame(lista_estoque, columns=['Produto', 'Quantidade', 'Valor', "Valor em Estoque"])
    df.to_csv(arquivo_csv, index=False)
    root.destroy()

def categorizar_produto(produto):
    # Esta função pode ser personalizada para categorizar produtos com base em nomes, palavras-chave, etc.
    if "eletrônico" in produto.lower():
        return "Eletrônicos"
    elif "roupa" in produto.lower():
        return "Roupas"
    elif "alimento" in produto.lower():
        return "Alimentos"
    else:
        return "Outros"
    
root = tk.Tk()
root.title("Controle de Estoque")
root.geometry("1080x720")  # Defina a resolução da janela

# Impede que a janela seja redimensionável
root.resizable(False, False)

# Configurando um estilo "dark mode"
style = ttk.Style()
style.theme_use("clam")  # Escolha um tema que funcione bem com o "dark mode"
style.configure("Treeview", background="#333", fieldbackground="#333", foreground="white", rowheight=25)
style.configure("TButton", background="#444", foreground="white")
style.map("TButton",
          background=[("active", "#666")]
          )

nome_produto = tk.StringVar()
quantidade_produto = tk.StringVar()
valor_produto = tk.StringVar()

tk.Label(root, text="Nome do Produto", bg="#333", fg="white").grid(row=0, column=0)
tk.Entry(root, textvariable=nome_produto).grid(row=0, column=1)
tk.Label(root, text="Quantidade", bg="#333", fg="white").grid(row=1, column=0)
tk.Entry(root, textvariable=quantidade_produto).grid(row=1, column=1)
tk.Label(root, text="Valor", bg="#333", fg="white").grid(row=2, column=0)
tk.Entry(root, textvariable=valor_produto).grid(row=2, column=1)
tk.Button(root, text="Adicionar Produto", command=adicionar_produto, bg="#444", fg="white").grid(row=3, column=0, columnspan=2)
tk.Button(root, text="Editar Produto", command=editar_produto, bg="#444", fg="white").grid(row=5, column=1)
tk.Button(root, text="Excluir Produto", command=excluir_produto, bg="#444", fg="white").grid(row=6, column=0)
tk.Button(root, text="Sair e Salvar", command=salvar_e_sair, bg="#444", fg="white").grid(row=6, column=1)
tk.Button(root, text="Calcular Valor Total de Estoque", command=exibir_valor_total_estoque, bg="#444", fg="white").grid(row=5, column=0, columnspan=2)

frame = tk.Frame(root)
frame.grid(row=4, column=0, columnspan=2)

# Adicione uma barra de rolagem vertical
scrollbar = ttk.Scrollbar(frame, orient="vertical")
scrollbar.pack(side="right", fill="y")

tabela = ttk.Treeview(frame, columns=('Produto', 'Quantidade', 'Valor', "Valor em Estoque"))
tabela.config(yscrollcommand=scrollbar.set)
tabela.heading('#1', text='Produto')
tabela.heading('#2', text='Quantidade')
tabela.heading('#3', text='Valor')
tabela.heading('#4', text='Valor em Estoque')
tabela.pack(fill='both', expand=1)

# Conecte a barra de rolagem à tabela
scrollbar.config(command=tabela.yview)
carregar_estoque()
root.mainloop()







