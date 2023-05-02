<template>
    <main>
        <div class="container">
            <UserStats v-bind:user="user" />
            <UserPhotos v-for="photo, index in posts" v-bind:photo="photo" v-bind:key="index" @click="view(index)" />
        </div>
    </main>
</template>
<script setup lang="ts">
    import { ref, onMounted } from 'vue'
    import UserStats from '../components/UserStats.vue'
    import UserPhotos from '../components/UserPhotos.vue'
    let emit = defineEmits(['logout'])

    let posts = ref([]);
    let user = ref({});
    let id:string = localStorage['id'];
    let posts_url:string = `/api/v1/users/${id}/posts`;
    let user_url:string = `/api/v1/users/${id}`;

    onMounted(() => {
        fetch(posts_url,{
            method:'GET',
            headers:{
                'Authorisation':`bearer ${localStorage['token']}`
            }
        })
        .then((result)=>{
            return result.json();
        })
        .then((data)=>{
            if (data.status_code == 200) {
                posts = data.data;
            }
        });

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
                let city = data.location;
                let country = data.location;
                let date = data.date;
                let posts = data.posts;
                let followers = data.followers;
                let biography = data.biography;
                user.value = {
                    image_url: image_url,
                    firstname: firstname,
                    lastname: lastname,
                    city: city,
                    country: country,
                    date: date,
                    posts: posts,
                    followers: followers,
                    biography: biography
                }
            } else {
                if (json_obj.type) {
                    emit('logout')
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
<style scope></style>