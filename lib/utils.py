import re


def money(value, precision=2):
	try:
		value = float(value)
	except:
		return value

	orig = format(value, f'.{precision}f')
	intpart, dec = orig.split('.')

	intpart = intcomma(intpart)

	return ','.join([intpart, dec])

def intcomma(value):
	orig = str(value)
	novo = re.sub(r'^(-?\d+)(\d{3})', '\g<1>.\g<2>', orig)

	if orig == novo:
		return novo

	return intcomma(novo)
