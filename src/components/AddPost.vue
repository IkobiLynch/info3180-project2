<template>
    <div id="add-post-modal" class="modal fade" tabindex="-1" role="dialog" aria-labelledby="modalLabel" aria-hidden="false">
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
                    <button type="button" v-on:click="addPost" class="btn btn-primary"><img src="./icons/save.png" />  Add Movie</button>
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { ref } from 'vue'
    let id:Number  = Number(localStorage['id']);
    let emit = defineEmits(["hide"]);
    let photo = ref("");

    let url:string = `/api/v1/users/${id}/posts`;

    function loadPreview() {
        photo.value = "";
    }

    function addPost() {
      if (id && typeof id == 'number') {
          console.log("make post function called");
          let form = new FormData($('form'));

          fetch(url, {
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

</script>