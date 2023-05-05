<script setup >
  import { ref, onMounted } from 'vue'
  import ThePost from '../components/ThePost.vue'
  
  let id  = Number(localStorage['id']);
  
  let posts = ref([]);
  let url = "/api/v1/posts";  
  
  let photo = ref("");
  let caption = ref("");
  let preview = ref(false);
  let posturl = `/api/v1/users/${id}/posts`;
  
  let addPostModal = $('#addpostmodal');

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
    photo.value = URL.createObjectURL(document.querySelector('#photo').files[0]);
    preview.value=true;
  }


  function addPost() {
    if (id && typeof id == 'number') {
      console.log("make post function called");
      let form = new FormData($('form#addPostForm')[0]);

      fetch(posturl, {
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
            location.reload();
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

  function clear() {
    photo.value = "";
    preview.value = false;
    caption.value = "";
  }

</script>

<template>
  <main>
    <div class="container">
      <button 
        v-if="id" 
        @click="clear"
        type="button" 
        value="New Post" 
        class="new_post text-center btn btn-primary float-end" 
        data-toggle="modal" 
        data-target="#addpostmodal">
        New Post
      </button>
        <ThePost #default class="float-start" v-for="(post, index) in posts" v-bind:post="post" v-bind:key="index" v-on:like="like(index)" @unlike="unlike(index)" />   
        <div id="addpostmodal" class="modal fade">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="modalLabel"> Create Post</h5>
                    <button type="button" class="btn-close" data-dismiss="modal" aria-label="Close" @click="clear" >x</button>
                </div>
                <div class="modal-body">
                  <div v-if="preview" class="preview">
                    <img id="preview-image" :src="`${photo}`" alt="image preview"/>
                  </div>
                    <form id="addPostForm" action="" method="post" enctype="multipart/form-data">
                        <div class="form-group">
                            <input @change="loadPreview" accept="image/*" type="file" name="photo" id="photo" class="form-control" />
                        </div>
                        <div class="form-group">
                            <label for="caption">Caption</label>
                            <textarea v-model="caption" name="caption" id="caption" cols="30" rows="2" class="form-control"></textarea>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" 
                      v-on:click="addPost" 
                      class="btn btn-primary">
                        <img id="save" src="../components/icons/save.png" alt="save" class="text-white" />  
                        Save
                    </button>
                    <button 
                      type="button" 
                      class="btn btn-secondary"
                      @click="clear" 
                      data-dismiss="modal">
                        Close
                    </button>
                </div>
            </div>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>

  .preview {
    width: 100%;
    justify-content: center;
    margin:25px auto;
  }

  input[type="file"] {
    width: 110px;
    border: none;
    background-color: none;
  }
  .btn-close {
    border-width: 0;
    border-color: rgb(182, 98, 98);
    border-radius: 5px;
    background-color: rgb(182, 98, 98);
    color: rgb(64, 64, 64);
    font-weight: 600;
    font-family: monospace;
    margin-top:2px;
    margin-right:2px
  }

  .btn-close:hover {
    font-weight:800;
    border-color: brown;
    background-color: red;
    color:white;
    box-shadow: 1px 1px 3px black;
  }

  #save {
    width: 16px;
    margin-right:6px;
    margin-bottom:4px;
  }

  .new_post {
    position:relative;
    float:right;
    margin-right:20px;
    width:250px;
  }

  @media (max-width:900px) {
    .new_post {
      position:absolute;
      justify-content: center;
      width:85%;
      max-width:400px;
      top: 150px;
      left: auto;
      right:auto;
      float:none;
      margin-left:15px;
    }
  }

</style>