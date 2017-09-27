# -*- coding: utf-8 -*-
###############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2017 Humanytek (<www.humanytek.com>).
#    Rubén Bravo <rubenred18@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from datetime import datetime
from pytz import timezone
from odoo import api, models
import logging
_logger = logging.getLogger(__name__)


class ProductSupply(models.AbstractModel):
    _name = 'report.product_supply.report_supply'

    @api.model
    def render_html(self, docids, data=None):
        _logger.info('DCCCCCCCCCCCDDDDDDDDDDDDDCCCCCCCCCCCCCCCCCDDDDDDDDDDDD')
        docids = data['ids']
        Report = self.env['report']
        StockMove = self.env['stock.move']
        report = Report._get_report_from_name(
            'product_supply.report_supply')
        docs = StockMove.browse(docids)
        #tz = self.env.context.get('tz', False)
        #if not tz:
            #tz = 'US/Arizona'
        datetime_now = datetime.now()
        data['extra_data'].update({
            'datetime': datetime_now.strftime('%d/%m/%y %H:%M:%S'), })
        docargs = {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': docs,
            'data': data['extra_data'],
        }

        return Report.render('product_supply.report_supply', docargs)
