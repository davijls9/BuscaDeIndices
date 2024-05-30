import json
import pdfkit
import os
from jinja2 import Environment, FileSystemLoader

# Função para carregar dados dos arquivos
def load_data(hyperparam_file, performance_file):
    try:
        with open(hyperparam_file, 'r', encoding='utf-8') as f:
            hyperparam_data = f.read()
        
        with open(performance_file, 'r', encoding='utf-8') as f:
            performance_data = f.readlines()
        
        tasks = []
        results = []

        # Processar dados de hiperparâmetros
        for block in hyperparam_data.split('\n\n'):
            if block.strip():  # Ignorar blocos vazios
                result = {}
                for line in block.split('\n'):
                    key, value = line.split(': ')
                    if 'Size' in key:  # Remover 'bytes' dos valores de tamanho
                        value = int(value.split()[0])
                    if 'Time' in key:  # Remover 'segundos' dos valores de tempo
                        value = float(value.split()[0])
                        key = 'average_search_time'  # Corrigir a chave para 'average_search_time'
                    result[key.lower().replace(' ', '_')] = value
                    
                results.append(result)
        print(result)
        # Processar dados de desempenho
        for line in performance_data:
            task = line.strip()
            if task:
                tasks.append(task)
        
        return tasks, results
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return [], []

# Função para gerar relatório detalhado
def generate_report(tasks, results, output_pdf):
    try:
        # Carregar template HTML
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template('template.html')

        # Renderizar template com dados
        html_out = template.render(tasks=tasks, results=results)

        # Configurar opções do pdfkit
        options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': 'UTF-8',
            'custom-header': [
                ('Accept-Encoding', 'gzip')
            ],
            'no-outline': None
        }

        # Configurar o caminho para o executável do wkhtmltopdf
        wkhtmltopdf_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'  # Exemplo de caminho padrão no Windows
        if os.path.isfile(wkhtmltopdf_path):
            config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
        else:
            raise FileNotFoundError("Executável do wkhtmltopdf não encontrado.")

        # Converter HTML para PDF
        pdfkit.from_string(html_out, output_pdf, options=options, configuration=config)
    except Exception as e:
        print(f"Erro ao gerar relatório: {e}")
        
# Definir caminhos dos arquivos
hyperparam_file = 'hyperparameter_analysis.txt'
performance_file = 'performance_metrics.txt'
output_pdf = 'relatorio_detalhado.pdf'

# Carregar dados dos arquivos
tasks, results = load_data(hyperparam_file, performance_file)
# Gerar relatório PDF
generate_report(tasks, results, output_pdf)
print(f"Relatório gerado: {output_pdf}")
