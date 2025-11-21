def calculate_percentage_and_grade(s):
    # s is a dict-like object with keys mark1 .. mark5
    marks = []
    for i in range(1, 6):
        k = f"mark{i}"
        m = float(s.get(k, 0.0))
        if m < 0:
            m = 0.0
        if m > 100:
            m = 100.0
        s[k] = m
        marks.append(m)
    total = sum(marks)
    s["percentage"] = total / 5.0
    p = s["percentage"]
    if p >= 90:
        s["grade"] = "A"
    elif p >= 80:
        s["grade"] = "B"
    elif p >= 70:
        s["grade"] = "C"
    elif p >= 60:
        s["grade"] = "D"
    else:
        s["grade"] = "F"