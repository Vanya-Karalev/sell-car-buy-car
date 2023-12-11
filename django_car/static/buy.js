var selectBrandId;
// brand
function toggleDropdown() {
        var dropdown = document.querySelector('.dropdown_brand');
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
    selectBrandId = element.getAttribute("data-brand-id");

    // Update the data-brand-id attribute of the model dropdown
    var modelDropdown = document.getElementById("modelDropdown");
    modelDropdown.setAttribute("data-brand-id", selectBrandId);

    // Enable the model dropdown
    var selectedModelBtn = document.getElementById("selectedModelBtn");
    selectedModelBtn.disabled = false;

    // Clear the selected model
    selectedModelBtn.value = "";

    filterModels(); // Call a function to filter models when a brand is selected
    dropdown.classList.remove('active');
}



document.addEventListener('click', function(event) {
    var dropdownContainer = document.getElementById('dropdownContainer');
    if (!dropdownContainer.contains(event.target)) {
        var dropdown = document.querySelector('.dropdown_brand');
        if (dropdown.classList.contains('active')) {
            dropdown.classList.remove('active');
        }
    }
});

function filterModels() {
    var modelDropdown = document.getElementById("modelDropdown");
    var models = modelDropdown.getElementsByClassName("car-model");

    for (var i = 0; i < models.length; i++) {
        var brandId = models[i].getAttribute("data-brand-id");
        if (brandId !== selectBrandId) {
            models[i].style.display = "none";
        } else {
            models[i].style.display = "";
        }
    }
}