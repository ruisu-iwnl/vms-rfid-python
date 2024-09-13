
document.addEventListener('DOMContentLoaded', () => {
    const registerButton = document.getElementById('registerButton');

    if (registerButton) {
        registerButton.addEventListener('click', (event) => {
            event.preventDefault(); 

            swal({
                title: "Are you sure?",
                text: "Do you want to register this account?",
                icon: "warning",
                buttons: true,
                dangerMode: true,
            }).then((willRegister) => {
                if (willRegister) {
                    document.querySelector('form').submit();
                }
            });
        });
    }
});
