<template>
    <main>
        <div class="card col-sm-12 col-md-9">
            <div class="card-header">
                <div class="profile_pic flex-start">
                    <img class="" :src="`../../uploads/${post.profile_photo}`" alt="profile_pic">
                    {{ post.username }}
                </div>
            </div>
            <div class="card-image">
                <img class="" :src="`../../uploads/${post.photo}`" alt="post image">
            </div>
            <div class="card-body">
                <p class="card-text">
                    {{ post.caption }}
                </p>
            </div>
            <div class="container footer">
                <span class="likes float-start">
                    <img src="../../uploads/full_heart.png" alt="like"/><small>{{ post.likes }} likes</small>
                </span>
                <span class="float-end">
                    <small>{{ post.created_on }}</small>
                </span>
            </div>
        </div>
    </main>

</template>

<script setup lang="ts">
    import { ref } from 'vue'
    let props = defineProps(['post']);
</script>

<style scoped>

    .card {
        width:80%;
        height:450px;
        margin-bottom:25px;
    }

    .card-header {
        height:fit-content;
        background-color: white;
        border:none;
    }

    .profile_pic img {
        width:24px;
    }

    .likes img {
        width:24px;
        padding-right:10px;
    }
    
    .card-image, .card-image img {
        width:100%;
        height:250px;
    }

    .card-body {
        height: 100%;
    }

    .card-text {
        height: 100%;
        margin-bottom:50px;
    }

    .footer {
        padding-bottom:10px;
    }

    .footer, .profile_pic {
        font-size: smaller;
        color:rgb(102, 102, 102);
        font-weight:700;
        font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif
    }

</style>