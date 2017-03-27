/*
 jQuery(function ($) {

 });*/

$(function () {
    var $helpers = $("#btnHelperAttributes, #btnHelperDependencies");

    var $attributes = $("#txtAttributes");
    var $dependencies = $("#txtDependencies");

    var $addDependenciesX = $("#txtAddImplicante");
    var $addDependenciesY = $("#txtAddImplicado");

    var $validator = $("#form").validator();
    var $validatorModal = $("#form-modal").validator();

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

    $validator.on('submit', function (e) {
        if (e.isDefaultPrevented()) {
            console.log("Handle the invalid form");
            var text = $dependencies.val() ? $dependencies.val().trim(): "";
            if(engineering.util.isEmpty(text)){
                // console.log("El Campo es requerido.")
            }
        } else {
            //console.log("Everything looks good!");
        }
    });

    $validatorModal.on('submit', function (e) {
        if (e.isDefaultPrevented()) {
            // console.log("Handle the invalid form");
        } else {
            // console.log("Everything looks good!");
            try{
                e.preventDefault();

                var tempDependencies = $dependencies.val();
                var result = $addDependenciesX.val() + ":" + $addDependenciesY.val();

                if(!engineering.util.isEmpty(tempDependencies)){
                    result = tempDependencies + "; " + result;
                }

                $dependencies.val(result);

                $(".modal-response").show();

                $("#txtResultDependenceX").text($addDependenciesX.val().replace(" ", "").replace(",", " "));
                $("#txtResultDependenceY").text($addDependenciesY.val().replace(" ", "").replace(",", " "));

                $(this)[0].reset();
                $addDependenciesX.val("");
                $addDependenciesY.val("");

                 setTimeout(function() {
                     $(".modal-response").hide();
                     $("#txtResultDependenceX").text("");
                     $("#txtResultDependenceY").text("");
                }, 1500);
            } catch (e){
                // console.log("Error");
            }
        }
    })
});