import {sanitizeValue,
		validData,
		sumDigits,
		getDV} from "./utils"

const validateCnpj = validData("cnpj");

/**
 * Valida o CNPJ
 * @param {string} value CNPJ a ser validado
 *
 * @returns {boolean}
 */
const validCNPJ = value => {
	// Isola apenas os dígitos na string
	value = sanitizeValue(value);

	// verifica se o tamanho da string está correta
	if (!validateCnpj(value)) {
		return false;
	}

	const originalValue = value.substring(0, 12);
	const originalDigit = value.substring(12);
	let sumDigits1 =
		sumDigits(originalValue, 5) + sumDigits(originalValue, 9, 4);
	let digit1 = getDV(sumDigits1);

	let sumDigits2 =
		sumDigits(originalValue + digit1, 6) +
		sumDigits(originalValue + digit1, 9, 5);
	let digit2 = getDV(sumDigits2);

	// verifica se o dígito original é igual aos dígitos obtidos
	return originalDigit == `${digit1}${digit2}`;
};
export default validCNPJ;