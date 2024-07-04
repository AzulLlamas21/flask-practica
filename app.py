from flask import Flask, render_template, make_response
import matplotlib
matplotlib.use('Agg')  # Usar el backend 'Agg' de Matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
import base64
import weasyprint

app = Flask(__name__)

# Datos de productos de la tienda OXXO
productos_oxxo = [
    {"id": 1, "nombre": "Refresco Coca-Cola", "precio": "$15.00"},
    {"id": 2, "nombre": "Papas Sabritas", "precio": "$10.50"},
    {"id": 3, "nombre": "Agua Ciel", "precio": "$8.00"},
    {"id": 4, "nombre": "Barritas Marinela", "precio": "$7.50"},
    {"id": 5, "nombre": "Chocolate Hershey's", "precio": "$12.75"}
]

# Datos ficticios de productos más vendidos
datos_productos_mas_vendidos = {
    'Refresco Coca-Cola': 1200,
    'Papas Sabritas': 900,
    'Agua Ciel': 800,
    'Chocolate Hershey\'s': 750,
    'Barritas Marinela': 700
}

# Datos ficticios de ventas mensuales
datos_ventas_mensuales = {
    'Enero': 25000,
    'Febrero': 28000,
    'Marzo': 30000,
    'Abril': 32000,
    'Mayo': 35000
}

def generar_grafico_ventas_mensuales():
    # Datos para el gráfico
    meses = list(datos_ventas_mensuales.keys())
    values = list(datos_ventas_mensuales.values())

    # Crear gráfico
    plt.figure(figsize=(10, 5))
    plt.plot(meses, values, marker='o')
    plt.title('Ventas Mensuales')
    plt.xlabel('Meses')
    plt.ylabel('Total Ventas ($)')
    plt.grid(True)

    # Guardar gráfico en memoria
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close()
    
    return img_base64

def generar_grafico_productos_mas_vendidos():
    # Datos para el gráfico
    productos = list(datos_ventas_mensuales.keys())
    ventas = list(datos_ventas_mensuales.values())

    # Crear gráfico de productos más vendidos
    plt.figure(figsize=(10, 5))
    plt.bar(productos, ventas, color='blue')
    plt.title('Productos Más Vendidos')
    plt.xlabel('Productos')
    plt.ylabel('Cantidad Vendida')
    plt.xticks(rotation=45)

    # Guardar gráfico en memoria
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close()
    
    return img_base64

@app.route('/')
def index():
    return render_template('index.html', titulo='OXXO', productos=productos_oxxo)

@app.route('/dashboard')
def dashboard():
    img_data = generar_grafico_ventas_mensuales()
    return render_template('dashboard.html', img_data=img_data, titulo='Ventas Mensuales', datos=datos_ventas_mensuales)

@app.route('/new_dashboard')
def new_dashboard():
    img_data = generar_grafico_productos_mas_vendidos()
    return render_template('new_dashboard.html', img_data=img_data, titulo='Productos Más Vendidos', datos=datos_productos_mas_vendidos)

@app.route('/report_dashboard')
def report_dashboard():
    # Generar PDF para el dashboard de ventas mensuales
    template = render_template('dashboard.html', img_data=generar_grafico_ventas_mensuales(),
                               titulo='Ventas Mensuales', datos=datos_ventas_mensuales)

    pdf = weasyprint.HTML(string=template).write_pdf()
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=reporte_dashboard.pdf'
    return response

@app.route('/report_new_dashboard')
def report_new_dashboard():
    # Generar PDF para el dashboard de productos más vendidos
    template = render_template('new_dashboard.html', img_data=generar_grafico_productos_mas_vendidos(),
                               titulo='Productos Más Vendidos', datos=datos_productos_mas_vendidos)

    pdf = weasyprint.HTML(string=template).write_pdf()
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=reporte_new_dashboard.pdf'
    return response

if __name__ == '__main__':
    app.run(debug=True)
    
    