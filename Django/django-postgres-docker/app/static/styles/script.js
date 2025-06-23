
    <script>
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.download-btn').forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const url = btn.getAttribute('data-img');
            const fileName = url.split('/').pop().split('?')[0];
            fetch(url)
                .then(resp => resp.blob())
                .then(blob => {
                    const link = document.createElement('a');
                    link.href = window.URL.createObjectURL(blob);
                    link.download = fileName;
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                });
        });
    });
});
</script>

<script>
document.querySelectorAll('.wallpaper-fav-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        // Reemplaza el 0 por el id real del wallpaper
        const url = "{% url 'toggle_wallpaper_favorito' 0 %}".replace('0', btn.dataset.id);
        fetch(url, {
            method: "POST",
            headers: {
                "X-CSRFToken": "{{ csrf_token }}",
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: new URLSearchParams({
                wallpaper_id: btn.dataset.id
            })
        })
        .then(resp => resp.json())
        .then(data => {
            if (data.success) {
                // Opcional: Cambia el color del botón o muestra mensaje
            }
        });
    });
});
</script>
<script>
document.querySelectorAll('.wallpaper-fav-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        // Deshabilita el botón para evitar múltiples clics
        btn.disabled = true;
        const url = "{% url 'toggle_wallpaper_favorito' 0 %}".replace('0', btn.dataset.id);
        fetch(url, {
            method: "POST",
            headers: {
                "X-CSRFToken": "{{ csrf_token }}",
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: new URLSearchParams({
                wallpaper_id: btn.dataset.id
            })
        })
        .then(resp => resp.json())
        .then(data => {
            // Aquí puedes actualizar el estado visual del botón si quieres
            btn.disabled = false; // Vuelve a habilitar el botón
            // Opcional: recarga la página o actualiza el DOM
        })
        .catch(() => {
            btn.disabled = false; // Asegura que se habilite en caso de error
        });
    });
});
</script>