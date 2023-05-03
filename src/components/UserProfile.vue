<template>
    <UserStats v-bind:user="user" />
    <UserPhotos v-for="photo, index in photos" v-bind:photo="photo" v-bind:key="index" @click="view(index)" />
</template>
<script setup lang="ts">
    import { ref, onMounted } from 'vue'
    import UserStats from '../components/UserStats.vue'
    import UserPhotos from '../components/UserPhotos.vue'
    let emit = defineEmits(['logout']);

    let photos = ref([]);
    let user = ref({});
    let id:string = localStorage['id'];

    
    onMounted(() => {
        let user_url:string = `/api/v1/users/${id}`;

        fetch(user_url,{
            method:'GET',
            headers:{
                'Authorization':`bearer ${localStorage['token']}`
            }
        })
        .then((result)=>{
            return result.json();
        })
        .then((json_obj)=>{
            if (json_obj.status == "success") {
                let data = json_obj.user;
                let image_url = data.image_url;
                let firstname = data.firstname;
                let lastname = data.lastname;
                let location = data.location;
                let date = data.date;
                let posts = data.posts;
                let followers = data.followers;
                let biography = data.biography;
                photos.value = json_obj.photos;
                user.value = {
                    image_url: image_url,
                    firstname: firstname,
                    lastname: lastname,
                    location: location,
                    date: date,
                    posts: posts,
                    followers: followers,
                    biography: biography
                }
            } else {
                if (json_obj.type) {
                    emit('logout');
                }
            }
        });
    });

    function view(index) {
        console.log(index);
    }

    function follow() {
        console.log("follow")
    }

</script>
