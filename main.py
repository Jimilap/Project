import sqlite3 
import tkinter as tk
from tkinter import ttk

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.db = db
        self.init_main()
        self.view_records()

    # Метод инициализации виджетов
    def init_main(self):
        # тулбар
        toolbar = tk.Frame(bg = '#d7d7d7', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Кнопка добавления 
        # PhotoImage - добавленное изображение
        self.add_img = tk.PhotoImage(file='add.png')
        # image - картинка, которая размещена на кнопке
        # bg - фон
        # bd - граница 
        btn_add = tk.Button(toolbar, text= 'Добавить',
                            image=self.add_img,
                            bg = "#d7d7d7", bd=0, 
                            command=self.open_child
                            )
        btn_add.pack(side=tk.LEFT)
        
        # Кнопка редактирования 
        self.upd_img = tk.PhotoImage(file='update.png')
        btn_upd = tk.Button(toolbar, image=self.upd_img,
                            bg = "#d7d7d7", bd=0, 
                            command=self.open_update
                            )
        btn_upd.pack(side=tk.LEFT)

        # Кнопка удаления 
        self.del_img = tk.PhotoImage(file='delete.png')
        del_upd = tk.Button(toolbar, image=self.del_img,
                            bg = "#d7d7d7", bd=0, 
                            command=self.del_records
                            )
        del_upd.pack(side=tk.LEFT)

        # Кнопка поиска 
        self.search_img = tk.PhotoImage(file='search.png')
        btn_search = tk.Button(toolbar, image=self.search_img,
                            bg = "#d7d7d7", bd=0, 
                            command=self.open_search
                            )
        btn_search.pack(side=tk.LEFT)

        # Кнопка обновления
        self.refresh_img = tk.PhotoImage(file='refresh.png')
        refresh_upd = tk.Button(toolbar, image=self.refresh_img,
                            bg = "#d7d7d7", bd=0, 
                            command=self.view_records
                            )
        refresh_upd.pack(side=tk.LEFT)

        # Таблица для вывода информации контактов 
        self.tree = ttk.Treeview(self,
                                columns=('ID', 'name', 'phone', 'email'),
                                show= 'headings', height= 17)
        
        # Настройки для столбцов
        self.tree.column('ID', width=45, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('phone', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)

        # Задаём подписи столбцам
        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('phone', text='Телефон')
        self.tree.heading('email', text='Email')

        self.tree.pack()

        # Создание скроллбара
        scroll = tk.Scrollbar(root, command=self.tree.yview)
        scroll.pack(side=tk.RIGHT, fill= tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    # Метод добавления в БД
    def record(self, name, phone, email):
        self.db.insert_data(name, phone, email)
        self.view_records()

    # Метод редактирования
    def upd_record(self, name, phone, email):
        id =self.tree.set(self.tree.selection()[0], '#1')
        self.db.cur.execute('''
            UPDATE Users SET name = ?, phone = ?, email = ?
            WHERE id = ?''', (name, phone, email, id))
        self.db.conn.commit()
        self.view_records()
    
    # Метод удаления
    def del_records(self):
        for i in self.tree.selection():
            self.db.cur.execute('DELETE FROM Users WHERE id = ?',
                                (self.tree.set(i, '#1'),))
        self.db.conn.commit()
        self.view_records()

    # Метод поиска
    def search_records(self, name):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.db.cur.execute('SELECT * FROM Users WHERE name LIKE ?', ('%' + name + '%',))
        r = self.db.cur.fetchall()
        for j in r:
            self.tree.insert('', 'end', values=j)
    
    # Перезаполнение виджета таблицы
    def view_records(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.db.cur.execute('SELECT * FROM Users')
        r = self.db.cur.fetchall()
        for j in r:
            self.tree.insert('', 'end', values=j)
    
    # Метод открытия окна добавления 
    def open_child(self):
        Child()
    
    # Метод открытия окна редактирования
    def open_update(self):
        Update()

    # Метод открытия окна поиска
    def open_search(self):
        Search()

class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.view = app
        self.init_child()
    
    def init_child(self):
        self.title('Добавление контакта')
        self.geometry('400x200')
        self.resizable(False, False)
        # Перехватываеем события, происходящие в приложении
        self.grab_set()
        # Перехватываем фокус
        self.focus_set()

        label_name = tk.Label(self, text='Фио')
        label_phone = tk.Label(self, text='Телефон')
        label_email = tk.Label(self, text='Email')
        label_name.place(x=60, y=50)
        label_phone.place(x=60, y=80)
        label_email.place(x=60, y=110)

        self.entry_name = tk.Entry(self)
        self.entry_phone = tk.Entry(self)
        self.entry_email = tk.Entry(self)
        self.entry_name.place(x=220, y=50)
        self.entry_phone.place(x=220, y=80)
        self.entry_email.place(x=220, y=110)

        btn_close = tk.Button(self, text='Закрыть', command=self.destroy)
        btn_close.place(x=220, y=160)

        self.btn_ok = tk.Button(self, text='Добавить')
        self.btn_ok.bind('<Button-1>', lambda ev: self.view.record(self.entry_name.get(),
                                                                   self.entry_phone.get(),
                                                                   self.entry_email.get()))
        self.btn_ok.place(x=290, y=160)

# Класс редактирования
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_update()
        self.db = db
        self.default_data()
    
    def init_update(self):
        self.title('Редактирование контакта')
        self.btn_ok.destroy()
        self.btn_upd = tk.Button(self, text='Сохранить')
        self.btn_upd.bind('<Button-1>', lambda ev: self.view.upd_record(self.entry_name.get(),
                                                                        self.entry_phone.get(),
                                                                        self.entry_email.get()))
        self.btn_upd.bind('<Button-1>', lambda ev: self.destroy(), add='+')
        self.btn_upd.place(x=290, y=160)

    # Метод автозаполнения формы
    def default_data(self):
        id = self.view.tree.set(self.view.tree.selection()[0], '#1')
        self.db.cur.execute('SELECT * FROM Users WHERE id = ?', (id,))
        row = self.db.cur.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_phone.insert(0, row[2])
        self.entry_email.insert(0, row[3])

# Класс окна поиска
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.view = app
        self.init_search()
    
    # Метод для создания виджетов для дочернего окна
    def init_search(self):
        self.title('')
        self.geometry('300x100')
        self.resizable(False, False)
        # Перехватываеем события, происходящие в приложении
        self.grab_set()
        # Перехватываем фокус
        self.focus_set()

        label_name = tk.Label(self, text='Фио')
        label_name.place(x=40, y=20)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=140, y=20)

        btn_close = tk.Button(self, text = 'Закрыть', command= self.destroy)
        btn_close.place(x=130, y= 70)

        self.btn_ok = tk.Button(self, text='Найти')
        self.btn_ok.bind('<Button-1>', lambda ev: self.view.search_records(self.entry_name.get(),))
        self.btn_ok.bind('<Button-1>', lambda ev: self.destroy(), add='+')
        self.btn_ok.place(x=220, y=70)


# Класс БД
class Db():
    # Создание соединения, курсора и таблицы (если её нет)
    def __init__(self):
        self.conn = sqlite3.connect('Contacts.db')
        self.cur = self.conn.cursor()
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                         id INTEGER PRIMARY KEY,
                         name TEXT,
                         phone TEXT,
                         email TEXT
            )''')
    
    # Метод добавления в БД
    def insert_data(self, name, phone, email):
        self.cur.execute('''
                INSERT INTO Users (name, phone, email)
                VALUES (?, ?, ?)
                ''', (name, phone, email))
        self.conn.commit()

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Телефонная книга')
    root.geometry('665x450')
    root.resizable(False, False)
    db = Db()
    app = Main(root)
    app.pack()
    root.mainloop()