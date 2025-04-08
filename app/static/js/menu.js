// /app/static/js/menu.js

export function renderMenu() {
  const menu = document.getElementById('menu');
  menu.innerHTML = `
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <a class="navbar-brand" href="index.html">My App</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" 
                aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <a class="nav-link" href="browse.html">Files</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="documents.html">Documents</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="events.html">Events</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="dbexplorer.html">DB Explorer</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="llm.html">MILOGen</a>
            </li>
          </ul>
          <ul class="navbar-nav">
            <li class="nav-item" id="loginNav">
              <a class="nav-link" href="login.html">Login</a>
            </li>
            <li class="nav-item" id="logoutNav" style="display: none;">
              <a class="nav-link" href="#" id="logoutBtn">Logout</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  `;

  // Check if the user is logged in (by checking for a stored token)
  if (localStorage.getItem('access_token')) {
    // Show logout and hide login menu items
    document.getElementById('logoutNav').style.display = 'block';
    document.getElementById('loginNav').style.display = 'none';

    // Bind the logout button event
    document.getElementById('logoutBtn').addEventListener('click', async (event) => {
      event.preventDefault();
      await logout();
    });
  } else {
    // If no token, only show the login link
    document.getElementById('logoutNav').style.display = 'none';
    document.getElementById('loginNav').style.display = 'block';
  }
}

async function logout() {
  try {
    // Optionally, notify the backend that we're logging out.
    // This endpoint currently just returns a message and does no token revocation.
    const response = await fetch('/api/login/logout', {
      method: 'POST'
    });
    const data = await response.json();
    console.log(data.message);
  } catch (err) {
    console.error('Error during logout:', err);
  }
  // Remove the token from local storage
  localStorage.removeItem('access_token');
  // Redirect to the login page (or any public page)
  window.location.href = 'login.html';
}

export { logout };
