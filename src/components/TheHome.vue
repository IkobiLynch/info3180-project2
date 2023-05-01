
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
  
  <div class="container col-sm-10 col-lg-12">
    <div id="home-photo" class="card home-card no-gutters float-left">
      <div class="card-image">
        <img id="home-card-photo" src="@/assets/images/home-card-image.jpg" alt="home page photo"/>
      </div>
    </div>

    <div id="home-actions" class="card home-card float-right">
      <div class="card-body text-center">
        <h1 class="card-title">
          <img id="camera"  class="camera-img" src="./icons/camera-24.png" alt="camera image">
          <!-- add camera icon -->
          Photogram
        </h1>
        <hr>
        <p class="card-text">Share photos of your favorite moments with friends, family and the world.</p>
      </div>
      <div class="buttons text-center">
          <a href="/register" class="card-link btn btn-success">Register</a>
          <a href="/login" class="card-link btn btn-primary">Login</a>
      </div>
    </div>
  </div>
</template>

<style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Lobster');
  .container {
    min-width: 560px;
    display:flex; 
  }

  .card {
    width:45%;
    height: 450px;
    margin-bottom:45px;
  }

  .card-body {
    display:flex;
    flex-direction: column;
  }

  .float-left {
    margin-right:10px;
  }

  .card-title {
    font-family: 'Lobster', sans-serif;
  }

  .btn {
    justify-content: center;
    width:100%;
  }

  .buttons a {
    margin-left:5px;
  }

  @media only screen and (max-width: 600px) {
    .btn {
      width: 90%;
      margin-left:10px;
    }

    .buttons{
      display:flex;
      flex-direction: column;
      margin-bottom: 40px;
    }
  }

  @media only screen and (min-width: 601px) {
    .btn {
      width: 45%;
      margin-bottom: 40px;
      margin-right:5px;
    }
  }

  #camera {
    padding-bottom: 15px;
    padding-right: 10px;
  }

  #home-card-photo {
    width: 100% !important;
    height:450px !important;
    border-radius: 5px !important;
  }

  p {
    padding: 20px 10px;;
  }
</style>