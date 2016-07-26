SELECT id, ficha, voe, cedula, nombre, apellido, indicador, fecha_nac, 
       fecha_ing, id_departamento, bl
FROM "Agenda".empleado;




SELECT * FROM "Agenda"."datosContacto" dc;
SELECT * FROM "Agenda"."tipoDatoContacto" dc;

DELETE FROM "Agenda"."datosContacto";

update "Agenda"."datosContacto" SET id_empleado=1117  ;





SELECT dc.id,
	dc.descripcion,
	to_char(dc.fec_ing, 'DD-MM-YYYY') as fec_ing,
	dc.id_empleado,
	tdc.id as id_tipo_contacto,
	tdc.descripcion as tipoContacto
FROM "Agenda"."datosContacto" dc
LEFT JOIN "Agenda"."tipoDatoContacto" tdc ON tdc.id = dc.id_tipo_contacto;


SELECT id, descripcion, fec_ing, bl
  FROM "Agenda"."tipoDatoContacto";


SELECT id, descripcion, fec_ing, id_empleado, id_tipo_contacto
  FROM "Agenda"."datosContacto";


delete from "Agenda".empleado where id > 1117;

