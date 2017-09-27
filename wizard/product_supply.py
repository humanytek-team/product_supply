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

from odoo import api, models
import logging
import datetime
_logger = logging.getLogger(__name__)


class ProductSupply(models.TransientModel):
    _name = "product.supply"

    @api.multi
    def confirm(self):
        StockMove = self.env['stock.move']
        stock_moves = StockMove.browse(self._context.get('active_ids'))
        list_prod = []
        list_qty = []
        list_ids = []
        list_brand = []
        for stock_move in stock_moves:
            band = False
            reserved_qty = stock_move.reserved_availability
            stock_move.action_assign()
            reserved_qty_after = stock_move.reserved_availability
            _logger.info(reserved_qty_after)
            #_logger.info(a)
            cont = 0
            for l in list_prod:
                #prod, qty = l
                if stock_move.product_id.id == l.id:
                    list_qty[cont] = list_qty[cont] + reserved_qty_after - reserved_qty
                    band = True
                    break
            if not band:
                list_ids.append(stock_move.product_id.id)
                list_prod.append(stock_move.product_id.name)
                list_brand.append(stock_move.product_id.product_brand_id.name)
                list_qty.append(reserved_qty_after - reserved_qty)

        data = dict()
        extra_data = dict()
        #data['ids'] = []
        data['ids'] = list_ids
        extra_data['date'] = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        extra_data['origin'] = stock_moves[0].location_id.name
        extra_data['dest'] = stock_moves[0].location_dest_id.name
        #data['list_prod'] = list_prod
        list_end = []
        cont = 0
        for l in list_prod:
            tup = (l, list_brand[cont], list_qty[cont])
            list_end.append(tup)
        extra_data['list_pro'] = list_end
        _logger.info(extra_data['list_pro'])
        _logger.info('lllllllllllpppppppppppppppppppps')
        extra_data['list_pro'].sort(key=lambda tup: tup[1])
        _logger.info(extra_data['list_pro'])
        #extra_data['list_qty'] = list_qty
        data['extra_data'] = extra_data
        Report = self.env['report']
        return Report.get_action(
            self,
            'product_supply.report_supply', data=data)


