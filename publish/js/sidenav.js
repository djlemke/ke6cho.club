function toggleMenu() {
    let sidenav = document.querySelector('#side_nav');

    if (sidenav.classList.contains('hidden'))
        sidenav.classList.remove('hidden')
    else
        sidenav.classList.add('hidden')
}

