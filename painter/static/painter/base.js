function delete_image_confirm() {
    console.log("Button pressed");
    if (confirm('Do you want to delete this Image?')) {
        document.forms["form1"].submit();
    }
}
