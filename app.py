from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
import mysql.connector
from datetime import timedelta
import os


app = Flask(__name__)
app.secret_key = 'G@1J5$*uTmPqDxLrJiSkB7E9H4nOqRvY0'
app.permanent_session_lifetime = timedelta(minutes=5)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'remidi'
}

conn = mysql.connector.connect(**db_config)

def get_mysql_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def get_users():
    try:
        connection = get_mysql_connection()
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
        return users
    except Exception as e:
        print(f"Error fetching users: {str(e)}")
        return []

def update_user(user_id, updated_username, updated_password, updated_role):
    try:
        try:
            user_id = int(user_id)
        except ValueError:
            print('Invalid user ID.')
            return False
        if not (updated_username and updated_password and updated_role):
            print('All fields must be filled out.')
            return False

        connection = get_mysql_connection()
        with connection.cursor() as cursor:
            query = "UPDATE users SET Username=%s, Password=%s, Role=%s WHERE ID=%s"
            cursor.execute(query, (updated_username, updated_password, updated_role, user_id))

        connection.commit()
        flash('User successfully updated.', 'success')
        return True
    except Exception as e:
        print(f"Error updating user: {str(e)}")
        flash('Error updating user. Please try again.', 'danger')
        return False
    finally:
        connection.close()


def update_product(product_id, updated_name, updated_price):
    try:
        connection = get_mysql_connection()
        cursor = connection.cursor()
        query = "UPDATE products SET name=%s, price=%s WHERE id=%s"
        cursor.execute(query, (updated_name, updated_price, product_id))
        connection.commit()
        return True
    except Exception as e:
        print(f"Error updating product: {str(e)}")
        return False
    finally:
        cursor.close()
        connection.close()


def get_product_by_id(product_id):
    try:
        connection = get_mysql_connection()
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
            product = cursor.fetchone()
        if not product:
            print(f"Product with ID {product_id} not found.")
    except Exception as e:
        print(f"Error getting product: {str(e)}")
        product = None
    finally:
        connection.close()
    return product


def delete_product_by_id(product_id):
    try:
        connection = get_mysql_connection()
        cursor = connection.cursor()
        query = "DELETE FROM products WHERE id = %s"
        cursor.execute(query, (product_id,))
        connection.commit()
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False
    finally:
        cursor.close()
        connection.close()



def get_user_by_id(user_id):
    connection = get_mysql_connection()
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
    connection.close()
    return user

def get_orders():
    connection = None
    try:
        connection = get_mysql_connection()
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM orders")
            orders = cursor.fetchall()
        return orders
    except Exception as e:
        print(f"Error in get_orders: {e}")
        return []
    finally:
        if connection and connection.is_connected():
            connection.close()

orders = get_orders()
print(orders)


   
def get_products():
    products = [
            {'id': 1, 'name': 'Komputer Gaming', 'price': 10000000, 'image_url': url_for('static', filename='img/komputer.jpg'),
     'specification': 'Prosesor: Intel Core i7, RAM: 16GB, GPU: NVIDIA GeForce RTX 3060'},
    {'id': 2, 'name': 'Komputer Gaming', 'price': 15000000, 'image_url': url_for('static', filename='img/komputer1.jpg'),
     'specification': 'Prosesor: AMD Ryzen 9 5900X, RAM: 32GB, GPU: NVIDIA GeForce RTX 3080'},
    {'id': 3, 'name': 'Monitor', 'price': 200000, 'image_url': url_for('static', filename='img/moni.jpg'),
     'specification': 'Ukuran Layar: 24 inch, Resolusi: 1920x1080'},
    {'id': 4, 'name': 'VGA', 'price': 10000000, 'image_url': url_for('static', filename='img/vga.jpeg'),
     'specification': 'GPU: AMD Radeon RX 6700 XT, VRAM: 12GB GDDR6'},
    {'id': 5, 'name': 'Komputer Kantor', 'price': 15000000, 'image_url': url_for('static', filename='img/komputerkantor.jpeg'),
     'specification': 'Prosesor: Intel Core i5, RAM: 8GB, Storage: 512GB SSD'},
    {'id': 6, 'name': 'Ram', 'price': 200000, 'image_url': url_for('static', filename='img/ram.jpeg'),
     'specification': 'Kapasitas: 16GB, DDR4, Kecepatan: 3200MHz'},
    {'id': 8, 'name': 'Ssd', 'price': 15000000, 'image_url': url_for('static', filename='img/ssd.jpg'),
     'specification': 'Kapasitas: 1TB, Interface: NVMe, Kecepatan Baca/Tulis: 3500/2500 MB/s'},
    {'id': 9, 'name': 'Motherboard', 'price': 200000, 'image_url': url_for('static', filename='img/mobo.jpeg'),
     'specification': 'Chipset: B450, Socket: AM4, Form Factor: ATX'},
    {'id': 10, 'name': 'Laptop Gaming', 'price': 10000000, 'image_url': url_for('static', filename='img/laptop.jpg'),
     'specification': 'Prosesor: Intel Core i7, RAM: 16GB, GPU: NVIDIA GeForce GTX 1660 Ti'},
    {'id': 11, 'name': 'Motherboard', 'price': 15000000, 'image_url': url_for('static', filename='img/asus.jpeg'),
     'specification': 'Chipset: Z590, Socket: LGA1200, Form Factor: ATX'},
    {'id': 12, 'name': 'Komputer Fullset', 'price': 200000, 'image_url': url_for('static', filename='img/fulset.jpg'),
     'specification': 'Prosesor: AMD Ryzen 5 3600, RAM: 16GB, GPU: NVIDIA GeForce GTX 1660 Super'},

    ]
    return products



@app.route('/products')
def products():
    if 'user' in session:
        products_data = get_products()
        return render_template('products.html', products=products_data) 
    else:
        flash('Silakan login terlebih dahulu.', 'info')
        return redirect(url_for('login'))
def get_product_by_id(product_id):
    products = get_products()
    for product in products:
        if product['id'] == product_id:
            return product
    return None
   
@app.route('/purchase/<int:product_id>')
def purchase(product_id):
    if 'user' in session:
        product = get_product_by_id(product_id)
        if product:
            return render_template('purchase.html', product=product)
        else:
            flash('Produk tidak ditemukan.', 'danger')
            return redirect(url_for('index'))
    else:
        flash('Silakan login terlebih dahulu.', 'info')
        return redirect(url_for('login'))
    
@app.route('/complete_purchase', methods=['POST'])
def complete_purchase():
    if 'user' in session:
        try:
            product_id = int(request.form.get('selectedProduct'))
            quantity = int(request.form.get('quantity'))
            buyer_name = request.form.get('buyer_name')
            shipping_address = request.form.get('shipping_address')
            buyer_email = request.form.get('buyer_email')            
            transaction_info = {
                'product_id': product_id,
                'quantity': quantity,
                'buyer_name': buyer_name,
                'shipping_address': shipping_address,
                'buyer_email': buyer_email
            }
            session['transaction_info'] = transaction_info
            return redirect(url_for('informasi'))
        except Exception as e:
            flash(f"Error: {str(e)}", 'danger')
            return redirect(url_for('products'))
    else:
        flash('Silakan login terlebih dahulu.', 'info')
        return redirect(url_for('login'))
    
@app.route('/informasi')
def informasi():
    transaction_info = session.get('transaction_info')
    if transaction_info:
        product_id = transaction_info.get('product_id')
        product = get_product_by_id(product_id)
        if product:
            return render_template('informasi.html', product=product, transaction_info=transaction_info)
        else:
            flash('Produk tidak ditemukan.', 'danger')
            return redirect(url_for('index'))
    else:
        flash('Informasi transaksi tidak ditemukan.', 'danger')
        return redirect(url_for('index'))

@app.route('/informasi-pembelian')
def informasi_pembelian():
    if 'user' in session:
        product = get_product_by_id(session.get('product_id'))
        if product:
            return render_template('informasi.html', product=product)
        else:
            flash('Produk tidak ditemukan.', 'danger')
            return redirect(url_for('index'))
    else:
        flash('Silakan login terlebih dahulu.', 'info')
        return redirect(url_for('login'))

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/admin')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/admin/products')
def admin_products():
    products = get_products()
    return render_template('admin_products.html', products=products)

@app.route('/admin/products/add', methods=['GET', 'POST'])
def admin_add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']        
        flash('Product added successfully.', 'success')
        return redirect(url_for('admin_products'))
    return render_template('admin_add_product.html')


@app.route('/admin/products/edit/<int:product_id>', methods=['GET', 'POST'])
def admin_edit_product(product_id):
    product = get_product_by_id(product_id)

    if product is None:
        flash('Produk tidak ditemukan.', 'danger')
        return redirect(url_for('admin_products'))

    if request.method == 'POST':
        try:
            updated_name = request.form.get('name')
            updated_price = request.form.get('price')

            if not all([updated_name, updated_price]):
                flash('Semua kolom harus diisi.', 'danger')
                return redirect(url_for('admin_edit_product', product_id=product_id))

            success = update_product(product_id, updated_name, updated_price)

            if success:
                flash('Produk berhasil diperbarui.', 'success')
                return redirect(url_for('admin_products'))  # Alihkan ke daftar produk

        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')

    return render_template('admin_edit_product.html', product=product, product_id=product_id)



@app.route('/admin/products/update/<int:product_id>', methods=['POST'])
def admin_update_product(product_id):
    try:
        updated_name = request.form.get('name')
        updated_price = request.form.get('price')
        if not all([updated_name, updated_price]):
            flash('All fields must be filled out.', 'danger')
            return redirect(url_for('admin_edit_product', product_id=product_id))
        success = update_product(product_id, updated_name, updated_price)
        if success:
            flash('Product updated successfully.', 'success')
        else:
            flash('Product not found or failed to update. Please try again.', 'danger')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')

    return redirect(url_for('admin_products'))




@app.route('/admin/products/delete/<int:product_id>', methods=['POST'])
def admin_delete_product(product_id):
    try:
        success = delete_product_by_id(product_id)
        if success:
            flash('Product deleted successfully.', 'success')
        else:
            flash('Product not found or failed to delete. Please try again.', 'danger')
    except Exception as e:
        print(f"Error: {str(e)}")
        flash('An error occurred while deleting the product. Please try again.', 'danger')
    return redirect(url_for('admin_products'))


@app.route('/admin/users')
def admin_users():
    try:
        users = get_users()
        return render_template('admin_users.html', users=users)
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return render_template('admin_users.html', users=[])

@app.route('/admin/users/edit/<int:user_id>', methods=['GET', 'POST'])
def admin_edit_user(user_id):
    try:
        user_id = int(user_id)
    except ValueError:
        flash('ID pengguna tidak valid.', 'danger')
        return redirect(url_for('admin_users'))

    try:
        user = get_user_by_id(user_id)
        if not user:
            flash('Pengguna tidak ditemukan.', 'danger')
            return redirect(url_for('admin_users'))

        if request.method == 'POST':
            updated_username = request.form.get('username')
            updated_password = request.form.get('password')
            updated_role = request.form.get('role')


            if not all([updated_username, updated_password, updated_role]):
                flash('Semua kolom harus diisi.', 'danger')
                return redirect(url_for('admin_edit_user', user_id=user_id))
            success = update_user(user_id, updated_username, updated_password, updated_role)
            if success:
                flash('Pengguna berhasil diperbarui.', 'success')
                return redirect(url_for('admin_users'))
            else:
                flash('Pengguna tidak ditemukan atau gagal diperbarui. Silakan coba lagi.', 'danger')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        print(f"Error updating user: {str(e)}")

    return render_template('admin_edit_user.html', user=user)
@app.route('/admin/users/delete/<int:user_id>', methods=['POST'])
def admin_delete_user(user_id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    try:
        delete_query = "DELETE FROM users WHERE id = %s"
        cursor.execute(delete_query, (user_id,))
        connection.commit()
        flash('User deleted successfully.', 'success')
    except Exception as e:
        flash(f'Error deleting user: {e}', 'error')
    finally:
        cursor.close()
        connection.close()
    return redirect(url_for('admin_users'))



@app.route('/admin/orders')
def admin_orders():
    orders = get_orders()
    return render_template('admin_orders.html', orders=orders)

@app.route('/admin/orders/change_status/<int:order_id>/<status>', methods=['POST'])
def admin_change_order_status(order_id, status):
    flash('Order status changed successfully.', 'success')
    return redirect(url_for('admin_orders'))

@app.route('/submit_order', methods=['POST'])
def submit_order():
    order_data = request.form.get('order_data')

    try:
        cursor = conn.cursor()
        insert_query = "INSERT INTO admin_orders (order_data) VALUES (%s)"
        cursor.execute(insert_query, (order_data,))
        conn.commit()
        cursor.close()
        return redirect(url_for('order_confirmation'))

    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
        return "Error occurred while processing the order", 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if 'user' in session:
            flash('Anda sudah login.', 'info')
            return redirect(url_for('index'))

        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            connection = get_mysql_connection()
            with connection.cursor(dictionary=True) as cursor:
                query = "SELECT * FROM users WHERE username = %s AND password = %s"
                cursor.execute(query, (username, password))
                user = cursor.fetchone()
            if user:
                session['user'] = user['username']
                if user['role'] == 'admin':
                    flash('Login berhasil sebagai admin.', 'success')
                    return redirect(url_for('admin_dashboard'))
                else:
                    flash('Login berhasil.', 'success')
                    return redirect(url_for('products'))
            else:
                flash('Username atau password salah.', 'danger')
    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'danger')
        print(f"MySQL Error: {err}")
        flash('Terjadi kesalahan. Silakan coba lagi.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        if 'user' in session:
            flash('Anda sudah login.', 'info')
            return redirect(url_for('index'))
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            connection = get_mysql_connection()
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
                connection.commit()
            flash('Registrasi berhasil. Anda sekarang login.', 'success')
            return redirect(url_for('login'))

    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'danger')
        return render_template('error.html')

    return render_template('register.html')


@app.route('/logout', methods=['POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        return redirect(url_for('login'))
    else:
        return 'Method Not Allowed', 405

 




if __name__ == '__main__':
    app.run(debug=True)
