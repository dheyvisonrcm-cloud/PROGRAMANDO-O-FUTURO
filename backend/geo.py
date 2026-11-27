import math


def distancia_metros(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Distância entre dois pontos da Terra em metros (fórmula de Haversine)."""
    raio_terra = 6371000
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = p2 - p1
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * raio_terra * math.asin(math.sqrt(a))