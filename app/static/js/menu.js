// /app/static/js/menu.js

export function renderMenu() {
    // Example: dynamically create a simple menu element
    const menuContainer = document.getElementById('menu');
    if (!menuContainer) return;
  
    const nav = document.createElement('nav');
    nav.innerHTML = `
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <a class="navbar-brand" href="index.html">My App</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <a class="nav-link" href="index.html">Home</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="upload.html">Upload</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="events.html">Events</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="browse.html">Files</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="dbexplorer.html">Database Explorer</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="llm.html">MILOGen</a>
            </li>
          </ul>
          <ul class="navbar-nav">
            <li class="nav-item">
              <a class="nav-link" href="#" @click="logout">Logout</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  `;
    menuContainer.appendChild(nav);
  }
  
  // Optionally, call renderMenu immediately if that fits your design
  // renderMenu();
  