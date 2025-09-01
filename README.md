<h1>Minha Lista de Tarefas em Python</h1>

Uma aplicação simples e intuitiva de lista de tarefas com interface gráfica, desenvolvida em Python. Este projeto permite organizar suas atividades, marcá-las como concluídas, editar, remover e reordená-las.

![Texto Alternativo para o GIF](https://i.imgur.com/qgDvr2G.gif)


<h2>Funcionalidades</h2>

- **Adicionar Tarefas:** Insira novas tarefas na lista de forma rápida.

- **Marcar como Concluído:** Use os checkboxes para marcar as tarefas que já foram finalizadas.

- **Editar Tarefas:** Modifique o título de qualquer tarefa existente.

- **Remover Tarefas:** Exclua tarefas da sua lista.

- **Reordenar:** Mova as tarefas para cima ou para baixo para priorizar a sua lista.

- **Persistência de Dados:** As tarefas são salvas em um banco de dados local (.db), garantindo que não sejam perdidas ao fechar o aplicativo.

<h2>Tecnologias Utilizadas</h2>

- **Python:** Linguagem de programação principal.

- **Tkinter:** Módulo nativo do Python para a criação da interface gráfica (frontend).

- **SQLite3:** Módulo nativo do Python para o gerenciamento de banco de dados (backend).

- **ttkbootstrap:** Biblioteca de temas para o Tkinter, utilizada para dar uma aparência moderna à aplicação.

<h2>Como Executar o Projeto</h2>

Siga os passos abaixo para rodar o projeto em sua máquina local.

**Pré-requisitos**
- Python 3.7+ instalado.
- Conexão com a internet para instalar as dependências.

**Passo a Passo**

1. Clone este repositório para a sua máquina:

*Bash*
>git clone https://github.com/guiysyama/todolist.git

2. Navegue até o diretório do projeto:

*Bash*
>cd [todolist]

3. Crie e ative um ambiente virtual (recomendado):

*Bash*
>python -m venv venv
.\venv\Scripts\activate  *# No Windows <p># source venv/bin/activate # No macOS/Linux*

4. Instale a dependência do projeto:

*Bash*
>pip install ttkbootstrap

5. Execute o arquivo principal para iniciar a aplicação:

*Bash*
>python todo.py


<h2>Autor</h2>
[Siraissi]

GitHub: @guiysyama