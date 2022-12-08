
function doLogin() {
    let login_params = {

        id : $('#inputID').val(),
        password : $('#inputPassword').val()

    }
    console.log(login_params.id, login_params['password'])

    var check_ajax = $.ajax({
        type:'POST',
        url: '/login',
        contentType: 'application/json',
        dataType: 'json',
        success: (res) =>{
            console.log("connect success: ", res);
        },
        error: (res, status, err) => {
            console.log('res: ', res)
            console.log('status: ', status)
            console.log('err: ', err)
        }
    })
}

// Example starter JavaScript for disabling form submissions if there are invalid fields
(function () {
    'use strict'
  
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.querySelectorAll('.needs-validation')
  
    // Loop over them and prevent submission
    Array.prototype.slice.call(forms)
      .forEach(function (form) {
        form.addEventListener('submit', function (event) {
          if (!form.checkValidity()) {
            event.preventDefault()
            event.stopPropagation()
          }
  
          form.classList.add('was-validated')
        }, false)
      })
  })()

