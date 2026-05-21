from __future__ import annotations

import argparse
from pathlib import Path


def build_qr_svg(url: str) -> str:
    import qrcode
    from qrcode.image.svg import SvgPathImage

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=12,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    image = qr.make_image(image_factory=SvgPathImage, fill_color="#17202a", back_color="white")
    return image.to_string(encoding="unicode")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate MVP QR-style SVG placeholder.")
    parser.add_argument("--url", default="http://127.0.0.1:5173")
    parser.add_argument("--output", type=Path, default=Path("frontend/public/qr-mvp.svg"))
    args = parser.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(build_qr_svg(args.url), encoding="utf-8")
    print(f"Wrote {args.output} for {args.url}")
    print("Generated a standards-compliant QR SVG.")


if __name__ == "__main__":
    main()
