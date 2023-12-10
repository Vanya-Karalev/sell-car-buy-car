function toggleDropdown() {
    var dropdown = document.querySelector('.dropdown');
    dropdown.classList.toggle('active');
  }

  function filterFunction() {
    var input, filter, a, i;
    input = document.getElementById("selectedBrandBtn");
    filter = input.value.toUpperCase();
    a = document.getElementsByClassName("car-brand");
    for (i = 0; i < a.length; i++) {
      if (a[i].innerHTML.toUpperCase().indexOf(filter) > -1) {
        a[i].style.display = "";
      } else {
        a[i].style.display = "none";
      }
    }
  }

  function selectBrand(element) {
    var selectedBrandBtn = document.getElementById("selectedBrandBtn");
    selectedBrandBtn.value = element.getAttribute("data-brand");
    toggleDropdown();
  }

  function clearSelection() {
    var selectedBrandBtn = document.getElementById("selectedBrandBtn");
    selectedBrandBtn.value = "";
    selectedBrandBtn.placeholder = "Марка";
    toggleDropdown();
  }

  document.addEventListener('click', function(event) {
    var dropdownContainer = document.getElementById('dropdownContainer');
    if (!dropdownContainer.contains(event.target)) {
      var dropdown = document.querySelector('.dropdown');
      if (dropdown.classList.contains('active')) {
        dropdown.classList.remove('active');
      }
    }
  });