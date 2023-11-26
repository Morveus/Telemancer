function toggleMenu() {
    var menu = document.getElementById("menu-items");
    if (menu.className === "hidden") {
        menu.className = "";
    } else {
        menu.className = "hidden";
    }
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.page-link').forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent default link behavior
            const pageName = link.getAttribute('href').substring(1); // Extract page name from href
            fetchContent(pageName);
        });
    });
});

function fetchContent(pageName) {
    fetch(`/${pageName}`)
        .then(response => response.text())
        .then(data => {
            const contentDiv = document.getElementById('content');
            contentDiv.innerHTML = data;

            // Find and execute scripts
            const scripts = contentDiv.getElementsByTagName('script');
            for (let script of scripts) {
                eval(script.textContent)
            }
        })
        .catch(error => console.error('Error:', error));
}

