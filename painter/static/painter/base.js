function delete_image_confirm(form) {
    console.log("Button pressed");
    if (confirm('Do you want to delete this Image?')) {
        form.submit();
    }
}
