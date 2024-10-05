document.addEventListener("DOMContentLoaded", function () {
    const contentTypeField = document.querySelector('select[name="content_type"]');
    const objectIdFieldWrapper = document.querySelector('#panel-child-details-object_id-section');

    // Function to toggle the visibility of the object_id field
    function toggleObjectIdField() {
        if (contentTypeField && contentTypeField.value !== "") {
            objectIdFieldWrapper.style.display = "block"; // Show if content_type is selected
        } else {
            objectIdFieldWrapper.style.display = "none"; // Hide if content_type is not selected
        }
    }

    // Initialize visibility on page load
    toggleObjectIdField();

    // Listen for changes to the content_type field
    contentTypeField.addEventListener("change", toggleObjectIdField);
});
