def color_toward_grey(r, g, b, grey_fraction=0.5, grey=(210, 190, 210)) -> str:
    r2, g2, b2 = grey
    r_x = round(r + (r2 - r) * grey_fraction)
    g_x = round(g + (g2 - g) * grey_fraction)
    b_x = round(b + (b2 - b) * grey_fraction)
    return f"rgb({r_x},{g_x},{b_x})"
