import tkinter as tk
from tkinter import messagebox, ttk, PhotoImage
import mysql.connector
import os

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        port=33061,
        user="root",
        password="123456",
        database="zhzb",
        charset="utf8mb4"
    )

def add_owner():
    rd = rd_entry.get()
    ner = ner_entry.get()
    owog = owog_entry.get()
    hayag = hayag_entry.get()
    utas = utas_entry.get()
    unemleh_val = unemleh_entry.get()

    if rd and ner and owog:
        try:
            db = connect_db()
            cur = db.cursor()
            cur.execute("""
                INSERT INTO ezemshgch (EzemshigchRD, Ner, Owog, Hayag, Utas, unemleh)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (rd, ner, owog, hayag or None, utas or None, unemleh_val or None))
            db.commit()
            messagebox.showinfo("Амжилттай", "Эзэмшигч нэмэгдлээ")
            clear_entries()
            read_owners()
        except mysql.connector.IntegrityError:
            messagebox.showerror("Алдаа", "RD давхцаж байна")
        finally:
            db.close()
    else:
        messagebox.showwarning("Анхаар", "RD, Нэр, Овог гурвыг заавал бөглөнө үү")

def read_owners():
    db = connect_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM ezemshgch")
    rows = cur.fetchall()
    db.close()

    for i in tree.get_children():
        tree.delete(i)
    for row in rows:
        tree.insert("", "end", values=row)

def update_owner():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Анхаар", "Мөр сонгоно уу")
        return

    old_rd = tree.item(selected)["values"][0]

    new_rd = rd_entry.get()
    ner = ner_entry.get()
    owog = owog_entry.get()
    hayag = hayag_entry.get()
    utas = utas_entry.get()
    unemleh_val = unemleh_entry.get()

    if not (new_rd and ner and owog):
        messagebox.showwarning("Анхаар", "RD, Нэр, Овог заавал бөглөнө үү")
        return

    db = connect_db()
    cur = db.cursor()
    cur.execute("""
        UPDATE ezemshgch
        SET EzemshigchRD=%s, Ner=%s, Owog=%s, Hayag=%s, Utas=%s, unemleh=%s
        WHERE EzemshigchRD=%s
    """, (new_rd, ner, owog, hayag or None, utas or None, unemleh_val or None, old_rd))
    db.commit()
    db.close()
    messagebox.showinfo("Амжилттай", "Шинэчлэгдлээ")
    clear_entries()
    read_owners()

def delete_owner():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Анхаар", "Мөр сонгоно уу")
        return
    rd = tree.item(selected)["values"][0]

    db = connect_db()
    cur = db.cursor()
    cur.execute("DELETE FROM ezemshgch WHERE EzemshigchRD=%s", (rd,))
    db.commit()
    db.close()
    messagebox.showinfo("Амжилттай", "Устгагдлаа")
    clear_entries()
    read_owners()

def search_owner():
    keyword = search_entry.get()
    if not keyword:
        messagebox.showwarning("Анхаар", "Хайх утга оруулна уу")
        return

    db = connect_db()
    cur = db.cursor()
    query = """
        SELECT * FROM ezemshgch
        WHERE EzemshigchRD LIKE %s OR Ner LIKE %s OR Owog LIKE %s
    """
    like = f"%{keyword}%"
    cur.execute(query, (like, like, like))
    rows = cur.fetchall()
    db.close()

    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert("", "end", values=row)

def on_select(event):
    selected = tree.focus()
    if not selected:
        return
    values = tree.item(selected, "values")
    rd_entry.delete(0, tk.END); rd_entry.insert(0, values[0])
    ner_entry.delete(0, tk.END); ner_entry.insert(0, values[1])
    owog_entry.delete(0, tk.END); owog_entry.insert(0, values[2])
    hayag_entry.delete(0, tk.END); hayag_entry.insert(0, values[3])
    utas_entry.delete(0, tk.END); utas_entry.insert(0, values[4])
    unemleh_entry.delete(0, tk.END); unemleh_entry.insert(0, values[5])

def clear_entries():
    for e in [rd_entry, ner_entry, owog_entry, hayag_entry, utas_entry, unemleh_entry]:
        e.delete(0, tk.END)

root = tk.Tk()
root.title("Эзэмшигчийн мэдээллийн систем")
root.geometry("1000x650")
root.configure(bg="#f5f5f5")

if os.path.exists("logo.png"):
    img = PhotoImage(file="logo.png")
    tk.Label(root, image=img, bg="#f5f5f5").pack(pady=10)

tk.Label(root, text="Эзэмшигчийн Мэдээллийн Систем", font=("Arial", 18, "bold"), bg="#f5f5f5").pack()

form_frame = tk.Frame(root, bg="#f5f5f5")
form_frame.pack(pady=10)

labels = ["RD", "Нэр", "Овог", "Хаяг", "Утас", "Үнэмлэх"]
entries = []
for i, label in enumerate(labels):
    tk.Label(form_frame, text=label, bg="#f5f5f5", font=("Arial", 11)).grid(row=i, column=0, sticky="e", padx=5, pady=4)
    entry = tk.Entry(form_frame, width=30)
    entry.grid(row=i, column=1, padx=5, pady=4)
    entries.append(entry)

rd_entry, ner_entry, owog_entry, hayag_entry, utas_entry, unemleh_entry = entries

btn_frame = tk.Frame(root, bg="#f5f5f5")
btn_frame.pack(pady=5)
tk.Button(btn_frame, text="Нэмэх", command=add_owner, bg="#27ae60", fg="white", width=12).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Шинэчлэх", command=update_owner, bg="#2980b9", fg="white", width=12).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Устгах", command=delete_owner, bg="#c0392b", fg="white", width=12).grid(row=0, column=2, padx=5)

search_frame = tk.Frame(root, bg="#f5f5f5")
search_frame.pack(pady=10)
tk.Label(search_frame, text="Хайлт:", bg="#f5f5f5").pack(side=tk.LEFT)
search_entry = tk.Entry(search_frame, width=30)
search_entry.pack(side=tk.LEFT, padx=5)
tk.Button(search_frame, text="Хайх", command=search_owner, bg="#8e44ad", fg="white").pack(side=tk.LEFT)

columns = ["RD", "Нэр", "Овог", "Хаяг", "Утас", "Үнэмлэх"]
tree = ttk.Treeview(root, columns=columns, show="headings", height=12)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=140)

tree.bind("<<TreeviewSelect>>", on_select)
tree.pack(padx=10, pady=15)

style = ttk.Style()
style.theme_use("default")
style.configure("Treeview",
                background="#ffffff",
                foreground="#000000",
                rowheight=25,
                fieldbackground="#ffffff",
                font=("Arial", 10))
style.configure("Treeview.Heading",
                background="#4CAF50",
                foreground="white",
                font=("Arial", 11, "bold"))
style.map("Treeview",
          background=[("selected", "#90caf9")])

read_owners()
root.mainloop()
