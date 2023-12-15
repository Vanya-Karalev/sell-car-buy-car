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

    var modelDropdown = document.getElementById("modelDropdown");
    modelDropdown.setAttribute("data-brand-id", selectBrandId);

    var selectedModelBtn = document.getElementById("selectedModelBtn");
    selectedModelBtn.disabled = false;

    selectedModelBtn.value = "";

    filterModels();
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
            toggleModelDropdown()
        }
    }
}

// model
function toggleModelDropdown() {
    var dropdown = document.querySelector('.dropdown_model');
        dropdown.classList.toggle('active');
}


function filterModelFunction() {
    var input, filter, a, i;
    input = document.getElementById("selectedModelBtn");
    filter = input.value.toUpperCase();
    a = document.getElementsByClassName("car-model");
    for (i = 0; i < a.length; i++) {
        if (a[i].innerHTML.toUpperCase().indexOf(filter) > -1) {
            a[i].style.display = "";
        } else {
            a[i].style.display = "none";
        }
    }
    filterModels();
}

function selectModel(element) {
     var selectedBrandBtn = document.getElementById("selectedModelBtn");
     selectedBrandBtn.value = element.getAttribute("data-model");
}

document.addEventListener('click', function(event) {
    var dropdownModelContainer = document.getElementById('dropdownModelContainer');
    if (!dropdownModelContainer.contains(event.target)) {
        var dropdown = document.querySelector('.dropdown_model');
        if (dropdown.classList.contains('active')) {
            dropdown.classList.remove('active');
        }
    }
});

function clearFields() {
    document.getElementById('selectedBrandBtn').value = '';
    document.getElementById('selectedModelBtn').value = '';
    document.getElementById('start_price').value = '';
    document.getElementById('end_price').value = '';
    document.getElementById('start_year').value = '';
    document.getElementById('end_year').value = '';
    document.getElementById('start_mileage').value = '';
    document.getElementById('end_mileage').value = '';
}
