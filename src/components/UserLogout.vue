<script setup lang="ts">
    const url: string = "/api/v1/auth/logout";
    fetch(url, {
        method: 'GET',
        headers: {
            // 'Accept': 'application/json',
            // 'Content-Type': 'application/json',
            'Authentication': `Bearer ${localStorage['token']}`
        }
    })
    .then((result)=>{
        const res = JSON.parse(JSON.stringify(result)) || result.json();
        if (res.status == 400) {
            // update the token
            localStorage.removeItem('token');
        }
    });
</script>

<template>
    <main></main>
</template>

<style></style>