$(document).ready(function() {
    $('.expand-collapse > p > button').click(function(e) {
        var button = $(e.target);
        var node_elt = $(e.target).parents('.literate-git-node')[0];
        var children_elt = $(node_elt).children('.children')[0];
        var children_visible_p = $(children_elt).is(':visible');
        if (children_visible_p) {
            button.attr('disabled', true);
            $(children_elt).slideUp(800, function() {
                button.html('Show details');
                button.attr('disabled', false);
            });
        } else {
            button.attr('disabled', true);
            $(children_elt).slideDown(800, function() {
                button.html('Hide details');
                button.attr('disabled', false);
            });
        }
    });
});
