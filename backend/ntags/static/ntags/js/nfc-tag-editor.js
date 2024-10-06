document.addEventListener("DOMContentLoaded", function () {
    const contentTypeField = document.querySelector('select[name="content_type"]');
    const ItemField = document.querySelector('select[name="item"]');
    const ItemFieldWrapper = document.querySelector('#panel-child-details-item-section');

    // Function to toggle the visibility of the item field and update its options
    function toggleItemField() {
        if (contentTypeField && contentTypeField.value !== "") {
            ItemFieldWrapper.style.display = "block"; // Show if content_type is selected
            updateItemFieldOptions(contentTypeField.value); // Dynamically populate options
        } else {
            ItemFieldWrapper.style.display = "none"; // Hide if content_type is not selected
            ItemField.innerHTML = ''; // Clear the item field when hidden
        }
    }

    // Function to update the item field options based on selected content_type
    function updateItemFieldOptions(contentTypeId) {
        if (contentTypeId) {
            fetch(`/link/get-linkable-objects/${contentTypeId}/`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    // Check if the field already has options (e.g., on page load for an existing instance)
                    if (ItemField.options.length > 1) {
                        // If the field already has options (more than the default empty option), don't overwrite
                        return;
                    }

                    // Clear current options in item field only if empty
                    ItemField.innerHTML = '';

                    // Add a default empty option
                    const defaultOption = document.createElement('option');
                    defaultOption.value = '';
                    defaultOption.textContent = 'Select an item';
                    ItemField.appendChild(defaultOption);

                    // Populate item field with new options
                    data.objects.forEach(obj => {
                        const option = document.createElement('option');
                        option.value = obj.id;
                        option.textContent = obj.name;
                        ItemField.appendChild(option);
                    });
                })
                .catch(error => {
                    console.error('Error fetching object options:', error);
                    ItemField.innerHTML = '<option value="">Error loading items</option>';
                });
        }
    }

    // Initialize visibility and populate item options on page load
    toggleItemField();

    // Listen for changes to the content_type field to update both visibility and options
    contentTypeField.addEventListener("change", toggleItemField);
});
