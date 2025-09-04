import { helpers } from '@vuelidate/validators'
import validateCpf from './vuevalidadeCpf'
import validCNPJ from './vuevalidadeCnpj'

export const cpfValidCheck = () => helpers.withParams(
	{ type: 'cpfValidCheck' },
	function (value) {
		if (value == undefined) value = ''
		value = value.replace(/\D/g, "");
		return validateCpf(value);
	}
);

export const cnpjValidCheck = () => helpers.withParams(
	{ type: 'cnpjValidCheck' },
	function (value) {
		if (value == undefined) value = ''
		value = value.replace(/\D/g, "");
		return !helpers.req(value) || validCNPJ(value);
	}
);
