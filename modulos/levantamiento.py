def evaluar_levantamiento(q, pr, pwf, gor, agua, profundidad):

    if pr <= pwf:
        return {"error": "Pr debe ser mayor que Pwf"}

    ip = q / (pr - pwf)

    if ip < 0.5:
        sistema = "Bombeo Mecánico (BM)" if agua < 70 else "PCP"
        zona = "Baja productividad"

    elif ip < 1.5:
        sistema = "Gas Lift" if gor > 800 else "BM / PCP"
        zona = "Media productividad"

    else:
        sistema = "ESP" if profundidad > 2000 else "Gas Lift"
        zona = "Alta productividad"

    return {
        "ip": ip,
        "zona": zona,
        "sistema": sistema
    }
