from __future__ import annotations

from backend.app.models.schemas import SpecialtyRecommendation


SPECIALTY_RULES = {
    "Tim mạch": ["đau ngực", "vã mồ hôi", "hồi hộp", "khó thở"],
    "Hô hấp": ["ho", "khó thở", "đau họng", "sổ mũi", "sốt"],
    "Tiêu hóa": ["đau bụng", "buồn nôn", "nôn", "tiêu chảy", "táo bón", "ợ nóng", "đầy bụng"],
    "Thần kinh": ["đau đầu", "chóng mặt", "co giật", "tê bì", "yếu liệt", "méo miệng", "nói khó"],
}


class SpecialtyService:
    def recommend(self, symptoms: list[str]) -> list[SpecialtyRecommendation]:
        lowered = [symptom.lower() for symptom in symptoms]
        scored: list[tuple[str, int, list[str]]] = []
        for specialty, keywords in SPECIALTY_RULES.items():
            matches = [keyword for keyword in keywords if keyword in lowered]
            if matches:
                scored.append((specialty, len(matches), matches))

        if not scored:
            return [
                SpecialtyRecommendation(
                    specialty="Nội tổng quát",
                    department="Khoa Khám bệnh",
                    reason="Chưa đủ dữ liệu để chọn chuyên khoa cụ thể.",
                    confidence=0.45,
                )
            ]

        scored.sort(key=lambda item: item[1], reverse=True)
        return [
            SpecialtyRecommendation(
                specialty=specialty,
                department=f"Khoa {specialty}",
                reason="Phù hợp với triệu chứng: " + ", ".join(matches),
                confidence=min(0.95, 0.55 + count * 0.15),
            )
            for specialty, count, matches in scored[:3]
        ]


specialty_service = SpecialtyService()
