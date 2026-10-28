# Análise Exploratória de Dados - Varejo (Mini-Projeto Módulo 1)

**Aluna:** Eliane Lopes de Jesus  
**Turma:** Analise_de_Dados_T7  

## Como executar este projeto
1. Clone este repositório na sua máquina local.
2. Certifique-se de ter o Python e a biblioteca `pandas` instalados no seu ambiente.
3. Abra a pasta do projeto no VS Code e certifique-se de que o arquivo `Base Varejo.csv` está na mesma pasta.
4. Execute o script no terminal digitando: `python "Miniprojeto_Eliane_Lopes_Analise_de_Dados_T7.py"`.

## Reflexão Teórica: ETL e Qualidade de Dados
A etapa de Extração, Transformação e Carga (ETL) é fundamental para garantir a confiabilidade de qualquer análise de dados. Durante este projeto, eu apliquei técnicas de limpeza em uma base de varejo real e enfrentei problemas muito comuns do dia a dia da área de dados, como valores nulos, registros duplicados e tipos de dados incorretos (datas formatadas como textos). 

O tratamento dessas inconsistências — por exemplo, preenchendo vazios com "Sem Categoria" e ajustando as tipagens usando funções do Pandas — foi essencial. Fazer isso garantiu que as minhas estatísticas descritivas e os meus agrupamentos não apresentassem falhas de cálculo. Afinal, a qualidade da decisão de negócio depende totalmente da qualidade do dado que preparamos.

## Insights Obtidos da Análise (Conclusões)
Com a minha Análise Exploratória de Dados (AED) após a limpeza, consegui obter os seguintes insights operacionais:

1. **Padrão de Qualidade da Base:** Logo na verificação inicial, identifiquei mais de 96 mil registros duplicados (linhas idênticas). Isso aponta para uma provável falha no sistema de registro do Ponto de Venda (PDV), que precisa ser corrigida na origem para não inflar relatórios de faturamento da empresa.
2. **Desempenho de Categorias:** Descobri que a categoria "ALIMENTOS" representa a esmagadora maioria do volume de compras (mais de 384 mil registros). Ela é o verdadeiro carro-chefe de atração e vendas da rede.
3. **Perfil de Público por Gênero:** Notei que o volume de compras é levemente superior entre o público feminino, uma informação valiosa que eu recomendaria para direcionar a linguagem e o foco visual das próximas campanhas promocionais.
4. **Estatísticas Familiares:** Ao calcular as estatísticas da coluna de Número de Filhos, vi que a média é de 1,15 por cliente, mas a mediana e a moda são 0. Isso me indica que a maior parte das transações é feita por clientes sem filhos registrados na base. Portanto, as ações de marketing não devem focar exclusivamente em embalagens "tamanho-família".