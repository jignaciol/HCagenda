INSERT INTO "Agenda".tipo_area(
             descipcion, fec_ing, bl)
    VALUES ('Piso', '03-12-2016', 1);


INSERT INTO "Agenda".tipo_area(
             descipcion, fec_ing, bl)
    VALUES ('Ubicacion', '03-12-2016', 1);





SELECT * FROM "Agenda".empleado;
SELECT * FROM "Agenda".tipo_area;
SELECT * FROM "Agenda".departamento;
SELECT * FROM "Agenda"."tipoDatoContacto";
SELECT * FROM "Agenda"."datosContacto";
SELECT * FROM "Agenda"."Extension";
SELECT * FROM "Agenda"."empleadoExtension";
SELECT * FROM "Agenda"."menuOpcion";


SELECT id, descripcion, fec_ing, bl, id_tipo_area FROM "Agenda"."Area";
SELECT * FROM "Agenda"."Area";

SELECT id_opcion, descripcion, url,
                         to_char(fec_asig, 'DD-MM-YYYY') as fec_asig,
                         to_char(fec_desact, 'DD-MM-YYYY') as fec_desct, bl
                  FROM "Agenda".tipoarea;


***CONSULTAS***

SELECT * FROM "Agenda".empleado as e WHERE e.ficha='13140';
SELECT * FROM "Agenda".empleado WHERE nombre LIKE 'JOSE%';
SELECT * FROM "Agenda".empleado WHERE id_departamento = 39;

SELECT * FROM "Agenda".departamento WHERE descripcion LIKE '%QUI%';

SELECT * FROM "Agenda"."Extension" WHERE numero = '41320';



SELECT e.* , d.descripcion
FROM "Agenda".empleado e 
LEFT JOIN "Agenda".departamento d ON d.id = e.id_departamento
WHERE id_departamento = 41;





***UPDATE***

UPDATE "Agenda".empleado SET id_departamento = 41 WHERE ficha = '13109';

UPDATE "Agenda".tipoarea SET descripcion='Ubicacion' WHERE id = 1;
SELECT * FROM "Agenda".tipoarea;
SELECT * FROM "Agenda"."Area";

***DELETE***

DELETE FROM "Agenda"."empleadoExtension" WHERE id = 278;



*****INSERT******

INSERT INTO "Agenda"."Extension"(
            id_departamento, numero, fec_ing, bl, csp, tipo, modelo, serial, "mac-pos", fecha_inventario)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, 
            ?, ?, ?);




INSERT INTO "Agenda"."menuOpcion"(descripcion, url, fec_asig, fec_desact, bl)
    VALUES ('Mensajeria (SMS)', '#', '2016-05-11', '2016-05-11', 1);







INSERT INTO "Agenda"."Area"(
             descripcion, fec_ing, bl, id_tipo_area)
    VALUES ('SOTANO', '02-16-2016', 1, 2);


INSERT INTO "Agenda".departamento(
            descripcion, fec_ing, bl, id_ubicacion, id_piso)
    VALUES ('ASEO Y SANEAMIENTO', '03-29-2016', 1, 3, 9);


INSERT INTO "Agenda".tipo_dato_contacto(
             descripcion, fec_ing)
    VALUES ('TELEFONO HABITACIÓN', '02-16-2016');

INSERT INTO "Agenda"."Extension"(
            id_departamento, numero, fec_ing, bl)
    VALUES (39, '41436', '02-16-2016', 1);

.

INSERT INTO "Agenda".empleado(
            ficha, voe, cedula, nombre, apellido, indicador, fecha_nac, 
            fecha_ing, id_departamento)
       VALUES ('11362', 'V', '15718732', 'JOSE I.', 'LUENGO BELTRAN', 'LUENGOJI', '05-22-1981', '03-16-2016', 39);


INSERT INTO "Agenda".tipoarea(fec_ing, bl, descripcion)
       VALUES ('2016-03-16', 1, '');



/* ENLACE DE EMPLEADO CON UNA EXTENSION */
 INSERT INTO "Agenda"."empleadoExtension"(
            id_empleado, id_extension, fec_asignacion, mostrar)
    VALUES (152, 63, '04-04-2016', 1);

SELECT * FROM "Agenda"."empleadoExtension";
SELECT * FROM "Agenda".empleado WHERE apellido LIKE 'CHIRI%' and nombre LIKE 'ZUL%';

DELETE FROM "Agenda".empleado WHERE id = 278;

DELETE FROM "Agenda"."empleadoExtension" WHERE id = 58;

SELECT * FROM "Agenda"."Extension" WHERE numero = '41013';

INSERT INTO "Agenda"."Extension"(
            id_departamento, numero, fec_ing, bl)
    VALUES (14, '41051', '04-04-2016', 1);



**** SQL select multiples tablas ****


SELECT e.*,
       epx.id_extension, epx.mostrar,
       ext.numero, ext.serial,
       d.descripcion as departamento,
       dcc.descripcion as correo_electronico,
       dcm.descripcion as telefono_celular,
       dct.descripcion as telefono_habitacion
FROM "Agenda".empleado e
LEFT JOIN "Agenda"."empleadoExtension" epx ON epx.id_empleado = e.id
LEFT JOIN "Agenda"."Extension" ext ON ext.id = epx.id_extension
LEFT JOIN "Agenda"."departamento" d ON d.id = e.id_departamento
LEFT JOIN "Agenda"."datosContacto" dcc ON dcc.id_empleado = e.id and dcc.id_tipo_contacto = 2
LEFT JOIN "Agenda"."datosContacto" dcm ON dcm.id_empleado = e.id and dcm.id_tipo_contacto = 3
LEFT JOIN "Agenda"."datosContacto" dct ON dct.id_empleado = e.id and dct.id_tipo_contacto = 4
WHERE char_length(ext.numero) > 0
ORDER BY d.descripcion, e.apellido, e.nombre;


/*WHERE e.id_departamento = 39;*/



SELECT  ext.id, ext.numero, ext.modelo,
	ext.id_departamento, d.descripcion
FROM "Agenda"."Extension" ext
LEFT JOIN "Agenda".departamento d ON d.id = ext.id_departamento

SELECT * FROM "Agenda".departamento;













-- DROP TABLE "Agenda"."menuOpcion";

CREATE TABLE "Agenda"."menuOpcion"
(
  id_opcion bigserial NOT NULL,
  descripcion character varying,
  url character varying,
  fec_asig date,
  fec_desact date,
  bl integer,
  CONSTRAINT id_opcion PRIMARY KEY (id_opcion)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE "Agenda"."menuOpcion"
  OWNER TO postgres;



-- DROP TABLE "Agenda"."menuUsuario";

CREATE TABLE "Agenda"."menuUsuario"
(
  "id_menuUsuario" bigserial NOT NULL,
  username character varying,
  "id_opcionMenu" bigint,
  fec_asig date,
  fec_desact date,
  bl integer,
  CONSTRAINT "id_menuUsuario" PRIMARY KEY ("id_menuUsuario")
)
WITH (
  OIDS=FALSE
);
ALTER TABLE "Agenda"."menuUsuario"
  OWNER TO postgres;

