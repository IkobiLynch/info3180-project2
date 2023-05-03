<script setup lang="ts">
  import { ref, onMounted } from 'vue'
  import ThePost from '../components/ThePost.vue'
  import AppPost from '../components/AddPost.vue'
  import 'bootstrap'
  
  let id:Number  = Number(localStorage['id']);
  
  let posts:any = ref([]);
  let url:string = "/api/v1/posts";  
  
  // let addPostModal = bootstrap.Modal.getOrCreateInstance(document.querySelector('#add-post-modal'));
  let addPostModal = $('#add-post-modal');

  onMounted(() => {
    if (id && typeof id == 'number' && localStorage['token']) {
      // user is logged in on the frontend
        fetch(url, {
            method: 'GET',
            headers: {
                token: `bearer ${localStorage['token']}`
          }
        })
        .then((result)=>{
            return result.json();
        })
        .then((data) => {
            // if status is 200, assign posts
            if (data.status == "success") {
              posts.value = data.posts;
            } else {
              posts.value = []

            }
        });
    } else {
      // user isn' logged in 
    }

  });

</script>

<template>
  <main>
    <div class="container">
      <button v-if="id" value="new_post" class="new_post text-center btn btn-primary float-end sol-sm-3" @click="function(){addPostModal.show()}">New Post</button>
      <ThePost class="float-start col-sm-9" v-for="(post, index) in posts" v-bind:post="post" v-bind:key="index" />
      <AppPost />
    </div>
  </main>
</template>

<style scoped>
  .new_post {
    position:fixed;
    right:55px;
    width:215px;
  }

</style>