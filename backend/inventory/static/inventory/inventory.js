document.addEventListener('DOMContentLoaded', function () {
  const loadMoreBtn = document.getElementById('load-more');

  if (loadMoreBtn) {
    loadMoreBtn.addEventListener('click', function (e) {
      e.preventDefault();
      const page = this.dataset.page;

      // Make an AJAX request
      fetch(`?page=${page}`, {
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      })
      .then(response => response.text())
      .then(data => {
        // Replace the plant list with new data
        const plantListWrapper = document.querySelector('.collection-list-wrapper-posts');
        plantListWrapper.innerHTML += data;

        // Update the "Load More" button
        const newLoadMoreBtn = document.getElementById('load-more');
        if (newLoadMoreBtn) {
          this.dataset.page = newLoadMoreBtn.dataset.page;
        } else {
          this.remove(); // Remove the button if there are no more pages
        }
      })
      .catch(error => console.error('Error:', error));
    });
  }
});