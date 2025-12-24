<script setup>
import { reactive, ref, computed, watch, defineExpose } from "vue";
import useVuelidate from "@vuelidate/core";
import {
  required,
  email,
  minLength,
  maxLength,
  minValue,
  maxValue,
  helpers,
} from "@vuelidate/validators";
import { vMaska } from "maska";
import Loader from "@/components/Loader.vue";
import { handleApiToast } from "@/components/toast";

// =============== Props & Emits ===============
const props = defineProps({
  modelValue: { type: Object, default: () => ({}) }, // dados iniciais (edição)
  fields: { type: Array, required: true },           // array de FieldConfig
  api: { type: Object, required: true },             // { save(data), update(id, data) }
  idField: { type: String, default: "id" },          // nome do campo id
  title: { type: String, default: "Editar / Criar" },
  extraPayload: { type: Object, default: () => ({}) }, // dados extras para enviar na criação
});

const emit = defineEmits([
  "update:modelValue",
  "saved",
  "close",
  "create",
  "edit"
]);

// =============== Estado do Form ===============
const isLoading = ref(false);
const form = reactive({});

// popular inicialmente + defaults dos fields
const ensureInitialState = (forNew = false) => {
  props.fields.forEach((f) => {
    if (f.skipInit) return;
    const key = f.name;

    // Se for criação (forNew=true), ignora modelValue
    if (!forNew && props.modelValue?.hasOwnProperty(key)) {
      form[key] = props.modelValue[key];
    } else if (f.hasOwnProperty("default")) {
      form[key] = typeof f.default === "function" ? f.default() : f.default;
    } else {
      form[key] = f.multiple ? [] : f.type === "checkbox" ? false : null;
    }
  });

  // garante que o idField esteja correto
  if (!forNew && props.modelValue?.[props.idField]) {
    form[props.idField] = props.modelValue[props.idField];
  } else {
    form[props.idField] = null;
  }
};
ensureInitialState();

watch(
  () => props.modelValue,
  (val) => {
    ensureInitialState();
    if (val) {
      Object.keys(val).forEach((k) => {
        if (form.hasOwnProperty(k)) form[k] = val[k];
      });
    }
  },
  { deep: true, immediate: true }
);

// =============== Normalização de Regras ===============
// Mapa de validators disponíveis (expanda conforme precisar)
const validatorMap = {
  required,
  email,
  minLength,
  maxLength,
  minValue,
  maxValue,
};

const defaultMessages = {
  required: "Campo obrigatório",
  email: "E-mail inválido",
  minLength: (ctx) => `Mínimo de ${ctx.$params.min} caracteres`,
  maxLength: (ctx) => `Máximo de ${ctx.$params.max} caracteres`,
  minValue: (ctx) => `O valor mínimo é ${ctx.$params.min}`,
  maxValue: (ctx) => `O valor máximo é ${ctx.$params.max}`,
};

// aplica mensagem custom ou padrão
const withMsg = (msg, v, name) => {
  if (msg) {
    return helpers.withMessage(msg, v);
  }

  // se houver default no dicionário
  if (defaultMessages[name]) {
    const def = defaultMessages[name];
    if (typeof def === "function") {
      return helpers.withMessage((ctx) => def(ctx), v);
    }
    return helpers.withMessage(def, v);
  }
  return helpers.withMessage("Campo inválido", v);
};

// converte "minLength:3" -> { name: 'minLength', args: [3] }
function parseRuleString(str) {
  if (!str) return null;
  if (str.includes(":")) {
    const [name, rawArgs] = str.split(":");
    const args = rawArgs
      .split(",")
      .map((a) => {
        const n = Number(a.trim());
        return isNaN(n) ? a.trim() : n;
      });
    return { name: name.trim(), args };
  }
  const m = str.match(/^(\w+)\((.*)\)$/);
  if (m) {
    const name = m[1];
    const args = m[2]
      .split(",")
      .map((a) => {
        const n = Number(a.trim());
        return isNaN(n) ? a.trim() : n;
      });
    return { name, args };
  }
  return { name: str.trim(), args: [] };
}

// transforma a definição de regras em objeto aceito pelo Vuelidate
function buildRulesForField(field) {
  const out = {};
  if (!field.rules) return out;

  const messages = field.messages || {}; // { required: "msg...", minLength: "..." }

  // 1) Array (strings | funções | objetos)
  if (Array.isArray(field.rules)) {
    field.rules.forEach((item, idx) => {
      if (typeof item === "function") {
        out[`r${idx}`] = item;
      } else if (typeof item === "string") {
        const parsed = parseRuleString(item);
        if (!parsed) return;
        const base = validatorMap[parsed.name];
        if (!base) return;
        const v = parsed.args?.length ? base(...parsed.args) : base;
        out[parsed.name] = withMsg(messages[parsed.name], v, parsed.name);
      } else if (item && typeof item === "object") {
        // ex.: { minLength: 3 } ou { minLength: { value: 3, message: "..." } }
        Object.entries(item).forEach(([name, val]) => {
          const base = validatorMap[name];
          if (!base) return;
          let v;
          let msg = messages[name];
          if (typeof val === "object" && val !== null) {
            const args = Array.isArray(val.value)
              ? val.value
              : val.value !== undefined
                ? [val.value]
                : val.args || [];
            msg = val.message || msg;
            v = args.length ? base(...args) : base;
          } else if (val === true || val === undefined) {
            v = base;
          } else {
            v = base(val);
          }
          out[name] = withMsg(msg, v, name);
        });
      }
    });
    return out;
  }

  // 2) Objeto simples: { required: true, minLength: 3 }
  if (typeof field.rules === "object") {
    Object.entries(field.rules).forEach(([name, val]) => {
      const base = validatorMap[name];
      if (!base) return;
      let v;
      let msg = messages[name];
      if (typeof val === "object" && val !== null) {
        const args = Array.isArray(val.value)
          ? val.value
          : val.value !== undefined
            ? [val.value]
            : val.args || [];
        msg = val.message || msg;
        v = args.length ? base(...args) : base;
      } else if (val === true || val === undefined) {
        v = base;
      } else {
        v = base(val);
      }
      out[name] = withMsg(msg, v, name);
    });
    return out;
  }

  // 3) String única: "required" | "minLength:3"
  if (typeof field.rules === "string") {
    const parsed = parseRuleString(field.rules);
    if (parsed) {
      const base = validatorMap[parsed.name];
      if (base) {
        const v = parsed.args?.length ? base(...parsed.args) : base;
        out[parsed.name] = withMsg(messages[parsed.name], v, parsed.name);
      }
    }
  }

  return out;
}

const rules = computed(() => {
  const r = {};
  props.fields.forEach((f) => {
    r[f.name] = buildRulesForField(f); // sempre cria uma chave (evita undefined)
  });
  return r;
});

const v$ = useVuelidate(rules, form);

const loader = ref(null);

// =============== Ações ===============
const submit = async () => {
  loader.value.loaderOn();
  v$.value.$touch();
  const valid = await v$.value.$validate();
  if (!valid) {
    loader.value.loaderOff();
    return;
  }
  let res;
  const formData = { ...form, ...props.extraPayload };
  if (form[props.idField]) {
    res = await props.api.update(form[props.idField], formData);
  } else {
    res = await props.api.save(formData);
  }
  handleApiToast(res, "Alterações salvas com sucesso");
  if (res?.success) {
    emit("saved", res.data ?? form);
    closeModal()
  }
  loader.value.loaderOff();
};

const openModal = (isNew = false) => {
  ensureInitialState(isNew);
  v$.value.$reset();
  let modal = new bootstrap.Modal(document.getElementById("modal-form"));
  modal.show();
  emit(isNew ? "create" : "edit", form);
};

defineExpose({
  openModal,
});

const closeModal = () => {
  ensureInitialState(false);
  v$.value.$reset();
  const modalEl = document.getElementById("modal-form");
  const modal = bootstrap.Modal.getInstance(modalEl);
  if (modal) modal.hide();
  emit("close");
};

</script>

<template>
  <Loader ref="loader" />
  <div class="modal fade" id="modal-form" tabindex="-1" role="dialog" aria-labelledby="modal-form" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-dialog-popin modal-lg" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ form[props.idField] ? 'Editar' : 'Criar' }}</h5>
          <button type="button" class="btn-close" @click="closeModal"></button>
        </div>

        <div class="modal-body">
          <div v-for="field in fields" :key="field.name" class="mb-3">
            <!-- Label -->
            <label v-if="field.type !== 'checkbox'" class="form-label">
              {{ field.label }}
            </label>

            <!-- Slot dinâmico (template custom) -->
            <slot v-if="field.slot" :name="field.slot" :field="field" :model="form" :v="v$" />

            <!-- Componente custom (ex.: VAsyncSelect) -->
            <component v-else-if="field.component" :is="field.component" v-model="form[field.name]" v-bind="field.props"
              :class="[
                field.class,
                { 'is-invalid': v$?.[field.name]?.$error && field.addInvalidClass !== false }
              ]" @blur="v$?.[field.name]?.$touch()" />

            <!-- Tipos básicos -->
             
            <input v-else-if="['text', 'email', 'number', 'password', 'date', 'tel'].includes(field.type)"
              v-model="form[field.name]" :type="field.type" class="form-control" :placeholder="field.placeholder"
              :disabled="field.disabled" v-maska :data-maska="field.mask" :class="{ 'is-invalid': v$?.[field.name]?.$errors.length }"
              @blur="v$?.[field.name]?.$touch" />

            <textarea v-else-if="field.type === 'textarea'" v-model="form[field.name]" class="form-control"
              :rows="field.rows || 3" :placeholder="field.placeholder" :disabled="field.disabled"
              :class="{ 'is-invalid': v$?.[field.name]?.$error }" @blur="v$?.[field.name]?.$touch()" />

            <select v-else-if="field.type === 'select'" v-model="form[field.name]" class="form-select"
              :disabled="field.disabled" :class="{ 'is-invalid': v$?.[field.name]?.$error }"
              @blur="v$?.[field.name]?.$touch()">
              <option v-for="opt in field.options || []" :key="opt.value" :value="opt.value">
                {{ opt.label }}
              </option>
            </select>
            <VAsyncSelect v-if="field.type === 'async-select'" :entity="field.entity" v-model="form[field.name]" :pre-filled-value="form[field.name]" />
            <div v-else-if="field.type === 'checkbox'" class="form-check">
              <input v-model="form[field.name]" type="checkbox" class="form-check-input" :id="field.name"
                @change="v$?.[field.name]?.$touch()" />
              <label class="form-check-label" :for="field.name">{{ field.label }}</label>
            </div>
            <div v-if="v$?.[field.name]?.$errors.length" class="invalid-feedback d-block">
              {{
                v$[field.name].$errors?.[0]?.$message
                || field.errorMessage
                || "Campo inválido"
              }}
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-danger btn-lg" @click="closeModal">Cancelar</button>
          <button type="button" class="btn btn-success btn-lg" @click="submit">Salvar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// registra diretiva localmente quando usar via <script> clássico
export default {
  directives: { maska: vMaska },
};
</script>

<style scoped>
.form-control.is-invalid,
.form-select.is-invalid {
  /* mantém comportamento visual do bootstrap */
}
</style>
