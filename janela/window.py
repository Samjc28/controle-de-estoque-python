from tkinter import *
from pathlib import Path
import sqlite3

# Definição de caminhos absolutos relativos ao script
PASTA_JANELA = Path(__file__).resolve().parent
DB_PATH = PASTA_JANELA.parent / "Estoque.db"

# Conexão com o banco de dados SQLite
conexao = sqlite3.connect(DB_PATH)
cursor = conexao.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Estoque (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Produto TEXT NOT NULL,
    Quantidade INTEGER,
    DataValidade TEXT,
    Lote INTEGER
)
''')
conexao.commit()

######## funcionalidades do sistema #############

def adicionar_insumo():
    nome = nome_insumo.get().strip()
    qtde = qtde_insumo.get().strip()
    data = data_insumo.get().strip()
    lote = lote_insumo.get().strip()

    if len(nome) < 2:
        caixa_texto.delete("1.0", END)
        caixa_texto.insert("1.0", "Nome do insumo inválido! Preencha ao menos 2 caracteres.")
        return

    cursor.execute('''
    INSERT INTO Estoque (Produto, Quantidade, DataValidade, Lote)
    VALUES (?, ?, ?, ?)
    ''', (nome, qtde, data, lote))
    conexao.commit()
   
    # Limpa a caixa de texto e exibe confirmação
    caixa_texto.delete("1.0", END)
    caixa_texto.insert("1.0", f"Insumo '{nome}' adicionado com sucesso ao estoque.")
    
def deletar_insumo():
    nome = nome_insumo.get().strip()
    if len(nome) < 2:
        caixa_texto.delete("1.0", END)
        caixa_texto.insert("1.0", f"'{nome}' Nome do insumo inválido para exclusão!")
        return

    # Deleta com query parametrizada (segurança contra SQL Injection)
    cursor.execute('DELETE FROM Estoque WHERE Produto = ?', (nome,))
    conexao.commit()

    caixa_texto.delete("1.0", END)
    caixa_texto.insert("1.0", f"Insumo '{nome}' deletado com sucesso do estoque!")

def consumir_insumo():
    nome = nome_insumo.get().strip()
    lote = lote_insumo.get().strip()
    qtde = qtde_insumo.get().strip()

    if len(nome) < 2 or len(lote) < 1 or len(qtde) < 1:
        caixa_texto.delete("1.0", END)
        caixa_texto.insert("1.0", "Informe o Nome, Lote e a Quantidade a ser consumida!")
        return

    try:
        qtde_int = int(qtde)
    except ValueError:
        caixa_texto.delete("1.0", END)
        caixa_texto.insert("1.0", "A Quantidade deve ser um número inteiro válido!")
        return

    # Atualiza a quantidade do insumo específico no lote informado
    cursor.execute('''
        UPDATE Estoque
        SET Quantidade = Quantidade - ?
        WHERE Produto = ? AND Lote = ?
    ''', (qtde_int, nome, lote))
    conexao.commit()

    caixa_texto.delete("1.0", END)
    caixa_texto.insert("1.0", f"Insumo '{nome}' (Lote {lote}): consumo de {qtde_int} unid. registrado com sucesso!")

def visualizar_insumo():
    nome = nome_insumo.get().strip()
    if len(nome) < 2:
        caixa_texto.delete("1.0", END)
        caixa_texto.insert("1.0", "Informe ao menos 2 caracteres no nome para pesquisar!")
        return

    cursor.execute('SELECT id, Produto, Quantidade, DataValidade, Lote FROM Estoque WHERE Produto = ?', (nome,))
    valores = cursor.fetchall()

    caixa_texto.delete("1.0", END)
    if not valores:
        caixa_texto.insert("1.0", f"Nenhum registro encontrado para o insumo '{nome}'.")
        return

    texto = ""
    for id_produto, prod, quantidade, validade, lote in valores:
        texto += f"""-----
- ID: {id_produto}
- Produto: {prod}
- Quantidade: {quantidade}
- Validade: {validade}
- Lote: {lote}
"""
    caixa_texto.insert("1.0", texto.strip())

######### criação da Janela ##################
    
window = Tk()

window.geometry("800x646")
window.configure(bg = "#ffffff")
window.resizable(False,False)
canvas = Canvas(
    window,
    bg = "#ffffff",
    height = 646,
    width = 800,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = PASTA_JANELA/"fundo_img.png")
background = canvas.create_image(
    355.5, 323.0,
    image=background_img)

img0 = PhotoImage(file = PASTA_JANELA/"img0.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = visualizar_insumo,
    relief = "flat")

b0.place(
    x = 479, y = 195,
    width = 178,
    height = 38)

img1 = PhotoImage(file = PASTA_JANELA/"img1.png")
b1 = Button(
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = deletar_insumo,
    relief = "flat")

b1.place(
    x = 247, y = 197,
    width = 178,
    height = 36)

img2 = PhotoImage(file = PASTA_JANELA/"img2.png")
b2 = Button(
    image = img2,
    borderwidth = 0,
    highlightthickness = 0,
    command = consumir_insumo,
    relief = "flat")

b2.place(
    x = 479, y = 123,
    width = 178,
    height = 35)

img3 = PhotoImage(file = PASTA_JANELA/"img3.png")
b3 = Button(
    image = img3,
    borderwidth = 0,
    highlightthickness = 0,
    command = adicionar_insumo,
    relief = "flat")

b3.place(
    x = 247, y = 125,
    width = 178,
    height = 34)

entry0_img = PhotoImage(file = PASTA_JANELA/"img_textBox0.png")
entry0_bg = canvas.create_image(
    455.0, 560.0,
    image = entry0_img)

caixa_texto = Text(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

caixa_texto.place(
    x = 250, y = 502,
    width = 410,
    height = 114)

entry1_img = PhotoImage(file = PASTA_JANELA/"img_textBox1.png")
entry1_bg = canvas.create_image(
    517.0, 294.5,
    image = entry1_img)

nome_insumo = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

nome_insumo.place(
    x = 377, y = 278,
    width = 280,
    height = 31)

entry2_img = PhotoImage(file = PASTA_JANELA/"img_textBox2.png")
entry2_bg = canvas.create_image(
    517.0, 340.5,
    image = entry2_img)

data_insumo = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

data_insumo.place(
    x = 377, y = 324,
    width = 280,
    height = 31)

entry3_img = PhotoImage(file = PASTA_JANELA/"img_textBox3.png")
entry3_bg = canvas.create_image(
    517.0, 388.5,
    image = entry3_img)

lote_insumo = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

lote_insumo.place(
    x = 377, y = 372,
    width = 280,
    height = 31)

entry4_img = PhotoImage(file = PASTA_JANELA/"img_textBox4.png")
entry4_bg = canvas.create_image(
    517.0, 436.5,
    image = entry4_img)

qtde_insumo = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

qtde_insumo.place(
    x = 377, y = 420,
    width = 280,
    height = 31)



window.resizable(False, False)
window.mainloop()

# fechando a conexão
cursor.close()
conexao.close()