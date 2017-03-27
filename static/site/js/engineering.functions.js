/*
 jQuery(function ($) {

 });*/

$(function () {
    var $helpers = $("#btnHelperAttributes, #btnHelperDependencies");
    var $attributes = $("#txtAttributes");
    var $dependencies = $("#txtDependencies");

    $helpers.popover({
        /* trigger : 'hover',
         delay: {
         show: "500",
         hide: "100"
         }*/
    });

    $helpers.on('shown.bs.popover', function() {
        setTimeout(function() {
            $helpers.popover('hide');
        }, 5000);
    });

    $attributes.on("change", function () {
        var self = $(this);
        var text  = self.val();

        if(engineering.util.isValidAttribute(text)){
            console.log("Valido: " + text);
        } else {
            console.log("No Valido");
        }
    });

    $("#form").validator().on('submit', function (e) {
        if (e.isDefaultPrevented()) {
            console.log("Handle the invalid form");
        } else {
            console.log("Everything looks good!");
            // $(this).submit();
        }
    })
});