🚚 Otimizador de Rotas de Entrega (Algoritmo de Dijkstra)

Implementação em Python de um motor de roteirização logística baseado em Teoria dos Grafos e no Algoritmo de Dijkstra, desenvolvido para calcular o trajeto de menor distância, tempo estimado e custo operacional entre centros de distribuição e pontos de entrega.

🎯 Problema & Contexto Logístico

Na operação de transporte e distribuição urbana (last-mile), a escolha intuitiva de trajetos sem análise de malha viária gera aumento no consumo de combustível, desgaste de frota e atrasos nas janelas de entrega.

Inspirado na experiência prática de planejamento de cobertura territorial em campo, este projeto modela bairros e hubs logísticos como vértices de um grafo ponderado, garantindo matematicamente o caminho mais curto entre qualquer origem e destino.

⚙️ Como Funciona

Estrutura de Grafo Ponderado: Cada ponto de entrega ou hub é representado como um nó, e as vias de ligação são arestas com peso equivalente à quilometragem real.

Algoritmo de Dijkstra com Fila de Prioridade (heapq): Garante complexidade eficiente $O((V + E) \log V)$ para encontrar o menor percurso acumulado.

Indicadores Operacionais: Além da sequência exata de paradas, o sistema calcula automaticamente:

1. Distância total em quilômetros ($\text{km}$);

2. Tempo estimado de percurso com base na velocidade média da via;

3. Consumo previsto de combustível e custo financeiro da viagem.

🚀 Como Executar

O projeto utiliza apenas a biblioteca padrão do Python 3 (sem dependências externas):

# Clone o repositório
git clone https://github.com/Fabisgb/otimizador-rotas-dijkstra.git

# Acesse a pasta e execute o script
cd otimizador-rotas-dijkstra
python otimizador_rotas.py


👩‍💻 Autora

Desenvolvido por Fabiana Silva Guimarães — Estudante de Ciência da Computação e Técnica em Logística.

🔗 Portfólio Completo | LinkedIn

