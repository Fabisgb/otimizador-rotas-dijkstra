"""
================================================================================
PROJETO: Otimizador de Rotas de Entrega (Algoritmo de Dijkstra)
AUTORA: Fabiana Silva Guimarães
DESCRIÇÃO: Modelagem de malha logística urbana como grafo ponderado para
           encontrar o trajeto de menor distância, tempo e custo operacional.
================================================================================
"""

import heapq
from typing import Dict, List, Tuple, Optional


class OtimizadorRotas:
    """Representa uma malha viária logística e calcula caminhos mínimos."""

    def __init__(self, consumo_km_litro: float = 10.5, preco_combustivel: float = 6.19):
        # Grafo representado como lista de adjacência:
        # { 'Origem': [('Destino', distancia_km), ...] }
        self.malha: Dict[str, List[Tuple[str, float]]] = {}
        self.consumo_km_litro = consumo_km_litro
        self.preco_combustivel = preco_combustivel

    def adicionar_trecho(self, origem: str, destino: str, distancia_km: float, mao_dupla: bool = True) -> None:
        """Adiciona uma conexão viária entre dois pontos de entrega ou centros."""
        if origem not in self.malha:
            self.malha[origem] = []
        if destino not in self.malha:
            self.malha[destino] = []

        self.malha[origem].append((destino, distancia_km))
        if mao_dupla:
            self.malha[destino].append((origem, distancia_km))

    def calcular_menor_rota(self, origem: str, destino: str) -> Tuple[Optional[List[str]], float]:
        """
        Executa o Algoritmo de Dijkstra usando fila de prioridade (min-heap)
        para determinar a rota de menor quilometragem entre origem e destino.
        """
        if origem not in self.malha or destino not in self.malha:
            return None, float("inf")

        distancias: Dict[str, float] = {ponto: float("inf") for ponto in self.malha}
        anteriores: Dict[str, Optional[str]] = {ponto: None for ponto in self.malha}
        distancias[origem] = 0.0

        # Fila de prioridade armazenando (distancia_acumulada, ponto_atual)
        fila_prioridade: List[Tuple[float, str]] = [(0.0, origem)]

        while fila_prioridade:
            dist_atual, ponto_atual = heapq.heappop(fila_prioridade)

            if ponto_atual == destino:
                break

            if dist_atual > distancias[ponto_atual]:
                continue

            for vizinho, peso_km in self.malha[ponto_atual]:
                nova_distancia = dist_atual + peso_km
                if nova_distancia < distancias[vizinho]:
                    distancias[vizinho] = nova_distancia
                    anteriores[vizinho] = ponto_atual
                    heapq.heappush(fila_prioridade, (nova_distancia, vizinho))

        if distancias[destino] == float("inf"):
            return None, float("inf")

        # Reconstrói o itinerário de trás para frente
        rota: List[str] = []
        atual: Optional[str] = destino
        while atual is not None:
            rota.append(atual)
            atual = anteriores[atual]
        rota.reverse()

        return rota, distancias[destino]

    def gerar_relatorio_entrega(self, origem: str, destino: str, velocidade_media_kmh: float = 35.0) -> str:
        """Formata um resumo executivo da rota otimizada com indicadores logísticos."""
        rota, distancia_total = self.calcular_menor_rota(origem, destino)

        if not rota:
            return f"[ERRO] Não há rota conectada entre '{origem}' e '{destino}'."

        tempo_minutos = (distancia_total / velocidade_media_kmh) * 60
        litros_estimados = distancia_total / self.consumo_km_litro
        custo_combustivel = litros_estimados * self.preco_combustivel

        linhas = [
            "=" * 68,
            "RELATÓRIO DE ROTEIRIZAÇÃO LOGÍSTICA (DIJKSTRA)",
            "=" * 68,
            f"Origem           : {origem}",
            f"Destino          : {destino}",
            f"Paradas na Rota  : {len(rota) - 1} trecho(s)",
            f"Itinerário Ótimo : {' -> '.join(rota)}",
            "-" * 68,
            f"Distância Total  : {distancia_total:.2f} km",
            f"Tempo Estimado   : {tempo_minutos:.0f} min (média de {velocidade_media_kmh:.0f} km/h)",
            f"Consumo Previsto : {litros_estimados:.2f} L",
            f"Custo Combustível: R$ {custo_combustivel:.2f}",
            "=" * 68,
        ]
        return "\n".join(linhas)


def montar_malha_regional() -> OtimizadorRotas:
    """Cria uma malha de distribuição regional (São Gonçalo / Niterói / Rio)."""
    otimizador = OtimizadorRotas(consumo_km_litro=10.5, preco_combustivel=6.19)

    trechos = [
        ("CD Alcântara", "Mutondo", 3.2),
        ("CD Alcântara", "Colubandê", 4.5),
        ("Mutondo", "Centro São Gonçalo", 2.8),
        ("Colubandê", "Tribobó", 3.6),
        ("Centro São Gonçalo", "Neves", 5.4),
        ("Tribobó", "Caramujo", 4.1),
        ("Neves", "Barreto", 3.0),
        ("Caramujo", "Fonseca", 3.8),
        ("Barreto", "Fonseca", 2.5),
        ("Fonseca", "Centro Niterói", 4.2),
        ("Barreto", "Ponte Rio-Niterói", 3.5),
        ("Centro Niterói", "Icaraí", 3.4),
        ("Ponte Rio-Niterói", "Hub Logístico Caju (RJ)", 13.8),
    ]

    for origem, destino, km in trechos:
        otimizador.adicionar_trecho(origem, destino, km)

    return otimizador


if __name__ == "__main__":
    sistema = montar_malha_regional()

    # Simulação 1: Transferência entre Centro de Distribuição e Hub no Rio
    print(sistema.gerar_relatorio_entrega("CD Alcântara", "Hub Logístico Caju (RJ)"))
    print()

    # Simulação 2: Entrega urbana última milha (Last-Mile)
    print(sistema.gerar_relatorio_entrega("CD Alcântara", "Icaraí", velocidade_media_kmh=28.0))