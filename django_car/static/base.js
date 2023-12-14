document.addEventListener('DOMContentLoaded', function () {
    var dropdownItems = document.querySelectorAll('.dropdown ul > li');
    var dropdownSpan = document.querySelector('.dropdown > span');

    dropdownItems.forEach(function (item) {
        item.addEventListener('click', function () {
            dropdownItems.forEach(function (item) {
                item.classList.remove('drop-selected');
            });
            this.classList.toggle('drop-selected');
            dropdownSpan.textContent = this.getAttribute('val');
        });
    });
});