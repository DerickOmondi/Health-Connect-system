document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menu-toggle');
    const sidebarMenu = document.getElementById('sidebar-menu');

    if (menuToggle && sidebarMenu) {
        menuToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            menuToggle.classList.toggle('active');
            sidebarMenu.classList.toggle('active');
        });

        // Close when clicking outside
        document.addEventListener('click', function(event) {
            if (!sidebarMenu.contains(event.target) && !menuToggle.contains(event.target)) {
                sidebarMenu.classList.remove('active');
                menuToggle.classList.remove('active');
            }
        });
    }
});