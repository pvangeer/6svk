from svk.visualization.helpers import measure_text
from svk.visualization.helpers import wrapped_lines


def test_measure_text_comparison():
    text = "Dit is een voorbeeld text"
    font_sizes = [12, 16, 24]

    for font_size in font_sizes:
        s1 = measure_text(text=text, font_size=font_size)
        s2 = measure_text(text=text, font_size=font_size, font_weight="bold")


def test_wrapped_lines_uses_batch_text_measurement():
    max_width = measure_text("one two ", 12)[0]

    lines = wrapped_lines("one two three", max_width=max_width, font_size=12)

    assert lines == ["one two ", "three "]
