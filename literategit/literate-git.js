$(document).ready(function() {
    var sections = [];
    $('div.content > div.literate-git-node').each(function(i, e) {
        sections.push({idx: i, elt: e});
    });

    $('.diff-or-children > .nav').click(function(e) {
        var button = $(e.target);
        var node_elt = $(e.target).parents('.literate-git-node')[0];
        var expanded_hdr = $(node_elt).find('.nav.collapse');
        var collapsed_hdr = $(node_elt).find('.nav.expand');
        var diff_elt = $(node_elt).find('.diff')[0];
        var children_elt = $(node_elt).find('.children')[0];
        var children_visible_p = $(children_elt).is(':visible');
        if (children_visible_p) {
            expanded_hdr.fadeOut(250, function() { collapsed_hdr.fadeIn(250); });
            $(children_elt).fadeOut(250, function() { $(diff_elt).fadeIn(250); });
        } else {
            collapsed_hdr.fadeOut(250, function() { expanded_hdr.fadeIn(250); });
            $(diff_elt).fadeOut(250, function() { $(children_elt).fadeIn(250); });
        }
    });
});
