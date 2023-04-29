<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
      <div class="container-fluid">
        <div class="brand">
          <a class="navbar-brand" href="/"><img class="camera-img" src="./icons/camera-16.png" alt="camera image"> Photogram</a>
        </div>
        <div class="menu float-end">
          <button
            class="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto">
              <li>
                <RouterLink class="text-white" to="/">Home</RouterLink>
              </li>
              <li>
                <RouterLink class="text-white" to="/explore">Explore</RouterLink>
              </li>
              <li v-if="login" >
                <RouterLink class="text-white" v-bind:id='id' to="{name:'profile', params:{user_id:id}}">My Profile</RouterLink>
              </li>
              <li v-if="login" >
                <RouterLink class="text-white" to="/logout">Logout</RouterLink>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup lang="ts">
  import { RouterLink } from "vue-router";
  let login:boolean = localStorage['token']? true : false;
  let id: number = localStorage['id'] ?? 0;
</script>

<style>
  /* Add any component specific styles here */
  @import url('https://fonts.googleapis.com/css2?family=Lobster');
  .navbar-brand {
    font-family: 'Lobster', sans-serif;
  }

  .camera-img {
    padding-bottom: 10px;
    padding-right: 6px;
  }
  header {
    margin-bottom: 200px;
  }

  a {
    text-decoration-line: none;
    -moz-text-decoration-line: none;
  }

  ul.nav li a, ul.nav li a:visited {
    color: white !important;
  }

  li {
    width:70px;
    /* margin-left: 20px; */
  }

  .menu {
    margin-right:35px;
  }

  a:hover {
    font-weight: bold;
  }
</style>