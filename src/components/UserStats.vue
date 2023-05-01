<template>
    <div class="container stats">
        <div class="card">
            <div class="card-body">
                <div class="image">
                    <img :src="user.value.image_url" alt="user avatar">
                </div>
                <div class="details">
                    <h5 class="h5">{{ user.value.name }}</h5>
                    <p>
                        {{ user.value.city }}, {{ user.value.country }}
                        <br>
                        Member since {{ user.value.date }}
                    </p>
                </div>
                <div class="following">
                    <span class="float-left">{{ user.posts }}<br/>Posts</span>
                    <span class="float-right">{{ user.followers }}<br/>Followers</span>
                    <button id="follow-btn" class="btn btn-primary" @click="follow">Follow</button>
                </div>
            </div>
        </div>

    </div>
</template>
<script setup lang="ts">
    import { ref } from 'vue'

    let prop = defineProps(['user']);
    let emit = defineEmits(['follow']);

    function follow() {
        emit('follow');
    }
</script>
<style scope>
    .card-body {
        display: flex;
        flex-direction: row;
    }
</style>