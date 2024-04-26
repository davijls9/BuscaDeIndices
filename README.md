# Busca de Índice e Consulta

Este repositório contém um conjunto de scripts Python para a criação e manipulação de um índice invertido, bem como a realização de consultas e compressão de texto utilizando o Código de Huffman e compressão baseada em dicionário.

## Reconstrução do Documento

O script `reconstruir_documento` permite reconstruir um documento a partir de um índice invertido[^2^][2]. O índice é representado por uma lista de tuplas, onde cada tupla contém o índice do termo, o índice do documento e as posições do termo no documento.

## Árvore de Sintaxe para Consultas

O código inclui uma implementação para criar uma árvore de sintaxe para consultas lógicas. A árvore é construída utilizando nodos que representam termos e operadores lógicos (AND, OR).

## Compressão Estática com Código de Huffman

A compressão de texto é realizada através do Código de Huffman. O script calcula as frequências dos caracteres, constrói a árvore de Huffman e codifica/decodifica o texto.

## Compressão Baseada em Dicionário

O script `compressao_baseada_em_dicionario` realiza a compressão de texto substituindo palavras por códigos definidos em um dicionário de compressão.

## Como Usar

1. Clone o repositório.
2. Execute os scripts Python para ver os exemplos em ação.

## Contribuições

Contribuições são bem-vindas! Por favor, abra uma issue ou envie um pull request com suas melhorias.

## Licença

Este projeto está licenciado sob a Licença GNU 3 - veja o arquivo LICENSE.md para detalhes.
