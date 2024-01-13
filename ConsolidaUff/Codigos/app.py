import os
import pdfquery
import openpyxl
from flask import Flask, request, render_template, send_file, redirect, url_for
import shutil
import threading
import webbrowser

app = Flask(__name__)

# Comando para esvaziar a pasta de PDFs
def empty_pdfs_folder(pdfs_directory):
    for filename in os.listdir(pdfs_directory):
        file_path = os.path.join(pdfs_directory, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
    print("Pasta 'pdfs' esvaziada.")
    
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_files = request.files.getlist('pdf_file')

        directory_path = os.path.dirname(os.path.abspath(__file__))
        pdfs_directory = os.path.join(directory_path, 'pdfs')
        excel_filename = "Modelo.xlsx"
        excel_path = os.path.join(directory_path, excel_filename)
        
        # Definir as coordenadas dos elementos desejados
        coordinates = [
            {'left': 200.0, 'top': 549.52, 'width': 16.68, 'height': 10.0},    # Coordenadas do final do número de empenho
            {'left': 41.0, 'top': 418.52, 'width': 374.62, 'height': 10.0},    # Coordenadas do fornecedor (nome e CNPJ) da nota de empenho
            {'left': 421.0, 'top': 642.52, 'width': 50.02, 'height': 10.0},    # Coordenadas do valor da nota de empenho
            {'left': 200.0, 'top': 464.52, 'width': 139.57, 'height': 10.0},   #Coordenadas do número do processo
            {'left': 200.0, 'top': 503.52, 'width': 56.7, 'height': 10.0},     # Coordenadas da fonte de despesa
            {'left': 43.0, 'top': 627.52, 'width': 387.29, 'height': 10.0},    # Coordenadas da natureza da despesa
            {'left': 125.0, 'top': 306.52, 'width': 122.66, 'height': 10.0} ,   # Modalidade da licitação
            {'left': 122.0, 'top': 503.52, 'width': 33.36, 'height': 10.0} ,   # Coordenadas do PTRES        
            {'left': 296.0, 'top': 503.52, 'width': 33.36, 'height': 10.0} ,   # Coordenadas do nº da natureza da despesa
            {'left': 485.0, 'top': 503.52, 'width': 73.88, 'height': 10.0} ,   # Coordenadas do plano interno
 
        ]
        
        copied_filename = "Consolidado.xlsx"
        copy_path = os.path.join(directory_path, copied_filename)
        shutil.copy(excel_path, copy_path)
        print('Cópia da pasta modelo do excel criada')

        copied_workbook = openpyxl.load_workbook(copy_path)
        copied_sheet = copied_workbook.active
        print('Excel aberto para inserção dos dados')

        start_row = 2

        for i, pdf_file in enumerate(uploaded_files):
            pdf_path = os.path.join(pdfs_directory, pdf_file.filename)
            pdf_file.save(pdf_path)
            
            pdf = pdfquery.PDFQuery(pdf_path)
            pdf.load()

            for j, coord in enumerate(coordinates):
                target_left = coord['left']
                target_top = coord['top']
                target_width = coord['width']
                target_height = coord['height']
                
                element = pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (target_left, target_top, target_left + target_width, target_top + target_height))
                text = element.text().strip()
                copied_sheet.cell(row=start_row + i, column=j+1).value = text
                

        copied_workbook.save(copy_path)
        copied_workbook.close()
        print("Dados inseridos na planilha.")

        return redirect(url_for('download_excel'))

    return render_template('index.html')
@app.route('/download_excel', methods=['GET'])
def download_excel():
    print('Download iniciado')
    directory_path = os.path.dirname(os.path.abspath(__file__))
    copied_filename = "Consolidado.xlsx"
    copied_path = os.path.join(directory_path, copied_filename)
    return send_file(copied_path, as_attachment=True)


if __name__ == '__main__':
    
    # Esvaziar a pasta pdfs antes de iniciar o servidor
    directory_path = os.path.dirname(os.path.abspath(__file__))
    pdfs_directory = os.path.join(directory_path, 'pdfs')
    empty_pdfs_folder(pdfs_directory)
    
    # Abre automaticamente o navegador ao executar o programa
    webbrowser.open('http://localhost:5000') 
    print('Servidor iniciado na porta http://localhost:5000 !') 

    # Iniciar o servidor Flask em um thread separado
    flask_thread = threading.Thread(target=app.run)
    flask_thread.start()
    flask_thread.join()
    
