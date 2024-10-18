export function obtainToken(username, password) {
    const xhr = new XMLHttpRequest();
    const apiUrl = '/api/token/';

    xhr.open('POST', apiUrl, true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            localStorage.setItem('jwtToken', response.access);
            localStorage.setItem('refreshToken', response.refresh);
        } else if (xhr.readyState === 4) {
            console.error('Error obtaining token:', xhr.statusText);
        }
    };

    const data = JSON.stringify({
        username: username,
        password: password
    });

    xhr.send(data);
}

export function refreshToken() {
    const xhr = new XMLHttpRequest();
    const apiUrl = '/api/token/refresh/';

    xhr.open('POST', apiUrl, true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            localStorage.setItem('jwtToken', response.access);
        } else if (xhr.readyState === 4) {
            console.error('Error refreshing token:', xhr.statusText);
        }
    };

    const refresh_token = localStorage.getItem('refreshToken');
    const data = JSON.stringify({
        refresh: refresh_token
    });

    xhr.send(data);
}
