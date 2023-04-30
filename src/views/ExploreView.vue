<script setup lang="ts">
  import { ref, onMounted } from 'vue'
  import ThePost from '../components/ThePost.vue'

  // fetch posts
  let posts:any = ref([]);
  let user_id:string  = localStorage['id'];
  
  let image = ref(new Blob());
  let caption = ref("");
  let post = ref(
    {
      id: user_id,
      image: image,
      caption: caption
    }
  );
  
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
        posts.value = [{
          username:"user",
          image_url:"/api/v1/1",
          caption:"test caption",
          likes:2,
          date:"2012-12-12",
        }];
    }

  });

</script>

<template>
  <main>
    <ThePost v-for="post, index in posts" v-bind:key="index" />
  </main>
</template>