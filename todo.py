import tkinter as tk
from tkinter import messagebox
import sqlite3
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# --- BACKEND: Gerenciamento do Banco de Dados SQLite (NOVA VERSÃO) ---
def setup_database():
    """Cria e configura o banco de dados e a tabela de tarefas, incluindo a coluna de ordem."""
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            completed INTEGER NOT NULL,
            list_order INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_tasks():
    """Obtém todas as tarefas do banco de dados, ordenadas por status e ordem."""
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    # Pega todas as tarefas, ordenando primeiro pelo status e depois pela ordem
    cursor.execute("SELECT id, title, completed, list_order FROM tasks ORDER BY completed ASC, list_order ASC")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def add_task(title):
    """Adiciona uma nova tarefa ao banco de dados com uma ordem."""
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    # Obtém o maior valor de ordem atual para a nova tarefa
    cursor.execute("SELECT MAX(list_order) FROM tasks")
    max_order = cursor.fetchone()[0]
    new_order = (max_order or 0) + 1
    cursor.execute("INSERT INTO tasks (title, completed, list_order) VALUES (?, 0, ?)", (title, new_order,))
    conn.commit()
    conn.close()

def delete_task(task_id):
    """Remove uma tarefa do banco de dados."""
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def update_task_status(task_id, completed_status):
    """Atualiza o status de uma tarefa (concluída ou não)."""
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", (completed_status, task_id))
    conn.commit()
    conn.close()

def update_task_title(task_id, new_title):
    """Edita o título de uma tarefa."""
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET title = ? WHERE id = ?", (new_title, task_id))
    conn.commit()
    conn.close()

def move_task_up(task_id, current_order):
    """Move uma tarefa para cima, trocando sua ordem com a tarefa anterior."""
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    # Encontra a tarefa acima da atual
    cursor.execute("SELECT id, list_order FROM tasks WHERE completed = 0 AND list_order < ? ORDER BY list_order DESC LIMIT 1", (current_order,))
    prev_task = cursor.fetchone()
    
    if prev_task:
        prev_id, prev_order = prev_task
        # Troca a ordem das duas tarefas
        cursor.execute("UPDATE tasks SET list_order = ? WHERE id = ?", (prev_order, task_id))
        cursor.execute("UPDATE tasks SET list_order = ? WHERE id = ?", (current_order, prev_id))
        conn.commit()
    conn.close()

def move_task_down(task_id, current_order):
    """Move uma tarefa para baixo, trocando sua ordem com a tarefa seguinte."""
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    # Encontra a tarefa abaixo da atual
    cursor.execute("SELECT id, list_order FROM tasks WHERE completed = 0 AND list_order > ? ORDER BY list_order ASC LIMIT 1", (current_order,))
    next_task = cursor.fetchone()
    
    if next_task:
        next_id, next_order = next_task
        # Troca a ordem das duas tarefas
        cursor.execute("UPDATE tasks SET list_order = ? WHERE id = ?", (next_order, task_id))
        cursor.execute("UPDATE tasks SET list_order = ? WHERE id = ?", (current_order, next_id))
        conn.commit()
    conn.close()

# --- FRONTEND: Interface Gráfica com ttkbootstrap ---
class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Minha Lista de Tarefas")
        
        setup_database()
        self.create_widgets()
        self.refresh_display()

    def create_widgets(self):
        """Cria todos os widgets da interface gráfica usando ttkbootstrap."""
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=BOTH, expand=True)

        input_frame = ttk.Frame(main_frame)
        input_frame.pack(pady=10)
        
        self.task_entry = ttk.Entry(input_frame, width=50)
        self.task_entry.pack(side=LEFT, padx=5)

        add_button = ttk.Button(input_frame, text="Adicionar", command=self.add_new_task, bootstyle="success")
        add_button.pack(side=LEFT)

        self.tasks_container = ttk.Frame(main_frame)
        self.tasks_container.pack(fill=BOTH, expand=True)

        self.canvas = tk.Canvas(self.tasks_container, width=500, height=300)
        scrollbar = ttk.Scrollbar(self.tasks_container, orient=VERTICAL, command=self.canvas.yview, bootstyle="round")
        self.tasks_frame = ttk.Frame(self.canvas)

        self.tasks_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.canvas.create_window((0, 0), window=self.tasks_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

    def refresh_display(self):
        """Limpa e recarrega a lista de tarefas, criando widgets com checkboxes."""
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()

        tasks = get_tasks()
        for task_id, title, completed, order in tasks:
            self.create_task_widget(task_id, title, completed, order)

    def create_task_widget(self, task_id, title, completed, order):
        """Cria um frame com checkbox, label e botões para uma tarefa."""
        task_frame = ttk.Frame(self.tasks_frame, padding=5)
        task_frame.pack(fill=X)
        
        status_var = tk.IntVar(value=completed)
        status_var.trace("w", lambda *args: self.update_task_status_via_checkbox(task_id, status_var.get()))

        checkbox = ttk.Checkbutton(task_frame, variable=status_var, bootstyle="round-toggle")
        checkbox.pack(side=LEFT)
        
        task_label = ttk.Label(task_frame, text=title, anchor='w')
        task_label.pack(side=LEFT, fill=X, expand=True)

        if not completed: # Mostra botões de reordenação apenas para tarefas "a fazer"
            up_button = ttk.Button(task_frame, text="▲", command=lambda: self.move_task("up", task_id, order), bootstyle="primary-outline", width=3)
            up_button.pack(side=RIGHT, padx=2)
            
            down_button = ttk.Button(task_frame, text="▼", command=lambda: self.move_task("down", task_id, order), bootstyle="primary-outline", width=3)
            down_button.pack(side=RIGHT, padx=2)
        
        edit_button = ttk.Button(task_frame, text="Editar", command=lambda: self.edit_task(task_id, task_label), bootstyle="info-outline", width=8)
        edit_button.pack(side=RIGHT, padx=5)
        
        remove_button = ttk.Button(task_frame, text="Remover", command=lambda: self.remove_task(task_id), bootstyle="danger-outline", width=8)
        remove_button.pack(side=RIGHT)

    def add_new_task(self):
        """Adiciona uma nova tarefa ao banco de dados e atualiza a lista."""
        title = self.task_entry.get()
        if title:
            add_task(title)
            self.task_entry.delete(0, tk.END)
            self.refresh_display()
        else:
            messagebox.showwarning("Aviso", "Por favor, digite uma tarefa.")

    def update_task_status_via_checkbox(self, task_id, status):
        """Atualiza o status da tarefa no banco de dados quando o checkbox é clicado."""
        update_task_status(task_id, status)
        self.refresh_display()

    def edit_task(self, task_id, task_label):
        """Permite editar o título de uma tarefa selecionada."""
        task_label.pack_forget()
        edit_entry = ttk.Entry(task_label.master, width=30)
        edit_entry.insert(0, task_label.cget("text"))
        edit_entry.pack(side=LEFT, fill=X, expand=True)
        edit_entry.focus_set()
        
        save_button = ttk.Button(task_label.master, text="Salvar", bootstyle="success",
                                 command=lambda: self.save_edited_task(task_id, edit_entry.get(), edit_entry, save_button, task_label))
        save_button.pack(side=LEFT)
        
        for widget in task_label.master.winfo_children():
            if widget.cget("text") in ["Editar", "Remover", "▲", "▼"]:
                widget.pack_forget()

    def save_edited_task(self, task_id, new_title, edit_entry, save_button, task_label):
        """Salva a tarefa editada e restaura a interface."""
        if new_title:
            update_task_title(task_id, new_title)
            self.refresh_display()
        else:
            messagebox.showwarning("Aviso", "O título da tarefa não pode estar vazio.")

    def remove_task(self, task_id):
        """Remove a tarefa do banco de dados."""
        if messagebox.askyesno("Remover Tarefa", "Tem certeza que deseja remover esta tarefa?"):
            delete_task(task_id)
            self.refresh_display()
            
    def move_task(self, direction, task_id, current_order):
        """Chama a função apropriada para mover a tarefa."""
        if direction == "up":
            move_task_up(task_id, current_order)
        elif direction == "down":
            move_task_down(task_id, current_order)
        self.refresh_display()

# --- Executa a Aplicação ---
if __name__ == "__main__":
    app = ttk.Window(themename="superhero")
    ToDoApp(app)
    app.mainloop()