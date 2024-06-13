import streamlit as st
import time
import re
import json
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from tqdm import tqdm
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer


"""
Sobre o codigo

Este código é um exemplo avançado de como usar o Streamlit junto com técnicas de processamento de linguagem natural (NLP) e machine learning para criar uma aplicação de busca eficiente. O código integra a preparação de dados textuais, cálculos de TF-IDF, e utiliza índices invertidos para realizar buscas rápidas e eficazes.

### Descrição dos Principais Componentes

#### 1. **Configuração Inicial**
- O código usa `streamlit` como interface gráfica para interação do usuário, `nltk` para processamento de texto, e `sklearn` para calcular TF-IDF.
- Utiliza `tqdm` para barra de progresso, mostrando o status de operações que podem ser demoradas.

#### 2. **Preparação e Download de Recursos do NLTK**
- **setup_nltk**: Configura recursos de NLP como stopwords e stemmers necessários para preprocessamento de texto em português. A função verifica se os recursos já estão disponíveis localmente e os baixa se necessário.
  
#### 3. **Funções de Processamento de Texto**
- **clean_text**: Realiza a limpeza básica do texto, removendo caracteres especiais e convertendo tudo para minúsculas. Também remove stopwords para reduzir ruídos e melhorar a eficácia da indexação.
- **apply_stemming**: Aplica a técnica de stemming para reduzir as palavras a suas raízes, permitindo que variantes da mesma palavra sejam associadas como equivalentes.
- **preprocess_query**: Combina limpeza e stemming para preparar as consultas de busca.

#### 4. **Funções de Busca**
- **search_query**: Implementa uma busca utilizando um índice invertido carregado, otimizando a consulta de grandes volumes de dados.
- **search_query_tfidf**: Utiliza o vetorizador TF-IDF para transformar documentos e consultas, e calcula a similaridade entre eles para identificar os documentos mais relevantes.

#### 5. **Apresentação dos Resultados**
- **display_results_with_scores**: Mostra os domínios mais relevantes com frequências e pontuações calculadas com base na frequência de ocorrência e no tempo de busca.
- **display_results_with_scores_tfidf**: Especificamente para resultados TF-IDF, exibe os arquivos e suas pontuações correspondentes.

### Funcionamento do Código

- **Inicialização**: Ao executar, o código tenta configurar e verificar todos os recursos necessários.
- **Interface do Usuário**: Utiliza Streamlit para capturar a entrada do usuário (consulta de texto) e oferece botões para escolher entre diferentes métodos de busca (TF-IDF ou índice invertido).
- **Processo de Busca**: Após a entrada do usuário, a consulta é preprocessada e utilizada para buscar documentos relevantes, seja por TF-IDF ou pelo índice invertido.
- **Exibição de Resultados**: Os resultados são exibidos diretamente na interface do Streamlit, permitindo uma interação visual e fácil de entender.

### Benefícios e Uso

- **Versatilidade e Eficiência**: A combinação de várias técnicas de NLP e métodos de indexação torna o sistema altamente eficiente para recuperar informações de grandes conjuntos de dados.
- **Interface Amigável**: O uso de Streamlit torna a aplicação acessível até para usuários sem conhecimento técnico profundo, permitindo que realizem buscas complexas com facilidade.
- **Aplicações**: Ideal para ambientes empresariais, educacionais ou de pesquisa, onde a busca rápida e precisa de documentos é essencial.

Este código é um exemplo prático de como técnicas modernas de NLP podem ser integradas em aplicações reais, utilizando bibliotecas populares e frameworks para criar uma ferramenta poderosa de busca e análise de dados.

"""

print("Iniciando a aplicação...")

def setup_nltk():
    try:
        print("Configurando stopwords e stemmer...")
        nltk.download("stopwords")
        nltk.download("rslp")
        nltk.download("punkt")

        stop_words = set(stopwords.words("portuguese"))
        stemmer = RSLPStemmer()
        print("Recursos do NLTK configurados com sucesso.")
    except Exception as e:
        st.error(f"Erro ao baixar os recursos NLTK: {e}")
        print(f"Erro ao configurar os recursos NLTK: {e}")

# Tentar carregar os recursos do NLTK e baixar se necessário
try:
    print("Baixando recursos do NLTK...")
    setup_nltk()
    stop_words = set(stopwords.words('portuguese'))
    stemmer = RSLPStemmer()
    print("Recursos do NLTK baixados com sucesso.")
except Exception as e:
    st.write(f"Erro ao baixar os recursos NLTK: {e}")
    print(f"Erro ao baixar os recursos NLTK: {e}")

# Funções de preprocessamento
# Funções de preprocessamento
def clean_text(text):
    if not isinstance(text, str):
        raise ValueError("O texto de entrada deve ser uma string.")
    
    print("Limpando texto...")
    text = re.sub(r"[^\w\s]", " ", str(text))  # Remove special characters
    text = text.lower()  # Convert to lowercase
    tokens = text.split()
    tokens = [word for word in tokens if word not in stop_words]  # Remove stopwords
    cleaned_text = " ".join(tokens)
    
    print("Texto limpo:", cleaned_text)
    return cleaned_text

def apply_stemming(text):
    if not isinstance(text, str):
        raise ValueError("O texto de entrada deve ser uma string.")
    
    print("Aplicando stemming...")
    tokens = nltk.word_tokenize(str(text), language="portuguese")
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    stemmed_text = " ".join(stemmed_tokens)
    
    print("Stemming aplicado:", stemmed_text)
    return stemmed_text

def preprocess_query(query):
    if not isinstance(query, str):
        raise ValueError("A query de entrada deve ser uma string.")
    
    print("Pré-processando query...")
    cleaned_query = clean_text(query)
    stemmed_query = apply_stemming(cleaned_query)
    
    print("Query pré-processada:", stemmed_query)
    return stemmed_query


# Funções da pesquisa normal

def extract_domain(file_name):
    #print("Extraindo o domonio")
    parts = file_name.split("]")
    if len(parts) > 0:
        domain = parts[0].replace("_", ".")
        return domain
    #print("Fim da extração do domonio")
    return None


def calculate_score(frequency, search_time):
    # Defina os pesos para frequência e tempo de busca
    frequency_weight = 0.7
    time_weight = 0.3

    # Calcule o score ponderado
    score = (frequency * frequency_weight) - (search_time * time_weight)
    return score


def display_results_with_scores(result_files, search_time):
    from collections import Counter

    domain_counter = Counter()
    for file in result_files:
        domain = extract_domain(file)
        if domain:
            domain_counter[domain] += 1

    # Criar lista para dataframe
    data = []
    for domain, frequency in domain_counter.most_common():
        score = calculate_score(frequency, search_time)
        data.append({"Site": domain, "Frequency": frequency, "Score(ms acumulado)": score, "Tempo de pesquisa": search_time})

    # Criar DataFrame
    df = pd.DataFrame(data)
    df.set_index("Site", inplace=True)  # Configura a coluna 'Site' como índice se desejado

    # Exibir tabela
    st.table(df)
    
# Função de pesquisa com índice invertido
def search_query(query, vocab_geral, index_geral):
    print("Iniciando busca com índice invertido...")
    start_time = time.time()

    query_terms = preprocess_query(query).split()
    query_terms = list(set(query_terms))

    word_ids = []
    for term in query_terms:
        if term in vocab_geral:
            word_ids.append(vocab_geral[term])

    result_files = set()
    for word_id in word_ids:
        word_id = str(word_id)
        if word_id in index_geral:
            result_files.update(index_geral[word_id]["file_names"])

    end_time = time.time()
    search_time = end_time - start_time

    print(f"Busca com índice invertido concluída em {search_time:.2f} segundos.")
    return list(set(result_files)), search_time








# Função de pesquisa TF-IDF

def load_document(file_path):
    print("Carregando os documentos")
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
    cleaned_text = clean_text(text)
    stemmed_text = apply_stemming(cleaned_text)
    print("Documentos carregados com sucesso")
    return stemmed_text

@st.cache(allow_output_mutation=True)
def get_documents(index_geral):
    print("Carregando os documentos")
    documents = set()  # Usar um set para evitar duplicatas
    doc_ids = set()  # Usar um set para IDs

    if not index_geral:
        print("O índice geral está vazio.")
        return list(documents), list(doc_ids)

    for word_id, data in tqdm(index_geral.items(), desc="Loading documents"):
        if 'doc_info' in data and 'file_names' in data and data['file_names']:
            for doc_id in data["doc_info"]:
                doc_ids.add(doc_id)
                documents.add(str(data["file_names"][0]))
        else:
            print(f"Falta de dados para o word_id {word_id}.")

    print("Documentos carregados com sucesso")
    return list(documents), list(doc_ids)


def remove_floats_from_list(lst):
    return [item for item in lst if not isinstance(item, float)]

def search_query_tfidf(query, index_geral):
    print("Carregando os documentos")
    documents = []
    doc_ids = []
    for word_id, data in index_geral.items():
        for doc_id in data["doc_info"]:
            doc_ids.append(doc_id)
            # Concatenate file names into a single string
            documents.append(" ".join(data["file_names"]))

    print("Iniciando busca TF-IDF...")
    
    start_time = time.time()

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)
    query_vector = vectorizer.transform([query])

    scores = (tfidf_matrix * query_vector.T).toarray().flatten()

    # Adicionar barra de progresso
    sorted_scores_idx = tqdm(
        scores.argsort()[::-1], desc="Calculating Scores", unit="doc"
    )

    sorted_scores = [
        (documents[i], scores[i]) for i in sorted_scores_idx if scores[i] > 0
    ]

    end_time = time.time()
    search_time = end_time - start_time

    print(f"Busca TF-IDF concluída em {search_time:.2f} segundos.")
    return list(set(sorted_scores)), search_time



def display_results_with_scores_tfidf(sorted_scores, search_time):
    st.write(f"{'Site':<200}{'Score':<110}")
    st.write("=" * 210)
    for file_name, score in sorted_scores:
        st.write(f"{file_name:<200}{score:<110.4f}")

    st.write(f"\nSearch completed in {search_time:.2f} seconds")




# Carregar dados com cache
@st.cache(allow_output_mutation=True)
def load_data():
    with open('cleaned_vocab_geral.json', 'r', encoding='utf-8') as f:
        vocab_geral = json.load(f)
    with open('cleaned_index_geral.json', 'r', encoding='utf-8') as f:
        index_geral = json.load(f)
    return vocab_geral, index_geral



def main():
    st.title("Central de Pesquisa")
    query = st.text_input("Digite sua query de pesquisa")

    if st.button("Buscar com TF-IDF"):
        if query:
            st.write(f"Carregando dados.")
            vocab_geral, index_geral = load_data()
            st.write(f"Fim do carregando dados.")
            
                        # TF-IDF Search
            st.write(f"Fazendo pesquisa.")
            # Verifica se cada documento é uma string e não está vazio
            preprocessed_query = preprocess_query(query)
            sorted_scores_tfidf, search_time_tfidf = search_query_tfidf(
                preprocessed_query, index_geral
            )
            st.write(f"Fim da pesquisa.")
            
            st.write("TF-IDF Results:")
            search_query_tfidf(sorted_scores_tfidf, search_time_tfidf)

    if st.button("Buscar com Índice Invertido"):
        if query:
            st.write(f"Carregando dados.")
            vocab_geral, index_geral = load_data()
            st.write(f"Fim do carregando dados.")
            
            st.write(f"Fazendo pesquisa.")
            result_files, search_time = search_query(query, vocab_geral, index_geral)
            st.write(f"Fim da pesquisa.")

            st.write(f"Query que foi feita: {query}\n")
            display_results_with_scores(result_files, search_time)
            st.write(f"\nSearch completed in {search_time:.2f} seconds")

if __name__ == "__main__":
    main()