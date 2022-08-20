function tryLogin(){
    $.ajax({
        type: 'GET',
        url: '/loginInput',
        data: {username: document.getElementById('username').value, password: document.getElementById('password').value},
        success: function(response){
            if(response = "EXISTS"){
                return true;
                    window.location.href = "../"
            }
            else{
                return false;
            }
        }
        
    })
}