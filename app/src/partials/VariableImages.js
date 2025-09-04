import { ref } from "vue";

// Importando imagens diretamente
import quantidade_de_animais from "@/assets/img/quantidade-de-animais.png";
import cocho_vazio from "@/assets/img/cocho-vazio.png";
import baia_suja from "@/assets/img/baia-suja.png";
import variacao_de_tamanho_de_animais from "@/assets/img/variação-de-tamanho-de-animais.png";
import frequencia_de_roedores from "@/assets/img/frequência-de-roedores.png";
import movimentacao_de_animais from "@/assets/img/movimentação-de-animais.png";

const variableImages = ref([
  { src: quantidade_de_animais, alt: "Quantidade de Animais", selected: false, name: "quantidade_de_animais", value: "pig_count" },
  { src: cocho_vazio, alt: "Cocho Vazio", selected: false, name: "cocho_vazio" },
  { src: baia_suja, alt: "Baia Suja", selected: false, name: "baia_suja" },
  { src: variacao_de_tamanho_de_animais, alt: "Variação de Tamanho de Animais", selected: false, name: "variacao_de_tamanho_de_animais" },
  { src: frequencia_de_roedores, alt: "Frequência de Roedores", selected: false, name: "frequencia_de_roedores" },
  { src: movimentacao_de_animais, alt: "Movimentação de Animais", selected: false, name: "movimentacao_de_animais" }
]);

export default variableImages;
