<template>
    <main>
        <div class="container col-sm-10 col-md-12">
            <div v-bind:post="post" class="card post">
                <div class="header">
                    <div class="flex-start">
                        <img src="" alt="">
                        { post.username }
                    </div>
                </div>
                <div class="card-image">
                    <img class="" src="{ post.image_url }" alt="post image">
                </div>
                <div class="card-body">
                    <p class="card-text">
                        { post.caption }
                        
                    </p>
                </div>
                <div class="footer">
                    <span class="float-start">
                        <img src="" alt="">{ post.likes } likes
                    </span>
                    <span class="float-end">
                        { post.date }
                    </span>
                </div>
            </div>
        </div>
    </main>

</template>

<script setup lang="ts">
    import { ref } from 'vue'
    let props = defineProps(['post']);
</script>

<style>
    .card-header {
        height:fit-content;
    }

    .card-image, .card-image img {
        width:100%;
        height:200px;
    }

    .card-body {
        height: 6rem;
    }

    .card-text {
        height: 5rem;
    }

</style>