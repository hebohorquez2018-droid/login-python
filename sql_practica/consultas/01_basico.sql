-- 1. Ver todos los clientes
SELECT * FROM clientes;

-- 2. Solo algunas columnas
SELECT nombre, zona FROM clientes;

-- 3. Filtrar con WHERE
SELECT nombre, precio FROM productos WHERE categoria = 'Accesorios';

-- 4. Varias condiciones
SELECT nombre, precio FROM productos WHERE precio > 100 AND categoria = 'Computadores';

-- 5. Ordenar
SELECT nombre, precio FROM productos ORDER BY precio DESC;

-- 6. Limitar resultados
SELECT nombre, precio FROM productos ORDER BY precio DESC LIMIT 3;

-- 7. Valores únicos
SELECT DISTINCT zona FROM clientes;

-- 8. Contar filas
SELECT COUNT(*) AS total_pedidos FROM pedidos;

-- 9. Buscar texto
SELECT nombre FROM clientes WHERE nombre LIKE 'M%';