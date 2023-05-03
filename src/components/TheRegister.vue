<template>
    <main>
        <div class="container col-sm-6">
            <h5>Register</h5>
            <div class="form">
                <form id="register" enctype="multipart/form-data" method="POST">
                    <div class="form-group">
                        <label for="username">Username</label>
                        <input id="username" name="username" type="text" class="form-control">
                    </div>
                    <div class="form-group">
                        <label for="password">Password</label>
                        <input id="password" name="password" type="password" class="form-control">
                    </div>
                    <div class="form-group">
                        <label for="firstname">FirstName</label>
                        <input id="firstname" name="firstname" type="text" class="form-control">
                    </div>
                    <div class="form-group">
                        <label for="lastname">LastName</label>
                        <input id="lastname" name="lastname" type="text" class="form-control">
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
                        <label for="profile_photo">Photo</label>
                        <input id="profile_photo" name="profile_photo" type="file" class="form-control">
                    </div>
                    <button @click="register" class="btn btn-primary" value="save">Register</button>
                </form>
            </div>
        </div>
    </main>
</template>

<script setup >

    function register(event) {
        event.preventDefault();

        let form = new FormData($('form#register')[0])
        let url = "/api/v1/register";

        fetch(url, {
            method: 'POST',
            headers: {
                // 'Content-Type': 'application/json'
            },
            body: form
        })
        .then(result => result.json())
        .then((data) => {
            if (data.message==="User created successfully") {
                console.log('user registered');
                window.location.assign('/login');
                
            } else {
                console.log('failed to register user');
                $('form#register').trigger('reset');
            }
        })
    }
</script>

<style scoped>
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