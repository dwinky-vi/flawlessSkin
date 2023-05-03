


let burgerBtn = document.getElementById("burger__btn");
let menu = document.querySelector("#menu");

burgerBtn.addEventListener("click", function () {
	menu.classList.toggle("disp");
})