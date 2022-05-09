$(function () {
    // *******************************************************
    //  U T I L I T Y   F U N C T I O N S
    // *******************************************************
    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    };
    // *******************************************************
    //  A D D R E S S   U T I L I T Y   F U N C T I O N S
    // *******************************************************
    // Updates the form with data from the response
    function update_address_form_data(res) {
        $("customer_address_id").val(res.id)
        $("#customer_address_customer_id").val(res.customer_id);
        $("#customer_address_name").val(res.name);
        $("#customer_address_street").val(res.street);
        $("#customer_address_city").val(res.city);
        $("#customer_address_state").val(res.state);
        $("#customer_address_postalcode").val(res.postalcode);
    };
    /// Clears all form fields
    function clear_address_form_data() {
        $("#customer_address_id").val("");
        $("#customer_address_customer_id").val("");
        $("#customer_address_name").val("");
        $("#customer_address_street").val("");
        $("#customer_address_city").val("");
        $("#customer_address_state").val("");
        $("#customer_address_postalcode").val("");
    };

    // *******************************************************
    //  A D D R E S S   F U N C T I O N S
    // *******************************************************
    // Create a Customer Address
    // *******************************************************
    $("#create-btn").click(function () {
        let customer_id = $("#customer_address_customer_id").val();
        let name = $("#customer_address_name").val();
        let street = $("#customer_address_street").val();
        let city = $("#customer_address_city").val();
        let state = $("#customer_address_state").val();
        let postalcode = $("#customer_address_postalcode").val();
        let data = {
            "customer_id": customer_id,
            "name": name,
            "street": street,
            "city": city,
            "state": state,
            "postalcode": postalcode
        };
        $("#flash_message").empty();
        let ajax = $.ajax({
            type: "POST",
            url: `/customers/${customer_id}/addresses`,
            contentType: "application/json",
            data: JSON.stringify(data),
        });
        ajax.done(function(res){
            update_address_form_data(res);
            flash_message("Success");
        });
        ajax.fail(function(res){
            flash_message(res.responseJSON.message);
        });
    });
    // *******************************************************
    // Update a Customer Address
    // *******************************************************
    $("#update-btn").click(function () {
        let address_id = $("#customer_address_id").val();
        let customer_id = $("#customer_address_customer_id").val();
        let name = $("#customer_address_name").val();
        let street = $("#customer_address_street").val();
        let city = $("#customer_address_city").val();
        let state = $("#customer_address_state").val();
        let postalcode = $("#customer_address_postalcode").val();
        let data = {
            "customer_id": customer_id,
            "name": name,
            "street": street,
            "city": city,
            "state": state,
            "postalcode": postalcode
        };
        $("#flash_message").empty();
        let ajax = $.ajax({
                type: "PUT",
                url: `/customers/${customer_id}/addresses/${address_id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            });
        ajax.done(function(res){
            update_address_form_data(res);
            flash_message("Success");
        });
        ajax.fail(function(res){
            flash_message(res.responseJSON.message);
        });
    });
    // *******************************************************
    // Retrieve a Customer Address
    // *******************************************************
    $("#retrieve-btn").click(function () {
        let address_id = $("#customer_address_id").val();
        let customer_id = $("#customer_address_customer_id").val();
        $("#flash_message").empty();
        let ajax = $.ajax({
            type: "GET",
            url: `/customers/${customer_id}/addresses/${address_id}`,
            contentType: "application/json",
            data: ''
        });
        ajax.done(function(res){
            update_address_form_data(res);
            flash_message("Success");
        });
        ajax.fail(function(res){
            clear_address_form_data();
            flash_message(res.responseJSON.message);
        });
    });
    // *******************************************************
    // Delete a Customer Address
    // *******************************************************
    $("#delete-btn").click(function () {
        let address_id = $("#customer_address_id").val();
        let customer_id = $("#customer_address_customer_id").val();
        $("#flash_message").empty();
        let ajax = $.ajax({
            type: "DELETE",
            url: `/customers/${customer_id}/addresses/${address_id}`,
            contentType: "application/json",
            data: ''
        });
        ajax.done(function(res){
            clear_address_form_data();
            flash_message("Address has been Deleted!");
        });
        // ajax.fail(function(res){
        //     flash_message("Server error!");
        // });
        ajax.fail(function(res){
            clear_address_form_data();
            flash_message(res.responseJSON.message);
        });
    });
    // *******************************************************
    // Clear the customer address form
    // *******************************************************
    $("#clear-btn").click(function () {
        clear_address_form_data();
        $("#flash_message").empty();
    });
    // *******************************************************
    // List Addresses for a Customer
    // *******************************************************
    $("#list-btn").click(function () {
        let id = $("#customer_address_id").val();
        let customer_id = $("#customer_address_customer_id").val();
        let queryString = "";
        
        $("#flash_message").empty();
        let ajax = $.ajax({
            type: "GET",
            url: `/customers/${customer_id}/addresses${queryString}`,
            contentType: "application/json",
            data: ''
        });
        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">';
            table += '<thead><tr>';
            table += '<th class="col-md-2">ID</th>';
            table += '<th class="col-md-2">Customer ID</th>';
            table += '<th class="col-md-2">Name</th>';
            table += '<th class="col-md-2">Street</th>';
            table += '<th class="col-md-2">City</th>';
            table += '<th class="col-md-2">State</th>'
            table += '<th class="col-md-3">Postal Code</th>';
            table += '</tr></thead><tbody>';
            let firstAddress = "";
            for(let i = 0; i < res.length; i++) {
                let address = res[i];
                table +=  `<tr id="row_${i}"><td>${address.id}</td><td>${address.customer_id}</td><td>${address.name}</td><td>${address.street}</td><td>${address.city}</td><td>${address.state}</td><td>${address.postalcode}</td></tr>`;
                if (i == 0) {
                    firstAddress = address;
                };
            };
            table += '</tbody></table>';
            $("#search_results").append(table);
            // copy the first result to the form
            if (firstAddress != "") {
                update_address_form_data(firstAddress)
            };
            flash_message("Success");
        });
        ajax.fail(function(res){
            flash_message(res.responseJSON.message);
        });
    });
});