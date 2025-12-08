const modal = document.getElementById('authorise');
const loginBtn = document.getElementById('login-modal-btn');
const signupBtn = document.getElementById('signup-modal-btn');
const closeBtn = document.getElementsByClassName('close-btn')[0];
const loginTabLink = document.querySelector('.tabs button:first-child');
const signupTabLink = document.querySelector('.tabs button:last-child');
const loginContent = document.getElementById('Login');
const signupContent = document.getElementById('Signup');



function openForm(evt, tabName) {
    loginTabLink.classList.remove('active');
    signupTabLink.classList.remove('active');
    loginContent.classList.remove('active');
    signupContent.classList.remove('active');

    if (tabName === 'Login') {
        loginTabLink.classList.add('active');
        loginContent.classList.add('active');
    } else if (tabName === 'Signup') {
        signupTabLink.classList.add('active');
        signupContent.classList.add('active');
    }
}


loginBtn.onclick = function(e) {
    e.preventDefault();
    modal.style.display = 'block';
    openForm(e, 'Login');
};


signupBtn.onclick = function(e) {
    e.preventDefault();
    modal.style.display = 'block';
    openForm(e, 'Signup');
};


closeBtn.onclick = function() {
    modal.style.display = 'none';
};


window.onclick = function(event) {
    if (event.target === modal) {
        modal.style.display = 'none';
    }
};

window.openForm = openForm;