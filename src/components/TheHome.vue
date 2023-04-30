
<script setup lang="ts">

  async function get_image(file:string) {
    const response = await fetch("/api/v1/images/"+file, {
      method: 'GET',
      headers: {
        'Accept':'image/jpeg'
      }
    });

    if (response) {
      const src = 'data:image/jpg;base64,' + response;
      return src;
    } 

    return "";
  }
  
</script>

<template>
  
  <div class="container">
    <div id="home-photo" class="card home-card col-sm-6 no-gutters" style="float:left">
      <div class="card-image">
        <img id="home-card-photo" src="@/assets/images/home-card-image.jpg" alt="home page photo"/>
      </div>
    </div>

    <div id="home-actions" class="card home-card col-sm-6" style="float:right">
      <div class="card-body">
        <h1 class="card-title text-center">
          <!-- add camera icon -->
          <img id="camera"  class="camera-img" src="./icons/camera-24.png" alt="camera image">
          Photogram
        </h1>
        <hr>
        <p class="card-text">Share photos of your favorite moments with friends, family and the world.</p>
        <div class="buttons text-center">
          <a href="/register" class="card-link btn btn-success">Register</a>
          <a href="/login" class="card-link btn btn-primary">Login</a>
        </div>
      </div>
    </div>
  </div>
</template>

<style scope>
  @import url('https://fonts.googleapis.com/css2?family=Lobster');
  .card {
    width:48%;
    height: 350px;
  }

  .card-title {
    font-family: 'Lobster', sans-serif;
  }

  .btn {
    justify-content: center;
    width: 45%;
  }

  #camera {
    padding-bottom: 15px;
    padding-right: 10px;
  }

  #home-card-photo {
    width: 100% !important;
    height:350px !important;
    border-radius: 5px !important;
  }

  p {
    padding-bottom: 75px;
  }
</style>