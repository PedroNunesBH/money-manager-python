import mysql.connector
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview, Combobox
from datetime import datetime
import locale
import re
from tkcalendar import Calendar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import yagmail

conexao = mysql.connector.connect(host="localhost",
                                  user="root",
                                  password="admin",
                                  database="controledegastos")

cursor = conexao.cursor()

locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
dia_atual = datetime.today()

meses_para_numeros = {
    "Janeiro": 1,
    "Fevereiro": 2,
    "Março": 3,
    "Abril": 4,
    "Maio": 5,
    "Junho": 6,
    "Julho": 7,
    "Agosto": 8,
    "Setembro": 9,
    "Outubro": 10,
    "Novembro": 11,
    "Dezembro": 12
}

email_do_app = yagmail.SMTP(user="email", password="senha")

def login():
    global cursor
    global conexao
    global estado_do_login
    global id_usuario_ativo

    def verificar_login():
        global estado_do_login
        global id_usuario_ativo
        usuario_do_login = entry_usuario.get()
        senha_do_login = entry_senha.get()
        comando_login_bd = (f'SELECT * FROM usuarios WHERE s_usuario_usuarios = "{usuario_do_login}" and'
                            f' s_senha_usuarios = "{senha_do_login}"')
        cursor.execute(comando_login_bd)
        resultado_consulta_login = cursor.fetchall()
        if len(resultado_consulta_login) > 0:
            id_usuario_ativo = resultado_consulta_login[0][0]
            estado_do_login = True
            janela_login.destroy()
        else:
            label_avisos_login["text"] = "Não foi possível realizar o login.\nTente novamente."
            estado_do_login = False

    def recuperar_senha():

        def confirmacao_recuperacao():
            email_do_cadastro = entry_email_de_cadastro.get()
            usuario_do_cadastro = entry_usuario_de_cadastro.get()
            nova_senha = entry_nova_senha.get()
            confirmacao_nova_senha = entry_nova_senha_confirmacao.get()
            palavra_chave_do_usuario = entry_palavra_chave_usuario.get()
            comando_para_recuperacao = (f'SELECT * from usuarios where s_email_usuarios = "{email_do_cadastro}"'
                                        f' and s_usuario_usuarios = "{usuario_do_cadastro}" and '
                                        f's_palavrasecreta_usuarios = "{palavra_chave_do_usuario}" ')
            cursor.execute(comando_para_recuperacao)
            resultado_existencia_do_usuario = cursor.fetchall()
            if len(resultado_existencia_do_usuario) == 0:
                label_avisos_recuperacao["text"] = ("Não existe usuário cadastrado com\n os dados informados ou\n "
                                                    "a palavra-chave está incorreta.")
            else:
                padrao_senha_de_recuperacao = re.compile(r'^(?=.*[A-Z])(?=.*[0-9])(?=.*[\W_])(?=.*[a-z]).{8,}$')
                checagem_senha_de_recuperacao = padrao_senha_de_recuperacao.findall(nova_senha)
                if len(checagem_senha_de_recuperacao) > 0 and nova_senha == confirmacao_nova_senha and nova_senha != "":
                    comando_substituicao_de_senha = (f'UPDATE usuarios set s_senha_usuarios = "{nova_senha}"'
                                                     f' where s_usuario_usuarios = "{usuario_do_cadastro}" and '
                                                     f's_email_usuarios = "{email_do_cadastro}"')
                    cursor.execute(comando_substituicao_de_senha)
                    conexao.commit()
                    label_avisos_recuperacao["text"] = "Senha redefinida com sucesso."
                    entry_email_de_cadastro.delete(0, END)
                    entry_usuario_de_cadastro.delete(0, END)
                    entry_nova_senha.delete(0, END)
                    entry_nova_senha_confirmacao.delete(0, END)
                else:
                    label_avisos_recuperacao["height"] = 5
                    label_avisos_recuperacao["text"] = (
                        "A senha informada deve conter pelo menos:\numa letra minúscula,"
                        "uma letra maiúscula,\num número,um caracter especial\n e "
                        "8 caracteres totais.")

        janela_recuperacao_de_senha = Toplevel()
        janela_recuperacao_de_senha.title("Esqueci Minha Senha")
        janela_recuperacao_de_senha.geometry("300x500")

        label_principal_recuperacao = Label(janela_recuperacao_de_senha, text="Recupere Sua Senha", width=17, height=1,
                                            font=("Arial", 15, "bold"))
        label_principal_recuperacao.place(x=50, y=30)

        label_email_de_cadastro = Label(janela_recuperacao_de_senha, text="Informe o seu Email:", width=15, height=1)
        label_email_de_cadastro.place(x=10, y=80)

        entry_email_de_cadastro = Entry(janela_recuperacao_de_senha, width=45)
        entry_email_de_cadastro.place(x=10, y=110)

        label_usuario_de_cadastro = Label(janela_recuperacao_de_senha, text="Informe seu Usuário:", width=15, height=1)
        label_usuario_de_cadastro.place(x=10, y=130)

        entry_usuario_de_cadastro = Entry(janela_recuperacao_de_senha, width=45)
        entry_usuario_de_cadastro.place(x=10, y=160)

        label_nova_senha = Label(janela_recuperacao_de_senha, text="Digite a Nova Senha:", width=15, height=1)
        label_nova_senha.place(x=10, y=190)

        entry_nova_senha = Entry(janela_recuperacao_de_senha, width=45, show="*")
        entry_nova_senha.place(x=10, y=220)

        label_nova_senha_confirmacao = Label(janela_recuperacao_de_senha, text="Confirme a Nova Senha:", width=17,
                                             height=1)
        label_nova_senha_confirmacao.place(x=10, y=250)

        entry_nova_senha_confirmacao = Entry(janela_recuperacao_de_senha, width=45, show="*")
        entry_nova_senha_confirmacao.place(x=10, y=280)

        label_palavra_chave_usuario = Label(janela_recuperacao_de_senha, text="Insira sua palavra-chave", width=15,
                                            height=1)
        label_palavra_chave_usuario.place(x=10, y=310)

        entry_palavra_chave_usuario = Entry(janela_recuperacao_de_senha, width=45)
        entry_palavra_chave_usuario.place(x=10, y=340)

        botao_confirmacao = Button(janela_recuperacao_de_senha, command=confirmacao_recuperacao, text="Confirmar",
                                   width=10, height=1, bg="green", fg="white")
        botao_confirmacao.place(x=100, y=380)

        label_avisos_recuperacao = Label(janela_recuperacao_de_senha, text="", width=40, height=4)
        label_avisos_recuperacao.place(x=0, y=410)

        janela_recuperacao_de_senha.mainloop()

    janela_login = Tk()
    janela_login.title("Faça seu login")
    janela_login.geometry("350x380")
    janela_login.resizable(width=False, height=False)

    label_principal = Label(janela_login, text="Faça Seu Login", width=15, height=1, font=("Arial", 15, "bold"))
    label_principal.place(x=100, y=20)

    label_usuario = Label(janela_login, text="Usuário :", width=10, height=1)
    label_usuario.place(x=10, y=80)

    entry_usuario = Entry(janela_login, width=55)
    entry_usuario.place(x=10, y=120)

    label_senha = Label(janela_login, text="Senha :", width=10, height=1)
    label_senha.place(x=10, y=150)

    entry_senha = Entry(janela_login, width=55, show="*")
    entry_senha.place(x=10, y=180)

    botao_login = Button(janela_login, text="Fazer login", command=verificar_login, width=10, height=1, bg="green",
                         fg="white")
    botao_login.place(x=10, y=220)

    botao_recuperacao_senha = Button(janela_login, command=recuperar_senha, text="Recuperar Senha", width=12, height=1,
                                     bg="red", fg="white")
    botao_recuperacao_senha.place(x=100, y=220)

    label_avisos_login = Label(janela_login, text="", width=25, height=2)
    label_avisos_login.place(x=70, y=260)

    label_cadastro = Label(janela_login, text="Não possui uma conta ainda?", width=25, height=1)
    label_cadastro.place(x=10, y=310)

    botao_cadastro = Button(janela_login, text="Cadastre-se", command=cadastrar_usuario, width=10, height=1, bg="blue",
                            fg="white")
    botao_cadastro.place(x=15, y=340)

    janela_login.bind("<Return>", lambda event: verificar_login())
    janela_login.mainloop()
    return estado_do_login, janela_login, id_usuario_ativo


def cadastrar_usuario():
    global email_do_app
    def verificar_cadastro():
        email_do_cadastro = entry_cadastro_email.get()
        usuario_do_cadastro = entry_cadastro_usuario.get()
        senha_do_cadastro = entry_cadastro_senha.get()
        palavra_chave = entry_palavra_chave.get()
        padrao_usuario_do_cadastro = re.compile("[a-zA-Z0-9]{8,}")
        padrao_senha_do_cadastro = re.compile(r'^(?=.*[A-Z])(?=.*[0-9])(?=.*[\W_])(?=.*[a-z]).{8,}$')
        # Pelo menos uma letra maiuscula, 1 letra minuscula, 1 numero, 1 caracter especial e no minimo 8caracteres total
        checar_padrao_usuario_do_cadastro = padrao_usuario_do_cadastro.findall(usuario_do_cadastro)
        checar_padrao_senha_do_cadastro = padrao_senha_do_cadastro.findall(senha_do_cadastro)
        if email_do_cadastro == "":
            label_avisos_cadastramento["width"] = 40
            label_avisos_cadastramento["fg"] = "red"
            label_avisos_cadastramento["text"] = ("O email deve ser preenchido obrigatoriamente.\n"
                                                  "Certifique-se de preencher corretamente.")
        else:
            pass
            if len(checar_padrao_usuario_do_cadastro) == 0:
                label_avisos_cadastramento["fg"] = "red"
                label_avisos_cadastramento["width"] = 40
                label_avisos_cadastramento["text"] = "O usuário deve conter pelo menos 8 caracteres."
            else:
                pass
                if len(checar_padrao_senha_do_cadastro) == 0:
                    label_avisos_cadastramento["height"] = 6
                    label_avisos_cadastramento["width"] = 40
                    label_avisos_cadastramento["text"] = ("A senha deve obedecer os seguintes parametros:\n"
                                                          "1- No mínimo uma letra minúscula\n"
                                                          "2- No mínimo uma letra maiúscula\n"
                                                          "3- No mínimo um número\n"
                                                          "4- No mínimo um caracter especial\n"
                                                          "5- Pelo menos 8 caracteres totais")
                else:
                    pass
                    if len(palavra_chave) < 8:
                        label_avisos_cadastramento["fg"] = "red"
                        label_avisos_cadastramento["width"] = 40
                        label_avisos_cadastramento["text"] = "A sua palavra-chave deve conter\npelo menos 8 caracteres."
                    else:
                        pass
                        try:
                            comando_de_cadastro_bd = (
                                f'INSERT INTO usuarios values ((select max(u.i_id_usuarios) from usuarios u)'
                                f' + 1, "{usuario_do_cadastro}", "{senha_do_cadastro}",'
                                f' "{email_do_cadastro}", "{palavra_chave}"); ')
                            cursor.execute(comando_de_cadastro_bd)
                            conexao.commit()
                        except mysql.connector.errors.IntegrityError:
                            label_avisos_cadastramento["width"] = 30
                            label_avisos_cadastramento["text"] = ("Não foi possível realizar o cadastro.\nEsse nome de usuário e/ou e-mail "
                                                                  "já existe. ")
                        else:
                            label_avisos_cadastramento["width"] = 35
                            label_avisos_cadastramento["text"] = "Cadastro realizado com sucesso."
                            email_do_app.send(to=email_do_cadastro, subject="Seja Bem Vindo ao Nosso App!",
                                              contents=f"Olá {usuario_do_cadastro}.\n"
                                                       f"Seu cadastro no app de controle de gastos foi bem-sucedido.\n"
                                                       f"Esperamos que você aproveite ao máximo todos os nossos recursos.\n"
                                                       f"Por favor,qualquer coisa não hesite em nos contatar através de nossos suportes. ")

    janela_cadastro = Toplevel()
    janela_cadastro.geometry("300x450")
    janela_cadastro.title("Cadastre-se")
    janela_cadastro.resizable(width=False, height=False)

    label_cadastro_principal = Label(janela_cadastro, text="Cadastre-se", width=10, height=1,
                                     font=("Arial", 15, "bold"))
    label_cadastro_principal.place(x=80, y=15)

    label_cadastro_email = Label(janela_cadastro, text="Insira seu melhor email :", width=20, height=1)
    label_cadastro_email.place(x=10, y=50)

    entry_cadastro_email = Entry(janela_cadastro, width=45)
    entry_cadastro_email.place(x=10, y=80)

    label_usuario_cadastro = Label(janela_cadastro, text="Escolha seu usuário :", width=15, height=1)
    label_usuario_cadastro.place(x=10, y=110)

    entry_cadastro_usuario = Entry(janela_cadastro, width=45)
    entry_cadastro_usuario.place(x=10, y=130)

    label_senha_cadastro = Label(janela_cadastro, text="Escolha sua senha :", width=15, height=1)
    label_senha_cadastro.place(x=10, y=160)

    entry_cadastro_senha = Entry(janela_cadastro, width=45, show="*")
    entry_cadastro_senha.place(x=10, y=190)

    label_palavra_chave = Label(janela_cadastro, text="Defina uma palavra-chave", width=20, height=1)
    label_palavra_chave.place(x=10, y=220)

    entry_palavra_chave = Entry(janela_cadastro, width=45)
    entry_palavra_chave.place(x=10, y=250)

    botao_realizar_cadastro = Button(janela_cadastro, text="Confirmar Cadastro", command=verificar_cadastro, width=15,
                                     height=1, bg="green", fg="white")
    botao_realizar_cadastro.place(x=80, y=290)

    label_avisos_cadastramento = Label(janela_cadastro, text="", width=50, height=2)
    label_avisos_cadastramento.place(x=10, y=330)

    janela_cadastro.mainloop()


def ver_registros(id_usuario_ativo):
    global conexao
    global cursor
    global dia_atual
    global janela_ver_registros
    global meses_para_numeros
    global visualizacao_tree_view

    def captura_selecao_combobox(event):
        mes_escolhido = selecione_o_mes.get()
        mes_escolhido_inteiro = meses_para_numeros.get(mes_escolhido, 10)
        ano_escolhido = selecione_o_ano.get()
        categoria_escolhida = selecione_a_categoria.get()
        label_data_registros["text"] = f"{mes_escolhido} / {ano_escolhido}"
        if categoria_escolhida == "Todas Categorias":
            novo_comando = (f'select * from gastos where month(d_data_gastos) = "{mes_escolhido_inteiro}" and '
                            f'year(d_data_gastos) = "{ano_escolhido}" and i_iddousuario_gastos = {id_usuario_ativo}')
        else:
            novo_comando = (f'select * from gastos where month(d_data_gastos) = "{mes_escolhido_inteiro}" and '
                            f'year(d_data_gastos) = "{ano_escolhido}" and s_categoria_gastos = "{categoria_escolhida}"'
                            f' and i_iddousuario_gastos = {id_usuario_ativo}')
        cursor.execute(novo_comando)
        resultado_nova_consulta = cursor.fetchall()
        for row in visualizacao_tree_view.get_children():
            visualizacao_tree_view.delete(row)
        for item in resultado_nova_consulta:
            visualizacao_tree_view.insert("", END,
                                          values=(item[0], item[1], "R$" + " " + str(item[2]), item[3], item[4]))
        visualizacao_tree_view.update()

    janela_ver_registros = Toplevel()
    janela_ver_registros.title("Visualização Das Despesas")
    janela_ver_registros.geometry("800x650")
    nome_do_mes = dia_atual.strftime("%B")

    label_data_registros = Label(janela_ver_registros, text=f"{nome_do_mes.capitalize()} / {dia_atual.year}", width=15,
                                 height=1, font=("Arial", 15, "bold"), anchor="center")
    label_data_registros.place(x=350, y=0)

    label_escolha_mes = Label(janela_ver_registros, text="Escolha o mês e ano que deseja visualizar :", width=35,
                              height=1, font=("Arial", 11))
    label_escolha_mes.place(x=10, y=40)

    selecione_o_mes = Combobox(janela_ver_registros, width=10, state="readonly")
    selecione_o_mes["values"] = ("Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto",
                                 "Setembro", "Outubro", "Novembro", "Dezembro")
    selecione_o_mes.place(x=20, y=80)
    selecione_o_mes.set(nome_do_mes.capitalize())
    selecione_o_mes.bind('<<ComboboxSelected>>', captura_selecao_combobox)

    selecione_o_ano = Combobox(janela_ver_registros, width=10, state="readonly")
    selecione_o_ano["values"] = tuple(range(1950, dia_atual.year + 1))
    selecione_o_ano.set(dia_atual.year)
    selecione_o_ano.place(x=120, y=80)
    selecione_o_ano.bind('<<ComboboxSelected>>', captura_selecao_combobox)
    mes_escolhido = ""

    label_escolha_categoria = Label(janela_ver_registros, text="Escolha a Categoria:", width=16, height=1,
                                    font=("Arial", 11))
    label_escolha_categoria.place(x=380, y=40)

    selecione_a_categoria = Combobox(janela_ver_registros, width=15, state="readonly")
    selecione_a_categoria["values"] = ("Todas Categorias", "Alimentação", "Saúde", "Transporte", "Lazer", "Moradia",
                                       "Outros")
    selecione_a_categoria.set("Todas Categorias")
    selecione_a_categoria.place(x=380, y=80)
    selecione_a_categoria.bind('<<ComboboxSelected>>', captura_selecao_combobox)

    comando = f"select sum(f_valor_gastos) from gastos where month(d_data_gastos) = {dia_atual.month} "
    cursor.execute(comando)
    resultado = cursor.fetchall()
    comando = (f'select s_descricao_gastos from gastos where f_valor_gastos'
               f' = (select max(f_valor_gastos) from gastos) and month(d_data_gastos) = {dia_atual.month};')
    cursor.execute(comando)
    despesa_mais_alta = cursor.fetchall()
    visualizacao_tree_view = Treeview(janela_ver_registros, columns=("ID", "Descrição",
                                                                     "Valor da Despesa", "Data da Despesa",
                                                                     "Categoria da Despesa"), show="headings")
    visualizacao_tree_view.column("ID", width=15)
    visualizacao_tree_view.column("Descrição", width=100)
    visualizacao_tree_view.column("Valor da Despesa", width=15)
    visualizacao_tree_view.column("Data da Despesa", width=50)
    visualizacao_tree_view.column("Categoria da Despesa", width=50)
    visualizacao_tree_view.heading("ID", text="ID")
    visualizacao_tree_view.heading("Descrição", text="Descrição")
    visualizacao_tree_view.heading("Valor da Despesa", text="Valor da Despesa")
    visualizacao_tree_view.heading("Data da Despesa", text="Data da Despesa")
    visualizacao_tree_view.heading("Categoria da Despesa", text="Categoria da Despesa")
    visualizacao_tree_view.place(x=0, y=120, width=790, height=490)
    comando = (f"select * from gastos where month(d_data_gastos) = {dia_atual.month} and"
               f" i_iddousuario_gastos = {id_usuario_ativo};")
    cursor.execute(comando)
    resultado = cursor.fetchall()
    for elemento in resultado:
        visualizacao_tree_view.insert("", END, values=(elemento[0], elemento[1], "R$" + " " + str(elemento[2]),
                                                       elemento[3], elemento[4]))
    janela_ver_registros.resizable(width=False, height=False)
    janela_ver_registros.mainloop()
    return janela_ver_registros, visualizacao_tree_view

def inserir_registros(id_usuario_ativo):
    def confirmar_registro():
        descricao_do_gasto = entry_descricao_gasto.get()
        valor_da_despesa = entry_valor_gasto.get()
        data_da_despesa = calendario.get_date()
        categoria_da_despesa = caixa_de_selecao_categoria.get()
        padrao_valor_da_despesa = re.compile(r"^[0-9]+\.[0-9]+$")
        padrao_data_da_despesa = re.compile("^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
        checar_padrao_valor_da_despesa = padrao_valor_da_despesa.findall(valor_da_despesa)
        checar_padrao_data_da_despesa = padrao_data_da_despesa.findall(data_da_despesa)
        if len(checar_padrao_valor_da_despesa) == 0:
            label_aviso[
                "text"] = "São aceitos apenas números no valor da despesa.\nAs casas decimais são separadas por ponto."
        else:
            pass
            if len(checar_padrao_data_da_despesa) == 0:
                label_aviso["text"] = "Insira a data no seguinte formato : ANO-MES-DIA"
            else:
                pass
                if (descricao_do_gasto != "" and valor_da_despesa != "" and data_da_despesa != ""
                        and categoria_da_despesa != ""):
                    comando = ("INSERT INTO gastos (i_id_gastos, s_descricao_gastos, f_valor_gastos, d_data_gastos,"
                               " s_categoria_gastos, i_iddousuario_gastos) "
                               f"VALUES ((SELECT MAX(i_id_gastos) + 1 FROM gastos g), %s, %s, %s, %s,"
                               f" {id_usuario_ativo})")
                    valores = (descricao_do_gasto, valor_da_despesa, data_da_despesa, categoria_da_despesa)
                    cursor.execute(comando, valores)
                    conexao.commit()
                    label_aviso["fg"] = "green"
                    label_aviso["text"] = "Registro inserido com sucesso!"
                    entry_descricao_gasto.delete(0, END)
                    entry_valor_gasto.delete(0, END)
                    calendario.selection_set(dia_atual)
                    try:
                        atualiza_interface_ver_despesas(janela_ver_registros)
                    except NameError:
                        pass
                    try:
                        atualiza_janela_analise(janela_analise)
                    except NameError:
                        pass
                else:
                    label_aviso["text"] = "Preencha todos os campos"
                entry_descricao_gasto.delete(0, END)
                entry_valor_gasto.delete(0, END)

    janela_registro = Toplevel()
    janela_registro.title("Insira o Registro")
    janela_registro.geometry("400x650")
    janela_registro.resizable(width=False, height=False)

    label_inserir_registro = Label(janela_registro, text="Insira Seu Registro", width=25, height=1, font=("Arial", 15))
    label_inserir_registro.place(x=55, y=10)

    label_categoria_gasto = Label(janela_registro, text="Categoria do Gasto", width=15, height=1, font=("Arial", 11))
    label_categoria_gasto.place(x=5, y=50)

    caixa_de_selecao_categoria = Combobox(janela_registro, state="readonly")
    caixa_de_selecao_categoria["values"] = ("Outros", "Alimentação", "Saúde", "Transporte", "Lazer", "Moradia")
    caixa_de_selecao_categoria.place(x=5, y=80)

    label_descricao_gasto = Label(janela_registro, text="Descrição do Gasto :", width=15, height=1, font=("Arial", 11))
    label_descricao_gasto.place(x=5, y=120)
    entry_descricao_gasto = Entry(janela_registro, width=60)
    entry_descricao_gasto.place(x=10, y=160)

    label_valor_gasto = Label(janela_registro, text="Preço da Despesa :", width=15, height=1, font=("Arial", 11))
    label_valor_gasto.place(x=5, y=200)
    entry_valor_gasto = Entry(janela_registro, width=60)
    entry_valor_gasto.place(x=10, y=240)

    label_data_gasto = Label(janela_registro, text="Data da Despesa :", width=15, height=1, font=("Arial", 11))
    label_data_gasto.place(x=5, y=280)

    calendario = Calendar(janela_registro, selectmode="day", year=dia_atual.year, month=dia_atual.month,
                          day=dia_atual.day, date_pattern="yyyy-mm-dd",
                          locale="pt_BR")
    calendario.place(x=70, y=320)

    botao_confirmar = Button(janela_registro, command=confirmar_registro, text="Confirmar", width=15, height=1,
                             bg="black", fg="white")
    botao_confirmar.place(x=140, y=520)

    label_aviso = Label(janela_registro, text="", width=50, height=3)
    label_aviso.place(x=10, y=570)

    janela_registro.bind("<Return>", lambda event: confirmar_registro())

    janela_registro.mainloop()


def confirmar_registro(descricao_do_gasto, valor_da_despesa, data_da_despesa):
    if descricao_do_gasto != "" and valor_da_despesa != "" and data_da_despesa != "":
        comando = (f'INSERT INTO gastos (i_id_gastos, s_descricao_gastos, f_valor_gastos, d_data_gastos)'
                   f'values ((select max(i_id_gastos) + 1 from gastos g), "{descricao_do_gasto}", "{valor_da_despesa}",'
                   f'"{data_da_despesa}"')
        cursor.execute(comando)
        conexao.commit()
    else:
        pass


def editar_registros(id_usuario_ativo):
    categorias_disponiveis = None

    def captura_selecao_option_menu(*args):
        nonlocal categorias_disponiveis
        valor_selecionado = variavel_menu_colunas.get()

        if valor_selecionado == "Categoria da Despesa":
            categorias_disponiveis = Combobox(janela_editar_registros)
            categorias_disponiveis["values"] = ['Alimentação', 'Saúde', "Transporte", "Lazer", "Moradia", "Outros"]
            entry_novo_valor.config(state="disabled")
            categorias_disponiveis["width"] = 23
            categorias_disponiveis.place(x=10, y=260)
        elif categorias_disponiveis != "Categoria da Despesa":
            try:
                categorias_disponiveis.destroy()
            except AttributeError:
                pass
            entry_novo_valor.config(state="normal")
            janela_editar_registros.update()

    janela_editar_registros = Toplevel()
    janela_editar_registros.title("Editar Registros")
    janela_editar_registros.geometry("400x400")
    janela_editar_registros.resizable(width=False, height=False)

    label_edite_seus_registros = Label(janela_editar_registros, text="Edite Seus Registros", width=20, height=1,
                                       font=("Arial", 15))
    label_edite_seus_registros.place(x=100, y=30)

    label_id_do_registro = Label(janela_editar_registros, text="Insira o ID do registro :",
                                 width=20, height=1, font=("Arial", 10), anchor="w")
    label_id_do_registro.place(x=10, y=90)

    entry_id_do_registro = Entry(janela_editar_registros, width=10)
    entry_id_do_registro.place(x=10, y=120)

    botao_ver_id_do_registro = Button(janela_editar_registros, text="Consultar ID's", width=12, height=1,
                                      command=lambda: ver_registros(id_usuario_ativo), bg="black", fg="white")
    botao_ver_id_do_registro.place(x=100, y=120)

    label_escolha_do_atributo = Label(janela_editar_registros, text="Escolha o que deseja editar :", width=20, height=1,
                                      font=("Arial", 10))
    label_escolha_do_atributo.place(x=10, y=150)

    colunas = ["Descrição da Despesa", "Valor da Despesa", "Data da Despesa", "Categoria da Despesa"]
    variavel_menu_colunas = StringVar()
    variavel_menu_colunas.set(colunas[0])
    menu_colunas = OptionMenu(janela_editar_registros, variavel_menu_colunas, command=captura_selecao_option_menu,
                              *colunas)
    menu_colunas.place(x=10, y=180)

    label_insira_novo_valor = Label(janela_editar_registros, text="Insira o novo valor do campo :", width=21, height=1,
                                    font=("Arial", 10))
    label_insira_novo_valor.place(x=10, y=220)

    entry_novo_valor = Entry(janela_editar_registros, width=25)
    entry_novo_valor.place(x=10, y=260)

    botao_confirmar_edicao = Button(janela_editar_registros, command=lambda: edicao_registro_bd(entry_id_do_registro,
                                                                                                variavel_menu_colunas,
                                                                                                entry_novo_valor,
                                                                                                label_aviso_edicao,
                                                                                                categorias_disponiveis,
                                                                                                id_usuario_ativo),
                                    text="Editar Registro", width=12, height=1,
                                    bg="green", fg="white")
    botao_confirmar_edicao.place(x=110, y=300)

    botao_deletar_registro = Button(janela_editar_registros, command=lambda: deletar_registros(entry_id_do_registro,
                                                                                               label_aviso_edicao),
                                    text="Deletar Registro", width=12, height=1, bg="red",
                                    fg="white")
    botao_deletar_registro.place(x=215, y=300)

    label_aviso_edicao = Label(janela_editar_registros, text="", width=30, height=2, fg="red",
                               font=("Arial", 10, "bold"))
    label_aviso_edicao.place(x=80, y=340)

    janela_editar_registros.mainloop()
    return entry_id_do_registro, variavel_menu_colunas, entry_novo_valor, label_aviso_edicao, variavel_menu_colunas


def edicao_registro_bd(entry_id_do_registro, variavel_menu_colunas, entry_novo_valor, label_aviso_edicao,
                       categorias_disponiveis, id_usuario_ativo):
    global cursor
    global conexao
    id_do_registro = entry_id_do_registro.get()
    campo_do_registro = variavel_menu_colunas.get()
    novo_valor_do_registro = entry_novo_valor.get()
    if campo_do_registro == "Descrição da Despesa":
        coluna_edicao = "s_descricao_gastos"
    elif campo_do_registro == "Valor da Despesa":
        coluna_edicao = "f_valor_gastos"
    elif campo_do_registro == "Data da Despesa":
        coluna_edicao = "d_data_gastos"
    elif campo_do_registro == "Categoria da Despesa":
        coluna_edicao = "s_categoria_gastos"
        novo_valor_do_registro = categorias_disponiveis.get()
    padrao_id_do_registro = re.compile("^[0-9]+$")
    checagem_padrao_id_do_registro = padrao_id_do_registro.findall(id_do_registro)
    if len(checagem_padrao_id_do_registro) == 0:
        label_aviso_edicao["width"] = 35
        label_aviso_edicao["text"] = "O ID de Registro deve ser um número inteiro."
    if campo_do_registro == "Valor da Despesa":
        padrao_valor_despesa = re.compile("^[0-9]+\\.[0-9]+$")
        checar_padrao_valor_despesa = padrao_valor_despesa.findall(novo_valor_do_registro)
        if len(checar_padrao_valor_despesa) == 0:
            label_aviso_edicao["width"] = 35
            label_aviso_edicao["text"] = "O valor da despesa deve ser um número\n com . decimal."
        else:
            pass
    if campo_do_registro == "Data da Despesa":
        padrao_data_da_despesa = re.compile("^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
        checar_padrao_data_da_despesa = padrao_data_da_despesa.findall(novo_valor_do_registro)
        if len(checar_padrao_data_da_despesa) == 0:
            label_aviso_edicao["text"] = "Formato correto :\nYEAR-MONTH-DAY"
        else:
            pass
    else:
        comando = (f'select * from gastos where i_id_gastos = "{id_do_registro}" and'
                   f' i_iddousuario_gastos = {id_usuario_ativo}')
        cursor.execute(comando)
        resultado = cursor.fetchall()
        if len(resultado) > 0:
            try:
                comando_de_edicao = (f'UPDATE gastos set {coluna_edicao} = "{novo_valor_do_registro}" where i_id_gastos'
                                     f'= {id_do_registro} and i_iddousuario_gastos = {id_usuario_ativo}; ')
                cursor.execute(comando_de_edicao)
                conexao.commit()
                label_aviso_edicao["fg"] = "green"
                label_aviso_edicao["text"] = "Registro editado com sucesso."
                try:
                    atualiza_interface_ver_despesas(janela_ver_registros, janela_analise)
                except NameError:
                    pass
            except:
                label_aviso_edicao["text"] = "Não foi possível realizar a edição.Ocorreu um erro."
        else:
            label_aviso_edicao["fg"] = "red"
            label_aviso_edicao["height"] = 3
            label_aviso_edicao["text"] = "Não foi possível atualizar o Registro.\nConfira o ID e o formato do valor."
    return id_do_registro


def deletar_registros(entry_id_do_registro, label_aviso_edicao):
    global cursor
    global conexao
    id_do_registro = entry_id_do_registro.get()
    padrao_do_id = re.compile("^[0-9]+$")
    checagem_padrao_do_id = padrao_do_id.findall(id_do_registro)
    if id_do_registro != "" and len(checagem_padrao_do_id) > 0:
        comando_verificacao_existencia = f'SELECT * from gastos where i_id_gastos = {id_do_registro}'
        cursor.execute(comando_verificacao_existencia)
        confirmacao_existencia = cursor.fetchall()
        if len(confirmacao_existencia) > 0:
            confirmacao_de_exclusao = messagebox.askyesno("Confirmação de Exclusão",
                                                          "ATENÇÃO ! A exclusão de um registro é permanente."
                                                          "\nVocê deseja continuar?")
            if confirmacao_de_exclusao:
                comando_exclusao = f'DELETE from gastos where i_id_gastos = {id_do_registro}'
                cursor.execute(comando_exclusao)
                conexao.commit()
                label_aviso_edicao["text"] = "Registro removido com sucesso."
                entry_id_do_registro.delete(0, END)
            else:
                label_aviso_edicao["text"] = "Exclusão cancelada com sucesso."
        else:
            label_aviso_edicao["width"] = 40
            label_aviso_edicao["text"] = "Não existe registros com o ID informado."
    else:
        label_aviso_edicao["text"] = "É necessário inserir um ID.\nO ID é um número inteiro."


def analise_orcamento(id_usuario_ativo):
    global janela_analise

    def imprimir_analise():
        global cursor
        global conexao
        global meses_para_numeros
        mes_escolhido_nome = caixa_de_selecao_mes.get()
        mes_escolhido_numero = meses_para_numeros.get(mes_escolhido_nome)
        ano_escolhido = spinbox_ano_de_analise.get()
        comando_total_gastos_mensal = (f"SELECT SUM(f_valor_gastos) from gastos where month(d_data_gastos) = "
                                       f"{mes_escolhido_numero} and year(d_data_gastos) = {ano_escolhido}"
                                       f" and i_iddousuario_gastos = {id_usuario_ativo}")
        cursor.execute(comando_total_gastos_mensal)
        resultado_total_mensal = cursor.fetchall()
        valor_total_mensal = resultado_total_mensal[0][0]
        if valor_total_mensal is not None:
            pass
        else:
            valor_total_mensal = 0
        label_total_gastos_mensal["width"] = 20
        label_total_gastos_mensal["text"] = f"Total de Gastos : R${valor_total_mensal}"
        lista_de_categorias = ['Alimentação', 'Saúde', "Transporte", "Lazer", "Moradia", "Outros"]
        lista_valores_categorias = []
        for categoria in lista_de_categorias:
            comando_gastos_mensal_por_categoria = (f"SELECT SUM(f_valor_gastos) from gastos where month(d_data_gastos)"
                                                   f" = {mes_escolhido_numero} and year(d_data_gastos) "
                                                   f"= {ano_escolhido} and s_categoria_gastos = '{categoria}'"
                                                   f" and i_iddousuario_gastos = {id_usuario_ativo}")
            cursor.execute(comando_gastos_mensal_por_categoria)
            resultado_valor_total_da_categoria = cursor.fetchall()
            valor_total_da_categoria = resultado_valor_total_da_categoria[0][0]
            if valor_total_da_categoria is None:
                valor_total_da_categoria = 0
            lista_valores_categorias.append(valor_total_da_categoria)
        valor_total_alimentacao = lista_valores_categorias[0]
        valor_total_saude = lista_valores_categorias[1]
        valor_total_transporte = lista_valores_categorias[2]
        valor_total_lazer = lista_valores_categorias[3]
        valor_total_moradia = lista_valores_categorias[4]
        valor_total_outros = lista_valores_categorias[5]
        label_total_gastos_mensal["height"] = 13
        label_total_gastos_mensal["width"] = 50
        label_total_gastos_mensal["justify"] = "left"
        label_total_gastos_mensal["text"] = (f"Total de Gastos Mensal : R${valor_total_mensal:.2f}\n\n"
                                             f"Total de Gastos Alimentação : R${valor_total_alimentacao:.2f}\n\n"
                                             f"Total de Gastos Saúde : R${valor_total_saude:.2f}\n\n"
                                             f"Total de Gastos Transporte: R${valor_total_transporte:.2f}\n\n"
                                             f"Total de Gastos Lazer : R${valor_total_lazer:.2f}\n\n"
                                             f"Total de Gastos Moradia : R${valor_total_moradia:.2f}\n\n"
                                             f"Total de Gastos Outros : R${valor_total_outros:.2f}")
        labels = ["Alimentação", "Saúde", "Transporte", "Lazer", "Moradia", "Outros"]
        sizes = [valor_total_alimentacao, valor_total_saude, valor_total_transporte, valor_total_lazer,
                 valor_total_moradia, valor_total_outros]
        sizes = [0 if value is None else value for value in sizes]
        colors = ["Red", "Blue", "Yellow", "Orange", "Black", "Pink"]
        fig, ax = plt.subplots(figsize=(4, 3))
        ax.bar(labels, sizes, color=colors)
        ax.set_title("Gastos por Categoria")
        ax.set_xlabel("Categorias")
        ax.set_ylabel("Valores em R$")

        plt.xticks(rotation=45)
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=janela_analise)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.place(x=20, y=390)

    janela_analise = Toplevel()
    janela_analise.title("Análise Financeira")
    janela_analise.geometry("450x700")
    janela_analise.resizable(width=False, height=False)

    label_analise_titulo = Label(janela_analise, text="Análise Financeira das Despesas", width=30, height=1,
                                 fg="black", font=("Arial", 13, "bold"))
    label_analise_titulo.place(x=60, y=20)

    label_mes_analise = Label(janela_analise, text="Escolha a data :", width=15, height=1, fg="black",
                              font=("Arial", 11))
    label_mes_analise.place(x=15, y=70)

    caixa_de_selecao_mes = Combobox(janela_analise, width=10, state="readonly")
    caixa_de_selecao_mes["values"] = ("Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto",
                                      "Setembro", "Outubro", "Novembro", "Dezembro")
    caixa_de_selecao_mes.place(x=30, y=110)

    label_ano_analise = Label(janela_analise, text="Ano :", width=5, height=1, fg="black", font=("Arial", 11))
    label_ano_analise.place(x=190, y=70)

    ano_padrao_spinboxanalise = StringVar()
    ano_padrao_spinboxanalise.set(f"{dia_atual.year}")
    spinbox_ano_de_analise = Spinbox(janela_analise, from_=2010, to=2024, width=8, state="readonly",
                                     readonlybackground="white", textvariable=ano_padrao_spinboxanalise)
    spinbox_ano_de_analise.place(x=190, y=110)

    botao_analisar = Button(janela_analise, command=imprimir_analise, text="OK", width=5, height=1, bg="green",
                            fg="white")
    botao_analisar.place(x=330, y=100)

    label_total_gastos_mensal = Label(janela_analise, text="Total de Gastos:", width=15, height=1, fg="black",
                                      font=("Arial", 11))
    label_total_gastos_mensal.place(x=10, y=160)

    janela_analise.bind("<Return>", lambda event: imprimir_analise())
    janela_analise.mainloop()
    return janela_analise


def atualiza_interface_ver_despesas(janela_ver_registros):
    try:
        situacao_janela_ver_registros = janela_ver_registros.winfo_exists()
        janela_ver_registros.destroy()
        if situacao_janela_ver_registros == 1:
            ver_registros(id_usuario_ativo)
        else:
            pass
    except:
        pass


def atualiza_janela_analise(janela_analise):
    try:
        janela_analise.destroy()
    except:
        pass


login()

if estado_do_login is True:
    janela = Tk()
    janela.title("Controlador de Despesas")
    janela.geometry("400x350")
    janela.resizable(width=False, height=False)

    boas_vindas = Label(janela, text="Bem Vindo ao Controlador \nde Despesas", width=30, height=2, fg="blue",
                        font=("Arial", 15))
    boas_vindas.place(x=35, y=40)

    label_opcoes = Label(janela, text="Escolha as opções :", width=15, height=1, fg="black", font=("Arial", 12))
    label_opcoes.place(x=10, y=150)

    botao_inserir_registro = Button(janela, command=lambda: inserir_registros(id_usuario_ativo),
                                    text="Inserir Registro", width=15, height=1, bg="black", fg="white")
    botao_inserir_registro.place(x=10, y=200)

    botao_editar_registros = Button(janela, command=lambda: editar_registros(id_usuario_ativo), text="Editar Registros",
                                    width=15, height=1,
                                    bg="black", fg="white")
    botao_editar_registros.place(x=130, y=200)

    botao_ver_despesas = Button(janela, command=lambda: ver_registros(id_usuario_ativo), text="Ver Despesas", width=15,
                                height=1, bg="black",
                                fg="white")
    botao_ver_despesas.place(x=250, y=200)

    botao_ver_analise = Button(janela, command=lambda: analise_orcamento(id_usuario_ativo), text="Ver Análise",
                               width=15, height=1, bg="black",
                               fg="white")
    botao_ver_analise.place(x=130, y=240)

    janela.mainloop()
