"use strict";

function dragNdrop(event) {
	var filename = URL.CreateObjectURL(event.target.files[0]);
	var preview = document.getElementById('preview');
	var previewImg = document.CreateElement("img");
	previewImg.setAttribute("src",filename);
	preview.innerHTML = "";
	previewImg.appendChild(previewImg);
}

function drag() {
	document.getElementById('uploadFile').parentNode.className = "draging dragBox";
}

function drop(){
	document.getElementById('uploadFile').parentNode.className = 'dragBox';
}