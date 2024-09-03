function getToken() {
    return localStorage.getItem('jwtToken');
}

// Function to fetch and populate data
async function fetchAndPopulateInventory() {
    try {
        // Fetch data from the API
        const response = await fetch('/api/v2/inventory/?fields=*');
        const data = await response.json();

        // Check if there are items to display
        if (data.items && data.items.length > 0) {
            const inventory = data.items[0];
            const entities = inventory.entities;

            // Get the containers for large and regular sections
            const largeContainer = document.querySelector('.collection-list-wrapper-posts.large .collection-list-posts');
            const regularContainer = document.querySelector('.collection-list-wrapper-posts:not(.large) .collection-list-posts');

            // Clear any existing content in the containers
            largeContainer.innerHTML = '';
            regularContainer.innerHTML = '';

            // Loop through each entity and create HTML elements
            entities.forEach((entity, index) => {
                // Determine if it's the first item (to be placed in the large section)
                const isFirst = index === 0;

                // Create a div to hold the entity
                const entityDiv = document.createElement('div');
                entityDiv.className = 'w-dyn-item' + (isFirst ? ' w--current' : '');

                // Create and append the content
                entityDiv.innerHTML = `
                    <div class="block-post ${isFirst ? 'large' : ''}">
                        <a href="${entity.url}" class="link-post-thumbnail ${isFirst ? 'large' : ''} w-inline-block">
                            <img alt="${entity.image.alt || entity.title}" loading="eager" src="${entity.image ? (isFirst ? entity.image.main : entity.image.thumbnail) : ''}" class="image-post-thumbnail ${isFirst ? 'large' : ''}">
                        </a>
                        <div class="post ${isFirst ? 'large' : ''}">
                            <div class="date"></div>
                            <a href="${entity.url}" class="link-heading-post ${isFirst ? 'large' : ''} w-inline-block">
                                <h${isFirst ? '3' : '4'} class="heading-post">${entity.title}</h${isFirst ? '3' : '4'}>
                            </a>
                            <p class="paragraph-post ${isFirst ? 'large' : ''}">${entity.description}</p>
                            <div class="block-button">
                                <a href="${entity.url}" class="button-small w-button">View</a>
                                <a href="${entity.url}" class="button-outline-small w-button">Edit</a>
                            </div>  
                        </div>
                    </div>
                `;

                // Append the entityDiv to the appropriate container
                if (isFirst) {
                    largeContainer.appendChild(entityDiv);
                } else {
                    regularContainer.appendChild(entityDiv);
                }
            });

            // Make the content visible
            document.querySelector('.section .content').style.opacity = 1;
        } else {
            // Handle the case where there are no items
            regularContainer.innerHTML = `
            <div class="empty-state w-dyn-empty">
                <div class="text-empty">No entities found.</div>
            </div>
            `;
        }
    } catch (error) {
        console.error('Error fetching inventory:', error);
    }
}

// Call the function when the page loads
document.addEventListener('DOMContentLoaded', fetchAndPopulateInventory);