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
            
            # Chama o método de busca
            joia = estoque.buscar_joia(indice, nome, idjoia)
            if joia:
                print(f"Joia encontrada: {joia.nome}, ID: {joia.idjoia}")
            else:
                print("Joia não encontrada.")
            pausa_para_continuar()