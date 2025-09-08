<script setup>
import { useTemplateStore } from "@/stores/template";

// Main store
const store = useTemplateStore();
</script>

<template>
  <!-- Footer -->
  <footer id="page-footer">
    <slot>
      <div class="bg-body-light">
        <div class="content py-3">
          <div class="row fs-sm">
            <div class="col-sm-6 order-sm-2 py-1 text-center text-sm-end">
              <slot name="content-right">
                <img
                  class="img-avatar img-avatar32"
                  src="@/assets/img/sals.png"
                  alt="SALS"
                />
              </slot>
            </div>
            <div class="col-sm-6 order-sm-1 py-1 text-center text-sm-start">
              <slot name="content-left">
                <div class="fw-semibold">
                  &copy; {{ "SALS" + " " + store.app.version }}
                </div>
              </slot>
            </div>
          </div>
        </div>
      </div>
    </slot>
  </footer>
  <!-- END Footer -->
</template>
