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
    //  C U S T O M E R   U T I L I T Y   F U N C T I O N S
    // *******************************************************
    // Updates the form with data from the response
    function update_customer_form_data(res) {
        $("#customer_id").val(res.id);
        $("#customer_name").val(res.name);
        $("#customer_first_name").val(res.first_name);
        $("#customer_last_name").val(res.last_name);
        $("#customer_email").val(res.email);
        $("#customer_phone_number").val(res.phone_number);
        $("#customer_account_status").val(res.account_status);
    };
    /// Clears all form fields
    function clear_customer_form_data() {
        $("#customer_id").val("");
        $("#customer_name").val("");
        $("#customer_first_name").val("");
        $("#customer_last_name").val("");
        $("#customer_email").val("");
        $("#customer_phone_number").val("");
        $("#customer_account_status").val("");
    };

    // *******************************************************
    //  C U S T O M E R   F U N C T I O N S
    // *******************************************************
    // Create a Customer
    // *******************************************************
    $("#create-btn").click(function () {
        let name = $("#customer_name").val();
        let first_name = $("#customer_first_name").val();
        let last_name = $("#customer_last_name").val();
        let email = $("#customer_email").val();
        let phone_number = $("#customer_phone_number").val();
        let account_status = $("#customer_account_status").val();
        let data = {
            "name": name,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone_number": phone_number,
            "addresses": "",
            "account_status": account_status
        };
        $("#flash_message").empty();
        let ajax = $.ajax({
            type: "POST",
            url: "/customers",
            contentType: "application/json",
            data: JSON.stringify(data),
        });
        ajax.done(function(res){
            update_customer_form_data(res);
            flash_message("Success");
        });
        ajax.fail(function(res){
            flash_message(res.responseJSON.message);
        });
    });
    // *******************************************************
    // Update a Customer
    // *******************************************************
    $("#update-btn").click(function () {
        let customer_id = $("#customer_id").val();
        let name = $("#customer_name").val();
        let first_name = $("#customer_first_name").val();
        let last_name = $("#customer_last_name").val();
        let email = $("#customer_email").val();
        let phone_number = $("#customer_phone_number").val();
        let account_status = $("#customer_account_status").val();
        let data = {
            "name": name,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone_number": phone_number,
            "addresses": "",
            "account_status": account_status
        };
        $("#flash_message").empty();
        let ajax = $.ajax({
                type: "PUT",
                url: `/customers/${customer_id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            });
        ajax.done(function(res){
            update_customer_form_data(res);
            flash_message("Success");
        });
        ajax.fail(function(res){
            flash_message(res.responseJSON.message);
        });
    });
    // *******************************************************
    // Retrieve a Customer
    // *******************************************************
    $("#retrieve-btn").click(function () {
        let customer_id = $("#customer_id").val();
        $("#flash_message").empty();
        let ajax = $.ajax({
            type: "GET",
            url: `/customers/${customer_id}`,
            contentType: "application/json",
            data: ''
        });
        ajax.done(function(res){
            update_customer_form_data(res);
            flash_message("Success");
        });
        ajax.fail(function(res){
            clear_customer_form_data();
            flash_message(res.responseJSON.message);
        });
    });
    // *******************************************************
    // Delete a Customer
    // *******************************************************
    $("#delete-btn").click(function () {
        let customer_id = $("#customer_id").val();
        $("#flash_message").empty();
        let ajax = $.ajax({
            type: "DELETE",
            url: `/customers/${customer_id}`,
            contentType: "application/json",
            data: ''
        });
        ajax.done(function(res){
            clear_customer_form_data();
            flash_message("Customer has been Deleted!");
        });
        ajax.fail(function(res){
            flash_message("Server error!");
        });
    });
    // *******************************************************
    // Clear the customer form
    // *******************************************************
    $("#clear-btn").click(function () {
        clear_customer_form_data();
        $("#flash_message").empty();
    });
    // *******************************************************
    // Search for a Customer
    // *******************************************************
    $("#search-btn").click(function () {
        let id = $("#customer_id").val();
        let name = $("#customer_name").val();
        let last_name = $("#customer_last_name").val();
        let first_name = $("#customer_first_name").val();
        let email = $("#customer_email").val();
        //let phone_number = $("#phone_number").val();
        let queryString = "";
        if (id) {
            queryString = '/' + id
        };
        if (name) {
            queryString += '?name=' + name
        };
        if (first_name) {
            queryString += '?first_name=' + first_name
        };
        if (last_name) {
            queryString += '?last_name=' + last_name
        };
        if (email) {
            queryString += '?email=' + email
        };
        // if (phone_number) {
        //     queryString += 'phone_number=' + phone_number
        // };
        $("#flash_message").empty();
        let ajax = $.ajax({
            type: "GET",
            url: `/customers${queryString}`,
            contentType: "application/json",
            data: ''
        });
        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">';
            table += '<thead><tr>';
            table += '<th class="col-md-2">ID</th>';
            table += '<th class="col-md-2">Username</th>';
            table += '<th class="col-md-2">First Name</th>';
            table += '<th class="col-md-2">Last Name</th>';
            table += '<th class="col-md-2">Email</th>';
            table += '<th class="col-md-2">Phone Number</th>';
            table += '</tr></thead><tbody>';
            let firstCustomer = "";
            for(let i = 0; i < res.length; i++) {
                let customer = res[i];
                table +=  `<tr id="row_${i}"><td>${customer.id}</td><td>${customer.name}</td><td>${customer.first_name}</td><td>${customer.last_name}</td><td>${customer.email}</td><td>${customer.phone_number}</td></tr>`;
                if (i == 0) {
                    firstCustomer = customer;
                };
            };
            table += '</tbody></table>';
            $("#search_results").append(table);
            // copy the first result to the form
            if (firstCustomer != "") {
                update_customer_form_data(firstCustomer)
            };
            flash_message("Success");
        });
        ajax.fail(function(res){
            flash_message(res.responseJSON.message);
        });
    });
    // *******************************************************
    // Suspend a customer
    // *******************************************************
    $("#suspend-btn").click(function () {
        let customer_id = $("#customer_id").val();
        let name = $("#customer_name").val();
        let first_name = $("#customer_first_name").val();
        let last_name = $("#customer_last_name").val();
        let email = $("#customer_email").val();
        let phone_number = $("#customer_phone_number").val();
        let data = {
            "name": name,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone_number": phone_number,
            "addresses": "",
            "account_status": "suspended"
        };
        $("#flash_message").empty();
        let ajax = $.ajax({
                type: "PUT",
                url: `/customers/${customer_id}/suspend`,
                contentType: "application/json",
                data: JSON.stringify(data)
            });
        ajax.done(function(res){
            update_form_data("Success");
        });
        ajax.fail(function(res){
            flash_message(res.responseJSON.message);
        });
    });

    // *******************************************************
    // Restore a customer
    // *******************************************************
    $("#restore-btn").click(function () {
        let customer_id = $("#customer_id").val();
        let name = $("#customer_name").val();
        let first_name = $("#customer_first_name").val();
        let last_name = $("#customer_last_name").val();
        let email = $("#customer_email").val();
        let phone_number = $("#customer_phone_number").val();
        let data = {
            "name": name,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone_number": phone_number,
            "addresses": "",
            "account_status": "suspended"
        };
        $("#flash_message").empty();
        let ajax = $.ajax({
                type: "PUT",
                url: `/customers/${customer_id}/restore`,
                contentType: "application/json",
                data: JSON.stringify(data)
            });
        ajax.done(function(res){
            update_form_data("Success");
        });
        ajax.fail(function(res){
            flash_message(res.responseJSON.message);
        });
    });

});