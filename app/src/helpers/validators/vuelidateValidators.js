import { helpers } from "@vuelidate/validators";
import validateCpf from "./vuevalidadeCpf";
import validCNPJ from "./vuevalidadeCnpj";
import { validateCompanyData } from "./check-company-data-conflicts";
import { validateUserData } from "./check-user-data-conflicts";

const customValidators = {};

customValidators.minCheck = (min) =>
  helpers.withParams(
    { type: "minCheck", min: min },
    (value) => !helpers.req(value) || value.length >= min
  );
customValidators.maxCheck = (max) =>
  helpers.withParams(
    { type: "maxCheck", max: max },
    (value) => !helpers.req(value) || value.length <= max
  );
customValidators.minMaxCheck = (min, max) =>
  helpers.withParams(
    { type: "minMaxCheck", min: min, max: max },
    (value) =>
      !helpers.req(value) || (min <= value.length && value.length <= max)
  );
customValidators.minMaxCheckNumberMask = (min, max) =>
  helpers.withParams(
    { type: "minMaxCheckNumberMask", min: min, max: max },
    function (value) {
      if (value) value = value.replace(/\D/g, "");
      return (
        !helpers.req(value) || (min <= value.length && value.length <= max)
      );
    }
  );
customValidators.cpfValidCheck = () =>
  helpers.withParams({ type: "cpfValidCheck" }, function (value) {
    if (value == undefined) value = "";
    value = value.replace(/\D/g, "");
    return validateCpf(value);
  });
customValidators.CNPJValidCheck = () =>
  helpers.withParams({ type: "CNPJValidCheck" }, function (value) {
    if (value == undefined) value = "";
    value = value.replace(/\D/g, "");
    return !helpers.req(value) || validCNPJ(value);
  });
customValidators.checkForCNPJConflicts = () =>
  helpers.withParams({ type: "checkForCNPJConflicts" }, function (value) {
    if (value == undefined) value = "";
    value = { company_federal_id: value };
    return !helpers.req(value) || validateCompanyData(value);
  });
customValidators.checkForEmailConflicts = () =>
  helpers.withParams({ type: "checkForEmailConflicts" }, function (value) {
    if (value == undefined) value = "";
    value = { email: value };
    return validateUserData(value);
  });
customValidators.isAfterDate = (valueInit) =>
  helpers.withParams(
    { type: "isAfterDate", valueInit: valueInit },
    (valueEnd) => !helpers.req(valueEnd) || valueInit <= valueEnd
  );

export default customValidators;
