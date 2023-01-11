odoo.define('cgm_base.relational_fields', function (require) {
    "use strict";

    var FormView = require('web.FormView');

    FormView.include({
        _setSubViewLimit: function (attrs) {
            var view = attrs.views && attrs.views[attrs.mode];
            var limit = view && view.arch.attrs.limit && parseInt(view.arch.attrs.limit, 10);
            attrs.limit = limit || attrs.Widget.prototype.limit || 250;
        }
    });
});