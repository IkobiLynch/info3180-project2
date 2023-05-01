<script setup lang="ts">
  import TheHome from '../components/TheHome.vue'
  import UserProfile from '../components/UserProfile.vue'
  let id = localStorage['id'];
  if(id) {
    window.location.replace(`users/${id}`);
  }
</script>

<template>
  <main>
    <Suspense>
      <TheHome v-if="!id" :id="id" />
    </Suspense>
  </main>
</template>
