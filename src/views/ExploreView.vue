<script setup >
  import { ref, onMounted } from 'vue'
  import ThePost from '../components/ThePost.vue'
  // import AppPost from '../components/AddPost.vue'
  
  let id  = Number(localStorage['id']);
  
  let posts = ref([]);
  let url = "/api/v1/posts";  

  let photo = ref("");
  let posturl = `/api/v1/users/${id}/posts`;
  
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

  function loadPreview() {
      photo.value = "";
  }

  function openModal() {
    addPostModal.show();
    // addPostModal.modal('show');
  }

  async function addPost() {
    if (id && typeof id == 'number') {
      console.log("make post function called");
      let form = new FormData($('form#add-post-form')[0]);

      await fetch(posturl, {
          method: 'POST',
          headers: {'token':`bearer ${localStorage['token']}`},
          body: form
      })
      .then((result)=>{
          return result.json();
      })
      .then((data)=>{
          if (data.status == "success") {
            console.log("post added successfully");
            $('form').hide();
          } else {
              console.log("failed to add post");
          }
      });
    }
  }

  function like(index) {
    if (id) {
      let post_id = posts.value[index].id;
      let like_url = `/api/v1/like/${post_id}`;

      fetch(like_url, {
        method:"POST",
        headers:{"Authorization": `bearer ${localStorage['token']}`}
      })
      .then(result => result.json())
      .then((data) => {
        if (data.status !== "success") {
          window.location.assign("/login");
        } else {
          // update local posts using index
          posts.value[Number(index)]['liked'] = true;
          posts.value[Number(index)]['likes'] += 1;
          console.log("post liked");
        }

      });
    } else {
      window.location.assign("/login");
    }
  }

  function unlike(index) {
    if (id) {
      let post_id = posts.value[index].id;
      let unlike_url = `/api/v1/unlike/${post_id}`;

      fetch(unlike_url, {
        method:'POST',
        headers:{
          'Authorization': `bearer ${localStorage['token']}`
        }
      })
      .then((result) => {
        return result.json();
      })
      .then((data) => {
        if (data.status=="success") {
          // reduce likes count for post
          posts.value[index]['likes'] -= 1;
          posts.value[index]['liked'] = false;
          console.log("post unliked");
        } else {
          window.location.assign("/login");
        }
      });
    } else {
      window.location.assign("/login");
    }
  }

</script>

<template>
  <main>
    <div class="container">
      <button v-if="id" value="new_post" class="new_post text-center btn btn-primary float-end col-sm-3" @click="openModal">New Post</button>
      <ThePost class="float-start col-sm-9" v-for="(post, index) in posts" v-bind:post="post" v-bind:key="index" v-on:like="like(index)" @unlike="unlike(index)" />

      <div id="add-post-modal" class="modal fade" tabindex="-1" role="dialog" aria-labelledby="modalLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="modalLabel"> Create Post</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <img id="preview-image" :src="`${photo}`" alt="image preview"/>
                    <form id="add-post-form" action="" method="post" enctype="multipart/form-data">
                        <div class="form-group">
                            <label for="photo">Image</label>
                            <input @change="loadPreview" type="file" name="photo" id="photo" class="form-control" />
                        </div>
                        <div class="form-group">
                            <label for="caption">Caption</label>
                            <textarea value="" name="caption" id="caption" cols="30" rows="5" class="form-control"></textarea>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" v-on:click="addPost" class="btn btn-primary"><img src="../components/icons/save.png" alt="save" />  Add Movie</button>
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
  .new_post {
    position:fixed;
    left:600px;
    right:55px;
    width:285px;
  }

  @media (max-width:900px) {
    .new_post {
      position:absolute;
      justify-content: center;
      width:400px;
      top: 150px;
      left: auto;
      right:auto;
      float:none;
      margin-left:10px;
    }
  }

</style>