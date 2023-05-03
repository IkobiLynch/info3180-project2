<template>
    <div class="photo col-sm-12 col-md-6 col-lg-4">
        <img class="container-fluid col-sm-12" :src="photo.url" alt="" @click="view">
    </div>
</template>
<script setup lang="ts">

    let prop = defineProps(['photo']);
    let emit = defineEmits(['click']);

    function view() {
        emit('click');
    }
    
</script>
<style scoped>
    img {
        width:100%;
        padding: 2px 2px;
    }
</style>