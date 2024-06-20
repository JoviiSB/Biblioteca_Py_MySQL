import mysql.connector
from mysql.connector import Error
from datetime import date, timedelta

class Livro:
    def __init__(self, titulo, autor, categoria):
        self.titulo = titulo
        self.autor = autor
        self.categoria = categoria

class Cliente:
    def __init__(self, nome, preferencias):
        self.nome = nome
        self.preferencias = preferencias

class BibliotecaDB:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="he182555@",
                database="biblioteca_db"
            )
            if self.conn.is_connected():
                print("Conectado ao MySQL!")
                print("="*40)
                self.cursor = self.conn.cursor()
        except Error as e:
            print(e)

    def adicionar_livro(self, livro):
        sql = "INSERT INTO livros (titulo, autor, categoria) VALUES (%s, %s, %s)"
        val = (livro.titulo, livro.autor, livro.categoria)
        self.cursor.execute(sql, val)
        self.conn.commit()
        print("Livro adicionado com sucesso.")
        print("="*40)

    def mostrar_livros_por_categoria(self, categoria):
        self.cursor.execute("SELECT * FROM livros WHERE categoria = %s", (categoria,))
        livros = self.cursor.fetchall()
        print(f"Lista de Livros na Categoria '{categoria}':")
        for livro in livros:
            print(livro)
        print("="*40)

    def adicionar_cliente(self, cliente):
        preferencias_str = ", ".join(cliente.preferencias)
        sql = "INSERT INTO clientes (nome, preferencias) VALUES (%s, %s)"
        val = (cliente.nome, preferencias_str)
        self.cursor.execute(sql, val)
        self.conn.commit()
        print("Cliente adicionado com sucesso.")
        print("="*40)

    def mostrar_clientes(self):
        self.cursor.execute("SELECT * FROM clientes")
        clientes = self.cursor.fetchall()
        print("Lista de Clientes:")
        for cliente in clientes:
            print(cliente)
        print("="*40)

    def realizar_emprestimo(self, id_cliente, id_livro):
        data_emprestimo = date.today()
        data_devolucao = data_emprestimo + timedelta(days=7)  # Exemplo: empréstimo por 7 dias
        sql = "INSERT INTO emprestimos (id_cliente, id_livro, data_emprestimo, data_devolucao) VALUES (%s, %s, %s, %s)"
        val = (id_cliente, id_livro, data_emprestimo, data_devolucao)
        self.cursor.execute(sql, val)
        self.conn.commit()
        print("Empréstimo realizado com sucesso.")
        print("="*40)

    def consultar_emprestimos_cliente(self, id_cliente):
        sql = "SELECT l.titulo, l.autor, e.data_emprestimo, e.data_devolucao FROM emprestimos e JOIN livros l ON e.id_livro = l.id WHERE e.id_cliente = %s"
        val = (id_cliente,)
        self.cursor.execute(sql, val)
        emprestimos = self.cursor.fetchall()
        if emprestimos:
            print(f"Empréstimos do cliente {id_cliente}:")
            for emprestimo in emprestimos:
                print(f"Título: {emprestimo[0]}, Autor: {emprestimo[1]}, Data Empréstimo: {emprestimo[2]}, Data Devolução: {emprestimo[3]}")
            print("="*40)
        else:
            print(f"Cliente {id_cliente} não possui empréstimos ativos.")
            print("="*40)

    def devolver_livro(self, id_cliente, id_livro):
        sql = "DELETE FROM emprestimos WHERE id_cliente = %s AND id_livro = %s"
        val = (id_cliente, id_livro)
        self.cursor.execute(sql, val)
        self.conn.commit()
        print("Livro devolvido com sucesso.")
        print("="*40)

    def fechar_conexao(self):
        self.cursor.close()
        self.conn.close()
        print("Conexão fechada.")
        print("="*40)

print("="*40)
def menu():
    print("-------- Escolha uma das Opções --------")
    print("1. Adicionar Livro;")
    print("2. Mostrar Livros por Categoria;")
    print("3. Adicionar Cliente;")
    print("4. Mostrar Clientes;")
    print("5. Realizar Empréstimo;")
    print("6. Consultar Empréstimos de um Cliente;")
    print("7. Devolver Livro;")
    print("8. Sair.")


if __name__ == "__main__":
    biblioteca_db = BibliotecaDB()

    while True:
        menu()
        escolha = input("Digite uma das opções (1 a 8): ")
        print('='*40)

        if escolha == "1":
            titulo = input("Título do livro: ")
            autor = input("Autor do livro: ")
            categoria = input("Categoria do livro: ")
            livro = Livro(titulo, autor, categoria)
            biblioteca_db.adicionar_livro(livro)

        elif escolha == "2":
            categoria = input("Digite a categoria dos livros que deseja visualizar: ")
            biblioteca_db.mostrar_livros_por_categoria(categoria)

        elif escolha == "3":
            nome = input("Nome do cliente: ")
            preferencias = input("Preferências do cliente (separadas por vírgula): ").split(",")
            cliente = Cliente(nome, preferencias)
            biblioteca_db.adicionar_cliente(cliente)

        elif escolha == "4":
            biblioteca_db.mostrar_clientes()

        elif escolha == "5":
            id_cliente = int(input("ID do cliente: "))
            id_livro = int(input("ID do livro: "))
            biblioteca_db.realizar_emprestimo(id_cliente, id_livro)

        elif escolha == "6":
            id_cliente = int(input("ID do cliente: "))
            biblioteca_db.consultar_emprestimos_cliente(id_cliente)

        elif escolha == "7":
            id_cliente = int(input("ID do cliente: "))
            id_livro = int(input("ID do livro: "))
            biblioteca_db.devolver_livro(id_cliente, id_livro)

        elif escolha == "8":
            print("Saindo...")
            biblioteca_db.fechar_conexao()
            break

        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
            print("="*40)