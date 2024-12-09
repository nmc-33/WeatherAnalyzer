function openInNewTab(url) {
    // Open a blank new tab
    const newTab = window.open();

    // Fetch the URL
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.text(); // Assuming the response is text or HTML
        })
        .then(htmlContent => {
            // Write the response into the new tab
            newTab.document.open();
            newTab.document.write(htmlContent);
            newTab.document.close();
        })
        .catch(error => {
            console.error('Error fetching the resource:', error);
            newTab.document.write(`<p>Error: ${error.message}</p>`);
        });
}

// Add event listener to the button
document.getElementById('open-new-tab-btn').addEventListener('click', () => {
    // Replace with your desired URL
    const url = 'http://example.com/api/resource';
    openInNewTab(url);
});