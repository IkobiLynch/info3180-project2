<template>
    <main> <div class="container col-sm-8 col-lg-5">
        <div v-if="displayAlerts" :class="[(status=='success' || status=='error')? (( status!=='success' ) ? alertDanger : alertSuccess) : 'alert']">
            <ul v-if="status=='error'">
                <li v-for="(error, indx) in errors" v-bind:errors="errors" v-bind:key="indx">
                    {{ error }}
                </li>
            </ul>
            <span v-else>{{ message }}</span>
        </div>
        <LoginForm :id="id" v-if="!id" @success='success' @fail="fail"/>
    </div> </main>
</template>

<script setup lang="ts">
    import LoginForm from './LoginForm.vue';
    import { ref } from 'vue';

    let id:string = localStorage['id'];

    if (localStorage['id']) {
        window.location.replace(`/users/${id}`)
    } 

    let displayAlerts = ref(false);
    let status = ref("");
    let errors = ref([""]);
    let message = ref("");
    const alertDanger: string = "alert alert-success";
    const alertSuccess: string = "alert alert-dander";

    function fail(e: string[], m: string) {
        status.value = "error";
        errors.value = e;
        message.value = m;
    }

    function success() {
        location.replace(`/users/${localStorage['id']}`)
    }
</script>

