<template>
  <div class="form-check">
    <input class="form-check-input" type="checkbox" :id="category" :value="category" :checked="isChecked"
      @click="$emit('updateFavourites', category)" />
    <label class="form-check-label" :for="category">{{ category }}</label>
  </div>
</template>

<script lang="ts">
export default {
  props: ['category', 'isChecked'],
}
</script>

<style scoped></style>
