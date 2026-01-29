"""color_palette.py

Signal 기본 색상 팔레트.

요구사항:
- 기본 색상(초기 표시)이 흰색/회색 고정이 아니라, "가시성 좋은 색"을 순서대로 할당.
- 주로 리스트에서 구분이 잘 되도록 대비가 있는 파스텔 계열을 사용.

주의:
- 이는 UI 표시용 메타데이터이며, DBC 텍스트 저장(SG_ 라인)에는 현재 포함되지 않습니다.
"""

from __future__ import annotations

from typing import Sequence

# 대비가 좋은 파스텔 팔레트(반복 사용)
DEFAULT_SIGNAL_COLORS: Sequence[str] = (
    "#8DD3C7",  # teal
    "#FFFFB3",  # light yellow
    "#BEBADA",  # lavender
    "#FB8072",  # salmon
    "#80B1D3",  # light blue
    "#FDB462",  # orange
    "#B3DE69",  # light green
    "#FCCDE5",  # pink
    "#D9D9D9",  # light gray
    "#BC80BD",  # purple
    "#CCEBC5",  # mint
    "#FFED6F",  # yellow
)


def pick_color(index: int, palette: Sequence[str] = DEFAULT_SIGNAL_COLORS) -> str:
    """index에 해당하는 팔레트 색상을 반환(순환)."""
    if not palette:
        return "#FFFFFF"
    return palette[index % len(palette)]
