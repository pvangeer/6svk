from svk.visualization.helpers import measure_text, measure_text_chromium


def test_measure_text_comparison():
    text = "Dit is een voorbeeld text"
    font_sizes = [12, 16, 24]

    for font_size in font_sizes:
        s1 = measure_text(text=text, font_size=font_size)
        s2 = measure_text_chromium(text=text, font_size=font_size, font_weight="bold")
