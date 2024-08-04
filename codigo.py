import random
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from collections import Counter

class Joia:
    def __init__(self, idjoia, nome, material, preco, qtd, codigo_validacao):
        self.idjoia = idjoia
        self.nome = nome
        self.material = material
        self.preco = preco
        self.qtd = qtd
        self.codigo_validacao = codigo_validacao

class Autenticar(ABC):
    @abstractmethod
    def autenticar(self):
        pass
    
    @classmethod
    def criar_joia(cls, tipo, idjoia, nome, material, preco, qtd, codigo_validacao, extra_info):
        if tipo == 'colar':
            if not isinstance(extra_info, str):  # Tamanho deve ser uma string
                raise ValueError("Para um Colar, 'extra_info' deve ser uma string representando o tamanho")
            return Colar(idjoia, nome, material, preco, qtd, extra_info, codigo_validacao)
        elif tipo == 'brinco':
            if not isinstance(extra_info, str):  # Estilo deve ser uma string
                raise ValueError("Para um Brinco, 'extra_info' deve ser uma string representando o estilo")
            return Brinco(idjoia, nome, material, preco, qtd, extra_info, codigo_validacao)
        elif tipo == 'pulseira':
            if extra_info is not None:  # Pulseira não deve ter informações extras
                raise ValueError("Pulseira não deve ter informações extras")
            return Pulseira(idjoia, nome, material, preco, qtd, codigo_validacao)
        else:
            raise ValueError("Tipo de joia inválido")
        
class Colar(Joia):
    def __init__(self, idjoia, nome, material, preco, qtd, tamanho, codigo_validacao):
        super().__init__(idjoia, nome, material, preco, qtd, codigo_validacao)
        self.tamanho = tamanho
    
    def autenticar(self):
        if isinstance(self, Colar):
            if self.codigo_validacao == "@riginal":
                return True, f'A peça {self.nome} é de material {self.material} legítimo.'
        return False, f'A peça {self.nome} não é de material {self.material} legítimo.'
    
class Brinco(Joia):
    def __init__(self, idjoia, nome, material, preco, qtd, estilo, codigo_validacao):
        super().__init__(idjoia, nome, material, preco, qtd, codigo_validacao)
        self.estilo = estilo
        
    def autenticar(self):
        if isinstance(self, Brinco):
            if self.codigo_validacao == "@riginal":
                return True, f'A peça {self.nome} é de material {self.material} legítimo.'
        return False, f'A peça {self.nome} não é de material {self.material} legítmo.'
    
    
class Pulseira(Joia):
    def __init__(self, idjoia, nome, material, preco, qtd, codigo_validacao):
        super().__init__(idjoia, nome, material, preco, qtd, codigo_validacao)
        
    def autenticar(self):
        if isinstance(self, Pulseira):
            if self.codigo_validacao == "@riginal":
                return True, f'A peça {self.nome} é de material {self.material} legítimo.'
        return False, f'A peça {self.nome} não é de material {self.material} legítimo.'

class Cliente:
    def __init__(self, nome, cpf, endereco, contato, pontos=0):
        self.nome = nome
        self.cpf = cpf
        self.endereco = endereco
        self.contato = contato
        self.pontos = pontos
        self.historico_compras = []
        
    def adicionar_compra(self, joia, quantidade, pagamento_recibo):
        
        if not self.historico_compras:
            self.pontos = 0
            
        self.historico_compras.append((joia, quantidade, pagamento_recibo))
        
        self.pontos += int((joia.preco * quantidade) // 10)

        
    def listar_historico_compras(self):
        print(f"\nHistórico de Compras para {self.nome}:")
        for compra in self.historico_compras:
            joia, quantidade, recibo = compra
            print(f"Joia: {joia.nome}, Material: {joia.material}, Preço: R${joia.preco}, Quantidade: {quantidade}")
            print(f"Recibo: {recibo}")
            
class GestaoClientes:
    
    def __init__(self):
        self.clientes = [] #armazenar clientes cadastrados
        self.dicionario_vendas = {} # rastrear as vendas por clientes
        
    def cadastrar_cliente(self, nome, cpf, endereco, contato):
        # Verifica se o CPF já está cadastrado
        for cliente in self.clientes:
            if cliente.cpf == cpf:
                print(f"Cliente com CPF {cpf} já está cadastrado.")
                return
        
        # Se o CPF não estiver cadastrado, adiciona o novo cliente
        novo_cliente = Cliente(nome, cpf, endereco, contato)
        self.clientes.append(novo_cliente)
        self.dicionario_vendas[cpf] = [] # Inicializa a lista de compras para o novo cliente
        print(f"Cliente {nome} cadastrado com sucesso.")

        
    def editar_cliente(self, cpf, nome=None, endereco=None, contato=None, pontos=None):
        for cliente in self.clientes:
            if cliente.cpf == cpf:
                cliente.nome = nome if nome is not None else cliente.nome
                cliente.endereco = endereco if endereco is not None else cliente.endereco
                cliente.contato = contato if contato is not None else cliente.contato
                cliente.pontos = pontos if pontos is not None else cliente.pontos
                print(f"Cliente {cliente.nome} atualizado com sucesso.")
                return
        print(f"Cliente com CPF {cpf} não encontrado.")
        
    def buscar_cliente(self, cpf):
        for cliente in self.clientes:
            if cliente.cpf == cpf:
                print(f"Cliente {cliente.nome} encontrado e cadastrado no sistema")
                return cliente
        print(f"Cliente não encontrado no sistema.")
        return None
        
    def listar_clientes(self):
        if self.clientes:
            print("----Clientes Cadastrados:----")
            for cliente in self.clientes:
                print(f"Nome: {cliente.nome},\n CPF: {cliente.cpf},\n Endereço: {cliente.endereco},\n Contato: {cliente.contato},\n Pontos: {cliente.pontos}")  
        else:
            print("Nenhum Cliente cadastrado. ")

              
    def adicionar_compra_cliente(self, cpf, joia, quantidade, estoque, gestao_vendas):
        cliente = self.buscar_cliente(cpf)
        if cliente is None:
            return

        if quantidade > joia.qtd:
            print(f"Quantidade indisponível. Apenas {joia.qtd} unidades disponíveis.")
            return

        valor_total = joia.preco * quantidade
        tipo_pagamento = input("Informe o tipo de pagamento (credito, debito, especie): ")
        numero_cartao = validade = cvv = None
        if tipo_pagamento in ['credito', 'debito']:
            numero_cartao = input("Número do cartão: ")
            validade = input("Validade do cartão (MM/AA): ")
            cvv = input("CVV do cartão: ")

        sistema_pagamento = SistemaPagamento(estoque)  # Passe o estoque aqui
        recibo = sistema_pagamento.realizar_pagamento(cliente, tipo_pagamento, valor_total, numero_cartao, validade, cvv)
        if recibo:
            cliente.adicionar_compra(joia, quantidade, recibo)
            joia.qtd -= quantidade
            self.dicionario_vendas[cpf].append((joia, quantidade))
            gestao_vendas.adicionar_venda(joia, quantidade, joia.preco)
            print(f"Compra da joia {joia.nome} adicionada ao histórico do cliente {cliente.nome}.")
        else:
            print("Compra não registrada devido a falha no pagamento.")

                
            
    def historico_compras_cliente(self, cpf):
        for cliente in self.clientes:
            if cliente.cpf == cpf:
                cliente.listar_historico_compras()
                return
        print(f"Cliente com CPF {cpf} não encontrado.")
    
    def consultar_cliente(self, cpf):
        for cliente in self.clientes:
            if cliente.cpf == cpf:
                print(f"Histórico de Compras do Cliente {cliente.nome}:")
                if not cliente.historico_compras:
                    print("Nenhuma compra registrada.")
                else:
                    for joia, quantidade in cliente.historico_compras:
                        print(f"Joia: {joia.nome}, Preço: R${joia.preco:.2f}, Quantidade: {joia.quantidade}, Pontos: {joia.pontos}")
                return
        print(f"Cliente com CPF {cpf} não encontrado.")
    
class Estoque:
    
    def __init__(self):
        self.produto = []
        self.clientes = []
        
    def adicionar_joia(self,joia):
        if joia.codigo_validacao == "@riginal":
            self.produto.append(joia)
            print(f"Joia {joia.nome} adicionada ao estoque.")
        else:
            print(f"Joia {joia.nome} não pode ser adicionada ao estoque")
        
    def buscar_joia(self, nome, idjoia):
        for joia in self.produto:
            if joia.nome == nome and joia.idjoia == idjoia:
                print(f"Joia {joia.nome} disponível no estoque.")
                return joia
        
        # Mensagem e retorno após o loop, se nenhum item for encontrado
        print(f"Joia {joia.nome} indisponível no estoque.")
        return None

        
    def editar_joia(self, indice, nome, idjoia, material, preco, quantidade, tamanho=None, estilo=None, codigo_validacao=None):
        if 0 <= indice < len(self.produto):
            joia = self.produto[indice]
            joia.nome = nome
            joia.idjoia = idjoia
            joia.material = material
            joia.preco = preco
            joia.quantidade = quantidade
            joia.codigo_validacao = codigo_validacao


            if isinstance(joia, Colar):
                if tamanho is not None:
                    joia.tamanho = tamanho
                    
            elif isinstance(joia, Brinco):
                if estilo is not None:
                    joia.estilo = estilo

            print(f"Joia {joia.nome} atualizada no estoque.")
        else:
            print("Índice inválido.")
            
            
    def remover_joia(self, indice, ):
        if 0 <= indice < len(self.produto):
            joia = self.produto.pop(indice)
            print(f"Joia {joia.nome} removida do estoque: ")
        else:
            print("Índice inválido.")
        
    def listar_joias(self):
        if self.produto:
            print("--- Joias Disponíveis no estoque: ---")
            for i, joia in enumerate(self.produto):
            # Exibe o nome da joia, o ID atualizado e o material/preço
                print(f"{i}: {joia.nome}, ID: {joia.idjoia}, ({joia.material}, R${joia.preco:.2f}), Quantidade: {joia.qtd}")
        else:
            print("Joias Indisponíveis.")
    
    def verificar_estoque(self):
        total_joias = sum(joia.qtd for joia in self.produto)
        print(f"Total de joias no estoque: {total_joias}")

    
class Pagamento(ABC):
    @abstractmethod
    def pagar(self, valor):
        pass

    @abstractmethod
    def emitir_recibo(self):
        pass

class CartaoCredito(Pagamento):
    def __init__(self, numero_cartao, validade, cvv):
        self.numero_cartao = numero_cartao
        self.validade = validade
        self.cvv = cvv

    def pagar(self, valor):
        # Simulando processamento de pagamento com cartão de crédito
        print(f"Pagamento de R${valor:.2f} realizado com cartão de crédito {self.numero_cartao}.")
        return True

    def emitir_recibo(self):
        return f"Recibo: Pagamento com Cartão de Crédito - Número: {self.numero_cartao} - Data: {datetime.now()}"

class CartaoDebito(Pagamento):
    def __init__(self, numero_cartao, validade, cvv):
        self.numero_cartao = numero_cartao
        self.validade = validade
        self.cvv = cvv

    def pagar(self, valor):
        # Simulando processamento de pagamento com cartão de débito
        print(f"Pagamento de R${valor:.2f} realizado com cartão de débito {self.numero_cartao}.")
        return True

    def emitir_recibo(self):
        return f"Recibo: Pagamento com Cartão de Débito - Número: {self.numero_cartao} - Data: {datetime.now()}"

class Especie(Pagamento):
    def __init__(self):
        pass

    def pagar(self, valor):
        # Simulando processamento de pagamento em espécie
        print(f"Pagamento de R${valor:.2f} realizado em espécie.")
        return True

    def emitir_recibo(self):
        return f"Recibo: Pagamento em Espécie - Data: {datetime.now()}"

class SistemaPagamento:
    def __init__(self, estoque):
        self.pagamentos = []
        self.estoque = estoque

    def realizar_pagamento(self, cliente, tipo_pagamento, valor, numero_cartao=None, validade=None, cvv=None):
        tipos_pagamento = {
            'credito': CartaoCredito,
            'debito': CartaoDebito,
            'especie': Especie
        }
        
        if tipo_pagamento not in tipos_pagamento:
            raise ValueError("Tipo de pagamento não suportado.")
        
        if tipo_pagamento in ['credito', 'debito']:
            if None in (numero_cartao, validade, cvv):
                raise ValueError("Todos os dados do cartão são necessários.")
            pagamento = tipos_pagamento[tipo_pagamento](numero_cartao, validade, cvv)
        else:
            pagamento = tipos_pagamento[tipo_pagamento]()
        
        if pagamento.pagar(valor):
            recibo = pagamento.emitir_recibo()
            self.pagamentos.append(recibo)
            print("Pagamento realizado com sucesso.")
            self.verificar_pontos_cliente(cliente)
            return recibo
        else:
            print("Falha no pagamento.")
            return None

    def verificar_pontos_cliente(self, cliente):
        if cliente.pontos > 500:
            if self.estoque.produto:
                joia_ganha = random.choice(self.estoque.produto)
                print(f"O cliente {cliente.nome} ganhou um(a) {joia_ganha.nome} por ter mais de 500 pontos!")
                self.estoque.remover_joia(self.estoque.produto.index(joia_ganha))
            else:
                print(f"O cliente {cliente.nome} tem mais de 500 pontos, mas não há joias disponíveis no estoque.")


class GestaoVendas:
    def __init__(self):
        self.vendas = []
        
    def adicionar_venda(self, joia, quantidade, preco):
        venda = {
            "joia": joia,
            "quantidade": quantidade,
            "preco": preco,
            "data_venda": datetime.now()
        }
        self.vendas.append(venda)
        print(f"Venda registrada: {venda['joia'].nome}, Quantidade: {venda['quantidade']}, Preço: R${venda['preco']:.2f}, Data: {venda['data_venda']}")


    def gerar_relatorio_vendas(self, inicio, fim):
        relatorio = [venda for venda in self.vendas if inicio <= venda["data_venda"] <= fim]
        if not relatorio:
            print("Nenhuma venda registrada no período especificado.")
        else:
            for venda in relatorio:
                print(f"Venda: {venda['joia'].nome}, Quantidade: {venda['quantidade']}, Data: {venda['data_venda']}")
    def joias_mais_vendidas(self):
        contagem_joias = Counter()
        for venda in self.vendas:
            contagem_joias[venda["joia"].nome] += venda["quantidade"]
        mais_vendidas = contagem_joias.most_common()
        if not mais_vendidas:
            print("Nenhuma joia foi vendida ainda.")
        else:
            print("Joias mais vendidas:")
            for joia, quantidade in mais_vendidas:
                print(f"{joia}: {quantidade} unidade(s)")

    def calcular_lucro_total(self, inicio, fim):
        lucro_total = sum(venda["quantidade"] * venda["preco"] for venda in self.vendas if inicio <= venda["data_venda"] <= fim)
        print(f"Lucro total no período de {inicio} a {fim}: R${lucro_total:.2f}")

       
def pausa_para_continuar():
    input("\nPressione Enter para continuar...")
          
def menu():
    estoque = Estoque()
    gestao_clientes = GestaoClientes()
    gestao_vendas = GestaoVendas()
    
    while True:
        print("\n----- Sistema Encanto e Glamour -----")
        print("Bem-vindo(a):")
        print("1. Cadastrar Colar")
        print("2. Cadastrar Brinco")
        print("3. Cadastrar Pulseira")
        print("4. Listar Joias")
        print("5. Cadastrar Cliente")
        print("6. Editar Cliente")
        print("7. Adicionar Compra ao Cliente")
        print("8. Consultar Histórico de Compras do Cliente")
        print("9. Listar Clientes")
        print("10. Gestão de Vendas")
        print("11. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            idjoia = input("ID da joia: ")
            nome = input("Nome: ")
            material = input("Material: ")
            preco = float(input("Preço: "))
            qtd = int(input("Quantidade: "))
            tamanho = input("Tamanho: ")
            codigo_validacao = input("Código de validação: ")
            try:
                colar = Autenticar.criar_joia('colar', idjoia, nome, material, preco, qtd, codigo_validacao, tamanho)
                estoque.adicionar_joia(colar)
                print(f"Colar {nome} cadastrado com sucesso!")
            except ValueError as e:
                print(f"Erro ao cadastrar colar: {e}")
            pausa_para_continuar()

        elif opcao == '2':
            idjoia = input("ID da joia: ")
            nome = input("Nome: ")
            material = input("Material: ")
            preco = float(input("Preço: "))
            qtd = int(input("Quantidade: "))
            estilo = input("Estilo: ")
            codigo_validacao = input("Código de validação: ")
            try:
                brinco = Autenticar.criar_joia('brinco', idjoia, nome, material, preco, qtd, codigo_validacao, estilo)
                estoque.adicionar_joia(brinco)
                print(f"Brinco {nome} cadastrado com sucesso!")
            except ValueError as e:
                print(f"Erro ao cadastrar brinco: {e}")
            pausa_para_continuar()

        elif opcao == '3':
            idjoia = input("ID da joia: ")
            nome = input("Nome: ")
            material = input("Material: ")
            preco = float(input("Preço: "))
            qtd = int(input("Quantidade: "))
            codigo_validacao = input("Código de validação: ")
            try:
                pulseira = Autenticar.criar_joia('pulseira', idjoia, nome, material, preco, qtd, codigo_validacao, None)
                estoque.adicionar_joia(pulseira)
                print(f"Pulseira {nome} cadastrada com sucesso!")
            except ValueError as e:
                print(f"Erro ao cadastrar pulseira: {e}")
            pausa_para_continuar()


        elif opcao == '4':
            estoque.listar_joias()
            pausa_para_continuar()

        elif opcao == '5':
            nome = input("Nome do cliente: ")
            cpf = input("CPF do cliente: ")
            endereco = input("Endereço do cliente: ")
            contato = input("Contato do cliente: ")
            gestao_clientes.cadastrar_cliente(nome, cpf, endereco, contato)
            pausa_para_continuar()

        elif opcao == '6':
            cpf = input("CPF do cliente a ser editado: ")
            nome = input("Novo nome (ou pressione Enter para manter o atual): ") or None
            endereco = input("Novo endereço (ou pressione Enter para manter o atual): ") or None
            contato = input("Novo contato (ou pressione Enter para manter o atual): ") or None
            pontos = input("Novos pontos (ou pressione Enter para manter o atual): ")
            pontos = int(pontos) if pontos else None
            gestao_clientes.editar_cliente(cpf, nome, endereco, contato, pontos)
            pausa_para_continuar()

        elif opcao == '7':
            cpf = input("CPF do cliente: ")
            cliente = gestao_clientes.buscar_cliente(cpf)
            if cliente:
                idjoia = input("ID da joia: ")
                quantidade = int(input("Quantidade: "))
                joia = next((j for j in estoque.produto if j.idjoia == idjoia), None)
                if joia:
                    gestao_clientes.adicionar_compra_cliente(cpf, joia, quantidade, estoque, gestao_vendas)
                    gestao_vendas.vendas.append({"joia": joia, "quantidade": quantidade, "data_venda": datetime.now()})
                else:
                    print("Joia não encontrada no estoque.")
            pausa_para_continuar()

        elif opcao == '8':
            cpf = input("CPF do cliente: ")
            gestao_clientes.historico_compras_cliente(cpf)
            pausa_para_continuar()

        elif opcao == '9':
            gestao_clientes.listar_clientes()
            pausa_para_continuar()

        elif opcao == '10':  # Novo menu de Gestão de Vendas
            while True:
                print("\n--- Gestão de Vendas ---")
                print("1. Ver Relatório de Vendas")
                print("2. Calcular Lucro em Intervalo de Tempo")
                print("3. Ver Lucro Total")
                print("4. Voltar ao Menu Principal")
                opcao_vendas = input("Escolha uma opção: ")

                if opcao_vendas == '1':
                    try:
                        inicio = datetime.strptime(input("Data de início (AAAA-MM-DD): "), "%Y-%m-%d")
                        fim = datetime.strptime(input("Data de fim (AAAA-MM-DD): "), "%Y-%m-%d") + timedelta(days=1)
                        gestao_vendas.gerar_relatorio_vendas(inicio, fim)
                    except ValueError:
                        print("Formato de data inválido.")
                    pausa_para_continuar()

                elif opcao_vendas == '2':
                    try:
                        inicio = datetime.strptime(input("Data de início (AAAA-MM-DD): "), "%Y-%m-%d")
                        fim = datetime.strptime(input("Data de fim (AAAA-MM-DD): "), "%Y-%m-%d") + timedelta(days=1)
                        gestao_vendas.calcular_lucro_total(inicio, fim)
                    except ValueError:
                        print("Formato de data inválido.")
                    pausa_para_continuar()

                elif opcao_vendas == '3':
                    try:
                        inicio = datetime.strptime(input("Data de início (AAAA-MM-DD): "), "%Y-%m-%d")
                        fim = datetime.strptime(input("Data de fim (AAAA-MM-DD): "), "%Y-%m-%d") + timedelta(days=1)
                        gestao_vendas.calcular_lucro_total(inicio, fim)
                    except ValueError:
                        print("Formato de data inválido.")
                    pausa_para_continuar()

                elif opcao_vendas == '4':
                    break

                else:
                    print("Opção inválida. Tente novamente.")
                    pausa_para_continuar()

        elif opcao == '11':
            break

        else:
            print("Opção inválida. Tente novamente.")

menu()