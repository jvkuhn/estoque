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
    atualizar_tabela()

def adicionar_produto():
    produto = nome_produto.get()
    quantidade = int(quantidade_produto.get())
    valor_str = valor_produto.get().replace(',', '.') 
    valor = float(valor_str)
    valor_estoque = quantidade * valor
    lista_estoque.append([produto, quantidade, valor, valor_estoque])
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
        produto, quantidade, valor, valor_estoque = lista_estoque[item_index]
        quantidade_a_remover = simpledialog.askinteger("Remover Quantidade", f"Quantidade para remover de {produto}:", initialvalue=quantidade, minvalue=0, maxvalue=quantidade)
        
        if quantidade_a_remover is not None:
            if quantidade_a_remover < quantidade:
                lista_estoque[item_index][1] -= quantidade_a_remover
            else:
                del lista_estoque[item_index]
            atualizar_tabela()
    else:
        messagebox.showerror("Erro", "Selecione um item para excluir.")

def editar_produto():
    item_selecionado = tabela.selection()
    if item_selecionado:
        item_index = tabela.index(item_selecionado)
        produto, quantidade, valor, valor_estoque = lista_estoque[item_index]
        quantidade_editada = simpledialog.askinteger("Editar Quantidade", f"Quantidade para {produto}:", initialvalue=quantidade, minvalue=0)
        
        if quantidade_editada is not None:
            lista_estoque[item_index][1] = quantidade_editada
            lista_estoque[item_index][3] = quantidade_editada * valor
            atualizar_tabela()
    else:
        messagebox.showerror("Erro", "Selecione um item para editar.")

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

root = tk.Tk()
root.title("Controle de Estoque")

nome_produto = tk.StringVar()
quantidade_produto = tk.StringVar()
valor_produto = tk.StringVar()

tk.Label(root, text="Nome do Produto").grid(row=0, column=0)
tk.Entry(root, textvariable=nome_produto).grid(row=0, column=1)
tk.Label(root, text="Quantidade").grid(row=1, column=0)
tk.Entry(root, textvariable=quantidade_produto).grid(row=1, column=1)
tk.Label(root, text="Valor").grid(row=2, column=0)
tk.Entry(root, textvariable=valor_produto).grid(row=2, column=1)
tk.Button(root, text="Adicionar Produto", command=adicionar_produto).grid(row=3, column=0, columnspan=2)
tk.Button(root, text="Editar Produto", command=editar_produto).grid(row=5, column=1)
tk.Button(root, text="Excluir Produto", command=excluir_produto).grid(row=6, column=0)
tk.Button(root, text="Sair e Salvar", command=salvar_e_sair).grid(row=6, column=1)
tk.Button(root, text="Calcular Valor Total de Estoque", command=exibir_valor_total_estoque).grid(row=5, column=0, columnspan=2)

frame = tk.Frame(root)
frame.grid(row=4, column=0, columnspan=2)
tabela = ttk.Treeview(frame, columns=('Produto', 'Quantidade', 'Valor', "Valor em Estoque"))
tabela.heading('#1', text='Produto')
tabela.heading('#2', text='Quantidade')
tabela.heading('#3', text='Valor')
tabela.heading('#4', text='Valor em Estoque')
tabela.pack(fill='both', expand=1)

carregar_estoque()

root.mainloop()