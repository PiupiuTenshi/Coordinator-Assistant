from __future__ import annotations

import math

from backend.app.data.sample_data import HOSPITALS
from backend.app.models.schemas import DepartmentRoute, HospitalRecommendation, Location


def haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    radius_km = 6371.0
    d_lat = math.radians(lat2 - lat1)
    d_lng = math.radians(lng2 - lng1)
    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lng / 2) ** 2
    )
    return 2 * radius_km * math.asin(math.sqrt(a))


class HospitalService:
    def nearby(
        self,
        location: Location | None,
        emergency_only: bool = False,
        limit: int = 3,
        target_specialty: str = "",
    ) -> list[HospitalRecommendation]:
        hospitals = [item for item in HOSPITALS if item["has_emergency"] or not emergency_only]
        if target_specialty and not emergency_only:
            hospitals.sort(key=lambda item: target_specialty not in item.get("departments", {}))
        rows = []
        for hospital in hospitals:
            distance = None
            if location is not None:
                distance = round(haversine_km(location.lat, location.lng, hospital["lat"], hospital["lng"]), 2)
            route_specialty = "Cấp cứu" if emergency_only else target_specialty
            rows.append(self._to_recommendation(hospital, distance, location, route_specialty))
        rows.sort(key=lambda item: item.distance_km if item.distance_km is not None else 999999)
        return rows[:limit]

    def directions(self, hospital_id: str, lat: float | None = None, lng: float | None = None, specialty: str = "") -> dict | None:
        hospital = next((item for item in HOSPITALS if item["id"] == hospital_id), None)
        if hospital is None:
            return None
        origin = f"&origin={lat},{lng}" if lat is not None and lng is not None else ""
        return {
            "hospital_id": hospital["id"],
            "name": hospital["name"],
            "lat": hospital["lat"],
            "lng": hospital["lng"],
            "map_url": self._google_directions_url(hospital, origin=origin),
            "osm_url": self._osm_url(hospital),
            "embed_map_url": self._embed_map_url(hospital),
            "department_route": self._department_route(hospital, specialty or "Cấp cứu"),
        }

    def name_for(self, hospital_id: str) -> str:
        hospital = next((item for item in HOSPITALS if item["id"] == hospital_id), None)
        return hospital["name"] if hospital else hospital_id

    def _to_recommendation(
        self,
        hospital: dict,
        distance: float | None,
        origin: Location | None = None,
        target_specialty: str = "",
    ) -> HospitalRecommendation:
        origin_query = f"&origin={origin.lat},{origin.lng}" if origin else ""
        return HospitalRecommendation(
            id=hospital["id"],
            name=hospital["name"],
            address=hospital["address"],
            lat=hospital["lat"],
            lng=hospital["lng"],
            distance_km=distance,
            phone=hospital["phone"],
            has_emergency=hospital["has_emergency"],
            opening_hours=hospital["opening_hours"],
            map_url=self._google_directions_url(hospital, origin=origin_query),
            osm_url=self._osm_url(hospital),
            embed_map_url=self._embed_map_url(hospital),
            department_route=self._department_route(hospital, target_specialty),
        )

    def _google_directions_url(self, hospital: dict, origin: str = "") -> str:
        return f"https://www.google.com/maps/dir/?api=1{origin}&destination={hospital['lat']},{hospital['lng']}"

    def _osm_url(self, hospital: dict) -> str:
        return f"https://www.openstreetmap.org/?mlat={hospital['lat']}&mlon={hospital['lng']}#map=16/{hospital['lat']}/{hospital['lng']}"

    def _embed_map_url(self, hospital: dict) -> str:
        lat = hospital["lat"]
        lng = hospital["lng"]
        delta = 0.006
        bbox = f"{lng - delta},{lat - delta},{lng + delta},{lat + delta}"
        return f"https://www.openstreetmap.org/export/embed.html?bbox={bbox}&layer=mapnik&marker={lat},{lng}"

    def _department_route(self, hospital: dict, target_specialty: str) -> DepartmentRoute | None:
        departments = hospital.get("departments", {})
        route = departments.get(target_specialty) or departments.get("Cấp cứu") or next(iter(departments.values()), None)
        if route is None:
            return None
        specialty = target_specialty if target_specialty in departments else route["department"].replace("Khoa ", "")
        return DepartmentRoute(
            specialty=specialty,
            department=route["department"],
            building=route["building"],
            floor=route["floor"],
            room=route["room"],
            estimated_walk_minutes=route["estimated_walk_minutes"],
            start_label="Cổng/Sảnh chính",
            end_label=route["department"],
            map_points=route["map_points"],
            steps=route["steps"],
        )


hospital_service = HospitalService()
