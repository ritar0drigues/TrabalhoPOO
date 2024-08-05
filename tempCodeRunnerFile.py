    def buscar_cliente(self, cpf):
        for cliente in self._clientes:
            if cliente.cpf == cpf:
                print(f"Cliente {cliente.nome} encontrado e cadastrado no sistema")
                return cliente
        print(f"Cliente não encontrado no sistema.")
        return None