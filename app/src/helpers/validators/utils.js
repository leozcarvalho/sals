const VALID_DATA = {
	cpf: {
		length: 11,
		invalid: [
			"00000000000",
			"11111111111",
			"22222222222",
			"33333333333",
			"44444444444",
			"55555555555",
			"66666666666",
			"77777777777",
			"88888888888",
			"99999999999"
		]
	},
	cnpj: {
		length: 14,
		invalid: [
			"00000000000000",
			"11111111111111",
			"22222222222222",
			"33333333333333",
			"44444444444444",
			"55555555555555",
			"66666666666666",
			"77777777777777",
			"88888888888888",
			"99999999999999"
		]
	}
};

/**
 * Isola os dígitos da string
 *
 * @param {String} value Valor a ser limpo
 */
export const sanitizeValue = value => value.replace(/\D/g, "");

/**
 * Valida a string do documento
 * @param {String} validType tipo de validação. OPÇÕES: cpf | cnpj
 * @param {String} value string a ser validada
 */
export const validData = validType => value =>
	value.length == VALID_DATA[validType].length &&
	!VALID_DATA[validType].invalid.find(v => v == value);

/**
 * Soma os dígitos do documento multiplicado pelo fator da posição
 * @param {string} value valor do documento
 * @param {Number} initialFactor valor inicial do fator de cálculo
 * @param {Number} initialPosition Posição inicial para ser feito o cálculo
 */
export const sumDigits = (value, initialFactor, initialPosition = 0) => {
	let sum = 0;
	for (let i = initialFactor; i > 1; i--) {
		sum += parseInt(value[initialPosition + (initialFactor - i)]) * i;
	}
	return sum;
};

/**
 * retorna o dígito verificador
 * @param {Number} value Valor da soma dos dígitos
 */
export const getDV = value =>
	(11 - (value % 11) > 9 ? 0 : 11 - (value % 11)).toString();

