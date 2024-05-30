# Motor de Busca - WebCrawler

Este projeto implementa um motor de busca básico utilizando arquivos JSON para armazenamento de índices e vocabulário. O projeto inclui funcionalidades de web crawling, limpeza de dados, análise léxica, stemming, indexação e busca. Além disso, há uma análise de hiperparâmetros para ajustar o desempenho da indexação e busca.

## Estrutura do Projeto
Motor_de_busca-WebCrawler/<br>
├── sites_visitados/<br>
│ ├── site1.txt<br>
│ ├── site2.txt<br>
│ ├── site3.txt<br>
│ └── ...<br>
└───────────────────────────── <br>
BuscaDeIndices/<br>
├── LICENSE<br>
├── .gitignore<br>
├── README.md<br>
├── index_geral.json<br>
├── vocab_geral.json<br>
├── tuple_format.json<br>
├── list_geral.json<br>
├── vocab_geral.json<br>
├── hyperparameter_analysis.txt<br>
├── hyperparametro_progress.txt<br>
├── performance_metrics.txt<br>
├── template.html<br>
├── Busca_de_indice_e_Consulta.ipynb<br>
├── analise_de_hiperparametro.ipynb<br>
├── Carregando_arquivos.ipynb<br>
├── Limpeza_e_transformacao.ipynb<br>
├── template.html<br>
└── relatorio.py<br>

## Funcionalidades

### 1. Coleta de Dados (Web Crawling)

Os documentos são coletados a partir de sites especificados e salvos no diretório `sites_visitados/`.

### 2. Limpeza e Transformação de Dados

Os dados coletados passam por um processo de limpeza que inclui:
- Remoção de caracteres especiais
- Conversão para UTF-8
- Remoção de stopwords

### 3. Análise Léxica e Stemming

Os textos são analisados lexicamente e as palavras são reduzidas à sua forma raiz (stemming).

### 4. Indexação

Os documentos são indexados, criando dois arquivos principais:
- `index_geral.json`: Contém o índice invertido dos documentos.
- `vocab_geral.json`: Contém o vocabulário geral dos documentos.

### 5. Análise de Hiperparâmetros

Uma análise de hiperparâmetros é realizada para determinar o melhor tamanho de chunk para indexação e busca, resultando em:
- `hyperparameter_analysis.txt`: Contém os resultados da análise de hiperparâmetros.
- `hyperparametro_progress.txt`: Contém o progresso da análise de hiperparâmetros.

### 6. Medição de Desempenho

O desempenho do sistema é medido em termos de:
- Tempo de busca
- Espaço para indexação
- Tamanho dos índices

Os resultados são armazenados em `performance_metrics.txt`.

### 7. Relatório

Um relatório detalhado é gerado descrevendo as tarefas realizadas e os resultados obtidos.

## Contribuições

Contribuições são bem-vindas! Por favor, abra uma issue ou envie um pull request com suas melhorias.

## Licença

Este projeto está licenciado sob a Licença GNU 3 - veja o arquivo LICENSE.md para detalhes.

## Contato
Autor: Davi J L Santos
Email: davi.jls@outlook.com


Esse README oferece uma visão geral completa do projeto, incluindo estrutura, funcionalidades, requisitos, instalação e execução. Sinta-se à vontade para personalizá-lo conforme necessário.
