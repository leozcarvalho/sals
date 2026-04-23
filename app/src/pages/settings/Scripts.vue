<script setup>
import { reactive, ref, onMounted } from "vue";
import { ScriptsClient } from "../../services/scriptsApi";
import Loader from "../../components/Loader.vue";
import { handleApiToast } from "../../components/toast";

const scriptsApi = new ScriptsClient();
const loader = ref(null);

const result = ref(null);
const selectedScript = ref(null);
const scriptOptions = [
  { value: "script_1", label: "Script 1", params: [{ name: "data_base", type: "date", label: "Dia inicial" }, { name: "considerar_fracao_liquida", type: "checkbox", label: "Considerar Fração Líquida" }] },
  { value: "script_2", label: "Script 2", params: [{ name: "another_param", type: "string", label: "Param 1" }, { name: "extra_param", type: "boolean", label: "Param 2" }] },
];

const data = reactive({});
const exec = async () => {
  loader.value.loaderOn();
  const res = await scriptsApi.execScript(selectedScript.value, data);
  result.value = res.data || null;
  handleApiToast(res, "Scripts executados com sucesso!");
  loader.value.loaderOff();
};
</script>

<template>
  <Loader ref="loader" />
  <div class="content">
    <BaseBlock title="Scripts" content-full>
      <div class="mb-3">
        <div>
          <select v-model="selectedScript" class="form-select">
            <option value="" disabled>Selecione um script</option>
            <option v-for="option in scriptOptions" :key="option.value" :value="option.value">{{ option.label }}
            </option>
          </select>
        </div>
        <div class="mt-3" v-if="selectedScript">
          <div v-for="param in scriptOptions.find(opt => opt.value === selectedScript).params" :key="param.name">

            <!-- INPUT NORMAL -->
            <input v-if="param.type !== 'checkbox'" :type="param.type" class="form-control mb-2"
              v-model="data[param.name]" :placeholder="param.label" />

            <!-- CHECKBOX -->
            <div v-else class="form-check mb-2">
              <input type="checkbox" class="form-check-input" v-model="data[param.name]" :id="param.name" />
              <label class="form-check-label" :for="param.name">
                {{ param.label }}
              </label>
            </div>

          </div>
          <div class="col-3">
            <button class="btn btn-secondary" data-bs-toggle="modal" data-bs-target="#modal-confirm">Executar
              Script</button>
          </div>
        </div>
      </div>
      <div>
        <div v-for="(rows, groupName) in result" :key="groupName" class="mb-4">
          <h5 class="mb-2 text-capitalize border-bottom pb-1">
            {{ groupName.replaceAll('_', ' ') }}
          </h5>

          <div class="table-responsive" v-if="rows && rows.length">

            <table class="table table-striped table-sm">

              <!-- HEADER -->
              <thead>
                <tr>
                  <th v-for="(value, key) in rows[0]" :key="key">
                    {{ key }}
                  </th>
                </tr>
              </thead>

              <!-- BODY -->
              <tbody>
                <tr v-for="(row, rowIndex) in rows" :key="rowIndex">
                  <td v-for="(value, key) in row" :key="key">
                    {{ value }}
                  </td>
                </tr>
              </tbody>

            </table>

          </div>

          <div v-else class="text-muted">
            Sem dados
          </div>

        </div>
      </div>
    </BaseBlock>
    <div class="modal fade" id="modal-confirm" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">Confirmar Ação</div>
          <div class="modal-body">Executar script</div>
          <div class="modal-footer">
            <button class="btn btn-secondary" data-bs-dismiss="modal">CANCELAR</button>
            <button class="btn btn-danger" data-bs-dismiss="modal" @click="exec">CONFIRMAR</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>