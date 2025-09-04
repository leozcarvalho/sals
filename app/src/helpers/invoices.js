export const fiscalDocStatus = {
	'emited': 'Emitida',
	'new': 'Nova',
	'processing': 'Processando'
}

export const toBrl = (value) => value.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })

export const dateToIsoFormat = (date) => {
	try {
		const splitDate = date.split('/')
		const parsedDate = new Date(splitDate[2], splitDate[1] - 1,  splitDate[0], 0, 0, 0, 0)
		return parsedDate.toISOString()
	} catch {
		return date
	}
}