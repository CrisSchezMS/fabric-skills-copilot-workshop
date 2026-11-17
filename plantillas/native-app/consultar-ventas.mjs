/**
 * Adaptador para el resultado normalizado de fabric-semanticmodel en Rayfin 2.
 * No crea clientes, no autentica y no consulta nada hasta llamar a la funcion.
 */
export async function consultarVentas(executeQuery, payload) {
  const result = await executeQuery(payload, { timeoutMs: 20_000 });
  if (result.status === "error") {
    throw new Error(
      `${result.error.category}: ${result.error.message} (${result.requestId})`,
    );
  }
  if (result.status !== "success") {
    throw new Error("Respuesta de conector no reconocida.");
  }

  const positions = new Map(
    result.table.columns.map((column, index) => [
      column.name.replace(/^\[|\]$/g, ""),
      index,
    ]),
  );
  const required = ["Categoria", "Lineas", "Unidades", "Ingresos EUR"];
  for (const name of required) {
    if (!positions.has(name)) {
      throw new Error(`Falta la columna ${name}. Revisa la consulta aprobada.`);
    }
  }
  return result.table.rows.map((row) => {
    const category = row[positions.get("Categoria")];
    const revenue = row[positions.get("Ingresos EUR")];
    const lines = row[positions.get("Lineas")];
    const units = row[positions.get("Unidades")];
    if (typeof category !== "string" || category.length === 0) {
      throw new Error("Categoria vacia o no textual.");
    }
    if (typeof revenue !== "string" || !/^-?\d+\.\d{2}$/.test(revenue)) {
      throw new Error("El importe debe llegar como texto decimal con dos decimales.");
    }
    if (
      !Number.isSafeInteger(lines) || lines < 0 ||
      !Number.isSafeInteger(units) || units < 0
    ) {
      throw new Error("Recuentos no enteros o fuera del rango seguro.");
    }
    return { category, lines, units, revenue, requestId: result.requestId };
  });
}
