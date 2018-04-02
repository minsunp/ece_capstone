
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
            showMessage_myFridge(response);
        }
    });
}

// Add item to shopping list - inside the shopping list
function addShopping() {
    var item_element = $("#new_item");
    var item = item_element.val();
    item_element.val('');

    // Send POST request to views.py > add_to_shoppingList()
    $.ajax({
        url: "/smartfridge/add_to_shoppingList",
        type: "POST",
        // Data to send: send user-added content of post
        data: "item_name="+item+"&csrfmiddlewaretoken="+getCSRFToken(),
        // Type of data we expect back
        dataType : "json",
        // If request was successful, run updateShoppingList
        success: function(response) {
            showMessage_shoppingList("Your item has been added to the shopping list");
            getShoppingList(response);
        }
    });
}

// Given an item id, delete the corresponding item from the shopping list
function del_shoppingItem(item_id) {
    // Send POST request to views.py > del_shoppingList()
    $.ajax({
        url: "/smartfridge/del_shoppingList",
        type: "POST",
        // Data to send: send user-added content of post
        data: "item_id="+item_id+"&csrfmiddlewaretoken="+getCSRFToken(),
        // Type of data we expect back
        dataType : "json",
        // If request was successful, run updateShoppingList
        success: function(response) {
            showMessage_shoppingList("Selected item has been deleted");
            getShoppingList(response);
        }
    });
}

// Show a message - notify that the selected item is added to the shopping list
function showMessage_myFridge(response) {

    // Show message
    $("#myFridge_message").append(
        "<div class='alert alert-warning alert-dismissible fade show' role='alert'>" + 
            "Your item has been added to the shopping list" +
            "<button type='button' class='close' data-dismiss='alert' aria-label='Close'>" +
                "<span aria-hidden='true'>&times;</span>" +
            "</button>" +
        "</div>");
}

// Show a message - notify that the selected item is added to the shopping list
function showMessage_shoppingList(message) {

    // Show message
    $("#shoppingList_message").append(
        "<div class='alert alert-warning alert-dismissible fade show' role='alert'>" + 
            message +
            "<button type='button' class='close' data-dismiss='alert' aria-label='Close'>" +
                "<span aria-hidden='true'>&times;</span>" +
            "</button>" +
        "</div>");
}

// Get all shopping list items - in json format
function getShoppingList() {
    $.ajax({
        url: "/smartfridge/get_shoppingList_json",
        dataType : "json",
        success: showShoppingList
    });
}

// Display all shopping list items
function showShoppingList(response) {

    $(".list-group-item").remove(); // remove all previous items

    $(response).each(function() {
        // Add html to shopping list page
        $("#shopping_list").append(
            "<li class='list-group-item'>" +
                "<input class='form-check-input' type='checkbox' onchange='del_shoppingItem(" + this.item_id + ")'>" +
                "<label class='form-check-label'>" + this.name + "</label>" +
            "</li>");
    });
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

window.onload = getShoppingList;
