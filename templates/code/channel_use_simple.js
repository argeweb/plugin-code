$(function() {
    if (typeof ArGeWebChannel != "undefined") {
        ArGeWebChannel.init($, {
            "after_connection": function(msg){
                console.log("connection")
            },
            "parse_message": function(msg){
                console.log(msg)
            }
        });
    }
});




