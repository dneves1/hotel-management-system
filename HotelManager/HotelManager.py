#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import random
from datetime import datetime, timedelta

# ─────────────────────────────────────────────
#  ARQUIVOS DE PERSISTÊNCIA (TXT)
# ─────────────────────────────────────────────
# usuarios.txt  → nome|senha|email|area|is_admin
# reservas.txt  → blocos separados por ---
# cardapio.txt  → categoria|nome_item|preco

ARQUIVO_USUARIOS = "usuarios.txt"
ARQUIVO_RESERVAS = "reservas.txt"
ARQUIVO_CARDAPIO = "cardapio.txt"

# ── SALVAR ────────────────────────────────────
def salvar_usuarios():
    arq = open(ARQUIVO_USUARIOS, "w", encoding="utf-8")
    for nome, u in usuarios.items():
        is_admin = "1" if u.get("is_admin") else "0"
        arq.write(nome + "|" + u["senha"] + "|" + u["email"] + "|" + u["area"] + "|" + is_admin + "\n")
    arq.close()

def salvar_reservas():
    arq = open(ARQUIVO_RESERVAS, "w", encoding="utf-8")
    for r in reservas.values():
        arq.write("---\n")
        ativa_str = "1" if r["ativa"] else "0"
        arq.write(r["codigo"] + "|" + ativa_str + "|" + str(r["qtd_pessoas"]) + "|" +
                  str(r["noites"]) + "|" + str(r["suite_id"]) + "|" +
                  r["suite_nome"] + "|" + str(r["quarto"]) + "\n")
        arq.write(str(r["valor_diarias"]) + "|" + str(r["gastos_restaurante"]) + "|" +
                  r["checkin"] + "|" + r["checkin_dt"] + "\n")
        if r.get("checkout"):
            arq.write(r["checkout"] + "|" + r["checkout_dt"] + "|" + str(r["total_pago"]) + "\n")
        else:
            arq.write("sem_checkout\n")
        arq.write(",".join(r["cpfs"]) + "\n")
        arq.write("PEDIDOS|" + str(len(r["pedidos"])) + "\n")
        for p in r["pedidos"]:
            itens_str = ";".join(item[0] + ":" + str(item[1]) for item in p["itens"])
            arq.write(p["data"] + "|" + str(p["subtotal"]) + "|" + itens_str + "\n")
    arq.close()

def salvar_cardapio():
    arq = open(ARQUIVO_CARDAPIO, "w", encoding="utf-8")
    for cat, itens in CARDAPIO.items():
        for nome_item, preco in itens:
            arq.write(cat + "|" + nome_item + "|" + str(preco) + "\n")
    arq.close()

# ── CARREGAR ──────────────────────────────────
def carregar_dados():
    global usuarios, reservas

    if os.path.exists(ARQUIVO_USUARIOS):
        arq = open(ARQUIVO_USUARIOS, "r", encoding="utf-8")
        linha = arq.readline()
        while linha != "":
            linha = linha.strip()
            if linha != "":
                partes = linha.split("|")
                nome  = partes[0]
                senha = partes[1]
                email = partes[2]
                area  = partes[3]
                is_admin = len(partes) > 4 and partes[4] == "1"
                usuarios[nome] = {"senha": senha, "email": email, "area": area, "is_admin": is_admin}
            linha = arq.readline()
        arq.close()

    if os.path.exists(ARQUIVO_RESERVAS):
        arq = open(ARQUIVO_RESERVAS, "r", encoding="utf-8")
        linha = arq.readline()
        while linha != "":
            linha = linha.strip()
            if linha == "---":
                l1 = arq.readline().strip().split("|")
                codigo      = l1[0]
                ativa       = l1[1] == "1"
                qtd_pessoas = int(l1[2])
                noites      = int(l1[3])
                suite_id    = int(l1[4])
                suite_nome  = l1[5]
                quarto      = int(l1[6])
                l2 = arq.readline().strip().split("|")
                valor_diarias      = float(l2[0])
                gastos_restaurante = float(l2[1])
                checkin            = l2[2]
                checkin_dt         = l2[3]
                l3 = arq.readline().strip()
                if l3 == "sem_checkout":
                    checkout = ""
                    checkout_dt = ""
                    total_pago = 0.0
                else:
                    partes_co   = l3.split("|")
                    checkout    = partes_co[0]
                    checkout_dt = partes_co[1]
                    total_pago  = float(partes_co[2])
                cpfs = arq.readline().strip().split(",")
                l_ped = arq.readline().strip().split("|")
                qtd_pedidos = int(l_ped[1])
                pedidos = []
                for _ in range(qtd_pedidos):
                    lp = arq.readline().strip().split("|")
                    data_ped = lp[0]
                    subtotal = float(lp[1])
                    itens = []
                    if len(lp) > 2 and lp[2] != "":
                        for item_str in lp[2].split(";"):
                            partes_item = item_str.split(":")
                            itens.append((partes_item[0], float(partes_item[1])))
                    pedidos.append({"data": data_ped, "subtotal": subtotal, "itens": itens})
                reservas[codigo] = {
                    "codigo": codigo, "ativa": ativa, "qtd_pessoas": qtd_pessoas,
                    "noites": noites, "suite_id": suite_id, "suite_nome": suite_nome,
                    "quarto": quarto, "valor_diarias": valor_diarias,
                    "gastos_restaurante": gastos_restaurante, "checkin": checkin,
                    "checkin_dt": checkin_dt, "checkout": checkout,
                    "checkout_dt": checkout_dt, "total_pago": total_pago,
                    "cpfs": cpfs, "pedidos": pedidos,
                }
            linha = arq.readline()
        arq.close()

    if os.path.exists(ARQUIVO_CARDAPIO):
        for cat in list(CARDAPIO.keys()):
            CARDAPIO[cat] = []
        arq = open(ARQUIVO_CARDAPIO, "r", encoding="utf-8")
        linha = arq.readline()
        while linha != "":
            linha = linha.strip()
            if linha != "":
                partes = linha.split("|")
                cat       = partes[0]
                nome_item = partes[1]
                preco     = float(partes[2])
                if cat in CARDAPIO:
                    CARDAPIO[cat].append((nome_item, preco))
            linha = arq.readline()
        arq.close()

# ─────────────────────────────────────────────
#  DADOS EM MEMÓRIA
# ─────────────────────────────────────────────
# usuarios: dicionário de dicionários {nome -> {senha, email, area, is_admin}}
usuarios = {}
# reservas: dicionário de dicionários {codigo -> {dados da reserva + lista de pedidos}}
reservas = {}

# CARDAPIO: dicionário de listas de tuplas {categoria -> [(nome, preco), ...]}
CARDAPIO = {
    "Comidas": [
        ("Frango Grelhado",       35.00),
        ("Filé ao Molho Madeira", 55.00),
        ("Macarrão ao Alho e Óleo", 28.00),
        ("Salada Caesar",         22.00),
        ("Sanduíche Club",        30.00),
    ],
    "Bebidas": [
        ("Água Mineral 500ml",  6.00),
        ("Suco Natural",       12.00),
        ("Refrigerante Lata",   8.00),
        ("Cerveja Artesanal",  18.00),
        ("Vinho Taça",         25.00),
    ],
    "Sobremesas": [
        ("Petit Gâteau",       22.00),
        ("Sorvete 2 Bolas",    14.00),
        ("Brownie c/ Calda",   18.00),
        ("Mousse de Maracujá", 16.00),
        ("Cheesecake",         20.00),
    ],
}

SUITES = {
    1: {"nome": "Standard", "andar": 1, "diaria": 300.0, "extra_pessoa": 50.0},
    2: {"nome": "Luxo",     "andar": 2, "diaria": 450.0, "extra_pessoa": 100.0},
    3: {"nome": "Master",   "andar": 3, "diaria": 600.0, "extra_pessoa": 150.0},
}

# ─────────────────────────────────────────────
#  UTILITÁRIOS
# ─────────────────────────────────────────────
def limpar():
    print("\033[2J\033[H", end="")

def linha(c="─", n=55):
    print(c * n)

def cabecalho(titulo):
    limpar()
    linha("═")
    print(f"  🏨  HOTEL GRANDEUR  –  {titulo}")
    linha("═")

def pausar():
    input("\n  [Enter para continuar]")

# Gera um código de reserva de 4 dígitos não utilizado
def gerar_codigo(dict_reservas):
    while True:
        cod = str(random.randint(1000, 9999))
        if cod not in dict_reservas:
            return cod

def data_hoje():
    return datetime.now()

# Retorna True se houver pelo menos um admin cadastrado
def tem_admin(dict_usuarios):
    for u in dict_usuarios.values():
        if u.get("is_admin"):
            return True
    return False

# ─────────────────────────────────────────────
#  SETUP INICIAL — cria conta de administrador
# ─────────────────────────────────────────────
def setup_inicial():
    cabecalho("CONFIGURAÇÃO INICIAL")
    print("  Bem-vindo ao Hotel Grandeur!")
    print("  Nenhum administrador encontrado.")
    print("  Crie a conta de administrador master:\n")
    nome = input("  Nome de usuário: ").strip()
    while nome == "":
        print("  ⚠️  Nome não pode ser vazio.")
        nome = input("  Nome de usuário: ").strip()
    email = input("  E-mail: ").strip()
    senha = input("  Senha: ").strip()
    while senha == "":
        print("  ⚠️  Senha não pode ser vazia.")
        senha = input("  Senha: ").strip()
    usuarios[nome] = {
        "senha": senha,
        "email": email,
        "area": "administracao",
        "is_admin": True,
    }
    salvar_usuarios()
    print(f"\n  ✅  Administrador '{nome}' criado com sucesso!")
    pausar()

# ─────────────────────────────────────────────
#  AUTENTICAÇÃO
# ─────────────────────────────────────────────
def tela_inicial():
    while True:
        limpar()
        cabecalho("TELA INICIAL")
        print("  1 – Login")
        print("  2 – Registrar-se")
        print("  0 – Sair")
        linha()
        op = input("  Opção: ").strip()
        if op == "1":
            usuario = fazer_login(usuarios)
            if usuario:
                return usuario
        elif op == "2":
            registrar_usuario()
        elif op == "0":
            print("\n  Até logo!\n")
            exit()

# Recebe o dicionário de usuários, valida login e retorna o usuário ou None
def fazer_login(dict_usuarios):
    cabecalho("LOGIN")
    nome = input("  Nome: ").strip()
    senha = input("  Senha: ").strip()
    u = dict_usuarios.get(nome)
    if u and u["senha"] == senha:
        print(f"\n  ✅  Bem-vindo(a), {nome}!")
        pausar()
        return {"nome": nome, **u}
    print("\n  ❌  Usuário ou senha incorretos.")
    pausar()
    return None

def registrar_usuario():
    cabecalho("REGISTRAR-SE")
    nome = input("  Nome: ").strip()
    if nome in usuarios:
        print("  ⚠️  Nome já cadastrado.")
        pausar()
        return
    email = input("  E-mail: ").strip()
    senha = input("  Senha: ").strip()
    print("\n  Área de trabalho:")
    print("    1 – Administração")
    print("    2 – Restaurante")
    area_op = input("  Opção: ").strip()
    area = "administracao" if area_op == "1" else "restaurante"
    usuarios[nome] = {"senha": senha, "email": email, "area": area, "is_admin": False}
    salvar_usuarios()
    print(f"\n  ✅  Usuário '{nome}' cadastrado na área de {area}.")
    pausar()

# ─────────────────────────────────────────────
#  ÁREA: RESTAURANTE
# ─────────────────────────────────────────────
def menu_restaurante(usuario):
    while True:
        limpar()
        cabecalho(f"RESTAURANTE  –  {usuario['nome']}")
        print("  1 – Registrar pedido do cliente")
        print("  2 – Listar cardápio")
        print("  0 – Sair")
        linha()
        op = input("  Opção: ").strip()
        if op == "1":
            registrar_pedido()
        elif op == "2":
            listar_cardapio()
        elif op == "0":
            break

def listar_cardapio():
    cabecalho("CARDÁPIO COMPLETO")
    for cat, itens in CARDAPIO.items():
        linha("─")
        print(f"  {cat}")
        linha("─")
        if not itens:
            print("  (nenhum item cadastrado)")
        for i, (nome_item, preco) in enumerate(itens, 1):
            print(f"    {i}. {nome_item:<30} R$ {preco:.2f}")
    linha("═")
    pausar()

def registrar_pedido():
    cabecalho("REGISTRAR PEDIDO")
    categorias = list(CARDAPIO.keys())
    for i, cat in enumerate(categorias, 1):
        print(f"  {i} – {cat}")
    print("  0 – Cancelar")
    linha()
    op = input("  Categoria: ").strip()
    if op == "0":
        return
    try:
        cat = categorias[int(op) - 1]
    except (ValueError, IndexError):
        print("  ⚠️  Opção inválida.")
        pausar()
        return

    cabecalho(f"CARDÁPIO – {cat}")
    itens = CARDAPIO[cat]
    if not itens:
        print("  ⚠️  Nenhum item nessa categoria.")
        pausar()
        return
    for i, (nome_item, preco) in enumerate(itens, 1):
        print(f"  {i} – {nome_item:<30} R$ {preco:.2f}")
    linha()
    selecionados = input("  Números dos itens (ex: 1 3): ").strip().split()

    pedido = []
    total = 0.0
    for s in selecionados:
        try:
            item = itens[int(s) - 1]
            pedido.append(item)
            total += item[1]
        except (ValueError, IndexError):
            pass

    if not pedido:
        print("  ⚠️  Nenhum item válido selecionado.")
        pausar()
        return

    cod = input("\n  Código de reserva do cliente: ").strip()
    if cod not in reservas:
        print("  ❌  Reserva não encontrada.")
        pausar()
        return
    if not reservas[cod]["ativa"]:
        print("  ❌  Essa reserva já foi encerrada.")
        pausar()
        return

    reservas[cod]["gastos_restaurante"] += total
    reservas[cod]["pedidos"].append({
        "data": data_hoje().strftime("%d/%m/%Y %H:%M"),
        "itens": pedido,
        "subtotal": total,
    })
    salvar_reservas()

    print(f"\n  ✅  Pedido adicionado à reserva {cod}.")
    print(f"     Itens: {', '.join(n for n, _ in pedido)}")
    print(f"     Subtotal: R$ {total:.2f}")
    pausar()

# ─────────────────────────────────────────────
#  ÁREA: ADMINISTRAÇÃO
# ─────────────────────────────────────────────
def menu_administracao(usuario):
    while True:
        limpar()
        cabecalho(f"ADMINISTRAÇÃO  –  {usuario['nome']}")
        print("  1 – Check-In")
        print("  2 – Check-Out")
        print("  3 – Consultar Reservas Ativas")
        print("  4 – Mudar Hóspede de Quarto")
        print("  5 – Estatísticas")
        print("  6 – Gerenciar Cardápio")
        if usuario.get("is_admin"):
            print("  7 – Gerenciar Usuários  [ADMIN]")
        print("  0 – Sair")
        linha()
        op = input("  Opção: ").strip()
        if op == "1":
            fazer_checkin()
        elif op == "2":
            fazer_checkout()
        elif op == "3":
            consultar_reservas()
        elif op == "4":
            mudar_quarto()
        elif op == "5":
            menu_estatisticas()
        elif op == "6":
            menu_cardapio()
        elif op == "7" and usuario.get("is_admin"):
            menu_usuarios(usuario)
        elif op == "0":
            break

# Recebe dados da suíte, quantidade de pessoas e noites,
# retorna o valor total a ser cobrado pelas diárias
def calcular_valor_diaria(suite, qtd_pessoas, noites):
    return (suite["diaria"] + suite["extra_pessoa"] * qtd_pessoas) * noites

# Busca o primeiro quarto disponível no andar da suíte escolhida.
# Retorna o número do quarto ou None se não houver vaga
def buscar_quarto_disponivel(dict_reservas, suite_id, andar, cod_excluir=None):
    quartos_usados = set()
    for r in dict_reservas.values():
        if r["suite_id"] == suite_id and r["ativa"] and r["codigo"] != cod_excluir:
            quartos_usados.add(r["quarto"])
    for n in range(1, 16):
        num = andar * 100 + n
        if num not in quartos_usados:
            return num
    return None

# ── CHECK-IN ──────────────────────────────────
def fazer_checkin():
    cabecalho("CHECK-IN")

    qtd_str = input("  Quantas pessoas na reserva? ").strip()
    try:
        qtd = int(qtd_str)
        if qtd < 1:
            raise ValueError
    except ValueError:
        print("  ⚠️  Número inválido.")
        pausar()
        return

    cpfs = []
    nomes = []
    for i in range(1, qtd + 1):
        nome_hosp = input(f"  Nome da {i}ª pessoa: ").strip()
        nomes.append(nome_hosp)
        cpf = input(f"  CPF da {i}ª pessoa: ").strip()
        cpfs.append(cpf)

    noites_str = input("  Quantas noites de estadia? ").strip()
    try:
        noites = int(noites_str)
        if noites < 1:
            raise ValueError
    except ValueError:
        print("  ⚠️  Número inválido.")
        pausar()
        return

    print("\n  Tipo de suíte:")
    for k, v in SUITES.items():
        print(f"    {k} – {v['nome']:10s}  R$ {v['diaria']:.2f}/noite  +R$ {v['extra_pessoa']:.2f} por pessoa")

    suite_op = input("  Opção: ").strip()
    try:
        suite_id = int(suite_op)
        suite = SUITES[suite_id]
    except (ValueError, KeyError):
        print("  ⚠️  Suíte inválida.")
        pausar()
        return

    valor_diaria = calcular_valor_diaria(suite, qtd, noites)
    codigo = gerar_codigo(reservas)
    checkin_dt = data_hoje()

    andar = suite["andar"]
    quarto_num = buscar_quarto_disponivel(reservas, suite_id, andar)

    if quarto_num is None:
        print("  ❌  Não há quartos disponíveis nesse tipo de suíte.")
        pausar()
        return

    reservas[codigo] = {
        "codigo": codigo, "cpfs": cpfs, "nomes": nomes, "qtd_pessoas": qtd,
        "noites": noites, "suite_id": suite_id, "suite_nome": suite["nome"],
        "quarto": quarto_num, "valor_diarias": valor_diaria,
        "gastos_restaurante": 0.0, "pedidos": [],
        "checkin": checkin_dt.strftime("%d/%m/%Y %H:%M"),
        "checkin_dt": checkin_dt.isoformat(), "ativa": True,
        "checkout": "", "checkout_dt": "", "total_pago": 0.0,
    }
    salvar_reservas()

    linha()
    print(f"  ✅  CHECK-IN REALIZADO COM SUCESSO")
    print(f"     Código de Reserva : {codigo}")
    print(f"     Quarto            : {quarto_num}  ({suite['nome']} – {andar}º andar)")
    print(f"     Hóspedes          : {qtd} pessoa(s)")
    for i in range(qtd):
        print(f"       {i+1}. {nomes[i]}  –  CPF: {cpfs[i]}")
    print(f"     Noites            : {noites}")
    print(f"     Valor Diárias     : R$ {valor_diaria:.2f}")
    linha()
    pausar()

# ── CHECK-OUT ─────────────────────────────────
def fazer_checkout():
    cabecalho("CHECK-OUT")
    cod = input("  Código de reserva: ").strip()
    r = reservas.get(cod)
    if not r:
        print("  ❌  Reserva não encontrada.")
        pausar()
        return
    if not r["ativa"]:
        print("  ⚠️  Esta reserva já foi encerrada.")
        pausar()
        return

    D = r["valor_diarias"]
    R = r["gastos_restaurante"]
    total = D + R

    linha()
    print(f"  RESUMO DA RESERVA {cod}")
    linha()
    nomes = r.get("nomes", [])
    for i in range(r["qtd_pessoas"]):
        nome_exib = nomes[i] if i < len(nomes) else "—"
        print(f"  Hóspede {i+1}         : {nome_exib}  –  CPF: {r['cpfs'][i]}")
    print(f"  Suíte             : {r['suite_nome']}  –  Quarto {r['quarto']}")
    print(f"  Check-In          : {r['checkin']}")
    print(f"  Noites            : {r['noites']}")
    print(f"  Gastos com Diárias: R$ {D:.2f}")
    print(f"  Gastos Restaurante: R$ {R:.2f}")
    linha("─")
    print(f"  TOTAL A PAGAR     : R$ {total:.2f}")
    linha("═")

    conf = input("  Confirmar checkout? (s/n): ").strip().lower()
    if conf == "s":
        reservas[cod]["ativa"] = False
        reservas[cod]["checkout"] = data_hoje().strftime("%d/%m/%Y %H:%M")
        reservas[cod]["checkout_dt"] = data_hoje().isoformat()
        reservas[cod]["total_pago"] = total
        salvar_reservas()
        print("  ✅  Checkout realizado. Até a próxima!")
    else:
        print("  ↩️  Operação cancelada.")
    pausar()

# ── CONSULTAR RESERVAS ────────────────────────
def consultar_reservas():
    cabecalho("RESERVAS ATIVAS")
    ativas = [r for r in reservas.values() if r["ativa"]]
    if not ativas:
        print("  Nenhuma reserva ativa no momento.")
        pausar()
        return

    for r in ativas:
        nomes = r.get("nomes", [])
        linha("─")
        print(f"  Código    : {r['codigo']}")
        print(f"  Quarto    : {r['quarto']}  ({r['suite_nome']})")
        print(f"  Hóspedes  : {r['qtd_pessoas']} pessoa(s)")
        for i in range(r["qtd_pessoas"]):
            nome_exib = nomes[i] if i < len(nomes) else "—"
            print(f"    {i+1}. {nome_exib}  –  CPF: {r['cpfs'][i]}")
        print(f"  Check-In  : {r['checkin']}")
        print(f"  Noites    : {r['noites']}")
        print(f"  Diárias   : R$ {r['valor_diarias']:.2f}")
        print(f"  Restaur.  : R$ {r['gastos_restaurante']:.2f}")
        print(f"  Parcial   : R$ {r['valor_diarias'] + r['gastos_restaurante']:.2f}")
    linha("═")
    pausar()

# ── MUDAR DE QUARTO ───────────────────────────
def mudar_quarto():
    cabecalho("MUDAR HÓSPEDE DE QUARTO")
    cod = input("  Código de reserva: ").strip()
    r = reservas.get(cod)
    if not r:
        print("  ❌  Reserva não encontrada.")
        pausar()
        return
    if not r["ativa"]:
        print("  ⚠️  Esta reserva já foi encerrada.")
        pausar()
        return

    print(f"\n  Reserva {cod} – Quarto atual: {r['quarto']} ({r['suite_nome']})")
    print("\n  Novo tipo de suíte:")
    for k, v in SUITES.items():
        print(f"    {k} – {v['nome']:10s}  R$ {v['diaria']:.2f}/noite  +R$ {v['extra_pessoa']:.2f}/pessoa")

    suite_op = input("\n  Opção (Enter para manter o mesmo tipo): ").strip()
    if suite_op == "":
        novo_suite_id = r["suite_id"]
    else:
        try:
            novo_suite_id = int(suite_op)
            if novo_suite_id not in SUITES:
                raise ValueError
        except ValueError:
            print("  ⚠️  Opção inválida.")
            pausar()
            return

    nova_suite = SUITES[novo_suite_id]

    novo_quarto = buscar_quarto_disponivel(reservas, novo_suite_id, nova_suite["andar"], cod_excluir=cod)

    if novo_quarto is None:
        print("  ❌  Não há quartos disponíveis nesse tipo de suíte.")
        pausar()
        return

    qtd = r["qtd_pessoas"]
    noites = r["noites"]
    novo_valor = calcular_valor_diaria(nova_suite, qtd, noites)
    andar = nova_suite["andar"]

    print(f"\n  Quarto atual  : {r['quarto']} ({r['suite_nome']})")
    print(f"  Novo quarto   : {novo_quarto} ({nova_suite['nome']} – {andar}º andar)")
    print(f"  Valor antigo  : R$ {r['valor_diarias']:.2f}")
    print(f"  Novo valor    : R$ {novo_valor:.2f}")

    conf = input("\n  Confirmar mudança? (s/n): ").strip().lower()
    if conf == "s":
        reservas[cod]["quarto"]     = novo_quarto
        reservas[cod]["suite_id"]   = novo_suite_id
        reservas[cod]["suite_nome"] = nova_suite["nome"]
        reservas[cod]["valor_diarias"] = novo_valor
        salvar_reservas()
        print(f"  ✅  Hóspede movido para o quarto {novo_quarto}.")
    else:
        print("  ↩️  Operação cancelada.")
    pausar()

# ── CARDÁPIO ──────────────────────────────────
def menu_cardapio():
    while True:
        limpar()
        cabecalho("GERENCIAR CARDÁPIO")
        print("  1 – Listar cardápio")
        print("  2 – Adicionar item")
        print("  3 – Remover item")
        print("  0 – Voltar")
        linha()
        op = input("  Opção: ").strip()
        if op == "1":
            listar_cardapio()
        elif op == "2":
            adicionar_item_cardapio()
        elif op == "3":
            remover_item_cardapio()
        elif op == "0":
            break

def adicionar_item_cardapio():
    cabecalho("ADICIONAR ITEM AO CARDÁPIO")
    categorias = list(CARDAPIO.keys())
    for i, cat in enumerate(categorias, 1):
        print(f"  {i} – {cat}")
    linha()
    op = input("  Categoria: ").strip()
    try:
        cat = categorias[int(op) - 1]
    except (ValueError, IndexError):
        print("  ⚠️  Opção inválida.")
        pausar()
        return

    nome_item = input("  Nome do item: ").strip()
    if nome_item == "":
        print("  ⚠️  Nome não pode ser vazio.")
        pausar()
        return
    try:
        preco = float(input("  Preço (R$): ").strip())
        if preco <= 0:
            raise ValueError
    except ValueError:
        print("  ⚠️  Preço inválido.")
        pausar()
        return

    CARDAPIO[cat].append((nome_item, preco))
    salvar_cardapio()
    print(f"  ✅  '{nome_item}' adicionado a {cat}.")
    pausar()

def remover_item_cardapio():
    cabecalho("REMOVER ITEM DO CARDÁPIO")
    categorias = list(CARDAPIO.keys())
    for i, cat in enumerate(categorias, 1):
        print(f"  {i} – {cat}")
    linha()
    op = input("  Categoria: ").strip()
    try:
        cat = categorias[int(op) - 1]
    except (ValueError, IndexError):
        print("  ⚠️  Opção inválida.")
        pausar()
        return

    itens = CARDAPIO[cat]
    if not itens:
        print("  ⚠️  Nenhum item nessa categoria.")
        pausar()
        return

    cabecalho(f"REMOVER – {cat}")
    for i, (nome_item, preco) in enumerate(itens, 1):
        print(f"  {i} – {nome_item:<30} R$ {preco:.2f}")
    linha()
    op2 = input("  Número do item a remover: ").strip()
    try:
        idx = int(op2) - 1
        if idx < 0 or idx >= len(itens):
            raise ValueError
    except ValueError:
        print("  ⚠️  Opção inválida.")
        pausar()
        return

    nome_removido = itens[idx][0]
    CARDAPIO[cat].pop(idx)
    salvar_cardapio()
    print(f"  ✅  '{nome_removido}' removido do cardápio.")
    pausar()

# ── GERENCIAR USUÁRIOS (ADMIN) ────────────────
def menu_usuarios(usuario_atual):
    while True:
        limpar()
        cabecalho("GERENCIAR USUÁRIOS  [ADMIN]")
        print("  1 – Listar usuários")
        print("  2 – Excluir usuário")
        print("  0 – Voltar")
        linha()
        op = input("  Opção: ").strip()
        if op == "1":
            listar_usuarios()
        elif op == "2":
            excluir_usuario(usuario_atual)
        elif op == "0":
            break

def listar_usuarios():
    cabecalho("LISTA DE USUÁRIOS")
    linha("─")
    print(f"  {'Nome':<20} {'Área':<16} {'E-mail':<30} Admin")
    linha("─")
    for nome, u in usuarios.items():
        admin_str = "✅" if u.get("is_admin") else "  "
        print(f"  {nome:<20} {u['area']:<16} {u['email']:<30} {admin_str}")
    linha("═")
    pausar()

def excluir_usuario(usuario_atual):
    cabecalho("EXCLUIR USUÁRIO")
    listar_nomes = [n for n in usuarios.keys() if n != usuario_atual["nome"]]
    if not listar_nomes:
        print("  Não há outros usuários para excluir.")
        pausar()
        return

    for i, nome in enumerate(listar_nomes, 1):
        u = usuarios[nome]
        admin_str = " [ADMIN]" if u.get("is_admin") else ""
        print(f"  {i} – {nome}  ({u['area']}){admin_str}")
    linha()
    op = input("  Número do usuário a excluir (0 para cancelar): ").strip()
    if op == "0":
        return
    try:
        idx = int(op) - 1
        if idx < 0 or idx >= len(listar_nomes):
            raise ValueError
    except ValueError:
        print("  ⚠️  Opção inválida.")
        pausar()
        return

    nome_alvo = listar_nomes[idx]
    conf = input(f"  Confirmar exclusão de '{nome_alvo}'? (s/n): ").strip().lower()
    if conf == "s":
        del usuarios[nome_alvo]
        salvar_usuarios()
        print(f"  ✅  Usuário '{nome_alvo}' excluído.")
    else:
        print("  ↩️  Operação cancelada.")
    pausar()

# ── ESTATÍSTICAS ──────────────────────────────
def menu_estatisticas():
    while True:
        limpar()
        cabecalho("ESTATÍSTICAS")
        print("  1 – Mensal  (últimos 30 dias)")
        print("  2 – Anual   (último ano)")
        print("  0 – Voltar")
        linha()
        op = input("  Opção: ").strip()
        if op == "1":
            mostrar_estatisticas(dias=30, titulo="MENSAL – Últimos 30 dias")
        elif op == "2":
            mostrar_estatisticas(dias=365, titulo="ANUAL – Último ano")
        elif op == "0":
            break

# Gera uma barra de progresso ASCII proporcional à porcentagem
def barra(pct, largura=30):
    filled = int(pct / 100 * largura)
    return "█" * filled + "░" * (largura - filled)

# ── ESTATÍSTICAS ──────────────────────────────
def menu_estatisticas():
    while True:
        limpar()
        cabecalho("ESTATÍSTICAS")
        print("  1 – Mensal  (últimos 30 dias)")
        print("  2 – Anual   (último ano)")
        print("  0 – Voltar")
        linha()
        op = input("  Opção: ").strip()
        if op == "1":
            mostrar_estatisticas(dias=30, titulo="MENSAL – Últimos 30 dias")
        elif op == "2":
            mostrar_estatisticas(dias=365, titulo="ANUAL – Último ano")
        elif op == "0":
            break

# Calcula e exibe as estatísticas financeiras do período informado
def mostrar_estatisticas(dias, titulo):
    cabecalho(f"ESTATÍSTICAS {titulo}")
    limite = data_hoje() - timedelta(days=dias)

    total_diarias, total_restaurante = calcular_totais(reservas, limite)
    total = total_diarias + total_restaurante

    if total == 0:
        print("  Sem movimentação financeira no período.")
        pausar()
        return

    pct_d = total_diarias / total * 100
    pct_r = total_restaurante / total * 100

    linha()
    print(f"  {'Categoria':<18} {'Valor':>12}   {'%':>6}   Barra")
    linha("─")
    print(f"  {'Diárias':<18} R$ {total_diarias:>9.2f}   {pct_d:>5.1f}%  {barra(pct_d)}")
    print(f"  {'Restaurante':<18} R$ {total_restaurante:>9.2f}   {pct_r:>5.1f}%  {barra(pct_r)}")
    linha("─")
    print(f"  {'TOTAL':<18} R$ {total:>9.2f}")
    linha("═")
    pausar()

# Recebe o dicionário de reservas e um limite de data,
# retorna uma tupla (total_diarias, total_restaurante)
# Só contabiliza reservas que já tiveram checkout realizado
def calcular_totais(dict_reservas, limite):
    total_diarias = 0.0
    total_restaurante = 0.0
    for r in dict_reservas.values():
        if r.get("ativa") or not r.get("checkout_dt"):
            continue
        try:
            dt = datetime.fromisoformat(r["checkout_dt"])
        except (ValueError, TypeError):
            continue
        if dt >= limite:
            total_diarias += r.get("valor_diarias", 0.0)
            total_restaurante += r.get("gastos_restaurante", 0.0)
    return total_diarias, total_restaurante

# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
def main():
    carregar_dados()

    # Se não houver nenhum admin, força o setup inicial
    if not tem_admin(usuarios):
        setup_inicial()

    while True:
        usuario = tela_inicial()
        if usuario["area"] == "administracao":
            menu_administracao(usuario)
        else:
            menu_restaurante(usuario)

if __name__ == "__main__":
    main()