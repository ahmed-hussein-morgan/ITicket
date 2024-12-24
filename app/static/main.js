document.querySelector('#nav_item').addEventListener('click', function() {
    console.log('Navbar clicked');
    this.style.backgroundColor = 'white';
});


// document.querySelectorAll('.nav-link').forEach(item => {
//     console.log('Adding listener to:', item);
//     item.addEventListener('click', function() {
//         console.log('Clicked:', this);
//         this.style.backgroundColor = 'white';
//     });
// });
