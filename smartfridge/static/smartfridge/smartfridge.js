
/**************** My Fridge ***********************/

// Manually add item to my fridge
function addItem() {
    // Get all inputs from modal
    var name_element = $("#name");
    var expiry_date_element = $("#expiry_date");
    var count_element = $("#count");
    var name = name_element.val();
    var expiry_date = expiry_date_element.val();
    var count = count_element.val();
    name_element.val('');
    expiry_date_element.val('');
    count_element.val('');
    // Close the modal
    $("#new_item").modal('toggle');

    // Send POST request to views.py > add_myFridge()
    $.ajax({
        url: "/smartfridge/add_myFridge",
        type: "POST",
        // Data to send: send user-added content of new item
        data: "name="+name+"&expiry_date="+expiry_date+"&count="+count+"&csrfmiddlewaretoken="+getCSRFToken(),
        // Type of data we expect back
        dataType : "json",
        // If request was successful
        success: function(response) {
            showMessage_myFridge("Your item has been added to My Fridge");
            getMyFridgeList(response);
        }
    });
}

function editItem() {
}

function getMyFridgeList(response) {
    $.ajax({
        url: "/smartfridge/get_myFridgeList_json",
        dataType : "json",
        success: showMyFridgeList
    });
}

function showMyFridgeList(response) {
    $(".col-3-3").remove(); // remove all previous items
 
    $(response).each(function() {
        // Add html for an item to my fridge page
        $("#fridge_items").append(
            "<div class='col-3-3'>" + 
                "<div class='card bg-light text-dark'>" +

                    "<div class='card-header'>" +
                        "<div class='btn-group-toggle' data-toggle='buttons'>" +
                            "<label class='btn btn-primary active'>" +
                                "<input type='checkbox' checked autocomplete='off'>" + this.name +
                            "</label>" +
                        "</div>" +
                    "</div>" +

                    "<div class='card-body'>" +
                        "<p>Expiry Date: " + this.expiry_date + "</p>" +
                        "<p>Count: " + this.count + "</p>" + 
                        "<button type='button' class='btn btn-primary' onclick='addShoppingList(" + this.item_id + ")'>Buy</button>" +
                        "<button type='button' class='btn btn-info' data-toggle='modal' data-target='#edit_item'>Edit</button>" +
                        "<button type='button' class='btn btn-danger' onclick='delete_myFridge(" + this.item_id + ")'>X</button>" +
                    "</div>" +

                "</div>" +
                "<p>&nbsp;</p>" +
            "</div>");
    });
}

// Add item to shopping list - from my fridge
function addShoppingList(item_id) {

    // Send POST request to views.py > add_to_shoppingList()
    $.ajax({
        url: "/smartfridge/add_to_shoppingList",
        type: "POST",
        // Data to send: send user-added content of new item
        data: "item_id="+item_id+"&csrfmiddlewaretoken="+getCSRFToken(),
        // Type of data we expect back
        dataType : "json",
        // If request was successful
        success: function(response) {
            showMessage_myFridge("Your item has been added to the shopping list");
        }
    });
}

// Delete the selected item to my fridge
function delete_myFridge(item_id) {
    // Send POST request to views.py > del_my_fridge()
    $.ajax({
        url: "/smartfridge/del_my_fridge",
        type: "POST",
        // Data to send: send user-added content of post
        data: "item_id="+item_id+"&csrfmiddlewaretoken="+getCSRFToken(),
        // Type of data we expect back
        dataType : "json",
        // If request was successful, run updateShoppingList
        success: function(response) {
            showMessage_myFridge("Selected item has been deleted");
            getMyFridgeList(response);
        }
    });
}

/********************* Shopping List **************************/

// Add item to shopping list - inside the shopping list
function addShopping() {
    var item_element = $("#new_item");
    var item = item_element.val();
    item_element.val('');

    // Send POST request to views.py > add_to_shoppingList()
    $.ajax({
        url: "/smartfridge/add_to_shoppingList_from_shopping",
        type: "POST",
        // Data to send: send user-added content of post
        data: "item_name="+item+"&csrfmiddlewaretoken="+getCSRFToken(),
        // Type of data we expect back
        dataType : "json",
        // If request was successful
        success: function(response) {
            showMessage_shoppingList("Your item has been added to the shopping list");
            getShoppingList();
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
            getShoppingList();
            showMessage_shoppingList("Selected item has been deleted");
        }
    });
}

// Show a message - notify that the selected item is added to the shopping list
function showMessage_myFridge(message) {

    // Show message
    $("#myFridge_message").append(
        "<div class='alert alert-warning alert-dismissible fade show' role='alert'>" + 
            message +
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

/******************** The Rest *************************/

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
window.onload = getMyFridgeList;
window.setInterval(getMyFridgeList, 5000);
window.setInterval(getShoppingList, 5000);