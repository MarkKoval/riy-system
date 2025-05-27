"""
geo_utils.py — Географічні утиліти для системи "Рій".
"""

import math


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Обчислює відстань між двома точками на земній кулі (в метрах).
    """
    R = 6371000  # Радіус Землі в метрах

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def bearing_between_points(lat1, lon1, lat2, lon2):
    """
    Обчислює азимут (кут напряму) від точки 1 до точки 2 (в градусах).
    """
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_lambda = math.radians(lon2 - lon1)

    x = math.sin(delta_lambda) * math.cos(phi2)
    y = math.cos(phi1) * math.sin(phi2) - (
        math.sin(phi1) * math.cos(phi2) * math.cos(delta_lambda)
    )

    theta = math.atan2(x, y)
    return (math.degrees(theta) + 360) % 360


def destination_point(lat, lon, distance_m, bearing_deg):
    """
    Обчислює нову координату через певну відстань і азимут.
    """
    R = 6371000  # радіус Землі
    bearing = math.radians(bearing_deg)

    phi1 = math.radians(lat)
    lambda1 = math.radians(lon)

    phi2 = math.asin(math.sin(phi1) * math.cos(distance_m / R) +
                     math.cos(phi1) * math.sin(distance_m / R) * math.cos(bearing))

    lambda2 = lambda1 + math.atan2(
        math.sin(bearing) * math.sin(distance_m / R) * math.cos(phi1),
        math.cos(distance_m / R) - math.sin(phi1) * math.sin(phi2)
    )

    return (math.degrees(phi2), math.degrees(lambda2))


def latlon_to_xy(lat, lon, origin_lat, origin_lon):
    """
    Перетворює GPS-координати в XY-площину відносно початкової точки (в метрах).
    """
    dx = haversine_distance(origin_lat, origin_lon, origin_lat, lon)
    dy = haversine_distance(origin_lat, origin_lon, lat, origin_lon)

    if lon < origin_lon:
        dx = -dx
    if lat < origin_lat:
        dy = -dy

    return dx, dy


def xy_to_latlon(dx, dy, origin_lat, origin_lon):
    """
    Перетворює координати XY (в метрах) у GPS-координати, виходячи з початкової точки.
    """
    dist = math.sqrt(dx**2 + dy**2)
    bearing = math.degrees(math.atan2(dx, dy))
    return destination_point(origin_lat, origin_lon, dist, bearing)
