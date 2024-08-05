import random
import re
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from collections import Counter

import abc

class Joia:
    def __init__(self, idjoia, nome, material, preco, qtd, codigo_validacao):
        self._idjoia = idjoia
        self._nome = nome
        self._material = material
        self._preco = preco
        self._qtd = qtd
        self._codigo_validacao = codigo_validacao

    @property
    def idjoia(self):
        return self._idjoia

    @idjoia.setter
    def idjoia(self, value):
        self._idjoia = value

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, value):
        self._nome = value

    @property
    def material(self):
        return self._material

    @material.setter
    def material(self, value):
        self._material = value

    @property
    def preco(self):
        return self._preco

    @preco.setter
    def preco(self, value):
        self._preco = value

    @property
    def qtd(self):
        return self._qtd

    @qtd.setter
    def qtd(self, value):
        self._qtd = value

    @property
    def codigo_validacao(self):
        return self._codigo_validacao

    @codigo_validacao.setter
    def codigo_validacao(self, value):
        self._codigo_validacao = value

class Autenticar(abc.ABC):
    def autenticar(self):
        pass

class Colar(Joia):
    def __init__(self, idjoia, nome, material, preco, qtd, tamanho, codigo_validacao):
        super().__init__(idjoia, nome, material, preco, qtd, codigo_validacao)
        self._tamanho = tamanho

    
    @property
    def tamanho(self):
        return self._tamanho

    @tamanho.setter
    def tamanho(self, value):
        self._tamanho = value
    
    def autenticar(self):
        if self._codigo_validacao == "@riginal":
            return True, f'A peça {self._nome} é de material {self._material} legítimo.'
        return False, f'A peça {self._nome} não é de material {self._material} legítimo.'

class Brinco(Joia):
    def __init__(self, idjoia, nome, material, preco, qtd, estilo, codigo_validacao):
        super().__init__(idjoia, nome, material, preco, qtd, codigo_validacao)
        self._estilo = estilo

    
    @property
    def estilo(self):
        return self._estilo

    @estilo.setter
    def estilo(self, value):
        self._estilo = value
        
    def autenticar(self):
        if self._codigo_validacao == "@riginal":
            return True, f'A peça {self._nome} é de material {self._material} legítimo.'
        return False, f'A peça {self._nome} não é de material {self._material} legítimo.'

class Pulseira(Joia, Autenticar):
    def __init__(self, idjoia, nome, material, preco, qtd, codigo_validacao):
        super().__init__(idjoia, nome, material, preco, qtd, codigo_validacao)

    def autenticar(self):
        if self._codigo_validacao == "@riginal":
            return True, f'A peça {self._nome} é de material {self._material} legítimo.'
        return False, f'A peça {self._nome} não é de material {self._material} legítimo.'

class Cliente:
    def __init__(self, nome, cpf, endereco, contato, pontos=0):
        self._nome = nome
        self._cpf = cpf
        self._endereco = endereco
        self._contato = contato
        self._pontos = pontos
        self._historico_compras = []

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, value):
        self._nome = value

    @property
    def cpf(self):
        return self._cpf

    @cpf.setter
    def cpf(self, value):
        self._cpf = value

    @property
    def endereco(self):
        return self._endereco

    @endereco.setter
    def endereco(self, value):
        self._endereco = value

    @property
    def contato(self):
        return self._contato

    @contato.setter
    def contato(self, value):
        self._contato = value

    @property
    def pontos(self):
        return self._pontos

    @pontos.setter
    def pontos(self, value):
        self._pontos = value

    @property
    def historico_compras(self):
        return self._historico_compras

    def adicionar_compra(self, joia, quantidade, pagamento_recibo):
        if not self._historico_compras:
            self._pontos = 0
            
        self._historico_compras.append((joia, quantidade, pagamento_recibo))
        self._pontos += int((joia.preco * quantidade) // 10)

    def listar_historico_compras(self):
        print(f"\nHistórico de Compras para {self._nome}:")
        if not self._historico_compras:
            print("O cliente não possui histórico de compra por não ter feito nenhuma compra.")
        else:
            for compra in self._historico_compras:
                joia, quantidade, recibo = compra
                print(f"Joia: {joia.nome}, Material: {joia.material}, Preço: R${joia.preco:.2f}, Quantidade: {quantidade}")
                print(f"Recibo: {recibo}")

class GestaoClientes:
    
    def __init__(self):
        self._clientes = []  
        self._dicionario_vendas = {}  
        
    def cadastrar_cliente(self, nome, cpf, endereco, contato):
        for cliente in self._clientes:
            if cliente.cpf == cpf:
                print(f"Cliente com CPF {cpf} já está cadastrado.")
                return
        
        novo_cliente = Cliente(nome, cpf, endereco, contato)
        self._clientes.append(novo_cliente)
        self._dicionario_vendas[cpf] = [] 
        print(f"Cliente {nome} cadastrado com sucesso.")

    def editar_cliente(self, cpf, nome=None, endereco=None, contato=None, pontos=None):
        for cliente in self._clientes:
            if cliente.cpf == cpf:
                cliente.nome = nome if nome is not None else cliente.nome
                cliente.endereco = endereco if endereco is not None else cliente.endereco
                cliente.contato = contato if contato is not None else cliente.contato
                cliente.pontos = pontos if pontos is not None else cliente.pontos
                print(f"Cliente {cliente.nome} atualizado com sucesso.")
                return
        print(f"Cliente com CPF {cpf} não encontrado.")
        
        
    def buscar_cliente(self, cpf):
        for cliente in self._clientes:
            if cliente.cpf == cpf:
                print(f"Cliente {cliente.nome} encontrado e cadastrado no sistema")
                return cliente
            else:
                print(f"Cliente não encontrado no sistema.")
                return None
       
        
    def listar_clientes(self):
        if self._clientes:
            print("----Clientes Cadastrados:----")
            for cliente in self._clientes:
                print(f" Nome: {cliente.nome},\n CPF: {cliente.cpf},\n Endereço: {cliente.endereco},\n Contato: {cliente.contato},\n Pontos: {cliente.pontos}")  
        else:
            print("Nenhum Cliente cadastrado.")

    def adicionar_compra_cliente(self, cpf, joia, quantidade, estoque):
        cliente = self.buscar_cliente(cpf)
        if cliente is None:
            print(f"Cliente com CPF {cpf} não encontrado.")
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

        sistema_pagamento = SistemaPagamento(estoque)  
        pagamento_aceito = False
        while not pagamento_aceito:
            valor_pagamento = float(input(f"Valor a ser pago (Total: R${valor_total:.2f}): "))
            if valor_pagamento < valor_total:
                print("Valor insuficiente. Tente novamente.")
            else:
                troco = valor_pagamento - valor_total
                if troco > 0:
                    print(f"Pagamento aceito. Seu troco é R${troco:.2f}.")
                recibo = sistema_pagamento.realizar_pagamento(cliente, tipo_pagamento, valor_total, numero_cartao, validade, cvv)
                if recibo:
                    cliente.adicionar_compra(joia, quantidade, recibo)
                    joia.qtd -= quantidade
                    if cpf not in self._dicionario_vendas:
                        self._dicionario_vendas[cpf] = []
                    self._dicionario_vendas[cpf].append((joia, quantidade))
                    print(f"Compra da joia {joia.nome} adicionada ao histórico do cliente {cliente.nome}.")
                    pagamento_aceito = True
                else:
                    print("Compra não registrada devido a falha no pagamento.")

    def historico_compras_cliente(self, cpf):
        cliente = self.buscar_cliente(cpf)
        if cliente:
            cliente.listar_historico_compras()
        else:
            print(f"Cliente com CPF {cpf} não encontrado.")
    
    def consultar_cliente(self, cpf):
        cliente = self.buscar_cliente(cpf)
        if cliente:
            print(f"Histórico de Compras do Cliente {cliente.nome}:")
            if not cliente.historico_compras:
                print("Nenhuma compra registrada.")
            else:
                for joia, quantidade in cliente.historico_compras:
                    print(f"Joia: {joia.nome}, Preço: R${joia.preco:.2f}, Quantidade: {quantidade}, Pontos: {cliente.pontos}")
        else:
            print(f"Cliente com CPF {cpf} não encontrado.")

    
class Estoque:
    
    def __init__(self):
        self._produto = []
        self._clientes = []
        

    @property
    def produto(self):
        return self._produto

    @produto.setter
    def produto(self, value):
        self._produto = value

    @property
    def clientes(self):
        return self._clientes

    @clientes.setter
    def clientes(self, value):
        self._clientes = value

    def adicionar_joia(self, joia):
        if joia.codigo_validacao == "@riginal":
            self._produto.append(joia)
            print(f"Joia {joia.nome} adicionada ao estoque.")
        else:
            print(f"Joia {joia.nome} não pode ser adicionada ao estoque")
        
    def buscar_joia(self, indice, nome, idjoia):
        if 0 <= indice < len(self._produto):
            joia = self._produto[indice]
            if joia.nome == nome and joia.idjoia == idjoia:
                print(f"Joia {joia.nome} disponível no estoque.")
                return joia
            else:
                print(f"Joia com nome {nome} e ID {idjoia} não corresponde ao índice {indice}.")
                return None
        else:
            print(f"Índice {indice} fora dos limites do estoque.")
            return None

    def editar_joia(self, indice, nome=None, idjoia=None, material=None, preco=None, quantidade=None, tamanho=None, estilo=None, codigo_validacao=None):
        if 0 <= indice < len(self._produto):
            joia = self._produto[indice]

            joia.nome = nome if nome is not None else joia.nome
            joia.idjoia = idjoia if idjoia is not None else joia.idjoia
            joia.material = material if material is not None else joia.material
            joia.preco = preco if preco is not None else joia.preco
            joia.qtd = quantidade if quantidade is not None else joia.qtd

            if isinstance(joia, Colar):
                joia.tamanho = tamanho if tamanho is not None else joia.tamanho
                joia.codigo_validacao = codigo_validacao if codigo_validacao is not None else joia.codigo_validacao
                
            if isinstance(joia, Brinco):
                joia.tamanho = tamanho if tamanho is not None else joia.tamanho
                joia.estilo = estilo if estilo is not None else joia.estilo

            print(f"Joia {joia.nome} atualizada com sucesso!")
        else:
            print("Índice inválido.")

    def remover_joia(self, idjoia, quantidade):
        for joia in self._produto:
            if joia.idjoia == idjoia:
                if joia.qtd >= quantidade:
                    joia.qtd -= quantidade
                    if joia.qtd == 0:
                        self._produto.remove(joia)
                        print(f"Joia {joia.nome} removida do estoque.")
                    else:
                        print(f"{quantidade} unidades da joia {joia.nome} removidas do estoque. Restam {joia.qtd} unidades.")
                else:
                    print(f"Quantidade insuficiente em estoque. Restam apenas {joia.qtd} unidades.")
                return
        print("ID da joia não encontrado no estoque.")
        
    def listar_joias(self):
        if self._produto:
            print("--- Joias Disponíveis no estoque: ---")
            for i, joia in enumerate(self._produto):
                preco = joia.preco if joia.preco is not None else 0.00
                print(f"{i}: {joia.nome}, ID: {joia.idjoia}, ({joia.material}, R${preco:.2f}), Quantidade: {joia.qtd}")
        else:
            print("Joias Indisponíveis.")


class Pagamento(ABC):
    @abstractmethod
    def pagar(self, valor):
        pass

    @abstractmethod
    def emitir_recibo(self):
        pass

class CartaoCredito(Pagamento):
    def __init__(self, numero_cartao, validade, cvv):
        self._numero_cartao = numero_cartao
        self._validade = validade
        self._cvv = cvv

    @property
    def numero_cartao(self):
        return self._numero_cartao

    @numero_cartao.setter
    def numero_cartao(self, value):
        self._numero_cartao = value

    @property
    def validade(self):
        return self._validade

    @validade.setter
    def validade(self, value):
        self._validade = value

    @property
    def cvv(self):
        return self._cvv

    @cvv.setter
    def cvv(self, value):
        self._cvv = value

    def pagar(self, valor):
        print(f"Pagamento de R${valor:.2f} realizado com cartão de crédito {self._numero_cartao}.")
        return True

    def emitir_recibo(self):
        return f"Recibo: Pagamento com Cartão de Crédito - Número: {self._numero_cartao} - Data: {datetime.now()}"

class CartaoDebito(Pagamento):
    def __init__(self, numero_cartao, validade, cvv):
        self._numero_cartao = numero_cartao
        self._validade = validade
        self._cvv = cvv

    @property
    def numero_cartao(self):
        return self._numero_cartao

    @numero_cartao.setter
    def numero_cartao(self, value):
        self._numero_cartao = value

    @property
    def validade(self):
        return self._validade

    @validade.setter
    def validade(self, value):
        self._validade = value

    @property
    def cvv(self):
        return self._cvv

    @cvv.setter
    def cvv(self, value):
        self._cvv = value

    def pagar(self, valor):
        print(f"Pagamento de R${valor:.2f} realizado com cartão de débito {self._numero_cartao}.")
        return True

    def emitir_recibo(self):
        return f"Recibo: Pagamento com Cartão de Débito - Número: {self._numero_cartao} - Data: {datetime.now()}"

class Especie(Pagamento):
    def __init__(self):
        pass

    def pagar(self, valor):
        print(f"Pagamento de R${valor:.2f} realizado em espécie.")
        return True

    def emitir_recibo(self):
        return f"Recibo: Pagamento em Espécie - Data: {datetime.now()}"

class SistemaPagamento:
    def __init__(self, estoque):
        self._pagamentos = []
        self._estoque = estoque

    @property
    def pagamentos(self):
        return self._pagamentos

    @pagamentos.setter
    def pagamentos(self, value):
        self._pagamentos = value

    @property
    def estoque(self):
        return self._estoque

    @estoque.setter
    def estoque(self, value):
        self._estoque = value

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
            self._pagamentos.append(recibo)
            self.verificar_pontos_cliente(cliente)
            return recibo
        else:
            print("Falha no pagamento.")
            return None

    def verificar_pontos_cliente(self, cliente):
        if cliente.pontos > 500:
            if self._estoque.produto:
                joia_ganha = random.choice(self._estoque.produto)
                print(f"O cliente {cliente.nome} ganhou um(a) {joia_ganha.nome} por ter mais de 500 pontos!")
                self._estoque.remover_joia(joia_ganha.idjoia, 1)
            else:
                print(f"O cliente {cliente.nome} tem mais de 500 pontos, mas não há joias disponíveis no estoque.")

            
def validar_cpf(cpf):
    return len(cpf) == 11 and cpf.isdigit()

def validar_contato(contato):
    return len(contato) == 11 and contato.isdigit()

def validar_float(valor):
    try:
        float(valor)
        return True
    except ValueError:
        return False

def validar_inteiro(valor):
    try:
        int(valor)
        return True
    except ValueError:
        return False

def validar_nome(nome):
    return bool(re.match(r"^[A-Za-z\s]+$", nome))

def validar_material(material):
    return bool(re.match(r"^[A-Za-z\s]+$", material))

def validar_tamanho(tamanho):
    return bool(re.match(r"^[A-Za-z0-9\s]+$", tamanho))

def validar_estilo(estilo):
    return bool(re.match(r"^[A-Za-z\s]+$", estilo))

def validar_endereco(endereco):
    return bool(re.match(r"^[A-Za-z0-9\s,]+$", endereco))


def pausa_para_continuar():
    input("\nPressione Enter para continuar...")

Autenticar.register(Colar)
Autenticar.register(Brinco)
Autenticar.register(Pulseira)

def menu():
    estoque = Estoque()
    sistema_pagamento = SistemaPagamento(estoque)
    gestao_clientes = GestaoClientes()
    
    while True:
        print("\n----- Sistema Encanto e Glamour -----")
        print("Bem-vindo(a):")
        print("1. Cadastrar Colar")
        print("2. Cadastrar Brinco")
        print("3. Cadastrar Pulseira")
        print("4. Listar Joias")
        print("5. Buscar Joia")
        print("6. Editar Joia")
        print("7. Remover Joia")
        print("8. Cadastrar Cliente")
        print("9. Buscar Cliente")
        print("10. Editar Cliente")
        print("11. Realizar Compra")
        print("12. Mostrar Histórico de Compras do Cliente")
        print("13. Listar Clientes")
        print("14. Verificar Pontos dos Clientes")
        print("15. Sair")

        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            idjoia = input("ID da joia: ")
            if not validar_inteiro(idjoia):
                print("ID da joia inválido. Deve ser um número inteiro.")
                pausa_para_continuar()
                continue
            idjoia = int(idjoia)

            nome = input("Nome: ")
            if not validar_nome(nome):
                print("Nome inválido. Deve conter apenas letras e espaços.")
                pausa_para_continuar()
                continue

            material = input("Material: ")
            if not validar_material(material):
                print("Material inválido. Deve conter apenas letras e espaços.")
                pausa_para_continuar()
                continue

            preco = input("Preço: ")
            if not validar_float(preco):
                print("Preço inválido. Deve ser um número.")
                pausa_para_continuar()
                continue
            preco = float(preco)

            qtd = input("Quantidade: ")
            if not validar_inteiro(qtd):
                print("Quantidade inválida. Deve ser um número inteiro.")
                pausa_para_continuar()
                continue
            qtd = int(qtd)

            tamanho = input("Tamanho: ")
            if not validar_tamanho(tamanho):
                print("Tamanho inválido. Deve conter apenas letras, números e espaços.")
                pausa_para_continuar()
                continue

            codigo_validacao = input("Código de validação: ")
            try:
                colar = Colar(idjoia, nome, material, preco, qtd, tamanho, codigo_validacao)
                autenticado, mensagem = colar.autenticar()
                if autenticado:
                    print(f"{mensagem}")
                    estoque.adicionar_joia(colar)
                else:
                    print(f"{mensagem}")
                    print(f"Erro ao cadastrar colar.")
            except ValueError as e:
                print(f"Erro ao cadastrar colar: {e}")
            pausa_para_continuar()

        elif opcao == '2':
            idjoia = input("ID da joia: ")
            if not validar_inteiro(idjoia):
                print("ID da joia inválido. Deve ser um número inteiro.")
                pausa_para_continuar()
                continue
            idjoia = int(idjoia)

            nome = input("Nome: ")
            if not validar_nome(nome):
                print("Nome inválido. Deve conter apenas letras e espaços.")
                pausa_para_continuar()
                continue

            material = input("Material: ")
            if not validar_material(material):
                print("Material inválido. Deve conter apenas letras e espaços.")
                pausa_para_continuar()
                continue

            preco = input("Preço: ")
            if not validar_float(preco):
                print("Preço inválido. Deve ser um número.")
                pausa_para_continuar()
                continue
            preco = float(preco)

            qtd = input("Quantidade: ")
            if not validar_inteiro(qtd):
                print("Quantidade inválida. Deve ser um número inteiro.")
                pausa_para_continuar()
                continue
            qtd = int(qtd)

            estilo = input("Estilo: ")
            if not validar_estilo(estilo):
                print("Estilo inválido. Deve conter apenas letras e espaços.")
                pausa_para_continuar()
                continue

            codigo_validacao = input("Código de validação: ")
            try:
                brinco = Brinco(idjoia, nome, material, preco, qtd, estilo, codigo_validacao)
                autenticado, mensagem = brinco.autenticar()
                if autenticado:
                    print(f"{mensagem}")
                    estoque.adicionar_joia(brinco)
                else:
                    print(f"{mensagem}")
                    print(f"Erro ao cadastrar brinco.")
            except ValueError as e:
                print(f"Erro ao cadastrar brinco: {e}")
            pausa_para_continuar()

        elif opcao == '3':
            idjoia = input("ID da joia: ")
            if not validar_inteiro(idjoia):
                print("ID da joia inválido. Deve ser um número inteiro.")
                pausa_para_continuar()
                continue
            idjoia = int(idjoia)

            nome = input("Nome: ")
            if not validar_nome(nome):
                print("Nome inválido. Deve conter apenas letras e espaços.")
                pausa_para_continuar()
                continue

            material = input("Material: ")
            if not validar_material(material):
                print("Material inválido. Deve conter apenas letras e espaços.")
                pausa_para_continuar()
                continue

            preco = input("Preço: ")
            if not validar_float(preco):
                print("Preço inválido. Deve ser um número.")
                pausa_para_continuar()
                continue
            preco = float(preco)

            qtd = input("Quantidade: ")
            if not validar_inteiro(qtd):
                print("Quantidade inválida. Deve ser um número inteiro.")
                pausa_para_continuar()
                continue
            qtd = int(qtd)

            codigo_validacao = input("Código de validação: ")
            try:
                pulseira = Pulseira(idjoia, nome, material, preco, qtd, codigo_validacao)
                autenticado, mensagem = pulseira.autenticar()
                if autenticado:
                    print(f"{mensagem}")
                    estoque.adicionar_joia(pulseira)
                else:
                    print(f"{mensagem}")
                    print(f"Erro ao cadastrar pulseira.")
            except ValueError as e:
                print(f"Erro ao cadastrar pulseira: {e}")
            pausa_para_continuar()

        elif opcao == '4':
            estoque.listar_joias()
            pausa_para_continuar()

        elif opcao == '5':
            nome = input("Nome da joia: ")
            if not validar_nome(nome):
                print("Nome inválido. Deve conter apenas letras e espaços.")
                pausa_para_continuar()
                continue
            
            idjoia = input("ID da joia: ")
            if not validar_inteiro(idjoia):
                print("ID da joia inválido. Deve ser um número inteiro.")
                pausa_para_continuar()
                continue
            idjoia = int(idjoia)
            
            indice = input("Índice da joia: ")
            if not validar_inteiro(indice):
                print("Índice inválido. Deve ser um número inteiro.")
                pausa_para_continuar()
                continue
            indice = int(indice)
            
            
            joia = estoque.buscar_joia(indice, nome, idjoia)
            if joia:
                print(f"Joia encontrada: {joia.nome}, ID: {joia.idjoia}")
            else:
                print("Joia não encontrada.")
            pausa_para_continuar()

        elif opcao == '6':
            try:
                indice = input("Índice da joia a ser editada: ")
                if not validar_inteiro(indice):
                    print("Índice inválido. Deve ser um número inteiro.")
                    pausa_para_continuar()
                    continue
                indice = int(indice)

                
                nome = input("Novo nome (ou pressione Enter para manter o atual): ") or None
                if nome and not validar_nome(nome):
                    print("Nome inválido. Deve conter apenas letras e espaços.")
                    pausa_para_continuar()
                    continue

                idjoia = input("ID da joia (ou pressione Enter para manter o atual): ") or None
                if idjoia and not validar_inteiro(idjoia):
                    print("ID da joia inválido. Deve ser um número inteiro.")
                    pausa_para_continuar()
                    continue
                idjoia = int(idjoia) if idjoia else None

                material = input("Novo material (ou pressione Enter para manter o atual): ") or None
                if material and not validar_material(material):
                    print("Material inválido. Deve conter apenas letras e espaços.")
                    pausa_para_continuar()
                    continue

                preco = input("Novo preço (ou pressione Enter para manter o atual): ") or None
                if preco and not validar_float(preco):
                    print("Preço inválido. Deve ser um número.")
                    pausa_para_continuar()
                    continue
                preco = float(preco) if preco else None

                quantidade = input("Nova quantidade (ou pressione Enter para manter o atual): ") or None
                if quantidade and not validar_inteiro(quantidade):
                    print("Quantidade inválida. Deve ser um número inteiro.")
                    pausa_para_continuar()
                    continue
                quantidade = int(quantidade) if quantidade else None

                tamanho = input("Novo tamanho (ou pressione Enter para manter o atual): ") or None
                if tamanho and not validar_tamanho(tamanho):
                    print("Tamanho inválido. Deve conter apenas letras, números e espaços.")
                    pausa_para_continuar()
                    continue

                estilo = input("Novo estilo (ou pressione Enter para manter o atual): ") or None
                if estilo and not validar_estilo(estilo):
                    print("Estilo inválido. Deve conter apenas letras e espaços.")
                    pausa_para_continuar()
                    continue

                codigo_validacao = input("Novo código de validação (ou pressione Enter para manter o atual): ") or None

                
                campos_editados = any([nome, idjoia, material, preco, quantidade, tamanho, estilo, codigo_validacao])
                if not campos_editados:
                    print("Nenhuma alteração foi feita.")
                    pausa_para_continuar()
                    continue

                
                estoque.editar_joia(indice, nome, idjoia, material, preco, quantidade, tamanho, estilo, codigo_validacao)
                print("Joia editada com sucesso.")
            except ValueError as e:
                print(f"Erro ao editar joia: {e}")
            pausa_para_continuar()


        elif opcao == '7':
            indice = input("ID da joia a ser removida: ")
            if not validar_inteiro(indice):
                print("ID deve ser um número inteiro.")
                pausa_para_continuar()
                continue
            indice = int(indice)

            quantidade = input("Quantidade a ser removida: ")
            if not validar_inteiro(quantidade):
                print("Quantidade deve ser um número inteiro.")
                pausa_para_continuar()
                continue
            quantidade = int(quantidade)

            estoque.remover_joia(indice, quantidade)
            pausa_para_continuar()
            
        elif opcao == '8':
            nome = input("Nome do cliente: ")
            if not validar_nome(nome):
                print("Nome inválido. Deve conter apenas letras e espaços.")
                pausa_para_continuar()
                continue

            endereco = input("Endereço: ")
            if not validar_endereco(endereco):
                print("Endereço inválido. Deve conter apenas letras, números e espaços.")
                pausa_para_continuar()
                continue

            contato = input("Contato (11 dígitos): ")
            if not validar_contato(contato):
                print("Contato inválido. Deve ter 11 dígitos.")
                pausa_para_continuar()
                continue

            cpf = input("CPF do cliente (11 dígitos): ")
            if not validar_cpf(cpf):
                print("CPF inválido. Deve ter 11 dígitos.")
                pausa_para_continuar()
                continue

            gestao_clientes.cadastrar_cliente(nome, cpf, endereco, contato)
            pausa_para_continuar()

        elif opcao == '9':
            cpf = input("CPF do cliente: ")
            if not validar_cpf(cpf):
                print("CPF inválido. Deve conter apenas números.")
                pausa_para_continuar()
                continue
            
            cliente = gestao_clientes.buscar_cliente(cpf)
            
            pausa_para_continuar()

        elif opcao == '10':
            try:
                cpf = input("CPF do cliente (11 dígitos): ")
                if not validar_cpf(cpf):
                    print("CPF inválido. Deve ter 11 dígitos.")
                    pausa_para_continuar()
                    continue

                nome = input("Novo nome (ou pressione Enter para manter o atual): ")
                if nome and not validar_nome(nome):
                    print("Nome inválido. Deve conter apenas letras e espaços.")
                    pausa_para_continuar()
                    continue

                endereco = input("Novo endereço (ou pressione Enter para manter o atual): ")
                if endereco and not validar_endereco(endereco):
                    print("Endereço inválido. Deve conter apenas letras, números e espaços.")
                    pausa_para_continuar()
                    continue

                contato = input("Novo contato (ou pressione Enter para manter o atual): ")
                if contato and not validar_contato(contato):
                    print("Contato inválido. Deve ter 11 dígitos.")
                    pausa_para_continuar()
                    continue

                pontos = input("Pontos (ou pressione Enter para manter o atual): ")
                pontos = int(pontos) if pontos and validar_inteiro(pontos) else None

                
                campos_editados = any([nome, endereco, contato, pontos is not None])
                if not campos_editados:
                    print("Nenhuma alteração foi feita.")
                    pausa_para_continuar()
                    continue

                gestao_clientes.editar_cliente(cpf, nome, endereco, contato, pontos)
                print("Cliente editado com sucesso.")
            except ValueError as e:
                print(f"Erro ao editar cliente: {e}")
            pausa_para_continuar()

        elif opcao == '11':
            cpf = input("CPF do cliente (11 dígitos): ")
            if not validar_cpf(cpf):
                print("CPF inválido. Deve ter 11 dígitos.")
                pausa_para_continuar()
                continue

            cliente = gestao_clientes.buscar_cliente(cpf)
            if cliente:
                idjoia = input("ID da joia: ")
                if not validar_inteiro(idjoia):
                    print("ID da joia inválido. Deve ser um número inteiro.")
                    pausa_para_continuar()
                    continue
                idjoia = int(idjoia)

                quantidade = input("Quantidade: ")
                if not validar_inteiro(quantidade):
                    print("Quantidade inválida. Deve ser um número inteiro.")
                    pausa_para_continuar()
                    continue
                quantidade = int(quantidade)

                joia = next((j for j in estoque.produto if j.idjoia == idjoia), None)
                if joia:
                    gestao_clientes.adicionar_compra_cliente(cpf, joia, quantidade, estoque)
                else:
                    print("Joia não encontrada no estoque.")
            else:
                print("Cliente não encontrado.")
            pausa_para_continuar()


        elif opcao == '12':
            cpf = input("CPF do cliente (11 dígitos): ")
            if not validar_cpf(cpf):
                print("CPF inválido. Deve ter 11 dígitos.")
                pausa_para_continuar()
                continue
            gestao_clientes.historico_compras_cliente(cpf)
            pausa_para_continuar()

        elif opcao == '13':
            gestao_clientes.listar_clientes()
            pausa_para_continuar()
            
        elif opcao == '14':
            cpf = input("CPF do cliente (11 dígitos): ")
            if not validar_cpf(cpf):
                print("CPF inválido. Deve ter 11 dígitos.")
                pausa_para_continuar()
                continue

            cliente = gestao_clientes.buscar_cliente(cpf)
            if cliente:
                sistema_pagamento.verificar_pontos_cliente(cliente)
            else:
                print("Cliente não encontrado.")
            pausa_para_continuar()
            
        elif opcao == '15':
            print("Saindo da aplicação...")
            break

        else:
            print("Opção inválida. Tente novamente.")
            pausa_para_continuar()

menu()