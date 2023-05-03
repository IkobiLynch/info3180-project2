<template>
    <div class="container stats">
        <div class="card">
            <div class="card-body col-sm-12 flex-row">
                <div class="image col-sm-2">
                    <img class="col-sm-12" :src="`../../uploads/${user.image_url}`" alt="user avatar">
                </div>
                <div class="details col-sm-7 flex-column">
                    <h5 class="h5 card-title">{{ user.firstname }} {{ user.lastname }}</h5>
                    <p>
                        <small>
                            {{ user.location }}
                        </small>
                    </p>
                    <p>
                        <small>
                            Member since {{ user.date }}
                        </small>
                    </p>
                    <p>
                        <small>
                            {{ user.biography }}
                        </small>
                    </p>
                </div>
                <div class="flex-column col-sm-3">
                    <div class="following">
                        <div id="posts" class="socials float-left">
                            <span class="small">{{ user.posts }}</span>
                            <span class="h6">Posts</span>
                        </div>
                        <div id="followers" class="socials float-right">
                            <span class="small">{{ user.followers }}</span>
                            <span class="h6">Followers</span>
                        </div>
                    </div>
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
<style scoped>
    .card-body, .following {
        display: flex;
        flex-direction: row;
    }

    .image {
        padding: 0 15px 0 0;
        margin:auto;
    }

    .card {
        height: fit-content;
        box-shadow: 2px 2px 2px gray;
    }

    .following {
        text-align: center;
    }

    .socials {
        width: 45%;
        display:flex;
        flex-direction: column;
        padding: 1px 1px;
    }

    #follow-btn {
        margin-top: 50px;
        width: 100%;
    }
</style>