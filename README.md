# ROELSTAR — Diagnóstico Financiero Empresarial

Aplicación Streamlit para talleres y empresas de servicios, en COP, con vistas mensual y anual.

## Funciones
- Ventas separadas de mano de obra y repuestos.
- Vista mensual por mes y vista anual con comparativo mensual y acumulado.
- Costos directos, gastos operativos, gastos financieros e impuestos.
- Márgenes bruto, operativo y neto.
- Punto de equilibrio estimado y datos básicos de liquidez.
- Exportación del resumen del periodo y de la tabla de los 12 meses a CSV/Excel.

## Ejecutar en Windows
1. Instala Python 3.10 o superior.
2. Descomprime el ZIP.
3. Ejecuta `INICIAR_ROELSTAR.bat`, o instala dependencias con `pip install -r requirements.txt`.
4. Ejecuta `streamlit run roelstar_diagnostico_empresarial.py`.

## Publicar en Streamlit Cloud
Sube `roelstar_diagnostico_empresarial.py` y `requirements.txt` a la raíz de un repositorio de GitHub. Crea una nueva app en Streamlit Cloud y selecciona ese archivo como entrada.

## Importante
Los datos se mantienen durante la sesión y no se guardan automáticamente de forma permanente. Descarga los CSV para conservarlos. En vista anual, para caja, cartera, inventario y deudas usa saldos de cierre; se recomienda colocarlos solo en diciembre para evitar sumar saldos repetidos. El punto de equilibrio es una estimación simplificada y debe adaptarse a la clasificación real de costos fijos y variables.
