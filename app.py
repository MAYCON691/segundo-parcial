from flask import Flask, session, render_template, redirect, url_for, request

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_sesion'

def inicializar_sesion():
    if 'productos' not in session:
        session['productos'] = []

@app.route('/')
def gestion_productos():
    inicializar_sesion()
    return render_template('index.html', productos=session['productos'])

@app.route('/nuevo_producto', methods=['POST'])
def nuevo_producto():
    inicializar_sesion()
    productos = session['productos']
    nuevo_id = len(productos) + 1
    producto = {
        'id': nuevo_id,
        'nombre': request.form['nombre'],
        'cantidad': int(request.form['cantidad']),
        'precio': float(request.form['precio']),
        'fecha_vencimiento': request.form['fecha_vencimiento'], 
        'categoria': request.form['categoria']
    }
    productos.append(producto)
    session['productos'] = productos
    return redirect(url_for('gestion_productos'))

@app.route('/eliminar/<int:id>')
def eliminar_producto(id):
    productos = session['productos']
    session['productos'] = [p for p in productos if p['id'] != id]
    return redirect(url_for('gestion_productos'))

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    productos = session['productos']
    producto = next((p for p in productos if p['id'] == id), None)
    
    if request.method == 'POST':
        producto['nombre'] = request.form['nombre']
        producto['cantidad'] = int(request.form['cantidad'])
        producto['precio'] = float(request.form['precio'])
        producto['fecha_vencimiento'] = request.form['fecha_vencimiento']  
        producto['categoria'] = request.form['categoria']
        session['productos'] = productos
        return redirect(url_for('gestion_productos'))
    
    return render_template('editar.html', producto=producto)

if __name__ == '__main__':
    app.run(debug=True)
