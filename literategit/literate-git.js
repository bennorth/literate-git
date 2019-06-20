// Copyright (C) 2016 Ben North
//
// This file is part of literate-git tools --- render a literate git repository
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

$(document).ready(function() {
    var sections = [];
    $('div.content > div.literate-git-node').each(function(i, e) {
        sections.push({idx: i, elt: e});
    });

    var first_section = $(sections[0].elt);
    first_section.children('.nav.prev').remove();

    var last_section = $(sections[sections.length - 1].elt);
    last_section.children('.nav.next').remove();

    var current_section_idx = 0;
    first_section.show();

    function change_section(d_idx) {
        $(sections[current_section_idx].elt).hide();
        current_section_idx += d_idx;
        $(sections[current_section_idx].elt).show();
    }

    function next_section() { change_section(+1); }
    function prev_section() { change_section(-1); }

    $('.literate-git-node > .nav.next').click(next_section);
    $('.literate-git-node > .nav.prev').click(prev_section);

    $('.diff-or-children > .nav').click(function(e) {
        var button = $(e.target);
        var node_elt = $(e.target).parents('.literate-git-node')[0];
        var expanded_hdr = $(node_elt).find('.nav.collapse:first');
        var collapsed_hdr = $(node_elt).find('.nav.expand:first');
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

    $(document).keypress(function(e) {
        if (e.which == 108) {
            if (current_section_idx < sections.length - 1)
                next_section();
        }
        else if (e.which == 104) {
            if (current_section_idx > 0)
                prev_section();
        }
    });
});
