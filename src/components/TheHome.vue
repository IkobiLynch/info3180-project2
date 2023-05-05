
<script setup lang="ts">
</script>

<template>
  
  <div class="container">
    <div id="home-photo" class="card home-card no-gutters">
      <div class="card-image">
        <img id="home-card-photo" src="@/assets/images/home-card-image.jpg" alt="home page photo"/>
      </div>
    </div>

    <div id="home-actions" class="card home-card">
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

  @media (max-width:900px) {

    .container {
      display:flex;
      flex-direction:column;
    }

    #home-photo {
      width:100%;
    }

    #home-actions {
      width:100%;
    }
  }

  @media (min-width:900px) {

    .container {
      display: flex;
      flex-direction: row;;
    }
    #home-photo {
      width:45%;
      position: relative;
      float:left;
      margin-right:35px;
    }

    #home-actions {
      width:45%;
      position: relative;
      float:right;
    } 

    #home-card-photo {
      height:380px;
    }
  }

  .container {
    width:100% 
  }

  .card-title {
    font-family: 'Lobster', sans-serif;
  }

  .btn {
    justify-content: center;
    width:100%;
  }

  .buttons{
    width: 85%;
    display:flex;
    justify-content: center;
    flex-direction: column;
    margin: 5px auto;
    margin-bottom: 40px;
    }

  .buttons a {
    margin-left:5px;
    margin: 5px auto;
  }

  .btn-success {
    margin-bottom:15px;
  }

  #camera {
    padding-bottom: 15px;
    padding-right: 10px;
  }

  #home-card-photo {
    width: 100% !important;
    border-radius: 5px !important;
  }

  p {
    padding: 20px 10px;;
  }
</style>