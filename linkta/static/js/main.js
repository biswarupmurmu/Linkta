var showpasswordinform = document.getElementById("showpasswordinform")
if (showpasswordinform != null){
    showpasswordinform.addEventListener("click", ()=>{
        var x = document.getElementById("passwordinform");
        var icon = document.querySelector("#passwordinformlabel > .material-symbols-outlined")
        if (x.type === "password") {
            x.type = "text"
            icon.textContent = "visibility"
        }
        else {
            x.type = "password"
            icon.textContent = "visibility_off"
        }
    })
}