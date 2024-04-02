function popCategories(categories) {
    var serviceTypeDropdown = document.getElementById("availableServiceType");
    var categoryDropdown = document.getElementById("availableCategory");
    // get serviceTypeId associated with selected service type
    var selectedServiceTypeId = serviceTypeDropdown.value;
    // get categories associated with the specific service type
    var selectedCategories = categories.filter(function(data) {
        return data.service_type_id == selectedServiceTypeId;
    });

    //remove category values in dropdown when user selected another service type
    var i, L = categoryDropdown.options.length - 1;
        for(i = L; i >= 0; i--) {
            categoryDropdown.remove(i);
    }

    //display category in the categorydropdown
    var option = document.createElement("option");
        option.value = "NULL";
        option.text = ""
        categoryDropdown.add(option);
    for (var i = 0; i < selectedCategories.length; i++) {
        var option = document.createElement("option");
        option.value = selectedCategories[i].id;
        option.text = selectedCategories[i].category;
        categoryDropdown.add(option);
    }
}




