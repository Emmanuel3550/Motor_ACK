def _df_to_table_story(df, styles):
    """Convierte un DataFrame a objetos de ReportLab (Table) con estilo y semáforo en
    la columna 'Dias_Integracion' según las reglas:
        - >20 -> rojo
        - 10..20 -> naranja
        - <10 -> amarillo
    Retorna (table)
    """
    # Extra imports local para no forzar pandas en este módulo
    cols = list(df.columns)

    # Construir matriz de datos con formateo de celdas
    data = [cols]
    for _, row in df.iterrows():
        formatted_row = [_format_cell_value(row[c]) for c in cols]
        data.append(formatted_row)

    # Crear tabla
    table = Table(data, repeatRows=1)

    # Estilos básicos
    tbl_style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ])

    # Aplicar semáforo en la columna 'Dias_Integracion' si existe
    if 'Dias_Integracion' in cols:

        # ⛔ FIX: evitar error si df no tiene filas
        if len(df) == 0:
            table.setStyle(tbl_style)
            return table

        dias_col_idx = cols.index('Dias_Integracion')

        # Recorremos filas de datos (row_idx en tabla = fila real + 1 por header)
        for row_idx, original_row in enumerate(df.itertuples(index=False), start=1):
            try:
                # obtener valor numérico si existe
                val = getattr(original_row, 'Dias_Integracion')
            except Exception:
                try:
                    val = original_row[cols.index('Dias_Integracion')]
                except Exception:
                    val = None

            # Determinar color
            color_to_apply = None
            try:
                if val is None:
                    color_to_apply = None
                else:
                    num = float(val)
                    if num > 20:
                        color_to_apply = colors.red
                    elif 10 <= num <= 20:
                        color_to_apply = colors.orange
                    elif num < 10:
                        color_to_apply = colors.yellow
            except Exception:
                color_to_apply = None

            # Aplicar si corresponde
            if color_to_apply:
                tbl_style.add((
                    'BACKGROUND',
                    (dias_col_idx, row_idx),  # celda específica
                    (dias_col_idx, row_idx),
                    color_to_apply
                ))

    # Aplicar estilos finales
    table.setStyle(tbl_style)
    return table
