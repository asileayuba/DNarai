document.addEventListener("DOMContentLoaded", () => {
    fetch('posts.json')
      .then(res => res.json())
      .then(data => {
        const list = document.getElementById('blog-list');
        list.innerHTML = data.map(post => `
          <li class="blog-post">
            <img src="${post.image}" alt="${post.title}">
            <h3>${post.title}</h3>
            <p>${post.excerpt}</p>
          </li>
        `).join('');
      })
      .catch(err => console.error("Failed to load blog posts:", err));
  });
  