from typing import Any, Dict, Optional

import httpx
from mcp.server.fastmcp import FastMCP
import json

weather_mcp = FastMCP("Weather")

OPEN_METEO_WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
OPEN_METEO_GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"


@weather_mcp.tool()
def geocde_city(name: str, country: Optional[str] = None, language: str = "zh") -> Dict[str, Any]:
    """将城市名称解析为经纬度

    Args:
        name (str): 城市名
        country (Optional[str], optional): 所属国家. Defaults to None.
        language (str, optional): 官方语言. Defaults to "zh".

    Returns:
        dict[str, Any]: 获取结果
    """
    print(f"[Wether Server] geocde_city start {name}, {country}, {language}")
    params = {"name": name, "count": 1, "language": language, "format": "json"}
    if country:
        params["country"] = country
    with httpx.Client(timeout=10) as client:
        r = client.get(OPEN_METEO_GEOCODE_URL, params=params)
        r.raise_for_status()
        data = r.json()
    results = data.get("results") or []
    if not results:
        return {"error": f"城市未找到: {name}"}
    top = results[0]
    result = {
        "name": top.get("name"),
        "lat": top.get("latitude"),
        "lon": top.get("longitude"),
        "country": top.get("country"),
    }
    print(f"[Wether Server] geocde_city result: {json.dumps(result)}")
    return result


@weather_mcp.tool()
def get_current_weather(lat: float, lon: float) -> Dict[str, Any]:
    """根据经纬度获取天气

    Args:
        lat (float): 纬度
        lon (float): 经度

    Returns:
        Dict[str, Any]: 结果
    """
    print(f"[Wether Server] get_current_weather start {lat}, {lon}")
    params = {"latitude": lat, "longitude": lon, "current_weather": True}
    with httpx.Client(timeout=10) as client:
        r = client.get(OPEN_METEO_WEATHER_URL, params=params)
        print(r)
        r.raise_for_status()
        payload = r.json()
    cw = payload.get("current_weather") or {}
    result = {**params, **cw}
    print(f"[Wether Server] get_current_weather result {json.dumps(result)}")
    return result


def get_current_weather_by_city(name: str, country: str | None = None, language: str = "zh") -> Dict[str, Any]:
    """获取城市天气

    Args:
        name (str): 城市名
        country (Optional[str], optional): 所属国家. Defaults to None.
        language (str, optional): 官方语言. Defaults to "zh".


    Returns:
        Dict[str, Any]: 结果
    """
    print(f"[Wether Server] get_current_weather_by_city start {name}, {country}, {language}")
    g = geocde_city(name=name, country=country, language=language)
    if "error" in g:
        return g
    w = get_current_weather(lat=g["lat"], lon=g["lon"])
    result = {**g, **w}
    print(f"[Wether Server] get_current_weather_by_city result {json.dumps(result)}")
    return result


def start():
    weather_mcp.run(transport="streamable-http")


def test():
    print(geocde_city("成都", "中国"))
    print(get_current_weather(30.66667, 104.06667))
    print(get_current_weather_by_city("成都", "中国"))


if __name__ == "__main__":
    start()
