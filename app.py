from __future__ import annotations

import colorsys
import random
from dataclasses import dataclass

import streamlit as st


@dataclass(frozen=True)
class Color:
    r: int
    g: int
    b: int

    def to_hex(self) -> str:
        return f"#{self.r:02X}{self.g:02X}{self.b:02X}"

    def to_rgb_label(self) -> str:
        return f"rgb({self.r}, {self.g}, {self.b})"

    def text_color(self) -> str:
        luminance = (0.299 * self.r) + (0.587 * self.g) + (0.114 * self.b)
        return "#111111" if luminance > 160 else "#FFFFFF"


def hex_to_rgb(hex_value: str) -> Color:
    clean = hex_value.strip().replace("#", "")
    if len(clean) != 6:
        raise ValueError("Color HEX inválido")
    return Color(int(clean[0:2], 16), int(clean[2:4], 16), int(clean[4:6], 16))


def rgb_to_hls(color: Color) -> tuple[float, float, float]:
    return colorsys.rgb_to_hls(color.r / 255, color.g / 255, color.b / 255)


def hls_to_rgb(h: float, l: float, s: float) -> Color:
    r, g, b = colorsys.hls_to_rgb(h % 1.0, max(0.0, min(1.0, l)), max(0.0, min(1.0, s)))
    return Color(int(round(r * 255)), int(round(g * 255)), int(round(b * 255)))


def shift_hue(hue: float, degrees: float) -> float:
    return (hue + (degrees / 360.0)) % 1.0


def generate_palette(base: Color, scheme: str, count: int) -> list[Color]:
    h, l, s = rgb_to_hls(base)

    if scheme == "Monocromática":
        lights = [0.14, 0.28, 0.42, 0.56, 0.70, 0.84]
        chosen = lights[:count]
        return [hls_to_rgb(h, light, s) for light in chosen]

    if scheme == "Análoga":
        offsets = [-36, -20, -8, 8, 20, 36]
        chosen = offsets[:count]
        return [hls_to_rgb(shift_hue(h, off), l, s) for off in chosen]

    if scheme == "Complementaria":
        points = [0, 180, -18, 18, 162, 198]
        chosen = points[:count]
        return [hls_to_rgb(shift_hue(h, off), l, s) for off in chosen]

    if scheme == "Triádica":
        points = [0, 120, 240, 16, 136, 256]
        chosen = points[:count]
        return [hls_to_rgb(shift_hue(h, off), l, s) for off in chosen]

    if scheme == "Complementaria dividida":
        points = [0, 150, 210, -12, 138, 222]
        chosen = points[:count]
        return [hls_to_rgb(shift_hue(h, off), l, s) for off in chosen]

    return [base]


def palette_css_variables(colors: list[Color]) -> str:
    lines = [":root {"]
    for i, color in enumerate(colors, start=1):
        lines.append(f"  --palette-{i}: {color.to_hex()};")
    lines.append("}")
    return "\n".join(lines)


def main() -> None:
    st.set_page_config(
        page_title="Generador de Paletas",
        page_icon="🎨",
        layout="wide",
    )

    st.markdown(
        """
        <style>
            .block-container {padding-top: 1.8rem; padding-bottom: 2rem;}
            h1, h2, h3 {letter-spacing: 0.2px;}
            .subtitle {color: #6B7280; margin-top: -0.4rem; margin-bottom: 1.2rem;}
            .card {
                border-radius: 14px;
                padding: 14px 12px;
                min-height: 130px;
                box-shadow: 0 8px 24px rgba(17, 24, 39, 0.12);
                border: 1px solid rgba(255, 255, 255, 0.18);
                display: flex;
                flex-direction: column;
                justify-content: flex-end;
            }
            .chip {
                display: inline-block;
                padding: 0.2rem 0.45rem;
                border-radius: 999px;
                font-size: 0.75rem;
                background: rgba(255,255,255,0.28);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("🎨 Generador de Paletas de Colores")
    st.markdown('<p class="subtitle">Simple, estético y útil para UI, branding o diseño web.</p>', unsafe_allow_html=True)

    with st.sidebar:
        st.header("Configuración")
        random_base = "#{:06X}".format(random.randint(0, 0xFFFFFF))
        base_hex = st.color_picker("Color base", value=random_base)
        scheme = st.selectbox(
            "Esquema",
            [
                "Monocromática",
                "Análoga",
                "Complementaria",
                "Triádica",
                "Complementaria dividida",
            ],
            index=0,
        )
        count = st.slider("Cantidad de colores", min_value=3, max_value=6, value=5)

    base_color = hex_to_rgb(base_hex)
    palette = generate_palette(base_color, scheme, count)

    st.subheader("Paleta generada")
    cols = st.columns(len(palette))
    for idx, (column, color) in enumerate(zip(cols, palette), start=1):
        hex_code = color.to_hex()
        rgb_label = color.to_rgb_label()
        text = color.text_color()
        with column:
            st.markdown(
                f"""
                <div class="card" style="background:{hex_code}; color:{text};">
                    <span class="chip">Color {idx}</span>
                    <div style="margin-top: 0.45rem; font-weight: 700;">{hex_code}</div>
                    <div style="font-size: 0.88rem; opacity: 0.92;">{rgb_label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.divider()
    st.subheader("Exportar")
    hex_list = [c.to_hex() for c in palette]
    st.code(", ".join(hex_list), language="text")

    css_text = palette_css_variables(palette)
    st.download_button(
        "Descargar variables CSS",
        data=css_text,
        file_name="palette.css",
        mime="text/css",
    )


if __name__ == "__main__":
    main()
