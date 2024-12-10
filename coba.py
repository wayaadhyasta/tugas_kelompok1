import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management with Class")
        
        # Koneksi ke MySQL
        self.conn = self.connect_db()
        
        # Membuat GUI
        self.create_gui()
        
        # Fetch data pertama
        self.fetch_items()
    
    def connect_db(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",  # Ganti sesuai user MySQL
                password="",  # Ganti sesuai password MySQL
                database="inventory_db"
            )
            return conn
        except Exception as e:
            messagebox.showerror("Database Error", f"Error connecting to database: {e}")
            self.root.destroy()
    
    def create_gui(self):
        # Frame Input
        frame_input = tk.Frame(self.root, padx=10, pady=10)
        frame_input.pack()

        tk.Label(frame_input, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_name = tk.Entry(frame_input, width=30)
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="jumlah barang:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_quantity = tk.Entry(frame_input, width=30)
        self.entry_quantity.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="Price:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_price = tk.Entry(frame_input, width=30)
        self.entry_price.grid(row=2, column=1, padx=5, pady=5)

        # Frame Tombol
        frame_buttons = tk.Frame(self.root, padx=10, pady=10)
        frame_buttons.pack()

        btn_add = tk.Button(frame_buttons, text="Add", command=self.add_item, width=10)
        btn_add.grid(row=0, column=0, padx=5)

        btn_update = tk.Button(frame_buttons, text="Update", command=self.update_item, width=10)
        btn_update.grid(row=0, column=1, padx=5)

        btn_delete = tk.Button(frame_buttons, text="Delete", command=self.delete_item, width=10)
        btn_delete.grid(row=0, column=2, padx=5)

        btn_clear = tk.Button(frame_buttons, text="Clear", command=self.clear_inputs, width=10)
        btn_clear.grid(row=0, column=3, padx=5)

        # Frame Tabel
        frame_table = tk.Frame(self.root, padx=10, pady=10)
        frame_table.pack()

        columns = ("ID", "Name", "Quantity", "Price")
        self.table = ttk.Treeview(frame_table, columns=columns, show="headings", height=8)
        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=100)

        self.table.pack(side=tk.LEFT)
        self.table.bind("<Double-1>", self.fill_form)

        scrollbar = tk.Scrollbar(frame_table, orient="vertical", command=self.table.yview)
        self.table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def fetch_items(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM items")
            rows = cursor.fetchall()
            for row in self.table.get_children():
                self.table.delete(row)
            for row in rows:
                self.table.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching data: {e}")
    
    def add_item(self):
        name = self.entry_name.get()
        jumlah_barang = self.entry_quantity.get()
        price = self.entry_price.get()
        if not (name and jumlah_barang and price):
            messagebox.showwarning("Input Error", "Semua field harus diisi!")
            return
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO items (name, jumlah_barang, price) VALUES (%s, %s, %s)", 
                           (name, int(jumlah_barang), float(price)))
            self.conn.commit()
            self.clear_inputs()
            self.fetch_items()
            messagebox.showinfo("Success", "Barang berhasil ditambahkan!")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")
    
    def update_item(self):
        selected = self.table.focus()
        if not selected:
            messagebox.showwarning("Selection Error", "Pilih data yang akan diupdate!")
            return
        values = self.table.item(selected, "values")
        id_ = values[0]
        name = self.entry_name.get()
        jumlah_barang = self.entry_quantity.get()
        price = self.entry_price.get()
        if not (name and jumlah_barang and price):
            messagebox.showwarning("Input Error", "Semua field harus diisi!")
            return
        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE items SET name=%s, jumlah_barang=%s, price=%s WHERE id=%s", 
                           (name, int(jumlah_barang), float(price), id_))
            self.conn.commit()
            self.clear_inputs()
            self.fetch_items()
            messagebox.showinfo("Success", "Barang berhasil diperbarui!")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")
    
    def delete_item(self):
        selected = self.table.focus()
        if not selected:
            messagebox.showwarning("Selection Error", "Pilih data yang akan dihapus!")
            return
        values = self.table.item(selected, "values")
        id_ = values[0]
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM items WHERE id=%s", (id_,))
            self.conn.commit()
            self.fetch_items()
            messagebox.showinfo("Success", "Barang berhasil dihapus!")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")
    
    def clear_inputs(self):
        self.entry_name.delete(0, tk.END)
        self.entry_quantity.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)
    
    def fill_form(self, event):
        selected = self.table.focus()
        if not selected:
            return
        values = self.table.item(selected, "values")
        self.entry_name.delete(0, tk.END)
        self.entry_quantity.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)
        self.entry_name.insert(0, values[1])
        self.entry_quantity.insert(0, values[2])
        self.entry_price.insert(0, values[3])

# Main Program
if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()
