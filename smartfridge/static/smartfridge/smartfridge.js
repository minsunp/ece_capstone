

function addItem() {
}

function editItem() {
}

// Add item to shopping list - from my fridge
function addShoppingList() {

    alert("does this run");

    var item_name = "Milk";

    // Create ShoppingItem model
    var item = ShoppingItem(name=item_name, count=1);
    item.save();

    // Add html to shopping list page
    $("#shopping_list").append(
        "<li class='list-group-item'>" +
            "<input class='form-check-input' type='checkbox' id='check1'>" +
            "<label class='form-check-label' for='check1'>" + item_name + "</label>" +
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

// Add item to shopping list - from shopping list
function addShopping() {
}

// Update shopping list page
function updateShoppingList() {

}