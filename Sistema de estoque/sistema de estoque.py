import json
import os

class Empresa:
    empresas = []

    def __init__(self, razao_social, nome_fantasia, cnpj, data_cadastro, email, telefone, celular, contato, endereco):
        if any(emp.cnpj == cnpj for emp in Empresa.empresas):
            raise ValueError("Empresa com esse CNPJ já cadastrada!")
        
        self.razao_social = razao_social
        self.nome_fantasia = nome_fantasia
        self.cnpj = cnpj
        self.data_cadastro = data_cadastro
        self.email = email
        self.telefone = telefone
        self.celular = celular
        self.contato = contato
        self.endereco = endereco
        Empresa.empresas.append(self)

class Cliente:
    clientes = []

    def __init__(self, nome, cpf, data_nascimento, data_cadastro, email, telefone, celular, endereco):
        if any(cli.cpf == cpf for cli in Cliente.clientes):
            raise ValueError("Cliente com esse CPF já cadastrado!")
        
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.data_cadastro = data_cadastro
        self.email = email
        self.telefone = telefone
        self.celular = celular
        self.endereco = endereco
        Cliente.clientes.append(self)

class Produto:
    produtos = []

    def __init__(self, descricao, codigo, valor, valor_promocional, data_inicio_promocao, data_fim_promocao, data_cadastro, status, estoque):
        if any(prod.codigo == codigo for prod in Produto.produtos):
            raise ValueError("Produto com esse código já cadastrado!")
        
        self.descricao = descricao
        self.codigo = codigo
        self.valor = valor
        self.valor_promocional = valor_promocional if valor_promocional else valor
        self.data_inicio_promocao = data_inicio_promocao
        self.data_fim_promocao = data_fim_promocao
        self.data_cadastro = data_cadastro
        self.status = status
        self.estoque = estoque
        Produto.produtos.append(self)

class Venda:
    vendas = []

    def __init__(self, empresa, cliente, data_venda, produtos_quantidades, desconto, valor_pago):
        self.empresa = empresa
        self.cliente = cliente
        self.data_venda = data_venda
        self.produtos_quantidades = produtos_quantidades
        self.desconto = desconto
        self.valor_pago = valor_pago

        self.total_sem_desconto = sum((prod.valor_promocional or prod.valor) * qtd for prod, qtd in produtos_quantidades.items())
        self.total_com_desconto = self.total_sem_desconto * (1 - desconto / 100)
        self.troco = valor_pago - self.total_com_desconto

    def baixar_estoque(self):
        """Deduz os produtos do estoque ao confirmar a venda."""
        for produto, qtd in self.produtos_quantidades.items():
            produto.estoque -= qtd

    def gerar_json(self):
        """Gera os dados da venda em formato JSON."""
        venda_json = {
            "empresa": self.empresa.nome_fantasia,
            "cliente": self.cliente.nome,
            "data_venda": self.data_venda,
            "produtos": [
                {
                    "descricao": prod.descricao,
                    "codigo": prod.codigo,
                    "quantidade": qtd,
                    "valor_unitario": prod.valor,
                    "valor_promocional": prod.valor_promocional or prod.valor
                }
                for prod, qtd in self.produtos_quantidades.items()
            ],
            "total_sem_desconto": self.total_sem_desconto,
            "total_com_desconto": self.total_com_desconto,
            "valor_pago": self.valor_pago,
            "troco": self.troco
        }
        return json.dumps(venda_json, indent=4)

    def salvar_json(self):
        """Salva os dados da venda em um arquivo JSON na pasta 'vendas'."""
        if not os.path.exists("vendas"):
            os.makedirs("vendas")

        nome_arquivo = f"vendas/venda_{self.cliente.nome.replace(' ', '_')}_{self.data_venda.replace('/', '-')}.json"
        with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(self.gerar_json())

        print(f"\n Venda registrada com sucesso! Arquivo salvo em: {nome_arquivo}")

def cadastrar_empresa():
    print("\n Cadastro de Empresa")
    razao_social = input("Razão Social: ")
    nome_fantasia = input("Nome Fantasia: ")
    cnpj = input("CNPJ: ")
    data_cadastro = input("Data de Cadastro (DD/MM/AAAA): ")
    email = input("E-mail: ")
    telefone = input("Telefone: ")
    celular = input("Celular: ")
    contato = input("Nome do Contato: ")
    endereco = input("Endereço: ")

    try:
        Empresa(razao_social, nome_fantasia, cnpj, data_cadastro, email, telefone, celular, contato, endereco)
        print("Empresa cadastrada com sucesso!")
    except ValueError as e:
        print(e)

def cadastrar_cliente():
    print("\n Cadastro de Cliente")
    nome = input("Nome: ")
    cpf = input("CPF: ")
    data_nascimento = input("Data de Nascimento (DD/MM/AAAA): ")
    data_cadastro = input("Data de Cadastro (DD/MM/AAAA): ")
    email = input("E-mail: ")
    telefone = input("Telefone: ")
    celular = input("Celular: ")
    endereco = input("Endereço: ")

    try:
        Cliente(nome, cpf, data_nascimento, data_cadastro, email, telefone, celular, endereco)
        print("Cliente cadastrado com sucesso!")
    except ValueError as e:
        print(e)

def cadastrar_produto():
    print("\n Cadastro de Produto")
    descricao = input("Descrição: ")
    codigo = input("Código do Produto: ")
    valor = float(input("Valor: "))
    valor_promocional = input("Valor Promocional (Deixe em branco se não houver): ")
    valor_promocional = float(valor_promocional) if valor_promocional else None
    data_inicio_promocao = input("Data Início Promoção (DD/MM/AAAA) ou deixe em branco: ")
    data_fim_promocao = input("Data Fim Promoção (DD/MM/AAAA) ou deixe em branco: ")
    data_cadastro = input("Data de Cadastro (DD/MM/AAAA): ")
    status = input("Status do Produto (Ativo/Inativo): ")
    estoque = int(input("Quantidade em Estoque: "))

    try:
        Produto(descricao, codigo, valor, valor_promocional, data_inicio_promocao, data_fim_promocao, data_cadastro, status, estoque)
        print("Produto cadastrado com sucesso!")
    except ValueError as e:
        print(e)


def cadastrar_venda():
    print("\nCadastro de Venda")

    if not Empresa.empresas:
        print("Nenhuma empresa cadastrada!")
        return
    if not Cliente.clientes:
        print("Nenhum cliente cadastrado!")
        return
    if not Produto.produtos:
        print("Nenhum produto cadastrado!")
        return

    empresa = Empresa.empresas[0]

# Exibir lista de clientes cadastrados

    print("\nSelecione o Cliente:")
    for i, cli in enumerate(Cliente.clientes, 1):
        print(f"{i} - {cli.nome} - CPF: {cli.cpf}")

    index_cliente = int(input("Escolha um cliente: ")) - 1
    cliente = Cliente.clientes[index_cliente]

    data_venda = input("Data da Venda (DD/MM/AAAA): ")
    produtos_quantidades = {}

    while True:
        print("\nSelecione os Produtos:")
        for i, prod in enumerate(Produto.produtos, 1):
            preco = prod.valor_promocional if prod.valor_promocional else prod.valor
            print(f"{i} - {prod.descricao} - R${preco:.2f} ({'Promoção' if prod.valor_promocional else 'Normal'})")

        index_produto = int(input("Escolha um produto: ")) - 1
        produto = Produto.produtos[index_produto]
        quantidade = int(input(f"Quantidade de {produto.descricao}: "))

        if quantidade > produto.estoque:
            print(f"Estoque insuficiente! Disponível: {produto.estoque}")
            continue

        produtos_quantidades[produto] = quantidade
        continuar = input("Adicionar mais produtos? (s/n): ").lower()
        if continuar != "s":
            break

    desconto_input = input("Desconto (%) (se não houver, apenas pressione Enter): ")
    desconto = float(desconto_input) if desconto_input.strip() else 0

    valor_pago = float(input("Valor Pago: "))

    try:
        venda = Venda(empresa, cliente, data_venda, produtos_quantidades, desconto, valor_pago)
        print(f"\nTotal com Desconto: R${venda.total_com_desconto:.2f}")
        print(f"Troco: R${venda.troco:.2f}")

        confirmar = input("\nConfirmar pagamento? (s/n): ").lower()
        if confirmar == "s":
            venda.baixar_estoque()
            json_venda = venda.gerar_json()
            venda.salvar_json()
            print("\nPagamento efetuado com sucesso! Estoque atualizado.")
        else:
            print("\nVenda cancelada. Nenhuma alteração foi feita.")

    except ValueError as e:
        print(e)

#Consultar estoque
def exibir_estoque():
    if not Produto.produtos:
        print("\nNenhum produto cadastrado no estoque.")
        return

    print("\nCONTROLE DE ESTOQUE")
    print("Nome do Produto | Valor | Data Cadastro | Quantidade Vendida | Quantidade em Estoque | Status")
    print("-" * 90)

    for prod in Produto.produtos:
        quantidade_vendida = sum(
            qtd for venda in Venda.vendas for produto, qtd in venda.produtos_quantidades.items() if produto == prod
        )
        print(f"{prod.descricao} | R${prod.valor:.2f} | {prod.data_cadastro} | {quantidade_vendida} | {prod.estoque} | {prod.status}")

    print("-" * 90)

def gerar_json(self):
    venda_json = {
    "empresa": self.empresa.nome_fantasia,
    "cliente": self.cliente.nome,
    "data_venda": self.data_venda,
    "produtos": [
        {
            "descricao": prod.descricao,
            "codigo": prod.codigo,
            "quantidade": qtd,
            "valor_unitario": prod.valor,
            "valor_promocional": prod.valor_promocional if prod.valor_promocional else prod.valor,
            "subtotal": (prod.valor_promocional if prod.valor_promocional else prod.valor) * qtd
            }
                for prod, qtd in self.produtos_quantidades.items()
            ],
            "total_sem_desconto": self.total_sem_desconto,
            "desconto_aplicado": self.desconto,
            "total_com_desconto": self.total_com_desconto,
            "valor_pago": self.valor_pago,
            "troco": self.troco
        }

# Salvar em um arquivo JSON
    with open("vendas.json", "w", encoding="utf-8") as arquivo:
        json.dump(venda_json, arquivo, indent=4, ensure_ascii=False)

    print("\n Arquivo 'vendas.json' gerado com sucesso!")

#Menu numérico
def menu():
    while True:
        print("\n MENU PRINCIPAL")
        print("1 - Cadastrar Empresa")
        print("2 - Cadastrar Cliente")
        print("3 - Cadastrar Produto")
        print("4 - Cadastrar Venda")
        print("5 - Exibir estoque")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            cadastrar_empresa()
        elif opcao == "2":
            cadastrar_cliente()
        elif opcao == "3":
            cadastrar_produto()
        elif opcao == "4":
            cadastrar_venda()
        elif opcao == "5":
            exibir_estoque()
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

menu()