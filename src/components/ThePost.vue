<template>
    <main>
        <div class="container col-sm-12 col-md-9">
            <div class="card post">
                <div class="header">
                    <div class="flex-start">
                        <img src="" alt="">
                        {{ post.value.username }}
                    </div>
                </div>
                <div class="card-image">
                    <img class="" :src="post.value.image_url" alt="post image">
                </div>
                <div class="card-body">
                    <p class="card-text">
                        {{ post.value.caption }}
                    </p>
                </div>
                <div class="container footer">
                    <span class="float-start">
                        <img src="" alt="">{{ post.value.likes }} likes
                    </span>
                    <span class="float-end">
                        {{ post.value.date }}
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

<style scope>
    .card {
        width: 100%;
    }

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