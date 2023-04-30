<script setup lang="ts">
  import { ref, onMounted } from 'vue'
  import ThePost from '../components/ThePost.vue'

  // fetch posts
  let posts:any = ref([]);
  let user_id:string  = localStorage['id'];
  
  let image_url = ref("/src/assets/images/home-card-image.jpg");
  let caption = ref("test caption...");
  let likes = ref("1");
  let date= ref("24 April 2018");

  let post = ref({
    username:"test_user",
    image_url:image_url,
    caption:caption,
    likes:likes,
    date:date
  });
  
  let url:string = `/api/v1/${user_id}/posts`; 

  function make_post() {
      if (user_id && user_id != "0") {
          console.log("make post function called");

          fetch(url, {
              method: 'POST',
              headers: {'token':`bearer ${localStorage['token']}`},
              body: JSON.stringify(post.value)
          })
          .then((result)=>{
              return result.json();
          })
          .then((data)=>{
              if (data.status_code == "200") {
                  console.log("post added successfully");
              }
              console.log("failed to add post");
          });
      }
  }

  onMounted(() => {
    if (user_id && user_id != "0") {
        fetch(url, {
            method: 'GET',
            headers: {
                token: `bearer ${localStorage['token']}`
          },
          body: JSON.stringify({id: user_id})
        })
        .then((result)=>{
            return result.json();
        })
        .then((data) => {
            // if status is 200, assign posts
            if (data.status_code == 200) {
              posts.value = data.data;
            }
        });
    } else {
      posts.value.push(post);
    }

  });

</script>

<template>
  <main>
    <ThePost v-for="(post, index) in posts" v-bind:post="post" v-bind:key="index" />
  </main>
</template>