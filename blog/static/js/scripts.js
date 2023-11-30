/*!
* Start Bootstrap - Blog Post v5.0.9 (https://startbootstrap.com/template/blog-post)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-blog-post/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project


const darkModeToggleBtn = document.getElementById('darkModeToggle');

// 클릭 이벤트 핸들러
darkModeToggleBtn.addEventListener('click', function() {
  document.body.classList.toggle('dark-mode');
});