# Calibration file for repeatability tests
# TODO: translate to english

repet_cero = -0.01020
repet_paso = 0.000015
repet_tarado = repet_cero + repet_paso
sentido_arriba = True
if (sentido_arriba):
	valor_prefijo = repet_cero
else:
	valor_prefijo = repet_tarado + repet_paso

print("Valor prefijo: " + str(valor_prefijo))
