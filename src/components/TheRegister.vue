<template>
    <main>
        <div class="container col-sm-6">
            <h5>Register</h5>
            <div class="form">
                <form action="/api/v1/register" id="register" method="POST">
                    <div class="form-group">
                        <label for="username">Username</label>
                        <input id="username" name="username" type="text" class="form-control">
                    </div>
                    <div class="form-group">
                        <label for="password">Password</label>
                        <input id="password" name="password" type="password" class="form-control">
                    </div>
                    <div class="form-group">
                        <label for="fname">FirstName</label>
                        <input id="fname" name="fname" type="text" class="form-control">
                    </div>
                    <div class="form-group">
                        <label for="lname">LastName</label>
                        <input id="lname" name="lname" type="text" class="form-control">
                    </div>
                    <div class="form-group">
                        <label for="email">Email</label>
                        <input id="email" name="email" type="email" class="form-control">
                    </div>
                    <div class="form-group">
                        <label for="location">Location</label>
                        <input id="location" name="location" type="text" class="form-control">
                    </div>
                    <div class="form-group">
                        <label for="biography">Biography</label>
                        <input id="biography" name="biography" type="textarea" class="form-control">
                    </div>
                    <div class="form-group">
                        <label for="photo">Photo</label>
                        <input id="photo" name="photo" type="file" class="form-control">
                    </div>
                    <button @click="register" class="btn btn-primary">Register</button>
                </form>
            </div>
        </div>
    </main>
</template>

<script setup lang="ts">

    // let registration_form = new FormData(document.querySelector('#register'));

    function register() {
        console.log("registration form");
        let form = new FormData($('#register'));
        let url:string = "/api/v1/user.value.id/follow"

        fetch(url, {
            method: 'POST',
            headers: {
                'Authentication': `bearer ${localStorage['token']}`
            },
            body: form
        })
        .then(result => result.json())
        .then((data) => {
            if (data.status_code==200) {
                console.log('user followed');
            } else {
                console.log('failed to follow user');
            }
        })
    }
</script>

<style scope>
    .btn {
        margin-top: 25px;
        width:100%;
    }

    h5 {
        margin-bottom: 20px;
    }

    .form {
        background-color: white;
        box-shadow:5px 5px 10px gray;
        margin-bottom: 30px;
        border-radius: 5px;
    }

    .form-group {
        margin-top: 15px;
    }

    #biography {
        height: 4rem;
    }

    #register {
        padding:15px;
    }
</style>