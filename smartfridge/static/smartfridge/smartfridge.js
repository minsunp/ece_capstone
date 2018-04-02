
function addItem() {
}

function editItem() {
}

// Add item to shopping list - from my fridge
function addShoppingList(item_name) {

    // Send POST request to views.py > add_to_shoppingList()
    $.ajax({
        url: "/smartfridge/add_to_shoppingList",
        type: "POST",
        // Data to send: send user-added content of post
        data: "item_name="+item_name+"&csrfmiddlewaretoken="+getCSRFToken(),
        // Type of data we expect back
        dataType : "json",
        // If request was successful, run updateShoppingList
        success: function(response) {
            updateShoppingList(response);
        }
    });
    
}


// Add item to shopping list - from shopping list
function addShopping() {
}

// Update shopping list page
function updateShoppingList(response) {

    // Add html to shopping list page
    $("#shopping_list").append(
        "<li class='list-group-item'>" +
            "<input class='form-check-input' type='checkbox' id='check1'>" +
            "<label class='form-check-label' for='check1'>" + this.name + "</label>" +
        "</li>");

    // Show message
    $("#myFridge_message").append(
        "<div class='alert alert-warning alert-dismissible fade show' role='alert'>" + 
            "Your item has been added to the shopping list" +
            "<button type='button' class='close' data-dismiss='alert' aria-label='Close'>" +
                "<span aria-hidden='true'>&times;</span>" +
            "</button>" +
        "</div>");
}

function getCSRFToken() {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
        if (cookies[i].startsWith("csrftoken=")) {
            return cookies[i].substring("csrftoken=".length, cookies[i].length);
        }
    }
    return "unknown";
}

// Put the message in error division
function displayError(message) {
    $("#error").html(message);
}
