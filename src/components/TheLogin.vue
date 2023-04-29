<template>
    <main> <div class="container col-sm-4">
        <div v-if="displayAlerts" :class="[(status=='success' || status=='error')? (( status!=='success' ) ? alertDanger : alertSuccess) : 'alert']">
            <ul v-if="status=='error'">
                <li v-for="(error, indx) in errors" v-bind:errors="errors" v-bind:key="indx">
                    {{ error }}
                </li>
            </ul>
            <span v-else>{{ message }}</span>
        </div>
        <LoginForm @fail="fail"/>
    </div> </main>
</template>

<script setup lang="ts">
    import LoginForm from './LoginForm.vue';
    import { ref } from 'vue';

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
</script>

