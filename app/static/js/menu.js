export function renderMenu() {

  if (!localStorage.getItem('access_token')) {
    window.location.href = '/login.html';
    return; // Stop processing further until the user logs in.
  }

  const menu = document.getElementById('menu');
  menu.innerHTML = `
    <nav class="navbar navbar-expand-sm navbar-light bg-light">
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
            <li class="nav-item" id="logoutNav" style="display: none;">
              <a class="nav-link" href="#" id="logoutBtn">Logout</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  `;

}

async function logout() {
  localStorage.removeItem('access_token');
  window.location.href = '/login.html';
}

export { logout };
