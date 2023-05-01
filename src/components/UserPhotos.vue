<template>
    <div class="photo col-sm-12 col-md-6 col-lg-4">
        <img :src="photo.value.url" alt="" @click="view">
    </div>
</template>
<script setup lang="ts">

    let prop = defineProps(['photo']);
    let emit = defineEmits(['click']);

    function view() {
        emit('click');
    }
    
</script>
<style scope></style>