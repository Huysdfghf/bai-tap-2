import tkinter as tk
from tkinter import messagebox
import psycopg2

class BookStoreApp:
    def __init__(self, master):
        self.master = master
        master.title("Quản Lý Cửa Hàng Sách")

        self.login_frame = tk.Frame(master)
        self.login_frame.pack()

        self.username_label = tk.Label(self.login_frame, text="Tên Người Dùng:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.pack()

        self.password_label = tk.Label(self.login_frame, text="Mật Khẩu:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.login_frame, show='*')
        self.password_entry.pack()

        self.login_button = tk.Button(self.login_frame, text="Đăng Nhập", command=self.login)
        self.login_button.pack()

        self.register_button = tk.Button(self.login_frame, text="Đăng Ký", command=self.register)
        self.register_button.pack()

        # Kết nối cơ sở dữ liệu
        self.conn = self.connect_to_database()

    def connect_to_database(self):
        conn = psycopg2.connect(
        database="demodb", 
        user="postgres", 
        password="200418", 
        host="127.0.0.1", 
        port="5432"
    )
    

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Kiểm tra thông tin đăng nhập
        if self.conn is not None:
            try:
                cur = self.conn.cursor()
                cur.execute("SELECT * FROM KhachHang WHERE TenKhachHang = %s AND SDT = %s", (username, password))
                customer = cur.fetchone()

                cur.execute("SELECT * FROM NhanVien WHERE TenNhanVien = %s AND SDTNhanVien = %s", (username, password))
                employee = cur.fetchone()

                if customer:
                    self.show_customer_dashboard()
                elif employee:
                    self.show_employee_dashboard()
                else:
                    messagebox.showerror("Lỗi", "Thông tin đăng nhập không hợp lệ")
                cur.close()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi đăng nhập: {e}")

    
    
     
    def register(self):
        # Thực hiện logic đăng ký
        messagebox.showinfo("Đăng Ký", "Chức năng đăng ký sẽ ở đây.")

    def show_customer_dashboard(self):
        self.login_frame.pack_forget()  # Ẩn khung đăng nhập
        customer_frame = tk.Frame(self.master)
        customer_frame.pack()
        
        tk.Label(customer_frame, text="Chào Mừng đến với Bảng Điều Khiển Khách Hàng").pack()
        tk.Button(customer_frame, text="Xem Sách Đã Mua", command=self.view_purchases).pack()
        tk.Button(customer_frame, text="Đăng Xuất", command=lambda: self.logout(customer_frame)).pack()

    
    def show_employee_dashboard(self):
        self.login_frame.pack_forget()  # Ẩn khung đăng nhập
        employee_frame = tk.Frame(self.master)
        employee_frame.pack()
        
        tk.Label(employee_frame, text="Chào Mừng đến với Bảng Điều Khiển Nhân Viên").pack()
        tk.Button(employee_frame, text="Thêm Sách Mới", command=self.add_book).pack()
        tk.Button(employee_frame, text="Ghi Nhận Bán Hàng", command=self.record_sale).pack()
        tk.Button(employee_frame, text="Đăng Xuất", command=lambda: self.logout(employee_frame)).pack()

    def view_purchases(self):
        # Lấy và hiển thị lịch sử mua hàng của khách hàng
        messagebox.showinfo("Mua Hàng", "Hiển thị sách đã mua ở đây.")

    def add_book(self):
        # Thực hiện logic thêm sách
        messagebox.showinfo("Thêm Sách", "Chức năng thêm sách sẽ ở đây.")

    def record_sale(self):
        # Thực hiện logic ghi nhận doanh số
        messagebox.showinfo("Ghi Nhận Bán Hàng", "Chức năng ghi nhận bán hàng sẽ ở đây.")

    def logout(self, frame):
        frame.pack_forget()  # Ẩn bảng điều khiển hiện tại
        self.login_frame.pack()  # Hiển thị lại khung đăng nhập

    def close(self):
        if self.conn:
            self.conn.close()
            print("Đã đóng kết nối đến cơ sở dữ liệu.")

if __name__ == "__main__":
    root = tk.Tk()
    app = BookStoreApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close)  # Đảm bảo kết nối được đóng khi thoát
    root.mainloop()
