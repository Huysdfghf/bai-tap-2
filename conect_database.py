import psycopg2
import random
def create_table_if_not_exists(cur, create_table_query):
    # Lệnh kiểm tra xem bảng đã tồn tại chưa
    table_name = create_table_query.split()[2]  # Lấy tên bảng từ câu lệnh tạo bảng
    cur.execute(f'''
        SELECT EXISTS (
            SELECT 1 
            FROM information_schema.tables 
            WHERE table_name = '{table_name}'
        );
    ''')
    exists = cur.fetchone()[0]
    
    # Nếu bảng chưa tồn tại, thực hiện tạo bảng
    if not exists:
        cur.execute(create_table_query)
        print(f"Table {table_name} created successfully")
    else:
        print(f"Table {table_name} already exists")



def insert_data(cur):
    # Chèn một tài khoản nhân viên
    cur.execute('''
        INSERT INTO NhanVien (TenNhanVien, SDTNhanVien) 
        VALUES ('nguyenvana', '0123456789');
    ''')

    # Chèn 2 tài khoản khách hàng
    cur.execute('''
        INSERT INTO KhachHang (TenKhachHang, SDT) 
        VALUES 
        ('Trần Thị B', '0987654321'),
        ('Lê Văn C', '0123456780');
    ''')

    # Chèn 4 tác giả
    cur.execute('''
        INSERT INTO TacGia (TenTacGia) 
        VALUES 
        ('Nguyễn Văn X'),
        ('Nguyễn Văn B'),
        ('Nguyễn Văn C'),
        ('Nguyễn Văn D');
    ''')

    # Chèn 3 nhà xuất bản
    cur.execute('''
        INSERT INTO NXB (TenNXB, SDTNXB) 
        VALUES 
        ('NXB ABC', '0123456789'),
        ('NXB AAB', '0223456789'),
        ('NXB AAA', '0323456789');
    ''')

    # Chèn 10 sản phẩm với IDTacGia, IDNXB ngẫu nhiên
    for i in range(1, 11):
        id_tacgia = random.randint(1, 4)  # Giả sử có 4 tác giả
        id_nxb = random.randint(1, 3)     # Giả sử có 3 nhà xuất bản
        cur.execute(f'''
            INSERT INTO SanPham (TenSanPham, GiaBan, IDTacGia, IDNXB, IDNhanVien) 
            VALUES ('Sản phẩm {i}', {i * 100}, {id_tacgia}, {id_nxb}, 1);
        ''')

    # Chèn 5 kho hàng với sản phẩm ngẫu nhiên
    for i in range(1, 6):
        id_sanpham = random.randint(1, 10)  # Giả sử có 10 sản phẩm
        soluong = random.randint(50, 200)   # Số lượng ngẫu nhiên từ 50 đến 200
        cur.execute(f'''
            INSERT INTO KhoHang (TenKhoHang, DiaChi, NgayNhapSP, IDSanPham, SoLuong) 
            VALUES ('Kho {i}', 'Địa chỉ {i}', CURRENT_DATE, {id_sanpham}, {soluong});
        ''')



try:
    # Kết nối với cơ sở dữ liệu
    conn = psycopg2.connect(
        database="demodb", 
        user="postgres", 
        password="200418", 
        host="127.0.0.1", 
        port="5432"
    )
    print("Opened database successfully")

    # Tạo con trỏ
    cur = conn.cursor()

    # Câu lệnh tạo bảng
    create_queries = [
    '''CREATE TABLE NhanVien
    (
        IDNhanVien SERIAL PRIMARY KEY NOT NULL,
        TenNhanVien TEXT,
        SDTNhanVien CHAR(15)
    );''',

    '''CREATE TABLE TacGia
    (
        IDTacGia SERIAL PRIMARY KEY NOT NULL,
        TenTacGia TEXT NOT NULL
    );''',

    '''CREATE TABLE NXB
    (
        IDNXB SERIAL PRIMARY KEY NOT NULL,
        TenNXB TEXT NOT NULL,
        SDTNXB CHAR(15)
    );''',

    '''CREATE TABLE KhachHang
    (
        MaKhachHang SERIAL PRIMARY KEY NOT NULL,
        TenKhachHang TEXT,
        SDT CHAR(15) UNIQUE
    );''',  # Tạo bảng KhachHang trước bảng HoaDon

    '''CREATE TABLE SanPham
    (
        IDSanPham SERIAL PRIMARY KEY NOT NULL,
        TenSanPham TEXT NOT NULL,
        GiaBan REAL,
        IDNhanVien INT REFERENCES NhanVien(IDNhanVien) ON DELETE SET NULL ON UPDATE CASCADE,
        IDTacGia INT REFERENCES TacGia(IDTacGia) ON DELETE SET NULL ON UPDATE CASCADE,
        IDNXB INT REFERENCES NXB(IDNXB) ON DELETE SET NULL ON UPDATE CASCADE
    );''',

    '''CREATE TABLE HoaDon
    (
        MaHoaDon SERIAL PRIMARY KEY NOT NULL,
        SoLuong INT,
        NgayBanSP DATE,
        TongTien NUMERIC,  -- Thêm cột TongTien để lưu tổng tiền
        IDSanPham INT REFERENCES SanPham(IDSanPham) ON DELETE CASCADE ON UPDATE CASCADE,
        SDT CHAR(15),  -- Chỉ định kiểu dữ liệu cho cột SDT
        FOREIGN KEY (SDT) REFERENCES KhachHang(SDT) ON DELETE CASCADE ON UPDATE CASCADE  -- Ràng buộc khóa ngoại cho cột SDT
    );''',

    '''CREATE TABLE KhoHang (
        IDKho SERIAL PRIMARY KEY,
        TenKhoHang TEXT,
        DiaChi TEXT,
        NgayNhapSP DATE,
        IDSanPham INT REFERENCES SanPham(IDSanPham) ON DELETE SET NULL ON UPDATE CASCADE,
        SoLuong INT NOT NULL
    );''',
]

# Tiến hành tạo bảng và chèn dữ liệu


    # Tạo các bảng nếu chưa tồn tại
    for query in create_queries:
        create_table_if_not_exists(cur, query)

    # Chèn dữ liệu vào các bảng
    insert_data(cur)

    # Commit thay đổi và đóng kết nối
    conn.commit()
    cur.close()
    conn.close()

except Exception as e:
    print(f"An error occurred: {e}")
