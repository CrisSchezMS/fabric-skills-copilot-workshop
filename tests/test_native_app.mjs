import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

import { consultarVentas } from "../plantillas/native-app/consultar-ventas.mjs";

const payload = JSON.parse(await readFile(
  new URL("../plantillas/native-app/ingresos-categoria.json", import.meta.url),
  "utf8",
));

function response(rows) {
  return {
    status: "success",
    table: {
      columns: ["[Unidades]", "[Ingresos EUR]", "[Categoria]", "[Lineas]"]
        .map((name) => ({ name })),
      rows,
    },
    requestId: "local-fixture",
  };
}

test("mapea columnas por nombre y conserva el decimal sin aritmetica binaria", async () => {
  const rows = await consultarVentas(async (query, options) => {
    assert.equal(query, payload);
    assert.equal(options.timeoutMs, 20_000);
    return response([[2, "0.10", "Categoria de prueba", 1]]);
  }, payload);
  assert.deepEqual(rows, [{
    category: "Categoria de prueba", lines: 1, units: 2,
    revenue: "0.10", requestId: "local-fixture",
  }]);
});

test("distingue ausencia de filas de un fallo de permisos o truncamiento", async () => {
  assert.deepEqual(await consultarVentas(async () => response([]), payload), []);
  for (const category of ["api", "overflow"]) {
    await assert.rejects(consultarVentas(async () => ({
      status: "error", error: { category, message: "Fallo de prueba" },
      requestId: "local-fixture",
    }), payload), new RegExp(category));
  }
});

test("rechaza importes numericos, recuentos inseguros y cambios de contrato", async () => {
  await assert.rejects(
    consultarVentas(async () => response([[2, 0.1, "Prueba", 1]]), payload),
    /texto decimal/,
  );
  await assert.rejects(
    consultarVentas(async () => response([[2, "1.00", "Prueba", 1.5]]), payload),
    /Recuentos/,
  );
  await assert.rejects(consultarVentas(async () => ({
    ...response([]), table: { columns: [], rows: [] },
  }), payload), /Falta la columna/);
});
