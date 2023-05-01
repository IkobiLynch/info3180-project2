<template>
    <main>
        <div class="container">
            <UserStats v-bind:user="user" />
            <UserPhotos v-for="photo, index in photos" v-bind:photo="photo" v-bind:key="index" @click="launch(index)" />
        </div>
    </main>
</template>
<script setup lang="ts">
    import { ref, onMounted } from 'vue'
    import UserStats from '../components/UserStats.vue'
    import UserPhotos from '../components/UserPhotos.vue'

    let photos = ref([]);
    let user = ref({});
    let id:string = localStorage['id'];
    let url:string = `/api/v1/${id}/photos`;

    onMounted(() => {
        fetch(url,{
            method:'GET',
            headers:{
                'token':`bearer ${localStorage['token']}`
            }
        })
        .then((result)=>{
            return result.json();
        })
        .then((data)=>{
            if (data.status_code == 200) {
                photos = data.data;
            }
        });
    });

    function launch(index) {
        console.log(index);
    }

    function follow() {
        console.log("follow")
    }

</script>
<style scope></style>