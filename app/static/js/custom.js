document.addEventListener("DOMContentLoaded", function() {
    const deleteForms = document.querySelectorAll('form[action*="delete_tour"]');

    deleteForms.forEach(form => {
        form.addEventListener('submit', function(event) {
            const confirmDelete = confirm("Ви впевнені, що хочете видалити цей тур?");
            if (!confirmDelete) {
                event.preventDefault();
            }
        });
    });
});
